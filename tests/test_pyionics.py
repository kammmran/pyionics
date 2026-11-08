"""Offline tests for pyionics. Network calls to ILThermo are mocked."""
import csv
import json

import pytest

import pyionics as pyi
from pyionics import base


SAMPLE_SET = {
    "ref": {"full": "Smith, J.; Doe, A. J. Chem. Eng. Data 2020"},
    "dhead": [["Temperature, K"], ["Pressure, kPa"], ["Specific density, kg/m<SUP>3</SUP>"]],
    "data": [[[298.15], [101.325], [1200.5, 0.5]], [[308.15], [101.325], [1193.1, 0.5]]],
    "components": [{"idout": "AAAomx", "name": "helium", "formula": "He"}],
}


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload
        self.content = json.dumps(payload).encode()

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


@pytest.fixture
def workdir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


def write_set(workdir, folder="dens_pure_data", setid="abc"):
    d = workdir / "data" / folder
    d.mkdir(parents=True, exist_ok=True)
    (d / f"idset_{setid}.json").write_text(json.dumps(SAMPLE_SET), encoding="utf-8")
    return d


def test_public_api():
    for name in ["getIdsets", "getData", "convert2csv", "convert2tsv", "addSmiles", "mergeFiles"]:
        assert callable(getattr(pyi, name))


def test_getidsets_requires_a_parameter(workdir):
    with pytest.raises(ValueError):
        pyi.getIdsets()


def test_getidsets_rejects_unknown_property(workdir):
    with pytest.raises(ValueError, match="not found"):
        pyi.getIdsets(prop="not-a-property")


def test_getidsets_builds_url_and_saves_json(workdir, monkeypatch):
    calls = []

    def fake_get(url):
        calls.append(url)
        return FakeResponse({"res": [["set1"], ["set2"]]})

    monkeypatch.setattr(base.requests, "get", fake_get)
    path = pyi.getIdsets(prop="dens", ncmp="1")

    assert "prp=JkYu" in calls[0]  # density property id
    assert "ncmp=1" in calls[0]
    assert path.endswith("dens_idsets_ncmp_pure.json")
    assert json.load(open(path))["res"] == [["set1"], ["set2"]]


def test_getdata_downloads_every_set(workdir, monkeypatch):
    def fake_get(url):
        if "ilsearch" in url:
            return FakeResponse({"res": [["s1"], ["s2"]]})
        return FakeResponse(dict(SAMPLE_SET))

    monkeypatch.setattr(base.requests, "get", fake_get)
    pyi.getData(prop="dens", ncmp="1")

    out = workdir / "data" / "dens_pure_data"
    assert sorted(p.name for p in out.iterdir()) == ["idset_s1.json", "idset_s2.json"]


def test_convert2csv(workdir):
    write_set(workdir)
    pyi.convert2csv("dens_pure_data")

    rows = read_csv(workdir / "data" / "csv_dens_pure_data" / "idset_abc.csv")
    header, first = rows[0], rows[1]
    assert header[:2] == ["idset", "author"]
    assert header[-3:] == ["component 1 idout", "component 1 name", "component 1 formula"]
    assert first[0] == "abc"
    assert first[1] == "Smith et al."
    assert first[2] == "298.15"
    assert first[4] == "1200.5;0.5"
    assert len(rows) == 3


def test_convert2tsv(workdir):
    write_set(workdir)
    pyi.convert2tsv("dens_pure_data")

    out = workdir / "data" / "tsv_dens_pure_data" / "idset_abc.tsv"
    lines = out.read_text(encoding="utf-8").splitlines()
    header = lines[0].split("\t")
    # Unlike CSV, TSV output has no idset/author columns (current behaviour).
    assert header[0] == "Temperature, K"
    assert header[-1] == "component 1 formula"
    assert len(lines) == 3


def test_addsmiles_replaces_formula(workdir):
    write_set(workdir)
    pyi.convert2csv("dens_pure_data")
    pyi.addSmiles("csv_dens_pure_data")

    rows = read_csv(workdir / "data" / "smiles_csv_dens_pure_data" / "idset_abc.csv")
    assert rows[0][-1] == "component 1 SMILES"
    assert rows[1][-1] == "[He]"


def test_mergefiles(workdir):
    write_set(workdir, setid="a")
    write_set(workdir, setid="b")
    pyi.convert2csv("dens_pure_data")
    pyi.mergeFiles("csv_dens_pure_data")

    rows = read_csv(workdir / "data" / "merged_csv_dens_pure_data.csv")
    assert len(rows) == 1 + 4  # header + 2 rows from each of 2 sets
    assert {r[0] for r in rows[1:]} == {"a", "b"}

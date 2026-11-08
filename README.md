# pyionics

[![PyPI](https://img.shields.io/pypi/v/pyionics?color=3775A9)](https://pypi.org/project/pyionics/)
[![tests](https://github.com/kammmran/pyionics/actions/workflows/tests.yml/badge.svg)](https://github.com/kammmran/pyionics/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Download ionic liquid property data from [NIST ILThermo](https://ilthermo.boulder.nist.gov/) and turn it into clean, analysis-ready CSV files with SMILES, in a few lines of Python.

- Search ILThermo by property, compound, number of components, year, author or keyword
- Download every matching dataset at once
- Convert the raw JSON to CSV or TSV
- Add SMILES for each component
- Merge many datasets into one table

## Install

```bash
pip install pyionics
```

## Quick start

Get all density measurements of pure ionic liquids as one CSV file:

```python
import pyionics as pyi

pyi.getData(prop="dens", ncmp="1")         # -> data/dens_pure_data/*.json
pyi.convert2csv("dens_pure_data")          # -> data/csv_dens_pure_data/*.csv
pyi.addSmiles("csv_dens_pure_data")        # -> data/smiles_csv_dens_pure_data/*.csv
pyi.mergeFiles("smiles_csv_dens_pure_data")  # -> data/merged_smiles_csv_dens_pure_data.csv
```

All files are written to a `data/` folder in your working directory. Folder names are passed relative to `data/`.

## API

### `getIdsets(prop, cmp, ncmp, year, auth, keyw)`

Searches ILThermo and saves the list of matching dataset IDs as JSON in `data/`.

| Parameter | Meaning | Example |
|---|---|---|
| `prop` | Property short name (see [Properties](#properties)) | `"dens"` |
| `cmp` | Compound name | `"benzene"` |
| `ncmp` | Number of components: `"0"` all, `"1"` pure, `"2"` binary, `"3"` ternary | `"1"` |
| `year` | Publication year | `"2020"` |
| `auth` | Author name | `"Smith"` |
| `keyw` | Keyword | `"ionic"` |

At least one search parameter is required.

### `getData(...)`

Takes the same parameters as `getIdsets`. Downloads every matching dataset as JSON into `data/{prop}_{ncmp}_data[_filters]/`.

### `convert2csv(folder_name="", file_name="")` / `convert2tsv(...)`

Converts downloaded JSON files to CSV (`data/csv_<folder>/`) or TSV (`data/tsv_<folder>/`). Pass a folder or a single file.

### `addSmiles(folder_name="", file_name="")`

Adds SMILES for each component to CSV files and writes them to `data/smiles_<folder>/`. Works on CSV output only.

### `mergeFiles(folder_name)`

Concatenates all CSV files in a folder into `data/merged_<folder>.csv`.

## Properties

Use the short name as `prop`. Names follow [pyILT2](http://wgserve.de/pyilt2/props.html).

<details>
<summary>Show all 55 properties</summary>

| Property Name                                               | ID    | Short  |
|-------------------------------------------------------------|-------|--------|
| activity                                                    | BPpY  | a      |
| osmotic-coefficient                                         | VjHv  | phi    |
| composition-at-phase-equilibrium                            | dNip  | Xpeq   |
| eutectic-composition                                        | MbEq  | Xeut   |
| henrys-law-constant                                         | lIUh  | Hc     |
| ostwald-coefficient                                         | eCTp  | L      |
| tieline                                                     | neae  | tline  |
| upper-consolute-composition                                 | WbZo  | Xucon  |
| critical-pressure                                           | BPNz  | Pc     |
| critical-temperature                                        | rDNz  | Tc     |
| lower-consolute-temperature                                 | qpSz  |        |
| upper-consolute-pressure                                    | MvMG  | Pucon  |
| upper-consolute-temperature                                 | bRXE  | Tucon  |
| apparent-enthalpy                                           | cpbY  | Hap    |
| apparent-molar-heat-capacity                                | teHk  | capm   |
| enthalpy-of-dilution                                        | rTYh  | Hdil   |
| enthalpy-of-mixing-of-a-binary-solvent-with-component       | aeiA  | Hmix   |
| enthalpy-of-solution                                        | VTiT  |        |
| excess-enthalpy                                             | brzp  | Hex    |
| partial-molar-enthalpy                                      | Sqxi  | Hpm    |
| partial-molar-heat-capacity                                 | mFmK  |        |
| enthalpy                                                    | tnYd  | H      |
| enthalpy-function                                           | kthO  | HvT    |
| entropy                                                     | qdUt  | S      |
| heat-capacity-at-constant-pressure                          | IZSt  | cp     |
| heat-capacity-at-constant-volume                            | KvgF  | cv     |
| heat-capacity-at-vapor-saturation-pressure                  | zJIE  | cpe    |
| enthalpy-of-transition-or-fusion                            | CXUw  | Hfus   |
| enthalpy-of-vaporization-or-sublimation                     | iaOF  | Hvap   |
| equilibrium-pressure                                        | SwyC  | Peq    |
| equilibrium-temperature                                     | ghKa  | Teq    |
| eutectic-temperature                                        | lnrs  | Teut   |
| monotectic-temperature                                      | LUaF  | Tmot   |
| normal-melting-temperature                                  | NmYB  | Tm     |
| interfacial-tension                                         | YQDr  | s      |
| refractive-index                                            | bNnk  | n      |
| relative-permittivity                                       | imdq  | rperm  |
| speed-of-sound                                              | NlQd  | sos    |
| surface-tension-liquid-gas                                  | ETUw  | slg    |
| binary-diffusion-coefficient                                | HooV  |        |
| electrical-conductivity                                     | Ylwl  | econd  |
| self-diffusion-coefficient                                  | jjnq  | Dself  |
| thermal-conductivity                                        | pAFI  | Tcond  |
| thermal-diffusivity                                         | KTcm  | Dterm  |
| tracer-diffusion-coefficient                                | vBeU  | Dtrac  |
| viscosity                                                   | PusA  | visc   |
| normal-boiling-temperature                                  | hkog  | Tb     |
| vapor-or-sublimation-pressure                               | HwfJ  |        |
| adiabatic-compressibility                                   | WxCH  | kS     |
| apparent-molar-volume                                       | zNjL  | Vapm   |
| density                                                     | JkYu  | dens   |
| excess-volume                                               | psRu  | Vex    |
| isobaric-coefficient-of-volume-expansion                    | hXfd  | aV     |
| isothermal-compressibility                                  | Bvon  | kT     |
| partial-molar-volume                                        | LNxL  | Vpm    |

</details>

## Contributing

Bug reports and pull requests are welcome in [Issues](https://github.com/kammmran/pyionics/issues).
If pyionics helps your research, a ⭐ on the repo helps others find it.

## Citation

If you use pyionics in your research, please cite it. Click **"Cite this repository"** in the sidebar on GitHub for APA and BibTeX, or see [`CITATION.cff`](CITATION.cff).

## License

[MIT](LICENSE). Data comes from NIST ILThermo; please cite ILThermo when you publish results based on it.

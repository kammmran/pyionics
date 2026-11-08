from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyionics',
    version='0.4.3',
    author='Kamran Heydarov',
    description='Download NIST ILThermo ionic liquid data and convert it to clean CSV/TSV with SMILES',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kammmran/pyionics',
    project_urls={
        'Source': 'https://github.com/kammmran/pyionics',
        'Issues': 'https://github.com/kammmran/pyionics/issues',
    },
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'requests>=2.25.0,<3.0.0',
        'pandas>=1.3.0,<3.0.0',
        'tqdm>=4.60.0,<5.0.0',
    ],
    keywords=['ionic liquids', 'ILThermo', 'NIST', 'cheminformatics', 'QSPR', 'dataset'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
)

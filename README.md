> :warning: This repository is for illustrative purposes only! The code here shows how one might test a libTokaMap data source but the one being used will not work unless you have data access to MAST-Upgrade (running on UKAEA machines or using a VPN).

# Demo steps

## Building library tester

```bash
g++ -std=c++17 test_library.cpp -o test_library
```

## Fetching uda data source

Download library from:
https://github.com/stephen-dixon/libtokamap-uda-datasource/actions/runs/23138463364

Use `./test_library` to try to load file

Fix security issue at "System Settings" > "Privacy & Security"

Use `./test_library` again

## New virtual environment

```bash
python3 -m venv venv
. ./venv/bin/activate
pip install --upgrade pip
```

## Install libtokamap

```bash
pip install libtokamap

python -c 'import libtokamap; print(libtokamap.__version__)'
```

## Running example with C++ data source

```bash
cd mast_mapping_cxx_data_source
python uda_mapper.py
```

## Running example with Python data source

```bash
pip install pyuda
cd mast_mapping_py_data_source
python pyuda_mapper.py
```

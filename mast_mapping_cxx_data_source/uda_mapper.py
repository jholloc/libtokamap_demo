from pathlib import Path
from typing import Any, override
import numpy as np
import json
import libtokamap


def map(mapper: libtokamap.Mapper, mapping: str, signal: str):
    res = mapper.map(mapping, signal, {'shot': 45272})
    if res.dtype == 'S1':
        res = res.tobytes().decode()
    print(f"{signal}: {res}")
    return res


def map_all(mapper: libtokamap.Mapper, mapping: str):
    map(mapper, mapping, "magnetics/ip/data")


def main(args):
    if len(args) == 2:
        if args[1] == "--help":
            print(f"Usage: python {args[0]}")
            sys.exit(0)
        else:
            print(f"Usage: python {args[0]}")
            sys.exit(1)

    print("Calling LibTokaMap version:", libtokamap.__version__)

    config_path = "/Users/jhollocombe/Projects/demo_mappings/mast_mapping_cxx_data_source/config.toml"
    mapper = libtokamap.Mapper(config_path)

    mapping = "mastu"
    try:
        map_all(mapper, mapping)
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    import sys
    main(sys.argv)

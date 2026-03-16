from pathlib import Path
from typing import Any, override
import numpy as np
import json
import libtokamap
import argparse


def map(mapper: libtokamap.Mapper, experiment: str, mapping_path: str, shot: int):
    res = mapper.map(experiment, mapping_path, {'shot': shot})
    if res.dtype == 'S1':
        res = res.tobytes().decode()
    print(f"{mapping_path}: {res}")
    return res


def map_all(mapper: libtokamap.Mapper, experiment: str, shot: int):
    map(mapper, experiment, "magnetics/ip/data", shot)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--shot', type=int, default=45272)
    args = parser.parse_args(args[1:])

    print("Calling LibTokaMap version:", libtokamap.__version__)
    print(f"With context = {vars(args)}")

    config_path = Path(__file__).parent / "config.toml"
    mapper = libtokamap.Mapper(str(config_path))

    experiment = "mastu"
    try:
        map_all(mapper, experiment, args.shot)
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    import sys
    main(sys.argv)

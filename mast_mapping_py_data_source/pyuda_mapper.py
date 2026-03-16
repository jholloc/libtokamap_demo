from pathlib import Path
from typing import Any, override
import numpy as np
import json
import libtokamap
import pyuda
import argparse

class UDADataSource(libtokamap.DataSource):
    def __init__(self, host: str, port: int, plugin_name: str, function: str = "get"):
        self.host = host
        self.port = port
        self.plugin_name = plugin_name
        self.function = function

        pyuda.Client.server = host
        pyuda.Client.port = port
        self.client = pyuda.Client()

    @override
    def get(self, args: dict[str, str]) -> np.ndarray:
        if 'signal' not in args:
            raise ValueError("signal is required")
        if 'source' not in args:
            raise ValueError("source is required")
        if 'host' not in args:
            raise ValueError("host is required")
        if 'port' not in args:
            raise ValueError("port is required")

        plugin_args = [f'{k}={v}' for (k, v) in args.items()]
        request = f'{self.plugin_name}::{self.function}({",".join(plugin_args)})'

        print(f'request = {request}')
        result = self.client.get(request, '')

        return result.data

def map(mapper: libtokamap.Mapper, experiment: str, mapping_path: str, shot: int):
    res = mapper.map(experiment, mapping_path, {'shot': shot})
    if res.dtype == 'S1':
        res = res.tobytes().decode()
    print(f"{mapping_path}: {res}")
    return res


def map_all(mapper: libtokamap.Mapper, experiment: str, shot: int):
    map(mapper, experiment, "magnetics/ip/data", shot)
    map(mapper, experiment, "magnetics/flux_loop[0]/flux/data", shot)
    map(mapper, experiment, "magnetics/flux_loop[1]/flux/data", shot)
    map(mapper, experiment, "magnetics/flux_loop[2]/flux/data", shot)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--shot', type=int, default=45272)
    args = parser.parse_args(args[1:])

    print("Calling LibTokaMap version:", libtokamap.__version__)
    print(f"With context = {vars(args)}")

    config_path = Path(__file__).parent / "config.toml"
    mapper = libtokamap.Mapper(str(config_path))
    mapper.register_python_data_source("UDA", UDADataSource("uda2.hpc.l", 59876, "UDA"))

    experiment = "mastu"
    try:
        map_all(mapper, experiment, args.shot)
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    import sys
    main(sys.argv)

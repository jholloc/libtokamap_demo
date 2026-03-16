from pathlib import Path
from typing import Any, override
import numpy as np
import json
import libtokamap
import pyuda

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

    config_path = "/Users/jhollocombe/Projects/demo_mappings/mast_mapping_py_data_source/config.toml"
    mapper = libtokamap.Mapper(config_path)
    mapper.register_python_data_source("UDA", UDADataSource("uda2.hpc.l", 59876, "UDA"))

    mapping = "mastu"
    try:
        map_all(mapper, mapping)
    except Exception as e:
        print(f"{e}")


if __name__ == "__main__":
    import sys
    main(sys.argv)

import os
import sys

import base58
import dns.resolver


CHUNK_SIZE = 32


if __name__ == "__main__":
    filepath = sys.argv[1]
    encoded_filepath = base58.b58encode(filepath).decode('ascii')
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [
        os.environ["TRANSFER_IO_NAMESERVER"],
    ]
    resolver.nameserver_ports = {
        os.environ["TRANSFER_IO_NAMESERVER"]: int(os.environ["TRANSFER_IO_NAMESERVER_PORT"]),
    }
    with open(filepath, "rb") as f:
        while True:
            data = f.read(CHUNK_SIZE)
            if not data:
                break
            encoded_data = base58.b58encode(data).decode('ascii')
            lookup_hostname = f"{encoded_filepath}.{encoded_data}.transfer.io"
            resolver.resolve(lookup_hostname, "TXT")

import os
import datetime

from dnslib.server import DNSServer, DNSLogger
from dnslib.dns import RR
from dnslib import QTYPE

import base58


TRANSFER_HOSTNAME = ".transfer.io"
PORT = 8053
OUTPUT_DIRECTORY = "/data"

class TransferResolver:
    def resolve(self, request, handler):
        qname = str(request.q.qname)
        reply = request.reply()
        if request.q.qtype != QTYPE.TXT:
            return reply
        if qname.endswith(f"{TRANSFER_HOSTNAME}."):
            encoded_filepath, encoded_chunk = qname.replace(f"{TRANSFER_HOSTNAME}.", "").split(".")
            decoded_filepath = base58.b58decode(encoded_filepath)
            print(f"received chunk for file: {decoded_filepath}")
            output_filepath = os.path.join(OUTPUT_DIRECTORY, encoded_filepath)
            with open(output_filepath, "ab") as f:
                decoded_chunk = base58.b58decode(encoded_chunk)
                f.write(decoded_chunk)
                reply.add_answer(*RR.fromZone(f"{qname} 1 TXT OK"))
        return reply


if __name__ == "__main__":
    resolver = TransferResolver()
    logger = DNSLogger(prefix=False)
    logger = None
    server = DNSServer(resolver, logger=logger, address="0.0.0.0", port=PORT)
    print("starting DNS server!")
    server.start()

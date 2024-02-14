'''
Copyright (c) 2020 Idena
Distributed under the MIT software license, see the accompanying   
file COPYING or http://www.opensource.org/licenses/mit-license.php.
'''

import utils.proto_file as proto_file
from binascii import unhexlify

class BurnAttachment:
    def __init__(self, key):
        self.key = key

    @classmethod
    def from_hex(cls, hex_string):
        return cls(
            proto_file.ProtoBurnAttachment.FromString(unhexlify(hex_string)).key
        )

    def to_hex(self):
        data = proto_file.ProtoBurnAttachment()
        data.key = self.key

        return data.SerializeToString().hex()
    

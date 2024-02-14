'''
Copyright (c) 2020 Idena
Distributed under the MIT software license, see the accompanying   
file COPYING or http://www.opensource.org/licenses/mit-license.php.
'''

import utils.proto_file as proto_file
from binascii import hexlify, unhexlify  # For hex conversions

class Profile:
    def __init__(self, ads=None):
        self.ads = ads or []

    @staticmethod
    def from_bytes(bytes):
        proto_profile = proto_file.ProtoProfile.FromString(bytes)
        ads_list = [Profile.to_dict(ad) for ad in proto_profile.ads]
        return Profile(ads=ads_list)

    @staticmethod
    def from_hex(hex_string):
        return Profile.from_bytes(unhexlify(hex_string))

    def to_bytes(self):
        proto_profile = proto_file.ProtoProfile()

        for ad in self.ads:
            profile_ad = proto_profile.ads.add()
            profile_ad.cid = ad['cid']
            profile_ad.target = ad['target']
            profile_ad.contract = ad['contract']
            profile_ad.author = ad['author']

        return proto_profile.SerializeToString()

    def to_hex(self):
        return hexlify(self.to_bytes()).decode('utf-8')
    
    def to_dict(ad):
        return {
        'cid': ad.cid,
        'target': ad.target,
        'contract': ad.contract,
        'author': ad.author
    }
    

class ProfileAd:
    def __init__(self, cid, key, voting_address):
        self.cid = cid
        self.key = key
        self.voting_address = voting_address

    def to_bytes(self):
        data = proto_file.ProtoProfile.ProtoProfileAd()
        data.cid = self.cid
        data.key = self.key
        data.votingaddress = self.voting_address

        return data.SerializeToString()

    def to_hex(self):
        return hexlify(self.to_bytes()).decode('utf-8')

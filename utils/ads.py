'''
Copyright (c) 2020 Idena
Distributed under the MIT software license, see the accompanying   
file COPYING or http://www.opensource.org/licenses/mit-license.php.
'''

import utils.proto_file as proto_file
from binascii import unhexlify
from io import BytesIO

class AdBurnKey:
    def __init__(self, cid=None, target=None):
        self.cid = cid
        self.target = target

    @staticmethod
    def from_hex(hex_string):
        try:
            # Decode hex string into bytes
            decoded_bytes = bytes.fromhex(hex_string)
            
            # Parse ProtoAdBurnKey message
            proto_ad_burn_key = proto_file.ProtoAdBurnKey()
            proto_ad_burn_key.ParseFromString(decoded_bytes)
            
            # Create AdBurnKey instance from parsed message
            return AdBurnKey(proto_ad_burn_key.cid, proto_ad_burn_key.target)
        except Exception as e:
            print(f"Error decoding hex: {e}")
            return AdBurnKey()

    def to_hex(self):
        # Create ProtoAdBurnKey message
        proto_ad_burn_key = proto_file.ProtoAdBurnKey()
        proto_ad_burn_key.cid = self.cid
        proto_ad_burn_key.target = self.target
        
        # Serialize message to bytes
        serialized_bytes = proto_ad_burn_key.SerializeToString()
        
        # Convert bytes to hex string
        hex_string = serialized_bytes.hex()
        return hex_string

class AdTarget:
    def __init__(self, language, age, os, stake):
        self.language = language
        self.age = age
        self.os = os
        self.stake = stake

    @staticmethod
    def from_bytes(bytes):
        proto_ad_key = proto_file.ProtoAdTarget.FromString(bytes)
        return AdTarget(proto_ad_key.language, proto_ad_key.age, proto_ad_key.os, proto_ad_key.stake)

    @staticmethod
    def from_hex(hex_string):
        return AdTarget.from_bytes(bytes.fromhex(hex_string))

    def to_bytes(self):
        data = proto_file.ProtoAdTarget()
        data.language = self.language
        data.age = self.age
        data.os = self.os
        data.stake = self.stake
        return data.SerializeToString()

    def to_hex(self):
        return self.to_bytes().hex()
    
class Ad:
    def __init__(self, title, desc, url, thumb, media, version, voting_params):
        self.title = title
        self.desc = desc
        self.url = url
        self.thumb = thumb
        self.media = media
        self.version = version
        self.voting_params = voting_params

    @classmethod
    def from_bytes(cls, bytes_data):
        proto_ad = proto_file.ProtoAd.FromString(bytes_data)

        thumb = proto_ad.thumb
        media = proto_ad.media
        voting_params = proto_ad.votingParams

        return cls(
            title=proto_ad.title,
            desc=proto_ad.desc,
            url=proto_ad.url,
            thumb=BytesIO(thumb) if thumb else None,
            media=BytesIO(media) if media else None,
            version=proto_ad.version,
            voting_params={
                'votingDuration': voting_params.votingDuration,
                'publicVotingDuration': voting_params.publicVotingDuration,
                'quorum': voting_params.quorum,
                'committeeSize': voting_params.committeeSize,
            }
        )

    @classmethod
    def from_hex(cls, hex_data):
        return cls.from_bytes(unhexlify(hex_data))

    def to_hex(self):
        return self.to_bytes().hex()
    
# other utilities
    
def competing_targets(target1, target2):
    if target1["language"] != '' and target1["os"] != '':
        if ((target1["language"] == target2["language"] or target2["language"] == '')
            and  (target1["os"] == target2["os"] or target2["os"] == '')):
                return 1
    elif target1["language"] != '' and target1["os"] == '':
        if (target1["language"] == target2["language"] or target2["language"] == ''):
            return 1
    elif target1["language"] == '' and target1["os"] != '':
        if (target1["os"] == target2["os"] or target2["os"] == ''):
            return 1
    elif target1["language"] == '' and target1["os"] == '':
        # if no language/os is set, ad will overtake other ads that have them set
        return 1
    return 0

def ad_sorting_key(ad):
    targets = AdTarget.from_hex(ad["target"]).__dict__
    score = 1
    lang_score_modifier = {'en': 2, 'ru': 1}
    
    if targets["language"] != '':
        score *= 22
    if targets["os"] != '':
        score *= 5
    if targets["language"] in lang_score_modifier:
        score -= lang_score_modifier[targets["language"]]
    return score

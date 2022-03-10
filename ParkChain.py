# GENERAL FEATURES:

# every 12 blocks ParkChain ages by 1
# every time nonce goes above 200k difficulty goes down by 1
# every time nonce goes below 1k difficulty goes up by 1


import datetime
import hashlib
import json


class ParkChain:
    def __init__(self):
        self.age = 0
        self.version = 1
        self.difficulty = 4
        self.timestamp = str(datetime.datetime.now())
        self.previous_hash = "start!"
        self.content = "to trzeba usiasc na spokojnie"

        self.chain = []

        # mine the first block on init
        self.mine_block(self.previous_hash, self.content)

    def mine_block(self, previous_hash, content=""):
        # create a timestamp
        timestamp = str(datetime.datetime.now())

        h_version = hashlib.sha256(str(self.version).encode()).hexdigest()
        h_difficulty = hashlib.sha256(
            str(self.difficulty).encode()
            ).hexdigest()
        h_timestamp = hashlib.sha256(str(timestamp).encode()).hexdigest()
        h_content = hashlib.sha256(content.encode()).hexdigest()

        # header without the nonce (all concatenated and hashed)
        header = hashlib.sha256(
            (
                f"{previous_hash}\
                {h_timestamp}\
                {h_version}\
                {h_difficulty}\
                {h_content}"
            ).encode()
        ).hexdigest()

        # proof of work (finding a nonce)
        nonce = 1
        found_nonce = False

        while found_nonce is False:
            test_hash = hashlib.sha256(
                str(nonce).encode() + header.encode()
            ).hexdigest()
            if test_hash[: self.difficulty] == self.difficulty * "0":
                found_nonce = True
            else:
                nonce += 1

        # new block data
        new_block = {
            "number": len(self.chain),
            "age": self.age,
            "version": self.version,
            "difficulty": self.difficulty,
            "timestamp": timestamp,
            "previous_hash": previous_hash,
            "content": content,
            "nonce": nonce,
        }

        # adjust the parameters
        if new_block["number"] % 12 == 0:
            self.age += 1
        if new_block["nonce"] > 200000:
            self.difficulty -= 1
        if new_block["nonce"] < 1000:
            self.difficulty += 1

        # append it to the chain
        self.chain.append(new_block)

        return new_block

    def get_previous_block(self):
        previous_block = self.chain[-1]

        return previous_block

    def get_previous_hash(self):
        previous_block = self.get_previous_block()

        previous_block_encoded = json.dumps(
            previous_block, sort_keys=True
            ).encode()
        previous_block_hash = hashlib.sha256(
            previous_block_encoded
            ).hexdigest()

        return previous_block_hash

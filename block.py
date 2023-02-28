from time import time
from printable import Printable

class Block(Printable):
    def __init__(b, index, previous_hash, transctions, proof, timestamp=None):
        b.index = index
        b.previous_hash = previous_hash
        b.timestamp = time() if timestamp is None else timestamp
        b.transactions = transctions
        b.proof = proof

    # def __repr__(b):
    #     return 'Index: {}, Previous Hash: {}, Proof: {}, Transactions: {}'.format(b.index, b.previous_hash, b.proof, b.transactions)
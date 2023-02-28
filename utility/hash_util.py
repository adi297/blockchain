import hashlib as hl
import json

# The __all__ list or the single-underscore (e.g. _hl) can be used to control exports under the import * method
# The __all__ list can contain included imports and the underscore syntax is used to exclude exports
# __all__ = ['hash_string_256', 'hash_block']

def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hl.sha256(json.dumps(hashable_block, sort_keys=True).encode()).hexdigest()
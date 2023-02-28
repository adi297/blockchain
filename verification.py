from hash_util import hash_string_256, hash_block

class Verification:

    # Decorators alter the functionality of class methods
    # @staticmethod is used to make the class have a container-like role for the method (no self attributes can be passed to the method, only external ones)
    # @classmethod is used make a method directly callable as a class property without having to instantiate the class.

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        # guess = (str(transactions) + str(last_hash) + str(proof)).encode()
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        # print(guess)
        # guess_hash = hl.sha256(guess).hexdigest()
        guess_hash = hash_string_256(guess)

        # print(guess_hash)
        return guess_hash[0:2] == '00'
    

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it's valid, False otherwise."""
        for (index, block) in enumerate(blockchain):
        # for block in blockchain:
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        
        return True



    @staticmethod
    def verify_transaction(transaction, get_balance):
        """Verify a transaction by checking whether the sender has sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        sender_balance = get_balance()
        return sender_balance >= transaction.amount
    

    
    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """Verifies all open transactions."""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])

    
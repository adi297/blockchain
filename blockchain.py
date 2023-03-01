from functools import reduce
import hashlib as hl
import json
import pickle
# from collections import OrderedDict
from utility.hash_util import hash_block

from block import Block
from transaction import Transaction
from utility.verification import Verification
from wallet import Wallet

# The reward we give to miners (for creating a new block)
MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id):
        # Our starting block for the blockchain
        genesis_block = Block('', 0, [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id


    @property
    def chain(self):
        return self.__chain[:]

    # def get_chain(self):
    #     return self.__chain[:]
    
    @chain.setter
    def chain(self, val):
        self.__chain = val


    def get_open_transactions(self):
        return self.__open_transactions
    
# Our starting block for the blockchain
# Initialized in load_data() IOError except statement
# genesis_block = {
#     'previous_hash': '',
#     'index': 0,
#     'transactions': [],
#     'proof': 100
# }
# Initializing our (empty) blockchain list
# blockchain = [genesis_block]
# blockchain = []
# Unhandled transactions
# open_transactions = []
# We are the owner of this blockchain node, hence this is our identifier (e.g. for sending coins)
# owner = 'Aditya'
# Registered participants: Ourself + other people sending/ receiving coins
# participants = {'Aditya'}


    def load_data(self):
        # global blockchain, open_transactions
        try:
            with open('blockchain.txt', mode='r') as f:
            # with open('blockchain.p', mode='rb') as f:
                file_content = f.readlines()
                # file_content = pickle.loads(f.read())
                print(file_content)
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                
                # Pickling retains OrderedDict structures and other similar code on un-pickling. 
                # Therefore recreating those structures from json strings by de-serializing with json.loads() is not necessary.
                # String content generated by json is preferable for viewing data as text for security/validation purposes.

                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    tx_dict = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    # tx_dict = [OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], tx_dict, block['proof'], timestamp=block['timestamp'])
                    # updated_block = {
                    #     'previous_hash': block['previous_hash'],
                    #     'index': block['index'],
                    #     'proof': block['proof'],
                    #     'transactions': [OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])for tx in block['transactions']]
                    # }
                    updated_blockchain.append(updated_block)
                
                self.chain = updated_blockchain

                # # loads() converts json strings to native python objects (de-serializing). '\n' is not valid json and therefore needs to be removed by using the range selector on the string.
                # # serializing: turning python objects into json/binary strings. (Reverse: de-serializing/un-serializing)

                self.__open_transactions = json.loads(file_content[1])
                updated_open_transactions = []
                for tx in self.__open_transactions:
                    updated_tx = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    # updated_tx = OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                    updated_open_transactions.append(updated_tx)

                self.__open_transactions = updated_open_transactions
        # except (ValueError , IOError):
        except (IOError, IndexError):
            print("File not found.")
            # # Our starting block for the blockchain
            # genesis_block = Block('', 0, [], 100, 0)
            # genesis_block = {
            #     'previous_hash': '',
            #     'index': 0,
            #     'transactions': [],
            #     'proof': 100
            # }
            # Initializing our (empty) blockchain list
            # blockchain = [genesis_block]
            # # Unhandled transactions
            # open_transactions = []
        finally:
            print("Cleanup.")


# load_data()


    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
            # default read/write mode is r/wt (text), whereas r/wb is used for binary files
            # with open('blockchain.p', mode='wb') as f:
                # f.write(str(blockchain))
                # f.write('\n')
                # f.write(str(open_transactions))

                # json.dump(blockchain, f)
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot' : open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print("Saving failed.")





    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # verifier = Verification()
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        """Calculate and return the balance for a participant.

        Arguments:
            :participant: The person for whom to calculate the balance.
        """
        participant = self.hosting_node
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of transactions that were already included in blocks of the blockchain
        tx_sender = [[tx.amount for tx in block.transactions
                    if tx.sender == participant] for block in self.__chain]
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of open transactions (to avoid double spending)
        open_tx_sender = [tx.amount
                        for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                            if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
        tx_recipient = [[tx.amount for tx in block.transactions
                        if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                                if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # Return the total balance
        return amount_received - amount_sent


    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]


    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """
        if self.hosting_node == None:
            return False
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }
        # transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])
        # verifier = Verification()
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            self.save_data()
            return True
        return False


    def mine_block(self):
        """Create a new block and add open transactions to it."""
        if self.hosting_node == None:
            return False
        # Fetch the currently last block of the blockchain
        last_block = self.__chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value)
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # Miners should be rewarded, so let's create a reward transaction
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        # reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        # Copy transaction instead of manipulating the original open_transactions list
        # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return False
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        # block = {
        #     'previous_hash': hashed_block,
        #     'index': len(blockchain),
        #     'transactions': copied_transactions,
        #     'proof': proof
        # }
        self.__chain.append(block)
        print(self.__open_transactions)
        self.__open_transactions = []
        self.save_data()
        return True



print(__name__)




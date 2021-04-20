from Block import Block
import time



class Blockchain:
    def __init__(self):
        self.uncomfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    difficulty = 2
    def proof_of_work(self, block):
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0'*Blockchain.difficulty):
            block.nonce+=1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)

    def is_valid_proof(self, block, block_hash: str):
        return (block_hash.startswith('0' * Blockchain.difficulty)
                and block_hash == block.compute_hash())

    def add_new_transaction(self, transaction):
        self.uncomfirmed_transactions.append(transaction)

    def mine(self):
        if not self.uncomfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(last_block.index+1, self.uncomfirmed_transactions,
                          time.time(), last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.uncomfirmed_transactions = []
        return new_block.index


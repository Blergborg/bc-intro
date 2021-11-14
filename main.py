from BlockChain import Block, Blockchain
from time import time

MeChain = Blockchain()

# Add a new block
MeChain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 100})))
# (this is just a simple example, real blockchains often have some more steps to implement).

# Prints out the updated chain
print(MeChain)
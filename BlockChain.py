from hashlib import sha256
from time import time
import json

class Block:
  def __init__(self, timestamp=None, data=None):
    self.timestamp = timestamp or time()
    # this.data should contain information like transactions.
    self.data = [] if data is None else data
    self.prevHash = None # previous block's hash
    self.nonce = 0
    self.hash = self.getHash()
  
  def getHash(self):
    hash = sha256()
    hash.update(str(self.prevHash).encode('utf-8'))
    hash.update(str(self.timestamp).encode('utf-8'))
    hash.update(str(self.data).encode('utf-8'))
    hash.update(str(self.nonce).encode('utf-8'))
    return hash.hexdigest()

  def mine(self, difficulty):
    # Basically, it loops until our hash starts with
    # the string 0...000 with length of <difficulty>.
    while self.hash[:difficulty] != '0' * difficulty:
      # We increase our nonce so that we can get a whole different hash.
      self.nonce += 1
      # Update our new hash with the new nonce value.
      self.hash = self.getHash()


class Blockchain:
  def __init__(self):
    # This property will contain all the blocks. 
    # Create our genesis block
    self.chain = [Block(str(int(time())))]
    self.difficulty = 1
    self.blockTime = 30000

  def __repr__(self):
    return json.dumps([{
      'data':item.data, 
      'timestamp':item.timestamp, 
      'nonce':item.nonce, 
      'hash': item.hash, 
      'prevHash': item.prevHash
      } for item in self.chain], indent=4)

  # Get latest block
  def getLastBlock(self):
    return self.chain[len(self.chain) - 1]

  # Add new block
  def addBlock(self, block):
    # Since we are adding a new block, prevHash will be the hash of the old latest block
    block.prevHash = self.getLastBlock().hash
    # Since now prevHash has a value, we must reset th block's hash
    block.hash = block.getHash()
    block.mine(self.difficulty)
    self.chain.append(block)

    self.difficulty += (-1, 1)[int(time()) - int(self.getLastBlock().timestamp) < self.blockTime]

  # Validation method
  def isValid(self):
    # Iterate over the chain, we need to set i to 1 b/c there's nothing before the genesis block, so we start at the 2nd block 
    for i in range(1, len(self.chain)):
      currentBlock = self.chain[i]
      prevBlock = self.chain[i - 1]

      # Check validation
      if (currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash):
        return False

    return True
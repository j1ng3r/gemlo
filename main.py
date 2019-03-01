#IP of j1ng3r
import math
import random

class Sequence:
  def __init__(self, seq, thru = ""):
    self.seq = list(seq)
    self.length = len(seq)
    self.thru = thru
    self.tests = []
  
  def _mutateValue(self, index, value):
    return self.seq[0:index] + [value] + self.seq[index+1:]
  
  def mutateValue(self, index, value):
    return Sequence(self._mutateValue(index, value), "mutateValue")
  
  def addTest(self, value):
    self.tests += [value]
    
  def getMean(self):
    sum = 0
    for i in self.tests:
      sum += i
    return sum/len(self.tests)
  
  def getVariance(self):
    if len(self.tests) < 2:
      return math.inf
    sum = 0
    mean = self.getMean()
    for i in self.tests:
      sum += (i-mean)**2
    return sum/(len(self.tests)-1)
  
  def getSTD(self):
    return self.getVariance()**0.5
  
  def getValue(self, optimism = 0):
    return self.getMean() + optimism * self.getSTD()
  
  def getRandomIndex(self):
    return math.floor(random.random() * self.length)
  
class Optimizer:
  seqs = []
  
  def __init__(self, chars, seq_ = []):
    self.chars = chars
    self.seqs = []
    self.seqlength = len(seq_)
    self.addSeq(seq_)
  
  def addSeqs(self, seqs_):
    for seq_ in seqs_:
      self.addSeq(seq_)
  
  def addSeq(self, seq_):
    if len(seq_) == self.seqlength:
      seq = Sequence(seq_)
      self.seqs += [seq]
      return seq
    else:
      raise ValueError(seq_, "does not have the required length", self.seqlength)
    
  def addTest(self, seq, value):
    seq.addTest(value)

  def getRandomFnChar(self, fn):
    R = 0
    i = 0
    while i < self.chars:
      R += fn(i)
      i += 1
    R *= random.random()
    i = 0
    while i < self.chars:
      R -= fn(i)
      if R < 0:
        return i
      i += 1
    return self.chars - 1
  
  def getWeight(self, v):
    return 1
  
  def getRandomWeightedChar(self):
    return self.getRandomFnChar(self.getWeight)
  
  def getAntiweight(self, v):
    return 1 / self.getWeight(v)
  
  def getRandomAntiweightedChar(self):
    return self.getRandomFnChar(self.getAntiweight)
  
  def mutate(self, seq):
    R = 0
    for v in seq.seq:
      R += self.getAntiweight(v)
    R *= random.random()
    i = 0
    for v in seq.seq:
      R -= self.getAntiweight(v)
      if R < 0:
        return seq.mutateValue(i,self.getRandomWeightedChar())
      i += 1
    return seq.mutateValue(seq.length-1,self.getRandomWeightedChar())
  
  def mutateN(self, N, seq):
    i = 0
    while i < N:
      seq = self.mutate(seq)
      i += 1
    return seq
  
  def addMutation(self, seq):
    newSeq = self.mutate(seq)
    while self.seqKnown(newSeq):
      newSeq = self.mutate(seq)
    return self.addSeq(newSeq.seq)
  
  def seqKnown(self, seq):
    for Seq in self.seqs:
      if Seq.seq == seq.seq:
        return True
    return False
  
  def addMutationN(self, N, seq):
    newSeq = self.mutateN(N, seq)
    while self.seqKnown(newSeq):
      newSeq = self.mutateN(N, seq)
    return self.addSeq(newSeq.seq)
    
  def generateNewN(self, N):
    self.addMutationN(N, self.rankBest()[0])
  
  def getSeqValue(self, seq, optimism = 0):
    return seq.getValue(optimism)
  
  def rankBest(self,optimism = 0):
    return sorted(self.seqs, key = lambda seq: self.getSeqValue(seq, optimism), reverse = True)
  
  def recommendBest(self, optimism = 0):
    return self.rankBest(optimism)[0]
  
  def getSeqs(self):
    seqs = []
    for seq in self.seqs:
      seqs += [seq.seq]
    return seqs
  
  def bestInfo(optimism):
    seq = self.recommendBest(optimism)

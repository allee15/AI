# -*- coding: utf-8 -*-
"""Lab1KR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t9YD8ChJbyr2UEonh6RT6xTIto10D8OY
"""

#1 Graf si nod

class Nod:
  def __init__(self, informatie, parinte = None, succesori =None):
    self.informatie = informatie
    self.parinte = parinte
    self.succesori = succesori 

  def __str__(self):
    return str(self.informatie)

  def __repr__(self):
    return "({}, ({}))".format(self.informatie, "->".join([ str(x) for x in self.drumRadacina()]))

  def drumRadacina(self):
    drum =[]
    nod = self
    while nod is not None:
      drum.append(nod)
      nod = nod.parinte
    return reversed(drum)

  def vizitat(self):
    nod = self.parinte
    while nod is not None:
      if nod.informatie == self.informatie:
        return True
      nod = nod.parinte
    return False

class Graf:
  def __init__(self, nodStart, noduriScop = None, matrix = None):
    self.nodStart = nodStart
    self.noduriScop = noduriScop 
    self.matrix = matrix 

  def scop(self, nod):
    return nod in self.noduriScop

  def succesori(self, nod):
    drum = []
    for i in range(len(self.matrix)):
      if self.matrix[nod.informatie][i]==1:
        new = Nod(i, nod, drum)
        if not new.vizitat():
          drum.append(new)
    return drum

#BFS

def BFS(graf, n):
  coada = [Nod(graf.nodStart)]
  while coada:
    nod = coada.pop(0)
    if graf.scop(nod.informatie):
      print(repr(nod))
      n-=1
      if n == 0:
        return
    drum = graf.succesori(nod)
    coada+=drum

#DFS recursiv

def DFS(graf, n):
  stiva = [Nod(graf.nodStart)]
  while stiva:
    nod = stiva.pop()
    if graf.scop(nod.informatie):
      print(repr(nod))
      n-=1
      if n==0:
        return
    drum = graf.succesori(nod)
    stiva+= drum[::-1]

#DFS iterativ

def DFS_iterativ(graf,n):
  stiva = [Nod(graf.nodStart)]
  while stiva and n > 0:
    nod = stiva.pop()
    if graf.scop(nod.informatie):
      print(repr(nod))
      n-=1
    drum = graf.succesori(nod)
    stiva+= drum[::-1]

#pt matricea data ca model in Lab1
matrix= [
    [0, 1, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 0, 0]
]

nodStart = 0
noduriScop = [4,6]
grefa = Graf(nodStart, noduriScop, matrix)

n= int(input("n="))

BFS(grefa,n)

DFS(grefa,n)

DFS_iterativ(grefa,n)
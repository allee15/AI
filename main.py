import copy


class State:
    N = 3
    M = 2

    def __init__(self, misionari=N, canibali=N, barca=-1):
        self.misionari = misionari
        self.canibali = canibali
        self.barca = barca

    def __eq__(self, cls):
        return self.barca == cls.barca and \
            self.misionari == cls.misionari and self.canibali == cls.canibali

    def __str__(self):
        return 'Stare curenta:\n' + \
            f'{str(self.misionari)} misionari, ' + \
            f'{str(self.canibali)} canibali | ' + \
            f'{str(self.N - self.misionari)} misionari, ' + \
            f'{str(self.N - self.canibali)} canibali \n' + \
            f'Barca se afla pe malul {"stang" if self.barca == -1 else "drept"}\n'

    def __repr__(self):
        return ('({} {} {})').format(self.misionari, self.canibali, self.barca)

    def succesori(self):
        succesori = []

        # Calculez cati misionari si canibali sunt pe malul cu barca
        misionari = self.misionari if self.barca == -1 else self.N - self.misionari
        canibali = self.canibali if self.barca == -1 else self.N - self.canibali

        for locuri in range(1, self.M + 1):
            for locuriMisionari in range(misionari + 1):
                if locuriMisionari > locuri:
                    continue

                # Verific sa existe cati canibali vreau sa plimb
                locuriCanibali = locuri - locuriMisionari
                if locuriCanibali < 0 or locuriCanibali > canibali:
                    continue

                # Verific sa nu fie mancati misionari in barca
                if locuriCanibali > locuriMisionari and locuriMisionari > 0:
                    continue

                # Verific sa nu fie mancati misionari pe malul de plecare
                if canibali - locuriCanibali > misionari - locuriMisionari and misionari - locuriMisionari > 0:
                    continue

                # Verific sa nu fie mancati misionari pe malul de sosire
                if (self.N - canibali) + locuriCanibali > (self.N - misionari) + locuriMisionari and (
                        self.N - misionari) + locuriMisionari > 0:
                    continue

                # Trucuri de notatie:
                stareCurenta = State(
                    self.misionari + self.barca * locuriMisionari,
                    self.canibali + self.barca * locuriCanibali,
                    (-1) * self.barca)

                succesori.append(stareCurenta)

        return succesori


# 1
class Node:
    def __init__(self, informatie, parinte=None, g=0, h=0):
        self.informatie = informatie
        self.parinte = parinte
        self.g = g
        self.h = h
        self.f = g + h

    def __str__(self):
        return "{} ({}, {})".format(self.informatie, self.g, self.f)

    def __repr__(self):
        return "({}, ({}), cost:{})".format(self.informatie, "->".join([str(x) for x in self.drumRadacina()]), self.f)

    def __eq__(self, other):
        return self.informatie == other.informatie and self.f == other.f

    def __le__(self, other):
        return self.f <= other.f

    def drumRadacina(self):
        drum = []
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

# 1
# Crearea obiectelor de tip Node
node1 = Node("Informatie1")
node2 = Node("Informatie2")

# Afișarea succesorilor pentru primul nod
print("Succesorii pentru Node1:")
print(node1)

# Afișarea succesorilor pentru al doilea nod
print("Succesorii pentru Node2:")
print(node2)


# 1
class Graph:
    def __init__(self, nodStart, noduriScop):
        self.nodStart = nodStart
        self.noduriScop = noduriScop
        if not self.valideaza():
            print("fisierul dat nu este bun")
            exit(0)

    # 2b
    def valideaza(self):
        if len(self.nodStart) != 3:
            return False
        if any([len(linie) != 3 for linie in self.nodStart]):
            return False
        matrix = sum(self.nodStart, start=[])
        if sorted(matrix) != list(range(9)):
            return False
        inversiuni = 0
        for i, elem in enumerate(matrix):
            for j, elem2 in enumerate(matrix[i + 1:]):
                if elem != 0 and elem2 != 0 and elem > elem2:
                    inversiuni += 1
        return inversiuni % 2 == 0

    # 2a
    def scop(self, nod):
        return nod in self.noduriScop

    def succesori(self, nod):
        l = []
        okay = False
        for iSpatiu in range(3):
            for jSpatiu in range(3):
                if nod.informatie[iSpatiu][jSpatiu] == 0:
                    okay = True
                    break
            if okay:
                break
        mutare = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for m in mutare:
            i = iSpatiu + m[0]
            j = jSpatiu + m[1]
            if 0 <= i <= 2 and 0 <= j <= 2:
                newState = copy.deepcopy(nod.informatie)
                newState[iSpatiu][jSpatiu], newState[i][j] = newState[i][j], newState[iSpatiu][jSpatiu]
                newNode = Node(newState, nod, nod.g + 1, self.calculeaza_h(newState))
                if not newNode.vizitat():
                    l.append(newNode)
        return l

    def calculeaza_h(self, informatie):
        return 0

    # ex 3
    def estimeaza_h(self, nod, tip_euristica):
        if self.scop(nod.informatie):
            return 0
        elif tip_euristica == "banala":
            return 1 if self.scop(nod.informatie) else 0
        elif tip_euristica == "euristica mutari":
            nb = float('inf')
            for scop in self.noduriScop:
                n = sum([1 for i in range(len(scop)) for j in range(len(nod.informatie)) if
                         nod.informatie[j][-1] != scop[i][-1]])
                if n < nb:
                    nb = n
            return nb
        elif tip_euristica == "euristica costurilor":
            costuri = []
            for scop in self.noduriScop:
                cost = 0
                for i in range(len(nod.informatie)):
                    for j in range(len(nod.informatie[i])):
                        if nod.informatie[i][j] != scop[i][j]:
                            cost += abs(ord(nod.informatie[i][j]) - ord(scop[i][j]))
                costuri.append(cost)
            return min(costuri)
        elif tip_euristica == "euristica manhattan":
            dm = []
            for i in range(len(nod.informatie)):
                for j in range(len(nod.informatie[i])):
                    x = nod.informatie[i][j]
                    for k in range(len(self.noduriScop[0])):
                        for l in range(len(self.noduriScop[0][k])):
                            if x == self.noduriScop[0][k][l]:
                                dm.append(abs(i - k) + abs(j - l))
                                break
            return sum(dm)
        elif tip_euristica == "euristica manhattan costuri":
            dm = []
            for i in range(len(nod.informatie)):
                for j in range(len(nod.informatie[i])):
                    x = nod.informatie[i][j]
                    for k in range(len(self.noduriScop[0])):
                        for l in range(len(self.noduriScop[0][k])):
                            if x == self.noduriScop[0][k][l]:
                                dm.append(abs(i - k) + abs(j - l))
                                break
            return sum([x * dm[x] for x in range(len(dm))])
        elif tip_euristica == "neadmisibila":
            return 1000000
        else:
            return 0


# 2c
def BFS(gr):
    coada = [Node(graf.nodStart)]
    while coada:
        nod = coada.pop(0)
        if gr.scop(nod.informatie):
            print(repr(nod))
        drum = gr.succesori(nod)
        coada += drum


def binary_search(listaNoduri, nodNou, st, dr):
    if len(listaNoduri) == 0:
        return 0
    if st == dr:
        if nodNou.f < listaNoduri[st].f:
            return st
        elif nodNou.f > listaNoduri[st].f:
            return dr + 1
        else:  # f-uri egale
            if nodNou.g < listaNoduri[st].g:
                return dr + 1
            else:
                return st
    else:
        mij = (st + dr) // 2
        if nodNou.f < listaNoduri[mij].f:
            return binary_search(listaNoduri, nodNou, st, mij)
        elif nodNou.f > listaNoduri[mij].f:
            return binary_search(listaNoduri, nodNou, mij + 1, dr)
        elif nodNou.g < listaNoduri[mij].g:
            return binary_search(listaNoduri, nodNou, mij + 1, dr)
        else:
            return binary_search(listaNoduri, nodNou, st, mij)


def a_star(graf):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open = [Node(graf.nodStart)]

    # l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)

    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        if graf.scop(nodCurent.informatie):
            print("Solutie:")
            drum = nodCurent.drumRadacina()
            print(("->").join([str(n.informatie) for n in drum]))
            print("cost:", nodCurent.g)
            return
        lSuccesori = graf.succesori(nodCurent)
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.informatie == nodC.informatie:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.informatie == nodC.informatie:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in graf.succesori(nodCurent):
            indice = binary_search(l_open, s, 0, len(l_open) - 1)
            if indice == len(l_open):
                l_open.append(s)
            else:
                l_open.insert(indice, s)


f = open("input.txt", "r")
start = [[int(x) for x in linie.strip().split(" ")] for linie in f.readlines()]
print(start)
scopuri = [[[1, 2, 3], [4, 5, 6], [7, 8, 0]]]

graf = Graph(start, scopuri)
BFS(graf)
a_star(graf)


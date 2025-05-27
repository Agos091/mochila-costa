import random
from src.config import CAPACITY

class Individuo:
    def __init__(self, genes, items):
        self.genes = genes
        self.items = items
        self.fitness = self.calcular_fitness()

    @classmethod
    def aleatorio(cls, tamanho, items):
        genes = [random.randint(0, 1) for _ in range(tamanho)]
        return cls(genes, items)

    def calcular_fitness(self):
        peso_total = valor_total = 0
        for i, gene in enumerate(self.genes):
            if gene:
                peso_total += self.items[i].weight
                valor_total += self.items[i].value
        if peso_total > CAPACITY:
            return 0
        return valor_total

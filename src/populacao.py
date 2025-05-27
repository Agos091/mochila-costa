import random
from src.individuo import Individuo
from src.config import POP_SIZE, MUTATION_RATE


class Populacao:
    def __init__(self, items, tamanho=POP_SIZE):
        self.items = items
        self.tamanho = tamanho
        self.individuos = [Individuo.aleatorio(len(items), items) for _ in range(tamanho)]

    def selecionar_pais(self):
        # Torneio binário
        return max(random.sample(self.individuos, 2), key=lambda ind: ind.fitness)

    def cruzar(self, pai1, pai2):
        ponto_corte = random.randint(1, len(pai1.genes) - 1)
        filho_genes = pai1.genes[:ponto_corte] + pai2.genes[ponto_corte:]
        return Individuo(filho_genes, self.items)

    def mutar(self, individuo):
        for i in range(len(individuo.genes)):
            if random.random() < MUTATION_RATE:
                individuo.genes[i] = 1 - individuo.genes[i]
        individuo.fitness = individuo.calcular_fitness()

    def nova_geracao(self):
        nova_pop = []
        while len(nova_pop) < self.tamanho:
            pai1 = self.selecionar_pais()
            pai2 = self.selecionar_pais()
            filho = self.cruzar(pai1, pai2)
            self.mutar(filho)
            nova_pop.append(filho)
        self.individuos = nova_pop

    def melhor_individuo(self):
        return max(self.individuos, key=lambda ind: ind.fitness)

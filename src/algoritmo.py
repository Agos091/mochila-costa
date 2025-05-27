from src.populacao import Populacao
from src.config import NUM_GENERATIONS


class AlgoritmoGenetico:
    def __init__(self, items, num_geracoes=NUM_GENERATIONS):
        self.items = items
        self.num_geracoes = num_geracoes

    def executar(self):
        populacao = Populacao(self.items)
        melhor_geral = populacao.melhor_individuo()

        for _ in range(self.num_geracoes):
            populacao.nova_geracao()
            melhor_geracao = populacao.melhor_individuo()
            if melhor_geracao.fitness > melhor_geral.fitness:
                melhor_geral = melhor_geracao

        return melhor_geral

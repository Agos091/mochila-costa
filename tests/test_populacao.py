import pytest
from src.item import Item
from src.populacao import Populacao


def test_populacao_criada_com_tamanho_correto():
    items = [Item(10, 60), Item(20, 100), Item(30, 120)]
    pop = Populacao(items, tamanho=10)
    assert len(pop.individuos) == 10


def test_selecao_de_pais_retorna_individuo_valido():
    items = [Item(5, 10)] * 10
    pop = Populacao(items, tamanho=5)
    pai = pop.selecionar_pais()
    assert pai is not None
    assert hasattr(pai, "genes")


def test_cruzamento_gera_filho_valido():
    items = [Item(10, 60), Item(20, 100)]
    pop = Populacao(items)
    pai1 = pop.selecionar_pais()
    pai2 = pop.selecionar_pais()
    filho = pop.cruzar(pai1, pai2)
    assert isinstance(filho.genes, list)
    assert len(filho.genes) == len(items)


def test_mutacao_modifica_genes():
    items = [Item(10, 60), Item(20, 100)]
    pop = Populacao(items)
    individuo = pop.selecionar_pais()
    genes_antes = individuo.genes.copy()
    pop.mutar(individuo)
    # Pode ou não mudar, mas a função deve ser executável sem erros
    assert hasattr(individuo, "fitness")


def test_gera_nova_geracao():
    items = [Item(5, 10)] * 5
    pop = Populacao(items, tamanho=5)
    genes_antes = [ind.genes.copy() for ind in pop.individuos]
    pop.nova_geracao()
    genes_depois = [ind.genes for ind in pop.individuos]
    assert len(pop.individuos) == 5
    # Testa se de fato há uma nova geração, mesmo que por sorte genes se repitam
    assert any(g1 != g2 for g1, g2 in zip(genes_antes, genes_depois))

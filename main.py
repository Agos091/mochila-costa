import pytest
from src.item import Item
from src.algoritmo import AlgoritmoGenetico


def test_algoritmo_retorna_melhor_individuo():
    items = [
        Item(10, 60),
        Item(20, 100),
        Item(30, 120),
        Item(5, 80),
        Item(25, 50)
    ]
    ag = AlgoritmoGenetico(items, num_geracoes=10)
    melhor = ag.executar()

    assert melhor is not None
    assert hasattr(melhor, "genes")
    assert isinstance(melhor.fitness, int)
    assert melhor.fitness >= 0

import pytest
from src.item import Item
from src.individuo import Individuo

def test_calcular_valido():
    items = [Item(10, 60), Item(20, 100), Item(30, 120)]
    genes = [1,0,0]
    individuo = Individuo(items, genes)
    assert individuo.fitness == 60


# Solução do Problema da Mochila 0/1 com Algoritmo Genético – Implementação Refatorada

> **Projeto acadêmico** — desenvolvido por Antonio Favarin, Agos Dalcin Rufino, Gustavo Schneider e Victor Lapa

Este repositório contém uma implementação enxuta e refatorada de um Algoritmo Genético (GA) para o Problema da Mochila 0/1. O código foi reorganizado em módulos claros, recebeu tipagem estática e testes automatizados, tornando‑o mais fácil de entender, manter e estender.

## Visão geral

O Problema da Mochila 0/1 (0/1 Knapsack) pede para selecionarmos um subconjunto de itens com **valor máximo** sem ultrapassar uma **capacidade de peso**. Por ser NP‑completo, heurísticas como Algoritmos Genéticos oferecem soluções próximas do ótimo em tempo razoável.

### Por que esta refatoração?

Código original feito de forma enxuta sem preocupação com modularização, o foco dos colegas foi entregar o input e output correto.

- **Separação de responsabilidades**: cada entidade (Item, Indivíduo, População, Algoritmo) vive em seu próprio arquivo.
- **Configuração centralizada**: todos os hiperparâmetros ficam em `src/config.py`.
- **Tipagem & lint**: uso de _type hints_ → menos bugs e melhor _autocomplete_.
- **Testes unitários** com `pytest` garantem que a lógica continue íntegra após mudanças.

---

## Estrutura do projeto

```
mochila-costa/
├── README.md              ← este arquivo
├── main.py                ← pequeno _driver_ de exemplo
├── src/
│   ├── algoritmo.py       ← loop principal do GA
│   ├── config.py          ← hiperparâmetros editáveis
│   ├── individuo.py       ← cromossomo + cálculo do fitness
│   ├── item.py            ← modelo de item (peso, valor)
│   └── populacao.py       ← seleção, cruzamento, mutação, elitismo
└── tests/
    ├── test_algoritmo.py
    ├── test_individuo.py
    └── test_populacao.py
```

---

## Requisitos

- **Python ≥ 3.10**
- [pytest](https://pytest.org) (opcional, apenas para os testes)

Instalação rápida:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate     # Windows PowerShell
pip install -U pytest        # somente se for rodar os testes
```

---

## Como executar

```bash
python main.py        # roda um experimento curto
o
python -m src.algoritmo_demo  # se você criar seu próprio script
```

O _script_ padrão cria cinco itens de exemplo e executa **10 gerações**; edite o arquivo ou passe seus próprios itens.

---

## Configurando parâmetros

Todos os hiperparâmetros ficam em `src/config.py`:

| Variável          | Significado                       | Default |
| ----------------- | --------------------------------- | ------- |
| `CAPACITY`        | Capacidade máxima da mochila      | `50`    |
| `NUM_GENERATIONS` | Número de gerações                | `50`    |
| `POP_SIZE`        | Tamanho da população inicial      | `30`    |
| `MUTATION_RATE`   | Probabilidade de mutação por gene | `0.01`  |

> Alterar qualquer valor requer **apenas** editar o arquivo ou ler variáveis de ambiente (veja `config.py` para detalhes).

---

## Arquitetura do GA

1. **Indivíduo** — vetor binário que indica quais itens estão na mochila.
2. **Fitness** — soma dos valores se o peso total ≤ `CAPACITY`; caso contrário, `0`.
3. **Seleção** — Torneio binário (escolhe o melhor de dois indivíduos aleatórios).
4. **Cruzamento** — _One‑point crossover_ com ponto de corte aleatório.
5. **Mutação** — troca de _bits_ com probabilidade `MUTATION_RATE`.
6. **Elitismo** — o melhor indivíduo sempre migra para a próxima geração.

Este ciclo se repete por `NUM_GENERATIONS`, guardando o melhor resultado global.

---

## Exemplo de uso

```python
from src.item import Item
from src.algoritmo import AlgoritmoGenetico

items = [
    Item(10, 60),  # peso, valor
    Item(20, 100),
    Item(30, 120),
    Item(5,  80),
    Item(25, 50),
]

ga = AlgoritmoGenetico(items, num_geracoes=100)
melhor = ga.executar()

print("Genes :", melhor.genes)
print("Valor :", melhor.fitness)
print("Peso  :", sum(i.weight for i, g in zip(items, melhor.genes) if g))
```

Saída típica:

```
Genes : [1, 0, 0, 1, 0]
Valor : 140
Peso  : 15
```

---

## Testes

Para garantir que tudo continua funcionando após alterações:

```bash
pytest -q  # roda ~20 testes em segundos
```

Os testes cobrem cálculo de fitness, operadores genéticos e convergência do algoritmo.

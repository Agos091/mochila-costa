import random
import numpy as np
import time
import statistics

# Função para inicializar a população com vetores binários aleatórios
# Cada indivíduo é uma lista de 0s e 1s, onde 1 indica que o item está na mochila
def initialize_population(pop_size, n_items):
    """
    Inicializa a população com pop_size indivíduos, cada um com n_items bits (0 ou 1).
    Args:
        pop_size (int): Tamanho da população.
        n_items (int): Número de itens.
    Returns:
        list: Lista de indivíduos (vetores binários).
    """
    return [np.random.randint(0, 2, n_items).tolist() for _ in range(pop_size)]

# Função de aptidão (fitness) para avaliar uma solução
def fitness(solution, weights, values, capacity):
    """
    Calcula a aptidão de uma solução, maximizando o valor total dos itens selecionados.
    Penaliza soluções que excedem a capacidade retornando um valor negativo.
    Args:
        solution (list): Vetor binário representando a solução.
        weights (list): Lista de pesos dos itens.
        values (list): Lista de valores dos itens.
        capacity (int): Capacidade máxima da mochila.
    Returns:
        float: Valor total se válida, ou penalização (-peso total) se inválida.
    """
    total_weight = sum(w * s for w, s in zip(weights, solution))
    total_value = sum(v * s for v, s in zip(values, solution))
    
    if total_weight > capacity:
        return -total_weight  # Penalização proporcional ao excesso de peso
    return total_value

# Seleção por torneio para escolher pais
def tournament_selection(population, fitnesses, tournament_size):
    """
    Realiza seleção por torneio, escolhendo o melhor indivíduo de um subconjunto aleatório.
    Args:
        population (list): Lista de indivíduos.
        fitnesses (list): Lista de aptidões correspondentes.
        tournament_size (int): Tamanho do torneio.
    Returns:
        list: Melhor indivíduo do torneio.
    """
    tournament = random.sample(range(len(population)), tournament_size)
    tournament_fitnesses = [fitnesses[i] for i in tournament]
    winner_idx = tournament[np.argmax(tournament_fitnesses)]
    return population[winner_idx]

# Crossover de dois pontos para gerar filhos
def crossover(parent1, parent2):
    """
    Realiza crossover de dois pontos, combinando partes de dois pais para gerar dois filhos.
    Args:
        parent1 (list): Primeiro pai (vetor binário).
        parent2 (list): Segundo pai (vetor binário).
    Returns:
        tuple: Dois filhos gerados (child1, child2).
    """
    point1 = random.randint(1, len(parent1) - 2)
    point2 = random.randint(point1, len(parent1) - 1)
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

# Mutação bit a bit com probabilidade mutation_rate
def mutate(solution, mutation_rate):
    """
    Aplica mutação bit a bit, invertendo bits (0->1 ou 1->0) com probabilidade mutation_rate.
    Args:
        solution (list): Solução a ser mutada.
        mutation_rate (float): Probabilidade de mutação por bit.
    Returns:
        list: Solução mutada.
    """
    return [1 - s if random.random() < mutation_rate else s for s in solution]

# Algoritmo Genético principal
def genetic_algorithm(weights, values, capacity, pop_size=100, generations=100, mutation_rate=0.01, tournament_size=3):
    """
    Executa o Algoritmo Genético para resolver o Problema da Mochila 0/1.
    Args:
        weights (list): Lista de pesos dos itens.
        values (list): Lista de valores dos itens.
        capacity (int): Capacidade da mochila.
        pop_size (int): Tamanho da população.
        generations (int): Número de gerações.
        mutation_rate (float): Taxa de mutação.
        tournament_size (int): Tamanho do torneio para seleção.
    Returns:
        tuple: Melhor solução (vetor binário), valor total, peso total.
    """
    n_items = len(weights)
    population = initialize_population(pop_size, n_items)
    
    for gen in range(generations):
        # Avaliar aptidão de toda a população
        fitnesses = [fitness(ind, weights, values, capacity) for ind in population]
        
        # Criar nova população
        new_population = []
        
        # Elitismo: manter o melhor indivíduo
        best_idx = np.argmax(fitnesses)
        new_population.append(population[best_idx])
        
        # Gerar o restante da população
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.extend([child1, child2])
        
        population = new_population[:pop_size]
    
    # Encontrar a melhor solução
    fitnesses = [fitness(ind, weights, values, capacity) for ind in population]
    best_idx = np.argmax(fitnesses)
    best_solution = population[best_idx]
    best_value = fitnesses[best_idx]
    best_weight = sum(w * s for w, s in zip(weights, best_solution))
    
    return best_solution, best_value, best_weight

# Função para executar testes com múltiplas execuções
def run_tests(pop_size=100, generations=100, mutation_rate=0.01, tournament_size=3, num_runs=5):
    """
    Executa testes com conjuntos de itens pequeno, grande e muito grande.
    Realiza múltiplas execuções para análise estatística.
    Args:
        pop_size (int): Tamanho da população.
        generations (int): Número de gerações.
        mutation_rate (float): Taxa de mutação.
        tournament_size (int): Tamanho do torneio.
        num_runs (int): Número de execuções por teste.
    """
    np.random.seed(42)  # Para reprodutibilidade
    
    # Conjunto de teste pequeno
    weights_small = [2, 3, 4, 5]
    values_small = [3, 4, 5, 6]
    capacity_small = 5
    
    print("\n=== Teste com Conjunto Pequeno (4 itens) ===")
    values, weights, times = [], [], []
    for i in range(num_runs):
        start_time = time.time()
        solution, value, weight = genetic_algorithm(
            weights_small, values_small, capacity_small, pop_size, generations, mutation_rate, tournament_size
        )
        end_time = time.time()
        values.append(value)
        weights.append(weight)
        times.append(end_time - start_time)
        
        print(f"Execução {i+1}:")
        print(f"  Solução: {solution}")
        print(f"  Valor total: {value}")
        print(f"  Peso total: {weight} (Válido: {weight <= capacity_small})")
        print(f"  Tempo: {end_time - start_time:.4f} segundos")
    
    print("\nEstatísticas:")
    print(f"  Média do valor: {statistics.mean(values):.2f}")
    print(f"  Desvio padrão do valor: {statistics.stdev(values) if len(values) > 1 else 0:.2f}")
    print(f"  Melhor valor: {max(values):.2f}")
    print(f"  Pior valor: {min(values):.2f}")
    print(f"  Média do tempo: {statistics.mean(times):.4f} segundos")
    
    # Conjunto de teste grande (1.000 itens)
    n_items_large = 1000
    weights_large = np.random.randint(1, 100, n_items_large).tolist()
    values_large = np.random.randint(1, 100, n_items_large).tolist()
    capacity_large = 5000
    
    print("\n=== Teste com Conjunto Grande (1.000 itens) ===")
    values, weights, times = [], [], []
    for i in range(num_runs):
        start_time = time.time()
        solution, value, weight = genetic_algorithm(
            weights_large, values_large, capacity_large, pop_size, generations, mutation_rate, tournament_size
        )
        end_time = time.time()
        values.append(value)
        weights.append(weight)
        times.append(end_time - start_time)
        
        print(f"Execução {i+1}:")
        print(f"  Valor total: {value}")
        print(f"  Peso total: {weight} (Válido: {weight <= capacity_large})")
        print(f"  Tempo: {end_time - start_time:.4f} segundos")
    
    print("\nEstatísticas:")
    print(f"  Média do valor: {statistics.mean(values):.2f}")
    print(f"  Desvio padrão do valor: {statistics.stdev(values) if len(values) > 1 else 0:.2f}")
    print(f"  Melhor valor: {max(values):.2f}")
    print(f"  Pior valor: {min(values):.2f}")
    print(f"  Média do tempo: {statistics.mean(times):.4f} segundos")
    
    # Conjunto de teste muito grande (10.000 itens)
    n_items_huge = 10000
    weights_huge = np.random.randint(1, 100, n_items_huge).tolist()
    values_huge = np.random.randint(1, 100, n_items_huge).tolist()
    capacity_huge = 50000
    
    print("\n=== Teste com Conjunto Muito Grande (10.000 itens) ===")
    values, weights, times = [], [], []
    for i in range(num_runs):
        start_time = time.time()
        solution, value, weight = genetic_algorithm(
            weights_huge, values_huge, capacity_huge, pop_size, generations, mutation_rate, tournament_size
        )
        end_time = time.time()
        values.append(value)
        weights.append(weight)
        times.append(end_time - start_time)
        
        print(f"Execução {i+1}:")
        print(f"  Valor total: {value}")
        print(f"  Peso total: {weight} (Válido: {weight <= capacity_huge})")
        print(f"  Tempo: {end_time - start_time:.4f} segundos")
    
    print("\nEstatísticas:")
    print(f"  Média do valor: {statistics.mean(values):.2f}")
    print(f"  Desvio padrão do valor: {statistics.stdev(values) if len(values) > 1 else 0:.2f}")
    print(f"  Melhor valor: {max(values):.2f}")
    print(f"  Pior valor: {min(values):.2f}")
    print(f"  Média do tempo: {statistics.mean(times):.4f} segundos")

# Executar os testes
if __name__ == "__main__":
    run_tests(pop_size=100, generations=100, mutation_rate=0.01, tournament_size=3, num_runs=5)
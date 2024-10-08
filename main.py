import random
import pygame
from deap import base, creator, tools
import itertools
import sys
from typing import Tuple
from pygame.surfarray import make_surface
from PIL import Image
import matplotlib.pyplot as plt
import io
import numpy as np

# Configuração do Pygame
pygame.init()
WINDOW_SIZE = 800
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Visualização do Algoritmo Genético")
clock = pygame.time.Clock()
generation_counter = itertools.count(start=1)  # Start the counter at 1
FPS = 1

def initialize_cities():
    # """ Inicializa as cidades com posições aleatórias dentro da janela. """
    # return [(random.randint(50, WINDOW_SIZE - 50), random.randint(50, WINDOW_SIZE - 50)) for _ in range(num_cities)]
    """ Inicializa as cidades com posições fixas. """
    return [
        (100, 100), (200, 100), (300, 100), (400, 100),
        (100, 200), (200, 200), (300, 200), (400, 200),
        (100, 300), (200, 300), (300, 300), (400, 300),
        (100, 400), (200, 400), (300, 400), (400, 400)
    ]

def draw_path(path, city_positions, color: Tuple[int, int, int], width: int):
    """ Desenha as cidades e o caminho na tela. """
    screen.fill((255, 255, 255))  # Fundo branco
    
    # Desenhar cidades
    for i, pos in enumerate(city_positions):
        pygame.draw.circle(screen, (0, 0, 255), pos, 10)
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(i), True, (0, 0, 0))
        screen.blit(text, (pos[0] + 10, pos[1] - 10))
    
    # Desenhar caminho
    if len(path) < 2 or not all(i < len(city_positions) for i in path):
        print("Caminho inválido:", path)
        return  # Não desenha se o caminho não for válido

    for i in range(len(path) - 1):
        start_pos = city_positions[path[i]]
        end_pos = city_positions[path[i + 1]]
        pygame.draw.line(screen, color, start_pos, end_pos, width)

    pygame.display.flip()

# Função para calcular a distância total de um caminho
def evaluate(individual):
    distance = 0

        # Enforce start and end points in the route
    if individual[0] != start_city or individual[-1] != end_city:
        distance += float('inf')

    for i in range(len(individual)):
        from_city = individual[i]
        to_city = individual[(i + 1) % len(individual)]
        distance += dist_matrix[from_city][to_city]

    return distance,

# Função para criar um indivíduo (pop)
def create_individual():
    # Cria um indivíduo que começa com o ponto de início e termina com o ponto de fim
    individual = random.sample(range(len(dist_matrix)), len(dist_matrix))
    if start_city in individual:
        individual.remove(start_city)
    if end_city in individual:
        individual.remove(end_city)
    return [start_city] + individual + [end_city]
    
    # Insere o ponto de início no início e o ponto de fim no final
    return [start_city] + individual + [end_city]

# Função para mutar um indivíduo
def mutate(individual):
    if len(individual) < 2:
        return individual,
    idx1, idx2 = random.sample(range(len(individual)), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual,

# Função para crossover entre dois indivíduos
def crossover(ind1, ind2):
    size = len(ind1)
    cxpoint1, cxpoint2 = sorted(random.sample(range(size), 2))
    
    # Criação do novo indivíduo
    child1 = [-1] * size
    child2 = [-1] * size
    
    # Cópia do segmento de ind1 para child1
    child1[cxpoint1:cxpoint2] = ind1[cxpoint1:cxpoint2]
    
    # Preenchimento dos valores restantes
    fill_child(child1, ind2)
    fill_child(child2, ind1)
    
    return child1, child2

# Preencher o restante do indivíduo
def fill_child(child, parent):
    size = len(child)
    child_set = set(child)
    
    # Valores a serem preenchidos
    fill_values = [v for v in parent if v not in child_set]
    
    # Preencher os índices faltantes
    fill_idx = [i for i in range(size) if child[i] == -1]
    for idx in fill_idx:
        child[idx] = fill_values.pop(0)

# Inicialização das cidades
city_positions = initialize_cities()

# Criar matriz de distâncias entre cidades
def create_distance_matrix(positions):
    size = len(positions)
    matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            distance = int(((positions[i][0] - positions[j][0]) ** 2 + (positions[i][1] - positions[j][1]) ** 2) ** 0.5)
            matrix[i][j] = distance
            matrix[j][i] = distance
    return matrix


# Configuração do DEAP
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", crossover)
toolbox.register("mutate", mutate)
toolbox.register("select", tools.selTournament, tournsize=3)

ELITE = 1

# Variáveis para armazenar a evolução do melhor fitness
generation_numbers = []
best_fitnesses = []

# Selecionar pontos de início e fim
start_city = 0
end_city = len(city_positions) - 1

def select_start_end_points():
    global start_city, end_city
    while True:  # Loop até obter entradas válidas
        try:
            print("Selecione o ponto de início e o ponto de fim:")
            for i, pos in enumerate(city_positions):
                print(f"Cidade {i}: {pos}")
            start_city = int(input("Digite o índice da cidade de início: "))
            end_city = int(input("Digite o índice da cidade de fim: "))
            if start_city < 0 or start_city >= len(city_positions):
                raise ValueError("Índice de início inválido")
            if end_city < 0 or end_city >= len(city_positions):
                raise ValueError("Índice de fim inválido")
            print(f"Ponto de início: {start_city}, Ponto de fim: {end_city}")
            break  # Sai do loop se tudo estiver correto
        except ValueError as e:
            print(e)  # Mostra o erro e repete o loop


def select_cities_to_remove() -> list[int]:
    """Permite ao usuário selecionar cidades para remover."""
    while True:
        try:
            print("Cidades disponíveis para remover:")
            for i, pos in enumerate(city_positions):
                print(f"Cidade {i}: {pos}")
            indices = input("Digite os índices das cidades para remover, separados por espaço: ")
            indices = list(map(int, indices.split()))
            return indices
        except ValueError:
            print("Por favor, insira índices válidos.")

def remove_cities(indices: list[int]):
    """Remove as cidades especificadas pelos índices da lista de cidades."""
    global city_positions, city_positions_rem
    city_positions = [pos for i, pos in enumerate(city_positions) if i not in indices]
    print(f"Cidades restantes: {city_positions}")

print(len(city_positions))
indices_to_remove = select_cities_to_remove()
remove_cities(indices_to_remove)
print(len(city_positions))
select_start_end_points()
dist_matrix = create_distance_matrix(city_positions)


# Main game loop
running = True
evolution_complete = False
population = toolbox.population(n=50)
NGEN, CXPB, MUTPB = 300, 0.5, 0.2
    
if not evolution_complete:
    print("Iniciando o processo evolutivo")

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, population)
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    for gen in range(NGEN):
        elitismo = tools.selBest(population, ELITE)
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))
        
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        # Recalculate fitness for all individuals with invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid] # Changed from population to offspring
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        population[:] = elitismo + toolbox.select(population + offspring, len(population)-ELITE)
        
        fits = [ind.fitness.values[0] for ind in population]
        length = len(population)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print(f"Gen {gen} - Média: {mean}  Std: {std}")
        
        # Desenhar o melhor indivíduo encontrado até o momento
        best_individual = tools.selBest(population, 1)[0]
        second_best_individual = tools.selBest(population, 2)[1]
        best_fitnesses.append(best_individual.fitness.values[0])
        generation_numbers.append(gen)
        draw_path(best_individual, city_positions, color=(0,255,0), width=4 )
        draw_path(second_best_individual, city_positions, color=(255,0,0),width=1)

        pygame.display.flip()
        clock.tick(15) 

    evolution_complete = True      

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    screen.fill((255, 255, 255))  # Limpar a tela
    draw_path(best_individual, city_positions, color=(0, 255, 0), width=4)  # Melhor caminho em verde
    draw_path(second_best_individual, city_positions, color=(255, 0, 0), width=1)  # Segundo melhor caminho em vermelho
    pygame.display.flip()
    clock.tick(10)  # Controlar a taxa de atualização

best_individual = tools.selBest(population, 1)[0]
print("Melhor caminho encontrado:", best_individual)
print("Distância total:", best_individual.fitness.values[0])

pygame.quit()
sys.exit() 
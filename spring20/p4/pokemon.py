"""
API file to access data from pokemon_data.csv file
"""

import csv

_pokemons = []

def init(filename='pokemon_data.csv'):
    if filename != 'pokemon_data.csv':
        print("WARNING! Recommended that you open data.csv for the current assignment")
    with open(filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            _pokemons.append(row)

def get_pokemon_stats(id=1):
    pokemon = _pokemons[id-1]
    stats = {
                'Name': pokemon['Name'].lower(),
                'HP': int(pokemon['HP']),
                'Total': int(pokemon['Total']),
                'Attack': int(pokemon['Attack']),
                'Defense': int(pokemon['Defense']),
                'Special_Attack': int(pokemon['Sp. Atk']),
                'Special_Defense': int(pokemon['Sp. Def']),
                'Generation': int(pokemon['Generation']),
                'Types': [pokemon['Type 1'], pokemon['Type 2']],
                'Legendary': pokemon['Legendary'],
            }
    return stats

def get_name(id=1):
    return get_pokemon_stats(id=id)['Name']

def get_hp(id=1):
    return get_pokemon_stats(id=id)['HP']

def get_total(id=1):
    return get_pokemon_stats(id=id)['Total']

def get_attack(id=1):
    return get_pokemon_stats(id=id)['Attack']

def get_defense(id=1):
    return get_pokemon_stats(id=id)['Defense']

def get_special_attack(id=1):
    return get_pokemon_stats(id=id)['Special_Attack']

def get_special_defense(id=1):
    return get_pokemon_stats(id=id)['Special_Defense']

def get_generation(id=1):
    return get_pokemon_stats(id=id)['Generation']

def get_types(id=1):
    types = get_pokemon_stats(id=id)['Types']
    if types[1] == '':
        types = [types[0]]
    return types

def get_legendary(id=1):
    return get_pokemon_stats(id=id)['Legendary']
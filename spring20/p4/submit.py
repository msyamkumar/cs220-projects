from pokemon import *



def is_multitype(id=1):
    if len(get_types(id)) > 1:
        return True
    else:
        return False


def pokemon_battle_simple(id1=1, id2=2, margin=0):
    if get_total(id1) - get_total(id2) - margin > 0:
        return get_name(id1)
    elif get_total(id2) - get_total(id1) - margin > 0:
        return get_name(id2)
    else:
        return "Draw"

def get_total_attack(id1=1):
    return (get_attack(id1) + get_special_attack(id1)) / 2.0

def get_total_defense(id1=1):
    return (get_defense(id1) + get_special_defense(id1)) / 2.0


def pokemon_battle_survival(id1=1, id2=2, margin=0, special_moves=False):

    if abs(get_generation(id1) - get_generation(id2)) > 3:
        # print(get_generation(id1), get_generation(id2))
        print("Not Compatible")
        return
    else:
        # print(get_name(id1), get_name(id2))
        # Compatible pokemons
        if special_moves:
            surv1 = get_total_defense(id1) - get_total_attack(id2)
            surv2 = get_total_defense(id2) - get_total_attack(id1)
            # print(surv1, surv2)
        else:
            surv1 = get_defense(id1) - get_attack(id2)
            surv2 = get_defense(id2) - get_attack(id1)

        if get_total(id1) - get_total(id2) - margin > 0:
            return get_name(id1)
        elif get_total(id2) - get_total(id1) - margin > 0:
            return get_name(id2)
        else:
            if surv1 > surv2:
                return get_name(id1)
            elif surv2 > surv1:
                return get_name(id2)
            else:
                return "Draw"

def calculate_score(id):
    """
    Returns a winnability score for a given pokemon
    """
    pass
    
    
def pokemon_battle_score(id1=1, id2=2):
    pass






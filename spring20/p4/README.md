# Project 4: Pokémon Simulation

## Corrections/Clarifications
None yet.

## Overview

For this project, you'll be using the data from `pokemon_stats.csv` to
simulate Pokémon battles. This data was gathered by the Python program
`gen_csv.ipynb` from the website https://www.pokemondb.net/.  This project will
focus on **conditional statements**. To start, download `project.py`,
`test.py` and `pokemon_stats.csv`. You'll do your work in a Jupyter Notebook,
producing a `main.ipynb` file. You'll test as usual by running `python test.py`
to test a `main.ipynb` file.

We won't explain how to use the `project` module here (the code in the
`project.py` file). The lab this week is designed to teach you how it
works. So, before starting P4, take a look at Lab P4.

This project consists of writing code to answer 20 questions. If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

## Questions and Functions

For the first few questions, we will try to simulate a very simple 'battle'.
Create a function `simple_battle(pkmn1, pkmn2)` which simply returns the name of
the Pokémon with the highest stat total.

**Hint: In Lab P4, you created a helper function which could be very useful here**
### Q1: What is the output of `simple_battle('Gligar', 'Pidgeotto')`?

### Q2: What is the output of `simple_battle('Gligar', 'Pidgeot')`?

While we are off to a good start, the function is not quite finished yet. For instance,
consider the Pokémon Charmander and Chimchar. Both of them have the same stat total
of 309. In such cases, we want our function to return the string `'Draw'` instead of
choosing between the two Pokémon.

### Q3: What is the output of `simple_battle('Chikorita', 'Turtwig')`?

Our function `simple_battle` is quite rudimentary. All it does is compare the stat
totals of different Pokémon. Although it can predict effectively when the stat
totals of two Pokémon are far apart, we cannot rely on its predictions, if the
two numbers are close to each other. Modify `simple_battle` so that it returns
`'Draw'` if `|stat total of pkmn1 - stat total of pkmn2| < 20`.

### Q4: What is the output of `simple_battle('Kingler', 'Staraptor')`?

### Q5: What is the output of `simple_battle('Heracross', 'Krookodile')`?

Our function `simple_battle` is a good start, but we can make our battles a bit
more interesting. Let us set up some rules for our battles.

1. The Pokémon take turns attacking each other.
2. The Pokémon with the higher Speed stat attacks first.
3. On each turn, the attacking Pokémon can choose between two moves - Physical
or Special
4. Based on the move chosen by the attacking Pokémon, the defending Pokémon
receives damage to its HP.
5. If a Pokémon's HP drops to (or below) 0, it faints and therefore loses
the battle.

The damage caused by a Pokémon's Physical move is `10 * Attack stat of
Attacker / Defense stat of Defender`, and the damage caused by a Pokémon's
Special move is `10 * Sp. Atk. stat of Attacker / Sp. Def. stat of Defender`.

**If a Pokémon wants to win, it should always choose the move which will do
more damage.**

For example, let the attacker be Scraggy and the defender be Tranquill. Their
stats are as follows:
```python
>>> project.print_stats('Scraggy')
Name :  Scraggy
Region :  Unova
Type 1 :  Dark
Type 2 :  Fighting
HP :  50
Attack :  75
Defense :  70
Sp. Atk :  35
Sp. Def :  70
Speed :  48
>>> project.print_stats('Tranquill')
Name :  Tranquill
Region :  Unova
Type 1 :  Normal
Type 2 :  Flying
HP :  62
Attack :  77
Defense :  62
Sp. Atk :  50
Sp. Def :  42
Speed :  65
>>>
```
The damage caused by Scraggy's physical move will be `10*75/62`, which is `12.0967`,
while the damage caused by its special move will be `10*35/42`, which is `8.33`.
**So, in this case, when facing Tranquill, Scraggy would always choose its physical
move to do `12.0967` damage.**

Copy/paste the following code in a new cell of your notebook and fill in the details.

```python
def most_damage(attacker, defender):
    if ???:
        return 10 * project.get_attack(attacker)/project.get_defense(defender)
    else:
        ???
```

Verify that `most_damage('Scraggy', 'Tranquill')` returns `12.0967`.

### Q6: What is the damage that will be done by Caterpie to Incineroar?

### Q7: What is the damage that will be done by Naganadel to Rockruff?

### Q8: What is the damage that will be done by Taillow to Swellow?

### Q9: What is the damage that will be done by Swellow to Taillow?

Now that we have a way of calculating the damage done by the Pokémon during
battle, we have to calculate how many hits each Pokémon can take before fainting.

Going back to our previous example, we saw that Scraggy does `12.0967` damage to
Tranquill, each turn. Since Tranquill has HP `62`, it can take a total of `62/12.0697
= 5.125` hits, which is rounded up to `6` hits. So, Tranquill
can take `6` hits from Scraggy before it faints.

Copy/paste the following code in a new cell of your notebook and fill in the details.

```python
def num_hits(attacker, defender):
    return math.ceil(project.get_hp(???)/???)
```

**Hint: You might want to use the method [math.ceil()](https://docs.python.org/3/library/math.html) here. First import the module math
and then look up the documentation of math.ceil to see how you could use it.**

### Q10: How many hits can Goomy take from Gible?

### Q11: How many hits can Donphan take from Aipom?

### Q12: How many hits can Aipom take from Donphan?

Since Donphan can take more hits from Aipom than Aipom can from Donphan, clearly
Donphan would win in a battle between the two. With the tools we have created
so far, we can now finally create a battle simulator. Copy/paste the following
code in a new cell of your notebook and fill in the details.

```python
def battle(pkmn1, pkmn2):
    #TODO: Return the name of the pkmn that can take more hits from the other
    # pkmn. If both pkmn faint within the same number of moves, return the
    # string 'Draw'
```

### Q13: What is the outcome of `battle('Infernape', 'Torterra')`?

### Q14: What is the outcome of `battle('Torkoal', 'Sceptile')`?

### Q15: What is the outcome of `battle('Tepig', 'Oshawott')`?

You may have noticed that the function `battle` does not quite follow all the rules
that we laid out at the beginning. Find the output of `battle('Swadloon', 'Palpitoad')`.
You will find that it is a draw, since they can both take 7 hits from the other Pokémon.
But since Palpitoad has a higher Speed, it attacks first, so it will land its
seventh hit on Swadloon, before Swadloon can hit Palpitoad. So, even though they
both go down in the same number of moves, Palpitoad should win the battle.

Go back and modify `battle()` so that if both Pokémon faint in the same number of
moves, the Pokémon with the higher Speed wins. If they both have the same Speed,
then the battle should be a `'Draw'`.

### Q16: What is the outcome of `battle('Bulbasaur', 'Squirtle')`?

### Q17: What is the outcome of `battle('Greninja', 'Hawlucha')`?

### Q18: What is the outcome of `battle('Snorlax', 'Charizard')`?

Our function `battle` is now working just as intended. But let us build some checks
and balances into the function, to make it more reasonable. We will assume that
Pokémon from different regions cannot battle each other, since they can't both meet
each other.

Create a new function `final_battle(attacker, defender)` so that if two Pokémon from
different regions try to fight each other, the function returns `'Cannot battle'`.
If both Pokémon are from the same region, the battle proceeds as before.

### Q19: What is the outcome of `final_battle('Pikachu', 'Snivy')`?

This restriction however, is a little too harsh. We can assume that Pokémon whose
type (Type 1 or Type 2) is `Flying` can reach other regions by flying there.

Modify `final_battle` so that even if the two Pokémon are from different regions, if the
Type 1 **or** Type 2 of the Attacker is 'Flying', then the battle can
take place as before.

### Q20: What is the outcome of `final_battle('Dragonite', 'Goodra')`?


That will be all for now. If you are interested, you can make your `battle` functions
as complicated as you want. Good luck with your project!

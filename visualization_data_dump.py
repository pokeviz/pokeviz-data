from visualization import *
import json

"""
SELECT pt.pokemon, p.stats, t1.type, t2.type
FROM 
	PokemonTier 
		JOIN
	Pokemon p ON pt.pokemon = p.pk
		JOIN
	(SELECT type
	FROM PokemonType pt
	WHERE pt.slot = 1) t1
		LEFT JOIN
	(SELECT type
	FROM PokemonType pt
	WHERE pt.slot = 2) t2
WHERE pt.tier = ?
---
pk, stats, t1, t2
---
{ 
	36: [[pk1, stats1, t11, t21]],
	37: [[...]],
	38: [[...]]
}  

Dominant Type;
For each type, the average stats, median stats

Dominant Type per tier
Average per tier
"""
def temp_tier_gen(tier):
	if tier - 8 < 0:
		return 3
	elif tier - 16 < 0:
		return 4
	elif tier - 27 < 0:
		return 5
	elif tier - 39 < 0:
		return 6
	else:
		return 0


def temp():
	pokeselect = ['pk', 'name', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed']
	zipkey = ['pk', 'n', 'hp', 'atk', 'def', 'satk', 'sdef', 'spd', 't1', 't2']
	container = {}

	for i in range(1, 39):
		container[i] = []
		gen = temp_tier_gen(i)
		pokemons = get_pokemon_by_tier(i)
		for pokemon in pokemons:
			temp = []
			pokemon = pokemon.pokemon.pk
			arg = [pokemon, gen, gen, pokemon, gen, gen]
			types = PokemonType.raw("""
				SELECT t1.pokemon_type AS pt1, t2.pokemon_type AS pt2
				FROM
				        (SELECT *
				        FROM PokemonType pt
				        WHERE pt.pokemon = ?
				        AND pt.slot = 1
				        AND pt.gen_start <= ?
				        AND pt.gen_until >= ?) t1
				LEFT JOIN (SELECT *
				        FROM PokemonType pt
				        WHERE pt.pokemon = ?
	        			AND pt.slot = 2
	        			AND pt.gen_start <= ?
	        			AND pt.gen_until >= ?) t2 
				ON t1.pokemon_type = t2.pokemon_type""", *arg)
			pokestats = get_pokemon(pokemon, pokeselect)
			for pokestat in pokestats:
				for s in pokeselect:
					temp.append(getattr(pokestat, s))

			for t in types:
				temp.append(t.pt1)
				if t.pt2 is None:
					temp.append(0)
				else:
					temp.append(t.pt2)

			container[i].append(dict(zip(zipkey, temp)))


	with open('output/v3.json', 'w') as v3:
		v3.write(json.dumps(container, separators=(',',':')))

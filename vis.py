"""
Queries to generate single and dual types.
http://i.imgur.com/c1z5YTa.png
By: reddit@user:ROMaster2

http://imgur.com/PnOqyam
By: reddit@user:glitterizer

- Strict mode 		: main and secondary type is non interchangeable
- Lax mode 			: main and secondary type is interchangeable
- No Arceus & Silv	: no arceus/silvally forms 
- No Forms 			: absolutely no other forms (rotom forms, alola, megas, all)
- No Megas 			: forms allowed but no megas 
- No Legendaries 	: *future*
- Generation 		: only include pokemon up to x generation 

"""
from Pokeclass import *
from random import randint
import json

# Type list grabbed from the kaggle website
TYPES = ['Normal', 
		 'Fighting', 
		 'Flying',
		 'Poison', 
		 'Ground', 
		 'Rock', 
		 'Bug', 
		 'Ghost', 
		 'Steel', 
		 'Fire', 
		 'Water', 
		 'Grass', 
		 'Electric',
		 'Psychic', 
		 'Ice', 
		 'Dragon', 
		 'Dark', 
		 'Fairy']  

# Color corresponding to each type, can simply just zip these two
COLORS = ['#BBBDAF', 
		  '#A35449', 
		  '#75A4F9', 
		  '#AD5CA2', 
		  '#F0CA42', 
		  '#CDBD72', 
		  '#C3D221', 
		  '#7673DA', 
		  '#C3C1D7', 
		  '#F95643', 
		  '#53AFFE', 
		  '#8ED752', 
		  '#F8E64E', 
		  '#FB61B4', 
		  '#66EBFF', 
		  '#8B76FF', 
		  '#8E6856', 
		  '#F9AEFE'];


# Various options for exclusions, i.e no megas, no forms
OPTIONS = {
	'DEFAULT': [12, 14, 11], 
	'NO-MEGA': [12, 14, 11, 16, 17],
	'NO-FORM': [12, 14, 11, 16, 17, 9, 13],
	'NO-LEGENDARY': [12, 14, 11, 3, 4, 8]
}


# NO NEED FOR THIS JUST USE http://docs.peewee-orm.com/en/latest/peewee/querying.html#counting-records
"""
Decorator to get count Pokemon by their primary type.
"""
# def count(f):
# 	def count_wrap(*args, **kwargs):
# 		query = f(*args, **kwargs).select(fn.COUNT('*'))
# 		return query
# 	return count_wrap


"""
Basic query to get Pokemon with a given type id.
TODO: figure out a way to clean up selection variable
""" 
def get_pokemon_type(gen, 
					 type_id=None, 
					 slot=None, 
					 selection=[], 
					 alias=None):
	# Hardcode this
	if 'pokemon' not in selection:
		selection.append('pokemon')

	# Base select and where clause
	selecting = [getattr(PokemonType, s) for s in selection]
	query = (PokemonType
		.select(*selecting)
		.where(PokemonType.gen_start <= gen,
			   PokemonType.gen_until >= gen))

	if type_id is not None:
		query = query.where(PokemonType.pokemon_type == type_id)

	if slot is not None:
		query = query.where(PokemonType.slot == slot)

	if alias is not None:
		query = query.alias(alias)

	return query


"""
Basic query to get Pokemon's classification given classification id.
"""
def get_pokemon_classification(option, 
							   alias=None):
	option = OPTIONS[option]
	query = (PokemonClassification
		.select(PokemonClassification.pokemon,
			    PokemonClassification.classification)
		.where(PokemonClassification.classification << option))

	if alias is not None:
		query = query.alias(alias)

	return query


"""
Basic query to get Pokemon's sprite given pokemon id.
"""
def get_spritename(pokemon):
	query = (PokemonSprite
		.select(PokemonSprite.spritename)
		.where(PokemonSprite.pokemon == pokemon))
	return query


"""
Query to get singly typed Pokemon(s).
"""
def get_single_type_pokemon(gen, 
							type_id, 
							selection=['pokemon_type'],
							option='DEFAULT'):
	# Main type
	pri = get_pokemon_type(gen=gen, 
						   type_id=type_id, 
						   slot=1, 
						   alias='pri')
	# Need to left join with secondary type and check for nulls
	sec = get_pokemon_type(gen=gen, 
						   slot=2, 
						   selection=selection,
						   alias='sec')
	# Left join again wtih classification to get rid
	# of redundant pokemons and perhaps extra stuff
	exclude = get_pokemon_classification(option, 'exclude')


	# Build main query
	main = (Pokemon
		.select(Pokemon.pk, 
				Pokemon.name)
		.join(pri,
			on=(pri.c.pokemon == Pokemon.pk))
		.switch(Pokemon)
		.join(sec, 
			JOIN.LEFT_OUTER, 
			on=(sec.c.pokemon == pri.c.pokemon))
		.switch(Pokemon)
		.join(exclude,
			JOIN.LEFT_OUTER,
			on=(exclude.c.pokemon == pri.c.pokemon))
		.where(exclude.c.classification >> None,
			sec.c.pokemon_type >> None))

	return main


"""
Query to get doubly typed Pokemon(s).
"""
def get_double_type_pokemon(gen, 
							type_id1, 
							type_id2, 
							option='DEFAULT', 
							mode='LAX'):
	# No need for aliases here since we are intersecting
	# pri and sec stands for primary and secondary
	if mode is 'STRICT':
		pri = get_pokemon_type(gen=gen, type_id=type_id1, slot=1)
		sec = get_pokemon_type(gen=gen, type_id=type_id2, slot=2)
	else: # mode is 'LAX'
		pri = get_pokemon_type(gen=gen, type_id=type_id1)
		sec = get_pokemon_type(gen=gen, type_id=type_id2)
			
	main = (pri & sec).alias('main')
	exclude = get_pokemon_classification(option, 'exclude')

	# Build main query
	main = (Pokemon
		.select(Pokemon.pk, 
				Pokemon.name)
		.join(main,
			on=(main.c.pokemon == Pokemon.pk))
		.switch(Pokemon)
		.join(exclude,
			JOIN.LEFT_OUTER,
			on=(exclude.c.pokemon == main.c.pokemon))
		.where(exclude.c.classification >> None))

	return main


"""

"""
def _fetchone(select_query, selection):
	retvals = [getattr(s, selection) for s in select_query]
	# Prevent index out of range error
	if len(retvals) == 0:
		return []
	return retvals[randint(0, len(retvals) - 1)]


"""
Generate master json for the first visualization.
"""
def generate_type_json():
	# {
	# 	"LAX": [
	#		[{	
	# 				'NO-FORM': [[]... repeated 18 times ...], 
	# 				'NO-LEGENDARY': [[]...], 
	# 				'NO-MEGA': [[]...]
	# 		}],
	# 		[... repeated for 7 generations ...] 	
	# 	],
	# 	"STRICT":[... same as lax ...]
	# }

	modes = ['LAX', 'STRICT']
	generations = range(0, 7)
	options = ['DEFAULT', 'NO-MEGA', 'NO-FORM', 'NO-LEGENDARY']
	primaries = range(0, 18)
	secondaries = range(0, 18)

	# lol 
	# to save space for the future, mega option should only be
	# available to gen 6 and 7 only, form option to gen 3 onwards
	retjson = {}
	for mode in modes:
		# Setup the container to get all generations
		gen_container = []
		for generation in generations:
			opt_container = {}
			for option in options:
				pri_container = []
				# Check, need to save space
				if "MEGA" in option and generation < 5:
					continue
				elif "FORM" in option and generation < 2:
					continue
				for i in primaries:
					sec_container = []
					for j in secondaries:

						# If they're the same fetch single typed
						if i == j:
							query = get_single_type_pokemon(
									gen = generation + 1, 
									type_id = i + 1, 
									option = option)
						else:
						# Otherwise fetch from double type
							query = get_double_type_pokemon(
									gen = generation + 1, 
									type_id1 = i + 1, 
									type_id2 = j + 1, 
									option = option, 
									mode = mode)

						
						pokemon = _fetchone(query, 'pk')
						# If its empty, that means theres no
						# pokemon with that typing
						# We can safely skip it
						spritename = ''
						# 'is not' doesn't work
						if pokemon != []:
							sprite_query = get_spritename(pokemon)
							spritename = _fetchone(sprite_query, 'spritename')
						sec_container.append(spritename)
					pri_container.append(sec_container)
				opt_container[option] = pri_container
			# Append to the container while we have all the options
			gen_container.append(opt_container)
		# Append mode to retjson 
		retjson[mode] = gen_container
	# Return minifed json
	return json.dumps(retjson, separators=(',',':'))


"""
Generate master json for the second visualization. 
This one is simply just counting.
"""
def generate_count_json():
	# [[
	# 	{		
	# 			'NO-FORM': [[]... repeated 18 times ...], 
	# 			'NO-LEGENDARY': [[]...], 
	# 			'NO-MEGA': [[]...]
	# 	}],
	# 	[... repeated for 7 generations ...] 	
	# ]
	generations = range(0, 7)
	options = ['DEFAULT', 'NO-MEGA', 'NO-FORM']
	primaries = range(0, 18)
	secondaries = range(0, 18)	

	retjson = []
	# lol again
	for generation in generations:
		opt_container = {}
		for option in options:
			pri_container = []
			# Check, need to save space
			if "MEGA" in option and generation < 5:
				continue
			elif "FORM" in option and generation < 2:
				continue
			for i in primaries:
				sec_container = []
				for j in secondaries:
					if i == j:
						query = get_single_type_pokemon(
								gen = generation + 1, 
								type_id = i + 1, 
								option = option)
					else:
					# Otherwise fetch from double type
						query = get_double_type_pokemon(
								gen = generation + 1, 
								type_id1 = i + 1, 
								type_id2 = j + 1, 
								option = option, 
								mode = 'STRICT')
					sec_container.append(query.count())
				pri_container.append(sec_container)
			opt_container[option] = pri_container
		retjson.append(opt_container)
	return json.dumps(retjson, separators=(',',':'))


if __name__ == '__main__':
	pass
	# a = get_single(3,14)
	# # Default
	# for i in a:
	# 	print i.name


	# No legendary
	# a = get_single_type_pokemon(1,14)

	# b = get_double_type_pokemon(gen=7, 
	# 	  type_id1=9, 
	# 	  type_id2=3, 
	# 	  option='DEFAULT', 
	# 	  mode='STRICT')

	# print a.count()

	# c = get_spritename(1)

	retjson = generate_count_json()
	filename = "v2.json"
	with open(filename, 'w') as outfile: 
		outfile.write(retjson)

from visualization import *
import json

# GENERATION INTRODUCED
# If there are two then just pick one with the lowest


# {
# 	"G1": {
# 		"name": "normal",
# 		"children": [
# 			{
# 				"name": "normal-normal",
# 				"count": 0 
# 			},
# 			{
# 				"name": "normal-fighting",
# 				"count": 1
# 			},
# 			...
# 	]}
# }

"""
Generate master json for the first visualization.
Generate master json for the second visualization. 
This one is simply just counting.
"""
def generate_v2a_json():
	generations = range(0, 7)
	option = 'DEFAULT'
	mode = 'STRICT'
	primaries = range(0, 18)
	secondaries = range(0, 18)

	# lol 
	# to save space for the future, mega option should only be
	# available to gen 6 and 7 only, form option to gen 3 onwards
	retjson = []
	# Check, need to save space
	for g in generations:
		genresult = {}
		genresult['name'] = str(g)
		genresult['children'] = []
		for i in primaries:
			imresult = {}
			imresult['name'] = TYPES[i].lower()
			imresult['children'] = []
			for j in secondaries:
				# If they're the same fetch single typed
				if i == j:
					query = get_single_type_pokemon(
							gen = g + 1, 
							type_id = i + 1, 
							option = option)
				else:
				# Otherwise fetch from double type
					query = get_double_type_pokemon(
							gen = g + 1, 
							type_id1 = i + 1, 
							type_id2 = j + 1, 
							option = option, 
							mode = mode)

				imresult['children'].append({'name': TYPES[j].lower(), 'size': query.count()})
			genresult['children'].append(imresult)
		retjson.append(genresult)

	# Return minifed json
	return json.dumps(retjson, separators=(',',':'))


def generate_v5_json():
	generations = range(0, 7)
	option = 'DEFAULT'
	mode = 'STRICT'
	primaries = range(0, 18)
	secondaries = range(0, 18)

	# lol 
	# to save space for the future, mega option should only be
	# available to gen 6 and 7 only, form option to gen 3 onwards
	retjson = []
	# Check, need to save space
	for g in generations:
		genresult = {}
		genresult['name'] = str(g)
		genresult['children'] = []
		for i in primaries:
			imresult = {}
			imresult['name'] = TYPES[i].lower()
			imresult['children'] = []
			for j in secondaries:
				# If they're the same fetch single typed
				if i == j:
					query = get_single_type_pokemon(
							gen = g + 1, 
							type_id = i + 1, 
							option = option)
				else:
				# Otherwise fetch from double type
					query = get_double_type_pokemon(
							gen = g + 1, 
							type_id1 = i + 1, 
							type_id2 = j + 1, 
							option = option, 
							mode = mode)

				imresult['children'].append({'name': TYPES[j].lower(), 'size': query.count()})
			genresult['children'].append(imresult)
		retjson.append(genresult)

	# Return minifed json
	return json.dumps(retjson, separators=(',',':'))

if __name__ == '__main__':
	with open('output/v5.json', 'w') as v3:
		retjson = generate_v2a_json()
		v3.write(retjson)
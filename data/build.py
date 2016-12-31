""" 
Build script.
"""
import os
import os.path
# Create new sqlite everytime
database_filename = 'poke.sqlite'
if os.path.isfile(database_filename): 
    os.system('rm ' + database_filename)


from Pokeclass import *
import csv
import sys
import inspect
import glob


# Reflection-ish
CLSMEMBERS = inspect.getmembers(sys.modules['Pokeclass'], inspect.isclass)
CLSMEMBERS = dict([m for m in CLSMEMBERS if m[1].__module__ == 'Pokeclass'])
DIR_LOCATION = os.path.dirname(os.path.realpath("__file__")) 
DATA_LOCATION = os.path.join(os.path.join(DIR_LOCATION, 'data'), '')


"""
Automatically fill all the tables using the files in the csv folder.
"""
def build():
	csvs = glob.glob(os.path.join(DATA_LOCATION, '*'))
	for csv in csvs:
		rows = get_rows(csv)
		csvname = csv.split("/")[-1].split(".")[0]
		classname = ''.join([x.title() for x in csvname.split('_')])
		
		print "Building " + classname
		# Go around the too many sql variables
		database.begin()
		for row in rows:
			CLSMEMBERS[classname].insert(row).execute()
		database.commit()


def get_rows(filename):
    data = load_data(filename)
    rows = []
    for index, info in enumerate(data):
        if index == 0: 
            labels = info
        else:
            values = info
            row = dict([(label, value) for label, value in zip(labels, values)])
            rows.append(row)

    return rows

"""
Helper functions for get_rows()
"""
def with_iter(context, iterable=None):
    if iterable is None:
        iterable = context
    with context:
        for value in iterable:
            yield value


def load_data(filename):
    # with_iter closes the file when it has finished
    return csv.reader(with_iter(open(filename, 'rt')), delimiter=',')


# Testing testing
if __name__ == '__main__':
	# Fill database with csv
	create_tables()
	build()
"""
http://stackoverflow.com/questions/1581183/prepared-statements-and-the-in-expression
https://google.github.io/styleguide/pyguide.html
https://github.com/coleifer/peewee
Redo SQLs

This database is pretty much static, read-only
PrimaryKeyField is autoincrementing
Reflection in Python
http://stackoverflow.com/questions/4513192/python-dynamic-class-names
http://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python
db_column 
https://github.com/coleifer/peewee/issues/44
Insert/Insert_Many generates SQL, need .execute()

Peewee things
http://www.blog.pythonlibrary.org/2014/07/17/an-intro-to-peewee-another-python-orm/
"""
from peewee import *
database_filename = 'poke.sqlite'
database = SqliteDatabase(database_filename)
database.set_autocommit(False)


"""
Create all the necessary tables for Pokemon. Declare all tables here.
"""
def create_tables():
	database.connect()
	database.create_tables([Ability, 
							Classification, 
							Competitive, 
							FinalEvolution,
							Generation,
							Pokemon,
							PokemonAbility,
							PokemonClassification,
							PokemonCompetitive,
							PokemonSprite,
							PokemonType,
							Type],
							safe=True)


class PokeModel(Model):
	class Meta:
		database = database


# Definition
class Generation(PokeModel):
	pk = IntegerField(primary_key=True) 
	name = CharField()


# Definition
class Type(PokeModel):
	pk = IntegerField(primary_key=True)
	name = CharField()
	gen = ForeignKeyField(Generation, to_field='pk', db_column='gen')


# Definition
class Ability(PokeModel):
	pk = IntegerField(primary_key=True)
	name = CharField()
	flavour_text = CharField()
	gen = ForeignKeyField(Generation, to_field='pk', related_name='ability_gen_introduced', db_column='gen')


# Definition
class Pokemon(PokeModel):
	pk = IntegerField(primary_key=True)
	species_id = IntegerField() # Should be self referential
	name = CharField()
	hp = IntegerField()
	attack = IntegerField()
	defense = IntegerField()
	sp_attack = IntegerField()
	sp_defense = IntegerField()
	speed = IntegerField()
	bst = IntegerField()
	height = IntegerField() 
	weight = IntegerField() 
	base_exp = IntegerField()
	gen = ForeignKeyField(Generation, to_field='pk', db_column='gen')
	is_default = BooleanField()

# Definition
class Classification(PokeModel):
	pk = IntegerField(primary_key=True)
	name = CharField()


# Definition
class Competitive(PokeModel):
	pk = IntegerField(primary_key=True)
	name = CharField()
	gen = ForeignKeyField(Generation, to_field='pk', db_column='gen')


# Many to many, sorta
class FinalEvolution(PokeModel):
	pk = IntegerField(primary_key=True)
	pokemon = ForeignKeyField(Pokemon, db_column='classification' )
	gen_start = ForeignKeyField(Generation, to_field='pk', related_name='evo_gen_start', db_column='gen_start')
	gen_until = ForeignKeyField(Generation, to_field='pk', related_name='evo_gen_until', db_column='gen_until') 


# Many to Many
class PokemonClassification(PokeModel):
	pk = IntegerField(primary_key=True)
	pokemon = ForeignKeyField(Pokemon, db_column='pokemon')
	classification = ForeignKeyField(Classification, db_column='classification')


# Many to Many
class PokemonCompetitive(PokeModel):
	pk = IntegerField(primary_key=True)
	pokemon = ForeignKeyField(Pokemon, db_column='pokemon')
	tier = ForeignKeyField(Competitive, db_column='tier')


# 1 - 1
class PokemonSprite(PokeModel):
	pk = IntegerField(primary_key=True)
	pokemon = ForeignKeyField(Pokemon, db_column='pokemon')
	spritename = CharField()


# Many to Many
class PokemonType(PokeModel):
	pk = IntegerField(primary_key=True)
	pokemon = ForeignKeyField(Pokemon, db_column='pokemon')
	pokemon_type = ForeignKeyField(Type, db_column='pokemon_type')
	slot = IntegerField()
	gen_start = ForeignKeyField(Generation, to_field='pk', related_name='type_gen_start', db_column='gen_start')
	gen_until = ForeignKeyField(Generation, to_field='pk', related_name='type_gen_until', db_column='gen_until')


# Many to Many
class PokemonAbility(PokeModel):
	pk = IntegerField(primary_key=True)
	pokemon = ForeignKeyField(Pokemon, db_column='pokemon')
	ability = ForeignKeyField(Ability, db_column='ability')
	slot = IntegerField()


if __name__ == "__main__":
	pass
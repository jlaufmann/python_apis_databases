'''

All of the following exercises should be done using sqlalchemy.

Using the provided database schema, write the necessary code to print information about the film and category table.

'''
import sqlalchemy as sa 
from pprint import pprint

engine = sa.create_engine('mysql+pymysql://root:JimSQL81!@localhost/sakila')
#connection = engine.connect()
metadata = sa.MetaData()
insp = sa.inspect(engine)

film = sa.Table('film', metadata, autoload=True, autoload_with=engine)
category = sa.Table('category', metadata, autoload=True, autoload_with=engine)

print(f"\nInformation about the film table:\n")
pprint(insp.get_columns('film'))
print(f"\nInformation about the category table:\n")
pprint(insp.get_columns('category'))

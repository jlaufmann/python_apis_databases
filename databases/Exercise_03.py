'''
Update all films in the film table to a rental_duration value of 10,
if the length of the movie is more than 150.

'''

import sqlalchemy as sa 
from pprint import pprint

engine = sa.create_engine('mysql+pymysql://root:JimSQL81!@localhost/sakila')
connection = engine.connect()
metadata = sa.MetaData()
#insp = sa.inspect(engine)

film = sa.Table('film', metadata, autoload=True, autoload_with=engine)
'''
print(f"Select all the actors with the first name of your choice:")
query = sa.select([actor]).where(actor.columns.first_name == 'GRETA').order_by(
	actor.columns.last_name)
result_proxy = connection.execute(query)
result_1 = result_proxy.fetchall()
pprint(result_1)
'''

# Update a record in the database:
query = sa.update(film).values(rental_duration=10).where(film.columns.length > 150)
result = connection.execute(query)

'''
Consider each of the tasks below as a separate database query. Using SQLAlchemy, which is the necessary code to:

- Select all the actors with the first name of your choice

- Select all the actors and the films they have been in

- Select all the actors that have appeared in a category of a comedy of your choice

- Select all the comedic films and sort them by rental rate

- Using one of the statements above, add a GROUP BY statement of your choice

- Using one of the statements above, add a ORDER BY statement of your choice

'''

import sqlalchemy as sa 
from pprint import pprint

engine = sa.create_engine('mysql+pymysql://root:JimSQL81!@localhost/sakila')
connection = engine.connect()
metadata = sa.MetaData()
#insp = sa.inspect(engine)

actor = sa.Table('actor', metadata, autoload=True, autoload_with=engine)
film_actor = sa.Table('film_actor', metadata, autoload=True, autoload_with=engine)
film = sa.Table('film', metadata, autoload=True, autoload_with=engine)
film_category = sa.Table('film_category', metadata, autoload=True, autoload_with=engine)
category = sa.Table('category', metadata, autoload=True, autoload_with=engine)

print(f"Select all the actors with the first name of your choice:")
query = sa.select([actor]).where(actor.columns.first_name == 'GRETA').order_by(
	actor.columns.last_name)
result_proxy = connection.execute(query)
result_1 = result_proxy.fetchall()
pprint(result_1)

'''
print(f"Select all the actors and the films they have been in:")
join_statement = actor.join(film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(film, film.columns.film_id == film_actor.columns.film_id)
query = sa.select([actor.columns.first_name, actor.columns.last_name, film.columns.title]).select_from(join_statement)
result_proxy = connection.execute(query)
result_2 = result_proxy.fetchall()
pprint(result_2)
'''

print(f"Select all the actors that have appeared in a category of a comedy of your choice:")
print(f"I'm taking this to be a comedy of rating NC-17")
# this means I don't care about the film title, every actor who has appeared in a sports comedy?
# comedy category: category_id = 5, name = 'Comedy'
# sports category: category_id = 15, name = 'Sports'
# film.column.rating: 'G', 'PG', 'PG-13', 'R', 'NC-17'
# There are 286 actors who have appeared in a comedy film
# There are 441 actors who have appeared in a sports film
# I want the subset of the actors who appeared in a sports comedy.
# Maybe I'm looking at this wrongly though.
join_statement = actor.join(
	film_actor, film_actor.columns.actor_id == actor.columns.actor_id).join(
	film, film.columns.film_id == film_actor.columns.film_id).join(
	film_category, film_category.columns.film_id == film.columns.film_id).join(
	category, category.columns.category_id == film_category.columns.category_id)
#query = sa.select([actor.columns.first_name, actor.columns.last_name, film.columns.title, film.columns.rating, category.columns.name]).select_from(
#	join_statement).where(sa.and_(category.columns.name == 'Comedy', film.columns.rating == 'NC-17'))
query = sa.select([sa.distinct(actor.columns.actor_id), actor.columns.first_name, actor.columns.last_name]).select_from(
	join_statement).where(
	sa.and_(category.columns.name == 'Comedy', film.columns.rating == 'NC-17')).order_by(
	actor.columns.first_name)
# I included the sa.distinct(actor.columns.actor_id) to eliminate duplicate entries for the same actor
result_proxy = connection.execute(query)
result_3 = result_proxy.fetchall()
pprint(result_3)
print(len(result_3))

# Ideally I would like to select all sports comedy's, but I don't know how to do that because I want to say:
# where(sa.and_(category.columns.name == 'Comedy', category.columns.name == 'Sports'))
# but that returns nothing.
# So as above, I have selected comedies rated NC-17?


print(f"Select all the comedic films and sort them by rental rate")
join_statement = film.join(
	film_category, film_category.columns.film_id == film.columns.film_id).join(
	category, category.columns.category_id == film_category.columns.category_id)
query = sa.select([film.columns.title, film.columns.rental_rate]).select_from(
	join_statement).where(category.columns.name == 'Comedy').order_by(
	sa.asc(film.columns.rental_rate))
result_proxy = connection.execute(query)
result_4 = result_proxy.fetchall()

#result_5 = result.proxy.fetchone()
#print(result_5.keys())

space = 25
print(f"{'title:': <{space}} rental_rate($):")
for res in result_4:
	print(f"{res['title']: <{space}} {res['rental_rate']}")

#pprint(result_4)
# this is not so nice, because the rental rate is being returned as: "Decimal('0.99')" or similar.

# Using one of the statements above, add a GROUP BY statement of your choice
# This isn't working for some reason.
# I tried making a sum, but couldn't get it to work:
# sa.func.sum(film.columns.rental_rate)
# but maybe I need to be summing something or doing something like that :)
# But I don't know how to sum something in sqlalchemy and then refer to it

print(f"Select all the comedic films and sort them by rental rate")
join_statement = film.join(
	film_category, film_category.columns.film_id == film.columns.film_id).join(
	category, category.columns.category_id == film_category.columns.category_id)
query = sa.select([film.columns.title, film.columns.rental_rate]).select_from(join_statement).where(
	category.columns.name == 'Comedy').order_by(
	sa.asc(film.columns.rental_rate))
result_proxy = connection.execute(query)
result_4 = result_proxy.fetchall()

#result_5 = result.proxy.fetchone()
#print(result_5.keys())

space = 25
print(f"{'title:': <{space}} rental_rate($):")
for res in result_4:
	print(f"{res['title']: <{space}} {res['rental_rate']}")


'''
sa.func.sum 

SELECT c.first_name, c.last_name, SUM(p.amount) as total_payments
FROM customer c
JOIN payment p
ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total_payments DESC;

query = sqlalchemy.select([film]).order_by(sqlalchemy.asc(film.columns.replacement_cost))
'''

# Using one of the statements above, add a ORDER BY statement of your choice
# That was easy enough. See first exercise with Greta.
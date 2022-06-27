import re
from sqlite3 import Row
import psycopg2
import matplotlib.pyplot as plt
import numpy as np

host = ""
dbname = ""
user = ""
password = ""
sslmode = "require"

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established...")

cursor = conn.cursor()

#Ερώτημα 1ο 
cursor.execute('SELECT COUNT(title),EXTRACT (YEAR FROM release_date) AS "Year" FROM "Movie" GROUP BY "Year" ORDER BY "Year"')
rows = cursor.fetchall()
zip(*rows)
plt.scatter(*zip(*rows))
plt.title('Number of movies per year')
plt.xlabel('Number of movies')
plt.ylabel('Year')
plt.show()

#Ερώτημα 2ο
cursor.execute('SELECT  DISTINCT(g.name) AS "Genres", COUNT(m.title) AS "Number of Movies" FROM "Movie" m JOIN "Movie_genres" mg ON m.id = mg.movie_id JOIN "Genre" g ON mg.genre_id = g.id GROUP BY g.name;')
rows = cursor.fetchall()
zip(*rows)
plt.scatter(*zip(*rows))
plt.title('Movies per Genre')
plt.xlabel('Genre')
plt.ylabel('Number of movies')
plt.show()

#Ερώτημα 3ο
cursor.execute('SELECT DISTINCT(g.name) AS "Genres",EXTRACT(YEAR FROM m.release_date) AS "Year",COUNT(m.title)  AS "Number of Movies" FROM  "Movie" m JOIN "Movie_genres" mg ON m.id = mg.movie_id JOIN "Genre" g ON mg.genre_id = g.id GROUP BY g.name,"Year" UNION SELECT  DISTINCT(g.name) AS "Genres",EXTRACT(YEAR FROM m.release_date) AS "Year", COUNT(m.title) AS "Number of Movies" FROM "Movie" m JOIN "Movie_genres" mg ON m.id = mg.movie_id JOIN "Genre" g ON mg.genre_id = g.id GROUP BY g.name, "Year" ORDER BY "Year";')
rows = cursor.fetchall()
y = [] #year
z = [] #count
x = [] #genres
for i in rows:
    x.append(i[0])
    y.append(i[1])
    z.append(i[2])
plt.scatter(y,x,z)
plt.title("Number of movies per genre and per year")
plt.xlabel("Year")
plt.ylabel("Genre")
plt.show()

#Ερώτημα 4ο
cursor.execute('SELECT EXTRACT(YEAR FROM release_date) AS "Year",MAX(budget) AS "Max_Budget" FROM "Movie" GROUP BY "Year" ORDER BY "Year";')
rows = cursor.fetchall()
zip(*rows)
plt.scatter(*zip(*rows))
plt.title("Max movie budget per year")
plt.xlabel('Year')
plt.ylabel('Budget')
plt.show()

#Ερώτημα 5ο
cursor.execute('SELECT  EXTRACT(YEAR FROM release_date) AS "Year", SUM(revenue) AS "Revenue" FROM "Movie" m JOIN "Movie_cast_project" mc ON m.id = mc.movie_id WHERE name = \'Johnny Depp\' GROUP BY "Year";')
rows = cursor.fetchall()
year = []
revenue = []
for i in rows:
    year.append(i[0])
    revenue.append(i[1])
plt.title("Johny Depp's revenue of movies for each year")
plt.xlabel('Year')
plt.ylabel('revenue (millions)')
plt.scatter(year,revenue)
plt.show()

#Ερώτημα 6ο
cursor.execute('SELECT DISTINCT(user_id) AS "User", AVG(rating) AS "Average Rating" FROM "Ratings" GROUP BY user_id ORDER BY user_id;')
rows = cursor.fetchall()
plt.title("Average rating per user")
plt.xlabel("User")
plt.ylabel("Rating")
zip(*rows)
plt.scatter(*zip(*rows))
plt.show()

#Ερώτημα 7ο
cursor.execute('SELECT DISTINCT(user_id) AS "User", COUNT(rating) AS "Number of Rating" FROM "Ratings" GROUP BY user_id ORDER BY user_id;')
rows = cursor.fetchall()
plt.title("Number of ratings per user")
plt.xlabel("User")
plt.ylabel("Number of ratings")
zip(*rows)
plt.scatter(*zip(*rows))
plt.show()

#Ερώτημα 8ο
cursor.execute('SELECT DISTINCT(user_id) AS "User" ,COUNT(rating) AS "Number of Ratings", AVG(rating) AS "Avarage Rating" FROM "Ratings" GROUP BY user_id ORDER BY user_id;')
rows = cursor.fetchall()
x = [] #user id 
y = [] #number of ratings
z = [] #average rating
for res in rows:
    x.append(res[0])
    y.append(res[1])
    z.append(res[2])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z)
plt.title("Number of ratings and average rating per user")
plt.xlabel("User")
plt.ylabel("Number of ratings")
plt.show()

#Ερωτημα 9ο
cursor.execute('SELECT DISTINCT(g.name) AS "Genre", AVG(rating) AS "Average Rating" FROM "Ratings" r JOIN "Movie_genres" mg ON r.movie_id = mg.movie_id JOIN "Genre" g ON mg.genre_id = g.id GROUP BY g.name ORDER BY 2;')
rows = cursor.fetchall()  
zip(*rows)
plt.scatter(*zip(*rows))
plt.title('Average rating per genre')
plt.xlabel('Genre')
plt.ylabel('Rating')
plt.show()  

conn.commit()
cursor.close()
conn.close()
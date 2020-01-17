# !/usr/bin/env/python3
# Copyright 2019 YueLiu liuyue2@bu.edu
# Program Goal: import the two datasets into mysql and join them together

# import libraries
import csv
import mysql.connector

#task1: import two .csv file
db_connection = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1', database='',
                              auth_plugin='mysql_native_password')
print(db_connection)
cursor = db_connection.cursor()
# insert the published_tweet.csv
try:
    with open('published_tweet.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        firstline = True
        sql = "INSERT INTO tweets (Tweets, id, keyword, location, text, target) VALUES (%s,%s,%s,%s,%s,%s)"
        for row in csv_reader:
            if firstline:
                firstline = False
                continue
            row = (', '.join(row))
            print(row)
            cursor.execute(sql, row)
            break

except:
    db_connection.rollback()
finally:
    db_connection.close()
# insert the sentiment_score.csv
try:
    with open('sentiment_score.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        firstline = True
        sql = "INSERT INTO sentiment (Tweets, score) VALUES (%s,%s)"
        for row in csv_reader:
            if firstline:
                firstline = False
                continue
            row = (', '.join(row))
            print(row)
            cursor.execute(sql, row)
            break
except:
    db_connection.rollback()
finally:
    db_connection.close()

# task2: join the two datasets together
db_connection = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1', database='',
                              auth_plugin='mysql_native_password')

cursor = db_connection.cursor()
sql = "SELECT \
  * \
  FROM tweets \
  INNER JOIN sentiment ON tweets.Tweets = sentiment.Tweets"
cursor.execute(sql)
myresult = cursor.fetchall()
for x in myresult:
  print(x)

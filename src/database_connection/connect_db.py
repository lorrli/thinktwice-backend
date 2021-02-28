#https://towardsdatascience.com/how-to-set-up-a-postgresql-database-on-amazon-rds-64e8d144179e
import psycopg2 as ps
from parse_excel import parse_excel
# define credentials
credentials = {
    'POSTGRES_ADDRESS':
    'database-1.cqt2ynkwdbyq.us-east-2.rds.amazonaws.com',  # change to your endpoint
    'POSTGRES_PORT': '5432',  # change to your port
    'POSTGRES_USERNAME': 'postgres',  # change to your username
    'POSTGRES_PASSWORD': '2xfydp2021!',  # change to your password
    'POSTGRES_DBNAME': 'postgres'
}  # change to your db name
#TODO: atm allowing inbound traffic from my IP address but might need to
# create connection and cursor
conn = ps.connect(host=credentials['POSTGRES_ADDRESS'],
                  database=credentials['POSTGRES_DBNAME'],
                  user=credentials['POSTGRES_USERNAME'],
                  password=credentials['POSTGRES_PASSWORD'],
                  port=credentials['POSTGRES_PORT'])

cur = conn.cursor()
#create Brand table
# cur.execute("""CREATE TABLE brand
#                 (id int PRIMARY KEY,
#                 name varchar(255) NOT NULL,
#                 transparency integer,
#                 worker_emp integer,
#                 env_mgmt integer,
#                 nonresponsive integer,
#                 url varchar(255)
#                 );""")
# # Commit table creation
# conn.commit()
# print("Table created successfully!")

#insert data
data = parse_excel()
insert_query = """INSERT INTO brand
                   (id, name, transparency, worker_emp, env_mgmt, nonresponsive)
                   VALUES (%s, %s, %s, %s, %s, %s);"""
cur.executemany(insert_query, data)
conn.commit()

#drop table
# cur.execute("""DROP TABLE Brand""")
# print("TABLE DROPPED")
# conn.commit()

cur.close()
conn.close()
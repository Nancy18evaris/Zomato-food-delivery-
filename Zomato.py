from faker import Faker
fake = Faker()
dir(fake)
import random
from datetime import time, timedelta, datetime

import pandas as pd
DataFrame = pd.DataFrame()
Faker.seed(random.randint(1,10000))


import mysql.connector
conn = mysql.connector.connect(
    host="gateway01.eu-central-1.prod.aws.tidbcloud.com",
    user="3QZvGaRzWhdvPdY.root",
    password="sLA9y6e33uqkwNJY",
    ssl_ca = "/path/to/D:\ca.pem.pem",
    port = "4000",
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Zomato;")
cursor.execute("USE Zomato;")


class Zomato :
  def __init__(self, host, user, password, ssl_ca, port, database):
    self.host = host
    self.user = user
    self.password = password
    self.ssl_ca = ssl_ca
    self.port = port
    self.database = database
    self.conn = None
    self.cursor = None
  def connect(self):
    self.conn = mysql.connector.connect(host = self.host, user = self.user, password = self.password, ssl_ca = self.ssl_ca,  port = self.port, database = self.database)
    self.cursor = self.conn.cursor()
    print("connection success")
  def creat_table(self, table_query):
    self.cursor.execute(table_query)
    self.conn.commit()
    print("table creation successful")
  def insert_list_of_tuple(self, insert_query, list_tuple):
    self.cursor.executemany(insert_query, list_tuple)
    self.conn.commit()
    print("insertion successful")

config = {"host":"gateway01.eu-central-1.prod.aws.tidbcloud.com", "user":"3QZvGaRzWhdvPdY.root", "port":4000, "password":"sLA9y6e33uqkwNJY", "ssl_ca":"/path/to/D:\ca.pem.pem", "database":"Zomato"}
db_obj = Zomato(**config)


cursor.execute("SHOW TABLES LIKE 'Customers'")
table_exists = cursor.fetchone()

cursor.fetchall()

if not table_exists:
    cursor.execute("""CREATE TABLE Customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone BIGINT NOT NULL,
    location VARCHAR(100),
    signup_date DATE NOT NULL,
    is_premium BOOLEAN DEFAULT 0,
    preferred_cuisine VARCHAR(50),
    total_orders INT DEFAULT 0 CHECK (total_orders >=0),
    average_rating DECIMAL(3,1) CHECK (average_rating BETWEEN 1.0 and 5.0));
    """)
    print("Customers table created successfully")
else:
    print("Customers table already exists")

cursor.execute("SHOW TABLES LIKE 'Restaurant'")
table_exists = cursor.fetchone()

cursor.fetchall()

if not table_exists:
    cursor.execute("""CREATE TABLE Restaurant(
    restaurant_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    cuisine_type VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    owner_name VARCHAR(100) NOT NULL,
    average_delivery_time INT NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    rating DECIMAL(3,1),
    total_orders INT DEFAULT 0 CHECK (total_orders >=0),
    is_active BOOLEAN DEFAULT 0);
    """)
    print("Restaurant table created successfully")
else:
    print("Restaurant table already exists")

cursor.execute("SHOW TABLES LIKE 'Order_table'")
table_exists = cursor.fetchone()

cursor.fetchall()

if not table_exists:
    cursor.execute("""CREATE TABLE Order_table (
    Order_id INT PRIMARY KEY AUTO_INCREMENT,
    Customer_id INT,
    Restaurant_id INT,
    Order_date DATE NOT NULL,
    Delivery_time TIME NOT NULL,
    Status ENUM('Pending', 'Delivered','Cancelled') NOT NULL,
    Total_amount DECIMAL(10,2) NOT NULL,
    Payment_mode ENUM('Credit Card', 'Cash', 'UPI') NOT NULL,
    Discount_applied DECIMAL(5,2) NOT NULL,
    Feedback_rating DECIMAL(3,1) CHECK (Feedback_rating BETWEEN 1.0 and 5.0),
    FOREIGN KEY (Customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (Restaurant_id) REFERENCES Restaurant(restaurant_id));
  """)
    print("Order_table created successfully")
else:
    print("Order_table already exists")

cursor.execute("SHOW TABLES LIKE 'Delivery_persons_table'")
table_exists = cursor.fetchone()

cursor.fetchall()

if not table_exists:
    cursor.execute("""CREATE TABLE Delivery_persons_table (
    Delivery_person_id INT PRIMARY KEY AUTO_INCREMENT,
    Delivery_person_name VARCHAR(100),
    contact_number VARCHAR(15),
    Vehicle_type ENUM('Bike', 'Car') NOT NULL,
    total_deliveries INT DEFAULT 0,
    average_rating DECIMAL(3,1) CHECK (average_rating BETWEEN 1.0 and 5.0),
    location VARCHAR(100));
    """)
    print("Delivery_persons_table created successfully")
else:
    print("Delivery_persons_table already exists")

cursor.execute("SHOW TABLES LIKE 'Delivery_table'")
table_exists = cursor.fetchone()

cursor.fetchall()

if not table_exists:
    cursor.execute("""CREATE TABLE Delivery_table (
    Delivery_id INT PRIMARY KEY AUTO_INCREMENT,
    Order_id INT,
    Delivery_person_id INT,
    Delivery_status ENUM('On the way', 'Delivered'),
    Distance Float Not NULL,
    Delivery_time TIME NOT NULL,
    Estimated_time TIME NOT NULL,
    Delivery_fee DECIMAL(5,2) NOT NULL,
    Vehicle_type ENUM('Bike', 'Car') NOT NULL,
    FOREIGN KEY (Order_id) REFERENCES Order_table(Order_id),
    FOREIGN KEY (Delivery_person_id) REFERENCES Delivery_persons_table(Delivery_person_id));
    """)
    print("Delivery_table created successfully")
else:
    print("Delivery_table already exists")

cursor.execute("SHOW TABLES LIKE 'Youth_Customers'")
table_exists = cursor.fetchone()

cursor.fetchall()

if not table_exists:
    cursor.execute("""CREATE TABLE Youth_Customers (
    Youth_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL CHECK (age BETWEEN 18 AND 26),
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    location VARCHAR(100));
    """)
    print("Youth_Customers created successfully")
else:
    print("Youth_Customers already exists")


def generate_Customers(num_records):
  Customers =[]
  for customer_id in range(1001, 1001 + num_records):

     while True:
        email = fake.unique.email()
        cursor.execute("SELECT 1 FROM Customers WHERE email = %s", (email,))
        if not cursor.fetchone(): 
            break


     Customers.append({
          "customer_id": customer_id,
          "name": fake.unique.name(),
          "email":email,
          "phone": random.randint(9000000000, 9999999999),
          "location": fake.unique.address(),
          "signup_date": fake.date_between(start_date="-2y",end_date ="today"),
          "is_premium" : random.choice([0, 1]),
          "preferred_cuisine": random.choice(["Indian", "Italian", "French", "Mexican", "Chinese", "Japanese", "Vietnamese"]),
          "total_orders" : random.randint(1, 100),
          "average_rating" : round(random.uniform(1.0, 5.0), 1)
          })
  return pd.DataFrame(Customers)


df = generate_Customers(1000)
print(df)


abc = [tuple(i) for i in generate_Customers(1000).to_numpy()]

abc

try:
 IQ = """INSERT INTO Customers (customer_id, name, email, phone, location, signup_date, is_premium, preferred_cuisine, total_orders, average_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

 for index, row in generate_Customers(1000).iterrows():
    cursor.execute(IQ, (row['customer_id'], row['name'], row['email'], row['phone'], row['location'], row['signup_date'], row['is_premium'], row['preferred_cuisine'], row['total_orders'], row['average_rating']))

 conn.commit()
except:
 pass    

def generate_Restaurant(num_records):
  Restaurant =[]
  cursor = conn.cursor()

  for restaurant_id in range(5001, 5001 + num_records):
     Restaurant.append({
          "restaurant_id": restaurant_id,
          "name": random.choice(["Sangeetha", "Wokasi", "Le Petit Four", "Chalet du Steak", "A2B", "Ombra", "Holbox", "Shoukouwa", "Gia", "Kwonsooksoo"]),
          "cuisine_type": random.choice(["Indian", "Italian", "French", "Mexican", "Chinese", "Japanese", "Vietnamese", "Korean"]),
          "location": fake.unique.address(),
          "owner_name":fake.name(),
          "average_delivery_time" : random.randint(10,60),
          "contact_number": random.randint(9000000000, 9999999999),
          "rating":round(random.uniform(1.0, 5.0), 1),
          "total_orders": random.randint(1, 500),
          "is_active" : random.choice([0, 1])
       })
  return pd.DataFrame(Restaurant)

df= generate_Restaurant(100)
print(df)


xyz = [tuple(i) for i in generate_Restaurant(100).to_numpy()]

xyz
try:
 IQ = """INSERT INTO Restaurant (restaurant_id, name, cuisine_type, location, owner_name, average_delivery_time, contact_number, rating, total_orders, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

 for index, row in generate_Restaurant(100).iterrows():
   cursor.execute(IQ, (row['restaurant_id'], row['name'], row['cuisine_type'], row['location'], row['owner_name'], row['average_delivery_time'], row['contact_number'], row['rating'], row['total_orders'], row['is_active']))
except:
 pass


def generate_Order_table(num_records, customer_ids, restaurant_ids):
    Order_table = []
    for _ in range(num_records):
        customer_id = random.choice(customer_ids)  
        restaurant_id = random.choice(restaurant_ids)  
        order_date = fake.date_between(start_date="-2y", end_date="today")
        delivery_time = time(hour=random.randint(10,23),minute=random.randint(0,59),second=random.randint(0,59))

        Order_table.append((
            customer_id,  
            restaurant_id,
            order_date,
            delivery_time,
            random.choice(['Pending', 'Delivered', 'Cancelled']),
            random.randint(100, 2000),
            random.choice(['Credit Card', 'Cash', 'UPI']),
            round(random.uniform(0, 1.0), 2),
            round(random.uniform(0, 5.0))
        ))

    return Order_table


customer_ids = list(range(1001, 2001))  
restaurant_ids = list(range(5001, 5101))  
cursor.execute("SELECT MAX(order_id) FROM Order_table")  
max_order_id = cursor.fetchone()[0]
if max_order_id is None:
    max_order_id = 0  
try:    
 IQ = """
 INSERT INTO Order_table(
    Customer_id, Restaurant_id, Order_date,
    Delivery_time, Status, Total_amount, Payment_mode,
    Discount_applied, Feedback_rating
 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
 """
except:
 pass     
df = generate_Order_table(10000, customer_ids, restaurant_ids)
cursor.executemany(IQ, df)

print(f"{len(df)} orders inserted successfully!")



print(df)


def generate_Delivery_persons_table(num_records):
    Delivery_persons_table = []

    for Delivery_person_id in range(501, 501 + num_records):
        Delivery_persons_table.append({
            "Delivery_person_id": Delivery_person_id,
            "Delivery_person_name": fake.unique.name(),
            "contact_number": random.randint(9000000000, 9999999999),
            "Vehicle_type": random.choice(['Bike', 'Car']),
            "total_deliveries": random.randint(5, 10),
            "average_rating": round(random.uniform(0, 5.0), 2),
            "location": fake.unique.address(),
        })

    return pd.DataFrame(Delivery_persons_table)

df = generate_Delivery_persons_table(500)
print(df)


try:
 IQ = """INSERT INTO Delivery_persons_table (Delivery_person_id, Delivery_person_name, contact_number, Vehicle_type, total_deliveries, average_rating, location)
 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
except:
   pass

df = generate_Delivery_persons_table(500)  

for index, row in df.iterrows():
    cursor.execute(IQ, (
        row['Delivery_person_id'],
        row['Delivery_person_name'],
        row['contact_number'],
        row['Vehicle_type'],
        row['total_deliveries'],
        row['average_rating'],
        row['location']
    ))

print(f"{len(df)} delivery persons inserted successfully!")



cursor.execute("SELECT Order_id FROM Order_table")
existing_order_ids = [row[0] for row in cursor.fetchall()]


cursor.execute("SELECT Delivery_person_id FROM Delivery_persons_table")
existing_delivery_person_ids = [row[0] for row in cursor.fetchall()]

if not existing_order_ids or not existing_delivery_person_ids:
    print("Error: No valid Order IDs or Delivery Person IDs found. Insert data into those tables first.")
    
    


def generate_Delivery_table(num_records, order_ids, delivery_person_ids):
    Delivery_table = []
    for _ in range(num_records):
        order_id = random.choice(order_ids)
        delivery_person_id = random.choice(delivery_person_ids)
        order_date = fake.date_between(start_date="-2y", end_date="today")
        delivery_time = time(hour=random.randint(10,23),minute=random.randint(0,59),second=random.randint(0,59))
        delivery_datetime = datetime.combine(datetime.today(),delivery_time)
        estimated_time = delivery_datetime + timedelta(minutes=random.randint(10, 60))
        Delivery_table.append((
            order_id,
            delivery_person_id,
            random.choice(['On the way', 'Delivered']),
            random.randint(1, 11),
            delivery_time,
            estimated_time,
            random.randint(50, 100),
            random.choice(['Bike', 'Car'])
        ))
    return pd.DataFrame(Delivery_table, columns=['Order_id', 'Delivery_person_id', 'Delivery_status', 'Distance', 'Delivery_time', 'Estimated_time', 'Delivery_fee', 'Vehicle_type'])

df = generate_Delivery_table(500, existing_order_ids, existing_delivery_person_ids)
print(df)

try:
 IQ = """
 INSERT INTO Delivery_table (Order_id, Delivery_person_id, Delivery_status, Distance, Delivery_time, Estimated_time, Delivery_fee, Vehicle_type)
 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
 """
except:
 pass     

df = generate_Delivery_table(500, existing_order_ids, existing_delivery_person_ids)
for index, row in df.iterrows():
  cursor.execute(IQ, (row['Order_id'],
                      row['Delivery_person_id'],
                      row['Delivery_status'],
                      row['Distance'],
                      row['Delivery_time'],
                      row['Estimated_time'],
                      row['Delivery_fee'],
                      row['Vehicle_type'] ))

print(f"{len(df)} delivery table inserted successfully!")



def create_Youth_Customers(num_records):
  Youth_Customers =[]
  for Youth_id in range(1801, 1801 + num_records):

     while True:
        email = fake.unique.email()
        cursor.execute("SELECT 1 FROM Youth_Customers WHERE email = %s", (email,))
        if not cursor.fetchone(): 
            break

     Youth_Customers.append({
          "Youth_id": Youth_id,
          "name": fake.unique.name(),
          "age":  random.randint(18, 27),
          "email":email,
          "phone": random.randint(9000000000, 9999999999),
          "location":fake.unique.address()
     })
  return pd.DataFrame(Youth_Customers)


df = create_Youth_Customers(50)
print(df)


pqr = [tuple(i) for i in create_Youth_Customers(50).to_numpy()]

pqr

try:
 IQ = """INSERT INTO Youth_Customers (Youth_id, name, age, email, phone, location)  VALUES (%s, %s, %s, %s, %s, %s)"""


 for index, row in create_Youth_Customers(50).iterrows():
     cursor.execute(IQ, (row['Youth_id'], row['name'], row['age'], row['email'], row['phone'], row['location']))
 conn.commit()
except:
 pass


print(f"{len(df)} Youth Customers inserted successfully!")

conn.commit()
cursor.close()
conn.close()

print("Database and tables created successfully!")



      




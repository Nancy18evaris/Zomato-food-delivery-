from faker import Faker
fake = Faker()
dir(fake)
import random
from datetime import time, timedelta, datetime


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
cursor.execute("CREATE DATABASE IF NOT EXISTS Zomato_food_delivery;")
cursor.execute("USE Zomato_food_delivery;")


import pandas as pd
import streamlit as st
import PIL 
from PIL import Image



def Add_Youth_Customer(name, age, email, phone, location):
    cursor.execute(f"""
        INSERT INTO Youth_Customers (name, age, email, phone, location)
        VALUES ('{name}', {age}, '{email}', '{phone}', '{location}');
    """)
    conn.commit()

# Update Youth Customer Function
def Update_Youth_Customer(selected_id, new_name, new_age, new_email, new_phone, new_location):
    cursor.execute(f"""
        UPDATE Youth_Customers 
        SET name = '{new_name}', age = {new_age}, email = '{new_email}', 
            phone = '{new_phone}', location = '{new_location}' 
        WHERE Youth_id = {selected_id};
    """)
    conn.commit()

# Delete Youth Customer Function
def Delete_Youth_Customer(delete_id):
    cursor.execute(f"DELETE FROM Youth_Customers WHERE Youth_id = {delete_id};")
    conn.commit()



st.set_page_config(page_title="Zomato Delivery App", page_icon="🍽️", layout="wide")
    
    # Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    
def login():
    st.title("🔐 Login to Zomato App")
    username = st.text_input("Username", value="", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    
    if st.button("Login"):
        if username == "Nancy" and password == "abcd1234": 
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password")

    if st.session_state.authenticated:
      st.success("Login Successful! Redirecting to the dashboard...")        

def home_page():
    st.title("🎉 Welcome to Zomato Delivery App")
    st.image("D:/Zomato Logo.png", caption="Zomato Food Delivery", use_container_width=True)
    st.success("Enjoy the best food delivery service!")
    st.balloons()

def menu_section():
    menu_choice = st.radio("Menu", ["TABLES", "QUERY"])
    if menu_choice == "TABLES":    
        options = st.selectbox("TABLES", ["Customers", "Restaurant", "Order_table", "Delivery_persons_table", "Delivery_table"],placeholder = 'Select', index = 0)
        cursor.execute(f"SELECT * FROM {options};")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df)

    elif menu_choice == 'QUERY':                           
        query_options = [ "1.Most popular cuisines based on orders", 
                                   "2.Top restaurants by total revenue",
                                   "3.Most popular restaurants by number of orders",
                                   "4.Most common delivery vehicle type",
                                   "5.Customers with highest feedback ratings",
                                   "6.Delivery personnel with most orders completed",
                                   "7.Customer order preferences based on cuisines",
                                   "8.Most popular cuisine among customers",
                                   "9.Top Spending Customers",
                                   "10.Count of Cancelled and Delayed Orders",
                                   "11.Locations with highest number of Orders",
                                   "12.Most Popular Payment Method",
                                   "13.Average distance covered by delivery personnel",
                                   "14.Fastest Restaurants Based on Estimated Delivery Time",
                                   "15.Delivered Orders Based on Date Range and Restaurant id",
                                   "16.Active French restaurants",
                                   "17.Premium customers",
                                   "18.Inactive Japanese restaurants",
                                   "19.Delivery Persons Who Delivered a Distance of 10 km",
                                   "20.Delivery Persons Who Used Car for Delivery"]
        selected_query = st.selectbox("Queries", query_options)
                                                                                                                    
        queries = {"1.Most popular cuisines based on orders":
                    """
                    SELECT Cuisine_type, COUNT(Order_id) AS order_count
                    FROM Restaurant
                    JOIN Order_table ON Restaurant.Restaurant_id = Order_table.Restaurant_id
                    GROUP BY Cuisine_type
                    ORDER BY order_count DESC;
                    """,
                    
                   "2.Top restaurants by total revenue":
                    """
                    SELECT Restaurant_id, SUM(Total_amount) AS total_revenue
                    FROM Order_table
                    GROUP BY Restaurant_id
                    ORDER BY total_revenue DESC
                    LIMIT 10;
                    """,

                    "3.Most popular restaurants by number of orders":
                    """
                    SELECT Restaurant_id, COUNT(Order_id) AS total_orders
                    FROM Order_table
                    GROUP BY Restaurant_id
                    ORDER BY total_orders DESC
                    LIMIT 10;
                    """,
                    

                    "4.Most common delivery vehicle type":
                    """
                    SELECT Vehicle_type, COUNT(*) AS usage_count
                    FROM Delivery_table
                    GROUP BY Vehicle_type
                    ORDER BY usage_count DESC;
                    """,
                    

                   "5.Customers with highest feedback ratings":
                    """
                    SELECT Customer_id, AVG(Feedback_rating) AS avg_rating
                    FROM Order_table
                    WHERE Feedback_rating IS NOT NULL
                    GROUP BY Customer_id
                    ORDER BY avg_rating DESC
                    LIMIT 10;
                    """,
                    

                   "6.Delivery personnel with most orders completed":
                    """
                    SELECT Delivery_person_id, COUNT(Delivery_id) AS completed_deliveries
                    FROM Delivery_table
                    GROUP BY Delivery_person_id
                    ORDER BY completed_deliveries DESC
                    LIMIT 10;
                     """,
                        
                    "7.Customer order preferences based on cuisines":
                    """
                    SELECT preferred_cuisine, COUNT(*) AS order_count
                    FROM Customers
                    JOIN Order_table ON Customers.Customer_id = Order_table.Customer_id
                    GROUP BY preferred_cuisine
                    ORDER BY order_count DESC;
                    """,
                    

                    "8.Most popular cuisine among customers":
                    """
                    SELECT preferred_cuisine, COUNT(*) AS total_customers
                    FROM Customers
                    GROUP BY preferred_cuisine
                    ORDER BY total_customers DESC;
                    """,
                    

                    "9.Top Spending Customers":
                    """
                    SELECT customer_id, SUM(total_amount) AS Total_Spent
                    FROM Order_table
                    GROUP BY customer_id
                    ORDER BY Total_Spent DESC
                    LIMIT 10;
                    """,
                    

                    "10.Count of Cancelled and Delayed Orders":
                    """
                    SELECT status, COUNT(*) AS Order_Count
                    FROM Order_table
                    WHERE status IN ('Cancelled', 'Pending')
                    GROUP BY status;
                    """,
                
                   "11.Locations with highest number of Orders":
                    """
                   SELECT r.location, COUNT(o.order_id) AS Total_Orders
                   FROM Order_table o
                   JOIN Restaurant r ON o.restaurant_id = r.restaurant_id
                   GROUP BY r.location
                   ORDER BY Total_Orders DESC;
                   """,
               
                  "12.Most Popular Payment Method":
                  """
                  SELECT payment_mode, COUNT(*) AS Usage_Count
                  FROM Order_table
                  GROUP BY payment_mode
                  ORDER BY Usage_Count DESC;
                 """,
                

                 "13.Average distance covered by delivery personnel":
                 """
                 SELECT Delivery_person_id, AVG(Distance) AS avg_distance
                 FROM Delivery_table
                 GROUP BY Delivery_person_id
                 ORDER BY avg_distance DESC;
                 """,

                 "14.Fastest Restaurants Based on Estimated Delivery Time":
                  """
                 SELECT 
                 D.Order_id,
                 D.Delivery_time,
                 D.Estimated_time,
                 TIMESTAMPDIFF(MINUTE, D.Delivery_time, D.Estimated_time) AS estimated_delivery_in_minutes
                 FROM 
                 Delivery_table D
                 JOIN 
                 Order_table O ON D.Order_id = O.Order_id
                 WHERE 
                 O.Order_date BETWEEN '2023-12-24' AND  '2024-01-08';
                 """,

                 "15.Delivered Orders Based on Date Range and Restaurant id":
                 """
                 SELECT 
                 Order_id, 
                 Customer_id, 
                 Restaurant_id, 
                 Order_date, 
                 Delivery_time, 
                 Status
                 FROM
                 Order_table
                 WHERE 
                 Status = 'Delivered'
                 AND Order_date BETWEEN '2023-12-01' AND '2024-01-31'
                 AND Restaurant_id = 5001;
                 """,

                 "16.Active French restaurants":
                 """
                 SELECT *
                 FROM Restaurant
                 WHERE is_active = 1
                 AND cuisine_type = 'French';
                 """,
               
                 "17.Premium customers":
                 """
                 SELECT *
                 FROM Customers
                 WHERE is_premium = 1;
                 """,
               

                 "18.Inactive Japanese restaurants":
                 """
                 SELECT *
                 FROM Restaurant
                 WHERE is_active = 0
                 AND cuisine_type = 'Japanese';
                 """,
                
                 "19.Delivery Persons Who Delivered a Distance of 10 km":
                 """
                 SELECT Delivery_person_id, Distance
                 FROM Delivery_table
                 WHERE Distance = 10;
                 """,
               

                 "20.Delivery Persons Who Used Car for Delivery":
                 """
                 SELECT dp.Delivery_person_id,
                 dp.Delivery_person_name,
                 dp.contact_number,
                 dp.Vehicle_type,
                 dp.total_deliveries,
                 dp.average_rating
                 FROM Delivery_persons_table dp
                 JOIN Delivery_table d ON dp.Delivery_person_id = d.Delivery_person_id
                 WHERE dp.Vehicle_type = 'Car';
                 """,
        }
    
        cursor.execute(queries[selected_query])
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df)

def crud_operations():
    st.title("CRUD Operations on Youth Customers")
    action = st.selectbox("Select Action", ["CREATE", "READ", "UPDATE", "DELETE"])
    
    if action == "CREATE":
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1)
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        location = st.text_input("Location")
        
        if st.button("Add Customer"):
            cursor.execute(f"INSERT INTO Youth_Customers (name, age, email, phone, location) VALUES ('{name}', {age}, '{email}', '{phone}', '{location}');")
            conn.commit()
            st.success(f"New Customer {name} Added Successfully!")
    
    elif action == "READ":
        cursor.execute("SELECT * FROM Youth_Customers;")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        st.dataframe(df)
    
    elif action == "UPDATE":
        cursor.execute("SELECT * FROM Youth_Customers;")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        
        if not df.empty:
            user_ids = df["Youth_id"].tolist()
            selected_id = st.selectbox("Select a Youth ID to Update", user_ids)
            selected_user = df[df["Youth_id"] == selected_id].iloc[0]
            new_name = st.text_input("Name", selected_user["name"])
            new_age = st.number_input("Age", value=selected_user["age"], min_value=1)
            new_email = st.text_input("Email", selected_user["email"])
            new_phone = st.text_input("Phone", selected_user["phone"])
            new_location = st.text_input("Location", selected_user["location"])
            
            if st.button("Update Customer"):
                cursor.execute(f"UPDATE Youth_Customers SET name = '{new_name}', age = {new_age}, email = '{new_email}', phone = '{new_phone}', location = '{new_location}' WHERE Youth_id = {selected_id};")
                conn.commit()
                st.success(f"Customer ID {selected_id} Updated Successfully!")
    
    elif action == "DELETE":
        cursor.execute("SELECT * FROM Youth_Customers;")
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        
        if not df.empty:
            user_ids = df["Youth_id"].tolist()
            delete_id = st.selectbox("Select a Youth ID to Delete", user_ids)
            
            if st.button("Delete Customer"):
                cursor.execute(f"DELETE FROM Youth_Customers WHERE Youth_id = {delete_id};")
                conn.commit()
                st.warning(f"Customer ID {delete_id} Deleted Successfully!")

def logout():
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.success("Logged Out Successfully!")
        st.rerun()

if not st.session_state.authenticated:
    login()

else:
    with st.sidebar:
        st.title("Navigation")
        selected_page = st.radio("Go to", ["Home", "Menu", "CRUD Operations", "Logout"])
        st.session_state.page = selected_page

    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Menu":
        menu_section()
    elif st.session_state.page == "CRUD Operations":
        crud_operations()
    elif st.session_state.page == "Logout":
        logout()




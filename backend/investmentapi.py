# from app import app, login_required, request, render_template,session, Crud, validate_csrf, flash
from dataform import InvestmentForm

import pymysql
def connect_to_database():
    investment_conn = pymysql.connect(
            host= 'investment-db.coyfqttc1msv.ap-northeast-1.rds.amazonaws.com', 
            port = 3306,
            user = 'nanhtuanfly', 
            password = 'Awesome123',
            charset='utf8mb4',
            db = 'investment_schema',
            cursorclass=pymysql.cursors.DictCursor
            )
    return investment_conn

#Create the database for investment 
def create_database(investment_conn):
    with investment_conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investments (
                investment_id VARCHAR(256) PRIMARY KEY,
                investment_poster_id VARCHAR(255),
                business_registration VARCHAR(255),
                business_address VARCHAR(255),
                company_name VARCHAR(255) ,
                current_round INT,
                presentation TEXT ,
                pictures TEXT,
                financial_situation TEXT ,
                approved BOOLEAN
            ) 
        """)
# Create the customers table
    with investment_conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT NOT NULL,
                investment_id INT NOT NULL,
                amount_invested INT NOT NULL,
                currency VARCHAR(255) NOT NULL,
                PRIMARY KEY (customer_id, investment_id),
                FOREIGN KEY (investment_id) REFERENCES investments(investment_id)
            ) ENGINE=InnoDB;
        """)

    investment_conn.commit()
    return 
# Check if the investments table exists

def check_database(investment_conn):
    with investment_conn.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE 'investments'")
        result = cursor.fetchone()

    if result:
        print("The investments table exists!")
    else:
        print("The investments table does not exist.")

    # Check if the customers table exists
    with investment_conn.cursor() as cursor:
        cursor.execute("SHOW TABLES LIKE 'customers'")
        result = cursor.fetchone()

    if result:
        print("The customers table exists!")
    else:
        print("The customers table does not exist.")


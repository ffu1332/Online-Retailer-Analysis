import mysql.connector
from mysql.connector import Error



class MysqlDB:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.password = 'admin'
        self.db = "online_retailer_analysis"
        self.charset = 'utf8'
        self.buffered = True  
        # self.conn = self.connect()


    def connect(self):  
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            buffered=self.buffered
        )
        if self.conn.is_connected():
            db_Info = self.conn.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = self.conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    def save_mysql(self, current_time, plat_id, platform, status_list, 
                   product_list, past_prices, price_list, product_url_list):
        if not self.conn.is_connected():
            self.connect()  # Connect to database


        cursor = self.conn.cursor() # create a cursor object to perform various SQL operations
        
        check_repeat_sameday_sql = ("SELECT * FROM sasa WHERE Date = %s AND Product_Link = %s")
        cursor.execute(check_repeat_sameday_sql, (current_time, product_url_list)) 
        result = cursor.fetchone()

        if result is None:
            sql = ("INSERT INTO sasa (Date, Plat_ID, Platform, Product_State, Product_Title, Original_Price, Discount_Price, Product_Link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            try: 
                cursor.execute(sql, (current_time, plat_id, platform, status_list, 
                    product_list, past_prices, price_list, product_url_list))
                
                self.conn.commit()
                print("Insert successful!")

            except Exception as e:
                print('Error:', e)
                self.conn.rollback()
            finally:
                cursor.close()
        else:
            print("Records for the same item already exist and will not be added to the database.")
            cursor.close()



    def create_table(self):
        # self.connect() 
        cursor = self.conn.cursor()

        try:
            table_names = ['SASA']

            for table_name in table_names:
                # Check if the table already exists
                cursor.execute(f"SHOW TABLES LIKE '{table_name.lower()}'")
                existing_tables = cursor.fetchall()

                if existing_tables:
                    print(f"Table '{table_name}' already exists.")
                    cursor.close()
                else:
                    mySql_insert_query = f"""CREATE TABLE {table_name.lower()}
                                            (Date DATE, 
                                            Plat_ID TEXT, 
                                            Platform VARCHAR(20), 
                                            Product_State VARCHAR(20),
                                            Product_Title VARCHAR(255), 
                                            Original_Price DECIMAL(10,2), 
                                            Discount_Price DECIMAL(10,2), 
                                            Product_Link TEXT)"""
                    cursor.execute(mySql_insert_query)
                    print(f"Table '{table_name}' created")
            
            self.conn.commit()
        except Exception as e:
            print('Error:', e)
            self.conn.rollback()
        finally:
            cursor.close()
        






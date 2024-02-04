import pandas as pd
import json
from utils import DEBUG
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class MySql_Interface:
    def __init__(self):
        '''
        This constructor initializes an interface to the MySQL DB connection using SQLAlchemy.
        '''
        try:
            print(
                "=== [Initializing MySQL Interface] Begin") if DEBUG == True else None

            with open('credentials.json', 'r') as file:
                datum = json.load(file)

            db_url = "mysql+mysqlconnector://{}:{}@{}/{}".format(
                datum["username"], datum["password"], datum["ip_address"], datum["database"])

            self.cnx = create_engine(db_url)

            print("\t=> MySQL Connection Successful.") if DEBUG == True else None

        except SQLAlchemyError as err:
            print(
                f"=== Failed to connect to DB due to the following error: \n\n\t\t{err}\n")
            print("=> Terminating application.")
            exit()

        print("=== [Initializing MySQL Interface] End") if DEBUG == True else None

    def close_cnx(self):
        '''
        This function closes the connection between the application and MySql.
        '''
        try:
            print("=== [Closing Connection Begin]") if DEBUG == True else None
            self.cnx.dispose()
            print("\t=> Cnx closed successfully.") if DEBUG == True else None
            print("=== [Closing Connection End]") if DEBUG == True else None

        except SQLAlchemyError as err:
            print(
                f"=== Failed to close to the following error: \n\n\t\t{err}\n")

    def send_query(self, query: str):
        '''
        Function to execute queries specific queries from MySQL based on user input.

        Args:
        Query (string): A legal SQL Query to execute

        Returns:
        Dataframe: Results of a select query in a pandas dataframe format.

        None: If running an insert or update query.
        '''

        df = None
        success = False

        print("=== [Send_Query Begin]") if DEBUG == True else None

        if "SELECT" in query.upper():
            print(f"\t=> Running a SELECT query: {query}") if DEBUG == True else None

            try:
                df = pd.read_sql_query(query, self.cnx)
                success = True
            except SQLAlchemyError as err:
                print(f"\n\t> Unable to read data from query: \n\n\t{err}")

        else:

            if DEBUG == True:
                print(f"\t=> Running an INSERT query: {query.strip()}") if "INSERT" in query else print(f"\t=> Running an Update query: {query.strip()}")
            
            with self.cnx.connect() as connection:
                try:
                    connection.execute(text(query.strip()))
                    connection.commit()
                    success = True
                except SQLAlchemyError as err:
                    print(
                        f"\n\t> Cannot update due to the following error:\n\n\t{err}")

        print("=== [Send_Query End]") if DEBUG == True else None

        return (df, success)
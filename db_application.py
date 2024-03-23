import psycopg2
from psycopg2 import connect

connection = None

def main():
    # Ask user for their username and password for PostgreSQL
    username = input("PostgreSQL username: ")
    password = input("PostgreSQL password: ")

    try:
        connectToDatabase(username, password)
    except Exception as e:
        print("Error connecting to HealthAndFitnessClubManagementSystem database: ", e)
        return

def showMemberMenu():
    return 1

def showTrainerMenu():
    return 2

# Creates and Connects to a new database titled HealthAndFitnessClubManagementSystem
def connectToDatabase(username, password):
    global connection
    connection = psycopg2.connect(database="HealthAndFitnessClubManagementSystem", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True
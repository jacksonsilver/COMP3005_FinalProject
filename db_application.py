import psycopg2
from psycopg2 import connect

connection = None
current_user = None

def main():
    # Ask user for their username and password for PostgreSQL
    username = input("PostgreSQL username: ")
    password = input("PostgreSQL password: ")

    try:
        connectToDatabase(username, password)
    except Exception as e:
        print("Error connecting to HealthAndFitnessClubManagementSystem database: ", e)
        return
    
    while(True):
        print("\n1. Login to an existing account")
        print("2. Create a new account")
        print("3. Access Admin Menu")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            showLoginMenu()
        elif choice == "2":
            showCreateAccountMenu()
        elif choice == "3":
            return
        elif choice == "4":
            connection.close()
            return
        else:
            print("Invalid choice. Please try again.")

def showLoginMenu():
    account_type = input("\nEnter your account type (M - Member or T - Trainer): ")

    # Can only login to Member or Trainer accounts
    if account_type != "M" and account_type != "T":
        print("Invalid account type. Please try again.")
        return
    
    name = input("Enter your account name: ")
    password = input("Enter your account password: ")

    try:
        if verifyCredentials(name, password, account_type):
            global current_user
            current_user = name
            if(account_type == "M"):
                showMemberMenu()
            else:
                showTrainerMenu()
        else:
            print("Invalid credentials. Please try again.")
    except Exception as e:
        print("Error verifying credentials", e) 

# Checks to see if user with name and password exists for Members or Trainers
def verifyCredentials(name, password, account_type):
    if account_type == "M":
        table = "Members"
    else:
        table = "Trainers"

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE name = %s AND password = %s", (name, password))
    output = cursor.fetchall()
    cursor.close()
    return len(output) == 1

def showCreateAccountMenu():
    account_type = input("\nEnter your account type (M - Member or T - Trainer): ")

    # Can only login to Member or Trainer accounts
    if account_type != "M" and account_type != "T":
        print("Invalid account type. Please try again.")
        return
    
    name = input("Enter your account name: ")
    password = input("Enter your account password: ")

     

def showMemberMenu():
    print("Hi member %s", current_user)

def showTrainerMenu():
    print("Hi trainer %s", current_user)
    
def showAdminMenu():
    return 1

# Creates and Connects to a new database titled HealthAndFitnessClubManagementSystem
def connectToDatabase(username, password):
    global connection
    connection = psycopg2.connect(database="HealthAndFitnessClubManagementSystem", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True

if __name__ == "__main__":
    main()
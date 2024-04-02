import psycopg2
from psycopg2 import connect
import datetime

from member import *
from trainer import *
import admin
from admin import *

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
            try:
                showLoginMenu()
            except Exception as e:
                print("Error logging in, ", e)
        elif choice == "2":
            try:
                showCreateAccountMenu()
            except Exception as e:
                print("Error creating account, ", e)
        elif choice == "3":
            name = input("\nEnter your admin name: ")
            password = input("Enter your admin password: ")
            try:
                if verifyCredentials(name, password, "A"):
                    admin.showAdminMenu(connection)
                else:
                    print("Invalid credentials.")
            except Exception as e:
                print("Error verrifying credentials, ", e)
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
                showMemberMenu(connection, current_user)
            else:
                showTrainerMenu(connection, current_user)
        else:
            print("Invalid credentials. Please try again.")
    except Exception as e:
        print("Error verifying credentials", e) 

# Checks to see if user with name and password exists for Members or Trainers
def verifyCredentials(name, password, account_type):
    cursor = connection.cursor()
    if account_type == "M":
        cursor.execute(f"SELECT * FROM Members WHERE member_name = %s AND password = %s", (name, password))
    elif account_type == "T":
        cursor.execute(f"SELECT * FROM Trainers WHERE trainer_name = %s AND password = %s", (name, password))
    else:
        cursor.execute(f"SELECT * FROM Admins WHERE admin_name = %s AND Password = %s", (name, password))

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

    try:
        if getUser(connection, name, account_type) == None:
            if account_type == "M":
                createMember(connection, name, password)
            else:
                createTrainer(connection, name, password)
        else:
            print("Cannot create account, name is already taken. Please try again.")
    except Exception as e:
        print("Error creating account", e) 

def getUser(connection, name, account_type):
    cursor = connection.cursor()
    if account_type == "M":
        cursor.execute(f"SELECT * FROM Members WHERE member_name ='{name}'")
    else:
        cursor.execute(f"SELECT * FROM Trainers WHERE trainer_name ='{name}'")

    output = cursor.fetchall()
    cursor.close()
    if(len(output) == 1):
        return output[0]
    return None

def ViewNotifications(connection, name, account_type):
    cursor = connection.cursor()
    if account_type == "M":
        cursor.execute(f"SELECT * FROM select_and_delete_membernotifications('{name}')")
    else:
        cursor.execute(f"SELECT * FROM select_and_delete_trainernotifications('{name}')")
    output = cursor.fetchall()
    cursor.close()
    
    print("\nHere are your new notifications: ")
    for notification in output:
        print(f"- {notification[1]}")

    if len(output) == 0:
        print("None.")


# Creates and Connects to a new database titled HealthAndFitnessClubManagementSystem
def connectToDatabase(username, password):
    global connection
    connection = psycopg2.connect(database="HealthAndFitnessClubManagementSystem", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True

if __name__ == "__main__":
    main()
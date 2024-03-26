import psycopg2
from psycopg2 import connect
import datetime

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

    try:
        if len(getUser(name, account_type)) == 0:
            if account_type == "M":
                createMember(name, password)
            else:
                createTrainer(name, password)
        else:
            print("Cannot create account, name is already taken. Please try again.")
    except Exception as e:
        print("Error creating account", e) 

def createMember(name, password):
    print("\nEnter personal information")
    current_weight = input("What is your current weight?: ")
    goal_weight = input("What is your goal weight?: ")
    goal_date = input("When would you like to achieve your goal weight? (YYYY-MM-DD): ")
    #need to do input checking.

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Members (name, password, current_weight, goal_weight, goal_date) VALUES (%s, %s, %s, %s, %s)", (name, password, current_weight, goal_weight, goal_date))
    cursor.close()

def createTrainer(name, password):
    print("\nEnter your start and end time. You may not start or end on a partial hour.")
    print("Example of input: Enter '5' for 5:00am and '15' for 3:00pm")
    start_hour = input("Enter your starting hour: ")
    start_time = datetime.time(int(start_hour), 0, 0)
    end_hour = input("Enter your ending hour: ")
    end_time = datetime.time(int(end_hour), 0, 0)
    #Need to do input checking for start_hour and end_hour

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Trainers (name, password, start_time, end_time) VALUES (%s, %s, %s, %s)", (name, password, start_time, end_time))
    cursor.close()

def getUser(name, account_type):
    if account_type == "M":
        table = "Members"
    else:
        table = "Trainers"

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE name ='{name}'")
    output = cursor.fetchall()
    cursor.close()
    return output

def showMemberMenu():
    print(f"\nHi {current_user}! Please select an option below.")
    while(True):
        print("\n1. Profile Management")
        print("2. Create a new account")
        print("3. Access Admin Menu")
        print("4. Logoff")

        choice = input("Enter your choice: ")

        if choice == "1":
            return
        elif choice == "2":
            return
        elif choice == "3":
            return
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")

def ViewNotifications(name, account_type):
    if account_type == "M":
        table = "MemberNotifications"
    else:
        table = "TrainerNotifications"

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE name ='{name}'")
    output = cursor.fetchall()
    cursor.close()
    #... to complete

def showTrainerMenu():
    print(f"\nHi {current_user}! Please select an option below.")
    while(True):
        print("\n1. Schedule Management")
        print("2. Member Profile Viewing")
        print("3. View Notifications")
        print("4. Logoff")

        choice = input("Enter your choice: ")

        if choice == "1":
            ScheduleManagement()
        elif choice == "2":
            return
        elif choice == "3":
            ViewNotifications(current_user, "T")
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")

def ScheduleManagement():
    print("\nEnter your new start and end time. You may not start or end on a partial hour.")
    print("Example of input: Enter '5' for 5:00am and '15' for 3:00pm")
    start_hour = input("Enter your new starting hour: ")
    start_time = datetime.time(int(start_hour), 0, 0)
    end_hour = input("Enter your new ending hour: ")
    end_time = datetime.time(int(end_hour), 0, 0)
    # need type checking

    cursor = connection.cursor()
    cursor.execute("UPDATE Trainers SET start_time = %s, end_time = %s WHERE name = %s", (start_time, end_time, current_user))
    cursor.close()

def MemberProfileViewing():
    member_name = input("Enter the name of Member profile you'd like to view: ")
    data = getUser(member_name, "M")

    return
def showAdminMenu():
    print(f"\nHi admin staff, Please select an option below.")
    while(True):
        print("\n1. Room Booking Management")
        print("2. Equipment Maintenance Monitoring")
        print("3. Class Schedule Updating")
        print("4. Billing and Payment Processing")

        choice = input("Enter your choice: ")

        if choice == "1":
            showLoginMenu()
        elif choice == "2":
            showCreateAccountMenu()
        elif choice == "3":
            return
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")

# Creates and Connects to a new database titled HealthAndFitnessClubManagementSystem
def connectToDatabase(username, password):
    global connection
    connection = psycopg2.connect(database="HealthAndFitnessClubManagementSystem", user=username, password=password, host="localhost", port="5432")
    connection.autocommit = True

if __name__ == "__main__":
    main()
import db_application
from db_application import *
import member
from member import *
import datetime

def createTrainer(connection, name, password):
    print("\nEnter your start and end time. You may not start or end on a partial hour.")
    print("Example of input: Enter '5' for 5:00am and '15' for 3:00pm")
    start_hour = input("Enter your starting hour: ")
    start_time = datetime.time(int(start_hour), 0, 0)
    end_hour = input("Enter your ending hour: ")
    end_time = datetime.time(int(end_hour), 0, 0)
    #Need to do input checking for start_hour and end_hour

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Trainers (trainer_name, password, start_time, end_time) VALUES (%s, %s, %s, %s)", (name, password, start_time, end_time))
    cursor.close()

def showTrainerMenu(connection, current_user):
    print(f"\nHi {current_user}! Please select an option below.")
    while(True):
        print("\n1. Schedule Management")
        print("2. Member Profile Viewing")
        print("3. View Notifications")
        print("4. Logoff")

        choice = input("Enter your choice: ")

        if choice == "1":
            ScheduleManagement(connection, current_user)
        elif choice == "2":
            MemberProfileViewing(connection, current_user)
        elif choice == "3":
            db_application.ViewNotifications(connection, current_user, "T")
        elif choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")

def ScheduleManagement(connection, current_user):
    print("\nEnter your new start and end time. You may not start or end on a partial hour.")
    print("Example of input: Enter '5' for 5:00am and '15' for 3:00pm")
    start_hour = input("Enter your new starting hour: ")
    start_time = datetime.time(int(start_hour), 0, 0)
    end_hour = input("Enter your new ending hour: ")
    end_time = datetime.time(int(end_hour), 0, 0)
    # need type checking

    cursor = connection.cursor()
    cursor.execute("UPDATE Trainers SET start_time = %s, end_time = %s WHERE trainer_name = %s", (start_time, end_time, current_user))
    cursor.close()

def viewTrainerSchedule(connection, trainer_name):
    data = db_application.getUser(connection, trainer_name, "T")
    if(data == None):
        print(f"Trainer with name {trainer_name} does not exist.")
        return

def checkAvailability(connection, session_id, trainer_name, session_start_date_time, session_end_date_time):
    data = db_application.getUser(connection, trainer_name, "T")
    if(data == None):
        print(f"Trainer with name {trainer_name} does not exist.")
        return False
    
    if not (session_start_date_time.time() >= data[2] and session_end_date_time.time() <= data[3]):
        print(f"Trainer {trainer_name} not available at the specified time")
        print(f"Their start time is {data[2]} and their end time is {data[3]}")
        return False
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SESSIONS WHERE trainer_name = %s AND session_id != %s AND start_date_and_time >= %s AND start_date_and_time < %s", (trainer_name, session_id, session_start_date_time, session_end_date_time))
    output = cursor.fetchall()
    cursor.close()

    if len(output) > 0:
        print("Existing sessions conflict with the specified time.")
        return False
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM SESSIONS WHERE trainer_name =%s AND session_id != %s AND start_date_and_time >= %s AND end_date_and_time <= %s", (trainer_name, session_id, session_start_date_time, session_start_date_time))
    output = cursor.fetchall()
    cursor.close()

    if len(output) > 0:
        print("Existing sessions conflict with the specified time.")
        return False
                   
    return True
    

def MemberProfileViewing(connection, current_user):
    member_name = input("\nEnter the name of the Member you'd like to view: ")
    data = db_application.getUser(connection, member_name, "M")
    if(data == None):
        print(f"Member with name {member_name} does not exist.")
        return
    
    member.displayProfile(connection, current_user, data, "T")
import db_application
from db_application import *

import math
import datetime
import trainer

def createMember(connection, name, password):
    print("\nEnter personal information")
    current_weight = input("What is your current weight?: ")
    goal_weight = input("What is your goal weight?: ")
    goal_date = input("When would you like to achieve your goal weight? (YYYY-MM-DD): ")
    #need to do input checking.

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Members (member_name, password, current_weight, goal_weight, goal_date) VALUES (%s, %s, %s, %s, %s)", (name, password, current_weight, goal_weight, goal_date))
    cursor.close()

def showMemberMenu(connection, current_user):
    print(f"\nHi {current_user}! Please select an option below.")
    while(True):
        print("\n1. Profile Management")
        print("2. Dashboard Display")
        print("3. Schedule Management")
        print("4. Make A Maintenance Report")
        print("5. View Notifications")
        print("6. Logoff")

        choice = input("Enter your choice: ")

        if choice == "1":
            data = db_application.getUser(connection, current_user, "M")
            displayProfile(connection, current_user, data, "M")
        elif choice == "2":
            displayDashboard(connection, current_user)
        elif choice == "3":
            scheduleManagement(connection, current_user)
        elif choice == "4":
            makeMaintenanceReport(connection, current_user)
        elif choice == "5":
            db_application.ViewNotifications(connection, current_user, "M")
        elif choice == "6":
            return
        else:
            print("Invalid choice. Please try again.")

def displayProfile(connection, current_user, data, account_type):
    member_name = data[0]
    print(f"\nProfile of {member_name}:")
    print("-----------")
    print(f"Current Weight: {data[2]}")
    print(f"Goal Weight: {data[3]}")
    print(f"Target Date To Achieve Goal Weight: {data[4]}")

    if(member_name == current_user and account_type == "M"):
        while True:
            choice = input("\nDo you want to update this information (y/n): ")

            if choice == "y" or choice == "Y":
                print("You will now be prompted to change the information. Enter nothing to keep it the same.")
                current_weight = input("Change Current Weight to: ") or data[2]
                goal_weight = input("Change Goal Weight to: ") or data[3]
                goal_date = input("Change Target Date to (YYYY-MM-DD): ") or data[4]

                cursor = connection.cursor()
                cursor.execute("UPDATE Members SET current_weight = %s, goal_weight = %s, goal_date = %s WHERE member_name = %s", (current_weight, goal_weight, goal_date, current_user))
                cursor.close()
                print("Profile updated.")

                # New achievement if you achieved your goal weight
                if str(current_weight) == str(goal_weight):
                    print("hi")
                    cursor = connection.cursor()
                    cursor.execute("INSERT INTO Achievements (member_name, achievement_text) VALUES (%s, %s)", (member_name, f"Congrats, you achieved your goal weight of {goal_weight}"))
                    cursor.close()
                return
            elif choice == "n" or choice == "N":
                return
            else:
                print("Invalid choice.")
    elif account_type == "T":
        while True:
            choice = input("\nDo you want to add an achievement (y/n): ")

            if choice == "y" or choice == "Y":
                text = input("What would you like to say?: ")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Achievements (member_name, achievement_text) VALUES (%s, %s)", (member_name, f"From Trainer {current_user} : {text}"))
                cursor.close()
                print("Achievement inserted")
            elif choice == "n" or choice == "N":
                return
            else:
                print("Invalid choice.")


def displayDashboard(connection, current_user):
    print(f"\nDisplay {current_user}'s Dashboard:")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Routines WHERE member_name = '{current_user}' ")
    output = cursor.fetchall()
    cursor.close()

    routine_numbers = []

    print("\nRoutines:")
    if len(output) == 0:
        print("None.")
    
    for routine in output:
        routine_numbers.append(str(routine[0]))
        print(f"- id:{routine[0]}, routine: {routine[2]}")

    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM Achievements WHERE member_name='{current_user}'")
    output = cursor.fetchall()
    cursor.close()

    print("\nAchievements:")
    if len(output) == 0:
        print("None.")

    for achievement in output:
        print(f"- {achievement[1]}")

    data = db_application.getUser(connection, current_user, "M")
    print("\nHealth Statistics: ")
    print(f"Current Weight: {data[2]}")
    print(f"Goal Weight: {data[3]}")
    print(f"Target Date To Achieve Goal Weight: {data[4]}")
    print("-------")
    diff = abs(data[2] - data[3])
    print(f"Difference Between Current and Goal Weight: {diff}")
    weeks = math.ceil(diff / 2.0) # if gain/lose 2 pounds a week
    print(f"Estimated Weeks To Achieve Goal Weight: {weeks}")

    while True:
            print("\nDashboard Options: ")
            print("1. Add Routine")
            print("2. Delete Routine")
            print("3. Exit")

            choice = input("\n What is your choice?: ")

            if choice == "1":
                text = input("Describe the routine here: ")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Routines (member_name, routine_text) VALUES (%s, %s)", (current_user, text))
                cursor.close()
                print("Routine added.")
                return
            elif choice == "2":
                num = input("Specify the id of the routine you would like to delete")

                if num in routine_numbers:
                    cursor = connection.cursor()
                    cursor.execute(f"DELETE FROM ROUTINES WHERE routine_id = '{num}'")
                    cursor.close()
                    print(f"Routine {num} deleted.")
                    return
                else:
                    print("Not a valid routine id.")
            elif choice == "3":
                return
            else:
                print("Invalid choice.")

def scheduleManagement(connection, current_user):
    while True:
        print("\nSchedule Options: ")
        print("1. Schedule personal training session")
        print("2. Reschedule personal training session")
        print("3. Cancel a personal training session")
        print("4. Register for group fitness class")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            scheduleSession(connection, current_user)
        elif choice == "2":
            rescheduleSession(connection, current_user)
        elif choice == "3":
            cancelSession(connection, current_user)
        elif choice == "4":
            registerClass(connection, current_user)
        elif choice == "5":
            return
        else:
            print("Invalid choice.")

def scheduleSession(connection, current_user):
    print("\nOkay great! Please enter the information below to schedule an hour personal training session")
    trainer_name = input("Enter the name of the trainer you want to schedule with: ")
    session_date = input("Enter the date of the session (YYYY-MM-DD): ")
    session_hour = input("Enter the hour you want the session to start (e.g., 15 = 3:00pm): ")
    session_minute = input("Enter the minute you want the session to start: ")
    session_end_hour = input("Enter the hour you want the session to end (e.g., 15 = 3:00pm): ")
    session_end_minute = input("Enter the minute you want the session to end: ")

    session_date = datetime.datetime.strptime(session_date, '%Y-%m-%d').date()
    session_start_date_time = datetime.datetime(session_date.year, session_date.month, session_date.day, int(session_hour), int(session_minute), 0)
    session_end_date_time = datetime.datetime(session_date.year, session_date.month, session_date.day, int(session_end_hour), int(session_end_minute), 0)

    if session_start_date_time >= session_end_date_time:
        print("Start time must be after end time")
        return

    if not trainer.checkAvailability(connection, -1, trainer_name, session_start_date_time, session_end_date_time):
        print("Cannot schedule session.")
        return
    
    print("\nSession time is available!")
    billing_data = input("Please enter billing info to pay $50 for session (assume this will be verified): ")

    if(billing_data == ""):
        print("Billing info not approved.")
        return

    print("Billing info Approved.")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Sessions (member_name, trainer_name, start_date_and_time, end_date_and_time) VALUES (%s, %s, %s, %s)", (current_user, trainer_name, session_start_date_time, session_end_date_time))
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Billings (member_name, billing_text) VALUES (%s, %s)", (current_user, f"Created session with {trainer_name} from {session_start_date_time} to {session_end_date_time}, billing data: {billing_data}"))
    cursor.close()
    print(f"Session with {trainer_name} from {session_start_date_time} to {session_end_date_time} created.")

def rescheduleSession(connection, current_user):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Sessions WHERE member_name = %s", (current_user,))
    output = cursor.fetchall()
    cursor.close()
    if len(output) == 0:
        print("You do not have any sessions that you can reschedule")
        return
    
    session_ids = []
    
    print("\nYour Scheduled Sessions:")
    for session in output:
        session_ids.append(str(session[0]))
        print(f"id: {session[0]}, trainer: {session[2]}, start date and time: {session[3]}, end date and time: {session[4]}")

    while True:
        id = input("\nEnter the id of the session you'd like reschedule (or nothing to quit): ")

        if(id == ""):
            return
        elif id in session_ids:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Sessions WHERE session_id=%s", id)
            output = cursor.fetchall()
            cursor.close()

            session = output[0]
            trainer_name = session[2]

            print("Ok great! Now enter the time information you want to change (or nothing to keep it the same)")
            session_date = input("Enter the date of the session (YYYY-MM-DD): ") or str(session[3].date())
            session_hour = input("Enter the hour you want the session to start (e.g., 15 = 3:00pm): ") or str(session[3].hour)
            session_minute = input("Enter the minute you want the session to start: ") or str(session[3].minute)
            session_end_hour = input("Enter the hour you want the session to end (e.g., 15 = 3:00pm): ") or str(session[4].hour)
            session_end_minute = input("Enter the minute you want the session to end: ") or str(session[4].minute)

            session_date = datetime.datetime.strptime(session_date, '%Y-%m-%d').date()
            session_start_date_time = datetime.datetime(session_date.year, session_date.month, session_date.day, int(session_hour), int(session_minute), 0)
            session_end_date_time = datetime.datetime(session_date.year, session_date.month, session_date.day, int(session_end_hour), int(session_end_minute), 0)

            if session_start_date_time >= session_end_date_time:
                print("Start time must be after end time")
                return

            if session_start_date_time.date() == session[3].date() and session_start_date_time.hour == session[3].hour and session_start_date_time.minute == session[3].minute:
                if session_end_date_time.date() == session[4].date() and session_end_date_time.hour == session[4].hour and session_end_date_time.minute == session[4].minute:
                    print("No changes were made.")
                    return
            
            if not trainer.checkAvailability(connection, session[0], trainer_name, session_start_date_time, session_end_date_time):
                print("Cannot reschedule session.")
                return
            
            print("\nSession time is available!")

            cursor = connection.cursor()
            cursor.execute("UPDATE Sessions SET start_date_and_time=%s, end_date_and_time=%s WHERE session_id=%s", (session_start_date_time, session_end_date_time, id))
            cursor.close()
            print("Session updated.")
            return
        else:
            print("Invalid choice.")

def cancelSession(connection, current_user):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Sessions WHERE member_name = %s", (current_user,))
    output = cursor.fetchall()
    cursor.close()
    if len(output) == 0:
        print("You do not have any sessions that you can cancel")
        return
    
    session_ids = []
    
    print("\nYour Scheduled Sessions:")
    for session in output:
        session_ids.append(str(session[0]))
        print(f"id: {session[0]}, trainer: {session[2]}, start date and time: {session[3]}, end date and time: {session[4]}")

    while True:
        id = input("\nEnter the id of the session you'd like reschedule (or nothing to quit): ")

        if(id == ""):
            return
        elif id in session_ids:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Sessions WHERE session_id=%s", (id,))
            cursor.close()
            print("Session cancelled. Refund will be processed.")
            return
        else:
            print("Invalid choice.")

def registerClass(connection, current_user):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes ORDER BY start_date_and_time ASC")
    output = cursor.fetchall()
    cursor.close()

    print("\nClasses: ")
    if len(output) == 0:
        print("None.")
        print("\nNo classes to join.")
        return
    
    class_ids = []
    for class_ in output:
        class_ids.append(str(class_[0]))
        print(f"id: {class_[0]}, name: {class_[1]}, start date and time: {class_[2]}, end date and time: {class_[3]}, room_id: {class_[4]}")

    while True:
        id = input("\nEnter the id of the class you want to register for (or nothing to exit): ")

        if id == "":
            return
        elif id in class_ids:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Participants WHERE class_id=%s AND member_name=%s", (id, current_user))
            output = cursor.fetchall()
            cursor.close()

            if len(output) > 1:
                print("You've already registered for this class!")
            else:
                billing_data = input("Please enter billing info to pay $25 for class (assume this will be verified): ")

                if(billing_data == ""):
                    print("Billing info not approved.")
                    return

                print("Billing info Approved.")

                cursor = connection.cursor()
                cursor.execute("INSERT INTO Participants (class_id, member_name) VALUES(%s, %s)", (id, current_user))
                cursor.close()

                cursor = connection.cursor()
                cursor.execute("INSERT INTO Billings (member_name, billing_text) VALUES (%s, %s)", (current_user, f"Registered for class {id}, billing data: {billing_data}"))
                cursor.close()

                print("Registered for class!")
        else:
            print("Invalid choice.")


def makeMaintenanceReport(connection, current_user):
    text = input("\nEnter a description of the problem (which machine, area of gym, etc): ")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Reports (member_name, report_text) VALUES (%s, %s)", (current_user, text))
    cursor.close()
    print("Maintenance report has been made. You will be notified when it is resolved.")



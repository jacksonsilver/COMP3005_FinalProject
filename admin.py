from db_application import *

import datetime

def showAdminMenu(connection):
    print(f"\nHi admin staff, Please select an option below.")
    while(True):
        print("\n1. Room Booking Management")
        print("2. Equipment Maintenance Monitoring")
        print("3. Class Schedule Updating")
        print("4. View All Billings")
        print("5. Process Billings/Payments")
        print("6. Go Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            RoomBookingManagement(connection)
        elif choice == "2":
            ViewMaintenanceReports(connection)
        elif choice == "3":
            ClassScheduling(connection)
        elif choice == "4":
            try:
                viewBillings(connection)
            except Exception as e:
                print("Error viewing billings, ", e)
        elif choice == "5":
            try:
                processBillings(connection)
            except Exception as e:
                print("Error processing billings, ", e)
        elif choice == "6":
            return
        else:
            print("Invalid choice. Please try again.")

def RoomBookingManagement(connection):
    while True:
        print("\nRoom Booking Management Options: ")
        print("1. View Rooms")
        print("2. View Bookings for a specific Room")
        print("3. Adjust a booking to another room")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            ViewRooms(connection)
        elif choice == "2":
            ViewBookingsForRoom(connection)
        elif choice == "3":
            AdjustBookingRoom(connection)
        elif choice == "4":
            return
        else:
            print("Invalid choice.")

def ViewRooms(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Rooms")
    output = cursor.fetchall()
    cursor.close()

    print("\nRooms")
    for room in output:
        print(f"id: {room[0]}, description: {room[1]}")
    
    if len(output) == 0:
        print("None.")

def ViewBookingsForRoom(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Rooms")
    output = cursor.fetchall()
    cursor.close()

    room_ids = []
    for room in output:
        room_ids.append(str(room[0]))

    id = input("Enter the id of the room you would like to view (or nothing to exit): ")

    if id == "":
        return
    
    if id not in room_ids:
        print("Invalid choice.")
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes WHERE room_id=%s ORDER BY start_date_and_time ASC", (id,))
    output = cursor.fetchall()
    cursor.close()

    print(f"Classes that booked that room {id}: ")
    if len(output) == 0:
        print("None.")
        return
    
    for class_ in output:
        print(f"id: {class_[0]}, name: {class_[1]}, start date and time: {class_[2]}, end date and time: {class_[3]}")

def AdjustBookingRoom(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes")
    output = cursor.fetchall()
    cursor.close()

    class_ids = []
    for class_ in output:
        class_ids.append(str(class_[0]))

    id = input("Enter the id of the class you would like to adjust the room for: ")
    
    if id not in class_ids:
        print("Invalid choice.")
        return
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes WHERE class_id=%s", (id,))
    output = cursor.fetchall()
    cursor.close()

    class_ = output[0]

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Rooms")
    output = cursor.fetchall()
    cursor.close()

    room_ids = []
    for room in output:
        room_ids.append(str(room[0]))

    new_room_id = input("Enter the id of the room you would like to move the class to: ")

    if new_room_id not in room_ids:
        print("Invalid choice.")
        return
    
    if new_room_id == str(class_[4]):
        print(f"Class already scheduled in room {class_[4]}")
        return
    
    if not checkTimeAvailability(connection, class_[0], new_room_id, class_[2], class_[3]):
        print("That room is not available at the time of this class")
        return
    
    print("Room available!")

    cursor = connection.cursor()
    cursor.execute("UPDATE Classes SET room_id=%s WHERE class_id=%s", (new_room_id, class_[0]))
    cursor.close()

    print("Booking updated! Any participants have been notified.")

def ViewMaintenanceReports(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Reports")
    output = cursor.fetchall()
    cursor.close()

    choices = []
    print("\nUnresolved maintenance reports: ")
    for report in output:
        choices.append(str(report[0]))
        print(f"id: {report[0]}, by: {report[1]}, description: {report[2]}")

    if len(choices) == 0:
        print("None.")
        return
    
    while True:
        choice = input("\nEnter the id of the report you'd like to resolve (or nothing to quit): ")

        if (choice == ""):
            return
        elif (choice in choices):
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Reports WHERE report_id=%s", choice)
            cursor.close()
            choices.remove(choice)
            print(f"Report {choice} deleted.")
            if(len(choices) == 0):
                return
        else:
            print("Invalid choice")

def ClassScheduling(connection):
    while True:
        print("\nClass Scheduling Options: ")
        print("1. Create A Class")
        print("2. Reschedule A Class")
        print("3. Cancel A Class")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            createAClass(connection)
        elif choice == "2":
            rescheduleClass(connection)
        elif choice == "3":
            cancelClass(connection)
        elif choice == "4":
            return
        else:
            print("Invalid choice.")

def createAClass(connection):
    print("\nOkay great! Enter the information below to create the class")
    class_name = input("Enter the name of the class: ")
    room_id = input("Enter the id of the room the class is in: ")
    class_date = input("Enter the date of the class (YYYY-MM-DD): ")
    class_hour = input("Enter the hour you want the class to start (e.g., 15 = 3:00pm): ")
    class_minute = input("Enter the minute you want the class to start: ")
    class_end_hour = input("Enter the hour you want the class to end (e.g., 15 = 3:00pm): ")
    class_end_minute = input("Enter the minute you want the class to end: ")

    class_date = datetime.datetime.strptime(class_date, '%Y-%m-%d').date()
    class_start_date_time = datetime.datetime(class_date.year, class_date.month, class_date.day, int(class_hour), int(class_minute), 0)
    class_end_date_time = datetime.datetime(class_date.year, class_date.month, class_date.day, int(class_end_hour), int(class_end_minute), 0)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Rooms")
    output = cursor.fetchall()
    cursor.close()

    room_ids = []
    for room in output:
        room_ids.append(str(room[0]))

    if room_id not in room_ids:
        print("Room with that id does not exist")
        return

    if class_start_date_time >= class_end_date_time:
        print("Start time must be after end time")
        return

    if not checkTimeAvailability(connection, -1, room_id, class_start_date_time, class_end_date_time):
        print("Cannot schedule class.")
        return
    
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Classes (class_name, start_date_and_time, end_date_and_time, room_id) VALUES (%s, %s, %s, %s)", (class_name, class_start_date_time, class_end_date_time, room_id))
    cursor.close()
    print("Class created!")

def rescheduleClass(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes ORDER BY start_date_and_time ASC")
    output = cursor.fetchall()
    cursor.close()

    print("\nClasses: ")
    if len(output) == 0:
        print("None.")
        print("\nNo classes to reschedule.")
        return
    
    class_ids = []
    for class_ in output:
        class_ids.append(str(class_[0]))
        print(f"id: {class_[0]}, name: {class_[1]}, start date and time: {class_[2]}, end date and time: {class_[3]}, room_id: {class_[4]}")

    while True:
        id = input("\nEnter the id of the class you would like to reschedule (or nothing to exit): ")
        if id == "":
            return
        elif id in class_ids:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Classes WHERE class_id=%s", (id,))
            output = cursor.fetchall()
            cursor.close()
            
            class_ = output[0]
            print("\nOk! Now enter the information you'd like to change (or enter nothing to keep it the same)")
            class_date = input("Enter the date of the class (YYYY-MM-DD): ") or str(class_[2].date())
            class_hour = input("Enter the hour you want the class to start (e.g., 15 = 3:00pm): ") or str(class_[2].hour)
            class_minute = input("Enter the minute you want the class to start: ") or str(class_[2].minute)
            class_end_hour = input("Enter the hour you want the class to end (e.g., 15 = 3:00pm): ") or str(class_[3].hour)
            class_end_minute = input("Enter the minute you want the class to end: ") or str(class_[3].minute)

            class_date = datetime.datetime.strptime(class_date, '%Y-%m-%d').date()
            class_start_date_time = datetime.datetime(class_date.year, class_date.month, class_date.day, int(class_hour), int(class_minute), 0)
            class_end_date_time = datetime.datetime(class_date.year, class_date.month, class_date.day, int(class_end_hour), int(class_end_minute), 0)

            if class_start_date_time >= class_end_date_time:
                print("Start time must be after end time")
                return
            
            if class_start_date_time.date() == class_[2].date() and class_start_date_time.hour == class_[2].hour and class_start_date_time.minute == class_[2].minute:
                if class_end_date_time.date() == class_[3].date() and class_end_date_time.hour == class_[3].hour and class_end_date_time.minute == class_[3].minute:
                    print("No changes were made.")
                    return
                
            if not checkTimeAvailability(connection, id, class_[4], class_start_date_time, class_end_date_time):
                print("Scheduling conflicts permit. Cannot reschedule to that time.")
                return
        
            print("\nClass time is available!")

            cursor = connection.cursor()
            cursor.execute("UPDATE Classes SET start_date_and_time=%s, end_date_and_time=%s WHERE class_id=%s", (class_start_date_time, class_end_date_time, id))
            cursor.close()
            print("Class updated.")
            return
        else:
            print("Invalid choice.")

def cancelClass(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes ORDER BY start_date_and_time ASC")
    output = cursor.fetchall()
    cursor.close()

    print("\nClasses: ")
    if len(output) == 0:
        print("None.")
        print("\nNo classes to cancel.")
        return
    
    class_ids = []
    for class_ in output:
        class_ids.append(str(class_[0]))
        print(f"id: {class_[0]}, name: {class_[1]}, start date and time: {class_[2]}, end date and time: {class_[3]}, room_id: {class_[4]}")

    while True:
        id = input("\nEnter the id of the class you would like to cancel (or nothing to exit): ")

        if id == "":
            return
        elif id in class_ids:
            cursor = connection.cursor()
            cursor.execute("SELECT notify_members_on_class_deletion(%s)", (id,))
            cursor.close()
            class_ids.remove(id)
            print("Class deleted and participating members notified.")
        else:
            print("Invalid choice.")

def checkTimeAvailability(connection, class_id, room_id, start_date_and_time, end_date_and_time):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes WHERE room_id = %s AND class_id != %s AND start_date_and_time >= %s AND start_date_and_time < %s", (room_id, class_id, start_date_and_time, end_date_and_time))
    output = cursor.fetchall()
    cursor.close()

    if len(output) > 0:
        print("Existing classes conflict with the specified time.")
        return False

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Classes WHERE room_id = %s AND class_id != %s AND start_date_and_time >= %s AND end_date_and_time < %s", (room_id, class_id, start_date_and_time, start_date_and_time))
    output = cursor.fetchall()
    cursor.close()

    if len(output) > 0:
        print("Existing classes conflict with the specified time.")
        return False
    
    return True
 
def viewBillings(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Billings")
    output = cursor.fetchall()
    cursor.close()

    if len(output) == 0:
        print("\n No billings")
        return
    
    print("\nAll Billings:")
    for billing in output:
        result = 'False' if billing[3] == False else 'True'
        print(f"id: {billing[0]}, processed:{result}, associated member: {billing[1]}, details: {billing[2]}")
        
def processBillings(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Billings WHERE processed = %s", (False,))
    output = cursor.fetchall()
    cursor.close()

    if len(output) == 0:
        print("\nNo billings to process")
        return
    
    print("\nUnprocessed Billings:")
    billing_ids = []
    for billing in output:
        billing_ids.append(str(billing[0]))
        print(f"id: {billing[0]}, associated member: {billing[1]}, details: {billing[2]}")

    while True:
        id = input("\nEnter the id of the billing you'd like to process (or nothing to exit): ")

        if id == "":
            return
        elif id in billing_ids:
            cursor = connection.cursor()
            cursor.execute("UPDATE Billings SET processed=%s WHERE billing_id=%s", (True, id))
            cursor.close()
            print("Billing processed.")
            billing_ids.remove(id)

            if len(billing_ids) == 0:
                return
        else:
            print("Invalid choice.")


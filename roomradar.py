import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from datetime import timedelta
import mysql.connector
from mysql.connector import Error


# This the password for ADMIN 
ADMIN_PASSWORD = "RRadmingold" 
# Admin username is "RRadmin"

# Function to connect database to this program
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Function in executing an SQL query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

# Parameters in creating database
host = "localhost"
user = "root"  
password = "" 
database = "RoomRadarDB"

connection = create_connection(host, user, password, database)

# Function to insert guest details to the database
def insert_guest(connection, guest_name, cellphone):
    query = f"INSERT INTO Guest (GuestName, CellphoneNumber) VALUES ('{guest_name}', '{cellphone}')"
    execute_query(connection, query)

# Function to insert reservation details to the database
def insert_reservation(connection, GuestID, reservation_date, num_days, total_price, room_id):
    query = f"INSERT INTO Reservation (GuestID, ReservationDate, NumberOfDays, TotalPrice, RoomID) VALUES ({GuestID}, '{reservation_date}', {num_days}, {total_price}, {room_id})"
    execute_query(connection, query)

# Function to retrieve a room_id from the database based on the RoomName
def get_room_id(room_name):
    cursor = connection.cursor()
    query = f"SELECT RoomID FROM Room WHERE RoomName = '{room_name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

# Function to check if a room is reserved for a specific date range
def roomreserved (room_id, reservation_date, num_days):
    cursor = connection.cursor()
    
    end_date = (datetime.strptime(reservation_date, "%Y-%m-%d") + timedelta(days=num_days)).strftime("%Y-%m-%d")
    query = f"""
    SELECT COUNT(*) FROM Reservation 
    WHERE RoomID = {room_id} AND (
        (ReservationDate >= '{reservation_date}' AND ReservationDate < '{end_date}') OR
        (DATE_ADD(ReservationDate, INTERVAL NumberOfDays DAY) > '{reservation_date}' AND ReservationDate < '{end_date}')
    )
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result > 0  


# Function to show standard room options
def showstandardrooms():
    # Window for selecting room in Standard
    standardrooms = tk.Toplevel(dash)
    standardrooms.title("Select Your Standard Room")
    standardrooms.geometry("2000x1000")

    # Standard room packages with their features and prices
    Stan_roompackages = {
        "Standard Room A": ("Features:\n- 1 Single Bed\n- Free Wi-Fi\n- Fan Cooling", 900),
        "Standard Room B": ("Features:\n- 1 Double Bed\n- Free Wi-Fi\n- Fan Cooling\n- Television", 1300),
        "Standard Room C": ("Features:\n- 1 King Bed\n- Free Wi-Fi\n- Breakfast\n- Fan Cooling\n- Television ", 1700),
    }

    # Variable to hold the selected room
    Stanselectroom = tk.StringVar(value="Select a room")

    # Label for the room options
    label = tk.Label(standardrooms, text="Available Standard Rooms", font=('Helvetica', 16))
    label.place(x=620, y=50)

    # Frame for the room list
    Stan_roomlist = tk.Frame(standardrooms)
    Stan_roomlist.place(x=570, y=200)

    # Buttons for each room package with their features and prices
    for Stan_roomname, (features, price) in Stan_roompackages.items():
        Stan_roominfo = f"{Stan_roomname} - Php{price}\n{features}"
        Stan_radiobutton = tk.Radiobutton(Stan_roomlist, text=Stan_roominfo, variable=Stanselectroom, value=Stan_roomname, anchor='w', justify='left')
        Stan_radiobutton.pack(anchor='w', padx=20)

    # Button to confirm the room selection
    def Stan_confirmselection():
        Stan_roomname = Stanselectroom.get()
        if Stan_roomname != "Select a room":
            features, price = Stan_roompackages[Stan_roomname]
            standardrooms.destroy()  
            Stan_inputdetails(Stan_roomname, features, price) 
        else:
            messagebox.showwarning("Selection Error", "Please select a room.")

    Stan_confirmbutton = tk.Button(standardrooms, text="Confirm Selection", command=Stan_confirmselection)
    Stan_confirmbutton.place(x=620 , y= 600)

# Function to input guest details
def Stan_inputdetails(Stan_roomname, features, price):
    standardguest = tk.Toplevel(dash)
    standardguest.title("Guest and Booking Details")
    standardguest.geometry("2000x1000")

    tk.Label(standardguest, text="Guest and Booking Details").place(x= 620, y= 50)

    tk.Label(standardguest, text="Guest Name:").place(x= 620, y= 100)
    Stan_guestname = tk.Entry(standardguest)
    Stan_guestname.place(x= 620, y= 150)

    tk.Label(standardguest, text="Cellphone Number:").place(x= 620, y= 200)
    Stan_cpnum = tk.Entry(standardguest)
    Stan_cpnum.place(x= 620, y= 250)

    tk.Label(standardguest, text="Date of Reservation (YYYY-MM-DD):").place(x= 620, y= 300)
    Stan_resdate = tk.Entry(standardguest)
    Stan_resdate.place(x= 620, y= 350)

    tk.Label(standardguest, text="Number of Days Stay:").place(x= 620, y= 400)
    Stan_daystay = tk.Entry(standardguest)
    Stan_daystay.place(x= 620, y= 450)

    def Stan_confirmguestdetails():
        guest_name = Stan_guestname.get()
        cellphone = Stan_cpnum.get()
        date_of_reservation = Stan_resdate.get()
        num_days = Stan_daystay.get()

        # Validating the user input
        try:
            datetime.strptime(date_of_reservation, "%Y-%m-%d")
            num_days = int(num_days)
            if num_days <= 0:
                raise ValueError("Number of days must be greater than 0.")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return

        # To get the RoomID for the selected room
        room_id = get_room_id(Stan_roomname)
        if room_id is not None:
            # Check if the room is reserved during the stay period
            if roomreserved (room_id, date_of_reservation, num_days):
                messagebox.showwarning("Reservation Error", "This room is already reserved during the selected date range.")
            else:
                # Calculate total price of stay
                total_price = price * num_days

                insert_guest(connection, guest_name, cellphone)
                cursor = connection.cursor()
                cursor.execute("SELECT LAST_INSERT_ID()")
                GuestID = cursor.fetchone()[0]

                insert_reservation(connection, GuestID, date_of_reservation, num_days, total_price, room_id)

                messagebox.showinfo("Reservation Summary", 
                                    f"Room Selected: {Stan_roomname}\n"
                                    f"Features: {features}\n"
                                    f"Price per Night: Php{price}\n"
                                    f"Total Price for {num_days} night(s): Php{total_price}\n"
                                    f"Guest Name: {guest_name}\n"
                                    f"Cellphone: {cellphone}\n"
                                    f"Date of Reservation: {date_of_reservation}")
        else:
            messagebox.showerror("Error", "Room not found. Please select a valid room.")

        standardguest.destroy()


    Stan_confirmguestbttn = tk.Button(standardguest, text="Confirm Details", command=Stan_confirmguestdetails)
    Stan_confirmguestbttn.place(x= 620, y= 620)
    

# START OF SUITE 


# Function to insert guest details to the database
def insert_guest(connection, guest_name, cellphone):
    query = f"INSERT INTO Guest (GuestName, CellphoneNumber) VALUES ('{guest_name}', '{cellphone}')"
    execute_query(connection, query)

# Function to insert reservation details to the database
def insert_reservation(connection, GuestID, reservation_date, num_days, total_price, room_id):
    query = f"INSERT INTO Reservation (GuestID, ReservationDate, NumberOfDays, TotalPrice, RoomID) VALUES ({GuestID}, '{reservation_date}', {num_days}, {total_price}, {room_id})"
    execute_query(connection, query)

# Function to retrieve a room_id from the database based on the RoomName
def get_room_id(room_name):
    cursor = connection.cursor()
    query = f"SELECT RoomID FROM Room WHERE RoomName = '{room_name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

# Function to check if a room is reserved for a specific date range
def roomreserved (room_id, reservation_date, num_days):
    cursor = connection.cursor()
    
    end_date = (datetime.strptime(reservation_date, "%Y-%m-%d") + timedelta(days=num_days)).strftime("%Y-%m-%d")
    query = f"""
    SELECT COUNT(*) FROM Reservation 
    WHERE RoomID = {room_id} AND (
        (ReservationDate >= '{reservation_date}' AND ReservationDate < '{end_date}') OR
        (DATE_ADD(ReservationDate, INTERVAL NumberOfDays DAY) > '{reservation_date}' AND ReservationDate < '{end_date}')
    )
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result > 0  

# Function to show suite room options
def showsuiterooms():
    # Window for selecting room in Suite
    suiterooms = tk.Toplevel(dash)
    suiterooms.title("Select Your Suite Room")
    suiterooms.geometry("2000x1000")

    # Suite room packages with their features and prices
    Suite_roompackages = {
        "Suite Room A": ("Features:\n- 1 King Bed\n- Free Wi-Fi\n- Air Conditioning\n- Television", 2500),
        "Suite Room B": ("Features:\n- 2 Queen Beds\n- Free Wi-Fi\n- Air Conditioning\n- Television\n- Balcony", 3500),
        "Suite Room C": ("Features:\n- 1 King Bed\n- Free Wi-Fi\n- Breakfast\n- Air Conditioning\n- Television\n- Jacuzzi", 5000),
    }

    # Variable to hold the selected room
    Suiteselectroom = tk.StringVar(value="Select a room")

    # Label for the room options
    label = tk.Label(suiterooms, text="Available Suite Rooms", font=('Helvetica', 16))
    label.place(x=620, y=50)

    # Frame for the room list
    Suite_roomlist = tk.Frame(suiterooms)
    Suite_roomlist.place(x=570, y=200)

    # Buttons for each room package with their features and prices
    for Suite_roomname, (features, price) in Suite_roompackages.items():
        Suite_roominfo = f"{Suite_roomname} - Php{price}\n{features}"
        Suite_radiobutton = tk.Radiobutton(Suite_roomlist, text=Suite_roominfo, variable=Suiteselectroom, value=Suite_roomname, anchor='w', justify='left')
        Suite_radiobutton.pack(anchor='w', padx=20)

    # Button to confirm the room selection
    def Suite_confirmselection():
        Suite_roomname = Suiteselectroom.get()
        if Suite_roomname != "Select a room":
            features, price = Suite_roompackages[Suite_roomname]
            suiterooms.destroy()  
            Suite_inputdetails(Suite_roomname, features, price) 
        else:
            messagebox.showwarning("Selection Error", "Please select a room.")

    Suite_confirmbutton = tk.Button(suiterooms, text="Confirm Selection", command=Suite_confirmselection)
    Suite_confirmbutton.place(x=620 , y= 600)

# Function to input guest details for suite room
def Suite_inputdetails(Suite_roomname, features, price):
    suiteguest = tk.Toplevel(dash)
    suiteguest.title("Guest and Booking Details")
    suiteguest.geometry("2000x1000")

    tk.Label(suiteguest, text="Guest and Booking Details").place(x= 620, y= 50)

    tk.Label(suiteguest, text="Guest Name:").place(x= 620, y= 100)
    Suite_guestname = tk.Entry(suiteguest)
    Suite_guestname.place(x= 620, y= 150)

    tk.Label(suiteguest, text="Cellphone Number:").place(x= 620, y= 200)
    Suite_cpnum = tk.Entry(suiteguest)
    Suite_cpnum.place(x= 620, y= 250)

    tk.Label(suiteguest, text="Date of Reservation (YYYY-MM-DD):").place(x= 620, y= 300)
    Suite_resdate = tk.Entry(suiteguest)
    Suite_resdate.place(x= 620, y= 350)

    tk.Label(suiteguest, text="Number of Days Stay:").place(x= 620, y= 400)
    Suite_daystay = tk.Entry(suiteguest)
    Suite_daystay.place(x= 620, y= 450)

    def Suite_confirmguestdetails():
        guest_name = Suite_guestname.get()
        cellphone = Suite_cpnum.get()
        date_of_reservation = Suite_resdate.get()
        num_days = Suite_daystay.get()

        # Validating the user input
        try:
            datetime.strptime(date_of_reservation, "%Y-%m-%d")
            num_days = int(num_days)
            if num_days <= 0:
                raise ValueError("Number of days must be greater than 0.")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return

        # To get the RoomID for the selected room
        room_id = get_room_id(Suite_roomname)
        if room_id is not None:
            # Check if the room is reserved during the stay period
            if roomreserved(room_id, date_of_reservation, num_days):
                messagebox.showwarning("Reservation Error", "This room is already reserved during the selected date range.")
            else:
                # Calculate total price of stay
                total_price = price * num_days

                insert_guest(connection, guest_name, cellphone)
                cursor = connection.cursor()
                cursor.execute("SELECT LAST_INSERT_ID()")
                GuestID = cursor.fetchone()[0]

                insert_reservation(connection, GuestID, date_of_reservation, num_days, total_price, room_id)

                messagebox.showinfo("Reservation Summary", 
                                    f"Room Selected: {Suite_roomname}\n"
                                    f"Features: {features}\n"
                                    f"Price per Night: Php{price}\n"
                                    f"Total Price for {num_days} night(s): Php{total_price}\n"
                                    f"Guest Name: {guest_name}\n"
                                    f"Cellphone: {cellphone}\n"
                                    f"Date of Reservation: {date_of_reservation}")
        else:
            messagebox.showerror("Error", "Room not found. Please select a valid room.")

        suiteguest.destroy()


    Suite_confirmguestbttn = tk.Button(suiteguest, text="Confirm Details", command=Suite_confirmguestdetails)
    Suite_confirmguestbttn.place(x= 620, y= 620)



#START OF DELUXE 

# Function to insert guest details to the database
def insert_guest(connection, guest_name, cellphone):
    query = f"INSERT INTO Guest (GuestName, CellphoneNumber) VALUES ('{guest_name}', '{cellphone}')"
    execute_query(connection, query)

# Function to insert reservation details to the database
def insert_reservation(connection, GuestID, reservation_date, num_days, total_price, room_id):
    query = f"INSERT INTO Reservation (GuestID, ReservationDate, NumberOfDays, TotalPrice, RoomID) VALUES ({GuestID}, '{reservation_date}', {num_days}, {total_price}, {room_id})"
    execute_query(connection, query)

# Function to retrieve a room_id from the database based on the RoomName
def get_room_id(room_name):
    cursor = connection.cursor()
    query = f"SELECT RoomID FROM Room WHERE RoomName = '{room_name}'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

# Function to check if a room is reserved for a specific date range
def roomreserved (room_id, reservation_date, num_days):
    cursor = connection.cursor()
    
    end_date = (datetime.strptime(reservation_date, "%Y-%m-%d") + timedelta(days=num_days)).strftime("%Y-%m-%d")
    query = f"""
    SELECT COUNT(*) FROM Reservation 
    WHERE RoomID = {room_id} AND (
        (ReservationDate >= '{reservation_date}' AND ReservationDate < '{end_date}') OR
        (DATE_ADD(ReservationDate, INTERVAL NumberOfDays DAY) > '{reservation_date}' AND ReservationDate < '{end_date}')
    )
    """
    cursor.execute(query)
    result = cursor.fetchone()[0]
    cursor.close()
    return result > 0  

# Function to show deluxe room options
def showdeluxerooms():
    # Window for selecting room in Deluxe
    deluxerooms = tk.Toplevel(dash)
    deluxerooms.title("Select Your Deluxe Room")
    deluxerooms.geometry("2000x1000")

    # Deluxe room packages with their features and prices
    Deluxe_roompackages = {
        "Deluxe Room A": ("Features:\n- 1 Queen Bed\n- Free Wi-Fi\n- Air Conditioning\n- Mini Bar", 2000),
        "Deluxe Room B": ("Features:\n- 2 King Beds\n- Free Wi-Fi\n- Air Conditioning\n- Television\n- Balcony", 3000),
        "Deluxe Room C": ("Features:\n- 1 King Bed\n- Free Wi-Fi\n- Breakfast\n- Air Conditioning\n- Television\n- Jacuzzi", 4500),
    }

    # Variable to hold the selected room
    Deluxeselectroom = tk.StringVar(value="Select a room")

    # Label for the room options
    label = tk.Label(deluxerooms, text="Available Deluxe Rooms", font=('Helvetica', 16))
    label.place(x=620, y=50)

    # Frame for the room list
    Deluxe_roomlist = tk.Frame(deluxerooms)
    Deluxe_roomlist.place(x=570, y=200)

    # Buttons for each room package with their features and prices
    for Deluxe_roomname, (features, price) in Deluxe_roompackages.items():
        Deluxe_roominfo = f"{Deluxe_roomname} - Php{price}\n{features}"
        Deluxe_radiobutton = tk.Radiobutton(Deluxe_roomlist, text=Deluxe_roominfo, variable=Deluxeselectroom, value=Deluxe_roomname, anchor='w', justify='left')
        Deluxe_radiobutton.pack(anchor='w', padx=20)

    # Button to confirm the room selection
    def Deluxe_confirmselection():
        Deluxe_roomname = Deluxeselectroom.get()
        if Deluxe_roomname != "Select a room":
            features, price = Deluxe_roompackages[Deluxe_roomname]
            deluxerooms.destroy()  
            Deluxe_inputdetails(Deluxe_roomname, features, price) 
        else:
            messagebox.showwarning("Selection Error", "Please select a room.")

    Deluxe_confirmbutton = tk.Button(deluxerooms, text="Confirm Selection", command=Deluxe_confirmselection)
    Deluxe_confirmbutton.place(x=620 , y= 600)

# Function to input guest details for deluxe room
def Deluxe_inputdetails(Deluxe_roomname, features, price):
    deluxeguest = tk.Toplevel(dash)
    deluxeguest.title("Guest and Booking Details")
    deluxeguest.geometry("2000x1000")

    tk.Label(deluxeguest, text="Guest and Booking Details").place(x= 620, y= 50)

    tk.Label(deluxeguest, text="Guest Name:").place(x= 620, y= 100)
    Deluxe_guestname = tk.Entry(deluxeguest)
    Deluxe_guestname.place(x= 620, y= 150)

    tk.Label(deluxeguest, text="Cellphone Number:").place(x= 620, y= 200)
    Deluxe_cpnum = tk.Entry(deluxeguest)
    Deluxe_cpnum.place(x= 620, y= 250)

    tk.Label(deluxeguest, text="Date of Reservation (YYYY-MM-DD):").place(x= 620, y= 300)
    Deluxe_resdate = tk.Entry(deluxeguest)
    Deluxe_resdate.place(x= 620, y= 350)

    tk.Label(deluxeguest, text="Number of Days Stay:").place(x= 620, y= 400)
    Deluxe_daystay = tk.Entry(deluxeguest)
    Deluxe_daystay.place(x= 620, y= 450)

    def Deluxe_confirmguestdetails():
        guest_name = Deluxe_guestname.get()
        cellphone = Deluxe_cpnum.get()
        date_of_reservation = Deluxe_resdate.get()
        num_days = Deluxe_daystay.get()

        # Validating the user input
        try:
            datetime.strptime(date_of_reservation, "%Y-%m-%d")
            num_days = int(num_days)
            if num_days <= 0:
                raise ValueError("Number of days must be greater than 0.")
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return

        # To get the RoomID for the selected room
        room_id = get_room_id(Deluxe_roomname)
        if room_id is not None:
            # Check if the room is reserved during the stay period
            if roomreserved(room_id, date_of_reservation, num_days):
                messagebox.showwarning("Reservation Error", "This room is already reserved during the selected date range.")
            else:
                # Calculate total price of stay
                total_price = price * num_days

                insert_guest(connection, guest_name, cellphone)
                cursor = connection.cursor()
                cursor.execute("SELECT LAST_INSERT_ID()")
                GuestID = cursor.fetchone()[0]

                insert_reservation(connection, GuestID, date_of_reservation, num_days, total_price, room_id)

                messagebox.showinfo("Reservation Summary", 
                                    f"Room Selected: {Deluxe_roomname}\n"
                                    f"Features: {features}\n"
                                    f"Price per Night: Php{price}\n"
                                    f"Total Price for {num_days} night(s): Php{total_price}\n"
                                    f"Guest Name: {guest_name}\n"
                                    f"Cellphone: {cellphone}\n"
                                    f"Date of Reservation: {date_of_reservation}")
        else:
            messagebox.showerror("Error", "Room not found. Please select a valid room.")

        deluxeguest.destroy()


    Deluxe_confirmguestbttn = tk.Button(deluxeguest, text="Confirm Details", command=Deluxe_confirmguestdetails)
    Deluxe_confirmguestbttn.place(x= 620, y= 620)


# Function for admin login window
def show_admin_login():
    admin_login = tk.Toplevel(dash)
    admin_login.title("Admin Login")
    admin_login.geometry("300x200")

    tk.Label(admin_login, text="Admin Username:").pack(pady=10)
    admin_username = tk.Entry(admin_login)
    admin_username.pack(pady=5)

    tk.Label(admin_login, text="Admin Password:").pack(pady=10)
    admin_password = tk.Entry(admin_login, show="*")
    admin_password.pack(pady=5)

    def login():
        if admin_username.get() == "RRadmin" and admin_password.get() == ADMIN_PASSWORD:
            messagebox.showinfo("Login Successful", "Welcome Admin!")
            admin_login.destroy()  # Close login window
            admin_dashboard()  # Show admin dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    tk.Button(admin_login, text="Login", command=login).pack(pady=20)

# Function to show admin dashboard
def admin_dashboard():
    admin_dash = tk.Toplevel(dash)
    admin_dash.title("Admin Dashboard")
    admin_dash.geometry("1750x750")

    tk.Label(admin_dash, text="Admin Dashboard", font=("Helvetica", 18)).pack(pady=50)

    # Button for viewing reservations
    tk.Button(admin_dash, text="View Reservations", command=view_reservations).pack(pady=50)

    # Button for viewing guests
    tk.Button(admin_dash, text="View Guests", command=view_guests).pack(pady=50)

    # Button for viewing feedback
    tk.Button(admin_dash, text="View Rooms", command=view_rooms).pack(pady=50)

# Function to view reservations
def view_reservations():
    display_table("Reservation")

# Function to view guests
def view_guests():
    display_table("Guest")

# Function to view feedback
def view_rooms():
    display_table("Room")

# Function to display a specific table from the database
def display_table(table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [i[0] for i in cursor.description]  # Get column names

        # Create a new window to display table contents
        table_window = tk.Toplevel(dash)
        table_window.title(f"{table_name} Table")
        table_window.geometry("1000x500")

        tree = ttk.Treeview(table_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)

        for row in rows:
            tree.insert('', 'end', values=row)

        tree.pack(expand=True, fill='both')

        # Delete row button
        delete_button = tk.Button(table_window, text="Delete Selected", command=lambda: delete_selected_row(tree, table_name))
        delete_button.pack(pady=20)
        # Go Back Button
        go_back_button = tk.Button(table_window, text="Go Back", command=table_window.destroy)
        go_back_button.pack(pady=20)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Function to delete selected row from the table
def delete_selected_row(tree, table_name):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a row to delete.")
        return
    
    item_values = tree.item(selected_item)['values'] 
    primary_key_value = item_values[0]
    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete row with {table_name} ID {primary_key_value}?")
    
    if confirm:  
        delete_query = f"DELETE FROM {table_name} WHERE {table_name}ID = {primary_key_value}" 

        execute_query(connection, delete_query)
        tree.delete(selected_item)
        messagebox.showinfo("Success", f"Row with {table_name} ID {primary_key_value} deleted successfully.")
    else:  
        messagebox.showinfo("Deletion Canceled", "The deletion was canceled.")

# MAIN DASHBOARD OF THE PROGRAM
dash = tk.Tk()
dash.title('RoomRadar')
dash.geometry('2000x1000')     

# Label for RoomRadar
label1r = Label(dash, 
            text='RoomRadar',
            font=('Comic Sans MS', 50, 'bold'),
            fg='Blue')
label1r.place(x=500, y=60)
# Label for welcome
label2w = Label(dash, 
            text='Welcome, Prestigious Guest!',
            font=('Times New Roman', 18),
            fg='Blue')
label2w.place(x=100, y=230)
# Label for your comfort
label3y = Label(dash, 
            text='Your Comfort, Our Priority!',
            font=('Times New Roman', 13, 'italic'),
            fg='Blue')
label3y.place(x=550, y=150)
# Label for explore
label4e = Label(dash, 
            text='Explore our diverse selection of beautifully designed rooms, each tailored to provide a unique and comfortable experience for you!',
            font=('Times New Roman', 13, 'italic'),
            fg='Blue')
label4e.place(x=100, y=280)
# Button for standard
bttn1 = Button(dash, text='STANDARD',
            font=('Times New Roman', 20, 'bold'),
            fg='Black')
bttn1.pack()
bttn1.place(x=250, y=450)
bttn1.config(command=showstandardrooms) 
# Button for suite
bttn2 = Button(dash, text='SUITE', 
            font=('Times New Roman', 20, 'bold'),
            fg='Black')
bttn2.pack()
bttn2.place(x=530, y=450)
bttn2.config(command=showsuiterooms) 
# Button for deluxe
bttn3 = Button(dash, text='DELUXE', 
            font=('Times New Roman', 20, 'bold'),
            fg='Black')
bttn3.pack()
bttn3.place(x=750, y=450)
bttn3.config(command=showdeluxerooms) 

# Function to view reservations
def historyreservation():
    historydisplay("Reservation")

# Button for history
bttn4 = Button(dash, text='H\nI\nS\nT\nO\nR\nY\n\nR\nE\nS\nE\nR\nV\nA\nT\nI\nO\nN', 
            font=('Times New Roman', 15)) 
bttn4.pack()
bttn4.place(x=1210, y=200)
bttn4.config(command=historyreservation)

# Function to display a specific table from the database
def historydisplay(table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [i[0] for i in cursor.description]  # Get column names

        # Create a new window to display table contents
        table_window = tk.Toplevel(dash)
        table_window.title(f"{table_name} Table")
        table_window.geometry("1000x500")

        tree = ttk.Treeview(table_window, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)

        for row in rows:
            tree.insert('', 'end', values=row)

        tree.pack(expand=True, fill='both')
    
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# Button for admin
bttn5 = Button(dash, text='Admin ',
               font=('Times New Roman', 15)) 
bttn5.pack()
bttn5.place(x=1200, y=50)
bttn5.config(command=show_admin_login)
dash.mainloop()

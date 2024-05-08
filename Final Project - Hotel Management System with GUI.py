import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
from mysql.connector import Error
from datetime import date, datetime, timedelta

#function to connect to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(host='your host', database='hotelmanagementsystem', user='your username', password='your password')
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to the database: {e}")
        return None

#function to list available rooms
def list_available_rooms():
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT HOTEL.Hotel_name, ROOM.Room_number, ROOM.Room_type, ROOM.Room_status, ROOM.Price_per_night FROM HOTEL, ROOM WHERE HOTEL.Hotel_id=ROOM.Hotel_id")
            rooms = cursor.fetchall()
            cursor.execute("SELECT * FROM HOTEL")
            hotel_information = cursor.fetchall()
            if not rooms:
                messagebox.showinfo("Available Rooms", "No available rooms.")
            else:
                updated_rooms = []
                for room in rooms:
                    room_number = room[1]
                    cursor.execute("SELECT Checkin_date, Checkout_date FROM BOOKING WHERE Room_number=%s ORDER BY Checkin_date", (room_number,))
                    reserved_dates = cursor.fetchall()
                    if reserved_dates:
                        reserved_info = "Reserved on dates: "
                        for reserved_date in reserved_dates:
                            reserved_info += f"{reserved_date[0]} - {reserved_date[1]}, "
                        room = room + (reserved_info,)
                    else:
                        room = room + ("Available for reservation",)
                    updated_rooms.append(room)
                show_table("Available Rooms", ["Hotel name", "Room number", "Room type", "Room status", "Price per night", "Reservation Info"], updated_rooms)
                show_table("Hotel Information", ["Hotel ID", "Hotel name", "Hotel number", "Stars", "Check-in time", "Check-out time", "Address Line", "City", "State", "Zipcode"], hotel_information)
        except Error as e:
            messagebox.showerror("Error", f"Error listing available rooms: {e}")

#function to make a reservation
def make_reservation():
    def submit_reservation():
        try:
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            email = email_entry.get()
            date_of_birth = dob_entry.get()
            mobile_number = mobile_number_entry.get()

            connection = connect_to_database()
            if connection:
                cursor = connection.cursor()

                cursor.execute("INSERT INTO GUEST (First_name, Last_name, Email, Date_of_birth) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, date_of_birth))
                connection.commit()

                cursor.execute("SELECT LAST_INSERT_ID()")
                guest_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO GUEST_MOBILE_NUMBER (Mobile_number, Guest_id) VALUES (%s, %s)", (mobile_number, guest_id))
                connection.commit()

                hotel_id = int(hotel_id_entry.get())
                room_number = int(room_number_entry.get())
                cursor.execute("SELECT Room_number, Price_per_night FROM ROOM WHERE Room_number=%s", (room_number,))
                room_existence = cursor.fetchone()
                if not room_existence:
                    raise ValueError("Room does not exist.")
                room_number, price_per_night = room_existence

                check_in_date = checkin_entry.get_date()
                check_out_date = checkout_entry.get_date()
                reservation_duration = (check_out_date - check_in_date).days
                total_price = reservation_duration * price_per_night
                cursor.execute("SELECT * FROM BOOKING WHERE Room_number=%s AND (Checkin_date BETWEEN %s AND %s OR Checkout_date BETWEEN %s AND %s)", (room_number, check_in_date, check_out_date, check_in_date, check_out_date))
                overlapping_reservations = cursor.fetchall()
                if overlapping_reservations:
                    raise ValueError("Room is already reserved for the selected dates.")
                
                number_of_guest = int(num_guest_entry.get())

                cursor.execute("UPDATE ROOM SET Room_status='occupied' WHERE Room_number=%s", (room_number,))
                connection.commit()

                cursor.execute("INSERT INTO BOOKING (Guest_id, Hotel_id, Room_number, Checkin_date, Checkout_date, Number_of_guest, Total_price) VALUES (%s, %s, %s, %s, %s, %s, %s)", (guest_id, hotel_id, room_number, check_in_date, check_out_date, number_of_guest, total_price))
                connection.commit()

                messagebox.showinfo("Reservation", f"Reservation made successfully!\n\n***Guest ID***: {guest_id}")
                reservation_window.destroy()
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input. {ve}")
        except Error as e:
            connection.rollback()
            messagebox.showerror("Error", f"Error making reservation: {e}")

    reservation_window = tk.Toplevel()
    reservation_window.title("Make Reservation")
    reservation_window.configure(background='light blue')

    frame = ttk.Frame(reservation_window, padding="20", style="Background.TFrame")
    frame.grid(row=0, column=0)

    ttk.Label(frame, text="First Name:").grid(row=0, column=0, sticky="e")
    first_name_entry = ttk.Entry(frame)
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Last Name:").grid(row=1, column=0, sticky="e")
    last_name_entry = ttk.Entry(frame)
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e")
    email_entry = ttk.Entry(frame)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Date of Birth (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")
    dob_entry = ttk.Entry(frame)
    dob_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Mobile Number:").grid(row=4, column=0, sticky="e")
    mobile_number_entry = ttk.Entry(frame)
    mobile_number_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Hotel ID:").grid(row=5, column=0, sticky="e")
    hotel_id_entry = ttk.Entry(frame)
    hotel_id_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Room Number:").grid(row=6, column=0, sticky="e")
    room_number_entry = ttk.Entry(frame)
    room_number_entry.grid(row=6, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Check-in Date:").grid(row=7, column=0, sticky="e")
    checkin_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    checkin_entry.grid(row=7, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Check-out Date:").grid(row=8, column=0, sticky="e")
    checkout_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    checkout_entry.grid(row=8, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Number of Guests:").grid(row=9, column=0, sticky="e")
    num_guest_entry = ttk.Entry(frame)
    num_guest_entry.grid(row=9, column=1, padx=5, pady=5)

    submit_button = ttk.Button(frame, text="Submit", command=submit_reservation)
    submit_button.grid(row=10, columnspan=2, pady=10)

def calculate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return age

#function to confirm and notify guests
def notify_guest():
    def show_guest_info():
        try:
            guest_id = int(guest_id_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valud integer for Guest ID.")
        connection = connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT GUEST.First_name, GUEST.Last_name, GUEST.Email, GUEST.Date_of_birth, GUEST_MOBILE_NUMBER.Mobile_number FROM GUEST JOIN GUEST_MOBILE_NUMBER ON GUEST.Guest_id = GUEST_MOBILE_NUMBER.Guest_id WHERE GUEST.Guest_id = %s", (guest_id,))
                guest_info = cursor.fetchone()
                
                cursor.execute("SELECT HOTEL.Hotel_name, HOTEL.Hotel_number, HOTEL.Stars, HOTEL.Checkin_time, HOTEL.Checkout_time, HOTEL.Address_line, HOTEL.City, HOTEL.State, HOTEL.Zip_code FROM BOOKING JOIN HOTEL ON BOOKING.Hotel_id = HOTEL.Hotel_id WHERE BOOKING.Guest_id = %s", (guest_id,))
                hotel_info = cursor.fetchall()

                cursor.execute("SELECT Booking_id, Room_number, Checkin_date, Checkout_date, Number_of_guest, Total_price FROM BOOKING WHERE Guest_id = %s", (guest_id,))
                booking_info = cursor.fetchall()

                if not guest_info:
                    messagebox.showinfo("Guest Information", "No guest found with the given ID.")
                else:
                    date_of_birth = guest_info[3]
                    age = calculate_age(date_of_birth)
                    guest_info_with_age = guest_info + (age,)
                    show_table("Guest Information", ["First Name", "Last Name", "Email", "Date of Birth", "Mobile Number", "Age"], [guest_info_with_age])
                    show_table("Hotel Information", ["Hotel Name", "Hotel Number", "Stars", "Check-in Time", "Check-out Time", "Address Line", "City", "State", "Zip Code"], hotel_info)
                    show_table("Booking Information", ["Booking ID", "Room Number", "Check-in Date", "Check-out Date", "Number of Guests", "Total price"], booking_info)
            except Error as e:
                messagebox.showerror("Error", f"Error notifying guest: {e}")

    notify_window = tk.Toplevel()
    notify_window.title("Notify Guest")
    notify_window.configure(background='light blue')

    frame = ttk.Frame(notify_window, padding="20", style="Background.TFrame")
    frame.grid(row=0, column=0)

    ttk.Label(frame, text="Guest ID:").grid(row=0, column=0, sticky="e")
    guest_id_entry = ttk.Entry(frame)
    guest_id_entry.grid(row=0, column=1, padx=5, pady=5)

    submit_button = ttk.Button(frame, text="Show Reservation Info", command=show_guest_info)
    submit_button.grid(row=1, columnspan=2, pady=10)

#function to display tables in a new window
def show_table(title, headers, data):
    table_window = tk.Toplevel()
    table_window.title(title)
    table_window.configure(background='light blue')

    frame = ttk.Frame(table_window, padding="20", style="Background.TFrame")
    frame.grid(row=0, column=0)

    tree = ttk.Treeview(frame, columns=headers, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in headers:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, width=max(100, len(col) * 20), anchor="center")

    for row in data:
        tree.insert("", "end", values=row)

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.config(yscrollcommand=scrollbar.set)

    for i, col in enumerate(headers):
        max_width = max([len(str(row[i])) for row in data])
        tree.column(col, width=max(100, max_width * 12), anchor="center")

    for col in headers:
        tree.heading(col, text=col, anchor="center", command=lambda _col=col: tree_sort_column(tree, _col))

#create main window and pack GUI elements
def create_main_window():
    root = tk.Tk()
    root.title("Hotel Management System")
    root.configure(background='light blue')

    # Header
    header_label = ttk.Label(root, text="Hotel Management System", font=("Helvetica", 20, "bold"), background='light blue')
    header_label.pack(pady=20)

    frame = ttk.Frame(root, padding="20", style="Background.TFrame")
    frame.pack()

    list_rooms_button = ttk.Button(frame, text="List Available Rooms", command=list_available_rooms)
    list_rooms_button.grid(row=0, column=0, pady=5)

    make_reservation_button = ttk.Button(frame, text="Make Reservation", command=make_reservation)
    make_reservation_button.grid(row=1, column=0, pady=5)

    notify_guest_button = ttk.Button(frame, text="Notify Guest", command=notify_guest)
    notify_guest_button.grid(row=2, column=0, pady=5)

    return root

def tree_sort_column(tree, col, reverse=False):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    try:
        data.sort(key=lambda x: int(x[0]), reverse=reverse)
    except ValueError:
        data.sort(reverse=reverse)

    for index, (val, child) in enumerate(data):
        tree.move(child, '', index)

    tree.heading(col, command=lambda: tree_sort_column(tree, col, not reverse))

if __name__ == "__main__":
    root = create_main_window()
    root.mainloop()

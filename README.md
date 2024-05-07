# Hotel Management System with GUI

This final project is a hotel management system implemented in SQL and Python. I used MySQL by first writing SQL scripts to implement the schema design. Then, I populated the tables with basic values suitable for testing my functions. Following this, I utilized Python to establish a connection with the MySQL database and implemented the remaining functionality with the GUI. The system allows you to list available rooms, reserve rooms, and notify guests about their reservations.

## Features

-List Available Rooms: View a list of available rooms in the hotel along with their details, such as hotel name, room number, room type, and room status, along with the corresponding hotel information.

-Make Reservation: Allow guests to make reservations by providing their personal information and desired booking details.

-Confirm and Notify Guest: Retrieve guest information, hotel information, and booking details based on the provided guest ID to confirm and notify guests about their reservations.


## Requirements

-Python 3.xx

-Tkinter (should be included with the Python installation)

-Python/MySQL connector (installed via 'pip install mysql-connector-python' on cmd)

-MySQL Workbench


## Installation and Usage

1. After having met the requirements, download the 'Hotel System with GUI.py' and 'Hotel Management System Table.sql' files.
2. Open the .sql file in MySQL, and after running it, a database with tables and testing values will be created.
3. Then, open the .py file with Python IDLE.
4. You might need to update the database connection details in the Python script to match your MySQL server configuration, which is located on the 'connect_to_database' function.
5. Save and run the Python script.
6. The GUI will open, allowing you to interact with the three fundamental functions.


## Please note:

This is just the basic version of the hotel management system application, meeting the requirements of my final project, and I am hoping to further implement and develop this program in order to have more features that can be used by end users.

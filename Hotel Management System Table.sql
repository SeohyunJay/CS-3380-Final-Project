create schema hotelmanagementsystem;

use hotelmanagementsystem;

create table HOTEL(
	Hotel_id int not null,
    Hotel_name varchar(255) not null,
    Hotel_number varchar(15) not null,
    Stars int not null,
    Checkin_time varchar(50) not null,
    Checkout_time varchar(50) not null,
    Address_line varchar(255) not null,
    City varchar(50) not null,
    State varchar(15) not null,
    Zip_code int not null,
    primary key(Hotel_id)
);

create table GUEST(
	Guest_id int auto_increment,
    First_name varchar(50) not null,
    Last_name varchar(50) not null,
    Email varchar(255),
    Date_of_birth date not null,
    #Age, a derived attribute, is implemented through Python
    primary key(Guest_id)
);

create table GUEST_MOBILE_NUMBER(
	Mobile_number varchar(15) not null,
    Guest_id int not null,
    foreign key(Guest_id) references GUEST(Guest_id)
);

create table ROOM(
	Room_number int not null,
    Room_type varchar(50),
    Room_status enum('available','occupied','under maintenance'),
    Price_per_night decimal(10,2),
    Hotel_id int,
    primary key(Room_number),
    foreign key(Hotel_id) references HOTEL(Hotel_id)
);

create table BOOKING(
	Booking_id int auto_increment,
    Hotel_id int,
    Room_number int,
    Total_price decimal(10,2),
    Checkin_date date not null,
    Checkout_date date not null,
    Number_of_guest int not null,
    Guest_id int,
    primary key(Booking_id),
    foreign key(Hotel_id) references HOTEL(Hotel_id),
    foreign key(Guest_id) references GUEST(Guest_id),
    foreign key(Room_number) references ROOM(Room_number)
);

create table EMPLOYEE(
	Employee_id int not null,
    First_name varchar(50) not null,
    Last_name varchar(50) not null,
    Position varchar(50) not null,
    Hotel_id int not null,
    primary key(Employee_id),
    foreign key(Hotel_id) references HOTEL(Hotel_id)
);

create table EMPLOYEE_MOBILE_NUMBER(
	Mobile_number varchar(15) not null,
    Employee_id int not null,
    foreign key(Employee_id) references EMPLOYEE(Employee_id)
);

create table PAYMENT(
	Payment_id int not null,
    Payment_amount decimal(10,2) not null,
    Payment_date date not null,
    Payment_method varchar(50) not null,
    Booking_id int,
    primary key(Payment_id),
    foreign key(Booking_id) references BOOKING(Booking_id)
);

create table ROOM_TYPE(
	Type_id int not null,
    Room_name varchar(50) not null,
    Price_per_night decimal(10,2) not null,
    Capacity int not null,
    primary key(Type_id)
);

insert into HOTEL
values (1,'Hampton Inn & Suites','(573) 214-2222',3,'15:00:00','11:00:00','1225 Fellows Pl','Columbia','MO','65201');
insert into HOTEL
values (2,'Grand Hyatt','(972) 973-1234',4,'15:00:00','12:00:00','2337 S International Pkwy','Dallas','TX','75261');
insert into HOTEL
values (3,'The Inn Above Tidel','(415) 332-9535',4,'15:00:00','11:00:00','30 El Portal','Sausalito','CA','94965');

insert into ROOM
values (100,'Standard','available',100.00,1);
insert into ROOM
values (200,'Deluxe','available',120.00,1);
insert into ROOM
values (300,'Suite','available',150.00,1);

insert into ROOM
values (400,'Standard','available',150.00,2);
insert into ROOM
values (500,'Deluxe','available',200.00,2);
insert into ROOM
values (600,'Suite','available',250.00,2);

insert into ROOM
values (700,'Standard','available',200.00,3);
insert into ROOM
values (800,'Deluxe','available',300.00,3);
insert into ROOM
values (900,'Suite','available',400.00,3);
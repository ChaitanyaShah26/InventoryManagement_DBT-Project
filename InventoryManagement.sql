create database InventoryManagement;
use InventoryManagement;

create table employee
(
    e_id int primary key,
    e_name varchar(50) not null,
    e_age int,
    e_experience int
);

create table customer_care
(
    cc_id int primary key,
    cc_contact int,
    cc_location varchar(100),
    e_id int,
    foreign key (e_id) references employee(e_id)
);

create table warehouse
(
    w_no int primary key,
    w_capacity int,
    w_location varchar(100)
);

create table provider
(
    pr_id int primary key,
    pr_type varchar(40),
    pr_address varchar(100)
);

create table products
(
    p_id int primary key,
    p_price int,
    p_expiry varchar(20)
);

create table offers
(
    o_no int primary key,
    o_name varchar(50),
    o_type varchar(20)
);

create table customer
(
    c_id int primary key,
    c_name varchar(50) not null,
    c_contact int,
    c_age int
);

create table payment
(
    py_id int primary key,
    py_time varchar(10),
    py_date varchar(16),
    py_mode varchar(50) not null
);

create table online
(
    on_upi varchar(80),
    on_credit varchar(80),
    on_debit varchar(80)
);

create table offline
(
    off_cod varchar(80)
);
import mysql.connector as ms
from tabulate import tabulate
import menu
from utils import clear_screen
import time


def make_con(db=None):
    """ Make a mySQL connection """
    PASS = 'my3ql'
    # PASS = 'my3qlP@ssword'
    if db:
        con = ms.connect(host='localhost', user='root', passwd=PASS, database=db)
    else:
        con = ms.connect(host='localhost', user='root', passwd=PASS)
    cur = con.cursor()
    return con, cur


def create_db(cur):
    """ Create the Database """
    cur.execute('CREATE DATABASE IF NOT EXISTS Password_manager;')
    cur.execute('USE Password_manager;')
    cur.execute('''CREATE TABLE IF NOT EXISTS Usernames (
        Item int primary key auto_increment,
        Category varchar(30),
        Name varchar(30),
        URL varchar(50),
        Username varchar(30)
    );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Passwords (
        Item int primary key auto_increment,
        Password varchar(1000)
    );''')


def get_all_rec():
    """ Display all the details """
    con, cur = make_con(db='Password_manager')
    cur.execute('select * from Usernames')
    all_rec = cur.fetchall()
    close_con(con)
    return all_rec


def close_con(con):
    """ Close the mySQL connection """
    con.close()


def to_table(rows=[]):
    """ Print the rows as table """
    if len(rows) > 0:
        print()
        print(tabulate(rows, ['Item', 'Category', 'Name', 'URL', 'Username']))
        print()
    else:
        print()
        print('No login items added yet. Add some!')
        print()


def query_db(query):
    """ Query the database """
    con, cur = make_con(db='Password_manager')
    cur.execute(f'select * from Passwords where {query};')
    rec = cur.fetchall()
    close_con(con)
    return rec


def search_id(query):
    """ Search database by id if query is int """
    if query.isdigit():
        rec = query_db(f'id = {query}')
        if rec:
            return [rec]


def search():
    """ Searches the database """
    query = menu.get_input(message='Search: ')

    if query in ['d', 'a', 'q']:
        return query

    results = search_id(query)

    if len(results) == 1:
        show_item(results)


def show_item(item):
    """ Shows one password item """
    clear_screen()
    print(to_table(item))


def add_items(name, url='', password=''):
    """ Adds a new login item """
    con, cur = make_con(db='Password_manager')
    q = f"INSERT INTO Usernames (Name, URL, Username) VALUES ('{name}', '{url}', '{password}');"
    cur.execute(q)
    con.commit()
    close_con(con)


def add():
    """ Ask for login details and add it """
    clear_screen()

    name = menu.get_input("Name: ")
    if name is False:
        return False

    url = menu.get_input("URL: ")
    if url is False:
        return False

    user = menu.get_input("Username: ")
    if user is False:
        return False

    password = menu.get_input("Password: ", secure=True)
    if password is False:
        return False

    add_items(name, url, password)

    print()
    print('The new items have been added!')
    print()

    time.sleep(5)

import sqlite3
from easygui import *
import models


db_file = 'bookie.sqlite'
conn = sqlite3.connect(db_file)
c = conn.cursor()


def home():

    msgbox('Welcome to autoBookie. The world\'s leading software for bookies\n', title='Welcome', ok_button='Advance')



def clear_table():
    # this function is used to delete the 'client' table from the database
    c.execute('drop table client')


def menu():
    # this function displays the menu given to the user and handles all choices made.
    # think of this as the program hub.
    client = models.Client()

    button_choices = {'first': ['Project', 'Client', 'Employee'],
                      'second': ['Create new client account', 'Display a client account',
                                 'Display all client accounts', 'Update client balance', 'Exit']}

    a = buttonbox('Which category will you be working in today?', 'autoBookie', choices=button_choices['first'])

    x = ''

    if a == 'Client':
        x = buttonbox('Please choose your option', 'autoBookie', choices=button_choices['second'])

    if x == 'Create new client account':

        msg = "Enter client information"
        title = "New client form"
        fieldNames = ["Name", "Street Address", "City", "Phone Number", "Balance"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg, title, fieldNames)

        if fieldValues:
            client.create_client_account(fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4])
        else:
            menu()

    elif x == 'Update client balance':

        client.update_client_balance()
        menu()

    elif x == 'Display a client account':
        # this option allows the user to select specific clients based on their id numbers.
        # the following function allows the user to update or delete said account.
        x = enterbox('Please enter the client\'s ID number')
        y = client.display_client_info(x)
        textbox('Name: ' + y[0] + '\n' + 'Address: ' + y[1] + '\n' + 'City: ' + y[2] + '\n' + 'Phone Number: ' + y[3] + '\n' + 'Balance: ' + y[4])
        menu()

    elif x == 'Display all client accounts':
        client.display_all_clients()
        menu()

    elif x == 'Exit':
        # this option ends the program, it is essentially an X button.
        return False
    else:
        print(x)


def delete_client_account(user_id):
    # this function is simply removing the client from the table.
    c.execute('''DELETE FROM client WHERE ROWID = ? ''', (user_id,))

    conn.commit()


def update_client_balance(user_id):
    # this function allows the user to update the client balance.
    c.execute('''select balance from client where ROWID=?''', (user_id,))
    balance = c.fetchone()
    real_balance = balance[0]

    print('Okay, if we are adding to the balance, enter A \n'
          'if we are subtracting from the balance, enter S ')
    x = input()

    if x == 'A':

        print('Great, what is the amount?')
        y = float(input())
        new_balance = real_balance + y
        c.execute('''update client set balance =? where ROWID = ?''', (new_balance, user_id,))
        conn.commit()
        # the below print statement and strange formatting is only there to add commas to the client balance.
        print('The client\'s new balance is: ${:,.2f}'.format(new_balance))
        print('\n')

    if x == 'S':

        print('Great, what is the amount?')
        y = float(input().replace(',', ''))
        new_balance = real_balance - y
        # the following if statement provides a measure of security against taking too much money from a balance.
        # it is a rare occurence when a customer is given credit, so you would want to double check here.
        if new_balance < 0:
            print('Warning! This will cause the client account to go into the negative.')
            print('Are you sure you want to do this? (Y/N)')
            z = input()
            if z == 'Y':
                c.execute('''update client set balance =? where ROWID = ?''', (new_balance, user_id,))
                conn.commit()
                print('The client\'s new balance is: ', new_balance)
            elif z == 'N':
                print('Disaster averted')





def retrieve_name(user_id):
    # this function does the actual name retrieval. I got tired of repeatedly typing this so I made a shortcut
    c.execute('''select name from client where ROWID=?''', (user_id,))
    name = c.fetchone()
    return name[0]

















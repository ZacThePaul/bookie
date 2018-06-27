import sqlite3
import Dialogue as d

db_file = 'bookie.sqlite'
conn = sqlite3.connect(db_file)
c = conn.cursor()


def clear_table():
    # this function is used to delete the 'client' table from the database
    c.execute('drop table client')


def create_client_account(name, address, city, number, balance):
    # this function creates the table 'client' and adds in its respective fields.
    # in addition, it adds in the input the user provided to the database.
    c.execute('create table if not exists client(name TEXT, address VARCHAR, city VARCHAR, number INTEGER, balance REAL)')
    c.execute('insert into client values(?, ?, ?, ?, ?)', (name, address, city, number, balance),)
    conn.commit()


def menu(option):
    # this function displays the menu given to the user and handles all choices made.
    # think of this as the program hub.
    if option == 'n':
        # if the user wants to create a new client file, the program takes in this information and
        # runs the client create function using it. Then ir returns the user to the menu.
        print('Okay, I just need some information from you.')
        name = input('What is the client\'s name?')
        address = input('What is the client\'s address?')
        city = input('What is the client\'s city?')
        number = input('What is the client\'s 10 digit phone number? No special characters please.')
        balance = input('Does the client have an initial balance? If not, enter 0.')

        create_client_account(name, address, city, number, balance)
        option = d.welcome()
        menu(option)

    elif option == 'l':
        # this option allows the user to select specific clients based on their id numbers.
        # the following function allows the user to update or delete said account.
        print('Okay, what is the client\'s ID number?')
        x = input()
        display_client_info(x)
        option = d.welcome()
        menu(option)

    elif option == 'a':
        # this option allows the user to see every client in the table.
        display_all_clients()

    elif option == 'b':
        # this option only displays the name and balance of a client.
        print('Okay, what is the client\'s ID number?')
        x = input()
        display_client_balance(x)

    elif option == 'x':
        # this option ends the program, it is essentially an X button.
        print('Thank you for choosing our services. Goodbye.')


def display_client_info(user_id):
    # this function takes the user id of a client and displays all of their information.
    # then it allows the user to update the balance or delete the account.
    c.execute('''SELECT ROWID, name, address, city, number, balance FROM client WHERE ROWID=?''', (user_id,))
    user = c.fetchone()
    print(

        '\nClient Name: ' + str(user[1]),
        '\nClient Address: ' + str(user[2]),
        '\nClient City: ' + str(user[3]),
        '\nClient Phone Number: ' + str(user[4]),
        '\nClient balance: ' + str(user[5]),
        '\n'

    )
    print('What would you like to do to this account?')
    print('Update balance = u. Delete client account = d')
    option = input()
    if option == 'd':
        # here the user calls the function that deletes accounts.
        delete_client_account(user_id)
        print('Account was successfully deleted!')
    elif option == 'u':
        # here the user calls the function that updates the balance.
        update_client_balance(user_id)


def display_all_clients():
    # this function allows the user to see every client in the table.
    c.execute('''select ROWID, name, address, city, number, balance from client''')
    # the for loop below loops through the list that is stored in the C object and the print function
    # prints each individual client out.
    for row in c:
        print(
            '\n',
            'Client ID: {} \n'.format(str(row[0])),
            'Client Name: {} \n'.format(str(row[1])),
            'Client Address: {} \n'.format(str(row[2])),
            'Client City: {} \n'.format(str(row[3])),
            'Client Phone Number: {} \n'.format(str(row[4])),
            'Client Balance: {} \n'.format(str(row[5])),
            '\n'
        )


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


def retrieve_balance(user_id):
    # this function does the actual balance retrieval. I got tired of repeatedly typing this so I made a shortcut
    c.execute('''select balance from client where ROWID=?''', (user_id,))
    balance = c.fetchone()
    return balance[0]


def retrieve_name(user_id):
    # this function does the actual name retrieval. I got tired of repeatedly typing this so I made a shortcut
    c.execute('''select name from client where ROWID=?''', (user_id,))
    name = c.fetchone()
    return name[0]


def display_client_balance(user_id):
    # this function does the actual displaying of balances. This function would be called from other functions
    # to do the actual work.
    balance = retrieve_balance(user_id)
    name = retrieve_name(user_id)

    print(name, '\'s balance is ', balance)
    print('\n')
    option = d.menu_display()
    menu(option)






















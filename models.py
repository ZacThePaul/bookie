import sqlite3
from easygui import *
import functions as f

db_file = 'bookie.sqlite'
conn = sqlite3.connect(db_file)
c = conn.cursor()


class Client:

    def __init__(self):
        self.create_table()

    def create_table(self):
        c.execute('create table if not exists client(name TEXT, address VARCHAR, city VARCHAR, number INTEGER, balance REAL)')


    def create_client_account(self, name, address, city, number, balance):
        # this function creates the table 'client' and adds in its respective fields.
        # in addition, it adds in the input the user provided to the database.
        c.execute('insert into client values(?, ?, ?, ?, ?)', (name, address, city, number, balance), )
        conn.commit()

    def display_client_info(self, user_id):
        # this function takes the user id of a client and displays all of their information.
        # then it allows the user to update the balance or delete the account.
        c.execute('''SELECT ROWID, name, address, city, number, balance FROM client WHERE ROWID=?''', (user_id,))
        user = c.fetchone()

        name = str(user[1])
        add = str(user[2])
        city = str(user[3])
        num = str(user[4])
        bal = str(user[5])
        return name, add, city, num, bal

    def display_all_clients(self):
        # this function allows the user to see every client in the table.
        c.execute('''select ROWID, name, address, city, number, balance from client''')
        # the for loop below loops through the list that is stored in the C object and the print function
        # prints each individual client out.

        x = []

        for row in c:
            x.append(

                'Client ID: {} '.format(str(row[0])) +
                'Client Name: {} '.format(str(row[1])) +
                'Client Address: {} '.format(str(row[2])) +
                'Client City: {} '.format(str(row[3])) +
                'Client Phone Number: {} '.format(str(row[4])) +
                'Client Balance: {} '.format(str(row[5])) +
                '                                          '
            )
        withnewlines = '\n'.join(x)

        textbox('All Client accounts', 'List all clients', str(withnewlines))

    def update_client_balance(self):

        identification = enterbox('Please enter client ID', 'autoBookie')
        balance = self.retrieve_balance(identification)
        yn = ynbox('Are you adding or subtracting from the balance?', 'autoBookie', ['Adding', 'Subtracting'])

        if yn:

            add = float(enterbox('How much will you add to client balance?', 'autoBookie'))
            new_balance = balance + add
            c.execute('''update client set balance =? where ROWID = ?''', (new_balance, identification,))
            conn.commit()
            clean_balance = self.retrieve_balance(identification)
            textbox('Client balance is now:  ${:,.2f}'.format(clean_balance))

        elif not yn:

            sub = float(enterbox('How much will you subtract from client balance?', 'autoBookie'))
            new_balance = balance - sub
            c.execute('''update client set balance =? where ROWID = ?''', (new_balance, identification,))
            conn.commit()
            clean_balance = self.retrieve_balance(identification)
            textbox('Client balance is now:  ${:,.2f}'.format(clean_balance))

    def retrieve_balance(self, user_id):

        # this function does the actual balance retrieval. I got tired of repeatedly typing this so I made a shortcut
        c.execute('''select balance from client where ROWID=?''', (user_id,))
        balance = c.fetchone()
        return balance[0]

    def delete_client_account(self, user_id):
        # this function is simply removing the client from the table.
        c.execute('''DELETE FROM client WHERE ROWID = ? ''', (user_id,))

        conn.commit()

    def client_menu(self):

        app = App()
        button_choices = ['Create new client account', 'Display a client account', 'Display all client accounts',
                          'Update client balance', 'Exit']
        x = ''

        x = buttonbox('Please choose your option', 'autoBookie', choices=button_choices)

        if x == 'Create new client account':

            msg = "Enter client information"
            title = "New client form"
            fieldNames = ["Name", "Street Address", "City", "Phone Number", "Balance"]
            fieldValues = []  # we start with blanks for the values
            fieldValues = multenterbox(msg, title, fieldNames)

            if fieldValues:
                self.create_client_account(fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3],
                                             fieldValues[4])
            else:
                app.menu()

        elif x == 'Update client balance':

            self.update_client_balance()

        elif x == 'Display a client account':

            x = enterbox('Please enter the client\'s ID number')
            y = self.display_client_info(x)
            textbox('Name: ' + y[0] + '\n' + 'Address: ' + y[1] + '\n' + 'City: ' + y[2] + '\n' + 'Phone Number: ' + y[
                3] + '\n' + 'Balance:  ${:,.2f}'.format(float(y[4])))
            app.menu()

        elif x == 'Display all client accounts':

            self.display_all_clients()
            app.menu()

        elif x == 'Exit':

            return False

        else:

            print(x)


class App:

    def home(self):
        msgbox('Welcome to autoBookie. The world\'s leading software for bookies\n', title='Welcome', ok_button='Advance')

    def menu(self):
        # this function displays the menu given to the user and handles all choices made.
        # think of this as the program hub.

        client = Client()

        button_choices = ['Project', 'Client', 'Employee']

        a = buttonbox('Which category will you be working in today?', 'autoBookie', choices=button_choices)

        if a == 'Client':
            client.client_menu()

    def clear_table(self):
        # this function is used to delete the 'client' table from the database
        c.execute('drop table client')




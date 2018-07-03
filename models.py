import sqlite3
from easygui import *

db_file = 'bookie.sqlite'
conn = sqlite3.connect(db_file)
c = conn.cursor()


class Client:

    def __init__(self):
        pass

    def create_client_account(self, name, address, city, number, balance):
        # this function creates the table 'client' and adds in its respective fields.
        # in addition, it adds in the input the user provided to the database.
        c.execute(
            'create table if not exists client(name TEXT, address VARCHAR, city VARCHAR, number INTEGER, balance REAL)')
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
            clean_balance = str(self.retrieve_balance(identification))
            textbox('Client balance is now ' + clean_balance)

        elif not yn:
            sub = float(enterbox('How much will you subtract from client balance?', 'autoBookie'))
            new_balance = balance - sub
            c.execute('''update client set balance =? where ROWID = ?''', (new_balance, identification,))
            conn.commit()
            clean_balance = str(self.retrieve_balance(identification))
            textbox('Client balance is now ' + clean_balance)

    def retrieve_balance(self, user_id):

        # this function does the actual balance retrieval. I got tired of repeatedly typing this so I made a shortcut
        c.execute('''select balance from client where ROWID=?''', (user_id,))
        balance = c.fetchone()
        return balance[0]



class App:
    pass


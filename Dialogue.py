def welcome():
    print('Welcome to autobooks. The world\'s leading bookkeeping A.I.')
    print('Please select the action you would like to take \n')

    # balance check should print out all available clients

    x = input(
        'n = create new customer file. b = balance check. \n\n'
        'l = list a client account. a = list all client accounts. \n\n'
        'u = update client balance. x = exit program.'
    )

    return x


def menu_display():

    print('Please select the action you would like to take \n')

    x = input(
        'n = create new customer file. b = balance check. \n\n'
        'l = list a client account. a = list all client accounts. \n\n'
        'u = update client balance. x = exit program.'
    )

    return x




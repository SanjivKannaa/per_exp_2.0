import os
import time
from cryptography.fernet import Fernet
import pickle
import csv




os.system('color A')


def encry(data):
    key = b'2tXATpqnMs7bRk6mGXjglY1fuFgrw8nW1jIBSsLjMP8='
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


def decry(data):
    key = b'2tXATpqnMs7bRk6mGXjglY1fuFgrw8nW1jIBSsLjMP8='
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()







def login(password):
    f = open('accounts.bin', 'rb')
    content = decry(pickle.load(f)['login']['password'])
    f.close()
    if password == content:
        menu()
    else:
        os.system('color C')
        print('wrong password...')
        time.sleep(0.1)
        os.system('color A')
        login(input('enter the password : '))

def menu():
    time.sleep(0.5)
    print('\n\n\t\t\t\t\t\t\tMenu\n\n1. new transaction\n2. generate report\n3. manage accounts\n4. backup options\n5. view raw data\n6. category options\n7. change password\n8. refresh\n99. exit')
    choice = input('>>')
    if choice == '1':
        new_transaction()
    elif choice == '2':
        report_menu()
    elif choice == '3':
        manage_accounts()
    elif choice == '4':
        backup_menu()
    elif choice == '5':
        view_raw_data()
    elif choice == '6':
        category_options()
    elif choice == '7':
        refresh()
    elif choice == '8':
        change_password(old1=input('enter the old password : '), old2=input('enter the old password again'), new=input('enter the new password : '))
    elif choice == '99':
        exit()
    else:
        print('wrong input...')
        menu()








##########################################################################################################################
# new transaction
def new_transaction():
    try:
        time_automatic = time.strftime("%d %m %Y", time.gmtime())
        bill_no = input('enter the bill no : ')
        date = input('enter the transaction date[leave empty if its today {} ] : '.format(time_automatic))
        if date == '' : 
            date = time.strftime("%d %m %Y", time.gmtime())
        for i in range(int(input('enter the number of transactions : '))):
            f = open('data.csv', 'r')
            content = list(csv.reader(f))
            f.close()
            for j in content[::-1]:
                try:
                    transaction_no = 1 + int(j[0])
                except:
                    pass
            while True:
                from_ = input('enter from account : ')
                to_ = input('enter to account : ')
                if from_ in accounts_list_function() or to_ in accounts_list_function():
                    break
            while True:
                category_list_as_a_string = ''
                category_list = list(category_list_function(['category', '']))
                for i in category_list:
                    category_list_as_a_string += ' ' + str(i)
                category = input('enter the categpry[{}] : '.format(category_list_as_a_string))
                if category in category_list_function(['category', '']):
                    subcategory_list_as_a_string = ''
                    subcategory_list = category_list_function(['subcategory', category])
                    for i in subcategory_list:
                        subcategory_list_as_a_string += ' ' + str(i)
                    subcategory = input('enter the subcatrgory[{}] : '.format(subcategory_list_as_a_string))
                if check_category_function(category, subcategory) == True:
                    break
            description = input('enter the decription : ')
            amount = str(int(input('enter the amount : ')))
            if from_ in accounts_list_function():
                dec_balance(account=from_, amount=amount)
            if to_ in accounts_list_function():
                inc_balance(account=to_, amount=amount)
            l = []
            l.append(transaction_no)
            l.append(bill_no)
            l.append(date)
            l.append(from_)
            l.append(to_)
            l.append(category)
            l.append(subcategory)
            l.append(description)
            l.append(amount)
            f = open('data.csv', 'r')
            content = list(csv.reader(f))
            f.close()
            content.append(l)
            f = open('data.csv', 'w')
            writer = csv.writer(f)
            writer.writerows(content)
            f.close()
        menu()
    except:
        os.system('color C')
        print('making transaction failed!')
        os.system('color A')
        menu()


def accounts_list_function():
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    l = list(content.keys())
    final = []
    for i in l:
        if i == 'login':
            pass
        else:
            final.append(i)
    return final

def category_list_function(return_for):
    f = open('category.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    if return_for[0] == 'category':
        return content.keys()
    elif return_for[0] == 'subcategory':
        l = []
        for i in content.keys():
            if return_for[1] == i:
                l.append(content[i])
        return l

def check_category_function(category, subcategory):
    f = open('category.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    try:
        if subcategory in content[category]:
            return True
        else:
            return False
    except:
        os.system('color C')
        print('error occured while checking category subcategory matching')
        os.system('color A')

def inc_balance(account, amount):
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    content[account]['balance'] = str(int(content[account]['balance']) + int(amount))
    f = open('accounts.bin', 'wb')
    pickle.dump(content, f)
    f.close()


def dec_balance(account, amount):
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    content[account]['balance'] = str(int(content[account]['balance']) - int(amount))
    f = open('accounts.bin', 'wb')
    pickle.dump(content, f)
    f.close()



##########################################################################################################################












##########################################################################################################################
# report menu
def report_menu():
    print('1. date\n2. from/to\n3. category/subcategory\n4. description\n5. tag\n6. hash\n7. amount range\n8. reference no\n99. back')
    choice = input('>>')
    if choice == '1':
        report_date()
    elif choice == '2':
        report_from_to()
    elif choice == '3':
        report_category_subcategory()
    elif choice == '4':
        report_description()
    elif choice == '5':
        report_tag()
    elif choice == '6':
        report_hash()
    elif choice == '7':
        report_amount_range()
    elif choice == '8':
        report_reference_no()
    elif choice == '99':
        menu()
    else:
        print('wrong input...')
        report_menu()

def report_date():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    choice1 = input('enter the starting date[ex : 2021 08 02] : ')
    choice2 = input('enter the ending date[ex : 2021 08 02] : ')
    for i in content:
        try:
            print('starting => ', compare_date(choice1, i[2]))
            print('ending => ', compare_date(choice2, i[2]))
            if compare_date(choice1, i[2]) == '>' and compare_date(choice2, i[2]) == '<':
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t\t')
        print()
    input('')
    menu()

def compare_date(date, i):
    try:
        date = date.split(' ')
        i = i.split(' ')
        if int(date[0]) < int(i[0]):
            return '<'
        elif int(date[0]) >= int(i[0]) and int(date[1]) < int(i[1]):
            return '<'
        elif int(date[0]) >= int(i[0]) and int(date[1]) >= int(i[1]) and int(date[2]) < int(i[2]):
            return '<'
        elif int(date[0]) >= int(i[0]) and int(date[1]) >= int(i[1]) and int(date[2]) > int(i[2]):
            return '>'
    except:
        return False

def report_from_to():
    f = open('data.csv', 'r')
    content = list(csv.reader(f)) 
    f.close()
    final = []
    from_ = input('enter the from account : ')
    to_ = input('enter the to account : ')
    for i in content:
        try:
            if i[3] == from_ or i[4] == to_:
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t')
        print()
    input('')
    menu()

def report_category_subcategory():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    category = input('enter the category : ')
    subcategory = input('enter the subcategory : ')
    for i in content:
        try:
            if i[5] == category or i[6] == subcategory:
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t')
        print()
    input('')
    menu()

def report_description():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    keyword = input('enter the keyword : ')
    for i in content:
        try:
            if keyword in i[7]:
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t')
        print()
    input('')
    menu()

def report_tag():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    keyword = '@' + input('enter the tag : @')
    for i in content:
        try:
            if keyword in i[7]:
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t')
        print()
    input('')
    menu()

def report_hash():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    keyword = '#' + input('enter the tag : #')
    for i in content:
        try:
            if keyword in i[7]:
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t')
        print()
    input('')
    menu()

def report_amount_range():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    low = input('enter the lower range : ')
    high = input('enter the higher range : ')
    for i in content:
        try:
            if int(low) < int(i[-1]) and int(high) > int(i[-1]):
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t\t')
        print()
    input('')
    menu()

def report_reference_no():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    ref = input('enter the reference number : ')
    for i in content:
        try:
            if ref == i[0]:
                final.append(i)
        except:
            pass
    for i in final:
        for j in i:
            print(j, end='\t')
        print()
    input('')
    menu()

##########################################################################################################################












##########################################################################################################################

# manage accounts
def manage_accounts():
    print('1. view balance\n2. add account\n3. read description\n4. update description\n5. update balance manually\n6. delete account\n7. read all content\n99. back')
    choice = input('>>')
    if choice == '1':
        manage_accounts_view_balance()
    elif choice == '2':
        manage_accounts_add_account()
    elif choice == '3':
        manage_accounts_read_description()
    elif choice == '4':
        manage_accounts_update_description()
    elif choice == '5':
        manage_accounts_update_balance()
    elif choice == '6':
        manage_accounts_delete_account()
    elif choice == '7':
        manage_accounts_read_all_content()
    elif choice == '99':
        menu()
    else:
        print('invalid option...')
        manage_accounts()


def manage_accounts_view_balance():
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    for i in content.keys():
        if i != 'login':
            print('\t\t' + str(i) + '\t\t' +  content[i]['balance'])
    menu()

def manage_accounts_add_account():
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    content[input('account name : ')] = {'balance' : input('balance'), 'description' : input('description')}
    f = open('accounts.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    menu()

def manage_accounts_read_description():
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    choice = input('enter the account name : ')
    try:
        print(content[choice]['description'])
        menu()
    except:
        menu()

def manage_accounts_update_description():
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    choice = input('enter the account name : ')
    choice1 = input('enter the new description : ')
    try:
        content[choice]['description'] = choice1
        f = open('accounts.bin', 'wb')
        pickle.dump(content, f)
        f.close()
        menu()
    except:
        menu()

def manage_accounts_update_balance():
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    choice = input('enter the account name : ')
    try:
        content[choice]['balance'] = input('enter the amount : ')
        f = open('accounts.bin', 'wb')
        pickle.dump(content, f)
        f.close()
        menu()
    except:
        menu()

def manage_accounts_delete_account():
    choice = input('enter the account to be deleted : ')
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    final = {}
    for i in content.keys():
        if choice != i:
            final[str(i)] = content[str(i)]
    f = open('accounts.bin', 'wb')
    pickle.dump(final, f)
    f.close()
    menu()


def manage_accounts_read_all_content():
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    for i in content.keys():
        print(str(i), end='\t')
        print(content[i])
    menu()

##########################################################################################################################












##########################################################################################################################
# backup opions
def backup_menu():
    print('1. take backup\n2. restore backup\n99. back')
    choice = input('>>')
    if choice == '1':
        take_backup()
    elif choice == '2':
        restore_backup()
    elif choice == '99':
        menu()
    else:
        print('invalid options...')
        menu()

def take_backup():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    f = open('data_backup.csv', 'w')
    writer_obj = csv.writer(f)
    writer_obj.writerows(content)
    f.close()
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    f = open('account_backup.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    f = open('category.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    f = open('category_backup.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    menu()

def restore_backup():
    f = open('data_backup.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    f = open('data.csv', 'w')
    writer_obj = csv.writer(f)
    writer_obj.writerows(content)
    f.close()
    f = open('account_backup.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    f = open('accounts.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    f = open('category_backup.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    f = open('category.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    menu()

##########################################################################################################################













##########################################################################################################################
# view raw data
def view_raw_data():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    count = 0
    print('trans_no bill no     date       from    to      category        subcategory     description     amount')
    for i in content:
        count += 1
        if count == 1:
            continue
        for j in i:
            print(j, end='\t')
        print()
    menu()

# category_options()
def category_options():
    print('\n\n1. view all available options\n2. add new category\n3. add new subcategory')
    choice = input('>>')
    if choice == '1':
        category_view()
    elif choice == '2':
        category_add_category()
    elif choice == '3':
        category_add_subcategory()
    elif choice == '99':
        menu()
    else:
        print('invalid option...')
        category_options()

def category_view():
    f = open('category.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    for i in content.keys():
        print(i)
        for j in content[i]:
            print('\t\t', end='')
            print(j, sep='\t')
    menu()

def category_add_category():
    f = open('category.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    category = input('enter the new category : ')
    subcategory = []
    for i in range(int(input('enter the number of subcateories in {} : '.format(category)))):
        subcategory.append(input('enter the subcategory : '))
    content[category] = subcategory
    f = open('category.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    menu()

def category_add_subcategory():
    f = open('category.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    category = input('enter the new category : ')
    subcategory = []
    for i in range(int(input('enter the number of new subcateories in {} : '.format(category)))):
        subcategory.append(input('enter the subcategory : '))
    content[category] = subcategory
    f = open('category.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    menu()


# change password
def change_password(old1, old2, new):
    f = open('accounts.bin', 'rb')
    content = decry(pickle.load(f)['login']['password'])
    f.close()
    if old1 == old2 and old1 == content:
        print('error changing the password')
    else:
        return False
    f = open('accounts.bin', 'rb')
    content = dict(pickle.load(f))
    f.close()
    content['login']['password'] = encry(new)
    f = open('accounts.bin', 'wb')
    pickle.dump(content, f)
    f.close()
    return True
    menu()

def refresh():
    f = open('data.csv', 'r')
    content = list(csv.reader(f))
    f.close()
    final = []
    for i in content:
        if i == []:
            pass
        else:
            final.append(i)
    f = open('data.csv', 'w')
    writer_obj = csv.writer(f)
    writer_obj.writerows(final)
    f.close()
    menu()







##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################
login(input('enter the password : '))
##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################
################################                  ###########                       ######################################
##########################################################################################################################

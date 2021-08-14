import os
import time
from cryptography.fernet import Fernet
import pickle
import csv




def encry(data):
    key = b'fono5DWEoUUbfZZPoLoMYMcAB4fGklet9Fat1DAbZeo='
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())



f = open('category.bin', 'wb')
content = {
    'personal' : ['education', 'transport', 'medical', 'manditory', 'snacks', 'subscriptions', 'clothing', 'occational purchases', 'monthly', 'others'],
    'income' : ['dad', 'mom', 'others'],
    'lend in' : ['get', 'return'],
    'lend out' : ['give', 'return'],
    'home' : [''],
    'transfer' : [''],
    'others' : ['']
}
pickle.dump(content, f)
f.close()


f = open('data.csv', 'w')
obj = csv.writer(f)
obj.writerows([['transaction no', 'bill no', 'date', 'from', 'to', 'category', 'subcategory', 'description', 'amount'], ['1', '', '14 08 2021', 'cash', 'init', 'others', '', 'init', '10']])
f.close()

f = open('accounts.bin', 'wb')
accounts = {
    'cash' : {'balance' : '0', 'description' : 'this is the amount i have in my wallet'},
    'login' : {'password' : encry(input('enter the password to be set : '))}
}
pickle.dump(accounts, f)
f.close()





'''
path_finder = input('path finder : ')
path = 'file' + path_finder[0] + '\\file' + path_finder[1] + '\\file' + path_finder[2] + '\\file.bin'

def encry(data):
    f = open('key.bin', 'rb')
    key = pickle.load(f)[0]
    f.close()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())


def decry(data):
    f = open('key.bin', 'rb')
    key = pickle.load(f)[0]
    f.close()
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()
'''
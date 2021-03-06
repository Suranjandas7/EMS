#ems access codebase
from core import *

#creates a new inventory object as inv
inv = inventory()

#Various functions that utilize the core functions on the inv object ->
def check_pkey():
	userkey = str(raw_input('Enter your user key: '))
	passkey = str(raw_input('Enter your pass key: '))
	mkey = str(raw_input('Enter mkey: '))
	if inv.check_pkey(userkey, passkey, mkey) == True:
		print 'Userkey : %s \n Passkey : %s \n Condition : Live' % (userkey, passkey)

def keys_addp():
	inv.map_pkey(userkey, pkey)

def adding():
	ID = str(raw_input('Enter the name of the product : ')) 
	pr = raw_input('Enter cost per unit : ' + '\t')
	amt = raw_input('Enter quantity : ' + '\t')
	u = str(raw_input('Enter units : ' + '\t'))
	passkey = str(raw_input('Enter key : ' + '\t'))
	inv.add_item(item(ID, pr, amt, u, passkey, 'EMS'))
	print '\n\n'

def renew():
	ID = str(raw_input('Enter the name of the product : '))
	cp = raw_input('Enter updated cost per unit : ' + '\t')
	qt = raw_input('Enter updated quantity : ' + '\t')
	key = raw_input('Enter key : ' + '\t')
	inv.update(ID, cp, qt, key)
	print '\n\n'

def clear():
	mkey = str(raw_input('Enter mkey : '))
	inv.remove_all(mkey)
	print 'All items removed.' + '\n\n'	

def showcosts():
	key = str(raw_input('Enter key : '))
	inv.only_price(key)
	print '\n\n'

def showquant():
	key = str(raw_input('Enter key : '))
	inv.only_quantity(key)
	print '\n\n'

def Output_Market(key):
	inv.create_html_Market(key)
	print '\n\n'

def showkeys():
	print inv.keys

def keys_create(x, mkey):
	inv.create_key(x, mkey, 'NA')
	print '\n\n'

def check_keymap():
	mkey = str(raw_input('Enter mkey : '))
	#print inv.check_key_map(mkey) #dd
	if inv.check_key_map(mkey) is True:
		print 'All Keys are mapped.'
	#else:
	#	print 'Not all Keys are mapped.'
	#print '\n\n'

def keys_remove():
	key = str(raw_input('Enter key to be removed : '))
	mkey = str(raw_input('Enter mkey : '))
	inv.remove_key(key, mkey)
	print '\n\n'

def showkeys():
	mkey = str(raw_input('Enter mkey : '))
	inv.show_keys(mkey)

def Search():
	skey = str(raw_input('Enter the item name to search for : '))
	key = str(raw_input('Enter key : '))
	inv.search(skey, key)
	print '\n\n'	

def mapkeys(key, ph, email):
	inv.map_keys(key, ph, email)
	print '\n\n'

def showmapkeys():
	mkey = str(raw_input('Enter mkey : '))
	inv.showmapkey(mkey)

def key_details():
	key = str(raw_input('Enter key : '))
	inv.showkeydetails(key)
	print '\n\n'

def add_buy():
	key = str(raw_input('Enter key : '))
	wkey = str(raw_input('Enter target key: '))
	wlabel = str(raw_input('Enter target item : '))
	inv.add_buyer(buyer(key, wkey, wlabel))
	print '\n\n'

def show_buy():
	key = str(raw_input('Enter key : '))
	inv.show_buyerlist(key)
	print '\n\n'

def connect_all():
	inv.establish_connection()
	print '\n\n'

def key_check():
	key = str(raw_input('Enter key : '))
	if inv.key_check(key) is 1:
		print 'Key valid.'
	else:
		print 'Key invalid'

def key_mcheck():
	mkey = str(raw_input('Enter mkey : '))
	if inv.key_mcheck(mkey) is 1:
		print 'Mkey valid.'
	else:
		print 'Mkey invalid'

def int_m(commandkey): #initial function that creates the "mkey"
	keyexists = False
	for key in inv.keys:
		if inv.key_mcheck(key) is 1:
			keyexists = True
	if keyexists is False:
		inv.create_key(666,'000', commandkey)
		mkey = inv.keys
		inv.map_keys(mkey[0], 'MA','')
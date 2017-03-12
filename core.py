#To-Do:IDEA: write the final email sending function into this core and extend it to the client via codebase
#To-Do:IDEA: write analytics function.

#To-Do:Change a lot of output functions to provide output in data.html and use them as email templates later once they are verified.
#		1		[print_items] has become obsolute. Replacing with other function [create_html_Market] that outputs in data.html

#To-Do: Clean up the code a lot.

import random
import string
import os
import base64
import time

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC 

class buyer(object):
	def __init__(self, key, wkey, wlabel):
		self.mykey = key
		self.wantedkey = wkey
		self.wanteditemlabel = wlabel

class item(object):
	def __init__(self, label, amt, qt, unit, key, ID):
		self.label = label
		self.ammount = amt
		self.quantity = qt
		self.unit = unit
		self.key = key
		self.ID = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(3))

class inventory(object):
	def __init__(self):
		self.items = {}
		self.keys = []
		self.mappedkeys = {}
		self.buyers = {}
		self.connections = {} #format is {selleremail maps to (buyeremail + '|' + buyerphone)}
		self.pkeys = {} #hashed passkeys 
		self.enckey = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10)) #hashkey primarykey

	def back_up(self):
		mkey = str(raw_input('Enter mkey: '))

		if self.key_mcheck(mkey) is 1:
			f = open("BACKUP.DAT", "w")
			backupall = ''
			backup_items = self.items
			backup_keys = self.keys
			backup_mappedkeys = self.mappedkeys
			backup_buyers = self.buyers
			backup_connections = self.connections
			backup_pkeys = self.pkeys
			backup_enckey = self.enckey
					
			#backup market items
			for element in backup_items.values():
				k = str(element.label) + '-' + str(element.ammount) + '-' + str(element.quantity) + '-' + str(element.unit) + '-' + str(element.key) + '-' +str(element.ID) + '--'
				backupall = backupall + str(k)

			backupall = backupall + '=SP='

			#backup market keys
			for keys in backup_keys:
				k = str(keys) + '-'
				backupall = backupall + k
			
			backupall = backupall + '=SP='

			#backup market mappedkeys
			for keys in backup_mappedkeys:
				k = keys
				mapped = backup_mappedkeys[k]
				data = str(k) + '-' + str(mapped) + '--'
				backupall = backupall + data

			backupall = backupall + '=SP='
			
			#backup buyers
			for keys in backup_buyers:
				k = keys
				maped = backup_buyers[k]
				data = str(k) + '-' + str(maped) + '--'
				backupall = backupall + data

			backupall = backupall + '=SP='

			#backup connections
			for keys in backup_connections:
				k = keys
				maped = backup_buyers[k]
				data = str(k) + '-' + str(maped) + '--'
				backupall = backupall + data

			backupall = backupall + '=SP='

			#backup pkeys
			for keys in backup_pkeys:
				k = keys
				maped = backup_buyers[k]
				data = str(k) + '-' + str(maped) + '--'
				backupall = backupall + data

			backupall = backupall + '=SP='

			#backup enckey
			backupall = backupall + backup_enckey

			f.write(self.encpt(backupall, mkey, 'NA', 'NA'))
			f.close()
			print 'Backup created as BACKUP.dat\n'
	
	def restore(self):
		#Restore function
		mkey = str(raw_input('Enter mkey of BACKUP: '))
		f = open('BACKUP.DAT', 'rb')

		#function used repetedly later on in this method
		def rqk(maininput):
			output = {}
			listcategory = maininput.split('--')
			for key in listcategory:
				try:
					firstfield = key.split('-')[0]
					secondfield = key.split('-')[1]
					output[firstfield] = secondfield
				except IndexError:
					print 'RESTORED.'
					return output

		#Sorting the decrypted data
		for line in f.readlines():
			backupdata = line
			backupdata = self.decpt(backupdata, mkey, 'NA', 'NA')
			backupdata = backupdata.split('=SP=')
		f.close()

		ITEMS = backupdata[0]
		INDVITEMS = ITEMS.split('--')
		print 'Market items found.'
		for entries in INDVITEMS:
			try:
				a = item(entries.split('-')[0], entries.split('-')[1], entries.split('-')[2], entries.split('-')[3], entries.split('-')[4], entries.split('-')[5])
				self.items[a.ID] = a
			except IndexError:
				print 'RESTORED'

		KEYS = backupdata[1]
		INDVKEYS = KEYS.split('-')
		print 'Market keys found.'
		for keys in INDVKEYS:
			self.keys.append(keys)
		print 'RESTORED.'
		
		mappedkeys = backupdata[2]
		print 'Keymaps found.'
		finaldict = rqk(mappedkeys)
		self.mappedkeys = finaldict
	
		BUYERS = backupdata[3]
		print 'Buyers found.'
		finaldict = rqk(BUYERS)
		self.buyers = finaldict

		CONNECTIONS = backupdata[4]
		print 'Connections found.'
		finaldict = rqk(CONNECTIONS)
		self.connections = finaldict

		PKEYS = backupdata[5]
		print 'Pkey map found.'
		finaldict = rqk(PKEYS)
		self.connections = finaldict
		
		ENCCODE = backupdata[6]
		self.enckey = ENCCODE
		print 'ENCCODE found.'
		print 'RESTORED.'
		
		for keys in self.keys:
			if keys == '':
				self.keys.remove(keys)

	def map_pkey(self, key, pkey, mkey):
		try:
			print self.pkeys[key], 'already has a pkey.'
		except KeyError:
			if self.key_check(key) is 1: 
				self.pkeys[key] = str(self.encpt(pkey, mkey,'NA', 'NA'))
				print 'Passkey added.\n'

	def check_pkey(self, key, pkey, mkey):
		if self.key_check(key) is 1:
			if pkey == str(self.decpt(self.pkeys[key], mkey, 'NA', 'NA')):
				return True

	def encpt(self, body, mkey, mode, modepass):
		try:
			if mode == 0:
				password = self.enckey #the encoding key
			else:
				password = mkey
			
			saltpass = mkey

			kdf = PBKDF2HMAC(
				algorithm = hashes.SHA256(),
				length = 32,
				salt = saltpass,
				iterations=100000,
				backend = default_backend()
				)
			key = base64.urlsafe_b64encode(kdf.derive(password))
		
			f = Fernet(key)	
			message = body 
			token = f.encrypt(message)
			return token
		except InvalidToken:
			print 'Sorry but the token is invalid.'
		
	def decpt(self, body, mkey, mode, modepass):
		try:
			if mode == 0:
				password = self.enckey #the decoding key
			else:
				password = mkey
		
			saltpass = mkey

			kdf = PBKDF2HMAC(
				algorithm = hashes.SHA256(),
				length = 32,
				salt = saltpass,
				iterations=100000,
				backend = default_backend()
			)

			key = base64.urlsafe_b64encode(kdf.derive(password))
			f = Fernet(key)
			token = f.decrypt(body)
			return token
		except InvalidToken:
			print 'Sorry but the token is invalid.'

	def check_key_map(self, mkey):
		mapped = False
		if self.key_mcheck(mkey) is 1:
			for keys in self.keys:
				try:
					print self.mappedkeys[keys] + '\t MAPPED'
					mapped = True
				except KeyError:
					mapped = False
		return mapped

	def key_check(self, key):
		for element in self.keys:
			if key == element: #CHANGED THIS TO enckey
				return 1


	def key_mcheck(self, key):
		for keys in self.keys:
			if keys == key or key == self.enckey:
				try:
					if self.mappedkeys[key] == 'MA|':
						return 1
				except KeyError:
						return 0

	#add a new buyer into the system
	def add_buyer(self, item):
		for key in self.keys:
			if key == item.mykey:
				for targetkey in self.keys:
					if targetkey == item.wantedkey:
						self.buyers[item.mykey] = item

	#shows all the buyers currently waiting with their target keys
	def show_buyerlist(self, key):
		if self.key_check(key) is 1:
			for items in self.buyers.values():
				print str(items.mykey) + ' ' + str(self.mappedkeys[items.mykey]) + ' ' +str(items.wantedkey)

	#creates a new item and adds it to self.items
	def add_item(self, item):
		for keys in self.keys:
			if item.key == keys:
				try:
					if self.mappedkeys[item.key] is self.mappedkeys[item.key]:
						self.items[item.ID] = item
						print 'Item added.'
				except KeyError:
					print 'Userkey not mapped.'

	#updates any item in self.items with new absolute values of amt and qt and checks for the key
	def update(self, ID, amt, qta, key):
		for item in self.items.values():
			if item.label == ID:
				if item.key == key:
					item.ammount = amt
					item.quantity = qta
				else:
					print 'invalid passkey' + '\n'

	#clears all the items
	def remove_all(self, mkey):
		if self.key_mcheck(mkey) is 1:
			self.items = {}

	#outputs html inventory
	def create_html_Market(self, key):
		if self.key_check(key) is 1:
			message1 = ''
			message101 = ''
			message2 = ''
			message3 = ''
			for items in self.items.values():
				if items.quantity == ' ':
					print 'Removed item'
				else:
					desc = '<tr><td>' + str(items.label) + '</td><td>' + str(items.ammount) + '</td><td>' + str(items.quantity) + '</td><td>' + str(items.unit) + '</td><td>' + str(items.key) + '</td></td>'
					message2 = message2 + """
					{desc}""".format(desc = desc)
			f = open('data.html', 'w')
			message1 = """<!DOCTYPE html>
			<html lang = "en">
			<head><meta charset = "utf-8"><meta name = "viewport" content = "width=device-width, initial-scale = 1"><title>Current Market</title></head>
			<link rel = "stylesheet" href = "bootstrap.min.css">
			<body>"""
			message101 = """<div class = container> <h2>Current Market</h2></div><div class = "container"><table class = "table table-striped"><tr><th>Label</th><th>Price per unit</th><th>Quantity available</th><th>Unit</th><th>Key</th></tr>"""
			message3 = """</table></div><div class = "container"><br><p>@2017</p></div>
			</body></html>"""
			final = message1 + message101 + message2 + message3
			f.write(final)
			f.close()
			print 'HTML FILE CREATED.' #change this to later make it return the final message and use that as email body.

	#creates x no. of keys and stores it in the system
	def create_key(self, noofkeys, mkey, int_mcommand):
		if self.key_mcheck(mkey) is 1 or mkey is '000':
			if noofkeys == 666:
				self.keys.append(int_mcommand)
			else:	
				for i in range(0, noofkeys):
					currentkey = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(4))
					self.keys.append(currentkey)
					print '\n' + 'key added : ' + currentkey

	#removes a particular key and all the items attached to it
	def remove_key(self, key, mkey):
		if self.key_mcheck(mkey) is 1:
			self.keys.remove(key)
			self.mappedkeys.pop(key)
			print '\n' + 'Key removed' + '\n\n'
			for items in self.items.values():
				if items.key == key:
					items.label = '[removed]'
				#these are later used in a math function so don't convert them to string
					items.ammount = ' '
					items.quantity = ' '
					items.unit = ' '
					items.id = ' '
					items.unit = ' '	
	#show_keys
	def show_keys(self, mkey):
		if self.key_mcheck(mkey) is 1:
			print self.keys

	#search
	def search(self, searchkey, key):
		if self.key_check(key) is 1:
			for items in self.items.values():
				if items.label == searchkey:
					print 'Item found: ' + '\n' + str(items.label) + '\t' + str(items.ammount) + '\t' + str(items.quantity) + '\t' + str(items.unit) + '\t' + str(items.key)

	#mapkeystoemail
	def map_keys(self, key, phone, email):
		for elements in self.keys:
			if elements == key:
				self.mappedkeys[key] = phone + '|' + email
				print str(key) + ' mapped to ' + str(phone)

	#shows mappedkeys
	def showmapkey(self, mkey):
		if self.key_mcheck(mkey) is 1:
			print self.mappedkeys

	#shows details of a particular key
	def showkeydetails(self, key):
		print 'Keyname : ' + '\t' + str(key)
		print 'Data : ' + '\t' + str(self.mappedkeys[key])
		print 'Items listed under key : '
		for item in self.items.values():
			if item.key == key:
				print str(item.label) + '\t' + str(item.ammount) + '\t' + str(item.quantity) + '\t' + str(item.unit)

	#Establishes connection of all existing buyers in the market
	def establish_connection(self):
		for buyer in self.buyers.values():
			buyerdata = str(self.mappedkeys[buyer.mykey])
			sellerdata = str(self.mappedkeys[buyer.wantedkey])
			buyeremail = buyerdata.split("|")[1]
			buyerphone = buyerdata.split("|")[0]
			selleremail = sellerdata.split("|")[1]
			sellerphone = sellerdata.split("|")[0]
			try:
				self.connections[selleremail] = str(self.connections[selleremail]) + '||' + buyeremail + '|' + buyerphone + '|' + str(buyer.wanteditemlabel)
			except KeyError:
				self.connections[selleremail] = buyeremail + '|' + buyerphone + '|' + str(buyer.wanteditemlabel) + '||' 
		return self.connections
		self.connections = {}
		self.buyers = {}
		#then we call a function which sends emails data back to the client which does the email thing.
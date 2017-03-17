#To-DO:NEXT: Write the show_keys email command [admin level]
#To-Do:NEXT: Write the other templates 
#To-Do:NEXT: write the connect command [user level]
#TO-DO:NEXT: Fix subject bug.
#To-DO:NEXT: Make the html emails look prettier somehow.
#listening script

from core import *
import codebase

import poplib
import email
import email.header
import sched, time

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

orders = []
log = []
e = str(raw_input('Enter the email id :'))
p = str(raw_input('Enter the password : '))

def send_email(user, body):
	fromaddr = e 
	to = user
	body = unicode(body)

	msg = MIMEMultipart('alternative')
	msg['From'] = str(fromaddr)
	msg['To'] = str(to) 
	msg['Subject'] = 'EMS' #not working. Why?

	chunk = MIMEText(body,'html')
	msg.attach(chunk)

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(e, p)
	server.sendmail(e, user, chunk.as_string())
	server.quit()

def check_for_orders(emailid, password):
	#we only check for max 10 orders every refresh
	max_orders = 10

	#log into pop
	pop_conn = poplib.POP3_SSL('pop.gmail.com')
	pop_conn.user(emailid)
	pop_conn.pass_(password)

	#counting number of messages
	msgcount = pop_conn.stat()[0]

	#main loop checking the subjects and adding them to orders list
	for i in range(msgcount, max(0, msgcount - max_orders), -1):
		response, msg_as_list, size = pop_conn.retr(i)
		msg = email.message_from_string('\r\n'.join(msg_as_list))
		if "subject" in msg:
			decheader = email.header.decode_header(msg["subject"])
			subject = decheader[0][0]
			charset = decheader[0][1]
			if charset:
				subject = subject.decode(charset)
			orders.append(subject)
	orders.reverse() #for sequence		
	pop_conn.quit()

def mainloop(emailid, password):
	check_for_orders(emailid, password)

	if orders == []:
		log.append('Searching for orders...')
	else:
		for items in orders:
			#admin command to create key -> crea [x] [MASTERKEY]
			if str(items)[0:4] == 'CREA':
				codebase.keys_create(int(str(items)[5:6]), str(items)[7:len(items)])
				log.append(items)
				print '\tKey(s) created.'
				orders.remove(items)

			#admin command to stop the program -> EXIT [MASTERKEY]
			if str(items)[0:4] == 'EXIT':
				mkey = str(items)[5:len(str(items))]
				if codebase.inv.key_mcheck(mkey) is 1:
					exit()

			#user command to activate a key -> acti [key] [ph|em|pk]
			if str(items)[0:4] == 'acti':
				key = str(items)[5:9]
				otherstuff = str(items)[10:len(str(items))]
				ph = otherstuff.split('|')[0]
				em = otherstuff.split('|')[1]
				pk = otherstuff.split('|')[2]
				for keys in codebase.inv.keys:
					if key == keys:
						for pkeys in codebase.inv.keys:
							try:
								if codebase.inv.mappedkeys[key] == pk:
									print 'Pkey already exists.' #nevergonnahappen
							except KeyError:	
								codebase.inv.map_keys(key, ph, em)
								codebase.inv.map_pkey(key, pk)
								log.append(items)
				orders.remove(items)

			#user command to add item -> add [key] [name|pricepu|quan|units|pkey]
			if str(items)[0:3] == 'add':
				log.append(items)
				key = str(items)[4:8]
				otherstuff = str(items)[9:len(str(items))]
				name = otherstuff.split('|')[0]
				pricepu = otherstuff.split('|')[1]
				quan = otherstuff.split('|')[2]
				units = otherstuff.split('|')[3]
				pkey = otherstuff.split('|')[4]
				for keys in codebase.inv.keys:
					if key == keys:
						for pkeys in codebase.inv.pkeys:
							try:
								if codebase.inv.decpt(codebase.inv.pkeys[key], codebase.inv.enckey, 'NA', 'NA') == pkey:
									codebase.inv.add_item(codebase.item(name, pricepu, quan, units, key, 'NA'))
							except KeyError:
								print '\tOops.'
				orders.remove(items)

			if str(items)[0:4] == 'show':
				key = str(items)[5:9]
				try:
					useremail = codebase.inv.mappedkeys[key].split('|')[1]
					thetext = str(codebase.inv.create_html_Market(key))
					body = MIMEText(thetext, 'html')
					send_email(useremail, body)
					print 'IREmail sent to : ' + str(useremail)
				except KeyError:
					print '\tOops'
				orders.remove(items)

			#user command to update item -> updt [key] [label|pricepu|quan|units|pkey]
			if str(items)[0:4] == 'updt':
				log.append(items)
				key = str(items)[5:9]
				otherstuff = str(items)[10:len(str(items))]
				name = otherstuff.split('|')[0]
				pricepu = otherstuff.split('|')[1]
				quan = otherstuff.split('|')[2]
				units = otherstuff.split('|')[3]
				pkey = otherstuff.split('|')[4]
				for keys in codebase.inv.keys:
					if key == keys:
						for pkeys in codebase.inv.pkeys:
							try:
								if codebase.inv.decpt(codebase.inv.pkeys[key], codebase.inv.enckey, 'NA', 'NA') == pkey:
									codebase.inv.update(name, pricepu, quan, key)
									print 'item updated'
							except KeyError:
								print '\tOops.'
				orders.remove(items)

			if str(items)[0:4] == 'BACK':
				log.append(items)
				key = str(items)[5:len(str(items))]
				if codebase.inv.key_mcheck(key) is 1:
					codebase.inv.back_up(key)
					print 'Backed up'
				orders.remove(items)

			if str(items)[0:3] == 'BAN':
				log.append(items)
				bankey = str(items)[4:8]
				masterkey = str(items)[9:len(str(items))]
				if codebase.inv.key_mcheck(masterkey) is 1:
					codebase.inv.remove_key(bankey, masterkey)
					print 'Removed: ' + str(bankey)
				orders.remove(items)

	s.enter(120,1,mainloop(emailid, password), (sc,)) #change 1 -> 10 or 20

choice = int(raw_input('1 - Start new \n2 - Backup old\nEnter choice : '))
if choice is 1:
	initialMkey = str(raw_input('Set the MASTERKEY: '))
	codebase.int_m(initialMkey)
	print 'Masterkey Created. EMS service online. Receiving Orders'
	log.append('Masterkey Created. EMS service started. Receiving Orders:')
if choice is 2:
	old_key = str(raw_input('Enter mkey of the backup : '))
	codebase.inv.restore(old_key)
else:
	print 'Unrecognized command'

s = sched.scheduler(time.time, time.sleep)
s.enter(120,1,mainloop(e, p), (sc,))
s.run
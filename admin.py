#DONE: Write the acti [key] email command [user level]
#DONE Write add [user level] 
#To-Do:NEXT: Write update [user level] 
#To-do:NEXT: Write remove [user level]
#To-DO:NEXT: Write the general email func
#To-DO:NEXT: Write the show_keys email command [admin level]
#TO-DO:NEXT: Finish the show via email command to include returning an email to user [user level]
#listening script

from core import *
import codebase

import poplib
import email
import email.header
import sched, time

orders = []
log = []
e = str(raw_input('Enter the email id :'))
p = str(raw_input('Enter the password : '))

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
			#admin command to create key -> crea [MASTERKEY]
			if str(items)[0:4] == 'crea':
				codebase.keys_create(int(str(items)[5:6]), str(items)[7:len(items)])
				log.append(items)
				print '\tKey(s) created.'
				orders.remove(items)

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
									codebase.inv.create_html_Market(key) #debug
							except KeyError:
								print '\tOops.'
				orders.remove(items)

	s.enter(120,1,mainloop(emailid, password), (sc,))

initialMkey = str(raw_input('Set the MASTERKEY: '))
codebase.int_m(initialMkey)
print 'Masterkey Created. EMS service online. Receiving Orders'
log.append('Masterkey Created. EMS service started. Receiving Orders:')
s = sched.scheduler(time.time, time.sleep)
s.enter(120,1,mainloop(e, p), (sc,))
s.run
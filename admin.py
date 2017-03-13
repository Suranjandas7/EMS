#DONE: Write the acti [key] email command
#TO-DO:NEXT: Finish the show [key] email command to include returning an email to the issued command
#TO-DO:NEXT: Value error catching
#listening script

from core import *
import codebase

import poplib
import email
import email.header
import sched, time

orders = []

def check_for_orders():
	#username goes here ->
	username = '420dopeshiteveryday@gmail.com'
	#password goes here ->
	password = 'kickasss1'

	#we only check for max 20 orders every 2 minutes
	max_orders = 100

	#log into pop
	pop_conn = poplib.POP3_SSL('pop.gmail.com')
	pop_conn.user(username)
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

def mainloop():
	check_for_orders()

	if orders == []:
		print 'No new orders...'
	else:
		for items in orders:
			#admin command to create key -> crea [MASTERKEY]
			if str(items)[0:4] == 'crea':
				codebase.keys_create(int(str(items)[5:6]), str(items)[7:len(items)])
				orders.remove(items)

			#show commands sends a email with the inventory html file as the body -> show [KEY]
			#MAW
			#if str(items)[0:4] == 'show':
			#	body = codebase.create_html_Market(str(items)[5:len(items)])
				#send email using this body. Use the maping to extract the email id of the key of the user.
			#	print 'Email sent with market inventory to: '
			#	orders.remove(items)

			#activates a key
			if str(items)[0:4] == 'acti':
				key = str(items)[5:9]
				otherstuff = str(items)[10:len(str(items))]
				ph = otherstuff.split('|')[0]
				em = otherstuff.split('|')[1]
				pk = otherstuff.split('|')[2]
				for keys in codebase.inv.keys:
					if key == keys:
						codebase.inv.map_keys(key, ph, em)
						codebase.inv.map_pkey(key, pk)
						print 'Key mapped.'
				orders.remove(items)

	s.enter(120,1,mainloop(), (sc,))

#initial masterkey creation command -> int_m [MASTERKEY]

initialMkey = str(raw_input('Set the MASTERKEY: '))
codebase.int_m(initialMkey)
print 'Masterkey Created. EMS service online. Receiving Orders'

s = sched.scheduler(time.time, time.sleep)
s.enter(120,1,mainloop(), (sc,))
s.run
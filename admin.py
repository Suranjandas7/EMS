#listening script

from core import *
import codebase

import poplib
import email
import email.header

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
		print 'No new order received'
	else:
		for items in orders:
			#initial masterkey creation command -> int_m
			if items == 'int_m':
				codebase.int_m('MASTER')
				codebase.main()

mainloop()
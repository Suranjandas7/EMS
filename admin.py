#TO-DO:IDEA: Write a client always-on app which will receive email incoming and use them to make commands go to the core through codebase

#admin server script

from core import *
import codebase

codebase.main()

def check_for_orders():
	username = ''
	password = ''

	max_orders = 10
	pop_conn = poplib.POP3_SSL('pop.gmail.com')
	pop_conn.user(username)
	pop_conn.pass_(password)

	msgcount = pop_conn.stat()[0]

	for i in range(msgcount, max(0, msgcount - max_orders), -1):
		response, msg_as_list, size = pop_conn.retr(i)
		msg = email.message_from_string('\r\n'.join(msg_as_list))
		if "subject" in msg:
			decheader = email.header.decode_header(msg["subject"])
			subject = decheader[0][0]
			charset = decheader[0][1]
			if charset:
				subject = subject.decode(charset)
			print "msg num" + str(i) + ',' + subject
pop_conn.quit()
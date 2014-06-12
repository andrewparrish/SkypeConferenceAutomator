from flask import Flask, request, render_template, Response, redirect
import subprocess
import Skype4Py
import config
import paramiko
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client[config.dbname]

@app.route('/makecall', methods=["GET", "POST"])
def makecall():

	if config.autoanswer:
		callers = []
		for key in config.accesses.keys():
			if config.accesses[key]['local']:
				callers.append(key)
		receivers = config.accesses.keys()
	else:
		callers = config.accesses.keys()
		receivers = callers

	if request.method == 'POST':
		caller = request.form['caller']
		receiver = request.form['receiver']

		call = {
			'caller' : caller,
			'receiver' : receiver,
			'status' : 'live'
		}

		call = db['calls'].insert(call)

		acc = config.accesses[receiver]
		calleracc = config.accesses[caller]

		if not config.autoanswer:

			filecheck(acc)
			filecheck(calleracc)

			command = "arch -i386 /usr/bin/python2.7 skype/autoanswer.py \'%s\'" % calleracc['skypename']
			executeorder(acc, command)

			command = "arch -i386 /usr/bin/python2.7 skype/makecall.py \'%s\'" % acc['skypename']
			executeorder(calleracc, command)
		else:

			filecheck(calleracc)

			command = "arch -i386 /usr/bin/python2.7 skype/makecall.py \'%s\'" % acc['skypename']
			executeorder(calleracc, command)


		return redirect('/calls')

	return render_template('makecall.html', callers=callers, receivers=receivers)

@app.route('/calls', methods=["GET", "POST"])
def calls():

	calls = db['calls'].find()

	return render_template('calls.html', calls=calls)

@app.route('/endcall/<caller>')
def endcall(caller):

	call = db['calls'].find_one({'caller' : caller})
	acc = config.accesses[call['receiver']]
	calleracc = config.accesses[call['caller']]

	command = "arch -i386 /usr/bin/python2.7 skype/endcall.py \'%s\'" % acc['skypename']
	executeorder(calleracc, command)

	if not config.autoanswer:
		command = "killall Python"
		executeorder(acc, command)

	db['calls'].remove({'caller': caller})
	return redirect('/calls')

@app.route('/holdcall/<caller>')
def holdcall(caller):

	call = db['calls'].find_one({'caller' : caller})
	acc = config.accesses[call['receiver']]
	calleracc = config.accesses[call['caller']]

	caller = call['caller']
	receiver = call['receiver']

	command = "arch -i386 /usr/bin/python2.7 skype/holdcall.py \'%s\'" % acc['skypename']
	executeorder(calleracc, command)

	if call['status'] == 'live':
		call = {
			'caller' : caller,
			'receiver' : receiver,
			'status' : 'hold'
		}
		db['calls'].remove({'caller': caller})
		db['calls'].insert(call)
	else:
		call = {
			'caller' : caller,
			'receiver' : receiver,
			'status' : 'live'
		}
		db['calls'].remove({'caller': caller})
		db['calls'].insert(call)
	return redirect('/calls')



def executeorder(acc, command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(acc['ip'], username=acc['username'], password=acc['password'])
	stdin, stdout, stderr = ssh.exec_command(command)
	ssh.close()

def filecheck(acc):
	transport = paramiko.Transport(acc['ip'])
	transport.connect(username=acc['username'], password=acc['password'])
	sftp = paramiko.SFTPClient.from_transport(transport)
	try:
		sftp.chdir('skype')
	except IOError:
		sftp.mkdir('skype')
		sftp.chdir('skype')
		sftp.put('autoanswer.py', 'autoanswer.py')
		sftp.put('makecall.py', 'makecall.py')
		sftp.put('endcall.py', 'endcall.py')
		sftp.put('holdcall.py', 'holdcall.py')
	sftp.close
	

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
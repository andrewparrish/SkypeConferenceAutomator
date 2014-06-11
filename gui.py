from flask import Flask, request, render_template, Response, redirect
import subprocess
import Skype4Py
import config
import paramiko

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def homepage():
	#proc = subprocess.call(['arch', '-i386', "python", "makecall.py"])

	contacts = config.accesses.keys()

	if request.method == 'POST':
		caller = request.form['caller']
		reciever = request.form['reciever']

		if not config.autoanswer:

			acc = config.accesses[reciever]
			calleracc = config.accesses[caller]

			filecheck(acc)
			filecheck(calleracc)

			command = "arch -i386 /usr/bin/python2.7 skype/autoanswer.py \'%s\'" % calleracc['skypename']
			executeorder(acc, command)

			command = "arch -i386 /usr/bin/python2.7 skype/makecall.py \'%s\'" % acc['skypename']
			executeorder(calleracc, command)

		

		return redirect('/endcall')

	return render_template('homepage.html', contacts=contacts)

@app.route('/endcall', methods=["GET", "POST"])
def endcall():

	contacts = config.accesses.keys()

	if request.method == 'POST':
		caller = request.form['caller']
		reciever = request.form['reciever']
		acc = config.accesses[reciever]
		calleracc = config.accesses[caller]


		command = "arch -i386 /usr/bin/python2.7 skype/endcall.py \'%s\'" % acc['skypename']
		executeorder(calleracc, command)

		command = "killall Python"
		executeorder(acc, command)

		return Response("Call Complete")
	return render_template('homepage.html', contacts=contacts)

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
	sftp.close
	

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')
# ABOUT

This is a webapp powered by Flask that uses the Python Package Skype4Py to interact with Skype and allow a user to start/end calls between two Skype clients simply by accessing the Flask webpage. This is useful for companies that may want to make connecting two conference rooms via skype even easier.

# REQUIREMENTS
#####IMPORTANT NOTE
You must be using Python 2.7 and Mac OSX. This should also work for various Linux flavors with some configurations of directories. It will not work with Windows without mass changes. 

#####Packages
1. Flask
2. Skype4Py-Must be installed on all Skype client computers (or only callers if you decide to use autoanswer=False More on that in Installation)
3. pymongo-Needed to keep track of active calls
4. Paramiko-Used for SSH and SFTP actions in python.

# INSTALLATION AND SETUP

1. The first step is to setup the Flask server on your local network. It can then be run simply by using 'python gui.py'. The server by default is set to run on port 5000, but that can be changed in the gui.py file (see [Flask documentation](http://flask.pocoo.org/docs/) for more detail).

2. Next, a decision must be made as to whether or not you will be running in 'autoanswer' mode. The skype client in preferences has a setting where you can choose to autoanswer incomming calls. You may choose to use this on your non-local skype users so that you can avoid having to SSH out of your local network which carries possible security issue. If you set autoanswer=True in config jump to that section, otherwise jump to autoanswer=False section of the instructions. In config.py you must create the "accesses" map that will list the connections for Skype. See the "exampleconfig.py" file for an example.



#####Autoanswer=True

3. For each non-local Skype client go to Skype --> Preferences --> Calls. Under Incomming calls choose "Answer automaticall". Click "Configure" and choose to "Answer automatically with video".

4. For each local PC go to System Preferences --> Sharing and ensure that "Remote Login" is checked.

5. For each local PC make sure to install the Skype4Py package. Suggested easiest install is simply by using "pip install Skype4Py".

#####Autoanswer=False

3. For each non-local computer running skype and a possible receiver you may want to ensure that you can SSH in from whatever will be running the server. Paramiko should handle this, but its not a bad idea to double check. 

4. For each PC running skype go to System Preferences --> Sharing and ensure that "Remote Login" is checked.

5. For each PC running skype make sure to install the Skype4Py package. Suggested easiest install is simply by using "pip install Skype4Py".


#####Some additional Security Setup




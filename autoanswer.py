import Skype4Py
import sys
import time

skype = Skype4Py.Skype()

skype.Attach()

print sys.argv[1]

x = 1
while (x == 1):
	try:
		if (len(skype.ActiveCalls) > 0 and skype.ActiveCalls[0].PartnerHandle == sys.argv[1]):
			skype.ActiveCalls[0].Answer()
			y = 1
			while (y==1):
				if (skype.ActiveCalls[0].Status == 'INPROGRESS'):
					break
			time.sleep(5)
			skype.ActiveCalls[0].StartVideoSend()
			skype.ActiveCalls[0].StartVideoReceive()
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		pass
import Skype4Py
import sys

skype = Skype4Py.Skype()

skype.Attach()

x = 1

skype.PlaceCall(sys.argv[1])
while (x == 1):
	if (len(skype.ActiveCalls) != 0):
		if (skype.ActiveCalls[0].Status == 'INPROGRESS'):
			break

skype.ActiveCalls[0].StartVideoSend()
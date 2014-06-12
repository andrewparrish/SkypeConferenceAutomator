import Skype4Py
import sys

skype = Skype4Py.Skype()

skype.Attach()

if (len(skype.ActiveCalls) > 0):
	if skype.ActiveCalls[0].PartnerHandle == sys.argv[1]:
		if skype.ActiveCalls[0].Status =='ONHOLD' or skype.ActiveCalls[0].Status == 'LOCALHOLD':
			skype.ActiveCalls[0].Resume()
		else:
			skype.ActiveCalls[0].Hold()
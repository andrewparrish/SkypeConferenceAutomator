import Skype4Py
import sys

skype = Skype4Py.Skype()

skype.Attach()

if len(skype.ActiveCalls) > 0:
	if skype.ActiveCalls[0].PartnerHandle == sys.argv[1]:
		skype.ActiveCalls[0].Finish()
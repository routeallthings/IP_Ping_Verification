#!/usr/bin/env python
'''
---AUTHOR---
Name: Matt Cross
Email: routeallthings@gmail.com

---PREREQ---
INSTALL netmiko (pip install netmiko)
INSTALL textfsm (pip install textfsm)

'''
'''Module Imports (Native)'''
import re
import getpass
import os
import unicodedata
import csv

'''Module Imports (Non-Native)'''
try:
	import netmiko
	from netmiko import ConnectHandler
except ImportError:
	netmikoinstallstatus = fullpath = raw_input ('Netmiko module is missing, would you like to automatically install? (Y/N): ')
	if "Y" in netmikoinstallstatus.upper() or "YES" in netmikoinstallstatus.upper():
		os.system('python -m pip install netmiko')
		import netmiko
		from netmiko import ConnectHandler
	else:
		print "You selected an option other than yes. Please be aware that this script requires the use of netmiko. Please install manually and retry"
		sys.exit()
try:
	import textfsm
except ImportError:
	textfsminstallstatus = fullpath = raw_input ('textfsm module is missing, would you like to automatically install? (Y/N): ')
	if "Y" in textfsminstallstatus.upper() or "YES" in textfsminstallstatus.upper():
		os.system('python -m pip install textfsm')
		import textfsm
	else:
		print "You selected an option other than yes. Please be aware that this script requires the use of textfsm. Please install manually and retry"
		sys.exit()
'''Global Variables'''
ipv4_address = re.compile('((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

'''(IOS/XE/NXOS/Comware/Procurve)'''

'''Global Variable Questions'''
print ''
print 'IP ICMP Verification Tool'
print '#########################################################'
print 'The purpose of this tool is to use a CSV import to check '
print 'reachability to all endpoints on a switch.'
print '#########################################################'
print ''
print '----Questions that need answering----'
csvimportq = raw_input ('Please enter the path of the CSV file? (e.g. C:\Python27\Template.csv): ')
if csvimportq == '':
	csvimportq = r'C:\Python27\testtemplate.csv'
sshusernameq = raw_input ('Enter the SSH username for the devices: ')
sshpasswordq = getpass.getpass('Enter the SSH password for the devices: ')
saveresults = raw_input ('Do you want to save the results to a file? (Y/N): ')
if "Y" in saveresults.upper() or "YES" in saveresults.upper():
	savepath = raw_input ('Please enter the path of the file? (e.g. C:\Python27\Results.csv): ')
	if savepath == '':
		savepath = r'C:\Python27\Results.csv'
print '----Starting to run verification test----'
#import CSV
try:
	reader = open(csvimportq,'r')
	verificationcsv = []
	for line in reader:
		if not "Name" in line and not "IP" in line:
			verificationcsv.append(line.strip().split(','))
except:
	print "Error with importing CSV file. Check the path/permissions and try again"
#start of verification
if "Y" in saveresults.upper() or "YES" in saveresults.upper():
	saveresults = "Y"
	saveresultslist = []
for sshdevice in verificationcsv:
	sshdevicename = sshdevice[:1][0]
	sshdeviceip = sshdevice[1:][0]
	sshdevicevendor = sshdevice[2:][0]
	sshdevicetype = sshdevice[3:][0]
	sshdevicetype = sshdevicevendor.lower() + "_" + sshdevicetype.lower()
	#Start Connection
	sshnet_connect = ConnectHandler(device_type=sshdevicetype, ip=sshdeviceip, username=sshusernameq, password=sshpasswordq)
	sshdevicehostname = sshnet_connect.find_prompt()
	sshdevicehostname = sshdevicehostname.strip('#')
	sshdevicehostname = sshdevicehostname.strip('>')
	print 'Successfully connected to ' + sshdevicehostname
	for pinglist in verificationcsv:
		pinglistname = pinglist[:1][0]
		pinglistip = pinglist[1:][0]
		pingcheckarp = "ping " + pinglistip
		pingcheck = "ping " + pinglistip
		sshnet_connect.send_command(pingcheckarp)
		pingresult = sshnet_connect.send_command(pingcheck)
		if "!!!!!" in pingresult:
			print "Success = " + sshdevicename + "->" + pinglistname
			if "Y" in saveresults:
				saveresultslist.append(sshdevicename + ', ' + pinglistname + ', SUCCESS')
		else:
			print "Failure = " + sshdevicename + "->" + pinglistname
			if "Y" in saveresults:
				saveresultslist.append(sshdevicename + ', ' + pinglistname + ', FAILURE')
	sshnet_connect.disconnect()
print '#########################################################'
if "Y" in saveresults:
	print 'Saving Results to File'
	with open(savepath, 'wb') as csvfile:
		fieldnames = ['Source', 'Destination', 'Ping Result']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		saveresultslistsplit = []
		for saveresultsrow in saveresultslist:
			saveresultslistsplit.append(saveresultsrow.strip().split(','))
		saveresultslistsplit = [saveresultslistsplit[i:i+3] for i in range(0,len(saveresultslistsplit),3)]
		for saveresultsplitrow in saveresultslistsplit:
			for saveresultssplitrow2 in saveresultsplitrow:
				saveresultsplitrowsource = saveresultssplitrow2[:1][0]
				saveresultsplitrowdestination = saveresultssplitrow2[1:][0]
				saveresultsplitrowresult = saveresultssplitrow2[2:][0]
				writer.writerow({'Source': saveresultsplitrowsource, 'Destination': saveresultsplitrowdestination, 'Ping Result': saveresultsplitrowresult})
	print '#########################################################'
#cleanup
'''
for name in dir():
	if not name.startswith('_'):
		del globals()[name]
'''
print 'SCRIPT IS COMPLETE'
		
import requests
from xml.dom import minidom

headers = {
	'Host': 'power',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0',
	'Accept': '*/*',
	'Accept-Language': 'en-GB,en;q=0.5',
	'Referer': 'https://power/',
	'Content-type': 'application/x-www-form-urlencoded',
	'Connection': 'keep-alive'
}

def login():
	payload = '<avtrans><sid></sid><action>login</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.topology</path></paths><payload><section structure="login"><parameter id="username" structure="RWtext"><value>admin</value></parameter><parameter id="password" structure="password"><value>avocent</value></parameter></section></payload></avtrans>'
	r = requests.post("https://power/appliance/avtrans", verify=False, data=payload, headers=headers)
	doc = minidom.parseString(r.text)
	sid = doc.getElementsByTagName("sid")[0].firstChild.nodeValue
	return sid

def poweron(sid, n):
	txt = ''
	for i in n:
		txt += '<array id="'+str(i)+'"></array>'
	payload = '<avtrans><sid>'+sid+'</sid><action>on</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.outletTable.Nazca_outlet_table</path><pathvar>1d-c5-f1P0_1</pathvar></paths><payload><section structure="table" id="outlet_details">'+txt+'</section></payload></avtrans>'

	try:
		r = requests.post("https://power/appliance/avtrans", verify=False, data=payload, headers=headers, timeout=1)
	except:
		pass

def poweroff(sid, n):
	txt = ''
	for i in n:
		txt += '<array id="'+str(i)+'"></array>'
	payload = '<avtrans><sid>'+sid+'</sid><action>off</action><agents><src>wmi</src><dest>controller</dest></agents><paths><path>units.powermanagement.pdu_management.pduDevicesDetails.outletTable.Nazca_outlet_table</path><pathvar>1d-c5-f1P0_1</pathvar></paths><payload><section structure="table" id="outlet_details">'+txt+'</section></payload></avtrans>'
	try:
		r = requests.post("https://power/appliance/avtrans", verify=False, data=payload, headers=headers, timeout=1)
	except:
		pass

sid = login()

while True:
	raw_input('on')
	poweron(sid, [2,3,4,5])
	raw_input('off')
	poweroff(sid, [2,3,4,5])
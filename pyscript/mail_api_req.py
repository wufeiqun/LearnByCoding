import requests

def test_req():
	url = 'http://127.0.0.1:5000/mail'
	payload = {'sub': '"Server Alarm"','con': 'This is a text server alarm from rocky!','rec':'wufeiqun@qfpay.com','test': 'Hello,this is from tes
t payload.'}
	r = requests.post(url=url,data=payload)
	print r.text

if __name__ == '__main__':
	test_req()

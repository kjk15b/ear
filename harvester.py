import requests
import json
'''
GET https://api.echotrail.io/v1/insights/{searchTerm}
'''
api_file = open('static/api-key.txt')
api_key = api_file.readlines()
api_key = api_key[0]
api_file.close()
exes = open('static/exes.txt')

for exe in exes.readlines():
    print(exe)
    exe = exe.strip('\n')
    url = 'https://api.echotrail.io/v1/insights/{}'.format(exe)
    headers = {"X-Api-key" : api_key }
    response = requests.get(url, headers=headers)
    payload = response.content
    payload = payload.decode('utf-8')
    print(payload)
    data = json.loads(payload)
    f = open('static/echotrail/{}.json'.format(exe), 'w')
    f.write(json.dumps(data, indent=3))
    f.close()

exes.close()
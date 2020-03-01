#Code taken from: https://disc.gsfc.nasa.gov/information/howto?title=How%20to%20Use%20the%20Web%20Services%20API%20for%20Subsetting%20MERRA-2%20Data
#STEP 1
import sys
import json
import urllib3
import certifi
import requests
from time import sleep
from http.cookiejar import CookieJar
import urllib.request
from urllib.parse import urlencode

#STEP 2
# Create a urllib PoolManager instance to make requests.
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
# Set the URL for the GES DISC subset service endpoint
url = 'https://disc.gsfc.nasa.gov/service/subset/jsonwsp'

#STEP 3
# This method POSTs formatted JSON WSP requests to the GES DISC endpoint URL
# It is created for convenience since this task will be repeated more than once
def get_http_data(request):
    hdrs = {'Content-Type': 'application/json',
            'Accept'      : 'application/json'}
    data = json.dumps(request)
    r = http.request('POST', url, body=data, headers=hdrs)
    response = json.loads(r.data)
    # Check for errors
    if response['type'] == 'jsonwsp/fault' :
        print('API Error: faulty %s request' % response['methodname'])
        sys.exit(1)
    return response

# STEP 4
# Define the parameters for the second subset example
product = 'M2T1NXSLV_5.12.4'
varNames =['TQV', 'TQL', 'TQI']
minlon = -180
maxlon = 180
minlat = -90
maxlat = 90
begTime = '1980-01-01'
endTime = '1980-01-05'
begHour = '00:30'
endHour = '23:30'
doMean = True
interp = 'remapbil'
destGrid = 'cfsr0.5a'

# STEP 5
# Construct JSON WSP request for API method: subset
subset_request = {
    'methodname': 'subset',
    'type': 'jsonwsp/request',
    'version': '1.0',
    'args': {
        'role'  : 'subset',
        'box'   : [minlon, minlat, maxlon, maxlat],
        'extent': [minlon, minlat, maxlon, maxlat],
        'start' : begTime,
        'end'   : endTime,
        'diurnalFrom': begHour,
        'diurnalTo': endHour,
        'diurnalMean': doMean,
        'mapping': interp,
        'grid'  : destGrid,
        'data': [{'datasetId': product,
                  'variable' : varNames[0]
                 },
                 {'datasetId': product,
                  'variable' : varNames[1]
                 },
                 {'datasetId': product,
                  'variable' : varNames[2]
                 }]
    }
}

#STEP 6
# Submit the subset request to the GES DISC Server
response = get_http_data(subset_request)
# Report the JobID and initial status
myJobId = response['result']['jobId']
print('Job ID: '+myJobId)
print('Job status: '+response['result']['Status'])

# STEP 7
# Construct JSON WSP request for API method: GetStatus
status_request = {
    'methodname': 'GetStatus',
    'version': '1.0',
    'type': 'jsonwsp/request',
    'args': {'jobId': myJobId}
}

# Check on the job status after a brief nap
while response['result']['Status'] in ['Accepted', 'Running']:
    sleep(5)
    response = get_http_data(status_request)
    status  = response['result']['Status']
    percent = response['result']['PercentCompleted']
    print ('Job status: %s (%d%c complete)' % (status,percent,'%'))
if response['result']['Status'] == 'Succeeded' :
    print ('Job Finished:  %s' % response['result']['message'])
else :
    print('Job Failed: %s' % response['fault']['code'])
    sys.exit(1)


result = requests.get('https://disc.gsfc.nasa.gov/api/jobs/results/'+myJobId)
try:
    result.raise_for_status()
    urls = result.text.split('\n')
    for i in urls : print('\n%s' % i)
except :
    print('Request returned error code %d' % result.status_code)

# STEP 8B
# Retrieve a plain-text list of results in a single shot using the saved JobID

result = requests.get('https://disc.gsfc.nasa.gov/api/jobs/results/'+myJobId)
try:
    result.raise_for_status()
    urls = result.text.split('\n')
    for i in urls : print('\n%s' % i)
except :
    print('Request returned error code %d' % result.status_code)

#STEP 9
# Sort the results into documents and URLs

docs = []
urls = []
for item in results:
    try:
        if item['start'] and item['end']: urls.append(item)
    except:
        docs.append(item)
# Print out the documentation links, but do not download them
print('\nDocumentation:')
for item in docs: print(item['label'] + ': ' + item['link'])

# ALTERNATIVE STEP 10
# Create a password manager to deal with the 401 response that is returned from
# Earthdata Login

username = "lber562@aucklanduni.ac.nz"
password = "Rojas891"

password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)

# Create a cookie jar for storing cookies. This is used to store and return the session cookie #given to use by the data server
cookie_jar = CookieJar()

# Install all the handlers.
opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(password_manager),
                                     urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)

# Open a request for the data, and download files
print('\nHTTP_services output:')
for item in urls:
    URL = item['link']
    DataRequest = urllib.request.Request(URL)
    DataResponse = urllib.request.urlopen(DataRequest)

    # Print out the result
    DataBody = DataResponse.read()

    # Save file to working directory
    try:
        file_name = item['label']
        file_ = open(file_name, 'wb')
        file_.write(DataBody)
        file_.close()
        print(file_name, "has downloaded")
    except requests.exceptions.HTTPError as e:
        print(e)


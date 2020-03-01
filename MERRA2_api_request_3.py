#Code taken from: https://disc.gsfc.nasa.gov/information/howto?keywords=api&title=How%20to%20Use%20the%20Web%20Services%20API%20for%20Subsetting
import sys
import json
import urllib3
import certifi
import requests
from time import sleep

# Create a urllib PoolManager instance to make requests.
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

# Set the URL for the GES DISC subset service endpoint
url = 'https://disc.gsfc.nasa.gov/service/subset/jsonwsp'

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

# Define the parameters for the data subset
product = 'ML2T_V004'
begTime = '2015-08-01T00:00:00.000Z'
endTime = '2015-08-03T23:59:59.999Z'
minlon = -180.0
maxlon = 180.0
minlat = -30.0
maxlat = 30.0
varNames = ['/HDFEOS/SWATHS/Temperature/Data Fields/Temperature',
            '/HDFEOS/SWATHS/Temperature/Data Fields/TemperaturePrecision',
            '/HDFEOS/SWATHS/Temperature/Data Fields/Quality']
# The dimension slice will be for pressure levels between 1000 and 100 hPa
dimName = '/HDFEOS/SWATHS/Temperature/nLevels'
dimVals = [1,2,3,4,5,6,7,8,9,10,11,12,13]
dimSlice = []
for i in range(len(dimVals)) :
    dimSlice.append({'dimensionId': dimName, 'dimensionValue': dimVals[i]})

# Construct JSON WSP request for API method: subset
subset_request = {
    'methodname': 'subset',
    'type': 'jsonwsp/request',
    'version': '1.0',
    'args': {
        'role'  : 'subset',
        'start' : begTime,
        'end'   : endTime,
        'box'   : [minlon, minlat, maxlon, maxlat],
        'extent': [minlon, minlat, maxlon, maxlat],
        'data'  : [{'datasetId': product,
                    'variable' : varNames[0],
                    'slice'    : dimSlice
                   },
                   {'datasetId': product,
                    'variable' : varNames[1],
                    'slice'    : dimSlice
                   },
                   {'datasetId': product,
                    'variable' : varNames[2]
                   }]
    }
}

# Submit the subset request to the GES DISC Server
response = get_http_data(subset_request)

# Report the JobID and initial status
myJobId = response['result']['jobId']
print('Job ID: '+myJobId)
print('Job status: '+response['result']['Status'])

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

# Construct JSON WSP request for API method: GetResult
batchsize = 20
results_request = {
    'methodname': 'GetResult',
    'version': '1.0',
    'type': 'jsonwsp/request',
    'args': {
        'jobId': myJobId,
        'count': batchsize,
        'startIndex': 0
    }
}

# Retrieve the results in JSON in multiple batches
# Initialize variables, then submit the first GetResults request
# Add the results from this batch to the list and increment the count
results = []
count = 0
response = get_http_data(results_request)
count = count + response['result']['itemsPerPage']
results.extend(response['result']['items'])

# Increment the startIndex and keep asking for more results until we have them all
total = response['result']['totalResults']
while count < total:
    results_request['args']['startIndex'] += batchsize
    response = get_http_data(results_request)
    count = count + response['result']['itemsPerPage']
    results.extend(response['result']['items'])

# Check on the bookkeeping
print('Retrieved %d out of %d expected items' % (len(results), total))

# Retrieve a plain-text list of results in a single shot using the saved JobID
result = requests.get('https://disc.gsfc.nasa.gov/api/jobs/results/' + myJobId)
try:
    result.raise_for_status()
    urls = result.text.split('\n')
    for i in urls: print('\n%s' % i)
except:
    print('Request returned error code %d' % result.status_code)

# Sort the results into documents and URLs
docs = []
urls = []
for item in results :
    try:
        if item['start'] and item['end'] : urls.append(item)
    except:
        docs.append(item)

# Print out the documentation links, but do not download them
print('\nDocumentation:')
for item in docs : print(item['label']+': '+item['link'])

# Use the requests library to submit the HTTP_Services URLs and write out the results.
print('\nHTTP_services output:')
for item in urls :
    URL = item['link']
    result = requests.get(URL)
    try:
        result.raise_for_status()
        outfn = item['label']
        f = open(outfn,'wb')
        f.write(result.content)
        f.close()
        print(outfn)
    except:
        print('Error! Status code is %d for this URL:\n%s' % (result.status.code,URL))
        print('Help for downloading data is at https://disc.gsfc.nasa.gov/data-access')

# Retrieve a plain-text list of results in a single shot using the saved JobID
#result = requests.get('https://disc.gsfc.nasa.gov/api/jobs/results/'+myJobId)
#try:
#    result.raise_for_status()
#   urls = result.text.split('\n')
#   for i in urls : print('\n%s' % i)
#except :
#   print('Request returned error code %d' % result.status_code)
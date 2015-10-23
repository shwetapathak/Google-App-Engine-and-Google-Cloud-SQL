#Code to upload the earthquakes details file to google cloud

#import statements.
import argparse
import httplib2
import os
import sys
import json
import time
import datetime
import io
import hashlib
from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools
from apiclient.http import MediaIoBaseDownload

file_name = raw_input("Enter the name of the file :\n")

_BUCKET_NAME = 'assg1_bucket' 
_API_VERSION = 'v1'

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')

FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/devstorage.full_control',
      'https://www.googleapis.com/auth/devstorage.read_only',
      'https://www.googleapis.com/auth/devstorage.read_write',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))


    #Puts a object into file after encryption and deletes the object from the local PC.
def put(service,file_name):  
  try:
    req = service.objects().insert(
		bucket=_BUCKET_NAME,
		name=file_name,
		media_body = file_name)
    resp = req.execute()
    

  except client.AccessTokenRefreshError:
    print ("Error in the credentials")

def main(argv):
  
  flags = parser.parse_args(argv[1:])
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  http = httplib2.Http()
  http = credentials.authorize(http)

  service = discovery.build('storage', _API_VERSION, http=http)
  options_toselect = {1: put}
  option = input("Enter your option 1. put \n")
  start_time = time.clock()
  #print start_time
  print " \n Uploading in progress."
  options_toselect[option](service,file_name)
  end_time = time.clock()
  print " \n File uploaded " + file_name 
  #print end_time
  total_time = end_time - start_time
  print "\n Total time taken in seconds to upload the file : %f" %total_time


if __name__ == '__main__':
  main(sys.argv)


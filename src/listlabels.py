from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
import os
import sys
import httplib2


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.labels']
SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

def main(gmail_user_id):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    delegated_credentials = credentials.create_delegated(gmail_user_id)
    http_auth = delegated_credentials.authorize(httplib2.Http())

    gmailclient = googleapiclient.discovery.build('gmail', 'v1', http=http_auth)

    # Call the Gmail API
    results = gmailclient.users().labels().list(userId=gmail_user_id).execute()

    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])



if __name__ == '__main__':
    main(sys.argv[1])



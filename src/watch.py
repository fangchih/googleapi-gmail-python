from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
import os
import sys
import time
import json
import httplib2
from google.cloud import pubsub_v1


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.labels']
SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']


def main(project_id, topic, sub, gmail_user_id):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    delegated_credentials = credentials.create_delegated(gmail_user_id)
    http_auth = delegated_credentials.authorize(httplib2.Http())

    topic_name = f'projects/{project_id}/topics/{topic}'
    subscription_name = f'projects/{project_id}/subscriptions/{sub}'

    gmailclient = googleapiclient.discovery.build('gmail', 'v1', http=http_auth)

    request = {
        'topicName': topic_name
    }
    watch_rsp = gmailclient.users().watch(userId=gmail_user_id, body=request).execute()
    print(watch_rsp, flush=True)
    time.sleep(0.1)

    subscriber = pubsub_v1.SubscriberClient()

    def callback(message):
        m = json.loads(message.data)
        print(m, flush=True)
        historyId = m["historyId"]
        print(historyId, flush=True)
        history_rsp = gmailclient.users().history().list(userId=gmail_user_id, startHistoryId=historyId, maxResults=1).execute()
        print(history_rsp, flush=True)
        if history_rsp["history"] :
            print(history_rsp["history"], flush=True)
        
        message.ack()
        time.sleep(0.1)

    print("watching ...", flush=True)
    time.sleep(0.1)
    future = subscriber.subscribe(subscription_name, callback)

    with subscriber:
        try:
            future.result()
        except KeyboardInterrupt:
            future.cancel()



if __name__ == "__main__":
    main("gsmme-andersen", "gmailpushnotification", "gmailpushnotification", sys.argv[1])



from oauth2client.service_account import ServiceAccountCredentials
import googleapiclient.discovery
import os
import httplib2
from google.cloud import pubsub_v1


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.labels']
SERVICE_ACCOUNT_FILE = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
USER_ID = "andersen@demo.hkmci.com"


def main(project_id, topic, sub):

    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)
    delegated_credentials = credentials.create_delegated(USER_ID)
    http_auth = delegated_credentials.authorize(httplib2.Http())

    topic_name = f'projects/{project_id}/topics/{topic}'
    subscription_name = f'projects/{project_id}/subscriptions/{sub}'

    gmailclient = googleapiclient.discovery.build('gmail', 'v1', http=http_auth)

    request = {
        'topicName': topic_name
    }
    watch_rsp = gmail.users().watch(userId=USER_ID, body=request).execute()
    print(watch_rsp)

    subscriber = pubsub_v1.SubscriberClient()
    subscriber.create_subscription(name=subscription_name, topic=topic_name)

    def callback(message):
        print(message.data)
        message.ack()

    future = subscriber.subscribe(subscription_name, callback)

    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()

if __name__ == "__main__":
    main("gsmme-andersen", "gmailpushnotification", "gmailpushnotification")



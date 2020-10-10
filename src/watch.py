
import os
from google.cloud import pubsub_v1

def main(project_id, topic, sub):
  subscriber = pubsub_v1.SubscriberClient()
  topic_name = f'projects/{project_id}/topics/{topic}'
  subscription_name = f'projects/{project_id}/subscriptions/{sub}'

  subscriber.create_subscription(
      name=subscription_name, topic=topic_name)

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


  https://developers.google.com/gmail/api/guides/push#python
FROM google/cloud-sdk:slim

RUN pip3 install --upgrade pip
RUN pip3 install google-cloud-pubsub==2.0.0
RUN pip3 install google-api-python-client
RUN pip3 install google-auth-httplib2
RUN pip3 install google-auth
RUN pip3 install oauth2client

ENV GOOGLE_APPLICATION_CREDENTIALS=/key/credentials.json

#!/bin/bash

source ~/.init-gcp
export YOUR_QUARANTINE_BUCKET=dlp-quarantine-bucket-cust01
export YOUR_SENSITIVE_DATA_BUCKET=dlp-sensitive-data-bucket-cust01
export YOUR_NON_SENSITIVE_DATA_BUCKET=dlp-nonsensitive-data-bucket-cust01

export PUB_SUB_TOPIC=dlp-pub-sub-topic-01
export PUB_SUB_SUBSCRIPTION=dlp-pub-sub-topic-01-sub-01


gsutil mb gs://${YOUR_QUARANTINE_BUCKET}
gsutil mb gs://${YOUR_SENSITIVE_DATA_BUCKET}
gsutil mb gs://${YOUR_NON_SENSITIVE_DATA_BUCKET}


gcloud pubsub topics create ${PUB_SUB_TOPIC}
gcloud pubsub subscriptions create ${PUB_SUB_SUBSCRIPTION} --topic ${PUB_SUB_TOPIC}

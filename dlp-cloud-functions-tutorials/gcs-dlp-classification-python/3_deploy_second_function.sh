#!/bin/bash
source ~/.init-gcp
export YOUR_QUARANTINE_BUCKET=dlp-quarantine-bucket-cust01
export YOUR_SENSITIVE_DATA_BUCKET=dlp-sensitive-data-bucket-cust01
export YOUR_NON_SENSITIVE_DATA_BUCKET=dlp-nonsensitive-data-bucket-cust01

export PUB_SUB_TOPIC=dlp-pub-sub-topic-01
export PUB_SUB_SUBSCRIPTION=dlp-pub-sub-topic-01-sub-01


gcloud functions deploy resolve_DLP --runtime python37 --trigger-topic ${PUB_SUB_TOPIC}

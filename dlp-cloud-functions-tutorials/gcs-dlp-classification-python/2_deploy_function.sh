#!/bin/bash
source ~/.init-gcp
export YOUR_QUARANTINE_BUCKET=dlp-quarantine-bucket-cust01

gcloud functions deploy create_DLP_job --runtime python37 \
    --trigger-resource ${YOUR_QUARANTINE_BUCKET} \
    --trigger-event google.storage.object.finalize


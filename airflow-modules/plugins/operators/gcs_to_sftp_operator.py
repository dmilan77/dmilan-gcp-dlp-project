# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from airflow.models import BaseOperator
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.hooks.ssh_hook import SSHHook
from tempfile import SpooledTemporaryFile
from tempfile import NamedTemporaryFile

from urllib.parse import urlparse
from airflow.utils.decorators import apply_defaults


class GCSToSFTPOperator(BaseOperator):
    """
    This operator enables the transferring of files from a Google gcs to SFTP server.

    :param sftp_conn_id: The sftp connection id. The name or identifier for
        establishing a connection to the SFTP server.
    :type sftp_conn_id: str
    :param sftp_dest: The sftp remote path. This is the specified file path
        for uploading the file to the SFTP server.
    :type sftp_dest: str
    :param google_cloud_storage_conn_id: The gcs connection id. The name or identifier for
        establishing a connection to gcs
    :type google_cloud_storage_conn_id: str
    :param gcs_bucket: The targeted gcs bucket. This is the gcs bucket to where
        the file is uploaded.
    :type gcs_bucket: str
    :param gcs_source: The source gcs key. This is the specified path for
        downloading the file from gcs.
    :type gcs_dest: str
    """

    template_fields = ('gcs_dest', 'sftp_dest_path')

    @apply_defaults
    def __init__(self,
                 gcs_bucket,
                 gcs_dest,
                 sftp_dest_path,
                 sftp_conn_id='ssh_default',
                 google_cloud_storage_conn_id='google_cloud_default',
                 mime_type='application/octet-stream',
                 gzip=False,
                 *args,
                 **kwargs):
        super(GCSToSFTPOperator, self).__init__(*args, **kwargs)
        self.sftp_conn_id = sftp_conn_id
        self.sftp_dest_path = sftp_dest_path
        self.gcs_bucket = gcs_bucket
        self.gcs_dest = gcs_dest
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.mime_type = mime_type
        self.gzip=gzip


    def execute(self, context):
        ssh_hook = SSHHook(ssh_conn_id=self.sftp_conn_id)
        gcs_hook = GoogleCloudStorageHook(self.google_cloud_storage_conn_id)

        sftp_client = ssh_hook.get_conn().open_sftp()

        with NamedTemporaryFile("w") as f:
            filename = f.name
            gcs_hook.download(
                bucket=self.gcs_bucket,
                object=self.gcs_dest,   
                filename=filename
            )
            file_msg = "from {0} to {1}".format(filename, self.sftp_dest_path)
            self.log.info("Starting to transfer file %s", file_msg)
            sftp_client.put(filename, self.sftp_dest_path, confirm=True)

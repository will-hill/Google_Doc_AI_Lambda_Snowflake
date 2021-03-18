import os
import json
import boto3
import urllib3
import base64
import threading
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

engine = create_engine(URL(user=os.environ['sf_user'],
                           password=os.environ['sf_password'],
                           account=os.environ['sf_account'],
                           warehouse=os.environ['sf_warehouse'],
                           database=os.environ['sf_db'],
                           schema='PUBLIC',
                           role='accountadmin'))


def doc_thread(data, bearer_token):
    ########################################################
    # API CALL
    r = urllib3.PoolManager().request('POST',
                                      os.environ['dai_uri'],
                                      headers={"Authorization": "Bearer " + bearer_token,"Content-Type": "application/json"},
                                      body=json.dumps(data))

    form_data = json.loads(r.data)['document']['entities']

    ########################################################
    # OBVIATE
    for e in form_data:
        for key in ['textAnchor', 'pageAnchor', 'confidence']:
            e.pop(key)

    ########################################################
    # SQL - INSERT
    cols = []
    for item in form_data:
        cols.append(item['type'])
    insert_sql = 'INSERT INTO form_1040 (' + ', '.join(cols) + ') VALUES ('

    ints = ['Year', 'SSN']
    flts = ['WagesSalariesTips', 'SocialSecurityBenefits', 'TotalIncome']

    vals = []

    for item in form_data:
        if item['type'] in flts:
            vals.append(item['mentionText'].replace(',', ''))
        elif item['type'] in ints:
            vals.append(item['mentionText'])
        else:
            vals.append("'" + item['mentionText'] + "'")

    insert_sql += ", ".join(vals) + ")"

    ########################################################
    # SNOWFLAKE INSERT

    connection = engine.connect()
    print(connection.execute(insert_sql).fetchall())
    if connection is not None:
        connection.close()



def lambda_handler(event=None, context=None):
    s3 = boto3.client('s3')
    bearer_token = event.get("bearer_token")

    ########################################################
    # LOOP OVER DOCUMENTS in S3 Bucket
    BUCKET_NAME = 'doc-ai-demo'
    threads = []

    for key in s3.list_objects(Bucket=BUCKET_NAME)['Contents']:

        ########################################################
        # DOCUMENT BLOB
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key['Key'])
        pdf_bytes = response['Body'].read()

        ########################################################
        # ENCODE BLOB DATA
        data = {
            "document": {
                "mimeType": "application/pdf",
                "content": base64.b64encode(pdf_bytes).decode()
            }
        }
        t = threading.Thread(target=doc_thread, args=(data,bearer_token,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return 'SUCCESS!!!'

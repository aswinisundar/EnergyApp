# modules
import pandas as pd
import os
from google.cloud import bigquery

# variables
gcp_project = 'my-project-cloud-app'
bq_dataset = 'consumption'

credential_path = "C:\Aswini\Cloud application design and development\EnergyApp\my-project-cloud-app-b2076257f9d0.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

# connections
client = bigquery.Client(project=gcp_project)
dataset_ref = client.dataset(bq_dataset)


# results to dataframe function
def gcp2df(sql):
    query = client.query(sql)
    results = query.result()
    return results.to_dataframe()




query = """
    SELECT Date, Client_ID, sum(Usage),
    FROM `my-project-cloud-app.consumption.Consumption2` where Client_ID=420321 and Date>= '2020-09-01' and Date <= '2020-09-01'
    group by Date, Client_ID 
    LIMIT 2000
    """
print(gcp2df(query))

'''
query_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter('limit', 'INTEGER', 100)
    ]
)
df = client.query(query, job_config=query_config).to_dataframe()
print(df)
'''
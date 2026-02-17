import functions_framework
from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig

dataset = "sales"
table = "orders"

@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data

    bucket = data["bucket"]
    filename = data["name"]

    # Skip folder placeholders
    if filename.endswith("/"):
        print(f"Skipping folder object: {filename}")
        return

    # Process only CSV
    if not filename.lower().endswith(".csv"):
        print(f"Skipping non-CSV file: {filename}")
        return

    print(f"Bucket: {bucket}")
    print(f"File: {filename}")

    load_bq(bucket, filename)

def load_bq(bucket, filename):
    client = bigquery.Client()

    table_ref = client.dataset(dataset).table(table)

    job_config = LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.create_disposition = bigquery.CreateDisposition.CREATE_IF_NEEDED

    uri = f"gs://{bucket}/{filename}"

    try:
        print(f"Loading from {uri} to {client.project}.{dataset}.{table}")
        load_job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
        load_job.result()
        print(f"{load_job.output_rows} rows loaded into {dataset}.{table}.")
    except Exception as e:
        print(f"BigQuery load failed for {uri}: {e}")
        raise

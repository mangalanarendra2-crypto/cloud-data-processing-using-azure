# Cloud Data Processing Using Azure

A simple base project demonstrating a common cloud data pipeline pattern with
**Azure Blob Storage**:

```
Local file --> Upload --> Azure (raw container)
                              |
                              v
                     Download for processing
                              |
                              v
                   Clean / transform with pandas
                              |
                              v
Azure (processed container) <-- Upload
```

## Project structure

```
cloud-data-processing-azure/
├── main.py              # Orchestrates the end-to-end pipeline
├── blob_helper.py        # Wrapper around Azure Blob Storage SDK operations
├── data_processor.py     # The actual data cleaning/transformation logic
├── config.py              # Loads Azure credentials from .env
├── requirements.txt
├── .env.example           # Template for your Azure connection string
└── sample_data/
    └── sample.csv         # Example input file (intentionally messy)
```

## Prerequisites

1. An Azure account with an active subscription.
2. An Azure **Storage Account** (Blob Storage). You can create one for free
   via the Azure Portal: Storage Accounts -> Create.
3. Python 3.9+

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get your Storage Account connection string:
   - Azure Portal -> your Storage Account -> **Access keys** -> copy
     "Connection string".

3. Configure credentials:
   ```bash
   cp .env.example .env
   ```
   Then open `.env` and paste your connection string:
   ```
   AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net
   ```

   You can leave `RAW_CONTAINER_NAME` and `PROCESSED_CONTAINER_NAME` as-is —
   the code will create these containers automatically if they don't exist.

## Run

```bash
python main.py
```

Expected output:

```
=== Cloud Data Processing Using Azure ===

Step 1: Uploading raw data to Azure...
Container 'raw-data' created.
Uploaded 'sample_data/sample.csv' -> container 'raw-data' as 'sample.csv'

Step 2: Downloading raw data from Azure...
Downloaded 'sample.csv' from container 'raw-data' -> 'workspace/downloaded_sample.csv'

Step 3: Processing data...
Processed data written to 'workspace/processed_sample.csv'

Step 4: Uploading processed data to Azure...
Container 'processed-data' created.
Uploaded 'workspace/processed_sample.csv' -> container 'processed-data' as 'processed_sample.csv'

Step 5: Current contents of each container:
  raw-data: ['sample.csv']
  processed-data: ['processed_sample.csv']

Done.
```

## What the "processing" step does

`data_processor.py` performs example cleaning on the CSV:
- Drops fully empty rows
- Strips extra whitespace from text fields
- Fills missing numeric values with the column average
- Adds a derived `percent_of_total` column based on the `amount` column

Replace the body of `process_csv()` with whatever transformation logic your
actual assignment/project requires (e.g. filtering, aggregation, joining
multiple files, JSON processing, image processing, etc.).

## Extending this base project

This base project is intentionally simple so it's easy to build on. Common
next steps:
- **Azure Functions**: move `process_csv` into an Azure Function triggered
  automatically whenever a new blob lands in the raw container (event-driven
  processing instead of manually running `main.py`).
- **Azure Data Factory**: orchestrate more complex, multi-step pipelines
  visually.
- **Azure Databricks / Synapse**: for large-scale / big-data processing.
- **Cosmos DB or SQL Database**: store processed results in a database
  instead of (or in addition to) a blob.

## Notes

- Never commit your real `.env` file — it contains secrets. Only
  `.env.example` should be checked into version control.
- The `workspace/` folder is created automatically when you run `main.py` and
  holds intermediate local files.

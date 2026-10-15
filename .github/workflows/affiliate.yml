
name: Affiliate Automation

on:
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * *'

permissions:
  contents: read
  id-token: write

jobs:
  read-products:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install google-auth requests

      - name: Authenticate Google Cloud
        uses: google-github-actions/auth@v3
        with:
          workload_identity_provider: 'projects/786049254562/locations/global/workloadIdentityPools/github-affiliate-pool/providers/github-provider'
          service_account: 'github-affiliate-bot@n8n-facebook-affiliate.iam.gserviceaccount.com'
          create_credentials_file: true
          export_environment_variables: true

      - name: Read Google Sheets Products
        run: python read_products.py

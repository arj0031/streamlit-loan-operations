# Loan Operations Portal — Streamlit application

Standalone Streamlit migration of the original Loan Operations Portal. This is an independent project and does not include the LoanDesk intake app.

## Included functionality

- Separate back-office layout, branding and colour theme.
- Manual refresh and retry for the applications register.
- Reads application records from MuleSoft only when Refresh records or Try again is selected.
- Supports array, single-record, nested and keyed-map API response formats.
- Masks PAN, Aadhaar and mobile numbers in the register.
- Indian currency formatting, empty states, error handling and illustrative-use disclaimer.

## MuleSoft endpoint

The app uses this default GET endpoint:

`https://loan-application-api-ygnir9.3m1neu-1.ind-w1.in1.cloudhub.io/api/v1/loans`

You can optionally override the URL using Streamlit secrets (`MULESOFT_LIST_URL`) or an environment variable of the same name. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` for local development. Never commit real secrets.

## Run locally

Python 3.12 (64-bit) is recommended.

```bash
python -m venv .venv
# Activate the environment, then:
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Put this project in its own GitHub repository (or deploy this folder as the app root).
2. In Streamlit Community Cloud, choose `app.py` as the main file.
3. Select Python 3.12 in Advanced settings.
4. Deploy. The default CloudHub endpoint is already configured; only add a secret if you need to override it.

## Disclaimer

This is an illustrative, mocked implementation for showcasing MuleSoft API functionality. Records and workflows are for demonstration purposes only and must not be treated as real loan decisions or production records.

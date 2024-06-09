# Google Spreadsheet to XML Exporter

This script exports a Google Spreadsheet to an XML file. It uses the Google Sheets API to retrieve the data and converts it into a structured XML format.

## Features

- Export data from Google Sheets to XML format.
- Support for sub-tables within the spreadsheet.
- Customizable field names and table names.
- Option to use service account or client credentials for authentication.
- Pretty XML rendering.

## Requirements

- Python 3.6 or higher
- Google API Client Library
- OAuth2Client Library
- Google Auth Oauthlib

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-repository/google-sheets-to-xml.git
cd google-sheets-to-xml
```

2. Install the required Python packages:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client
```

## Usage

### Command Line Arguments

- `-s`, `--src`: Source spreadsheet ID (required).
- `-d`, `--dest`: Destination file.
- `--pretty`: Pretty XML render (default: True).
- `--service_account`: Google service account credentials JSON file.
- `--client_credentials`: Client credentials JSON file.
- `--rename`: Add table rename (can be used multiple times).
- `--preset`: Compile time preset.

### Examples

1. **Basic usage**:

```bash
python export_to_xml.py -s your_spreadsheet_id -d output.xml
```

2. **Using service account**:

```bash
python export_to_xml.py -s your_spreadsheet_id -d output.xml --service_account path/to/service_account.json
```

3. **Using client credentials**:

```bash
python export_to_xml.py -s your_spreadsheet_id -d output.xml --client_credentials path/to/client_credentials.json
```

4. **Renaming tables**:

```bash
python export_to_xml.py -s your_spreadsheet_id -d output.xml --rename old_table_name:new_table_name
```

## Authentication

To use this script, you need to authenticate with the Google Sheets API. You can do this using either a service account or client credentials.

### Service Account

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (if you don't have one).
3. Enable the Google Sheets API for your project.
4. Create a service account and download the JSON credentials file.
5. Share your Google Spreadsheet with the service account email.

### Client Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (if you don't have one).
3. Enable the Google Sheets API for your project.
4. Create OAuth 2.0 Client IDs and download the JSON credentials file.
5. When you run the script, it will open a browser window for authentication.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [OAuth2Client](https://github.com/google/oauth2client)
- [Google Auth Oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib)

import json
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd

SCOPE_RW = ['https://www.googleapis.com/auth/spreadsheets']
SCOPE_R = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def create_service(scope):
    """
    Create service to Google Sheets API.

    :param scope: Defined scope of the service, see constants SCOPE_RW and SCOPE_R.
    :return: Created service.
    """
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scope)
    creds = flow.run_local_server(port=0)
    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    return service


def store_df_to_gdrive(service, df, OUTPUT_SPREADSHEET_ID, OUTPUT_RANGE):
    """
    Store Pandas DataFrame to Google Sheets.

    :param service: Sheets API service.
    :param df: DataFrame to store.
    :param OUTPUT_SPREADSHEET_ID: ID of the spreadsheet where you want to store results (must exist already).
    :param OUTPUT_RANGE: Range where to store output, e.g. 'A1:AA200'.
    :return: Nothing.
    """
    response_data = service.spreadsheets().values().update(
        spreadsheetId=OUTPUT_SPREADSHEET_ID,
        valueInputOption='RAW',
        range=OUTPUT_RANGE,
        body=dict(
            majorDimension='ROWS',
            values=df.T.reset_index().T.values.tolist())
    ).execute()
    print('Sheet successfully updated at ID {}'.format(OUTPUT_SPREADSHEET_ID))

def gsheet2df(service, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    """ Converts Google sheet data to a Pandas DataFrame.
    Note: This script assumes that your data contains a header file on the first row!
    Also note that the Google API returns 'none' from empty cells - in order for the code
    below to work, you'll need to make sure your sheet doesn't contain empty cells,
    or update the code to account for such instances.

    :param service: Sheets API service.
    :param SAMPLE_SPREADSHEET_ID String ID of the spreadsheet, e.g. "1234rfg5t3fG".
    :param SAMPLE_RANGE_NAME String range to get from the spreadsheet, e.g. 'A1:AA200'.
    """
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    header = result.get('values', [])[0]   # Assumes first line is header!
    values = result.get('values', [])[1:]  # Everything else is data.
    if not values:
        print('No data found.')
    else:
        all_data = []
        for col_id, col_name in enumerate(header):
            column_data = []
            for row in values:
                column_data.append(row[col_id])
            column_data = [x if x is not None else np.nan for x in column_data]
            ds = pd.Series(data=column_data, name=col_name)
            all_data.append(ds)
        df = pd.concat(all_data, axis=1)
        return df

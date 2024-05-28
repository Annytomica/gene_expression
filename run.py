import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('FUSdelta14_gene_expression_database')

NAMES = SHEET.worksheet("names").get_all_values()
ENSEMBL = SHEET.worksheet("ensembl").get_all_values()
DATA = SHEET.worksheet("expression").get_all_values()
HEADINGS = DATA[0]

fus_index = NAMES.index(['Fus'])
print(fus_index)

gene_data = DATA[fus_index]
print(gene_data)

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('FUSdelta14_gene_expression_database')

NAMES = SHEET.worksheet("expression").col_values(1)
ENSEMBL = SHEET.worksheet("expression").col_values(2)
EXPRESSION = SHEET.worksheet("expression").col_values(5)
DATA = SHEET.worksheet("expression").get_all_values()
HEADINGS = DATA[0]

def name_search():
    user_gene = input('Enter gene name here: ').capitalize()

    if user_gene in NAMES:
        global gene_index
        gene_index = NAMES.index(user_gene)
        # return gene_index
    else:
        print(f"{user_gene} not found in dataset")
#user_ensembl = input('Enter Ensembl ID here: ').upper()

name_search()

gene_data = DATA[gene_index]
expression_data = round(float(EXPRESSION[gene_index]), 2)
print(gene_data)
print(expression_data)

'''
ensembl_index = ENSEMBL.index(user_ensembl)
ensembl_data = DATA[ensembl_index]
print(ensembl_data)
'''

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

def user_search():
    print('''
    Welcome to the gene expression search engine!
    Here you can search expression changes of your gene of interest in the FUSDelta14 model of MND
    You can search using a gene name or Ensembl ID
    To search by gene name enter 1
    To search by Ensembl ID enter 2
    ''')
    search_type = input('Enter 1 or 2 now: \n')
    
    if search_type == '1':
        print('You have chosen to search by gene name\n')
        name_search()
    elif search_type == '2':
        print('You have chosen to search by ensembl ID\n')
        ensembl_search()
    else:
        print('You have entered an invalid value. Please enter 1 or 2')

def name_search():
    user_gene = input('Enter gene name here: ').capitalize()

    if user_gene in NAMES:
        global gene_index
        gene_index = NAMES.index(user_gene)
        # return gene_index
    else:
        print(f"{user_gene} not found in dataset")
#user_ensembl = input('Enter Ensembl ID here: ').upper()

def ensembl_search():
    ensembl_index = ENSEMBL.index(user_ensembl)
    ensembl_data = DATA[ensembl_index]
    print(ensembl_data)

user_search()

gene_data = DATA[gene_index]
expression_data = round(float(EXPRESSION[gene_index]), 2)
print(gene_data)
print(expression_data)



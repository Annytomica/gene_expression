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
PVALUE = SHEET.worksheet("expression").col_values(6)
DATA = SHEET.worksheet("expression").get_all_values()
HEADINGS = DATA[0]

def user_search():
    """ 
    Gets search type choice from user
    """
    while True:
        print('''
        You can search using a gene name or Ensembl ID
        To search by gene name enter 1
        To search by Ensembl ID enter 2
        ''')
        global search_type
        search_type = input('Enter 1 or 2 now: ')

        if validate_user_search(search_type):
            print('Search type valid\n')
            break
    
    return search_type

def validate_user_search(values):
    """
    Uses try method to check validity of search_type input from user
    Raises a ValueError if:
    1. input is not a number ie. cannot be converted to an integer
    2. is not 1 or 2, which are the only numerical choices that are valid
    It does not assume the user will input a single value, which is why iteration is used.
    This is a modification of the try method used in CI Love Sandwiches walkthrough project
    """

    try:
        [int(value) for value in values]
        if not values == '1' or values == '2':
            raise ValueError(
                f"You have entered an invalid value. Please enter 1 or 2.\n"
                )
    except ValueError as e:
        print(f"Invalid data: {e}, please enter a numerical value of 1 or 2.\n")
        return False

    return True

def search_selection():
    """
    Takes validated search type and selects appropriate gene search function 
    """
    if search_type == '1':
        print('You have chosen to search by gene name\n')
        name_search()
    elif search_type == '2':
        print('You have chosen to search by ensembl ID\n')
        ensembl_search()

def name_search():
    """ 
    Takes gene name from user and searches database for gene
    Outputs index for gene if present, or notifies user gene not found in database
    """
    user_gene = input('Enter gene name here: ').capitalize()

    if user_gene in NAMES:
        global gene_index
        gene_index = NAMES.index(user_gene)
        return gene_index
    else:
        print(f"{user_gene} not found in dataset")

def ensembl_search():
    """ 
    Takes ensembl ID from user and searches database for gene
    Outputs index for gene if present, or notifies user gene not found in database
    """
    user_ensembl = input('Enter Ensembl ID here: ').upper()
    ensembl_index = ENSEMBL.index(user_ensembl)
    ensembl_data = DATA[ensembl_index]
    print(ensembl_data)

def gene_expression():
    """ 
    Takes gene index and outputs the expression data, with rounding to 2 decimal places, for the relevant gene
    """
    expression_data = round(float(EXPRESSION[gene_index]), 2)
    gene = NAMES[gene_index]
    pvalue = round(float(PVALUE[gene_index]), 4)
    print(f'The gene {gene} is differentially expressed by {expression_data}% with a significance of {pvalue}')

def main():
    """ 
    Runs all functions for gene expression database search
    """
    user_search()
    search_selection()
    gene_expression()


print("""
    Welcome to the gene expression search engine!
    Here you can search expression changes of your gene of interest in the FUSDelta14 model of MND
    This data is from Devoy et al., Brain, 2017.
    """)
main()

#gene_data = DATA[gene_index]
#
#print(gene_data)
#print(expression_data)



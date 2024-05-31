#setting up API and links to googlesheets
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

#Accessing specific information from database in googlesheet
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
        search_type = input('Enter 1 or 2 now: \n')

        if validate_input(search_type):
            print('Search type valid\n')
            break
    
    return search_type

def validate_input(value):
    """
    Uses try method to check validity of search_type input from user
    Raises a ValueError if:
    1. input is not a number ie. cannot be converted to an integer
    2. is not 1 or 2, which are the only numerical choices that are valid
    This is a modification of the try method used in CI Love Sandwiches walkthrough project
    """

    try:
        [int(value)]
        if value != '1' and value != '2':
            raise ValueError(
                f"You have entered an invalid number: {value}"
                )
    except ValueError as e:
        print(f"Invalid data: {value}. Please enter a numerical value of 1 or 2.")
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
    user_gene = input('Enter gene name here: \n').capitalize()

    if user_gene in NAMES:
        gene_index = NAMES.index(user_gene)
        gene_expression()
    else:
        print(f"{user_gene} not found in dataset")
        not_found()

def ensembl_search():
    """ 
    Takes ensembl ID from user and searches database for gene
    Outputs index for gene if present, or notifies user gene not found in database
    """
    user_ensembl = input('Enter Ensembl ID here: \n').upper()

    if user_ensembl in ENSEMBL:
        gene_index = ENSEMBL.index(user_ensembl)
        gene_expression()
    else:
        print(f"{user_ensembl} not found in dataset")
        not_found()

def gene_expression():
    """ 
    Takes gene index and outputs the expression data and significance value for the relevant gene
    Formats expression data to 2 decimal places and significance to 4 decimal places.
    """
    expression_data = round(float(EXPRESSION[gene_index]), 2)
    gene = NAMES[gene_index]
    pvalue = round(float(PVALUE[gene_index]), 4)
    print(f'\nThe gene {gene} is differentially expressed by {expression_data}%,\n with a significance (p-value) of {pvalue}')
    print(""" 
    Explanation of result:
    1. Expression
    A positive expression % indicates an upregulation of gene expression 
    from normal controls
    A negative expression % indicates a downregulation of gene expression 
    from normal controls
    2. p-value
    This dataset only contains genes with significance (p-value) of 
    0.01 or lower, which is a higher stringency for significance than
    0.05 which is generally regarded as acceptable in this field
    """)

def not_found():
    """ 
    Function to deal with user input (gene name or Ensembl ID) not being found in dataset
    """
    print("""
    Potential reasons why your gene was not found:
    1. Your gene is not significantly disregulated in the FUSDelta14 model.
        - this dataset only contains genes with significance (p-value) of 
        0.01 or lower
    2. Your gene was not identified in the RNAseq analysis
        - low abundance transcripts are not always identified successfully
        - you can check your genes expression level in spinal cord at 
        GeneCards.org
    3. Your gene input had a typo:
        - Please check you input, as not all typo's can be detected by our 
        validation protocols
    4. Your gene is not a mouse gene:
        - This dataset is from mouse, therefore contains mouse genes only.
        - you can check correct mouse gene nomenclature at ensembl.org
    """)

    search_again()

def search_again():
    """ 
    Function to check if user wants to search for another gene or exit search engine
    """
    initiate_search_again()
    process_search_again()

def initiate_search_again():
    """ 
    Function that initiates the request proccessing for searching agiain or exiting search engine
    """
    while True:
        print("Would you like to search for another gene?\n Enter 1 for Yes to continue or 2 for No to exit search engine")

        global try_again
        try_again = input('Please enter 1 for Yes or 2 for No: \n')

        if validate_input(try_again):
            print("Processing request...")
            break

    return try_again

def process_search_again():
    """ 
    Function to process search again/exit request after validation
    """

    if try_again == '1':
        main()
    elif try_again == '2':
        print("Thank you for using the FUSDelta14 gene expression search engine!")
        exit()

def main():
    """ 
    Runs all functions for gene expression database search
    """
    user_search()
    search_selection()
    search_again()


print("""
    Welcome to the gene expression search engine!
    Here you can search expression changes of your gene of interest 
    in the FUSDelta14 model of MND
    This data is from Devoy et al., Brain, 2017.
    """)
main()

#gene_data = DATA[gene_index]
#
#print(gene_data)
#print(expression_data)



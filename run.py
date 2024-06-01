# setting up API and links to googlesheets
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

# Constants that access specific information from database in googlesheets
NAMES = SHEET.worksheet("expression").col_values(1)
ENSEMBL = SHEET.worksheet("expression").col_values(2)
EXPRESSION = SHEET.worksheet("expression").col_values(5)
PVALUE = SHEET.worksheet("expression").col_values(6)


# Gene class as data model
class Gene:
    def __init__(self, name, ensembl_id, expression, pvalue):
        self.name = name
        self.ensembl_id = ensembl_id
        self.expression = expression
        self.pvalue = pvalue

    def gene_expression(self):
        """
        Outputs the expression data and
        significance value for the relevant gene.
        Formats expression data to 2 decimal places and
        significance to 4 decimal places.
        """
        expression_data = round(float(self.expression), 2)
        pvalue = round(float(self.pvalue), 4)

        print(f"""
        Result:
        Gene: {self.name}
        Ensembl ID: {self.ensembl_id}
        Expression: {expression_data} %
        P-value: {pvalue}\n""")
        print(f"""
        Summary:
        The gene {self.name} is differentially expressed by {expression_data}%,
        with a significance (p-value) of {pvalue}""")
        print("""
        Explanation of result:
        The result is a comparison of the FUSDelta14 model, when it is
        showing early symptoms of Motor Neuron Disease (MND),
        compared to healthy controls.

        1. Expression
        - A positive expression % indicates an upregulation of gene expression
        from healthy controls
        - A negative expression % indicates a downregulation of gene expression
        from healthy controls

        2. p-value
        This dataset only contains genes with significance (p-value) of
        0.01 or lower, which is a higher stringency for significance than
        0.05 which is generally regarded as acceptable in this field
        """)


def gene_data():
    """
    Formats data from googlesheets for use as list of Gene objects
    Logic for this function was developed with help from ChatGPT
    """
    genes = []
    for name, ensembl_id, expression, pvalue in zip(NAMES, ENSEMBL,
                                                    EXPRESSION, PVALUE):
        genes.append(Gene(name, ensembl_id, expression, pvalue))

    return genes


def user_search():
    """
    Gets search type choice from user
    Validates user input
    """
    while True:
        print('''
        You can search using a gene name or Ensembl ID
        To search by gene name enter 1
        To search by Ensembl ID enter 2
        ''')

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
    This is a modification of the try method used in CI Love Sandwiches
    walkthrough project
    """
    try:
        [int(value)]
        if value != '1' and value != '2':
            raise ValueError(f"You have entered an invalid number: {value}")

    except ValueError as e:
        print(f"""
        Invalid data: {value}.
        Please enter a numerical value of 1 or 2.""")
        return False

    return True


def search_selection(search_type, genes):
    """
    Takes validated search type and selects appropriate gene search function
    """
    if search_type == '1':
        print('You have chosen to search by gene name\n')
        name_search(genes)

    elif search_type == '2':
        print('You have chosen to search by ensembl ID\n')
        ensembl_search(genes)


def name_search(genes):
    """
    Takes gene name from user and searches database for gene
    Outputs expression data for gene if present,
    or notifies user gene not found in database
    """
    while True:
        user_gene = input('Enter gene name here: \n').capitalize()

        if validate_name(user_gene):
            print("Your gene name is accepted for search\n")

            for gene in genes:
                if gene.name == user_gene:
                    gene.gene_expression()
                    return

            print(f"{user_gene} not found in database")
            not_found()


def validate_name(value):
    """
    Checks if user has input a gene name and not left input empty
    """
    
    if value == "" or value.isspace():
        print(f"No gene name provided: Please enter gene name")
        return False

    return True


def ensembl_search(genes):
    """
    Takes ensembl ID from user and searches database for gene
    Validates user input for correct ensembl ID format
    Outputs index for gene if present,
    or notifies user gene not found in database
    """
    while True:
        print("""
        This is a mouse gene database. Your Ensembl ID must:
        1. Start with 'ENSMUSG'
        2. End with 11 numbers after 'ENSMUSG'
        Example: ENSMUSG00000032047
        """)

        user_ensembl = input('Enter Ensembl ID here: \n').upper()

        if validate_ensembl(user_ensembl):
            print("Your Ensembl ID is valid\n")

            for gene in genes:
                if gene.ensembl_id == user_ensembl:
                    gene.gene_expression()
                    return

            print(f"{user_ensembl} not found in dataset")
            not_found()


def validate_ensembl(value):
    """
    Checks if user input for ensembl ID is correct format by checking:
    1. That is starts with the correct ensembl mouse gene
       nomenclature of ENSMUSG
    2. That it is 18 characters long
    3. That the last 11 characters are numbers
    """
    if value.startswith('ENSMUSG') and len(value) == 18:
        try:
            int_value = value[7:]
            int(int_value)

        except ValueError:
            print(f"Incorrect ID: {value}. Ensembl IDs end with 11 numbers")
            return False

        return True

    else:
        print(f"""
        Incorrect data: {value}.
        Must start with 'ENSMUSG' followed by 11 numbers""")
        return False


def not_found():
    """
    Function to deal with user input (gene name or Ensembl ID)
    not being found in dataset
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
        - please check you input, as not all typo's can be detected by our
        validation protocols
    4. Your gene is not a mouse gene:
        - this dataset is from mouse, therefore contains mouse genes only.
        - you can check correct mouse gene nomenclature at ensembl.org
    """)

    search_again()


def search_again():
    """
    Function to check if user wants to search for another gene
    or exit search engine
    """
    try_again = initiate_search_again()
    process_search_again(try_again)


def initiate_search_again():
    """
    Function that initiates the request processing for searching again
    or exiting search engine
    """
    while True:
        print("""
        Would you like to search for another gene?
        Enter 1 for Yes to continue or 2 for No to exit search engine""")

        try_again = input('Please enter 1 for Yes or 2 for No: \n')

        if validate_input(try_again):
            print("Processing request...")
            break

    return try_again


def process_search_again(try_again):
    """
    Function to process search again/exit request after validation
    """
    if try_again == '1':
        main()
    elif try_again == '2':
        print("""
        Thank you for using the FUSDelta14 gene expression search engine!""")
        exit()


def main():
    """
    Runs all functions for gene expression database search
    """
    genes = gene_data()
    search_type = user_search()
    search_selection(search_type, genes)
    search_again()


print("""
    Welcome to the gene expression search engine!
    Here you can search expression changes of your gene of interest
    in the FUSDelta14 model of MND
    This data is from Devoy et al., Brain, 2017.
    """)
main()

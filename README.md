![header](assets/static/publication_header.png)

This is a command line python application for searching gene expression changes in a motor neuron disease model database.

The database is gene expression data generated from the FUSDelta14 model, published in Devoy et al. Brain, 2017. The full publication can be found [here](https://academic.oup.com/brain/article/140/11/2797/4372144)

The live application can be found [here](https://gene-expression-d9cbf16d3290.herokuapp.com/)
![mock-up](assets/static/mock-up_amiresponsive.png)

# Features

## Existing features

### Introduction and search options
The app loads and presents the user with a brief introduction to the app and explanation of its purpose. 

It then introduces the choices of method to search the database, using either gene name or Ensembl ID. This is followed by the prompt for the user to chose which search method they would like to use.

![intro](assets/static/intro.png)

### Gene search request
The two search methods have different validation steps for user input, before providing the same output if the search is successful.

#### Validation
If the user does not input an appropriate value input validation will provide an error message and request the user try again

![choice-error](assets/static/incorrect_search_choice.png)

#### Gene Name
After intial selection, if valid, the user recieves a confirmation of thier choice and a prompt to enter the gene name.

![enter-gene](assets/static/gene-name_initial-choice.png)

Validation of gene name:
The only validation of gene name is checking if it is in the database. This is because gene names can be a mix of letters and numbers and of variable character length. An improvement of this validation is discussed in future features.

If the name is not found in the database the following message is displayed - explaining why it may not have been be found - along with provision to search again or exit.

![not-in-dataset](assets/static/not-in-dataset-message.png)

#### Ensembl ID
After intial selection, if valid, the user recieves a confirmation of thier choice and a prompt to enter the ensembl ID. This ID has a very specific format and so the criteria for the ID are set out for the user to minimise input error.

![enter-ensembl](assets/static/ensembl_initial-choice.png)

Validation of ensembl ID: As the ID has a very specific format, the validation confirms that the user input:
1. That is starts with the correct ensembl mouse gene
nomenclature of ENSMUSG
2. That it is 18 characters long
3. That the last 11 characters are numbers

If the user input is not validated the following error message is displayed and the user is prompted to input the ID again.

![wrong-ensembl](assets/static/incorrect-ensembl.png)

### Output
If the gene, searched via name or ID, is found in the database the user recieves a tabulated result and summary statement of the result.

![result](assets/static/output-result.png)

Below this, the user is also presented with an explainer, providing information on how to interpret result.

![explainer](assets/static/output-explanation.png)

### Search another gene or exit
After a successful or unsuccessful (but valid) gene search, the user is provided with the opportunity to search for another gene or exit the app. 
If they choose to search again they receive the same menu choice at start of app:
![search-again](assets/static/search-again.png)

If they choose to exit, they recieve a short thank you message

![exit-message](assets/static/exit-message.png)

## Future features
### Multiple gene search
Allow a user to input several gene names/IDs into a single search to save time. This feature requires each entry to be seperated, validated and processed individually before all output brought togther at the end. This also allows the user to make easy comparisons between genes.

### Validation of gene name/ID against all known genes
To extend the accuracy of validating a correct gene name or ensembl ID a worksheet that contains all known mouse genes and associated ID's will be generated and included. This would allow the statement that the gene exists but is not dysregulated in this model to be made which is very useful.

### Expand number of databases to search
Include other motor neuron disease gene expression databases. This allows to user to compare genes between databases and allows user to see if expression changes are consistent across all databases (reliable result) or present in some or one database (less reliable result).

# App design process

## Rationale
Searching for expression changes in genes of interest is difficult for interested readers of the original publication. The original gene expression data is only accessible from a secondary pdf document provided as supplimentary data from the publishing house website OR by downloading the raw expression data from a data repository and carrying out your own analysis. 

To resolve this issue, and make the information more accessible, a console-based app has been developed using python. This app allows the user to simply input a gene name and they will be provided with the relevant gene expression for thier query.

## Goal
 A console based app that:
 - is user friendly and intuitive
 - provides requested data quickly
 - provides the expression data in a format that is easy to understand and interpret
 - provides appropriate error feedback and explanation if users input is not matched in dataset

## Design of information processing flow
A flowchart of the steps in information processing that the app needed to follow was mapped out in Figma.
![flowchart](assets/static/app_flowchart.png)
This flowchart was used to guide the development of functions and processes within the app. As the app was built and changes were made to the flow of the app, the flow chart was adjusted accordingly.

## Development process


# Technologies
- Python - all app functions
- Figma – flowchart development
- Photoshop - Readme image processing
- ChatGPT - troubleshooting of typos and logic problems
- Heroku - app deployment and hosting

# Testing

## General Strategy

## Devices and Browsers

### Web browsers

### Devices

### Testing Summary

## Final Validation
PYTHON - PEP8 validation: The app passed validation with no errors reported from [CI pep8 python linter](https://pep8ci.herokuapp.com/)
![Validation](assets/static/pep8_validation_result.png)

# Bugs
## Fixed
- Gene_expression function print output occurs twice if user has selected to search again on deployed app. FIX: Cause unknown. Was present in first Heroku deployment and dissapeared after update. Logic for calling the function was changed anyway, to protect from similar bug occuring in future.
- Validation of ensembl ID input not working. Does not detect change in length or incorrect format. FIX: Logic error - used ChatGPT to troubleshoot and adjust logic so that validation steps worked correctly.

## Unfixed

- No bugs remaining

# Deployment


# Credits
I would like to acknowledge and thank the following people and resources used in the creation of this site.

## Content
- [Code Institute (CI)](https://github.com/Code-Institute-Solutions) for providing all supporting code for the virtual console used for deployment of app
- [CI Love Sandwiches walkthrough project](https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode):
    - linking API and Google sheets process and code
    - Deployment to Heroku
    - usage of try method - used as starting point for validate_input function
- [Medium](https://aryanirani123.medium.com/read-and-write-data-in-google-sheets-using-python-and-the-google-sheets-api-6e206a242f20) for tutorial on methods of getting specific information from Google sheets
- [W3Schools](https://www.w3schools.com/python/python_try_except.asp) tutorial on usage of try/except for validation functions
- [Digital Ocean](https://www.digitalocean.com/community/tutorials/python-valueerror-exception-handling-examples) for tutorial on ValueError handling
- [ChatGPT](https://chatgpt.com) for typo identification and optimising logic for validation functions (not writing of primary code)
- [Free Code Camp](https://www.freecodecamp.org/news/python-exit-how-to-use-an-exit-function-in-python-to-stop-a-program/) for tutorial on how to use exit() function
- [geeksforgeeks.org](https://www.geeksforgeeks.org/precision-handling-python/) for rounding float to 2 decimal places tutorial

## Media
The original gene expression data used as the dataset for this app is from [Devoy et al, Brain, 2017](https://academic.oup.com/brain/article/140/11/2797/4372144)

## Acknowledgements
- My wife, Megan, for help with testing and general emotional support while I was trying to study and code while also moving country
- My original science colleagues, without thier contributions I would not have produced the dataset this app is based around.

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!
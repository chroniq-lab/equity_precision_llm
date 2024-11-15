import pandas as pd 
import numpy as np
import os as os
import sklearn as sklearn

import matplotlib.pyplot as plt
import seaborn as sns
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import re as re

if os.getlogin()=="JVARGH7":
    path_equity_precision_llm_folder = "C:/Cloud/OneDrive - Emory University/Papers/Global Equity in Diabetes Precision Medicine LLM"
    path_equity_precision_llm_repo =  'C:/code/external/equity_precision_llm'
if os.getlogin()=='aamnasoniwala':
    path_equity_precision_llm_folder = '/aamnasoniwala/Library/CloudStorage/OneDrive-Emory/Global Equity in Diabetes Precision Medicine LLM'
    path_equity_precision_llm_repo = '/Users/aamnasoniwala/code/equity_precision_llm'

excel_path = path_equity_precision_llm_folder + "/llm training/Methods.xlsx"

base_prompt_files = ['p1v4', 'p2v4', 'p3v4']

base_prompts = []

for index, prompt_file in enumerate(base_prompt_files):

    # Read the files as a list and save it to base_prompts
    file_path = path_equity_precision_llm_repo + "/prompts/" + prompt_file + '.txt'


    with open(file_path, "r") as file:
        # print(prompt_file)
        # Create a base_prompts list of the three prompts saved as an index 
        # base_prompts[0]: p1v1.txt
        # base_prompts[1]: p2v1.txt
        # base_prompts[2]: p3v1.txt
        base_prompts.append(file.read()) 



def prompt_generator(PMID, base_prompt_list, excel_path):
    # print(PMID)

    # Step 1: Read the excel sheet
    df = pd.read_excel(excel_path, sheet_name='Training Data')

    # Step 2: Filter the excel sheet for the PMID, and create 3 variables: title, abstract, mesh
    record = df[df['PMID'] == PMID].iloc[0]
    title = record['Title']
    abstract = record['Abstract']
    mesh = record['MeSH']


    # Step 3: Generate the prompt based on the PMID and source_population
    prompt_template = base_prompt_list[2] 

        # For base_prompt_list[2] (i.e. p3vN.txt) 
        # Replace <INSERT TITLE> with the title (title)
        # Replace <INSERT ABSTRACT> with the abstract (abstract)
        # Replace <INSERT MESH TERMS> with the MeSH terms (mesh)

        # Use regular expressions to replace the text in the base prompt with the title, abstract, and MeSH terms
    prompt_new = re.sub(r"<INSERT TITLE>", title, prompt_template)
    prompt_new = re.sub(r"<INSERT ABSTRACT>", abstract, prompt_new)
    if pd.notna(mesh):
        # print("Mesh is not null")
        prompt_new = re.sub(r"<INSERT MESH TERMS>", mesh, prompt_new)
        # Step 4: Return the prompt
    else:
        prompt_new = re.sub(r"<INSERT MESH TERMS>", "", prompt_new)
    
    # Handling exceptions
    prompt_new = re.sub(r"\u03b2", "beta", prompt_new)
    prompt_new = re.sub(r"\u2265", "", prompt_new)
    prompt_new = re.sub(r"\u0131", "i", prompt_new)
    prompt_new = re.sub(r"\u2032", "'", prompt_new)
    prompt_new = re.sub(r"\u03b1", "alpha", prompt_new)
    prompt_new = re.sub(r"â€™", "'", prompt_new)
    prompt_new = re.sub(r"\"", "'", prompt_new)

    return prompt_new


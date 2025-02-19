


def prompt_generator(PMID, base_prompt_list, excel_path, sheet_name = 'Training Data'):
    # print(PMID)

    # Step 1: Read the excel sheet
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # Step 2: Filter the excel sheet for the PMID, and create 3 variables: title, abstract, mesh
    record = df[df['PMID'] == PMID].iloc[0]
    title = record['Title']
    abstract = record['Abstract']
    mesh = record['MeSH']

    title = title.replace("\\", "/")
    


    # Step 3: Generate the prompt based on the PMID and source_population
    prompt_template = base_prompt_list[2] 

        # For base_prompt_list[2] (i.e. p3vN.txt) 
        # Replace <INSERT TITLE> with the title (title)
        # Replace <INSERT ABSTRACT> with the abstract (abstract)
        # Replace <INSERT MESH TERMS> with the MeSH terms (mesh)

        # Use regular expressions to replace the text in the base prompt with the title, abstract, and MeSH terms
    prompt_new = re.sub(r"<INSERT TITLE>", title, prompt_template)
    prompt_new = re.sub(r"<INSERT PMID>", str(PMID), prompt_new)
    if pd.notna(abstract):
        abstract = abstract.replace("\\", "/")
        # print("Mesh is not null")
        prompt_new = re.sub(r"<INSERT ABSTRACT>", abstract, prompt_new)
        # Step 4: Return the prompt
    else:
        prompt_new = re.sub(r"<INSERT ABSTRACT>", "", prompt_new)
    
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


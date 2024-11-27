

def base_prompt_append(base_prompt_files):  
    base_prompts = []
    for index, prompt_file in enumerate(base_prompt_files):
        file_path = path_equity_precision_llm_repo + "/prompts/" + prompt_file + '.txt'

    # Read the files as a list and save it to base_prompts
        with open(file_path, "r") as file:
            # print(prompt_file)
            # Create a base_prompts list of the three prompts saved as an index 
            # base_prompts[0]: p1v1.txt
            # base_prompts[1]: p2v1.txt
            # base_prompts[2]: p3v1.txt
            base_prompts.append(file.read()) 
    return base_prompts





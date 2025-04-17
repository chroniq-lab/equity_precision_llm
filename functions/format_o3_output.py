import pandas as pd
import re

def format_o3_output(json_output):
    try:
        df = pd.read_json(json_output.content.decode('utf-8'), lines=True)
    except ValueError as e:
        raise ValueError("Invalid JSON format") from e

    results = pd.DataFrame()  # Initialize an empty DataFrame

    for i in range(len(df)):
        try:
            markdown_table = df['response'][i]['body']['choices'][0]['message']['content'] # Extracts markdown table
            cleaned_table = re.sub(r'^.*?(?=\| PMID)', '', markdown_table, flags=re.DOTALL) # Identifies and removes everything before 'PMID'
            
            table_data = cleaned_table.split('\n\n')[0]  # Extract the first part after splitting on \n\n  
            out = pd.read_csv(pd.io.common.StringIO(table_data), 
                      sep="|", 
                      skipinitialspace=False, 
                      engine='python', 
                      header=0)
            out.columns = out.columns.str.lower().str.strip().str.replace('**', '')
            results = pd.concat([results, out.iloc[[1]]], ignore_index=True)
        except (KeyError, IndexError, pd.errors.ParserError) as e:
            raise ValueError("Error parsing markdown table") from e
            

        

    # Remove unnamed columns
    results = results.loc[:, ~results.columns.str.contains('^unnamed')]

    # Rename columns
    rename_dict = {
        'precision medicine': 'o3_precision_medicine',
        'diabetes': 'o3_diabetes',
        'primary study': 'o3_primary_study',
        'source population': 'o3_source_population'
    }
    results = results.rename(columns=rename_dict)

    # Ensure 'pmid' column exists before conversion
    if 'pmid' in results.columns:
        results['pmid'] = results['pmid'].astype('int32', errors='ignore')

    # Convert string columns to lowercase
    for col in ['o3_precision_medicine', 'o3_diabetes', 'o3_primary_study', 'o3_source_population']:
        if col in results.columns:
            results[col] = results[col].str.lower().str.strip()

    return results


def format_o3_output_v2(json_saved_output):
    try:
        df = json_saved_output
    except ValueError as e:
        raise ValueError("Invalid JSON format") from e

    results = pd.DataFrame()  # Initialize an empty DataFrame

    for i in range(len(df)):
        try:
            markdown_table = df['response'][i]['body']['choices'][0]['message']['content'] # Extracts markdown table
            cleaned_table = re.sub(r'^.*?(?=\| PMID)', '', markdown_table, flags=re.DOTALL) # Identifies and removes everything before 'PMID'
            
            table_data = cleaned_table.split('\n\n')[0]  # Extract the first part after splitting on \n\n  
            out = pd.read_csv(pd.io.common.StringIO(table_data), 
                      sep="|", 
                      skipinitialspace=False, 
                      engine='python', 
                      header=0)
            out.columns = out.columns.str.lower().str.strip().str.replace('**', '')
            results = pd.concat([results, out.iloc[[1]]], ignore_index=True)
        finally:
            # raise ValueError("Error parsing markdown table") from e
            continue
            

        

    # Remove unnamed columns
    results = results.loc[:, ~results.columns.str.contains('^unnamed')]

    # Rename columns
    rename_dict = {
        'precision medicine': 'o3_precision_medicine',
        'diabetes': 'o3_diabetes',
        'primary study': 'o3_primary_study',
        'source population': 'o3_source_population'
    }
    results = results.rename(columns=rename_dict)

    # Ensure 'pmid' column exists before conversion
    if 'pmid' in results.columns:
        results['pmid'] = results['pmid'].astype('int32', errors='ignore')

    # Convert string columns to lowercase
    for col in ['o3_precision_medicine', 'o3_diabetes', 'o3_primary_study', 'o3_source_population']:
        if col in results.columns:
            results[col] = results[col].str.lower().str.strip()

    return results
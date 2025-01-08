import pandas as pd

def format_gpt_output(json_output):
    # Code for formatting GPT output
    df = pd.read_json(json_output.content.decode('utf-8'), lines=True)

    results = pd.DataFrame()
    for index in range(len(df)):
        markdown_table = df['response'][index]['body']['choices'][0]['message']['content']
        out = pd.read_csv(pd.io.common.StringIO(markdown_table.split('\n\n')[1]), 
                      sep="|", skipinitialspace=False, 
                      skipfooter=0, engine='python',header=0)

        out.columns = out.columns.str.lower().str.strip().str.replace('**', '')
        results = pd.concat([results,out.iloc[[1]]])
    
    results = results.filter(regex=r'^(?!unnamed)')


    # Rename 'precision medicine' as 'precision_medicine'
    results = results.rename(columns={'precision medicine': 'gpt_precision_medicine', 
                                    'diabetes': 'gpt_diabetes', 
                                    'primary study': 'gpt_primary_study', 
                                    'source population': 'gpt_source_population'})
    results['pmid'] = results['pmid'].astype('int32')
    # Convert to lower to match
    results['gpt_precision_medicine'] = results['gpt_precision_medicine'].str.lower().str.strip()
    results['gpt_diabetes'] = results['gpt_diabetes'].str.lower().str.strip()
    results['gpt_primary_study'] = results['gpt_primary_study'].str.lower().str.strip()
    results['gpt_source_population'] = results['gpt_source_population'].str.lower().str.strip()


    return results


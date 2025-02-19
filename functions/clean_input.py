def clean_input(input_path,sheet_name = 'Training Data'):

    input = pd.read_excel(input_path,sheet_name=sheet_name)

    input['pubmed_source_population'] = input['Source Population'].apply(lambda x: ''.join([word[0] for word in x.split()])).str.replace(r'&', '')
    input = input.rename(columns={'Precision Medicine': 'orig_precision_medicine', 
                                    'Diabetes': 'orig_diabetes', 
                                    'Primary Study': 'orig_primary_study', 
                                    'Correct Source Population': 'orig_source_population'})

    # Convert to lower
    input['orig_precision_medicine'] = input['orig_precision_medicine'].str.lower()
    input['orig_diabetes'] = input['orig_diabetes'].str.lower()
    input['orig_primary_study'] = input['orig_primary_study'].str.lower()
    input['orig_source_population'] = input['orig_source_population'].str.lower()
    input['orig_source_population'] = input['orig_source_population'].fillna('unk')


    input.drop(columns=['Source Population'], inplace=True)
    return(input)
# Function for classification comparison
def adjusted_source_population_match(row):
    """
    Adjusted logic for source population matching:
    - If either column is NaN or categorized as "Unknown", classify it as 'Unknown'.
    - Match is True if GPT's classification contains at least one exact category from the original classification.
    """
    orig_population = row['orig_source_population']
    gpt_population = row['gpt_source_population']
    
    orig_set = set(orig_population.split(', '))
    gpt_set = set(gpt_population.split(', '))

    # If GPT predicted 'Unknown', it doesn't match any known category.
    if gpt_population == 'Unknown':
        return orig_population == 'Unknown'  # Only match if both are 'Unknown'

    # Match only if GPT contains at least one exact category from the original classification
    return any(category in orig_set for category in gpt_set)
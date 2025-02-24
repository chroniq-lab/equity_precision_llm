# Standardize source population categories
def standardize_population(value):
    if pd.isna(value) or value.strip().lower() in ["unknown", "not applicable", "n/a", "N/A", "unk", "not specified", "Unknown", "Not Applicable", "Not Specified"]:
        return "Unknown"
    return value.strip()
import pandas as pd

def load_financial_data(file_path):
    """Loads and standardizes raw financial CSV data."""
    df = pd.read_csv(file_path)
    print(f'Successfully loaded data from {file_path}')
    return df

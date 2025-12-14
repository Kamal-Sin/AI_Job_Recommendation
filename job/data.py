import pandas as pd

url = "https://raw.githubusercontent.com/luminati-io/Indeed-dataset-samples/refs/heads/main/indeed-job-listings-information.csv"

try:
    df = pd.read_csv(url)
    df.dropna(subset=['company_name', 'job_title', 'description_text', 'location'], inplace=True)
    df.drop_duplicates(subset=['company_name', 'job_title'], inplace=True)
    if 'is_expired' in df.columns:
        df = df[df['is_expired'] == False]
except Exception as e:
    # Fallback: create empty dataframe with required columns
    print(f"Warning: Could not load job data from URL: {e}")
    df = pd.DataFrame(columns=['company_name', 'job_title', 'description_text', 'location', 'description'])

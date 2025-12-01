import pandas as pd

url = "https://raw.githubusercontent.com/luminati-io/Indeed-dataset-samples/refs/heads/main/indeed-job-listings-information.csv"
df=pd.read_csv(url)

df.dropna(subset=['company_name', 'job_title', 'description_text', 'location'], inplace=True)
df.drop_duplicates(subset=['company_name', 'job_title'], inplace=True)  
df = df[df['is_expired'] == False]

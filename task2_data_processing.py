import pandas as pd
import glob
import os

def clean_trend_data():
    # 1. --- Load the JSON File ---
    # Find the most recent trends JSON file in the data folder
    json_files = glob.glob('data/trends_*.json')
    if not json_files:
        print("Error: No JSON files found in data/ folder. Please run Task 1 first.")
        return
    
    # Sort files to get the newest one if multiple exist
    latest_file = max(json_files, key=os.path.getctime)
    
    df = pd.read_json(latest_file)
    print(f"Loaded {len(df)} stories from {latest_file}")

    # 2. --- Clean the Data ---
    
    # Remove Duplicates: ensures each post_id appears only once
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")
    
    # Missing Values: drop rows where critical fields are NaN
    # subset ensures we only drop if these specific columns are empty
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    
    # Whitespace: strip extra spaces from titles (e.g., "  Title  " -> "Title")
    df['title'] = df['title'].str.strip()
    
    # Data Types: convert score and num_comments to standard integers
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].astype(int)
    
    # Low Quality: Filter out posts with a score less than 5
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    # 3. --- Save as CSV ---
    output_path = 'data/trends_clean.csv'
    df.to_csv(output_path, index=False)
    
    print(f"\nSaved {len(df)} rows to {output_path}")
    
    # Quick Summary: Count stories per category
    print("\nStories per category:")
    summary = df['category'].value_counts()
    print(summary)

if __name__ == "__main__":
    clean_trend_data()

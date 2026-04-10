import pandas as pd
import numpy as np

# --- Task 1: Load and Explore ---
# Load the cleaned dataset
df = pd.read_csv('data/trends_clean.csv')

print(f"Loaded data: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())

# Compute averages for the summary
avg_score = df['score'].mean()
avg_comments = df['num_comments'].mean()

print(f"\nAverage score   : {avg_score:,.0f}")
print(f"Average comments: {avg_comments:,.0f}")

# --- Task 2: Basic Analysis with NumPy ---
# Converting columns to NumPy arrays for calculation
scores = df['score'].values
comments = df['num_comments'].values

print("\n--- NumPy Stats ---")
print(f"Mean score   : {np.mean(scores):,.0f}")
print(f"Median score : {np.median(scores):,.0f}")
print(f"Std deviation: {np.std(scores):,.0f}")
print(f"Max score    : {np.max(scores):,}")
print(f"Min score    : {np.min(scores):,}")

# Finding the category with the most stories
# Note: Using pandas value_counts() is standard, but we index the result
top_category = df['category'].value_counts().idxmax()
category_count = df['category'].value_counts().max()
print(f"\nMost stories in: {top_category} ({category_count} stories)")

# Finding the most commented story
max_comments_idx = np.argmax(comments)
top_story_title = df.iloc[max_comments_idx]['title']
top_story_count = df.iloc[max_comments_idx]['num_comments']
print(f"Most commented story: \"{top_story_title}\" — {top_story_count:,} comments")

# --- Task 3: Add New Columns ---
# Calculate engagement: num_comments / (score + 1)
df['engagement'] = df['num_comments'] / (df['score'] + 1)

# Flag popular stories: True if score > average score
df['is_popular'] = df['score'] > avg_score

# --- Task 4: Save the Result ---
df.to_csv('data/trends_analysed.csv', index=False)
print("\nSaved to data/trends_analysed.csv")

import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Task 1: Setup ---
if not os.path.exists('outputs'):
    os.makedirs('outputs')

df = pd.read_csv('data/trends_analysed.csv')

# --- Task 2: Top 10 Stories by Score ---
top_10 = df.sort_values(by='score', ascending=False).head(10).copy()
# Shorten titles longer than 50 characters
top_10['display_title'] = top_10['title'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)

plt.figure(figsize=(10, 6))
plt.barh(top_10['display_title'], top_10['score'], color='skyblue')
plt.xlabel('Score')
plt.ylabel('Story Title')
plt.title('Top 10 Stories by Score')
plt.gca().invert_yaxis()  # Highest score at the top
plt.tight_layout()
plt.savefig('outputs/chart1_top_stories.png')
plt.close()

# --- Task 3: Stories per Category ---
cat_counts = df['category'].value_counts()
colors = plt.cm.get_cmap('Set3', len(cat_counts))

plt.figure(figsize=(10, 6))
cat_counts.plot(kind='bar', color=[colors(i) for i in range(len(cat_counts))])
plt.xlabel('Category')
plt.ylabel('Number of Stories')
plt.title('Stories per Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/chart2_categories.png')
plt.close()

# --- Task 4: Score vs Comments ---
plt.figure(figsize=(10, 6))
popular = df[df['is_popular'] == True]
not_popular = df[df['is_popular'] == False]

plt.scatter(popular['score'], popular['num_comments'], color='orange', label='Popular', alpha=0.6)
plt.scatter(not_popular['score'], not_popular['num_comments'], color='blue', label='Non-Popular', alpha=0.6)

plt.xlabel('Score')
plt.ylabel('Number of Comments')
plt.title('Score vs Comments (Engagement)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('outputs/chart3_scatter.png')
plt.close()

# --- Bonus: Dashboard ---
fig, axs = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('TrendPulse Dashboard', fontsize=22, fontweight='bold')

# Subplot 1: Top 10
axs[0, 0].barh(top_10['display_title'], top_10['score'], color='skyblue')
axs[0, 0].set_title('Top 10 Stories by Score')
axs[0, 0].invert_yaxis()

# Subplot 2: Categories
cat_counts.plot(kind='bar', ax=axs[0, 1], color=[colors(i) for i in range(len(cat_counts))])
axs[0, 1].set_title('Stories per Category')

# Subplot 3: Scatter Plot
axs[1, 0].scatter(popular['score'], popular['num_comments'], color='orange', alpha=0.5, label='Popular')
axs[1, 0].scatter(not_popular['score'], not_popular['num_comments'], color='blue', alpha=0.5, label='Other')
axs[1, 0].set_title('Score vs Comments')
axs[1, 0].legend()

# Subplot 4: Summary Text
axs[1, 1].axis('off')
summary_text = (f"Analysis Summary\n\n"
                f"Total Stories: {len(df)}\n"
                f"Avg Score: {df['score'].mean():.0f}\n"
                f"Avg Comments: {df['num_comments'].mean():.0f}")
axs[1, 1].text(0.5, 0.5, summary_text, ha='center', va='center', fontsize=16, 
              bbox=dict(facecolor='lightgray', alpha=0.3, boxstyle='round'))

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('outputs/dashboard.png')
plt.close()

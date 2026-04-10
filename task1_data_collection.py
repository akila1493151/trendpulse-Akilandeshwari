import requests
import time
import json
import os
from datetime import datetime

# --- Configuration & Keyword Mapping ---
CATEGORIES = {
    "technology": ["AI", "software", "tech", "code", "computer", "data", "cloud", "API", "GPU", "LLM"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["NFL", "NBA", "FIFA", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "NASA", "genome"],
    "entertainment": ["movie", "film", "music", "Netflix", "game", "book", "show", "award", "streaming"]
}

HEADERS = {"User-Agent": "TrendPulse/1.0"}
BASE_URL = "https://hacker-news.firebaseio.com/v0"
LIMIT_PER_CATEGORY = 25
STORY_ID_LIMIT = 500

def get_category(title):
    """Assigns a category based on keywords found in the title."""
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                return category
    return None

def main():
    all_collected_stories = []
    # Track count per category to stop at 25 each
    counts = {cat: 0 for cat in CATEGORIES}
    
    # 1. Fetch Top Story IDs
    print("Fetching top story IDs...")
    try:
        id_resp = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS)
        id_resp.raise_for_status()
        story_ids = id_resp.json()[:STORY_ID_LIMIT]
    except Exception as e:
        print(f"Critical Error fetching IDs: {e}")
        return

    # 2. Iterate through categories (as per Task 1 requirements)
    for category in CATEGORIES:
        print(f"Processing category: {category}...")
        
        # We iterate through the IDs to find stories matching the current category
        for s_id in story_ids:
            # Stop if we hit 25 for this specific category
            if counts[category] >= LIMIT_PER_CATEGORY:
                break
                
            try:
                # Fetch individual story details
                item_url = f"{BASE_URL}/item/{s_id}.json"
                item_resp = requests.get(item_url, headers=HEADERS)
                item_resp.raise_for_status()
                story = item_resp.json()

                # Basic validation: ensure it's a story and has a title
                if not story or 'title' not in story:
                    continue

                # Check if this story belongs to the current category loop
                assigned_cat = get_category(story['title'])
                
                if assigned_cat == category:
                    # Extract Fields (Task 2)
                    story_entry = {
                        "post_id": story.get("id"),
                        "title": story.get("title"),
                        "category": category,
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "author": story.get("by"),
                        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    all_collected_stories.append(story_entry)
                    counts[category] += 1
                    
            except Exception as e:
                # Task 1: Print message and move on, don't crash
                print(f"Request failed for ID {s_id}: {e}")
                continue

        # Task 1: Wait 2 seconds between each category loop
        print(f"Finished {category}. Cooling down...")
        time.sleep(2)

    # 3. Save to JSON File (Task 3)
    if not os.path.exists('data'):
        os.makedirs('data')

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"
    
    with open(filename, 'w') as f:
        json.dump(all_collected_stories, f, indent=4)

    print("-" * 30)
    print(f"Collected {len(all_collected_stories)} stories. Saved to {filename}")

if __name__ == "__main__":
    main()

import os
import json
import re
import requests
from bs4 import BeautifulSoup

USERNAME = "EchlouchiAli07"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT_PATH = os.path.join("data", "contributions.json")

def fetch_contributions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch contributions: HTTP {response.status_code}")
        
    soup = BeautifulSoup(response.text, "html.parser")
    
    days = []
    # GitHub renders days as <td data-date="..." data-level="..."> or <rect data-date="..." data-level="...">
    # and tooltips as <tool-tip for="... ">X contributions on Month Day, Year</tool-tip>
    
    # Try finding rect or td elements with data-date
    elements = soup.find_all(attrs={"data-date": True})
    
    for el in elements:
        date = el.get("data-date")
        level = int(el.get("data-level", "0"))
        
        # Count extraction: check tool-tip or id or aria-label
        el_id = el.get("id")
        count = 0
        if el_id:
            tooltip = soup.find("tool-tip", attrs={"for": el_id})
            if tooltip:
                text = tooltip.text.strip()
                # e.g., "5 contributions on September 27, 2026" or "No contributions on..."
                match = re.search(r"(\d+)\s+contribution", text)
                if match:
                    count = int(match.group(1))
        
        # Fallback if no tooltip found directly
        if count == 0 and level > 0:
            count = level * 2 # estimate if needed
            
        days.append({
            "date": date,
            "count": count,
            "level": level
        })
        
    # Sort days chronologically
    days.sort(key=lambda x: x["date"])
    
    total_contributions = sum(d["count"] for d in days)
    
    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": "", "count": 0}
    
    for d in days:
        cnt = d["count"]
        if cnt > best_day["count"]:
            best_day = {"date": d["date"], "count": cnt}
            
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak from the end
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            # Allow today to be 0 if yesterday was positive
            if current_streak == 0:
                continue
            break
            
    os.makedirs("data", exist_ok=True)
    
    payload = {
        "username": USERNAME,
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "days": days
    }
    
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        
    print(f"Successfully saved {len(days)} days ({total_contributions} total contributions) to {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_contributions()

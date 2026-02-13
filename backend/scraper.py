from google_play_scraper import search
from database import insert_app
import time

# Countries to scrape
COUNTRIES = ["us", "gb", "in", "de", "fr", "br", "jp", "kr", "au", "ca"]

# Search queries for broader coverage
SEARCH_QUERIES = [
    # General new apps
    "new apps 2025", "new apps 2026", "latest apps", "trending apps",
    "new free apps", "new paid apps", "best new apps",
    
    # Games
    "new games 2025", "new mobile games", "new free games", "indie games 2025",
    "new puzzle games", "new action games", "new racing games", "new rpg games",
    "new casual games", "new strategy games", "new simulation games",
    
    # Productivity & Tools
    "productivity apps 2025", "new utility apps", "new tools apps",
    "note taking app", "calendar app", "task manager app",
    
    # Social & Communication
    "new social media apps", "new messaging apps", "new dating apps",
    
    # Entertainment
    "new streaming apps", "new music apps", "new video apps", "new podcast apps",
    
    # Lifestyle
    "new fitness apps", "new health apps", "meditation app", "workout app",
    "new food delivery apps", "new shopping apps",
    
    # Finance
    "new finance apps", "new banking apps", "crypto wallet app", "budget app",
    
    # Education
    "new education apps", "language learning app", "new coding apps",
    
    # Tech
    "ai apps 2025", "chatgpt apps", "new vpn apps", "password manager app",
    "new photo editor", "new video editor"
]

# All Play Store App Categories (33)
APP_CATEGORIES = [
    "art and design", "auto and vehicles", "beauty", "books and reference",
    "business", "comics", "communication", "dating", "education",
    "entertainment", "events", "finance", "food and drink",
    "health and fitness", "house and home", "libraries and demo",
    "lifestyle", "maps and navigation", "medical", "music and audio",
    "news and magazines", "parenting", "personalization", "photography",
    "productivity", "shopping", "social", "sports", "tools",
    "travel and local", "video players", "weather"
]

# All Play Store Game Categories (17)
GAME_CATEGORIES = [
    "action games", "adventure games", "arcade games", "board games",
    "card games", "casino games", "casual games", "educational games",
    "music games", "puzzle games", "racing games", "role playing games",
    "simulation games", "sports games", "strategy games", "trivia games",
    "word games"
]

# Combined categories
CATEGORIES = APP_CATEGORIES + GAME_CATEGORIES

def scrape_by_search(query: str, limit: int = 100, country: str = "us"):
    """Scrape apps using search query."""
    results = []
    try:
        apps = search(query, n_hits=limit, country=country, lang="en")
        for app_data in apps:
            insert_app(app_data)
            results.append(app_data)
        print(f"  Found {len(apps)} apps for '{query}'")
    except Exception as e:
        print(f"  Error searching '{query}': {e}")
    return results

def scrape_new_apps(country: str = "us", limit: int = 100):
    """Scrape new apps using new-related search terms."""
    results = []
    new_queries = ["new apps 2025", "new apps 2026", "latest apps", "new free apps"]
    for query in new_queries:
        results.extend(scrape_by_search(query, limit=limit, country=country))
        time.sleep(0.5)
    return results

def scrape_all_new_apps(countries: list = None, limit_per: int = 100):
    """Scrape new apps from multiple countries."""
    if countries is None:
        countries = COUNTRIES[:3]
    
    results = []
    for country in countries:
        print(f"Scraping from {country}...")
        results.extend(scrape_new_apps(country=country, limit=limit_per))
        time.sleep(1)
    return results

def scrape_by_category(category: str, country: str = "us", limit: int = 100):
    """Scrape apps by category search term."""
    query = f"new {category} apps"
    return scrape_by_search(query, limit=limit, country=country)

def scrape_all_categories(limit_per_category: int = 100):
    """Scrape apps from all 50 categories (33 app + 17 game)."""
    results = []
    for cat in CATEGORIES:
        print(f"Scraping category: {cat}")
        results.extend(scrape_by_category(cat, limit=limit_per_category))
        time.sleep(0.5)
    return results

def scrape_app_categories(limit_per_category: int = 100):
    """Scrape only app categories (no games)."""
    results = []
    for cat in APP_CATEGORIES:
        print(f"Scraping app category: {cat}")
        results.extend(scrape_by_category(cat, limit=limit_per_category))
        time.sleep(0.5)
    return results

def scrape_game_categories(limit_per_category: int = 100):
    """Scrape only game categories."""
    results = []
    for cat in GAME_CATEGORIES:
        print(f"Scraping game category: {cat}")
        results.extend(scrape_by_category(cat, limit=limit_per_category))
        time.sleep(0.5)
    return results

def scrape_by_queries(queries: list = None, limit: int = 100):
    """Scrape using multiple search queries."""
    if queries is None:
        queries = SEARCH_QUERIES
    
    results = []
    for query in queries:
        print(f"Searching: {query}")
        results.extend(scrape_by_search(query, limit=limit))
        time.sleep(0.5)
    return results

def full_scrape():
    """Run a comprehensive scrape."""
    results = []
    
    print("=== Scraping new apps from multiple countries ===")
    results.extend(scrape_all_new_apps(countries=COUNTRIES[:5], limit_per=100))
    
    print("=== Scraping by categories ===")
    results.extend(scrape_all_categories(limit_per_category=100))
    
    print("=== Scraping by search queries ===")
    results.extend(scrape_by_queries(limit=100))
    
    print(f"=== Done! Total scraped: {len(results)} ===")
    return results

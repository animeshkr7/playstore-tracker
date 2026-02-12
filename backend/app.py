from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_apps_by_month, get_all_months, get_stats
from scraper import (
    scrape_by_search, scrape_new_apps, scrape_all_new_apps,
    scrape_all_categories, scrape_by_queries, full_scrape,
    CATEGORIES, COUNTRIES
)

app = FastAPI(title="PlayStore Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "PlayStore Tracker API"}

@app.get("/apps")
def get_apps(year: int = Query(...), month: int = Query(...)):
    """Get apps discovered in a specific month."""
    apps = get_apps_by_month(year, month)
    return {"year": year, "month": month, "count": len(apps), "apps": apps}

@app.get("/months")
def list_months():
    """Get list of all months with app counts."""
    return get_all_months()

@app.get("/stats")
def get_statistics():
    """Get database statistics."""
    return get_stats()

@app.get("/categories")
def list_categories():
    """List all available categories."""
    return {"categories": CATEGORIES}

@app.get("/countries")
def list_countries():
    """List all available countries."""
    return {"countries": COUNTRIES}

@app.post("/scrape/search")
def trigger_search_scrape(query: str = Query(default="new apps 2025"), limit: int = 50):
    """Scrape by search query."""
    apps = scrape_by_search(query=query, limit=limit)
    return {"scraped": len(apps), "query": query}

@app.post("/scrape/new")
def trigger_new_scrape(country: str = "us", limit: int = 50):
    """Scrape new apps from one country."""
    apps = scrape_new_apps(country=country, limit=limit)
    return {"scraped": len(apps), "country": country}

@app.post("/scrape/new/all")
def trigger_all_new_scrape():
    """Scrape new apps from multiple countries."""
    apps = scrape_all_new_apps(countries=COUNTRIES[:5], limit_per=30)
    return {"scraped": len(apps)}

@app.post("/scrape/categories")
def trigger_category_scrape():
    """Scrape apps from all categories."""
    apps = scrape_all_categories(limit_per_category=30)
    return {"scraped": len(apps)}

@app.post("/scrape/queries")
def trigger_query_scrape():
    """Scrape using predefined search queries."""
    apps = scrape_by_queries(limit=30)
    return {"scraped": len(apps)}

@app.post("/scrape/full")
def trigger_full_scrape():
    """Run comprehensive scrape (takes several minutes)."""
    apps = full_scrape()
    return {"scraped": len(apps)}

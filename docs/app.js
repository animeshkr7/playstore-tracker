// const API_URL = 'http://localhost:8000';
// To (placeholder - will update after Render deploy):
const API_URL = 'https://playstore-tracker.onrender.com';

const monthSelect = document.getElementById('month');
const yearSelect = document.getElementById('year');
const searchBtn = document.getElementById('searchBtn');
const scrapeSelect = document.getElementById('scrapeType');
const scrapeBtn = document.getElementById('scrapeBtn');
const statsDiv = document.getElementById('stats');
const appsDiv = document.getElementById('apps');

// Set current month/year as default
const now = new Date();
monthSelect.value = now.getMonth() + 1;
yearSelect.value = now.getFullYear();

async function fetchApps(year, month) {
    appsDiv.innerHTML = '<div class="loading">Loading...</div>';

    try {
        const res = await fetch(`${API_URL}/apps?year=${year}&month=${month}`);
        const data = await res.json();

        statsDiv.textContent = `Found ${data.count} apps for ${getMonthName(month)} ${year}`;

        if (data.apps.length === 0) {
            appsDiv.innerHTML = '<div class="empty">No apps found for this month. Try scraping some apps first!</div>';
            return;
        }

        appsDiv.innerHTML = data.apps.map(app => `
            <div class="app-card">
                <img src="${app.icon_url || 'https://via.placeholder.com/64'}" alt="${app.title}">
                <h3>${app.title}</h3>
                <div class="developer">${app.developer || 'Unknown'}</div>
                <div class="meta">
                    <span class="category">${app.category || 'N/A'}</span>
                    <span class="score">⭐ ${app.score ? app.score.toFixed(1) : 'N/A'}</span>
                </div>
                <div class="meta">
                    <span>${app.installs || 'N/A'} installs</span>
                </div>
            </div>
        `).join('');
    } catch (err) {
        appsDiv.innerHTML = '<div class="empty">Error connecting to API. Make sure the backend is running.</div>';
    }
}

async function scrapeApps() {
    const scrapeType = scrapeSelect.value;
    scrapeBtn.disabled = true;
    scrapeBtn.textContent = '⏳ Scraping...';

    const endpoints = {
        'new': '/scrape/new',
        'new-all': '/scrape/new/all',
        'categories': '/scrape/categories',
        'queries': '/scrape/queries',
        'full': '/scrape/full'
    };

    const labels = {
        'new': 'Quick (New apps - US)',
        'new-all': 'New apps (5 countries)',
        'categories': 'All categories',
        'queries': 'Search queries',
        'full': 'Full scrape (slow)'
    };

    try {
        const res = await fetch(`${API_URL}${endpoints[scrapeType]}`, { method: 'POST' });
        const data = await res.json();
        alert(`Scraped ${data.scraped} apps!`);
        fetchApps(yearSelect.value, monthSelect.value);
        loadStats();
    } catch (err) {
        alert('Error scraping. Check if backend is running.');
    } finally {
        scrapeBtn.disabled = false;
        scrapeBtn.textContent = '🔄 Scrape';
    }
}

async function loadStats() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        const data = await res.json();
        document.getElementById('totalApps').textContent = `Total: ${data.total_apps} apps`;
    } catch (err) {
        console.log('Could not load stats');
    }
}

function getMonthName(month) {
    const months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];
    return months[month];
}

searchBtn.addEventListener('click', () => {
    fetchApps(yearSelect.value, monthSelect.value);
});

scrapeBtn.addEventListener('click', scrapeApps);

// Initial load
fetchApps(yearSelect.value, monthSelect.value);
loadStats();

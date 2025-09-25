// PULSE UK Dashboard JavaScript

// Configuration
const API_URL = 'http://localhost:3001'; // Using proxy to avoid CORS
const REFRESH_INTERVAL = 300000; // 5 minutes
let autoRefreshTimer = null;
let isLoading = false;

// Dashboard state
const dashboardData = {
    culturalPulse: null,
    viralVelocity: null,
    regionalData: null,
    weatherReport: null,
    emergingThemes: null,
    brandOpportunities: null
};

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    initializeDashboard();
    loadAllDashboardData();
    setupEventListeners();
    startAutoRefresh();
});

// Initialize dashboard
function initializeDashboard() {
    // Check for dark mode preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Update theme button
    const themeBtn = document.getElementById('theme-toggle');
    themeBtn.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

    updateTimestamp();
}

// Setup event listeners
function setupEventListeners() {
    // Theme toggle
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

    // About button
    document.getElementById('about-btn').addEventListener('click', toggleAboutPanel);

    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', () => {
        showToast('Refreshing dashboard...', 'info');
        loadAllDashboardData();
    });

    // Chat functionality
    document.getElementById('send-btn').addEventListener('click', sendChatMessage);
    document.getElementById('chat-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChatMessage();
        }
    });

    // Close about panel on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const aboutPanel = document.getElementById('about-panel');
            if (aboutPanel.style.display !== 'none') {
                toggleAboutPanel();
            }
        }
    });

    // Close about panel on background click
    document.getElementById('about-panel').addEventListener('click', (e) => {
        if (e.target.id === 'about-panel') {
            toggleAboutPanel();
        }
    });
}

// Load all dashboard data
async function loadAllDashboardData() {
    if (isLoading) return;
    isLoading = true;

    // Show loading spinners
    showAllLoadingStates();

    try {
        // Fetch all data in parallel
        const [
            culturalPulse,
            viralVelocity,
            regionalData,
            weatherReport,
            emergingThemes,
            brandOpportunities
        ] = await Promise.all([
            fetchCulturalPulse(),
            fetchViralVelocity(),
            fetchRegionalData(),
            fetchWeatherReport(),
            fetchEmergingThemes(),
            fetchBrandOpportunities()
        ]);

        // Update dashboard with fetched data
        updateCulturalPulse(culturalPulse);
        updateViralVelocity(viralVelocity);
        updateRegionalData(regionalData);
        updateWeatherReport(weatherReport);
        updateEmergingThemes(emergingThemes);
        updateBrandOpportunities(brandOpportunities);

        updateTimestamp();
        showToast('Dashboard updated successfully!', 'success');
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showToast('Failed to load some dashboard data', 'error');
    } finally {
        isLoading = false;
    }
}

// API Calls
async function fetchCulturalPulse() {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: 'What are the top 5 trending topics across UK Reddit, YouTube, and news right now? Provide brief titles and sources only.'
            })
        });
        const data = await response.json();
        return parseResponse(data.response || data);
    } catch (error) {
        console.error('Error fetching cultural pulse:', error);
        return generateMockCulturalPulse();
    }
}

async function fetchViralVelocity() {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: 'Identify 3 UK trends gaining rapid momentum with velocity scores (0-100). Include topic, platform, and momentum score.'
            })
        });
        const data = await response.json();
        return parseResponse(data.response || data);
    } catch (error) {
        console.error('Error fetching viral velocity:', error);
        return generateMockViralVelocity();
    }
}

async function fetchRegionalData() {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: 'What are the top trending topics in London, Scotland, Wales, and Northern Ireland? One topic per region.'
            })
        });
        const data = await response.json();
        return parseResponse(data.response || data);
    } catch (error) {
        console.error('Error fetching regional data:', error);
        return generateMockRegionalData();
    }
}

async function fetchWeatherReport() {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: 'Generate a brief UK cultural weather report with current mood and 3-day forecast. Include mood emoji and brief description.'
            })
        });
        const data = await response.json();
        return parseResponse(data.response || data);
    } catch (error) {
        console.error('Error fetching weather report:', error);
        return generateMockWeatherReport();
    }
}

async function fetchEmergingThemes() {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: 'Identify 5 emerging cross-platform themes in UK culture. Just list the theme names.'
            })
        });
        const data = await response.json();
        return parseResponse(data.response || data);
    } catch (error) {
        console.error('Error fetching emerging themes:', error);
        return generateMockEmergingThemes();
    }
}

async function fetchBrandOpportunities() {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: 'List 3 safe brand engagement opportunities based on current UK trends. Include opportunity, risk level (low/medium/high), and confidence score.'
            })
        });
        const data = await response.json();
        return parseResponse(data.response || data);
    } catch (error) {
        console.error('Error fetching brand opportunities:', error);
        return generateMockBrandOpportunities();
    }
}

// Parse API response
function parseResponse(response) {
    if (typeof response === 'string') {
        return response;
    }
    return JSON.stringify(response, null, 2);
}

// Render markdown to HTML
function renderMarkdown(text) {
    // Configure marked options for better rendering
    marked.setOptions({
        breaks: true,
        gfm: true,
        headerIds: false,
        mangle: false
    });
    return marked.parse(text);
}

// Update UI Functions
function updateCulturalPulse(data) {
    const container = document.querySelector('#pulse-monitor .pulse-content');
    const loader = document.querySelector('#pulse-monitor .loading-spinner');
    const trendList = document.querySelector('#pulse-monitor .trend-list');

    loader.style.display = 'none';
    container.style.display = 'block';

    // If data is markdown text, render it directly
    if (typeof data === 'string' && data.includes('*') || data.includes('#') || data.includes('-')) {
        trendList.innerHTML = `<div class="markdown-content">${renderMarkdown(data)}</div>`;
    } else {
        // Parse the response and create trend items
        const trends = extractTrends(data);
        trendList.innerHTML = trends.map(trend => `
            <div class="trend-item">
                <span class="trend-source source-${trend.source.toLowerCase()}">${trend.source}</span>
                <span class="trend-title">${trend.title}</span>
            </div>
        `).join('');
    }
}

function updateViralVelocity(data) {
    const container = document.querySelector('#velocity-tracker .velocity-content');
    const loader = document.querySelector('#velocity-tracker .loading-spinner');
    const itemsContainer = document.querySelector('#velocity-tracker .velocity-items');

    loader.style.display = 'none';
    container.style.display = 'block';

    const velocityItems = extractVelocityItems(data);
    itemsContainer.innerHTML = velocityItems.map(item => `
        <div class="velocity-item">
            <div class="velocity-header">
                <strong>${item.topic}</strong>
                <span class="velocity-score">${item.score}%</span>
            </div>
            <div class="velocity-platform">${item.platform}</div>
            <div class="velocity-bar">
                <div class="velocity-fill" style="width: ${item.score}%"></div>
            </div>
        </div>
    `).join('');
}

function updateRegionalData(data) {
    const container = document.querySelector('#regional-heat .regional-content');
    const loader = document.querySelector('#regional-heat .loading-spinner');
    const regionGrid = document.querySelector('#regional-heat .region-grid');

    loader.style.display = 'none';
    container.style.display = 'block';

    const regions = extractRegionalData(data);
    regionGrid.innerHTML = regions.map(region => `
        <div class="region-card">
            <div class="region-name">${region.name}</div>
            <div class="region-trend">${region.trend}</div>
        </div>
    `).join('');
}

function updateWeatherReport(data) {
    const container = document.querySelector('#sentiment-weather .weather-content');
    const loader = document.querySelector('#sentiment-weather .loading-spinner');
    const summary = document.querySelector('#sentiment-weather .weather-summary');
    const forecast = document.querySelector('#sentiment-weather .weather-forecast');

    loader.style.display = 'none';
    container.style.display = 'block';

    // If data is markdown text, render it directly
    if (typeof data === 'string' && data.length > 0) {
        summary.innerHTML = renderMarkdown(data);
        forecast.innerHTML = ''; // Clear forecast for now
    } else {
        const weather = extractWeatherData(data);
        summary.innerHTML = `
            <div class="weather-mood">${weather.mood}</div>
            <div class="weather-description">${weather.description}</div>
        `;

        forecast.innerHTML = weather.forecast.map(day => `
            <div class="forecast-item">
                <div class="forecast-day">${day.day}</div>
                <div class="forecast-icon">${day.icon}</div>
                <div class="forecast-desc">${day.description}</div>
            </div>
        `).join('');
    }
}

function updateEmergingThemes(data) {
    const container = document.querySelector('#emerging-themes .themes-content');
    const loader = document.querySelector('#emerging-themes .loading-spinner');
    const bubbles = document.querySelector('#emerging-themes .theme-bubbles');

    loader.style.display = 'none';
    container.style.display = 'block';

    const themes = extractThemes(data);
    bubbles.innerHTML = themes.map(theme => `
        <div class="theme-bubble" onclick="exploreTheme('${theme}')">${theme}</div>
    `).join('');
}

function updateBrandOpportunities(data) {
    const container = document.querySelector('#brand-opportunities .opportunities-content');
    const loader = document.querySelector('#brand-opportunities .loading-spinner');
    const list = document.querySelector('#brand-opportunities .opportunity-list');

    loader.style.display = 'none';
    container.style.display = 'block';

    const opportunities = extractOpportunities(data);
    list.innerHTML = opportunities.map(opp => `
        <div class="opportunity-item">
            <div class="opportunity-title">${opp.title}</div>
            <div class="opportunity-meta">
                <span class="risk-level risk-${opp.risk}">${opp.risk} risk</span>
                <span class="confidence">${opp.confidence}% confidence</span>
            </div>
        </div>
    `).join('');
}

// Data extraction functions (parse API responses)
function extractTrends(data) {
    // This would parse the actual API response
    // For now, return sample data
    return [
        { source: 'Reddit', title: 'UK Weather Discussion Thread' },
        { source: 'YouTube', title: 'Premier League Highlights' },
        { source: 'Guardian', title: 'NHS Funding Debate' },
        { source: 'Reddit', title: 'British Problems Weekly' },
        { source: 'YouTube', title: 'London Underground Documentary' }
    ];
}

function extractVelocityItems(data) {
    return [
        { topic: 'Cost of Living Crisis', platform: 'Cross-platform', score: 95 },
        { topic: 'Eurovision 2024', platform: 'YouTube/Twitter', score: 78 },
        { topic: 'UK Tech Startups', platform: 'LinkedIn/Reddit', score: 65 }
    ];
}

function extractRegionalData(data) {
    return [
        { name: '🏴󐁧󐁢󐁥󐁮󐁧󐁿 London', trend: 'Housing Market Crisis' },
        { name: '🏴󐁧󐁢󐁳󐁣󐁴󐁿 Scotland', trend: 'Independence Debate' },
        { name: '🏴󐁧󐁢󐁷󐁬󐁳󐁿 Wales', trend: 'Rugby Six Nations' },
        { name: '🇬🇧 N. Ireland', trend: 'Windsor Framework' }
    ];
}

function extractWeatherData(data) {
    return {
        mood: '⛅ Partly Optimistic',
        description: 'The UK cultural climate shows mixed sentiments with pockets of optimism around sports and entertainment, balanced by ongoing economic concerns.',
        forecast: [
            { day: 'Today', icon: '⛅', description: 'Mixed' },
            { day: 'Tomorrow', icon: '🌤️', description: 'Improving' },
            { day: 'Weekend', icon: '☀️', description: 'Positive' }
        ]
    };
}

function extractThemes(data) {
    return [
        'Sustainability',
        'Mental Health',
        'Remote Work',
        'AI Ethics',
        'Local Communities'
    ];
}

function extractOpportunities(data) {
    return [
        { title: 'Eco-friendly Product Launch', risk: 'low', confidence: 85 },
        { title: 'Community Support Initiative', risk: 'low', confidence: 92 },
        { title: 'Tech Innovation Campaign', risk: 'medium', confidence: 75 }
    ];
}

// Chat functionality
async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('chat-messages');
    const message = input.value.trim();

    if (!message) return;

    // Add user message
    addMessage(message, 'user');

    // Clear input and disable send button
    input.value = '';
    sendBtn.disabled = true;

    // Update chat status
    document.querySelector('.chat-status').textContent = 'Thinking...';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: message })
        });

        const data = await response.json();
        const reply = data.response || data.error || 'No response received';

        addMessage(reply, 'assistant');
    } catch (error) {
        addMessage('Sorry, I encountered an error. Please try again.', 'assistant');
    } finally {
        sendBtn.disabled = false;
        document.querySelector('.chat-status').textContent = 'Ready';
    }
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Render markdown for assistant messages, plain text for user messages
    if (sender === 'assistant') {
        contentDiv.innerHTML = renderMarkdown(text);
    } else {
        contentDiv.textContent = text;
    }

    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Quick query function
function quickQuery(query) {
    document.getElementById('chat-input').value = query;
    sendChatMessage();
}

// Explore theme function
function exploreTheme(theme) {
    quickQuery(`Tell me more about the "${theme}" trend in UK culture`);
}

// Utility functions
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);

    const themeBtn = document.getElementById('theme-toggle');
    themeBtn.textContent = newTheme === 'dark' ? '☀️' : '🌙';
}

function toggleAboutPanel() {
    const aboutPanel = document.getElementById('about-panel');
    if (aboutPanel.style.display === 'none' || !aboutPanel.style.display) {
        aboutPanel.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    } else {
        aboutPanel.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
    }
}

function updateTimestamp() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-GB', {
        hour: '2-digit',
        minute: '2-digit'
    });
    const dateString = now.toLocaleDateString('en-GB', {
        day: 'numeric',
        month: 'short'
    });

    document.getElementById('last-update').textContent = `Last updated: ${timeString}, ${dateString}`;
}

function showAllLoadingStates() {
    const cards = document.querySelectorAll('.dashboard-card');
    cards.forEach(card => {
        const loader = card.querySelector('.loading-spinner');
        const content = card.querySelector('.card-content > div:last-child');
        if (loader) loader.style.display = 'block';
        if (content) content.style.display = 'none';
    });
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function startAutoRefresh() {
    autoRefreshTimer = setInterval(() => {
        loadAllDashboardData();
    }, REFRESH_INTERVAL);
}

// Mock data generators (fallback for when API is unavailable)
function generateMockCulturalPulse() {
    return 'Loading sample data...';
}

function generateMockViralVelocity() {
    return 'Loading sample data...';
}

function generateMockRegionalData() {
    return 'Loading sample data...';
}

function generateMockWeatherReport() {
    return 'Loading sample data...';
}

function generateMockEmergingThemes() {
    return 'Loading sample data...';
}

function generateMockBrandOpportunities() {
    return 'Loading sample data...';
}
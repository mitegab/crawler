# Tech News Crawler & Amharic Translation ## 📚 Documentation

**Backend Setup:**
- 🚀 **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- 📘 **[Appwrite Setup Guide](docs/APPWRITE_SETUP.md)** - Complete step-by-step Appwrite configuration
- ⚡ **[Appwrite Functions Guide](docs/APPWRITE_FUNCTIONS.md)** - Serverless functions deployment
- 📋 **[Quick Reference](docs/APPWRITE_QUICK_REFERENCE.md)** - Checklists and visual guides

**Frontend Setup:**
- 🎨 **[Vue.js Frontend Setup](docs/VUE_FRONTEND_SETUP.md)** - Build the public website with Vue.js
- 🌐 **[Web Platform Configuration](docs/APPWRITE_SETUP.md#step-24-add-web-platform-optional---for-future-frontend)** - Configure Appwrite for frontendrm

A comprehensive web application that crawls tech news from popular channels, translates content to Amharic, and publishes it on a website.

## 🚀 Features

- **Multi-Source Scraping**: Automatically scrapes articles from TechCrunch, The Verge, Ars Technica, Wired, and more
- **Translation**: Translates English tech news to Amharic using AI translation services
- **Backend as a Service**: Uses Appwrite for database, storage, and authentication
- **Anti-Bot Protection**: Optional Zyte API integration for bypassing anti-scraping measures
- **Automated Pipeline**: Scheduled scraping and translation with Appwrite Functions
- **Admin Dashboard**: Web interface for managing articles and translations
- **Responsive Website**: Public-facing website with mobile-first design

## 📋 Project Structure

```
crawler/
├── backend/                    # Python backend for scraping & translation
│   ├── scrapers/              # Site-specific scrapers
│   ├── translators/           # Translation services
│   ├── services/              # Business logic
│   ├── appwrite_functions/    # Serverless functions
│   ├── config/                # Configuration files
│   ├── utils/                 # Utility functions
│   └── main.py                # Entry point
├── frontend/                  # Next.js frontend (to be created)
├── tests/                     # Unit tests
├── docker/                    # Docker configuration
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🛠️ Technology Stack

- **Backend**: Python 3.9+
- **Web Scraping**: BeautifulSoup4, Scrapy, Selenium
- **Translation**: Google Translate API / Azure Translator / OpenAI
- **BaaS**: Appwrite (Database, Storage, Functions, Auth)
- **Anti-Bot**: Zyte API (optional)
- **Frontend**: Next.js, React, TypeScript (to be implemented)

## � Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Appwrite Setup Guide](docs/APPWRITE_SETUP.md)** - Complete step-by-step Appwrite configuration
- **[Appwrite Functions Guide](docs/APPWRITE_FUNCTIONS.md)** - Serverless functions deployment
- **[Quick Reference](docs/APPWRITE_QUICK_REFERENCE.md)** - Checklists and visual guides

## �📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Appwrite Cloud account (free tier available - [Sign up here](https://cloud.appwrite.io))
- Optional: Zyte API account for advanced scraping

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd crawler
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Set up Appwrite**
   
   See the **[Complete Appwrite Setup Guide](docs/APPWRITE_SETUP.md)** for detailed instructions.
   
   **Quick Setup:**
   - Create Appwrite account at https://cloud.appwrite.io
   - Follow **[APPWRITE_SETUP.md](docs/APPWRITE_SETUP.md)** for:
     - Database creation (3 collections)
     - Storage bucket setup
     - API key generation
     - Serverless functions deployment
   
   **Or use the quick test:**
   ```bash
   cd backend
   python test_appwrite.py  # Tests your Appwrite configuration
   ```

6. **Seed News Sources**
   ```bash
   cd backend
   python seed_sources.py --seed  # Adds initial news sources to database
   ```

## 🚀 Usage

### Running the Crawler

```bash
cd backend
python main.py
```

This will:
1. Scrape articles from configured sources
2. Translate content to Amharic
3. Save to Appwrite database (if configured)
4. Save output to `output/articles.json`

### Managing News Sources

```bash
cd backend

# List all sources
python seed_sources.py --list

# Enable a source
python seed_sources.py --enable "TechRadar"

# Disable a source
python seed_sources.py --disable "Wired"

# Re-seed sources
python seed_sources.py --seed
```

### Configuration

Edit `backend/config/sources.json` to add/remove news sources:

```json
{
  "sources": [
    {
      "name": "Source Name",
      "url": "https://example.com",
      "enabled": true,
      "scraper_class": "ScraperClassName"
    }
  ]
}
```

## 🧪 Testing

Run tests with pytest:

```bash
cd tests
pytest
```

## 📝 Environment Variables

Key environment variables (see `.env.example` for full list):

- `APPWRITE_PROJECT_ID`: Your Appwrite project ID
- `APPWRITE_API_KEY`: Your Appwrite API key
- `ZYTE_API_KEY`: Zyte API key (optional)
- `USE_ZYTE`: Enable/disable Zyte (true/false)
- `TRANSLATION_SERVICE`: Translation service (google/azure/openai)
- `MAX_ARTICLES_PER_SOURCE`: Number of articles to scrape per source

## 🗺️ Roadmap

- [x] Backend scraping infrastructure
- [x] Translation service
- [x] Appwrite integration
- [ ] Appwrite Functions for automation
- [ ] Frontend website (Next.js)
- [ ] Admin dashboard
- [ ] User authentication
- [ ] Comment system
- [ ] Social sharing
- [ ] Mobile app

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Legal Disclaimer

This tool is for educational purposes. Always:
- Respect website Terms of Service
- Follow robots.txt directives
- Implement appropriate rate limiting
- Link back to original sources
- Respect copyright and intellectual property

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is an early version. Frontend and automation features are coming soon!

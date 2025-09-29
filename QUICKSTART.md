# Quick Start Guide

## Get Started in 5 Minutes

### 1. Prerequisites Check
```bash
# Check Python version (need 3.9+)
python --version

# Check pip
pip --version
```

### 2. Setup Virtual Environment
```bash
# Navigate to project
cd /home/ethiopique/Downloads/os/crawler

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your credentials
nano .env  # or use your preferred editor
```

**Minimum required settings for testing (without Appwrite):**
```bash
# Leave Appwrite settings empty for local testing
USE_ZYTE=false
TRANSLATION_SERVICE=google
MAX_ARTICLES_PER_SOURCE=3
LOG_LEVEL=INFO
```

### 5. Test Run (Without Database)
```bash
# Run the crawler
python main.py
```

This will:
- Scrape 3 articles from each source
- Translate them to Amharic
- Save results to `output/articles.json`
- NOT save to database (since Appwrite is not configured)

### 6. View Results
```bash
# Check the output file
cat output/articles.json | head -50
```

---

## Full Setup with Appwrite

### 1. Create Appwrite Account
1. Go to https://cloud.appwrite.io
2. Sign up for free account
3. Create a new project

### 2. Create Database
1. In Appwrite Console, go to **Databases**
2. Click **Create Database**
3. Name it: `tech-news-db`
4. Note the Database ID

### 3. Create Collection
1. Inside your database, click **Create Collection**
2. Name it: `articles`
3. Add the following attributes:

| Attribute Name | Type | Size | Required |
|---------------|------|------|----------|
| title_en | String | 500 | Yes |
| title_am | String | 500 | No |
| content_en | String | 65535 | Yes |
| content_am | String | 65535 | No |
| source | String | 100 | Yes |
| source_url | String | 500 | Yes |
| author | String | 200 | No |
| published_date | String | 50 | No |
| scraped_at | String | 50 | No |
| category | String | 100 | No |
| tags | String[] | - | No |
| featured_image | String | 500 | No |
| status | String | 50 | No |

4. Set permissions to allow API key access

### 4. Create Storage Bucket
1. Go to **Storage** in Appwrite Console
2. Click **Create Bucket**
3. Name it: `article-images`
4. Configure permissions for API access

### 5. Generate API Key
1. Go to **Settings** → **API Keys**
2. Click **Create API Key**
3. Name it: `Crawler API Key`
4. Set scopes:
   - Database: Read, Write
   - Storage: Read, Write
5. Copy the API key (you'll only see it once!)

### 6. Update .env File
```bash
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id_here
APPWRITE_API_KEY=your_api_key_here
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles
APPWRITE_STORAGE_BUCKET_ID=article-images
```

### 7. Run with Database
```bash
python main.py
```

Now articles will be saved to Appwrite!

---

## Docker Setup (Optional)

### Build and Run with Docker
```bash
# Build the image
cd docker
docker-compose build

# Run the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Translation Errors
```bash
# If googletrans fails, try alternative:
pip uninstall googletrans
pip install googletrans==4.0.0rc1
```

### Scraping Blocked
- Some sites may block requests
- Consider using Zyte API (sign up at https://www.zyte.com)
- Add your Zyte API key to `.env`
- Set `USE_ZYTE=true`

### No Articles Scraped
- Check your internet connection
- Some sites may have changed their HTML structure
- Check logs in `logs/crawler.log`
- Try running with fewer sources first

---

## Next Steps

1. **Customize Sources**: Edit `backend/config/sources.json`
2. **Add More Scrapers**: Create new scraper classes in `backend/scrapers/`
3. **Setup Frontend**: Follow the detailed plan to create Next.js frontend
4. **Deploy Functions**: Deploy Appwrite Functions for automation
5. **Schedule Jobs**: Set up CRON jobs for periodic scraping

---

## Need Help?

- Check the main README.md for detailed documentation
- Review the code comments in each module
- Open an issue on GitHub

Happy Crawling! 🚀

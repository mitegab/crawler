# Appwrite Cloud Setup Guide

Complete guide to setting up Appwrite Cloud for the Tech News Crawler project.

---

## Table of Contents
1. [Create Appwrite Account](#1-create-appwrite-account)
2. [Create Project](#2-create-project)
3. [Database Setup](#3-database-setup)
4. [Storage Setup](#4-storage-setup)
5. [Authentication & API Keys](#5-authentication--api-keys)
6. [Serverless Functions](#6-serverless-functions)
7. [Configuration](#7-configuration)
8. [Testing](#8-testing)

---

## 1. Create Appwrite Account

### Step 1.1: Sign Up
1. Navigate to [https://cloud.appwrite.io](https://cloud.appwrite.io)
2. Click **"Get Started"** or **"Sign Up"**
3. Choose sign-up method:
   - Email and password
   - GitHub account (recommended for developers)
   - Google account
4. Verify your email address
5. Complete profile setup

### Step 1.2: Choose Plan
- **Free Tier** includes:
  - 75,000 database reads/day
  - 375,000 database writes/day
  - 2 GB bandwidth
  - 2 GB storage
  - Unlimited projects
  - Perfect for development and testing!

---

## 2. Create Project

### Step 2.1: Create New Project
1. From the Appwrite dashboard, click **"Create Project"**
2. Enter project details:
   - **Name**: `Tech News Crawler`
   - **Project ID**: Auto-generated (e.g., `tech-news-crawler-abc123`)
3. Click **"Create"**

### Step 2.2: Note Project Details
📝 **Save this information - you'll need it later:**
```
Project ID: [your-project-id]
Endpoint: https://cloud.appwrite.io/v1
```

### Step 2.3: Project Settings
1. Go to **Settings** → **General**
2. Configure:
   - **Description**: "Automated tech news crawler with Amharic translation"
   - **Logo**: (optional) Upload a logo
3. Note the **API Endpoint**: `https://cloud.appwrite.io/v1`

---

## 3. Database Setup

### Step 3.1: Create Database
1. In your project, navigate to **Databases** (left sidebar)
2. Click **"Create Database"**
3. Enter:
   - **Database ID**: `tech-news-db`
   - **Name**: `Tech News Database`
4. Click **"Create"**

📝 **Save your Database ID**: `tech-news-db`

### Step 3.2: Create Collections

#### Collection 1: `articles`
This stores all scraped and translated articles.

1. Inside `tech-news-db`, click **"Create Collection"**
2. Enter:
   - **Collection ID**: `articles`
   - **Name**: `Articles`
3. Click **"Create"**

**Add Attributes:**

Click **"Add Attribute"** for each of the following:

| Attribute Name | Type | Size/Options | Required | Default | Description |
|---------------|------|--------------|----------|---------|-------------|
| `title_en` | String | 500 | ✅ Yes | - | Original English title |
| `title_am` | String | 500 | ❌ No | - | Translated Amharic title |
| `content_en` | String | 65535 | ✅ Yes | - | Original English content |
| `content_am` | String | 65535 | ❌ No | - | Translated Amharic content |
| `summary_en` | String | 2000 | ❌ No | - | English summary |
| `summary_am` | String | 2000 | ❌ No | - | Amharic summary |
| `source` | String | 100 | ✅ Yes | - | Source name (e.g., "TechCrunch") |
| `source_url` | String | 1000 | ✅ Yes | - | Original article URL |
| `author` | String | 200 | ❌ No | - | Article author |
| `published_date` | DateTime | - | ❌ No | - | Original publish date |
| `scraped_at` | DateTime | - | ✅ Yes | - | When article was scraped |
| `translated_at` | DateTime | - | ❌ No | - | When translation completed |
| `category` | String | 100 | ❌ No | - | Article category (AI, Hardware, etc.) |
| `tags` | String[] | - | ❌ No | - | Array of tags |
| `featured_image` | String | 1000 | ❌ No | - | Main image URL |
| `images` | String[] | - | ❌ No | - | Array of image URLs |
| `status` | Enum | - | ✅ Yes | pending | See options below |
| `view_count` | Integer | - | ❌ No | 0 | Number of views |
| `is_featured` | Boolean | - | ❌ No | false | Featured article flag |

**Status Enum Options:**
- `pending`: Just scraped, awaiting translation
- `translating`: Currently being translated
- `translated`: Translation complete
- `published`: Published to frontend
- `failed`: Processing failed
- `archived`: Old/archived article

**Create Indexes:**
1. Click **"Indexes"** tab
2. Add the following indexes for better query performance:

| Index Key | Type | Attributes | Order |
|-----------|------|------------|-------|
| `status_scraped` | Key | status, scraped_at | ASC, DESC |
| `source_date` | Key | source, published_date | ASC, DESC |
| `category` | Key | category | ASC |
| `featured` | Key | is_featured | DESC |

**Set Permissions:**
1. Click **"Settings"** tab
2. Under **Permissions**:
   - **Read**: Anyone (for public access)
   - **Create**: API Key only
   - **Update**: API Key only
   - **Delete**: API Key only

#### Collection 2: `sources`
This manages news sources configuration.

1. Click **"Create Collection"**
2. Enter:
   - **Collection ID**: `sources`
   - **Name**: `News Sources`
3. Click **"Create"**

**Add Attributes:**

| Attribute Name | Type | Size/Options | Required | Default | Description |
|---------------|------|--------------|----------|---------|-------------|
| `name` | String | 100 | ✅ Yes | - | Source name (e.g., "TechCrunch") |
| `url` | String | 500 | ✅ Yes | - | Base URL of the news site |
| `enabled` | Boolean | - | ✅ Yes | true | Whether to scrape this source |
| `scraper_class` | String | 100 | ✅ Yes | - | Python class name (e.g., "TechCrunchScraper") |
| `selector_config` | String | 10000 | ✅ Yes | - | JSON string with CSS selectors |
| `last_crawled` | DateTime | - | ❌ No | - | Last successful crawl time |
| `crawl_frequency` | Integer | - | ✅ Yes | 3600 | Seconds between crawls |
| `max_articles` | Integer | - | ✅ Yes | 10 | Max articles per crawl |
| `category` | String | 50 | ❌ No | - | Main category of source |
| `language` | String | 10 | ✅ Yes | en | Source language code |
| `priority` | Integer | - | ✅ Yes | 1 | Crawl priority (1-10) |
| `error_count` | Integer | - | ❌ No | 0 | Consecutive errors |
| `status` | Enum | - | ✅ Yes | active | See options below |

**Status Enum Options:**
- `active`: Currently scraping
- `paused`: Temporarily disabled
- `error`: Too many errors
- `testing`: In testing phase

**Create Indexes:**

| Index Key | Type | Attributes | Order |
|-----------|------|------------|-------|
| `enabled_priority` | Key | enabled, priority | ASC, DESC |
| `status` | Key | status | ASC |

**Set Permissions:**
- **Read**: Anyone or API Key
- **Create**: API Key only
- **Update**: API Key only
- **Delete**: API Key only

**Seed Initial Data:**
After creating the collection, add initial sources via Appwrite Console or API:

```json
[
  {
    "name": "TechCrunch",
    "url": "https://techcrunch.com",
    "enabled": true,
    "scraper_class": "TechCrunchScraper",
    "selector_config": "{\"article_links\": \".post-block__title__link\", \"title\": \".article__title\", \"content\": \".article-content\", \"author\": \".article__byline a\", \"date\": \".article__byline time\"}",
    "crawl_frequency": 3600,
    "max_articles": 10,
    "language": "en",
    "priority": 10,
    "status": "active"
  },
  {
    "name": "The Verge",
    "url": "https://www.theverge.com/tech",
    "enabled": true,
    "scraper_class": "TheVergeScraper",
    "selector_config": "{\"article_links\": \"h2 a\", \"title\": \".duet--article--article-title\", \"content\": \".duet--article--article-body\", \"author\": \".duet--article--article-author-name\", \"date\": \".duet--article--article-date\"}",
    "crawl_frequency": 3600,
    "max_articles": 10,
    "language": "en",
    "priority": 9,
    "status": "active"
  },
  {
    "name": "Ars Technica",
    "url": "https://arstechnica.com",
    "enabled": true,
    "scraper_class": "ArsTechnicaScraper",
    "selector_config": "{\"article_links\": \".article-title a\", \"title\": \"h1.heading\", \"content\": \".article-content\", \"author\": \".author-name\", \"date\": \"time.date\"}",
    "crawl_frequency": 3600,
    "max_articles": 10,
    "language": "en",
    "priority": 8,
    "status": "active"
  },
  {
    "name": "Wired",
    "url": "https://www.wired.com",
    "enabled": true,
    "scraper_class": "WiredScraper",
    "selector_config": "{\"article_links\": \".summary-item__hed-link\", \"title\": \".content-header__row h1\", \"content\": \".article__body\", \"author\": \".byline__name\", \"date\": \"time.content-header__publish-date\"}",
    "crawl_frequency": 3600,
    "max_articles": 10,
    "language": "en",
    "priority": 7,
    "status": "active"
  }
]
```

#### Collection 3: `translations_queue`
This manages the translation processing queue.

1. Click **"Create Collection"**
2. Enter:
   - **Collection ID**: `translations_queue`
   - **Name**: `Translation Queue`
3. Click **"Create"**

**Add Attributes:**

| Attribute Name | Type | Size/Options | Required | Default | Description |
|---------------|------|--------------|----------|---------|-------------|
| `article_id` | String | 100 | ✅ Yes | - | Reference to articles collection |
| `status` | Enum | - | ✅ Yes | pending | See options below |
| `retry_count` | Integer | - | ✅ Yes | 0 | Number of retry attempts |
| `max_retries` | Integer | - | ✅ Yes | 3 | Maximum retry attempts |
| `created_at` | DateTime | - | ✅ Yes | - | When added to queue |
| `started_at` | DateTime | - | ❌ No | - | When translation started |
| `completed_at` | DateTime | - | ❌ No | - | When translation finished |
| `error_message` | String | 1000 | ❌ No | - | Last error message |
| `translation_service` | String | 50 | ✅ Yes | google | Service used (google, azure, openai) |
| `priority` | Integer | - | ✅ Yes | 5 | Queue priority (1-10) |

**Status Enum Options:**
- `pending`: Waiting in queue
- `processing`: Currently translating
- `completed`: Successfully translated
- `failed`: Translation failed
- `retrying`: Waiting for retry

**Create Indexes:**

| Index Key | Type | Attributes | Order |
|-----------|------|------------|-------|
| `status_priority` | Key | status, priority | ASC, DESC |
| `article_status` | Key | article_id, status | ASC, ASC |

**Set Permissions:**
- **Read**: API Key only
- **Create**: API Key only
- **Update**: API Key only
- **Delete**: API Key only

---

## 4. Storage Setup

### Step 4.1: Create Storage Bucket
1. Navigate to **Storage** in the left sidebar
2. Click **"Create Bucket"**
3. Configure:
   - **Bucket ID**: `article-images`
   - **Name**: `Article Images`
   - **Permissions**: Select "Bucket" level
4. Click **"Create"**

### Step 4.2: Configure Bucket Settings
1. Click on the `article-images` bucket
2. Go to **Settings** tab

**File Security:**
- **Maximum File Size**: 10 MB
- **Allowed File Extensions**: `jpg, jpeg, png, gif, webp, svg`
- **Compression**: Enabled (select "Compression" option)
- **Antivirus**: Enabled (for security)

**Permissions:**
- **Read**: Anyone (for public image access)
- **Create**: API Key only
- **Update**: API Key only
- **Delete**: API Key only

### Step 4.3: Optional - Create Additional Buckets
If you want to organize images better:

**Bucket 2: `article-thumbnails`**
- For storing compressed thumbnails
- Maximum size: 2 MB
- Same permissions as above

**Bucket 3: `source-logos`**
- For storing news source logos
- Maximum size: 1 MB
- Same permissions as above

---

## 5. Authentication & API Keys

### Step 5.1: Create API Key
1. Go to **Settings** → **API Keys**
2. Click **"Create API Key"**
3. Configure:
   - **Name**: `Crawler Backend API Key`
   - **Expiration**: Never (or set custom date)
   
4. **Select Scopes** (check all that apply):
   
   **Database:**
   - ✅ `databases.read`
   - ✅ `databases.write`
   - ✅ `collections.read`
   - ✅ `collections.write`
   - ✅ `documents.read`
   - ✅ `documents.write`
   
   **Storage:**
   - ✅ `files.read`
   - ✅ `files.write`
   
   **Functions:**
   - ✅ `functions.read`
   - ✅ `functions.write`
   - ✅ `execution.read`
   - ✅ `execution.write`

5. Click **"Create"**

### Step 5.2: Save API Key
⚠️ **IMPORTANT**: Copy and save the API key immediately!
```
API Key: [your-secret-api-key]
```
You'll only see it once. Store it securely.

### Step 5.3: Create Additional API Keys (Optional)

**For Frontend (Read-only):**
1. Create another API key: `Frontend Read API Key`
2. Scopes:
   - ✅ `documents.read` (databases)
   - ✅ `files.read` (storage)

**For Functions:**
1. Create: `Functions API Key`
2. Scopes:
   - ✅ All function-related scopes
   - ✅ Database read/write
   - ✅ Storage read/write

---

## 6. Serverless Functions

### Step 6.1: Enable Functions
1. Navigate to **Functions** in left sidebar
2. Appwrite Functions are enabled by default in Cloud

### Step 6.2: Create Scheduled Crawler Function

1. Click **"Create Function"**
2. Configure:
   - **Function ID**: `scheduled-crawler`
   - **Name**: `Scheduled News Crawler`
   - **Runtime**: Python 3.11
   - **Entrypoint**: `main.py`
   - **Execute Access**: API Key only

3. Click **"Create"**

**Configure Trigger:**
1. Go to **Settings** tab
2. Under **Triggers**, click **"Add Trigger"**
3. Select **Schedule**
4. Set CRON expression:
   ```
   0 */3 * * *
   ```
   (Runs every 3 hours)
5. Click **"Add"**

**Deploy Function:**
1. Go to **Code** tab
2. Click **"Upload Code"**
3. Upload the contents of `backend/appwrite_functions/scheduled_crawler/`
   - Include: `main.py`, `requirements.txt`, `appwrite.json`
4. Or connect to GitHub:
   - Click **"Connect Git"**
   - Select repository
   - Set path: `backend/appwrite_functions/scheduled_crawler`
   - Enable auto-deploy on push

**Environment Variables:**
1. Go to **Settings** tab
2. Under **Environment Variables**, add:
   ```
   APPWRITE_API_KEY=[your-api-key]
   APPWRITE_DATABASE_ID=tech-news-db
   APPWRITE_ARTICLES_COLLECTION_ID=articles
   APPWRITE_SOURCES_COLLECTION_ID=sources
   TRANSLATION_SERVICE=google
   MAX_ARTICLES_PER_SOURCE=10
   ```

### Step 6.3: Create Translation Function

1. Click **"Create Function"**
2. Configure:
   - **Function ID**: `translate-article`
   - **Name**: `Article Translation Service`
   - **Runtime**: Python 3.11
   - **Entrypoint**: `main.py`
   - **Execute Access**: API Key only

3. Click **"Create"**

**Configure Trigger:**
1. Go to **Settings** tab
2. Under **Triggers**, click **"Add Trigger"**
3. Select **Event**
4. Event type: `databases.*.collections.articles.documents.*.create`
   (Triggers when new article is created)
5. Click **"Add"**

**Deploy Function:**
1. Upload code from `backend/appwrite_functions/translate_article/`
2. Or connect to GitHub (same as above)

**Environment Variables:**
```
APPWRITE_API_KEY=[your-api-key]
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles
APPWRITE_QUEUE_COLLECTION_ID=translations_queue
TRANSLATION_SERVICE=google
GOOGLE_TRANSLATE_API_KEY=[optional]
AZURE_TRANSLATOR_KEY=[optional]
OPENAI_API_KEY=[optional]
```

### Step 6.4: Create Queue Processor Function (Optional)

For processing the translation queue asynchronously:

1. Create function: `process-translation-queue`
2. Runtime: Python 3.11
3. Trigger: Schedule (`*/10 * * * *` - every 10 minutes)
4. Upload code (you'll need to create this):

**Create file**: `backend/appwrite_functions/queue_processor/main.py`
```python
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
import os

def main(req, res):
    client = Client()
    client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
    client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
    client.set_key(os.getenv('APPWRITE_API_KEY'))
    
    databases = Databases(client)
    
    # Get pending items from queue
    queue_items = databases.list_documents(
        database_id=os.getenv('APPWRITE_DATABASE_ID'),
        collection_id='translations_queue',
        queries=[
            Query.equal('status', 'pending'),
            Query.less_than('retry_count', 3),
            Query.order_desc('priority'),
            Query.limit(10)
        ]
    )
    
    processed = 0
    for item in queue_items['documents']:
        # Process translation
        # Update article
        # Update queue item status
        processed += 1
    
    return res.json({
        'success': True,
        'processed': processed
    })
```

### Step 6.5: Test Functions

**Test Scheduled Crawler:**
1. Go to function details
2. Click **"Execute Now"**
3. Check logs for output
4. Verify articles in database

**Test Translation Function:**
1. Manually create an article in the `articles` collection
2. Function should auto-trigger
3. Check logs
4. Verify translation in article document

---

## 7. Configuration

### Step 7.1: Update .env File

Update your local `backend/.env` file with all the IDs:

```bash
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id-here
APPWRITE_API_KEY=your-api-key-here

# Database
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles
APPWRITE_SOURCES_COLLECTION_ID=sources
APPWRITE_QUEUE_COLLECTION_ID=translations_queue

# Storage
APPWRITE_STORAGE_BUCKET_ID=article-images
APPWRITE_THUMBNAILS_BUCKET_ID=article-thumbnails  # if created
APPWRITE_LOGOS_BUCKET_ID=source-logos  # if created

# Translation
TRANSLATION_SERVICE=google
GOOGLE_TRANSLATE_API_KEY=  # optional, uses free googletrans
AZURE_TRANSLATOR_KEY=  # optional
AZURE_TRANSLATOR_REGION=  # optional
OPENAI_API_KEY=  # optional

# Zyte (optional)
USE_ZYTE=false
ZYTE_API_KEY=

# Scraper Settings
MAX_ARTICLES_PER_SOURCE=10
CRAWL_DELAY=2
REQUEST_TIMEOUT=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/crawler.log
```

### Step 7.2: Update Backend Code

Ensure your `backend/config/settings.py` reads all these variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Appwrite
APPWRITE_ENDPOINT = os.getenv('APPWRITE_ENDPOINT', 'https://cloud.appwrite.io/v1')
APPWRITE_PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID', '')
APPWRITE_API_KEY = os.getenv('APPWRITE_API_KEY', '')
APPWRITE_DATABASE_ID = os.getenv('APPWRITE_DATABASE_ID', 'tech-news-db')
APPWRITE_ARTICLES_COLLECTION_ID = os.getenv('APPWRITE_ARTICLES_COLLECTION_ID', 'articles')
APPWRITE_SOURCES_COLLECTION_ID = os.getenv('APPWRITE_SOURCES_COLLECTION_ID', 'sources')
APPWRITE_QUEUE_COLLECTION_ID = os.getenv('APPWRITE_QUEUE_COLLECTION_ID', 'translations_queue')
APPWRITE_STORAGE_BUCKET_ID = os.getenv('APPWRITE_STORAGE_BUCKET_ID', 'article-images')
```

---

## 8. Testing

### Step 8.1: Test Database Connection

Create `backend/test_appwrite.py`:

```python
from appwrite.client import Client
from appwrite.services.databases import Databases
from config.settings import *

client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)

databases = Databases(client)

# Test connection
try:
    result = databases.list_collections(APPWRITE_DATABASE_ID)
    print("✅ Connected to Appwrite successfully!")
    print(f"Found {result['total']} collections:")
    for collection in result['collections']:
        print(f"  - {collection['name']} ({collection['$id']})")
except Exception as e:
    print(f"❌ Error: {e}")
```

Run:
```bash
cd backend
python test_appwrite.py
```

### Step 8.2: Test Article Creation

```python
from appwrite.id import ID
from datetime import datetime

# Create test article
try:
    article = databases.create_document(
        database_id=APPWRITE_DATABASE_ID,
        collection_id=APPWRITE_ARTICLES_COLLECTION_ID,
        document_id=ID.unique(),
        data={
            'title_en': 'Test Article',
            'content_en': 'This is a test article.',
            'source': 'Test',
            'source_url': 'https://example.com',
            'scraped_at': datetime.now().isoformat(),
            'status': 'pending'
        }
    )
    print(f"✅ Article created: {article['$id']}")
except Exception as e:
    print(f"❌ Error creating article: {e}")
```

### Step 8.3: Test Storage Upload

```python
from appwrite.services.storage import Storage
from appwrite.input_file import InputFile

storage = Storage(client)

try:
    file = storage.create_file(
        bucket_id=APPWRITE_STORAGE_BUCKET_ID,
        file_id=ID.unique(),
        file=InputFile.from_path('path/to/test/image.jpg')
    )
    print(f"✅ File uploaded: {file['$id']}")
except Exception as e:
    print(f"❌ Error uploading file: {e}")
```

### Step 8.4: Run Full Crawler Test

```bash
cd backend
python main.py
```

Check:
1. Articles appear in Appwrite console
2. Images uploaded to storage
3. Translation queue populated
4. Logs show no errors

---

## 9. Monitoring & Maintenance

### Dashboard Overview
Monitor your crawler from Appwrite Console:

1. **Database** → `articles` collection
   - View article count
   - Check status distribution
   - Monitor recent entries

2. **Storage** → `article-images`
   - Check storage usage
   - View recent uploads

3. **Functions**
   - Check execution logs
   - Monitor success/failure rate
   - View execution time

### Set Up Alerts (Optional)
1. Go to **Settings** → **Webhooks**
2. Create webhook for errors
3. Send to your monitoring service (Slack, Discord, etc.)

### Backup Strategy
1. **Database**: Use Appwrite's export feature
   - Go to Database → Settings → Export
2. **Storage**: Periodically download important images
3. **Code**: Keep git repository updated

---

## 10. Troubleshooting

### Common Issues

**"Permission denied" errors:**
- Check API key has correct scopes
- Verify collection permissions
- Ensure API key hasn't expired

**"Document not found":**
- Verify Database ID and Collection ID
- Check document exists in console
- Confirm API key can read collection

**Functions not triggering:**
- Check CRON expression is valid
- Verify event patterns match
- Check function logs for errors

**Translation not working:**
- Verify translation service credentials
- Check queue collection permissions
- Review function logs

### Get Help
- **Documentation**: https://appwrite.io/docs
- **Discord**: https://appwrite.io/discord
- **GitHub**: https://github.com/appwrite/appwrite

---

## Summary Checklist

✅ **Account & Project**
- [ ] Appwrite Cloud account created
- [ ] Project created and configured
- [ ] Project ID and endpoint noted

✅ **Database**
- [ ] Database `tech-news-db` created
- [ ] Collection `articles` created with all attributes
- [ ] Collection `sources` created and seeded
- [ ] Collection `translations_queue` created
- [ ] Indexes created for all collections
- [ ] Permissions configured

✅ **Storage**
- [ ] Bucket `article-images` created
- [ ] File security configured
- [ ] Permissions set

✅ **Authentication**
- [ ] API key created with full scopes
- [ ] API key saved securely
- [ ] Optional: Additional API keys for frontend/functions

✅ **Functions**
- [ ] `scheduled-crawler` function deployed
- [ ] `translate-article` function deployed
- [ ] CRON schedules configured
- [ ] Environment variables set

✅ **Configuration**
- [ ] Local `.env` file updated
- [ ] Backend settings configured
- [ ] Connection tested

✅ **Testing**
- [ ] Database connection verified
- [ ] Test article created
- [ ] Storage upload tested
- [ ] Full crawler run successful

---

**Next Steps:**
1. Start the crawler: `python backend/main.py`
2. Monitor Appwrite console for new articles
3. Build the frontend (Phase 6)
4. Set up continuous deployment

🎉 **Congratulations! Your Appwrite backend is fully configured!**

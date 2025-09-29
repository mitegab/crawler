# Appwrite Setup - Quick Reference

Visual guide and checklists for setting up Appwrite Cloud.

---

## 📋 Setup Checklist

### Phase 1: Account & Project (5 minutes)
```
☐ Create Appwrite Cloud account (https://cloud.appwrite.io)
☐ Verify email address
☐ Create new project: "Tech News Crawler"
☐ Note Project ID: ___________________________
☐ Note Endpoint: https://cloud.appwrite.io/v1

☐ (Optional) Add Web Platform for Frontend:
    ⚠️  BACKEND-ONLY (Python Crawler): Skip this step entirely
    
    🌐 FOR VUE.JS FRONTEND:
    ☐ Go to Settings → Platforms → Add platform
    ☐ Select: Web → Vue
    ☐ Enter Hostname: localhost (exactly, no port!)
        ✅ Correct: localhost
        ❌ Wrong: http://localhost:5173
        ❌ Wrong: localhost:5173
    
    ☐ Clone Vue starter (optional):
        git clone https://github.com/appwrite/starter-for-vue
        cd starter-for-vue
        
    ☐ Configure .env:
        VITE_APPWRITE_PROJECT_ID = "YOUR_PROJECT_ID"
        VITE_APPWRITE_PROJECT_NAME = "crawler"
        VITE_APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"
        
    ☐ Install & run:
        npm install
        npm run dev
        
    ☐ Test connection:
        Open http://localhost:5173
        Click "Send a ping" button
        
    📖 Full guide: docs/VUE_FRONTEND_SETUP.md
```

### Phase 2: Database Setup (15 minutes)
```
☐ Create database: "tech-news-db"
☐ Create collection: "articles" (17 attributes)
    ☐ title_en (String, 500, required)
    ☐ title_am (String, 500)
    ☐ content_en (String, 65535, required)
    ☐ content_am (String, 65535)
    ☐ summary_en (String, 2000)
    ☐ summary_am (String, 2000)
    ☐ source (String, 100, required)
    ☐ source_url (String, 1000, required)
    ☐ author (String, 200)
    ☐ published_date (DateTime)
    ☐ scraped_at (DateTime, required)
    ☐ translated_at (DateTime)
    ☐ category (String, 100)
    ☐ tags (String[])
    ☐ featured_image (String, 1000)
    ☐ images (String[])
    ☐ status (Enum: pending/translating/translated/published/failed/archived)
    ☐ view_count (Integer, default: 0)
    ☐ is_featured (Boolean, default: false)
    ☐ Add indexes (4 indexes)
    ☐ Set permissions

☐ Create collection: "sources" (12 attributes)
    ☐ name (String, 100, required)
    ☐ url (String, 500, required)
    ☐ enabled (Boolean, required, default: true)
    ☐ scraper_class (String, 100, required)
    ☐ selector_config (String, 10000, required)
    ☐ last_crawled (DateTime)
    ☐ crawl_frequency (Integer, required, default: 3600)
    ☐ max_articles (Integer, required, default: 10)
    ☐ category (String, 50)
    ☐ language (String, 10, required, default: "en")
    ☐ priority (Integer, required, default: 1)
    ☐ error_count (Integer, default: 0)
    ☐ status (Enum: active/paused/error/testing)
    ☐ Add indexes (2 indexes)
    ☐ Set permissions
    ☐ Seed with 4 news sources

☐ Create collection: "translations_queue" (10 attributes)
    ☐ article_id (String, 100, required)
    ☐ status (Enum: pending/processing/completed/failed/retrying)
    ☐ retry_count (Integer, required, default: 0)
    ☐ max_retries (Integer, required, default: 3)
    ☐ created_at (DateTime, required)
    ☐ started_at (DateTime)
    ☐ completed_at (DateTime)
    ☐ error_message (String, 1000)
    ☐ translation_service (String, 50, required, default: "google")
    ☐ priority (Integer, required, default: 5)
    ☐ Add indexes (2 indexes)
    ☐ Set permissions
```

### Phase 3: Storage Setup (5 minutes)
```
☐ Create bucket: "article-images"
    ☐ Max file size: 10 MB
    ☐ Allowed extensions: jpg, jpeg, png, gif, webp, svg
    ☐ Enable compression
    ☐ Enable antivirus
    ☐ Set permissions (Read: Anyone, Write: API Key)

☐ Optional buckets:
    ☐ "article-thumbnails" (2 MB)
    ☐ "source-logos" (1 MB)
```

### Phase 4: Authentication & API Keys (5 minutes)
```
☐ Create API key: "Crawler Backend API Key"
    ☐ Expiration: Never (or custom)
    ☐ Scopes:
        ☐ databases.read
        ☐ databases.write
        ☐ collections.read
        ☐ collections.write
        ☐ documents.read
        ☐ documents.write
        ☐ files.read
        ☐ files.write
        ☐ functions.read
        ☐ functions.write
        ☐ execution.read
        ☐ execution.write
    ☐ Copy and save API key: ___________________________

☐ Optional: Create read-only key for frontend
```

### Phase 5: Serverless Functions (20 minutes)
```
☐ Function 1: "scheduled-crawler"
    ☐ Runtime: Python 3.11
    ☐ Trigger: Schedule (0 */3 * * *)
    ☐ Upload code from: backend/appwrite_functions/scheduled_crawler/
    ☐ Set environment variables (11 variables)
    ☐ Test with "Execute Now"
    ☐ Verify articles created in database

☐ Function 2: "translate-article"
    ☐ Runtime: Python 3.11
    ☐ Trigger: Event (databases.*.collections.articles.documents.*.create)
    ☐ Upload code from: backend/appwrite_functions/translate_article/
    ☐ Set environment variables (9 variables)
    ☐ Test by creating article manually
    ☐ Verify translation in article

☐ Optional Function 3: "queue-processor"
    ☐ Runtime: Python 3.11
    ☐ Trigger: Schedule (*/10 * * * *)
    ☐ Create and upload code
    ☐ Set environment variables
```

### Phase 6: Configuration (5 minutes)
```
☐ Update backend/.env file with all IDs and keys
☐ Test connection: python backend/test_appwrite.py
☐ Verify all tests pass
```

### Phase 7: Testing (10 minutes)
```
☐ Run test script: python backend/test_appwrite.py
    ☐ Connection test passes
    ☐ Collections test passes
    ☐ Article creation test passes
    ☐ Storage test passes
    ☐ Sources data check passes

☐ Manual tests:
    ☐ Create test article in console
    ☐ Verify translation function triggers
    ☐ Check article has Amharic translation
    ☐ Upload test image to storage
    ☐ Verify image accessible

☐ Run full crawler: python backend/main.py
    ☐ Articles scraped successfully
    ☐ Images uploaded
    ☐ No errors in logs
```

---

## 🎯 Database Schema Visual

### Collection: `articles`
```
┌─────────────────────────────────────────────┐
│              ARTICLES                        │
├─────────────────────────────────────────────┤
│ • title_en          [String, 500] ✓ req     │
│ • title_am          [String, 500]           │
│ • content_en        [String, 65535] ✓ req   │
│ • content_am        [String, 65535]         │
│ • summary_en        [String, 2000]          │
│ • summary_am        [String, 2000]          │
│ • source            [String, 100] ✓ req     │
│ • source_url        [String, 1000] ✓ req    │
│ • author            [String, 200]           │
│ • published_date    [DateTime]              │
│ • scraped_at        [DateTime] ✓ req        │
│ • translated_at     [DateTime]              │
│ • category          [String, 100]           │
│ • tags              [String[]]              │
│ • featured_image    [String, 1000]          │
│ • images            [String[]]              │
│ • status            [Enum] ✓ req            │
│   ↳ pending, translating, translated,       │
│     published, failed, archived             │
│ • view_count        [Integer] = 0           │
│ • is_featured       [Boolean] = false       │
├─────────────────────────────────────────────┤
│ Indexes:                                    │
│  ⚡ status_scraped (status, scraped_at)     │
│  ⚡ source_date (source, published_date)    │
│  ⚡ category (category)                     │
│  ⚡ featured (is_featured)                  │
└─────────────────────────────────────────────┘
```

### Collection: `sources`
```
┌─────────────────────────────────────────────┐
│               SOURCES                        │
├─────────────────────────────────────────────┤
│ • name              [String, 100] ✓ req     │
│ • url               [String, 500] ✓ req     │
│ • enabled           [Boolean] ✓ req = true  │
│ • scraper_class     [String, 100] ✓ req     │
│ • selector_config   [String, 10000] ✓ req   │
│ • last_crawled      [DateTime]              │
│ • crawl_frequency   [Integer] ✓ req = 3600  │
│ • max_articles      [Integer] ✓ req = 10    │
│ • category          [String, 50]            │
│ • language          [String, 10] ✓ req="en" │
│ • priority          [Integer] ✓ req = 1     │
│ • error_count       [Integer] = 0           │
│ • status            [Enum] ✓ req = active   │
│   ↳ active, paused, error, testing          │
├─────────────────────────────────────────────┤
│ Indexes:                                    │
│  ⚡ enabled_priority (enabled, priority)    │
│  ⚡ status (status)                         │
└─────────────────────────────────────────────┘
```

### Collection: `translations_queue`
```
┌─────────────────────────────────────────────┐
│          TRANSLATIONS_QUEUE                  │
├─────────────────────────────────────────────┤
│ • article_id           [String, 100] ✓ req  │
│ • status               [Enum] ✓ req         │
│   ↳ pending, processing, completed,         │
│     failed, retrying                        │
│ • retry_count          [Integer] ✓ req = 0  │
│ • max_retries          [Integer] ✓ req = 3  │
│ • created_at           [DateTime] ✓ req     │
│ • started_at           [DateTime]           │
│ • completed_at         [DateTime]           │
│ • error_message        [String, 1000]       │
│ • translation_service  [String, 50]="google"│
│ • priority             [Integer] ✓ req = 5  │
├─────────────────────────────────────────────┤
│ Indexes:                                    │
│  ⚡ status_priority (status, priority)      │
│  ⚡ article_status (article_id, status)     │
└─────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    APPWRITE CLOUD                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────┐        │
│  │  FUNCTION: scheduled-crawler                    │        │
│  │  Trigger: CRON (every 3 hours)                 │        │
│  └────────────────┬───────────────────────────────┘        │
│                   │                                          │
│                   │ 1. Scrapes tech news                    │
│                   ▼                                          │
│  ┌────────────────────────────────────────────────┐        │
│  │  COLLECTION: sources                            │        │
│  │  • TechCrunch (enabled, priority: 10)          │        │
│  │  • The Verge (enabled, priority: 9)            │        │
│  │  • Ars Technica (enabled, priority: 8)         │        │
│  │  • Wired (enabled, priority: 7)                │        │
│  └────────────────┬───────────────────────────────┘        │
│                   │                                          │
│                   │ 2. Creates articles                     │
│                   ▼                                          │
│  ┌────────────────────────────────────────────────┐        │
│  │  COLLECTION: articles                           │        │
│  │  • title_en, content_en                        │        │
│  │  • status: "pending"                           │        │
│  └────────────────┬───────────────────────────────┘        │
│                   │                                          │
│                   │ 3. Triggers event                       │
│                   ▼                                          │
│  ┌────────────────────────────────────────────────┐        │
│  │  FUNCTION: translate-article                    │        │
│  │  Trigger: On article create                    │        │
│  └────────────────┬───────────────────────────────┘        │
│                   │                                          │
│                   │ 4. Translates to Amharic                │
│                   ▼                                          │
│  ┌────────────────────────────────────────────────┐        │
│  │  COLLECTION: articles (updated)                 │        │
│  │  • title_am, content_am                        │        │
│  │  • status: "translated"                        │        │
│  └────────────────┬───────────────────────────────┘        │
│                   │                                          │
│                   │ 5. Downloads images                     │
│                   ▼                                          │
│  ┌────────────────────────────────────────────────┐        │
│  │  BUCKET: article-images                         │        │
│  │  • Original images                             │        │
│  │  • Compressed thumbnails                       │        │
│  └────────────────┬───────────────────────────────┘        │
│                   │                                          │
│                   │ 6. Article ready                        │
│                   ▼                                          │
│            ┌──────────────┐                                 │
│            │  Frontend    │                                 │
│            │  (Next.js)   │                                 │
│            └──────────────┘                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔑 Environment Variables Reference

### Backend (.env)
```bash
# === APPWRITE ===
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=                    # From Appwrite console
APPWRITE_API_KEY=                       # Created in Step 4

# === DATABASE ===
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles
APPWRITE_SOURCES_COLLECTION_ID=sources
APPWRITE_QUEUE_COLLECTION_ID=translations_queue

# === STORAGE ===
APPWRITE_STORAGE_BUCKET_ID=article-images

# === TRANSLATION ===
TRANSLATION_SERVICE=google              # google | azure | openai
GOOGLE_TRANSLATE_API_KEY=               # Optional for googletrans
AZURE_TRANSLATOR_KEY=                   # If using Azure
AZURE_TRANSLATOR_REGION=                # If using Azure
OPENAI_API_KEY=                         # If using OpenAI

# === SCRAPING ===
USE_ZYTE=false                          # Enable Zyte API
ZYTE_API_KEY=                           # If using Zyte
MAX_ARTICLES_PER_SOURCE=10              # Articles per scrape
CRAWL_DELAY=2                           # Seconds between requests
REQUEST_TIMEOUT=30                      # Request timeout

# === LOGGING ===
LOG_LEVEL=INFO                          # DEBUG | INFO | WARNING | ERROR
LOG_FILE=logs/crawler.log
```

### Function: scheduled-crawler
```bash
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=
APPWRITE_API_KEY=
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles
APPWRITE_SOURCES_COLLECTION_ID=sources
APPWRITE_STORAGE_BUCKET_ID=article-images
MAX_ARTICLES_PER_SOURCE=10
REQUEST_TIMEOUT=30
USE_ZYTE=false
ZYTE_API_KEY=
LOG_LEVEL=INFO
```

### Function: translate-article
```bash
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=
APPWRITE_API_KEY=
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles
APPWRITE_QUEUE_COLLECTION_ID=translations_queue
TRANSLATION_SERVICE=google
GOOGLE_TRANSLATE_API_KEY=
AZURE_TRANSLATOR_KEY=
AZURE_TRANSLATOR_REGION=
OPENAI_API_KEY=
```

---

## ⚡ Quick Commands

### Test Appwrite Setup
```bash
cd backend
python test_appwrite.py
```

### Run Crawler Locally
```bash
cd backend
python main.py
```

### Check Logs
```bash
tail -f backend/logs/crawler.log
```

### View Output
```bash
cat backend/output/articles.json | jq '.[] | {title: .title_en, source: .source}'
```

### Deploy Function (CLI)
```bash
appwrite deploy function \
  --function-id scheduled-crawler \
  --code backend/appwrite_functions/scheduled_crawler
```

---

## 🆘 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| **"Permission denied"** | Check API key scopes in Appwrite console |
| **"Collection not found"** | Verify collection IDs in .env match console |
| **"Function timeout"** | Increase timeout in function settings (max 900s) |
| **"Translation failed"** | Check translation service API key |
| **"No articles scraped"** | Check sources are enabled in database |
| **"Import error"** | Run `pip install -r requirements.txt` |
| **"Connection refused"** | Check APPWRITE_ENDPOINT is correct |
| **"Invalid API key"** | Regenerate API key in console |

---

## 📊 Expected Results

After complete setup, you should have:

✅ **Database:**
- 3 collections with proper schemas
- 4+ news sources configured and enabled
- Indexes for fast queries

✅ **Storage:**
- 1+ buckets for images
- Proper permissions set

✅ **Functions:**
- 2-3 functions deployed
- Scheduled crawler running every 3 hours
- Translation on article creation

✅ **Testing:**
- All test_appwrite.py tests pass
- Sample articles created
- Translations working

✅ **Monitoring:**
- Function logs accessible
- No critical errors
- Articles appearing in database

---

## 📚 Documentation Links

- **Main Setup Guide**: `docs/APPWRITE_SETUP.md`
- **Functions Guide**: `docs/APPWRITE_FUNCTIONS.md`
- **Quick Start**: `QUICKSTART.md`
- **Project README**: `README.md`

---

## 🎉 Next Steps After Setup

1. ✅ Verify all tests pass
2. 🚀 Run first crawler execution
3. 📝 Check articles in Appwrite console
4. 🌐 Build frontend (Next.js)
5. 📱 Deploy to production
6. 📊 Set up monitoring/analytics

---

**Total Setup Time: ~60 minutes**

**Need help?** Check the detailed guides in the `docs/` folder!

# Appwrite Functions - Detailed Guide

Complete guide to deploying and managing serverless functions for the Tech News Crawler.

---

## Table of Contents
1. [Overview](#overview)
2. [Function 1: Scheduled Crawler](#function-1-scheduled-crawler)
3. [Function 2: Article Translator](#function-2-article-translator)
4. [Function 3: Queue Processor](#function-3-queue-processor)
5. [Deployment Methods](#deployment-methods)
6. [Environment Variables](#environment-variables)
7. [Monitoring & Logs](#monitoring--logs)
8. [Troubleshooting](#troubleshooting)

---

## Overview

### What are Appwrite Functions?
Appwrite Functions are serverless functions that run on Appwrite Cloud. They can be:
- **Scheduled** (CRON jobs) - Run at specific intervals
- **Event-driven** - Triggered by database/storage events
- **On-demand** - Called via API

### Benefits for This Project
- ✅ **Automated scraping** - No need to manually run crawler
- ✅ **Event-driven translation** - Auto-translate new articles
- ✅ **Scalable** - Handles high traffic automatically
- ✅ **Cost-effective** - Only pay for execution time
- ✅ **No server management** - Fully managed by Appwrite

### Architecture
```
┌─────────────────────────────────────────────────────┐
│                  Appwrite Functions                  │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────┐    ┌──────────────────┐     │
│  │ Scheduled        │    │ Event-Driven     │     │
│  │ Crawler          │    │ Translator       │     │
│  │                  │    │                  │     │
│  │ Runs every 3hrs  │    │ On article create│     │
│  │ Scrapes news     │───▶│ Translates text  │     │
│  │ Saves to DB      │    │ Updates article  │     │
│  └──────────────────┘    └──────────────────┘     │
│           │                       │                 │
│           ▼                       ▼                 │
│  ┌────────────────────────────────────────┐        │
│  │      Appwrite Database & Storage       │        │
│  └────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

---

## Function 1: Scheduled Crawler

### Purpose
Automatically scrapes tech news from configured sources every 3 hours.

### Configuration

**Function Details:**
- **Function ID**: `scheduled-crawler`
- **Name**: Scheduled News Crawler
- **Runtime**: Python 3.11
- **Entry Point**: `main.py`
- **Trigger**: Schedule (CRON)

**CRON Schedule Options:**

| Schedule | CRON Expression | Description |
|----------|----------------|-------------|
| Every 3 hours | `0 */3 * * *` | Recommended for production |
| Every hour | `0 * * * *` | For testing/high-frequency sites |
| Every 6 hours | `0 */6 * * *` | For low-traffic sites |
| Daily at 9 AM | `0 9 * * *` | Once per day |
| Every 30 mins | `*/30 * * * *` | Testing only |

### Code Structure

**File: `backend/appwrite_functions/scheduled_crawler/main.py`**

```python
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
import os
import sys

# Import your scraper logic
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
from scrapers import run_all_scrapers  # Your scraper code


def main(req, res):
    """
    Main function called by Appwrite
    
    Args:
        req: Request object
        res: Response object
    """
    try:
        # Initialize Appwrite client
        client = Client()
        client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
        client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
        client.set_key(os.getenv('APPWRITE_API_KEY'))
        
        databases = Databases(client)
        
        # Get enabled sources from database
        sources = databases.list_documents(
            database_id=os.getenv('APPWRITE_DATABASE_ID'),
            collection_id=os.getenv('APPWRITE_SOURCES_COLLECTION_ID'),
            queries=[
                Query.equal('enabled', True),
                Query.order_desc('priority')
            ]
        )
        
        # Run scrapers for each source
        results = {
            'total_sources': sources['total'],
            'articles_scraped': 0,
            'sources_processed': [],
            'errors': []
        }
        
        for source in sources['documents']:
            try:
                # Scrape articles from this source
                articles = scrape_source(source)
                
                # Save articles to database
                for article in articles:
                    save_article(databases, article)
                    results['articles_scraped'] += 1
                
                results['sources_processed'].append({
                    'name': source['name'],
                    'articles': len(articles),
                    'status': 'success'
                })
                
                # Update last_crawled timestamp
                databases.update_document(
                    database_id=os.getenv('APPWRITE_DATABASE_ID'),
                    collection_id=os.getenv('APPWRITE_SOURCES_COLLECTION_ID'),
                    document_id=source['$id'],
                    data={'last_crawled': datetime.now().isoformat()}
                )
                
            except Exception as e:
                results['errors'].append({
                    'source': source['name'],
                    'error': str(e)
                })
        
        return res.json({
            'success': True,
            'message': f"Scraped {results['articles_scraped']} articles from {len(results['sources_processed'])} sources",
            'results': results
        })
        
    except Exception as e:
        return res.json({
            'success': False,
            'error': str(e)
        }, 500)
```

### Deployment Steps

#### Method 1: Manual Upload

1. **Prepare deployment package:**
```bash
cd backend/appwrite_functions/scheduled_crawler
zip -r function.zip . -x "*.git*" -x "*__pycache__*"
```

2. **Upload to Appwrite:**
   - Go to Functions → scheduled-crawler
   - Click "Deploy Function"
   - Upload `function.zip`
   - Wait for build to complete

3. **Activate deployment:**
   - Once build succeeds, click "Activate"

#### Method 2: Git Integration

1. **Connect Git repository:**
   - In function settings, click "Connect Git"
   - Authorize GitHub
   - Select your repository
   - Set root directory: `backend/appwrite_functions/scheduled_crawler`
   - Set production branch: `main`

2. **Enable auto-deploy:**
   - Toggle "Automatic Deployments"
   - Now deploys on every push to main

### Environment Variables

Set these in Function Settings → Environment Variables:

```bash
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id
APPWRITE_API_KEY=your-api-key
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles
APPWRITE_SOURCES_COLLECTION_ID=sources
APPWRITE_STORAGE_BUCKET_ID=article-images

# Scraping Configuration
MAX_ARTICLES_PER_SOURCE=10
REQUEST_TIMEOUT=30
USER_AGENT=Mozilla/5.0 (Tech News Crawler)

# Zyte (optional)
USE_ZYTE=false
ZYTE_API_KEY=

# Logging
LOG_LEVEL=INFO
```

### Testing

**Manual Execution:**
1. Go to function page
2. Click "Execute Now"
3. View logs in real-time
4. Check results in Response tab

**Verify Results:**
```bash
# Check articles were created
# Go to Databases → articles → View documents
# Should see new articles with recent scraped_at timestamp
```

---

## Function 2: Article Translator

### Purpose
Automatically translates articles to Amharic when they're created.

### Configuration

**Function Details:**
- **Function ID**: `translate-article`
- **Name**: Article Translation Service
- **Runtime**: Python 3.11
- **Entry Point**: `main.py`
- **Trigger**: Event

**Event Configuration:**
- **Event**: `databases.*.collections.articles.documents.*.create`
- This triggers whenever a new article is created

### Code Structure

**File: `backend/appwrite_functions/translate_article/main.py`**

```python
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID
import os
from datetime import datetime

# Import translation logic
from translators.translator import Translator


def main(req, res):
    """
    Translates an article when it's created
    
    Triggered by: Article creation event
    """
    try:
        # Get article ID from event
        article_id = req.variables.get('APPWRITE_FUNCTION_EVENT_DATA', {}).get('$id')
        
        if not article_id:
            return res.json({
                'success': False,
                'error': 'No article ID provided'
            }, 400)
        
        # Initialize Appwrite
        client = Client()
        client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
        client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
        client.set_key(os.getenv('APPWRITE_API_KEY'))
        
        databases = Databases(client)
        
        # Get article
        article = databases.get_document(
            database_id=os.getenv('APPWRITE_DATABASE_ID'),
            collection_id=os.getenv('APPWRITE_ARTICLES_COLLECTION_ID'),
            document_id=article_id
        )
        
        # Check if already translated
        if article.get('title_am') or article.get('status') == 'translated':
            return res.json({
                'success': True,
                'message': 'Article already translated',
                'article_id': article_id
            })
        
        # Update status to translating
        databases.update_document(
            database_id=os.getenv('APPWRITE_DATABASE_ID'),
            collection_id=os.getenv('APPWRITE_ARTICLES_COLLECTION_ID'),
            document_id=article_id,
            data={'status': 'translating'}
        )
        
        # Translate
        translator = Translator()
        
        translated_title = translator.translate_text(
            article['title_en'],
            source='en',
            target='am'
        )
        
        translated_content = translator.translate_text(
            article['content_en'],
            source='en',
            target='am'
        )
        
        translated_summary = None
        if article.get('summary_en'):
            translated_summary = translator.translate_text(
                article['summary_en'],
                source='en',
                target='am'
            )
        
        # Update article with translations
        databases.update_document(
            database_id=os.getenv('APPWRITE_DATABASE_ID'),
            collection_id=os.getenv('APPWRITE_ARTICLES_COLLECTION_ID'),
            document_id=article_id,
            data={
                'title_am': translated_title,
                'content_am': translated_content,
                'summary_am': translated_summary,
                'translated_at': datetime.now().isoformat(),
                'status': 'translated'
            }
        )
        
        return res.json({
            'success': True,
            'message': 'Article translated successfully',
            'article_id': article_id,
            'title': translated_title[:100]  # First 100 chars
        })
        
    except Exception as e:
        # Mark as failed
        try:
            databases.update_document(
                database_id=os.getenv('APPWRITE_DATABASE_ID'),
                collection_id=os.getenv('APPWRITE_ARTICLES_COLLECTION_ID'),
                document_id=article_id,
                data={'status': 'failed'}
            )
        except:
            pass
        
        return res.json({
            'success': False,
            'error': str(e),
            'article_id': article_id
        }, 500)
```

### Deployment

Same as Scheduled Crawler:
1. Prepare code in `backend/appwrite_functions/translate_article/`
2. Upload manually or connect Git
3. Set environment variables
4. Test by creating an article manually

### Environment Variables

```bash
# Appwrite
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your-project-id
APPWRITE_API_KEY=your-api-key
APPWRITE_DATABASE_ID=tech-news-db
APPWRITE_ARTICLES_COLLECTION_ID=articles

# Translation Services
TRANSLATION_SERVICE=google
GOOGLE_TRANSLATE_API_KEY=  # optional
AZURE_TRANSLATOR_KEY=
AZURE_TRANSLATOR_REGION=
OPENAI_API_KEY=

# Settings
MAX_TEXT_LENGTH=5000
CHUNK_SIZE=4500
```

---

## Function 3: Queue Processor

### Purpose
Processes translation queue for async/batch translation.

### When to Use
- High article volume
- Want to rate-limit API calls
- Need retry logic for failed translations

### Configuration

**Function Details:**
- **Function ID**: `queue-processor`
- **Name**: Translation Queue Processor
- **Runtime**: Python 3.11
- **Trigger**: Schedule
- **CRON**: `*/10 * * * *` (every 10 minutes)

### Code

Create: `backend/appwrite_functions/queue_processor/main.py`

```python
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.query import Query
from datetime import datetime
import os

def main(req, res):
    """Process translation queue"""
    try:
        client = Client()
        client.set_endpoint(os.getenv('APPWRITE_ENDPOINT'))
        client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
        client.set_key(os.getenv('APPWRITE_API_KEY'))
        
        databases = Databases(client)
        
        # Get pending items from queue
        queue_items = databases.list_documents(
            database_id=os.getenv('APPWRITE_DATABASE_ID'),
            collection_id=os.getenv('APPWRITE_QUEUE_COLLECTION_ID'),
            queries=[
                Query.equal('status', 'pending'),
                Query.less_than('retry_count', 3),  # Max 3 retries
                Query.order_desc('priority'),
                Query.limit(10)  # Process 10 at a time
            ]
        )
        
        processed = 0
        failed = 0
        
        for item in queue_items['documents']:
            try:
                # Update status
                databases.update_document(
                    database_id=os.getenv('APPWRITE_DATABASE_ID'),
                    collection_id=os.getenv('APPWRITE_QUEUE_COLLECTION_ID'),
                    document_id=item['$id'],
                    data={
                        'status': 'processing',
                        'started_at': datetime.now().isoformat()
                    }
                )
                
                # Get article
                article = databases.get_document(
                    database_id=os.getenv('APPWRITE_DATABASE_ID'),
                    collection_id=os.getenv('APPWRITE_ARTICLES_COLLECTION_ID'),
                    document_id=item['article_id']
                )
                
                # Translate (call your translation logic)
                # ...
                
                # Update queue item as completed
                databases.update_document(
                    database_id=os.getenv('APPWRITE_DATABASE_ID'),
                    collection_id=os.getenv('APPWRITE_QUEUE_COLLECTION_ID'),
                    document_id=item['$id'],
                    data={
                        'status': 'completed',
                        'completed_at': datetime.now().isoformat()
                    }
                )
                
                processed += 1
                
            except Exception as e:
                # Update retry count
                databases.update_document(
                    database_id=os.getenv('APPWRITE_DATABASE_ID'),
                    collection_id=os.getenv('APPWRITE_QUEUE_COLLECTION_ID'),
                    document_id=item['$id'],
                    data={
                        'status': 'retrying' if item['retry_count'] < 2 else 'failed',
                        'retry_count': item['retry_count'] + 1,
                        'error_message': str(e)
                    }
                )
                failed += 1
        
        return res.json({
            'success': True,
            'processed': processed,
            'failed': failed,
            'total': queue_items['total']
        })
        
    except Exception as e:
        return res.json({
            'success': False,
            'error': str(e)
        }, 500)
```

---

## Deployment Methods

### Option 1: Appwrite CLI

```bash
# Install Appwrite CLI
npm install -g appwrite-cli

# Login
appwrite login

# Initialize
appwrite init function

# Deploy
appwrite deploy function \
  --function-id scheduled-crawler \
  --code backend/appwrite_functions/scheduled_crawler
```

### Option 2: GitHub Actions

Create `.github/workflows/deploy-functions.yml`:

```yaml
name: Deploy Appwrite Functions

on:
  push:
    branches: [main]
    paths:
      - 'backend/appwrite_functions/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install Appwrite CLI
        run: npm install -g appwrite-cli
      
      - name: Deploy Functions
        env:
          APPWRITE_ENDPOINT: ${{ secrets.APPWRITE_ENDPOINT }}
          APPWRITE_PROJECT_ID: ${{ secrets.APPWRITE_PROJECT_ID }}
          APPWRITE_API_KEY: ${{ secrets.APPWRITE_API_KEY }}
        run: |
          appwrite deploy function \
            --function-id scheduled-crawler \
            --code backend/appwrite_functions/scheduled_crawler
```

---

## Monitoring & Logs

### Viewing Logs

1. **Real-time logs:**
   - Go to Functions → [function-name] → Executions
   - Click on any execution
   - View logs in real-time

2. **Log levels:**
   ```python
   print("INFO: Starting scraper")  # Info
   print("ERROR: Failed to scrape", file=sys.stderr)  # Error
   ```

3. **Structured logging:**
   ```python
   import json
   
   log = {
       'level': 'INFO',
       'message': 'Scraped articles',
       'count': 10,
       'source': 'TechCrunch'
   }
   print(json.dumps(log))
   ```

### Monitoring Dashboard

**Key Metrics:**
- Execution count
- Success rate
- Average execution time
- Error rate

**Set up alerts:**
1. Go to function settings
2. Click "Webhooks"
3. Add webhook for errors
4. Send to Slack/Discord/Email

---

## Troubleshooting

### Common Issues

**Function times out:**
- Increase timeout in function settings
- Optimize code (reduce API calls)
- Process fewer items per execution

**Out of memory:**
- Reduce batch size
- Free memory explicitly: `del large_object`
- Use streaming for large files

**Module not found:**
- Check `requirements.txt` includes all dependencies
- Ensure correct Python version
- Rebuild function

**Environment variable not set:**
- Double-check variable names
- Ensure no typos
- Check if variable is marked as "Secret"

### Debugging Tips

1. **Add verbose logging:**
   ```python
   print(f"DEBUG: Processing article {article_id}")
   print(f"DEBUG: Article data: {article}")
   ```

2. **Test locally first:**
   ```bash
   cd backend/appwrite_functions/scheduled_crawler
   python main.py
   ```

3. **Use try-except blocks:**
   ```python
   try:
       # risky code
   except Exception as e:
       print(f"ERROR: {str(e)}", file=sys.stderr)
       raise  # Re-raise to mark execution as failed
   ```

---

## Best Practices

1. **Keep functions small** - One function = one task
2. **Use environment variables** - Never hardcode secrets
3. **Add error handling** - Always catch exceptions
4. **Log everything** - Makes debugging easier
5. **Test before deploying** - Use "Execute Now" button
6. **Version your code** - Use Git tags for versions
7. **Monitor regularly** - Check logs weekly
8. **Set up alerts** - Know when things break

---

## Next Steps

1. Deploy all three functions
2. Test each function individually
3. Monitor execution logs
4. Optimize based on performance
5. Set up error notifications
6. Configure production schedules

🚀 **Happy Function Deployment!**

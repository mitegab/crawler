# Zyte Integration Guide

## 🔑 Getting Your Zyte API Key

The key you provided (`60bb85ab9bba4034b4ddb5c4f83f936b`) is your **Scrapy Cloud deployment key**, not the Zyte API key.

### Steps to Get the Correct API Key:

1. **Go to Zyte Dashboard:**
   - Visit: https://app.zyte.com/

2. **Navigate to API Access:**
   - Click on your account name (top right)
   - Select "API Access" or "Settings" → "API Access"
   - OR visit directly: https://app.zyte.com/account/apikey

3. **Copy Your Zyte API Key:**
   - You should see a field labeled "Zyte API Key" or "API Key"
   - Copy this key (it's different from the Scrapy Cloud key)

4. **Update .env File:**
   ```bash
   ZYTE_API_KEY=your_actual_zyte_api_key_here
   USE_ZYTE=true
   ```

## 📋 Zyte Products Available

Your Zyte Pro plan may include different products:

### 1. **Zyte API** (Recommended for this project)
   - Modern API for web scraping
   - Automatic browser rendering
   - Anti-bot bypass
   - Usage: `https://api.zyte.com/v1/extract`

### 2. **Smart Proxy Manager** (formerly Crawlera)
   - Rotating proxy service
   - Works as HTTP proxy
   - Good for distributed scraping

### 3. **Scrapy Cloud**
   - Cloud-based Scrapy deployment
   - For running Scrapy spiders
   - Not applicable for our current setup

### 4. **Automatic Extraction**
   - AI-powered data extraction
   - Pre-trained extractors
   - Higher cost per request

## 🛠️ Current Implementation

Our code currently uses **Zyte API** method. Once you have the correct API key:

1. Update `.env`:
   ```bash
   ZYTE_API_KEY=<your_real_zyte_api_key>
   USE_ZYTE=true
   ```

2. Test the integration:
   ```bash
   cd /home/ethiopique/Downloads/os/crawler
   /bin/python backend/test_zyte.py
   ```

3. Run the crawler with Zyte:
   ```bash
   cd backend && /bin/python main.py
   ```

## 💡 Alternative: Use Smart Proxy Manager

If you have Smart Proxy Manager instead of Zyte API:

1. Get your Smart Proxy credentials from: https://app.zyte.com/p/828589/proxy

2. The credentials format is: `<username>:<password>`

3. I can update the code to use Smart Proxy Manager instead of Zyte API

## ❓ Which Product Do You Have?

To check which Zyte products are available in your plan:

1. Visit: https://app.zyte.com/p/828589/
2. Look at the sidebar menu - you should see:
   - **Zyte API** - Click to get API key
   - **Smart Proxy** - Click to get proxy credentials
   - **Scrapy Cloud** - For deploying Scrapy projects
   - **Automatic Extraction** - AI extraction service

## 🔄 Next Steps

**Option A: If you have Zyte API access**
- Get the API key from https://app.zyte.com/account/apikey
- Update the ZYTE_API_KEY in .env
- Current code will work

**Option B: If you only have Smart Proxy Manager**
- Get proxy credentials from Zyte dashboard
- I'll update the code to use proxy mode instead
- Provide credentials in format: `username:password`

**Option C: Skip Zyte for now**
- Set `USE_ZYTE=false` in .env
- Use direct requests (may face rate limiting/blocking)
- Focus on getting scrapers working first

## 📞 Need Help?

Let me know:
1. Which Zyte products you see in your dashboard
2. Or share a screenshot of your Zyte dashboard menu (hide sensitive info)
3. And I'll configure the correct integration method

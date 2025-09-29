# Vue.js Frontend Setup for Tech News Crawler

Complete guide to building the Vue.js frontend for your Amharic tech news website using Appwrite.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Appwrite Web Platform Setup](#appwrite-web-platform-setup)
3. [Vue.js Project Setup](#vuejs-project-setup)
4. [Configure Environment](#configure-environment)
5. [Appwrite Integration](#appwrite-integration)
6. [Building Components](#building-components)
7. [Running & Testing](#running--testing)
8. [Deployment](#deployment)

---

## 🔧 Prerequisites

### Required Software
- **Node.js**: v18.0.0 or higher
- **npm**: v9.0.0 or higher
- **Git**: Latest version

### Check Versions
```bash
node --version    # Should be v18+
npm --version     # Should be v9+
git --version
```

### Appwrite Requirements
- ✅ Appwrite Cloud account created
- ✅ Project created ("Tech News Crawler")
- ✅ Database and collections set up
- ✅ Storage bucket configured
- ✅ API keys created (for backend)

---

## 🌐 Appwrite Web Platform Setup

### Step 1: Add Web Platform in Appwrite Console

1. **Navigate to Platforms**
   ```
   Appwrite Console → Your Project → Settings → Platforms
   ```

2. **Click "Add platform"**

3. **Select Platform Type**
   - Choose: **"Web"**

4. **Select Framework**
   - Choose: **"Vue"** from the dropdown

5. **Configure Platform Details**

   **Clone starter (Optional)**
   
   If you're starting a new project, you can clone the Appwrite Vue starter kit from GitHub:

   ```bash
   git clone https://github.com/appwrite/starter-for-vue
   cd starter-for-vue
   ```

   **Platform Configuration:**
   ```
   Name: Tech News Frontend
   Hostname: localhost
   ```

   ⚠️ **CRITICAL - Hostname Format:**
   ```
   ✅ CORRECT:   localhost
   ❌ WRONG:     http://localhost:5173
   ❌ WRONG:     localhost:5173
   ❌ WRONG:     https://localhost
   ```

   **Why just "localhost"?**
   - The port (`:5173`) is automatically handled
   - Protocol (`http://`) is not part of hostname
   - Appwrite adds these automatically

6. **Click "Create"** to save the platform

### Step 2: Verify Platform Configuration

Your platform should appear in the list:

```
✓ Tech News Frontend
  Type: Vue
  Hostname: localhost
  Status: Active
```

### Step 3: Add Production Platform (When Ready)

When deploying to production, add another platform:

```
Name: Tech News Frontend (Production)
Type: Vue
Hostname: yourdomain.com
```

Or for Vercel/Netlify:
```
Hostname: yourapp.vercel.app
Hostname: yourapp.netlify.app
```

---

## 🚀 Vue.js Project Setup

### Option A: Use Appwrite Starter Template (Recommended for Beginners)

This is the easiest way to get started with Appwrite and Vue.js.

#### 1. Clone the Starter Kit

```bash
# Clone from GitHub
git clone https://github.com/appwrite/starter-for-vue tech-news-frontend
cd tech-news-frontend
```

#### 2. Copy Environment File

```bash
# Copy the example environment file
cp .env.example .env
```

#### 3. Update Configuration Settings

Edit the `.env` file and update with your Appwrite credentials:

```dotenv
VITE_APPWRITE_PROJECT_ID = "68daf772003b1b1f5c78"
VITE_APPWRITE_PROJECT_NAME = "crawler"
VITE_APPWRITE_ENDPOINT = "https://cloud.appwrite.io/v1"
```

**Replace the values:**
- `VITE_APPWRITE_PROJECT_ID`: Your actual Project ID from Appwrite Console
- `VITE_APPWRITE_PROJECT_NAME`: "crawler" (or your project name)
- `VITE_APPWRITE_ENDPOINT`: 
  - US/Global: `https://cloud.appwrite.io/v1`
  - NYC: `https://nyc.cloud.appwrite.io/v1`
  - EU: `https://eu.cloud.appwrite.io/v1`

**How to find your Project ID:**
```
Appwrite Console → Your Project → Settings → Project ID
```

#### 4. Install Project Dependencies

```bash
npm install
```

This will install:
- Vue 3
- Vite (build tool)
- Appwrite SDK
- Vue Router
- Other dependencies

#### 5. Run the App

```bash
npm run dev
```

**Demo app runs on:** `http://localhost:5173`

#### 6. Verify the Setup

1. Open your browser and navigate to: `http://localhost:5173`
2. Click the **"Send a ping"** button to verify the Appwrite connection
3. If successful, you'll see a confirmation message

**Expected output:**
```
✓ Connected to Appwrite successfully!
Project: crawler
Endpoint: https://cloud.appwrite.io/v1
```

---

### Option B: Create Custom Vue Project (Advanced)

If you want to build from scratch or integrate into existing project:

#### 1. Create New Vite + Vue Project

```bash
npm create vite@latest tech-news-frontend -- --template vue
cd tech-news-frontend
```

#### 2. Install Dependencies

```bash
# Install core dependencies
npm install

# Install Appwrite SDK
npm install appwrite

# Install additional packages (optional)
npm install @vueuse/core vue-router pinia
```

#### 3. Create Environment File

Create `.env` in project root:

```dotenv
VITE_APPWRITE_PROJECT_ID=68daf772003b1b1f5c78
VITE_APPWRITE_PROJECT_NAME=crawler
VITE_APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
VITE_APPWRITE_DATABASE_ID=tech-news-db
VITE_APPWRITE_ARTICLES_COLLECTION_ID=articles
VITE_APPWRITE_SOURCES_COLLECTION_ID=sources
VITE_APPWRITE_STORAGE_BUCKET_ID=article-images
```

#### 4. Setup Appwrite Client

Create `src/lib/appwrite.js`:

```javascript
import { Client, Databases, Storage, Query } from 'appwrite';

// Initialize Appwrite Client
const client = new Client()
    .setEndpoint(import.meta.env.VITE_APPWRITE_ENDPOINT)
    .setProject(import.meta.env.VITE_APPWRITE_PROJECT_ID);

// Initialize services
export const databases = new Databases(client);
export const storage = new Storage(client);

// Export Query helper
export { Query };

// Configuration
export const config = {
    databaseId: import.meta.env.VITE_APPWRITE_DATABASE_ID,
    articlesCollectionId: import.meta.env.VITE_APPWRITE_ARTICLES_COLLECTION_ID,
    sourcesCollectionId: import.meta.env.VITE_APPWRITE_SOURCES_COLLECTION_ID,
    storageBucketId: import.meta.env.VITE_APPWRITE_STORAGE_BUCKET_ID
};

export default client;
```

---

## 📁 Project Structure

```
tech-news-frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/
│   │   ├── logo.svg
│   │   └── styles/
│   │       └── main.css
│   ├── components/
│   │   ├── ArticleCard.vue          # Single article card
│   │   ├── ArticleList.vue          # List of articles
│   │   ├── FeaturedArticle.vue      # Hero section
│   │   ├── CategoryFilter.vue       # Category selector
│   │   ├── SearchBar.vue            # Search component
│   │   ├── LanguageToggle.vue       # EN/AM toggle
│   │   └── LoadingSpinner.vue       # Loading state
│   ├── views/
│   │   ├── HomeView.vue             # Homepage
│   │   ├── ArticleView.vue          # Single article page
│   │   ├── CategoryView.vue         # Category page
│   │   └── AboutView.vue            # About page
│   ├── composables/
│   │   ├── useAppwrite.js           # Appwrite client
│   │   ├── useArticles.js           # Article fetching
│   │   └── useLanguage.js           # Language switching
│   ├── router/
│   │   └── index.js                 # Vue Router config
│   ├── stores/
│   │   ├── articles.js              # Pinia store
│   │   └── language.js              # Language state
│   ├── lib/
│   │   └── appwrite.js              # Appwrite setup
│   ├── App.vue                      # Root component
│   └── main.js                      # Entry point
├── .env                             # Environment variables (IMPORTANT!)
├── .env.example                     # Example env file
├── .gitignore
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

---

## 🔌 Appwrite Integration

### 1. Create Articles Composable

**`src/composables/useArticles.js`**

```javascript
import { ref } from 'vue';
import { databases, storage, Query, config } from '@/lib/appwrite';

export function useArticles() {
    const articles = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const currentLanguage = ref('am'); // 'en' or 'am'

    // Fetch latest articles
    const fetchArticles = async (limit = 20, category = null) => {
        loading.value = true;
        error.value = null;
        
        try {
            const queries = [
                Query.equal('status', 'translated'),
                Query.orderDesc('published_date'),
                Query.limit(limit)
            ];

            if (category) {
                queries.push(Query.equal('category', category));
            }

            const response = await databases.listDocuments(
                config.databaseId,
                config.articlesCollectionId,
                queries
            );

            articles.value = response.documents;
            return response.documents;
        } catch (err) {
            error.value = err.message;
            console.error('Error fetching articles:', err);
            return [];
        } finally {
            loading.value = false;
        }
    };

    // Fetch single article by ID
    const fetchArticle = async (articleId) => {
        loading.value = true;
        error.value = null;

        try {
            const article = await databases.getDocument(
                config.databaseId,
                config.articlesCollectionId,
                articleId
            );

            // Increment view count
            await databases.updateDocument(
                config.databaseId,
                config.articlesCollectionId,
                articleId,
                {
                    view_count: (article.view_count || 0) + 1
                }
            );

            return article;
        } catch (err) {
            error.value = err.message;
            console.error('Error fetching article:', err);
            return null;
        } finally {
            loading.value = false;
        }
    };

    // Get image URL from storage
    const getImageUrl = (fileId) => {
        if (!fileId) return null;
        
        return storage.getFilePreview(
            config.storageBucketId,
            fileId,
            800,      // width
            0,        // height (auto)
            'center', // gravity
            85,       // quality
            0,        // border width
            '000000', // border color
            0,        // border radius
            1,        // opacity
            0,        // rotation
            'FFFFFF', // background
            'webp'    // output format
        );
    };

    // Get article title in current language
    const getTitle = (article) => {
        return currentLanguage.value === 'am' 
            ? article.title_am || article.title_en
            : article.title_en;
    };

    // Get article content in current language
    const getContent = (article) => {
        return currentLanguage.value === 'am'
            ? article.content_am || article.content_en
            : article.content_en;
    };

    // Get article summary in current language
    const getSummary = (article) => {
        return currentLanguage.value === 'am'
            ? article.summary_am || article.summary_en
            : article.summary_en;
    };

    return {
        articles,
        loading,
        error,
        currentLanguage,
        fetchArticles,
        fetchArticle,
        getImageUrl,
        getTitle,
        getContent,
        getSummary
    };
}
```

### 2. Create Language Composable

**`src/composables/useLanguage.js`**

```javascript
import { ref, watch } from 'vue';

export function useLanguage() {
    const currentLanguage = ref(
        localStorage.getItem('language') || 'am'
    );

    const toggleLanguage = () => {
        currentLanguage.value = currentLanguage.value === 'en' ? 'am' : 'en';
    };

    const setLanguage = (lang) => {
        if (['en', 'am'].includes(lang)) {
            currentLanguage.value = lang;
        }
    };

    // Save to localStorage on change
    watch(currentLanguage, (newLang) => {
        localStorage.setItem('language', newLang);
    });

    return {
        currentLanguage,
        toggleLanguage,
        setLanguage
    };
}
```

---

## 🎨 Building Components

### 1. Language Toggle Component

**`src/components/LanguageToggle.vue`**

```vue
<template>
  <div class="language-toggle">
    <button 
      @click="toggleLanguage" 
      class="toggle-btn"
      :aria-label="`Switch to ${currentLanguage === 'en' ? 'Amharic' : 'English'}`"
    >
      <span :class="{ active: currentLanguage === 'en' }">EN</span>
      <span class="separator">|</span>
      <span :class="{ active: currentLanguage === 'am' }">አማ</span>
    </button>
  </div>
</template>

<script setup>
import { useLanguage } from '@/composables/useLanguage';

const { currentLanguage, toggleLanguage } = useLanguage();
</script>

<style scoped>
.language-toggle {
  display: flex;
  align-items: center;
}

.toggle-btn {
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  gap: 0.5rem;
  align-items: center;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.toggle-btn:hover {
  background: #e5e7eb;
}

.toggle-btn span {
  color: #9ca3af;
  transition: color 0.3s;
}

.toggle-btn span.active {
  color: #4f46e5;
  font-weight: 600;
}

.separator {
  color: #d1d5db;
}
</style>
```

### 2. Article Card Component

**`src/components/ArticleCard.vue`**

```vue
<template>
  <article class="article-card">
    <router-link :to="`/article/${article.$id}`" class="article-link">
      <!-- Featured Image -->
      <div class="article-image">
        <img 
          v-if="article.featured_image" 
          :src="getImageUrl(article.featured_image)"
          :alt="getTitle(article)"
          loading="lazy"
        />
        <div v-else class="placeholder-image">
          <span>{{ article.source }}</span>
        </div>
      </div>

      <!-- Content -->
      <div class="article-content">
        <!-- Category Badge -->
        <span v-if="article.category" class="category-badge">
          {{ article.category }}
        </span>

        <!-- Title -->
        <h3 class="article-title">
          {{ getTitle(article) }}
        </h3>

        <!-- Summary -->
        <p class="article-summary">
          {{ getSummary(article) }}
        </p>

        <!-- Metadata -->
        <div class="article-meta">
          <span class="source">{{ article.source }}</span>
          <span class="separator">•</span>
          <time :datetime="article.published_date">
            {{ formatDate(article.published_date) }}
          </time>
          <span class="separator">•</span>
          <span class="views">{{ article.view_count || 0 }} views</span>
        </div>
      </div>
    </router-link>
  </article>
</template>

<script setup>
import { useArticles } from '@/composables/useArticles';

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
});

const { getImageUrl, getTitle, getSummary } = useArticles();

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('am-ET', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
};
</script>

<style scoped>
.article-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.article-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.article-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f0f0f0;
}

.article-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.article-content {
  padding: 1.5rem;
}

.category-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #e0e7ff;
  color: #4f46e5;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
}

.article-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
  color: #1a1a1a;
}

.article-summary {
  font-size: 0.95rem;
  color: #666;
  margin: 0 0 1rem 0;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #999;
  flex-wrap: wrap;
}

.separator {
  color: #ddd;
}

.source {
  font-weight: 600;
  color: #666;
}
</style>
```

### 3. Article List Component

**`src/components/ArticleList.vue`**

```vue
<template>
  <div class="article-list">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading articles...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>⚠️ Error loading articles: {{ error }}</p>
      <button @click="retry" class="retry-btn">Retry</button>
    </div>

    <!-- Articles Grid -->
    <div v-else-if="articles.length > 0" class="articles-grid">
      <ArticleCard 
        v-for="article in articles" 
        :key="article.$id" 
        :article="article"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <p>📰 No articles found</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useArticles } from '@/composables/useArticles';
import ArticleCard from './ArticleCard.vue';

const props = defineProps({
  category: {
    type: String,
    default: null
  },
  limit: {
    type: Number,
    default: 20
  }
});

const { articles, loading, error, fetchArticles } = useArticles();

const loadArticles = () => {
  fetchArticles(props.limit, props.category);
};

const retry = () => {
  loadArticles();
};

onMounted(() => {
  loadArticles();
});
</script>

<style scoped>
.article-list {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
}

@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
  }
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #4f46e5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.retry-btn:hover {
  background: #4338ca;
}
</style>
```

---

## 🏃 Running & Testing

### Start Development Server

```bash
npm run dev
```

**Output:**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### Testing Connection

1. **Open Browser**: Navigate to `http://localhost:5173`

2. **Test Appwrite Connection**:
   - Click "Send a ping" button (if using starter template)
   - Or check browser console for connection status

3. **Verify in Browser Console (F12)**:
   ```javascript
   // Should see no CORS errors
   ✓ Connected to Appwrite
   ✓ Articles loaded successfully
   ```

4. **Test Articles Display**:
   - Articles should load from Appwrite database
   - Images should display from Appwrite storage
   - Language toggle should work (EN ↔ አማ)

### Common Issues & Solutions

#### Issue: CORS Error

```
Access to fetch at 'https://cloud.appwrite.io/v1' from origin 'http://localhost:5173' 
has been blocked by CORS policy
```

**Solution:**
1. Go to Appwrite Console → Settings → Platforms
2. Verify hostname is exactly: `localhost` (not `localhost:5173`)
3. Remove and re-add platform if needed

#### Issue: Articles Not Loading

**Solution:**
1. Check `.env` file has correct Project ID
2. Verify database and collection IDs
3. Check collection permissions (Read: Anyone)
4. Check browser console for errors

#### Issue: Images Not Displaying

**Solution:**
1. Check storage bucket permissions (Read: Anyone)
2. Verify `featured_image` field has valid file ID
3. Check CORS settings for storage bucket

---

## 📦 Building for Production

### Build Command

```bash
# Create production build
npm run build
```

**Output:**
```
dist/
├── assets/
│   ├── index-[hash].js
│   └── index-[hash].css
├── index.html
└── ...
```

### Preview Production Build

```bash
# Preview before deploying
npm run preview
```

Opens at: `http://localhost:4173`

---

## 🚀 Deployment

### Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

**Important: Add Production Platform in Appwrite**
```
Go to: Appwrite Console → Settings → Platforms → Add platform
Type: Vue
Hostname: yourapp.vercel.app
```

### Deploy to Netlify

```bash
# Build first
npm run build

# Deploy dist/ folder
# Or connect GitHub repo for auto-deployment
```

**Add Production Platform:**
```
Hostname: yourapp.netlify.app
```

### Environment Variables for Production

In Vercel/Netlify dashboard, add:
```
VITE_APPWRITE_PROJECT_ID=68daf772003b1b1f5c78
VITE_APPWRITE_PROJECT_NAME=crawler
VITE_APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
VITE_APPWRITE_DATABASE_ID=tech-news-db
VITE_APPWRITE_ARTICLES_COLLECTION_ID=articles
VITE_APPWRITE_STORAGE_BUCKET_ID=article-images
```

---

## ✅ Testing Checklist

### Development Testing
```
☐ App loads without errors (http://localhost:5173)
☐ "Send a ping" button works (starter template)
☐ No CORS errors in browser console
☐ Articles fetch from Appwrite successfully
☐ Images load from Appwrite Storage
☐ Language toggle works (EN ↔ አማ)
☐ Routing works (article pages)
☐ View count increments
☐ Category filtering works
☐ Search functionality works
☐ Responsive on mobile (test with DevTools)
☐ Loading states display correctly
☐ Error handling works
```

### Production Testing
```
☐ Production build succeeds (npm run build)
☐ Preview works (npm run preview)
☐ Deployed app loads correctly
☐ Environment variables are set
☐ Production platform added in Appwrite
☐ HTTPS works correctly
☐ SEO meta tags present
☐ Performance is acceptable (Lighthouse score)
```

---

## 🔧 Configuration Files

### `vite.config.js`

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    host: true
  }
})
```

### `.env.example`

```dotenv
# Appwrite Configuration
VITE_APPWRITE_PROJECT_ID=your_project_id_here
VITE_APPWRITE_PROJECT_NAME=crawler
VITE_APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1

# Database Configuration
VITE_APPWRITE_DATABASE_ID=tech-news-db
VITE_APPWRITE_ARTICLES_COLLECTION_ID=articles
VITE_APPWRITE_SOURCES_COLLECTION_ID=sources

# Storage Configuration
VITE_APPWRITE_STORAGE_BUCKET_ID=article-images
```

---

## 🎯 Next Steps

### Phase 1: Setup ✅
- [x] Add Web Platform in Appwrite
- [x] Clone starter or create custom project
- [x] Configure environment variables
- [x] Test connection

### Phase 2: Development 🔄
- [ ] Customize design and branding
- [ ] Add more components (Search, Filter, etc.)
- [ ] Implement routing (Vue Router)
- [ ] Add state management (Pinia)
- [ ] Create article detail pages
- [ ] Add pagination

### Phase 3: Enhancement 📈
- [ ] Add SEO optimization (vue-meta)
- [ ] Implement PWA features
- [ ] Add analytics (Google Analytics)
- [ ] Optimize performance
- [ ] Add caching strategy
- [ ] Implement lazy loading

### Phase 4: Production 🚀
- [ ] Build production bundle
- [ ] Deploy to Vercel/Netlify
- [ ] Configure custom domain
- [ ] Set up CI/CD pipeline
- [ ] Monitor performance
- [ ] Gather user feedback

---

## 📚 Additional Resources

### Appwrite Documentation
- [Appwrite Web SDK](https://appwrite.io/docs/sdks#web)
- [Appwrite Vue.js Guide](https://appwrite.io/docs/quick-starts/vue)
- [Appwrite Databases](https://appwrite.io/docs/products/databases)
- [Appwrite Storage](https://appwrite.io/docs/products/storage)

### Vue.js Resources
- [Vue.js Documentation](https://vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Pinia (State Management)](https://pinia.vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)

### Project Documentation
- [Main Setup Guide](APPWRITE_SETUP.md)
- [Functions Guide](APPWRITE_FUNCTIONS.md)
- [Quick Reference](APPWRITE_QUICK_REFERENCE.md)
- [Platform Setup](APPWRITE_PLATFORM_SETUP.md)

---

## 🆘 Troubleshooting

### Problem: "Waiting for connection..."

**Possible Causes:**
1. Wrong Project ID in `.env`
2. Wrong endpoint URL
3. Web Platform not configured
4. CORS issues

**Solutions:**
1. Double-check `.env` values match Appwrite Console
2. Verify endpoint (US: `cloud.appwrite.io`, NYC: `nyc.cloud.appwrite.io`, EU: `eu.cloud.appwrite.io`)
3. Add Web Platform with hostname: `localhost`
4. Check browser console for specific errors

### Problem: "Module not found"

**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Problem: Build fails

**Solution:**
```bash
# Check for TypeScript errors
npm run type-check

# Clear Vite cache
rm -rf node_modules/.vite
npm run build
```

---

## 🎉 Success!

You now have a fully functional Vue.js frontend connected to Appwrite!

**What you've accomplished:**
✅ Appwrite Web Platform configured
✅ Vue.js project set up with Vite
✅ Appwrite SDK integrated
✅ Connection verified
✅ Ready to build features

**Start building:**
```bash
cd tech-news-frontend
npm run dev
# Open http://localhost:5173
```

Happy coding! 🚀

# 🚀 Deployment Guide - Todo AI Chatbot

Complete step-by-step guide to deploy your Todo AI Chatbot on **Render** (Backend) and **Vercel** (Frontend).

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Deployment (Render)](#backend-deployment-render)
3. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
4. [Environment Variables](#environment-variables)
5. [Database Setup](#database-setup)
6. [Post-Deployment](#post-deployment)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before deploying, make sure you have:

- [ ] GitHub account
- [ ] Render account (https://render.com)
- [ ] Vercel account (https://vercel.com)
- [ ] Neon/PostgreSQL database (https://neon.tech)
- [ ] OpenAI API Key (https://platform.openai.com)

---

## 🔧 Backend Deployment (Render)

### Step 1: Prepare Your Repository

1. **Push code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

#### Option A: Using render.yaml (Recommended - One Click)

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com

2. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Apply"

3. **Set Environment Variables**
   - Render will create the service
   - Go to service → "Environment"
   - Add the required environment variables (see below)

#### Option B: Manual Setup

1. **Go to Render Dashboard**
   - Visit https://dashboard.render.com

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service:**
   - **Name:** `todo-ai-chatbot-backend`
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

4. **Set Instance Type:**
   - Choose "Free" for testing
   - Or "Starter" ($7/month) for production

5. **Add Environment Variables** (see section below)

6. **Click "Create Web Service"**

### Step 3: Environment Variables for Backend

Add these in Render Dashboard → Your Service → Environment:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@host/dbname

# JWT Secret (Generate a random string)
JWT_SECRET_KEY=your-super-secret-jwt-key-here-change-this

# OpenAI API
OPENAI_API_KEY=sk-your-openai-api-key-here

# CORS (Your frontend URL)
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173

# Optional: OpenAI Model
OPENAI_MODEL=gpt-4o-mini
```

### Step 4: Get Your Backend URL

After deployment completes:
- Your backend URL will be: `https://todo-ai-chatbot-backend.onrender.com`
- Copy this URL for frontend configuration

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. **Update API URL in frontend**

   Create/update `frontend/.env.production`:
   ```env
   VITE_API_BASE_URL=https://todo-ai-chatbot-backend.onrender.com
   ```

2. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add production environment variables"
   git push origin main
   ```

### Step 2: Deploy on Vercel

#### Option A: Using Vercel CLI (Quick)

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Follow prompts:**
   - Setup and deploy: Yes
   - Which scope: Your account
   - Link to existing project: No
   - Project name: todo-ai-chatbot
   - Directory: ./
   - Override settings: No

5. **Deploy to production:**
   ```bash
   vercel --prod
   ```

#### Option B: Using Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit https://vercel.com/dashboard

2. **Import Project**
   - Click "Add New..." → "Project"
   - Import your GitHub repository

3. **Configure Project:**
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

4. **Add Environment Variables:**
   - Click "Environment Variables"
   - Add:
     ```
     VITE_API_BASE_URL = https://todo-ai-chatbot-backend.onrender.com
     ```

5. **Click "Deploy"**

### Step 3: Get Your Frontend URL

After deployment:
- Your frontend URL will be: `https://todo-ai-chatbot.vercel.app`
- Or custom domain if configured

### Step 4: Update Backend CORS

Go back to Render → Your Backend Service → Environment:
- Update `ALLOWED_ORIGINS` to include your Vercel URL:
  ```
  ALLOWED_ORIGINS=https://todo-ai-chatbot.vercel.app,http://localhost:5173
  ```

---

## 🗄️ Database Setup

### Using Neon PostgreSQL (Recommended - Free)

1. **Create Neon Account**
   - Go to https://neon.tech
   - Sign up for free

2. **Create New Project**
   - Click "New Project"
   - Name: `todo-ai-chatbot`
   - Region: Choose closest to your Render region
   - PostgreSQL version: 15+

3. **Get Connection String**
   - Copy the connection string
   - It looks like: `postgresql://user:pass@host/dbname`

4. **Convert to AsyncPG format**
   - Change `postgresql://` to `postgresql+asyncpg://`
   - Example:
     ```
     postgresql+asyncpg://user:pass@ep-xyz.neon.tech/neondb
     ```

5. **Add to Render Environment Variables**
   - Go to Render → Your Service → Environment
   - Add `DATABASE_URL` with the converted connection string

### Database Migration

The app will automatically create tables on first run. To verify:

1. **Check Render Logs**
   - Go to your service → "Logs"
   - Look for: "Database tables initialized successfully"

2. **If needed, run migrations manually:**
   ```bash
   # SSH into Render service (if available)
   python backend/add_title_column.py
   python backend/add_thread_id_column.py
   ```

---

## 🔐 Environment Variables

### Backend (.env)

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@host/database

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-minimum-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# CORS Configuration
ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:5173
```

### Frontend (.env.production)

```env
# API URL
VITE_API_BASE_URL=https://your-backend.onrender.com
```

### How to Generate JWT Secret

```bash
# Option 1: Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Option 2: Using OpenSSL
openssl rand -base64 32

# Option 3: Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

---

## ✅ Post-Deployment Checklist

### 1. Test Backend

```bash
# Health check
curl https://your-backend.onrender.com/api/health

# Should return: {"status":"healthy"}
```

### 2. Test Frontend

- Visit your Vercel URL
- Try to sign up/login
- Create a task
- Check if everything works

### 3. Monitor Logs

**Render:**
- Go to Dashboard → Your Service → Logs
- Check for any errors

**Vercel:**
- Go to Dashboard → Your Project → Logs
- Check runtime logs

### 4. Set Up Custom Domain (Optional)

**Vercel:**
- Go to Project Settings → Domains
- Add your custom domain
- Follow DNS configuration steps

**Render:**
- Go to Service Settings → Custom Domain
- Add your domain
- Update DNS records

---

## 🔧 Troubleshooting

### Backend Issues

#### 1. "Application failed to start"

**Check:**
- Build logs in Render
- Make sure all dependencies in `requirements.txt`
- Verify Python version compatibility

**Fix:**
```bash
# Make sure requirements.txt is up to date
pip freeze > requirements.txt
```

#### 2. "Database connection failed"

**Check:**
- DATABASE_URL is correct
- Format: `postgresql+asyncpg://...`
- Database is accessible from Render

**Fix:**
- Verify connection string
- Check Neon dashboard for database status
- Ensure IP whitelist allows Render (Neon allows all by default)

#### 3. "CORS errors"

**Check:**
- ALLOWED_ORIGINS includes frontend URL
- No trailing slashes in URLs

**Fix:**
```env
ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:5173
```

#### 4. "OpenAI API errors"

**Check:**
- API key is valid
- You have credits in OpenAI account
- Model name is correct

**Fix:**
- Verify API key at https://platform.openai.com
- Check billing status

### Frontend Issues

#### 1. "Failed to fetch"

**Check:**
- Backend is running
- VITE_API_URL is correct
- No CORS issues

**Fix:**
```env
# In Vercel environment variables
VITE_API_BASE_URL=https://your-backend.onrender.com
```

#### 2. "Build failed"

**Check:**
- Build logs in Vercel
- All dependencies in package.json
- No TypeScript errors

**Fix:**
```bash
# Test build locally
cd frontend
npm install
npm run build
```

#### 3. "Environment variables not working"

**Important:** In Vite, environment variables must start with `VITE_`

**Fix:**
- Redeploy after adding environment variables
- Clear Vercel build cache: Settings → Clear Cache

### General Issues

#### 1. "Slow first request (Cold Start)"

**Cause:** Render free tier spins down after inactivity

**Solutions:**
- Upgrade to paid tier ($7/month)
- Use a service like UptimeRobot to ping periodically
- Accept 30-60 second delay on first request

#### 2. "Database connection timeout"

**Fix:**
- Increase connection timeout in code
- Use connection pooling
- Check Neon database status

---

## 📊 Monitoring & Maintenance

### 1. Monitor Uptime

Use services like:
- [UptimeRobot](https://uptimerobot.com) - Free
- [Better Uptime](https://betteruptime.com) - Free tier
- [Pingdom](https://www.pingdom.com)

### 2. Check Logs Regularly

**Render:**
```
Dashboard → Service → Logs
```

**Vercel:**
```
Dashboard → Project → Logs
```

### 3. Database Backups

**Neon:**
- Automatic backups included
- Point-in-time recovery available

### 4. API Usage

**OpenAI:**
- Monitor usage at https://platform.openai.com/usage
- Set usage limits to avoid unexpected charges

---

## 💰 Cost Breakdown

### Free Tier (Testing)

| Service | Cost | Limitations |
|---------|------|-------------|
| Render (Backend) | Free | 750 hrs/month, sleeps after 15 min |
| Vercel (Frontend) | Free | 100 GB bandwidth/month |
| Neon (Database) | Free | 0.5 GB storage, 1 project |
| **Total** | **$0/month** | Good for testing |

### Production Setup

| Service | Cost | Benefits |
|---------|------|----------|
| Render Starter | $7/month | Always on, no cold starts |
| Vercel Pro | Free (or $20/month) | More bandwidth |
| Neon Pro | $19/month | More storage & compute |
| OpenAI API | Pay-per-use | ~$0.01-0.10 per conversation |
| **Total** | **~$26-46/month** | Production ready |

---

## 🎯 Quick Deploy Commands

```bash
# 1. Prepare repository
git add .
git commit -m "Deploy to production"
git push origin main

# 2. Deploy backend (automatic with render.yaml)
# Just push to GitHub, Render will auto-deploy

# 3. Deploy frontend
cd frontend
vercel --prod

# 4. Check status
curl https://your-backend.onrender.com/api/health
```

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Neon Documentation](https://neon.tech/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)

---

## 🆘 Need Help?

1. Check logs in Render/Vercel dashboard
2. Review this guide's troubleshooting section
3. Check GitHub issues
4. Verify all environment variables are set correctly

---

**🎉 Congratulations! Your Todo AI Chatbot is now live!**

**Backend:** https://your-backend.onrender.com
**Frontend:** https://your-app.vercel.app

Share with friends and start managing tasks with AI! 🚀

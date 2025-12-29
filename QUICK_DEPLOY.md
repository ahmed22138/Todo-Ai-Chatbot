# 🚀 Quick Deploy Guide

Fast track deployment for Todo AI Chatbot on Render + Vercel.

---

## ⚡ 5-Minute Setup

### 1️⃣ Prerequisites (2 minutes)

Get these ready:
- [ ] GitHub account
- [ ] OpenAI API Key: https://platform.openai.com/api-keys
- [ ] Neon Database: https://neon.tech (free, 2-min signup)

---

### 2️⃣ Database Setup (1 minute)

1. Go to https://neon.tech → Sign up
2. Create new project: `todo-ai-chatbot`
3. Copy connection string
4. **Important:** Change `postgresql://` to `postgresql+asyncpg://`
   ```
   Before: postgresql://user:pass@host/db
   After:  postgresql+asyncpg://user:pass@host/db
   ```

---

### 3️⃣ Backend Deploy - Render (1 minute)

#### Using render.yaml (One Click)

1. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Deploy"
   git push origin main
   ```

2. Go to: https://dashboard.render.com
3. Click: **New +** → **Blueprint**
4. Connect your GitHub repo
5. Render auto-detects `render.yaml` → Click **Apply**

6. **Set Environment Variables:**
   - Go to service → **Environment**
   - Add:
     ```
     DATABASE_URL = postgresql+asyncpg://[your-neon-url]
     OPENAI_API_KEY = sk-[your-key]
     ALLOWED_ORIGINS = http://localhost:5173
     ```

7. Wait for deploy (~2 minutes)
8. Copy your backend URL: `https://[your-service].onrender.com`

---

### 4️⃣ Frontend Deploy - Vercel (1 minute)

1. Go to: https://vercel.com/new
2. Import your GitHub repo
3. Configure:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

4. **Add Environment Variable:**
   ```
   VITE_API_BASE_URL = https://[your-backend].onrender.com
   ```

5. Click **Deploy**
6. Wait (~1 minute)

---

### 5️⃣ Final Step - Update CORS

1. Go back to Render → Your service → **Environment**
2. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS = https://[your-app].vercel.app,http://localhost:5173
   ```
3. Service will auto-redeploy

---

## ✅ Done!

**Your app is live!**
- Frontend: `https://[your-app].vercel.app`
- Backend: `https://[your-backend].onrender.com`

Test it:
1. Open your Vercel URL
2. Sign up
3. Send a message: "add buy groceries"

---

## 🔧 Troubleshooting

### "Failed to fetch"
- Check backend is running (Render logs)
- Verify `VITE_API_BASE_URL` in Vercel
- Check `ALLOWED_ORIGINS` in Render

### "Database connection failed"
- Verify `DATABASE_URL` format: `postgresql+asyncpg://...`
- Check Neon database is active

### "OpenAI API error"
- Verify API key at https://platform.openai.com
- Check you have credits

### "Cold start (first request slow)"
- Free tier sleeps after 15 min
- First request takes ~30 seconds
- Upgrade to Starter ($7/month) to avoid

---

## 💰 Cost

**Free Tier:**
- Render: Free (sleeps after 15 min)
- Vercel: Free (100 GB bandwidth)
- Neon: Free (0.5 GB storage)
- OpenAI: ~$0.01 per conversation
- **Total: $0/month** ✅

**Production:**
- Render Starter: $7/month (no sleep)
- Total: ~$7-10/month

---

## 📚 Need More Info?

See full guide: [DEPLOYMENT.md](./DEPLOYMENT.md)

---

**🎉 Happy Deploying!**

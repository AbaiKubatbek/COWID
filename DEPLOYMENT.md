# CowID Deployment Guide

## Local Development

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+ (for backend)
- Git

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:5173`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will run on `http://localhost:8000`

---

## Deployment Options

### Option 1: Vercel (Recommended for Frontend)

**Frontend Deployment:**

1. **Connect repository:**
   - Push code to GitHub
   - Go to [vercel.com](https://vercel.com)
   - Click "Import Project"
   - Select your GitHub repository

2. **Configure:**
   - Framework: React (auto-detected)
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

3. **Environment Variables:**
   ```
   VITE_API_URL=https://your-api-domain.com
   ```

4. **Deploy:**
   ```bash
   npm run deploy:vercel
   ```

### Option 2: Netlify (Alternative for Frontend)

1. **Connect:**
   - Go to [netlify.com](https://netlify.com)
   - Click "Import an existing project"
   - Connect GitHub

2. **Configure:**
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`

3. **Deploy:**
   ```bash
   npm run deploy:netlify
   ```

### Option 3: Render (For Backend)

1. **Create New Service:**
   - Go to [render.com](https://render.com)
   - Click "New +"
   - Select "Web Service"
   - Connect GitHub

2. **Configure:**
   - Name: `cowid-backend`
   - Region: Choose closest to users
   - Branch: `main`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Environment: Python 3.11

3. **Environment Variables:**
   ```
   DATABASE_URL=<your-postgres-url>
   ENVIRONMENT=production
   ```

4. **Set Up Database:**
   - Add PostgreSQL database on Render
   - Get connection string
   - Add as `DATABASE_URL`

### Option 4: Docker + Any Cloud Provider

**Build Docker image:**

```bash
# Frontend
docker build -t cowid-frontend ./frontend

# Backend
docker build -t cowid-backend ./backend
```

**Push to registry:**

```bash
docker tag cowid-frontend your-registry/cowid-frontend
docker push your-registry/cowid-frontend
```

---

## Production Checklist

### Frontend
- [ ] Environment variables configured
- [ ] API URL points to production backend
- [ ] Build tested: `npm run build`
- [ ] Preview working: `npm run preview`
- [ ] No console errors or warnings
- [ ] HTTPS enabled
- [ ] Responsive design verified on mobile

### Backend
- [ ] Database properly migrated
- [ ] Environment variables configured
- [ ] CORS configured for frontend domain
- [ ] Error logging enabled
- [ ] Rate limiting configured
- [ ] API health check working

### Security
- [ ] HTTPS enabled on all endpoints
- [ ] API keys and secrets in environment variables
- [ ] Database credentials secured
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] Rate limiting enabled

---

## Monitoring & Maintenance

### Health Checks
- Frontend: Load main page and check console for errors
- Backend: `GET /health` endpoint

### Logs
- Vercel: Vercel Dashboard > Logs
- Netlify: Netlify Dashboard > Logs
- Render: Render Dashboard > Logs

### Performance
- Frontend: Use Lighthouse to check performance
- Backend: Monitor API response times

---

## Troubleshooting

### CORS Errors
Update backend CORS settings:
```python
# app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Camera Not Working
- Ensure HTTPS is enabled (camera requires secure context)
- Check browser permissions
- Test on different devices

### Database Connection Issues
- Verify `DATABASE_URL` format
- Check database is online and accessible
- Verify credentials in environment variables

---

## Build Commands Reference

```bash
# Frontend
npm run build        # Production build
npm run preview      # Preview production build locally
npm run dev          # Development server
npm run lint         # Run linter
npm run deploy:vercel    # Deploy to Vercel
npm run deploy:netlify   # Deploy to Netlify
```

---

## Quick Deploy Summary

### Fastest Setup (Vercel + Render)

1. **Frontend (Vercel):**
   ```bash
   npm run deploy:vercel
   ```

2. **Backend (Render):**
   - Connect GitHub repository
   - Set environment variables
   - Deploy automatically on push

3. **Update Frontend API URL:**
   - Set `VITE_API_URL` to Render backend URL
   - Redeploy frontend

### Estimated Time: 15-20 minutes

---

## Post-Deployment

1. Test all features with production build
2. Verify camera functionality works on mobile
3. Test file uploads
4. Verify database operations
5. Monitor error logs for first 24 hours
6. Update DNS if using custom domain

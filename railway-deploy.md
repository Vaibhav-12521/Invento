# Railway Deployment Guide

## Why Railway?
- ✅ **Easier than Vercel** for Python apps
- ✅ **Built-in PostgreSQL** database
- ✅ **Automatic deployments** from GitHub
- ✅ **Free tier** available
- ✅ **No complex configuration** needed

## Step 1: Prepare Your Code

### 1. Create a `Procfile` for Railway
```
web: gunicorn app:app
```

### 2. Update `requirements.txt`
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3
SQLAlchemy==2.0.21
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### 3. Update `app.py` for Railway
```python
# Add this at the end of app.py
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
```

## Step 2: Deploy to Railway

### Method 1: GitHub Integration (Recommended)
1. **Push code to GitHub**
2. **Go to [railway.app](https://railway.app)**
3. **Sign up/Login** with GitHub
4. **Click "New Project"**
5. **Select "Deploy from GitHub repo"**
6. **Choose your repository**
7. **Railway will automatically detect Python and deploy**

### Method 2: Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## Step 3: Add Database

1. **In Railway dashboard**, click "New"
2. **Select "Database"** → "PostgreSQL"
3. **Railway will automatically connect** your app to the database
4. **Environment variables** will be set automatically

## Step 4: Configure Environment Variables

In Railway dashboard, add:
```
SECRET_KEY=your_secret_key_here
```

## Step 5: Deploy

Railway will automatically deploy your app and give you a URL like:
`https://your-app-name.railway.app`

## Benefits of Railway
- ✅ **Zero configuration** for Python apps
- ✅ **Automatic database setup**
- ✅ **Continuous deployment** from GitHub
- ✅ **Free tier** with generous limits
- ✅ **Built-in monitoring** and logs

## Troubleshooting
- Check Railway logs in dashboard
- Ensure `Procfile` is in root directory
- Verify all dependencies in `requirements.txt` 
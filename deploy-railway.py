#!/usr/bin/env python3
"""
Railway Deployment Helper
"""

import os
import subprocess
import webbrowser

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'templates/',
        'static/'
    ]
    
    print("🔍 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def main():
    print("🚀 Railway Deployment Helper")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("\n❌ Some required files are missing!")
        print("Please ensure all files are in place before deploying.")
        return
    
    print("\n📋 Deployment Steps:")
    print("1. Push code to GitHub")
    print("2. Deploy on Railway")
    print("3. Add database")
    print("4. Configure environment variables")
    
    # Step 1: Check if git is initialized
    if not os.path.exists('.git'):
        print("\n🔧 Initializing Git repository...")
        subprocess.run(['git', 'init'], check=True)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit for Railway deployment'], check=True)
        print("✅ Git repository initialized")
    
    print("\n📤 Step 1: Push to GitHub")
    print("1. Create a new repository on GitHub")
    print("2. Run these commands:")
    print("   git remote add origin https://github.com/yourusername/your-repo-name.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n🌐 Step 2: Deploy on Railway")
    print("1. Go to https://railway.app")
    print("2. Sign up with GitHub")
    print("3. Click 'New Project'")
    print("4. Select 'Deploy from GitHub repo'")
    print("5. Choose your repository")
    print("6. Railway will auto-detect Python and deploy!")
    
    print("\n🗄️ Step 3: Add Database")
    print("1. In Railway dashboard, click 'New'")
    print("2. Select 'Database' → 'PostgreSQL'")
    print("3. Railway connects it automatically")
    
    print("\n⚙️ Step 4: Environment Variables")
    print("Add in Railway dashboard:")
    print("SECRET_KEY=your_secret_key_here")
    
    print("\n🎉 Step 5: Get Your URL")
    print("Railway gives you a URL like: https://your-app-name.railway.app")
    
    # Open Railway in browser
    print("\n🌐 Opening Railway website...")
    try:
        webbrowser.open('https://railway.app')
        print("✅ Railway website opened in browser")
    except:
        print("⚠️ Could not open browser automatically")
        print("Please visit: https://railway.app")
    
    print("\n📖 For detailed instructions, see:")
    print("- railway-deploy.md")
    print("- DEPLOYMENT_OPTIONS.md")

if __name__ == "__main__":
    main() 
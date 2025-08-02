#!/usr/bin/env python3
"""
Deployment helper script for Vercel
"""

import secrets
import os

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_hex(32)

def main():
    print("🚀 Vercel Deployment Helper")
    print("=" * 40)
    
    # Generate secret key
    secret_key = generate_secret_key()
    print(f"\n🔑 Generated Secret Key:")
    print(f"SECRET_KEY={secret_key}")
    
    print("\n📋 Next Steps:")
    print("1. Set up a PostgreSQL database (Supabase, Railway, or Neon)")
    print("2. Get your DATABASE_URL from the database provider")
    print("3. Deploy to Vercel using one of these methods:")
    print("   - Vercel CLI: vercel")
    print("   - GitHub integration: Push to GitHub and connect to Vercel")
    
    print("\n🔧 Environment Variables to set in Vercel:")
    print(f"SECRET_KEY={secret_key}")
    print("DATABASE_URL=your_postgresql_connection_string")
    
    print("\n📖 For detailed instructions, see DEPLOYMENT.md")
    
    # Create .env file for local development
    env_content = f"""# Local development environment variables
SECRET_KEY={secret_key}
DATABASE_URL=sqlite:///inventory.db
"""
    
    with open('.env.example', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Created .env.example file for local development")

if __name__ == "__main__":
    main() 
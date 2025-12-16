#!/usr/bin/env python3
"""
Quick API Setup Helper for COLLIDE AI Lead Generation
Helps you configure and test API integrations
"""

import os
import sys

def check_env_file():
    """Check if .env file exists"""
    env_path = os.path.expanduser("~/Documents/collide-ai-platform/.env")
    return os.path.exists(env_path)

def main():
    print("🔧 COLLIDE AI - API Setup Helper")
    print("=" * 60)
    print()
    
    if not check_env_file():
        print("❌ .env file not found!")
        print("   Creating from template...")
        os.system("cp ~/Documents/collide-ai-platform/.env.example ~/Documents/collide-ai-platform/.env")
        print("✅ Created .env file")
        print()
    
    print("📋 API Integration Options:")
    print()
    print("1️⃣  FREE OPTION (Start here!)")
    print("   • Demo mode (no API keys needed)")
    print("   • Manual CSV import")
    print("   • Gmail SMTP for outreach")
    print("   Cost: $0/month")
    print()
    
    print("2️⃣  BASIC OPTION ($10-20/month)")
    print("   ✅ Hunter.io FREE (50 emails/month)")
    print("   ✅ RapidAPI Instagram ($10/month, 1000 requests)")
    print("   ✅ Gmail SMTP")
    print("   → Best for: 100-500 leads/month")
    print()
    
    print("3️⃣  PROFESSIONAL OPTION ($50-100/month)")
    print("   ✅ Hunter.io Pro ($49/month, 1000 searches)")
    print("   ✅ RapidAPI Instagram ($10-30/month)")
    print("   ✅ RapidAPI LinkedIn ($20-50/month)")
    print("   ✅ Apify scrapers ($49/month)")
    print("   → Best for: 1,000-10,000 leads/month")
    print()
    
    print("=" * 60)
    print()
    
    choice = input("Which option would you like to set up? (1/2/3): ").strip()
    print()
    
    if choice == "1":
        setup_free_option()
    elif choice == "2":
        setup_basic_option()
    elif choice == "3":
        setup_professional_option()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

def setup_free_option():
    """Setup free demo mode + Gmail"""
    print("🆓 Setting up FREE option...")
    print()
    print("Step 1: Email Configuration (for outreach)")
    print("-" * 60)
    
    email = input("Enter your Gmail address: ").strip()
    
    print()
    print("Step 2: Get Gmail App Password")
    print("  1. Go to: https://myaccount.google.com/apppasswords")
    print("  2. Generate password for 'COLLIDE AI'")
    print("  3. Copy the 16-character code")
    print()
    
    password = input("Enter your Gmail App Password: ").strip()
    
    # Update .env
    env_path = os.path.expanduser("~/Documents/collide-ai-platform/.env")
    
    with open(env_path, 'a') as f:
        f.write(f"\n# Email Configuration\n")
        f.write(f"EMAIL_USER={email}\n")
        f.write(f"EMAIL_PASSWORD={password}\n")
    
    print()
    print("✅ Free option configured!")
    print()
    print("You can now:")
    print("  • Use demo mode for testing")
    print("  • Import leads from CSV")
    print("  • Send personalized emails")
    print()
    print("Next steps:")
    print("  1. Go to: http://localhost:8080/lead-gen")
    print("  2. Try demo campaign (no API keys needed)")
    print("  3. Or manually import CSV with your own leads")

def setup_basic_option():
    """Setup Hunter.io + RapidAPI Instagram"""
    print("💰 Setting up BASIC option...")
    print()
    
    print("Step 1: Hunter.io (Email Discovery)")
    print("-" * 60)
    print("  1. Sign up: https://hunter.io/")
    print("  2. Go to Dashboard → API")
    print("  3. Copy your API key")
    print()
    
    hunter_key = input("Enter Hunter.io API key (or press Enter to skip): ").strip()
    
    print()
    print("Step 2: RapidAPI (Instagram Scraper)")
    print("-" * 60)
    print("  1. Sign up: https://rapidapi.com/")
    print("  2. Search 'Instagram Scraper'")
    print("  3. Subscribe to API (usually has free tier)")
    print("  4. Copy your RapidAPI key from dashboard")
    print()
    
    rapidapi_key = input("Enter RapidAPI key (or press Enter to skip): ").strip()
    
    print()
    print("Step 3: Email Configuration")
    print("-" * 60)
    
    email = input("Enter your Gmail address: ").strip()
    password = input("Enter your Gmail App Password: ").strip()
    
    # Update .env
    env_path = os.path.expanduser("~/Documents/collide-ai-platform/.env")
    
    with open(env_path, 'a') as f:
        f.write(f"\n# API Configuration\n")
        if hunter_key:
            f.write(f"HUNTER_API_KEY={hunter_key}\n")
        if rapidapi_key:
            f.write(f"RAPIDAPI_KEY={rapidapi_key}\n")
            f.write(f"RAPIDAPI_INSTAGRAM_HOST=instagram-scraper-api2.p.rapidapi.com\n")
        f.write(f"\n# Email Configuration\n")
        f.write(f"EMAIL_USER={email}\n")
        f.write(f"EMAIL_PASSWORD={password}\n")
    
    print()
    print("✅ Basic option configured!")
    print()
    print("Active features:")
    if hunter_key:
        print("  ✅ Email discovery via Hunter.io")
    if rapidapi_key:
        print("  ✅ Instagram lead search")
    print("  ✅ Email outreach")
    print()
    print("Start generating leads: http://localhost:8080/lead-gen")

def setup_professional_option():
    """Setup full professional suite"""
    print("🚀 Setting up PROFESSIONAL option...")
    print()
    
    print("This will configure:")
    print("  • Hunter.io Pro (email discovery)")
    print("  • RapidAPI Instagram (profile scraping)")
    print("  • RapidAPI LinkedIn (professional search)")
    print("  • Apify (advanced scraping)")
    print()
    
    # Collect all keys
    hunter_key = input("Hunter.io API key: ").strip()
    rapidapi_key = input("RapidAPI key: ").strip()
    apify_token = input("Apify API token (optional): ").strip()
    email = input("Gmail address: ").strip()
    password = input("Gmail App Password: ").strip()
    
    # Update .env
    env_path = os.path.expanduser("~/Documents/collide-ai-platform/.env")
    
    with open(env_path, 'a') as f:
        f.write(f"\n# Professional API Configuration\n")
        f.write(f"HUNTER_API_KEY={hunter_key}\n")
        f.write(f"RAPIDAPI_KEY={rapidapi_key}\n")
        f.write(f"RAPIDAPI_INSTAGRAM_HOST=instagram-scraper-api2.p.rapidapi.com\n")
        f.write(f"RAPIDAPI_LINKEDIN_HOST=linkedin-data-scraper.p.rapidapi.com\n")
        if apify_token:
            f.write(f"APIFY_API_TOKEN={apify_token}\n")
        f.write(f"\n# Email Configuration\n")
        f.write(f"EMAIL_USER={email}\n")
        f.write(f"EMAIL_PASSWORD={password}\n")
    
    print()
    print("✅ Professional option configured!")
    print()
    print("You now have access to:")
    print("  ✅ Full Instagram lead search")
    print("  ✅ LinkedIn professional search")
    print("  ✅ Automated email discovery")
    print("  ✅ Bulk outreach campaigns")
    print()
    print("🎉 Ready to scale! Visit: http://localhost:8080/lead-gen")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)

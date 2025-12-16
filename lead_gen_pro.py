"""
COLLIDE AI - Lead Generation with Real API Integration
Supports: RapidAPI Instagram/LinkedIn, Hunter.io, Official APIs
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LeadGeneratorPro:
    """
    Enhanced lead generation with real API integrations.
    Supports RapidAPI, Hunter.io, and official Instagram/LinkedIn APIs.
    """
    
    def __init__(self):
        self.leads = []
        self.qualified_leads = []
        self.outreach_log = []
        
        # API Keys from environment
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY', '')
        self.rapidapi_instagram_host = os.getenv('RAPIDAPI_INSTAGRAM_HOST', 'instagram-scraper-api2.p.rapidapi.com')
        self.rapidapi_linkedin_host = os.getenv('RAPIDAPI_LINKEDIN_HOST', 'linkedin-data-scraper.p.rapidapi.com')
        
        self.hunter_api_key = os.getenv('HUNTER_API_KEY', '')
        self.apify_token = os.getenv('APIFY_API_TOKEN', '')
        
        # Official APIs (if available)
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
        
        # Email configuration
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
        # Target industries
        self.target_industries = ['fashion', 'beauty', 'lifestyle', 'design', 'sustainable', 'wellness']
    
    
    def search_instagram_rapidapi(self, hashtag: str, max_results: int = 50) -> List[Dict]:
        """
        Search Instagram using RapidAPI scraper.
        Requires RAPIDAPI_KEY in environment.
        """
        if not self.rapidapi_key:
            logger.warning("No RapidAPI key found. Using demo data.")
            return self._generate_demo_instagram_leads(hashtag, max_results)
        
        try:
            url = f"https://{self.rapidapi_instagram_host}/v1/hashtag/{hashtag}"
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": self.rapidapi_instagram_host
            }
            
            params = {
                "count": max_results
            }
            
            logger.info(f"Searching Instagram for #{hashtag} via RapidAPI...")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                leads = self._parse_instagram_response(data, hashtag)
                logger.info(f"Found {len(leads)} Instagram leads for #{hashtag}")
                return leads
            else:
                logger.error(f"RapidAPI error: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching Instagram: {str(e)}")
            return []
    
    
    def search_instagram_apify(self, hashtag: str, max_results: int = 50) -> List[Dict]:
        """
        Search Instagram using Apify Instagram Hashtag Scraper.
        Requires APIFY_API_TOKEN in environment.
        """
        if not self.apify_token:
            logger.warning("No Apify token found. Using demo data.")
            return self._generate_demo_instagram_leads(hashtag, max_results)
        
        try:
            # Start Apify actor
            url = "https://api.apify.com/v2/acts/apify~instagram-hashtag-scraper/runs"
            
            headers = {
                "Authorization": f"Bearer {self.apify_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "hashtags": [hashtag],
                "resultsLimit": max_results
            }
            
            logger.info(f"Starting Apify Instagram scraper for #{hashtag}...")
            response = requests.post(url, headers=headers, json=payload, params={"token": self.apify_token})
            
            if response.status_code == 201:
                run_id = response.json()['data']['id']
                
                # Wait for completion (with timeout)
                for _ in range(30):  # Max 30 seconds
                    time.sleep(1)
                    status_url = f"https://api.apify.com/v2/acts/apify~instagram-hashtag-scraper/runs/{run_id}"
                    status = requests.get(status_url, params={"token": self.apify_token})
                    
                    if status.json()['data']['status'] == 'SUCCEEDED':
                        # Get results
                        dataset_id = status.json()['data']['defaultDatasetId']
                        results_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
                        results = requests.get(results_url, params={"token": self.apify_token})
                        
                        leads = self._parse_apify_response(results.json(), hashtag)
                        logger.info(f"Found {len(leads)} Instagram leads for #{hashtag}")
                        return leads
                
                logger.warning("Apify scraper timed out")
                return []
            else:
                logger.error(f"Apify error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with Apify: {str(e)}")
            return []
    
    
    def search_linkedin_rapidapi(self, keyword: str, max_results: int = 50) -> List[Dict]:
        """
        Search LinkedIn using RapidAPI scraper.
        Requires RAPIDAPI_KEY in environment.
        """
        if not self.rapidapi_key:
            logger.warning("No RapidAPI key found. Using demo data.")
            return self._generate_demo_linkedin_leads(keyword, max_results)
        
        try:
            url = f"https://{self.rapidapi_linkedin_host}/search/people"
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": self.rapidapi_linkedin_host
            }
            
            params = {
                "keywords": keyword,
                "limit": max_results
            }
            
            logger.info(f"Searching LinkedIn for '{keyword}' via RapidAPI...")
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                leads = self._parse_linkedin_response(data, keyword)
                logger.info(f"Found {len(leads)} LinkedIn leads for '{keyword}'")
                return leads
            else:
                logger.error(f"RapidAPI LinkedIn error: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching LinkedIn: {str(e)}")
            return []
    
    
    def find_email_hunter(self, domain: str, first_name: str = "", last_name: str = "") -> Optional[str]:
        """
        Find email address using Hunter.io API.
        Requires HUNTER_API_KEY in environment.
        """
        if not self.hunter_api_key:
            logger.warning("No Hunter.io API key found. Skipping email discovery.")
            return None
        
        try:
            url = "https://api.hunter.io/v2/email-finder"
            
            params = {
                "domain": domain,
                "first_name": first_name,
                "last_name": last_name,
                "api_key": self.hunter_api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data') and data['data'].get('email'):
                    email = data['data']['email']
                    confidence = data['data'].get('score', 0)
                    logger.info(f"Found email: {email} (confidence: {confidence}%)")
                    return email
            
            return None
            
        except Exception as e:
            logger.error(f"Hunter.io error: {str(e)}")
            return None
    
    
    def _parse_instagram_response(self, data: Dict, hashtag: str) -> List[Dict]:
        """Parse RapidAPI Instagram response into lead format."""
        leads = []
        
        posts = data.get('data', {}).get('recent', [])
        
        for post in posts:
            owner = post.get('owner', {})
            
            lead = {
                'name': owner.get('username', 'Unknown'),
                'platform': 'instagram',
                'profile_url': f"https://instagram.com/{owner.get('username', '')}",
                'followers': owner.get('follower_count', 0),
                'bio': owner.get('biography', ''),
                'website': owner.get('external_url', ''),
                'engagement_rate': self._calculate_engagement_rate(post),
                'recent_posts': post.get('edge_owner_to_timeline_media', {}).get('count', 0),
                'hashtag': hashtag,
                'source': 'rapidapi'
            }
            
            leads.append(lead)
        
        return leads
    
    
    def _parse_apify_response(self, data: List[Dict], hashtag: str) -> List[Dict]:
        """Parse Apify Instagram response into lead format."""
        leads = []
        
        for item in data:
            lead = {
                'name': item.get('ownerUsername', 'Unknown'),
                'platform': 'instagram',
                'profile_url': f"https://instagram.com/{item.get('ownerUsername', '')}",
                'followers': item.get('ownerFollowers', 0),
                'bio': item.get('caption', ''),
                'website': '',
                'engagement_rate': (item.get('likesCount', 0) / max(item.get('ownerFollowers', 1), 1)) * 100,
                'recent_posts': 0,
                'hashtag': hashtag,
                'source': 'apify'
            }
            
            leads.append(lead)
        
        return leads
    
    
    def _parse_linkedin_response(self, data: Dict, keyword: str) -> List[Dict]:
        """Parse RapidAPI LinkedIn response into lead format."""
        leads = []
        
        results = data.get('data', [])
        
        for person in results:
            name_parts = person.get('name', '').split()
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[-1] if len(name_parts) > 1 else ''
            
            lead = {
                'name': person.get('name', 'Unknown'),
                'first_name': first_name,
                'last_name': last_name,
                'platform': 'linkedin',
                'profile_url': person.get('profileUrl', ''),
                'title': person.get('headline', ''),
                'company': person.get('company', ''),
                'location': person.get('location', ''),
                'industry': person.get('industry', ''),
                'connections': person.get('connections', 0),
                'keyword': keyword,
                'source': 'rapidapi'
            }
            
            # Try to find email from LinkedIn data or Hunter.io
            company_domain = self._extract_domain_from_company(lead.get('company', ''))
            if company_domain and self.hunter_api_key:
                email = self.find_email_hunter(company_domain, first_name, last_name)
                if email:
                    lead['email'] = email
            
            leads.append(lead)
        
        return leads
    
    
    def _calculate_engagement_rate(self, post: Dict) -> float:
        """Calculate engagement rate from Instagram post data."""
        likes = post.get('edge_liked_by', {}).get('count', 0)
        comments = post.get('edge_media_to_comment', {}).get('count', 0)
        total_engagement = likes + comments
        
        followers = post.get('owner', {}).get('follower_count', 1)
        
        return (total_engagement / max(followers, 1)) * 100
    
    
    def _extract_domain_from_company(self, company_name: str) -> Optional[str]:
        """Extract likely domain from company name."""
        if not company_name:
            return None
        
        # Simple heuristic: lowercase, remove spaces, add .com
        domain = company_name.lower().replace(' ', '').replace('inc.', '').replace('llc', '')
        return f"{domain}.com"
    
    
    def _generate_demo_instagram_leads(self, hashtag: str, count: int) -> List[Dict]:
        """Generate demo Instagram leads for testing without API keys."""
        demo_leads = []
        
        demo_names = [
            "sustainable_style_co", "eco_fashion_lab", "clean_beauty_studio",
            "slow_fashion_movement", "green_beauty_brand", "ethical_closet",
            "conscious_lifestyle", "minimal_wardrobe", "plant_based_beauty",
            "zero_waste_fashion"
        ]
        
        for i in range(min(count, len(demo_names))):
            lead = {
                'name': demo_names[i],
                'platform': 'instagram',
                'profile_url': f"https://instagram.com/{demo_names[i]}",
                'followers': 5000 + (i * 1000),
                'bio': f"Sustainable {hashtag.replace('#', '')} brand • DM for collabs",
                'website': f"https://{demo_names[i].replace('_', '')}.com",
                'engagement_rate': 3.5 + (i * 0.5),
                'recent_posts': 50 + (i * 10),
                'hashtag': hashtag,
                'source': 'demo'
            }
            demo_leads.append(lead)
        
        return demo_leads
    
    
    def _generate_demo_linkedin_leads(self, keyword: str, count: int) -> List[Dict]:
        """Generate demo LinkedIn leads for testing without API keys."""
        demo_leads = []
        
        demo_profiles = [
            {"name": "Sarah Chen", "title": "Founder & CEO", "company": "Eco Beauty Co"},
            {"name": "Emma Rodriguez", "title": "Creative Director", "company": "Sustainable Style"},
            {"name": "Alex Johnson", "title": "Brand Strategist", "company": "Green Fashion Lab"},
            {"name": "Maya Patel", "title": "Founder", "company": "Clean Beauty Studio"},
            {"name": "Sofia Martinez", "title": "CEO", "company": "Ethical Wardrobe"},
        ]
        
        for i in range(min(count, len(demo_profiles))):
            profile = demo_profiles[i]
            lead = {
                'name': profile['name'],
                'first_name': profile['name'].split()[0],
                'last_name': profile['name'].split()[-1],
                'platform': 'linkedin',
                'profile_url': f"https://linkedin.com/in/{profile['name'].lower().replace(' ', '-')}",
                'title': profile['title'],
                'company': profile['company'],
                'location': 'United States',
                'industry': 'Fashion & Beauty',
                'connections': 500 + (i * 100),
                'keyword': keyword,
                'source': 'demo'
            }
            demo_leads.append(lead)
        
        return demo_leads


# Add this to your existing lead_gen.py or create lead_gen_pro.py
if __name__ == '__main__':
    print("🚀 COLLIDE AI - Lead Generation Pro")
    print("=" * 50)
    print()
    
    # Check for API keys
    generator = LeadGeneratorPro()
    
    print("📊 API Configuration Status:")
    print(f"  RapidAPI: {'✅ Configured' if generator.rapidapi_key else '❌ Not configured'}")
    print(f"  Hunter.io: {'✅ Configured' if generator.hunter_api_key else '❌ Not configured'}")
    print(f"  Apify: {'✅ Configured' if generator.apify_token else '❌ Not configured'}")
    print()
    
    if not generator.rapidapi_key:
        print("ℹ️  Running in DEMO mode (no API keys found)")
        print("   To connect real APIs, see: API_SETUP_GUIDE.md")
        print()
    
    # Test search
    print("Testing Instagram search...")
    instagram_leads = generator.search_instagram_rapidapi("sustainablefashion", max_results=5)
    print(f"Found {len(instagram_leads)} Instagram leads")
    print()
    
    print("Testing LinkedIn search...")
    linkedin_leads = generator.search_linkedin_rapidapi("fashion brand founder", max_results=5)
    print(f"Found {len(linkedin_leads)} LinkedIn leads")
    print()
    
    print("✅ Test complete!")
    print(f"   Total leads: {len(instagram_leads) + len(linkedin_leads)}")

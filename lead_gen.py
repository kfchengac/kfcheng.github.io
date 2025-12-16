"""
COLLIDE AI - Lead Generation & Outreach Tool
Automatically search, identify, qualify, and reach out to creative entrepreneurs
across LinkedIn, Email, Instagram, and other social media platforms.
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

class LeadGenerator:
    """
    Lead generation and outreach automation for COLLIDE AI.
    Finds creative entrepreneurs in fashion, beauty, lifestyle, and design.
    """
    
    def __init__(self):
        self.leads = []
        self.qualified_leads = []
        self.outreach_log = []
        
        # API Keys from environment
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.hunter_api_key = os.getenv('HUNTER_API_KEY', '')  # For email finding
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN', '')
        
        # Email configuration
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')
        
        # Search criteria
        self.target_industries = [
            'fashion', 'beauty', 'lifestyle', 'design', 'skincare',
            'cosmetics', 'apparel', 'accessories', 'home decor', 'jewelry'
        ]
        
        self.target_titles = [
            'founder', 'ceo', 'creative director', 'brand director',
            'owner', 'entrepreneur', 'designer', 'brand manager'
        ]
        
        self.lead_qualification_criteria = {
            'min_followers': 1000,  # Minimum social media following
            'has_website': True,
            'engagement_rate': 2.0,  # Minimum engagement %
            'recent_activity': 30  # Days
        }
    
    def search_instagram_leads(self, hashtags: List[str], max_results: int = 50) -> List[Dict]:
        """
        Search Instagram for potential leads using hashtags.
        Note: Requires Instagram Graph API access or scraping (use carefully with ToS).
        """
        print(f"🔍 Searching Instagram with hashtags: {hashtags}")
        
        leads = []
        
        # Sample structure - in production, integrate with Instagram Graph API
        # For demonstration, showing the structure
        sample_leads = [
            {
                'platform': 'instagram',
                'username': '@sustainablebeautyco',
                'name': 'Sarah Chen',
                'followers': 15000,
                'bio': 'Founder of sustainable beauty brand | Clean skincare',
                'website': 'sustainablebeautyco.com',
                'engagement_rate': 3.5,
                'recent_posts': 12,
                'industry': 'beauty',
                'found_via': hashtags[0] if hashtags else 'search'
            }
        ]
        
        print(f"✅ Found {len(sample_leads)} potential leads on Instagram")
        return sample_leads
    
    def search_linkedin_leads(self, keywords: List[str], location: str = "", max_results: int = 50) -> List[Dict]:
        """
        Search LinkedIn for creative entrepreneurs and brand founders.
        Requires LinkedIn API access or Sales Navigator.
        """
        print(f"🔍 Searching LinkedIn with keywords: {keywords}")
        
        leads = []
        
        # Sample structure - integrate with LinkedIn API in production
        sample_leads = [
            {
                'platform': 'linkedin',
                'name': 'Emily Rodriguez',
                'title': 'Founder & Creative Director',
                'company': 'Lumière Lifestyle',
                'industry': 'lifestyle',
                'location': 'New York, NY',
                'profile_url': 'linkedin.com/in/emilyrodriguez',
                'company_size': '1-10 employees',
                'founded_year': 2023,
                'website': 'lumierelifestyle.com'
            }
        ]
        
        print(f"✅ Found {len(sample_leads)} potential leads on LinkedIn")
        return sample_leads
    
    def find_email(self, name: str, company: str, domain: str = "") -> Optional[str]:
        """
        Find email address using Hunter.io API or pattern matching.
        """
        if not self.hunter_api_key:
            # Generate common email patterns
            first_name = name.split()[0].lower() if name else ""
            last_name = name.split()[-1].lower() if len(name.split()) > 1 else ""
            
            if domain:
                patterns = [
                    f"{first_name}@{domain}",
                    f"{first_name}.{last_name}@{domain}",
                    f"{first_name[0]}{last_name}@{domain}",
                    f"hello@{domain}",
                    f"info@{domain}"
                ]
                return patterns[0]  # Return first pattern as guess
            return None
        
        # Use Hunter.io API
        try:
            url = f"https://api.hunter.io/v2/email-finder"
            params = {
                'domain': domain,
                'first_name': name.split()[0] if name else "",
                'last_name': name.split()[-1] if len(name.split()) > 1 else "",
                'api_key': self.hunter_api_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('data', {}).get('email'):
                return data['data']['email']
        except Exception as e:
            print(f"⚠️  Email lookup error: {e}")
        
        return None
    
    def qualify_lead(self, lead: Dict) -> Dict:
        """
        Score and qualify leads based on criteria.
        Returns lead with qualification score.
        """
        score = 0
        reasons = []
        
        # Follower count
        followers = lead.get('followers', 0)
        if followers >= 10000:
            score += 30
            reasons.append(f"Strong following ({followers:,})")
        elif followers >= 5000:
            score += 20
            reasons.append(f"Good following ({followers:,})")
        elif followers >= 1000:
            score += 10
            reasons.append(f"Growing following ({followers:,})")
        
        # Website presence
        if lead.get('website'):
            score += 15
            reasons.append("Has website")
        
        # Industry match
        bio = (lead.get('bio', '') + ' ' + lead.get('title', '')).lower()
        for industry in self.target_industries:
            if industry in bio:
                score += 10
                reasons.append(f"In {industry} industry")
                break
        
        # Title/role match
        for title in self.target_titles:
            if title in bio:
                score += 15
                reasons.append(f"Is {title}")
                break
        
        # Engagement rate
        engagement = lead.get('engagement_rate', 0)
        if engagement >= 3.0:
            score += 15
            reasons.append(f"High engagement ({engagement}%)")
        elif engagement >= 2.0:
            score += 10
            reasons.append(f"Good engagement ({engagement}%)")
        
        # Recent activity
        if lead.get('recent_posts', 0) > 5:
            score += 10
            reasons.append("Active poster")
        
        lead['qualification_score'] = score
        lead['qualification_reasons'] = reasons
        lead['qualified'] = score >= 50  # Threshold for qualified lead
        
        return lead
    
    def generate_personalized_message(self, lead: Dict, channel: str = 'email') -> str:
        """
        Generate personalized outreach message for each lead.
        """
        name = lead.get('name', 'there').split()[0]
        company = lead.get('company', lead.get('username', 'your brand'))
        industry = lead.get('industry', 'creative')
        
        if channel == 'email':
            subject = f"Elevate {company}'s Brand Strategy"
            
            body = f"""Hi {name},

I came across {company} and was impressed by your work in the {industry} space. Your approach to [specific observation based on their content] really resonates with the creative entrepreneurs we work with at COLLIDE.

COLLIDE is a brand-shaping and business development consultancy exclusively for creative entrepreneurs in fashion, beauty, lifestyle, and design. We help founders like you:

• Translate authentic visions into compelling brand identities
• Align strategic positioning with sustainable business metrics  
• Develop cohesive visual identity systems
• Define and reach ideal customers
• Build go-to-market strategies that drive growth

I'd love to share some insights specific to {industry} brands that could support {company}'s evolution.

Would you be open to a quick 15-minute conversation? I can also offer a complimentary brand audit to identify immediate opportunities.

Looking forward to connecting,

[Your Name]
COLLIDE - Brand-Shaping & Business Development
https://collideartistry.com

P.S. We're currently offering our AI-powered brand advisor to a select group of founders. Happy to give you early access."""
            
            return {'subject': subject, 'body': body}
        
        elif channel == 'linkedin':
            message = f"""Hi {name},

Impressed by {company}'s work in {industry}. At COLLIDE, we specialize in brand-shaping and business development for creative entrepreneurs like you.

Would love to share some insights on scaling {industry} brands and explore how we could support {company}'s growth.

Open to a brief chat?

Best,
[Your Name] | COLLIDE"""
            
            return {'message': message}
        
        elif channel == 'instagram':
            message = f"""Love what you're building with {company}! 🎨 

At COLLIDE, we help {industry} founders translate their vision into thriving brands. Would love to connect and share some insights.

Check out our AI brand advisor: [link]

DM me if you'd like to chat! 💬"""
            
            return {'message': message}
        
        return {'message': f"Hi {name}, let's connect!"}
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send personalized email to lead.
        """
        if not self.email_user or not self.email_password:
            print("⚠️  Email credentials not configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # HTML version
            html_body = body.replace('\n', '<br>')
            
            part1 = MIMEText(body, 'plain')
            part2 = MIMEText(html_body, 'html')
            
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False
    
    def run_lead_generation_campaign(self, 
                                    instagram_hashtags: List[str] = None,
                                    linkedin_keywords: List[str] = None,
                                    max_leads: int = 100,
                                    auto_outreach: bool = False):
        """
        Run complete lead generation campaign.
        """
        print("\n" + "="*60)
        print("🎨 COLLIDE AI - Lead Generation Campaign")
        print("="*60 + "\n")
        
        all_leads = []
        
        # Instagram search
        if instagram_hashtags:
            instagram_leads = self.search_instagram_leads(instagram_hashtags, max_leads//2)
            all_leads.extend(instagram_leads)
        
        # LinkedIn search
        if linkedin_keywords:
            linkedin_leads = self.search_linkedin_leads(linkedin_keywords, max_results=max_leads//2)
            all_leads.extend(linkedin_leads)
        
        print(f"\n📊 Total leads found: {len(all_leads)}")
        
        # Qualify leads
        print("\n🎯 Qualifying leads...")
        qualified = []
        for lead in all_leads:
            qualified_lead = self.qualify_lead(lead)
            if qualified_lead['qualified']:
                qualified.append(qualified_lead)
                print(f"✅ {qualified_lead['name']} - Score: {qualified_lead['qualification_score']}")
        
        print(f"\n✨ Qualified leads: {len(qualified)}/{len(all_leads)}")
        
        # Sort by score
        qualified.sort(key=lambda x: x['qualification_score'], reverse=True)
        
        # Find emails
        print("\n📧 Finding email addresses...")
        for lead in qualified:
            if lead.get('website'):
                domain = lead['website'].replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0]
                email = self.find_email(lead['name'], lead.get('company', ''), domain)
                lead['email'] = email
                if email:
                    print(f"✉️  {lead['name']}: {email}")
        
        # Auto outreach (if enabled)
        if auto_outreach:
            print("\n📤 Starting outreach campaign...")
            for lead in qualified[:10]:  # Limit to top 10 for demo
                if lead.get('email'):
                    message_data = self.generate_personalized_message(lead, 'email')
                    success = self.send_email(
                        lead['email'],
                        message_data['subject'],
                        message_data['body']
                    )
                    
                    self.outreach_log.append({
                        'lead': lead['name'],
                        'email': lead['email'],
                        'platform': lead['platform'],
                        'sent_at': datetime.now().isoformat(),
                        'success': success
                    })
        
        # Save results
        self.save_campaign_results(qualified)
        
        return {
            'total_found': len(all_leads),
            'qualified': len(qualified),
            'top_leads': qualified[:20],
            'outreach_sent': len(self.outreach_log)
        }
    
    def save_campaign_results(self, leads: List[Dict]):
        """Save campaign results to JSON file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"leads_campaign_{timestamp}.json"
        
        results = {
            'campaign_date': datetime.now().isoformat(),
            'total_qualified_leads': len(leads),
            'leads': leads,
            'outreach_log': self.outreach_log
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
        return filename
    
    def export_to_csv(self, leads: List[Dict], filename: str = "leads.csv"):
        """Export leads to CSV for CRM import."""
        import csv
        
        if not leads:
            print("No leads to export")
            return
        
        with open(filename, 'w', newline='') as f:
            fieldnames = ['name', 'company', 'email', 'platform', 'industry', 
                         'website', 'qualification_score', 'title', 'location']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            
            writer.writeheader()
            for lead in leads:
                writer.writerow(lead)
        
        print(f"📊 Exported {len(leads)} leads to {filename}")


def main():
    """Demo lead generation campaign."""
    print("\n🚀 COLLIDE AI Lead Generation Tool\n")
    
    # Initialize
    generator = LeadGenerator()
    
    # Configure search
    instagram_hashtags = [
        '#sustainablefashion', '#cleanbeauty', '#luxuryskincare',
        '#independentdesigner', '#fashionbrand', '#beautybrand',
        '#lifestylebrand', '#homewellness'
    ]
    
    linkedin_keywords = [
        'fashion brand founder', 'beauty brand founder',
        'lifestyle brand CEO', 'design studio owner',
        'creative director fashion', 'sustainable beauty founder'
    ]
    
    # Run campaign (demo mode - no auto outreach)
    results = generator.run_lead_generation_campaign(
        instagram_hashtags=instagram_hashtags[:3],
        linkedin_keywords=linkedin_keywords[:2],
        max_leads=20,
        auto_outreach=False  # Set to True to enable actual outreach
    )
    
    print("\n" + "="*60)
    print("📈 CAMPAIGN SUMMARY")
    print("="*60)
    print(f"Total Leads Found: {results['total_found']}")
    print(f"Qualified Leads: {results['qualified']}")
    print(f"Outreach Sent: {results['outreach_sent']}")
    
    print("\n🏆 TOP 5 LEADS:")
    for i, lead in enumerate(results['top_leads'][:5], 1):
        print(f"\n{i}. {lead['name']} - Score: {lead['qualification_score']}")
        print(f"   Platform: {lead['platform']}")
        print(f"   Industry: {lead.get('industry', 'N/A')}")
        print(f"   Reasons: {', '.join(lead['qualification_reasons'])}")
        if lead.get('email'):
            print(f"   Email: {lead['email']}")
    
    print("\n✨ Campaign complete!")


if __name__ == '__main__':
    main()

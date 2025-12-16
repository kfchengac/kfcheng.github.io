"""Background task functions to be enqueued with RQ (or called directly by worker).

Functions should be pure-ish and return JSON-serializable dicts.
"""
import os
from lead_gen import LeadGenerator


def process_lead_campaign(payload: dict):
    """Run the lead generation campaign and return results dict.

    Expected payload keys: instagram_hashtags, linkedin_keywords, max_leads, auto_outreach
    """
    generator = LeadGenerator()

    instagram_hashtags = payload.get('instagram_hashtags', [])
    linkedin_keywords = payload.get('linkedin_keywords', [])
    max_leads = int(payload.get('max_leads', 50))
    auto_outreach = payload.get('auto_outreach', False)

    results = generator.run_lead_generation_campaign(
        instagram_hashtags=instagram_hashtags,
        linkedin_keywords=linkedin_keywords,
        max_leads=max_leads,
        auto_outreach=auto_outreach
    )

    # Optionally transform or redact sensitive fields here
    return results

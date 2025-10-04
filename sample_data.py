"""
Sample data for VisionFlow demonstration
"""

SAMPLE_EXTRACTIONS = [
    {
        "id": 1,
        "url": "https://openai.com",
        "name": "OpenAI",
        "description": "AI research and deployment company creating powerful AI models",
        "features": "GPT models, ChatGPT, DALL-E, Codex, CLIP, Whisper",
        "pricing": "Freemium model with usage-based pricing",
        "extracted_at": "2024-01-15 10:30:00",
        "status": "success"
    },
    {
        "id": 2,
        "url": "https://stripe.com",
        "name": "Stripe",
        "description": "Online payment processing platform for internet businesses",
        "features": "Payment APIs, Fraud prevention, Authorization rates, Recurring billing",
        "pricing": "2.9% + 30¢ per successful charge",
        "extracted_at": "2024-01-15 10:45:00",
        "status": "success"
    },
    {
        "id": 3,
        "url": "https://vercel.com",
        "name": "Vercel",
        "description": "The platform for frontend developers and teams",
        "features": "Edge functions, Automatic deployments, Analytics, Integrations",
        "pricing": "Free tier available, Pro at $20/month",
        "extracted_at": "2024-01-15 11:00:00",
        "status": "success"
    },
    {
        "id": 4,
        "url": "https://github.com/pricing",
        "name": "GitHub",
        "description": "Code hosting platform for version control and collaboration",
        "features": "Git repositories, Code review, CI/CD, Package registry, Security scanning",
        "pricing": "Free for public repos, Team at $4/user/month",
        "extracted_at": "2024-01-15 11:15:00",
        "status": "success"
    },
    {
        "id": 5,
        "url": "https://cloudinary.com",
        "name": "Cloudinary",
        "description": "Cloud-based image and video management platform",
        "features": "Image optimization, Video streaming, AI-powered tagging, Transform on the fly",
        "pricing": "Free tier: 25GB storage, Pro starts at $99/month",
        "extracted_at": "2024-01-15 11:30:00",
        "status": "success"
    }
]

def populate_sample_data():
    """Populate database with sample data for demonstration"""
    from backend.database import add_extraction
    
    print("📊 Adding sample extractions to database...")
    
    for extraction in SAMPLE_EXTRACTIONS:
        try:
            add_extraction(
                url=extraction["url"],
                extracted_data={
                    "name": extraction["name"],
                    "description": extraction["description"],
                    "features": extraction["features"],
                    "pricing": extraction["pricing"]
                },
                raw_html="",
                status=extraction["status"]
            )
            print(f"✅ Added: {extraction['name']}")
        except Exception as e:
            print(f"❌ Failed to add {extraction['name']}: {e}")
    
    print("📊 Sample data population complete!")

if __name__ == '__main__':
    populate_sample_data()

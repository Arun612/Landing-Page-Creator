"""
Business information collection and industry-specific context enhancement.

Provides interactive prompts for gathering business details and a
comprehensive industry guidance map covering 30+ business types.
"""

from typing import Dict, Tuple, Optional


# ═══════════════════════════════════════════════════════════════
#  Interactive collectors
# ═══════════════════════════════════════════════════════════════

def create_sample_business_info() -> Dict:
    """Return a ready-made sample business for quick demos."""
    return {
        "business_name": "TechFlow Solutions",
        "business_type": "SaaS",
        "description": (
            "AI-powered workflow automation platform that streamlines business "
            "processes, reduces manual tasks, and increases team productivity "
            "through intelligent automation and seamless integrations."
        ),
        "target_audience": (
            "Small to medium businesses, operations managers, and teams "
            "looking to optimize their workflows"
        ),
        "goals": (
            "Generate qualified leads, schedule product demos, "
            "and drive subscription sign-ups"
        ),
        "contact_info": {
            "email": "contact@techflow-solutions.com",
            "phone": "+1 (555) 123-4567",
            "address": "123 Innovation Drive, Tech City, CA 94301",
        },
    }


def create_custom_business_info() -> Dict:
    """Interactively collect custom business information from the user."""
    print("\n" + "=" * 50)
    print("CUSTOM BUSINESS INFORMATION CREATOR")
    print("=" * 50)

    info: Dict = {}
    info["business_name"] = input("\nBusiness Name: ").strip()

    business_types = [
        "SaaS", "E-commerce", "Consulting", "Healthcare", "Education",
        "Finance", "Real Estate", "Technology", "Marketing", "Other",
    ]
    print("\nBusiness Type Options:")
    for i, bt in enumerate(business_types, 1):
        print(f"  {i}. {bt}")

    try:
        idx = int(input("\nSelect business type (number): "))
        if 1 <= idx <= len(business_types):
            info["business_type"] = business_types[idx - 1]
        else:
            info["business_type"] = input("Enter custom business type: ").strip()
    except ValueError:
        info["business_type"] = input("Enter business type: ").strip()

    info["description"] = input("\nBusiness Description (detailed): ").strip()
    info["target_audience"] = input("\nTarget Audience: ").strip()
    info["goals"] = input("\nLanding Page Goals: ").strip()

    print("\nContact Information:")
    info["contact_info"] = {
        "email": input("  Email: ").strip(),
        "phone": input("  Phone: ").strip(),
        "address": input("  Address (optional): ").strip(),
    }
    return info


def get_theme_choice() -> str:
    """Prompt the user to select a visual theme."""
    print("\n🎨 THEME OPTIONS:")
    print("1. Light Theme (Clean, bright, professional)")
    print("2. Dark Theme  (Modern, sleek, high-contrast)")

    while True:
        try:
            choice = int(input("\n🎯 Select theme option (1-2): "))
            if choice in (1, 2):
                return {1: "light", 2: "dark"}[choice]
            print("❌ Please select 1-2")
        except ValueError:
            print("❌ Please enter a valid number (1-2)")


def get_image_choice() -> Tuple[str, Optional[str]]:
    """Prompt the user to select an image generation method."""
    print("\n🖼️  IMAGE GENERATION OPTIONS:")
    print("1. DALL-E 3 (AI-generated custom images)")
    print("2. Pixabay  (Professional stock photos)")
    print("3. Both     (DALL-E first, Pixabay fallback)")
    print("4. User URL (Provide your own hero image link)")
    print("5. None     (No hero image)")

    while True:
        try:
            choice = int(input("\n🎯 Select image option (1-5): "))
            if choice not in range(1, 6):
                print("❌ Please select 1-5")
                continue

            choice_map = {1: "dalle", 2: "pixabay", 3: "both", 4: "user_url", 5: "none"}
            selected = choice_map[choice]

            if selected == "user_url":
                url = input("\n🔗 Enter your hero image URL: ").strip()
                if not url:
                    print("❌ Please provide a valid URL")
                    continue
                return selected, url

            return selected, None
        except ValueError:
            print("❌ Please enter a valid number (1-5)")


# ═══════════════════════════════════════════════════════════════
#  Industry guidance map  (30+ verticals)
# ═══════════════════════════════════════════════════════════════

_INDUSTRY_GUIDANCE: Dict[str, Dict] = {
    # ── Tech & Digital ───────────────────────────────────────
    "saas": {
        "key_values": ["efficiency", "automation", "scalability", "integration"],
        "tone": "innovative, technical yet approachable",
        "focus_areas": ["features", "integrations", "pricing", "demos"],
        "cta_style": "trial-focused",
        "visual_style": "tech-forward, gradient backgrounds",
        "social_proof": "user metrics and enterprise logos",
        "urgency_type": "limited-time trial offers",
    },
    "mobile_app": {
        "key_values": ["convenience", "speed", "user-friendly", "lifestyle"],
        "tone": "casual, lifestyle-oriented",
        "focus_areas": ["app features", "screenshots", "ratings", "download"],
        "cta_style": "download-focused",
        "visual_style": "mobile mockups, app store badges",
        "social_proof": "app store ratings and download counts",
        "urgency_type": "limited-time download bonuses",
    },
    # ── Healthcare & Wellness ────────────────────────────────
    "healthcare": {
        "key_values": ["trust", "expertise", "care", "results", "safety"],
        "tone": "professional, caring, authoritative",
        "focus_areas": ["credentials", "services", "patient care", "technology"],
        "cta_style": "appointment-focused",
        "visual_style": "clean, medical imagery, trust badges",
        "social_proof": "patient testimonials and certifications",
        "urgency_type": "limited appointment availability",
    },
    "dental": {
        "key_values": ["comfort", "modern technology", "gentle care", "results"],
        "tone": "reassuring, friendly, professional",
        "focus_areas": ["services", "technology", "comfort", "insurance"],
        "cta_style": "appointment-booking",
        "visual_style": "bright, welcoming, before/after",
        "social_proof": "patient reviews and technology certifications",
        "urgency_type": "limited new patient slots",
    },
    "fitness": {
        "key_values": ["transformation", "energy", "community", "results"],
        "tone": "motivational, energetic, supportive",
        "focus_areas": ["programs", "trainers", "results", "membership"],
        "cta_style": "trial-class focused",
        "visual_style": "dynamic, action shots, progress images",
        "social_proof": "transformation photos and member testimonials",
        "urgency_type": "limited membership availability",
    },
    "spa": {
        "key_values": ["relaxation", "luxury", "rejuvenation", "self-care"],
        "tone": "calming, luxurious, inviting",
        "focus_areas": ["services", "ambiance", "products", "packages"],
        "cta_style": "booking-focused",
        "visual_style": "serene, luxury imagery, soft colors",
        "social_proof": "client testimonials and luxury certifications",
        "urgency_type": "seasonal package offers",
    },
    # ── E-commerce & Retail ──────────────────────────────────
    "ecommerce": {
        "key_values": ["quality", "selection", "value", "convenience"],
        "tone": "enthusiastic, trustworthy, customer-focused",
        "focus_areas": ["products", "pricing", "shipping", "guarantees"],
        "cta_style": "purchase-focused",
        "visual_style": "product-focused, lifestyle imagery",
        "social_proof": "customer reviews and purchase counts",
        "urgency_type": "low stock alerts and flash sales",
    },
    "fashion": {
        "key_values": ["style", "trendy", "quality", "expression"],
        "tone": "stylish, aspirational, confident",
        "focus_areas": ["collections", "styling", "quality", "sustainability"],
        "cta_style": "shop-now focused",
        "visual_style": "editorial, lifestyle, model shots",
        "social_proof": "influencer endorsements and customer photos",
        "urgency_type": "limited collection drops",
    },
    "jewelry": {
        "key_values": ["elegance", "craftsmanship", "timeless", "luxury"],
        "tone": "elegant, sophisticated, personal",
        "focus_areas": ["craftsmanship", "materials", "customization", "warranty"],
        "cta_style": "consultation-focused",
        "visual_style": "luxury, close-ups, elegant backgrounds",
        "social_proof": "customer testimonials and craftsmanship certifications",
        "urgency_type": "limited edition pieces",
    },
    # ── Food & Beverage ──────────────────────────────────────
    "restaurant": {
        "key_values": ["taste", "ambiance", "service", "experience"],
        "tone": "inviting, descriptive, warm",
        "focus_areas": ["menu", "ambiance", "location", "reviews"],
        "cta_style": "reservation-focused",
        "visual_style": "food photography, interior shots",
        "social_proof": "diner reviews and chef credentials",
        "urgency_type": "limited table availability",
    },
    "catering": {
        "key_values": ["customization", "quality", "service", "reliability"],
        "tone": "professional, accommodating, detailed",
        "focus_areas": ["menu options", "service types", "testimonials", "gallery"],
        "cta_style": "quote-request focused",
        "visual_style": "event shots, food displays",
        "social_proof": "event testimonials and portfolio",
        "urgency_type": "booking calendar filling up",
    },
    "cafe": {
        "key_values": ["atmosphere", "quality", "community", "comfort"],
        "tone": "cozy, friendly, inviting",
        "focus_areas": ["menu", "atmosphere", "location", "hours"],
        "cta_style": "visit-focused",
        "visual_style": "warm, cozy interior, coffee shots",
        "social_proof": "regular customer testimonials and ratings",
        "urgency_type": "daily specials and limited offerings",
    },
    # ── Professional Services ────────────────────────────────
    "consulting": {
        "key_values": ["expertise", "results", "strategy", "ROI"],
        "tone": "authoritative, results-driven, strategic",
        "focus_areas": ["methodology", "case studies", "team", "industries"],
        "cta_style": "consultation-focused",
        "visual_style": "professional, data-driven, corporate",
        "social_proof": "client results and case studies",
        "urgency_type": "limited consultation slots",
    },
    "legal": {
        "key_values": ["expertise", "trust", "advocacy", "results"],
        "tone": "confident, reassuring, professional",
        "focus_areas": ["practice areas", "experience", "testimonials", "process"],
        "cta_style": "consultation-focused",
        "visual_style": "professional, trustworthy, serious",
        "social_proof": "case results and client testimonials",
        "urgency_type": "time-sensitive legal matters",
    },
    "accounting": {
        "key_values": ["accuracy", "compliance", "savings", "peace of mind"],
        "tone": "professional, dependable, clear",
        "focus_areas": ["services", "expertise", "technology", "pricing"],
        "cta_style": "consultation-focused",
        "visual_style": "clean, professional, organized",
        "social_proof": "client testimonials and certifications",
        "urgency_type": "tax deadline urgency",
    },
    "marketing_agency": {
        "key_values": ["creativity", "results", "innovation", "growth"],
        "tone": "creative, confident, results-oriented",
        "focus_areas": ["services", "portfolio", "results", "process"],
        "cta_style": "project-inquiry focused",
        "visual_style": "bold, creative, portfolio-showcase",
        "social_proof": "client success stories and portfolio",
        "urgency_type": "limited project capacity",
    },
    # ── Events & Entertainment ───────────────────────────────
    "events": {
        "key_values": ["experience", "networking", "learning", "memorable"],
        "tone": "exciting, exclusive, engaging",
        "focus_areas": ["agenda", "speakers", "venue", "networking"],
        "cta_style": "ticket-purchase focused",
        "visual_style": "energetic, crowd shots, speaker photos",
        "social_proof": "attendee testimonials and speaker lineup",
        "urgency_type": "limited tickets and early bird pricing",
    },
    "wedding": {
        "key_values": ["romance", "perfection", "memories", "elegance"],
        "tone": "romantic, detailed, reassuring",
        "focus_areas": ["packages", "venues", "services", "gallery"],
        "cta_style": "consultation-focused",
        "visual_style": "romantic, elegant, ceremony/reception shots",
        "social_proof": "couple testimonials and wedding portfolio",
        "urgency_type": "prime date availability",
    },
    "concert": {
        "key_values": ["excitement", "performance", "atmosphere", "unforgettable"],
        "tone": "energetic, enthusiastic, hyped",
        "focus_areas": ["lineup", "venue", "tickets", "experience"],
        "cta_style": "ticket-purchase urgent",
        "visual_style": "dynamic, stage shots, crowd energy",
        "social_proof": "fan testimonials and past event highlights",
        "urgency_type": "tickets selling fast",
    },
    # ── Education & Training ─────────────────────────────────
    "education": {
        "key_values": ["learning", "career growth", "expertise", "certification"],
        "tone": "encouraging, authoritative, supportive",
        "focus_areas": ["curriculum", "instructors", "outcomes", "support"],
        "cta_style": "enrollment-focused",
        "visual_style": "educational, success stories, learning environment",
        "social_proof": "graduate success stories and placement rates",
        "urgency_type": "enrollment deadlines",
    },
    "online_course": {
        "key_values": ["flexibility", "expert instruction", "practical skills", "certification"],
        "tone": "accessible, empowering, clear",
        "focus_areas": ["curriculum", "format", "outcomes", "testimonials"],
        "cta_style": "enrollment-focused",
        "visual_style": "digital, screen mockups, student success",
        "social_proof": "student testimonials and completion rates",
        "urgency_type": "limited enrollment periods",
    },
    # ── Real Estate & Property ───────────────────────────────
    "realestate": {
        "key_values": ["location", "value", "service", "expertise"],
        "tone": "professional, knowledgeable, trustworthy",
        "focus_areas": ["listings", "services", "market knowledge", "testimonials"],
        "cta_style": "viewing-schedule focused",
        "visual_style": "property photos, luxury aesthetic",
        "social_proof": "sold properties and client testimonials",
        "urgency_type": "market condition urgency",
    },
    "property_management": {
        "key_values": ["reliability", "maintenance", "tenant satisfaction", "ROI"],
        "tone": "professional, dependable, efficient",
        "focus_areas": ["services", "process", "technology", "pricing"],
        "cta_style": "consultation-focused",
        "visual_style": "professional, property showcase",
        "social_proof": "property owner testimonials and portfolio",
        "urgency_type": "property management openings",
    },
    # ── Financial Services ───────────────────────────────────
    "finance": {
        "key_values": ["security", "growth", "expertise", "transparency"],
        "tone": "trustworthy, professional, clear",
        "focus_areas": ["services", "security", "returns", "process"],
        "cta_style": "signup/consultation focused",
        "visual_style": "secure, professional, data visualization",
        "social_proof": "user success metrics and security certifications",
        "urgency_type": "limited-time rate offers",
    },
    "insurance": {
        "key_values": ["protection", "peace of mind", "coverage", "support"],
        "tone": "reassuring, clear, helpful",
        "focus_areas": ["coverage types", "process", "claims", "pricing"],
        "cta_style": "quote-request focused",
        "visual_style": "trustworthy, family-focused, protective",
        "social_proof": "policyholder testimonials and coverage examples",
        "urgency_type": "rate changes and coverage deadlines",
    },
    # ── Home & Lifestyle ─────────────────────────────────────
    "interior_design": {
        "key_values": ["aesthetics", "functionality", "personalization", "quality"],
        "tone": "creative, sophisticated, consultative",
        "focus_areas": ["portfolio", "process", "services", "style"],
        "cta_style": "consultation-focused",
        "visual_style": "portfolio-heavy, before/after, styled spaces",
        "social_proof": "client testimonials and project portfolio",
        "urgency_type": "limited project availability",
    },
    "landscaping": {
        "key_values": ["beauty", "maintenance", "expertise", "transformation"],
        "tone": "professional, creative, reliable",
        "focus_areas": ["services", "portfolio", "maintenance", "process"],
        "cta_style": "quote-request focused",
        "visual_style": "outdoor photography, before/after, seasonal",
        "social_proof": "client testimonials and project photos",
        "urgency_type": "seasonal booking windows",
    },
    "cleaning": {
        "key_values": ["reliability", "thoroughness", "convenience", "trust"],
        "tone": "friendly, professional, dependable",
        "focus_areas": ["services", "process", "pricing", "guarantee"],
        "cta_style": "booking-focused",
        "visual_style": "clean spaces, before/after, professional",
        "social_proof": "customer testimonials and service guarantees",
        "urgency_type": "booking availability",
    },
    # ── Automotive ───────────────────────────────────────────
    "automotive": {
        "key_values": ["quality", "reliability", "service", "value"],
        "tone": "knowledgeable, trustworthy, enthusiastic",
        "focus_areas": ["inventory", "services", "financing", "reviews"],
        "cta_style": "test-drive/service focused",
        "visual_style": "vehicle photography, showroom, action shots",
        "social_proof": "customer reviews and service ratings",
        "urgency_type": "limited inventory and seasonal offers",
    },
    # ── Non-Profit & Sustainability ──────────────────────────
    "nonprofit": {
        "key_values": ["impact", "mission", "transparency", "community"],
        "tone": "inspiring, authentic, mission-driven",
        "focus_areas": ["mission", "impact", "programs", "involvement"],
        "cta_style": "donation/volunteer focused",
        "visual_style": "impact imagery, community, beneficiaries",
        "social_proof": "impact metrics and beneficiary stories",
        "urgency_type": "campaign deadlines and matching gifts",
    },
    "sustainability": {
        "key_values": ["impact", "responsibility", "innovation", "future"],
        "tone": "purposeful, optimistic, informative",
        "focus_areas": ["mission", "products", "impact", "community"],
        "cta_style": "engagement-focused",
        "visual_style": "nature, impact metrics, sustainable practices",
        "social_proof": "environmental impact data and community size",
        "urgency_type": "environmental urgency and collective action",
    },
    # ── Pet Services ─────────────────────────────────────────
    "pet_services": {
        "key_values": ["care", "safety", "love", "expertise"],
        "tone": "warm, caring, professional",
        "focus_areas": ["services", "facility", "staff", "safety"],
        "cta_style": "booking-focused",
        "visual_style": "pet photography, facility, happy pets",
        "social_proof": "pet owner testimonials and facility certifications",
        "urgency_type": "boarding and grooming availability",
    },
    # ── Technology ───────────────────────────────────────────
    "technology": {
        "key_values": ["innovation", "reliability", "performance", "support"],
        "tone": "technical, confident, forward-thinking",
        "focus_areas": ["products", "specifications", "support", "integration"],
        "cta_style": "demo/trial focused",
        "visual_style": "tech-forward, product shots, diagrams",
        "social_proof": "user reviews and technical certifications",
        "urgency_type": "product launches and limited offers",
    },
    # ── Default fallback ─────────────────────────────────────
    "general": {
        "key_values": ["quality", "service", "trust", "value", "results"],
        "tone": "professional, friendly, trustworthy",
        "focus_areas": ["services", "benefits", "testimonials", "contact"],
        "cta_style": "inquiry-focused",
        "visual_style": "clean, professional, versatile",
        "social_proof": "customer testimonials and ratings",
        "urgency_type": "limited availability",
    },
}


def enhance_business_context(business_info: Dict) -> Dict:
    """
    Enrich business info with industry-specific guidance.

    Performs fuzzy matching on the business_type field to find the
    closest industry vertical, then attaches the guidance dict.
    """
    btype = business_info.get("business_type", "").lower()

    matched = "general"
    for key in _INDUSTRY_GUIDANCE:
        if key in btype or btype in key:
            matched = key
            break

    business_info["industry_guidance"] = _INDUSTRY_GUIDANCE[matched]
    business_info["business_type_normalized"] = matched
    return business_info

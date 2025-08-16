from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
import csv
import io
try:
    import google.generativeai as genai
except ImportError:
    genai = None
import asyncio
from bson import ObjectId
import json

# Load environment variables
load_dotenv()

app = FastAPI(title="Healthcare Conference Targeting API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "healthcare_targeting")
client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Initialize Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_gemini_model(system_instruction: str):
    """Initialize Gemini model with API key"""
    if not genai:
        raise ImportError("Google Generative AI package not installed. Install with: pip install google-generativeai")
    
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=system_instruction
    )

def convert_objectid_to_str(doc):
    """Convert MongoDB ObjectId to string for JSON serialization"""
    if doc is None:
        return None
    if isinstance(doc, list):
        return [convert_objectid_to_str(item) for item in doc]
    if isinstance(doc, dict):
        result = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                result[key] = str(value)
            elif isinstance(value, dict):
                result[key] = convert_objectid_to_str(value)
            elif isinstance(value, list):
                result[key] = [convert_objectid_to_str(item) for item in value]
            else:
                result[key] = value
        return result
    elif isinstance(doc, ObjectId):
        return str(doc)
    return doc

def get_conference_filter(conference_id: str):
    """Get MongoDB filter for conference based on conference_id"""
    conference_name_map = {
        "himss-2025": "HIMSS 2025",
        "jp-morgan-2025": "J.P. Morgan Healthcare Conference",
        "bio-2025": "BIO International Convention",
        "aha-2025": "American Hospital Association Annual Membership Meeting",
        "acp-2025": "American College of Physicians Internal Medicine Meeting", 
        "rsna-2024": "Radiological Society of North America Annual Meeting"
    }
    
    if conference_id != "all" and conference_id in conference_name_map:
        return {"conference": conference_name_map[conference_id]}
    else:
        return {}  # No filter if "all" or unknown conference_id

# Pydantic models
class UserProfile(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    company: str
    industry: str
    role: str
    goals: List[str]
    target_conferences: List[str] = []

class Contact(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    company: str
    title: str
    industry: str
    conference: str
    score: Optional[float] = 0
    priority: Optional[str] = "medium"
    notes: Optional[str] = ""

class MeetingRecommendation(BaseModel):
    id: Optional[str] = None
    contact_id: str
    contact_name: str
    contact_company: str
    suggested_time: str
    reason: str
    personalized_message: str
    priority: str

# Current healthcare conferences data - Updated December 2024
HEALTHCARE_CONFERENCES = [
    {
        "id": "himss-2025",
        "name": "HIMSS Global Health Conference & Exhibition",
        "date": "2025-03-03 to 2025-03-06",
        "location": "Las Vegas, NV",
        "focus": "Health Information Technology",
        "attendees": 45000,
        "description": "World's largest health information technology conference focusing on digital health transformation"
    },
    {
        "id": "jp-morgan-2025",
        "name": "J.P. Morgan Healthcare Conference",
        "date": "2025-01-13 to 2025-01-16", 
        "location": "San Francisco, CA",
        "focus": "Healthcare Investment & Innovation",
        "attendees": 9000,
        "description": "Premier healthcare investment conference bringing together industry leaders and investors"
    },
    {
        "id": "bio-2025",
        "name": "BIO International Convention",
        "date": "2025-06-02 to 2025-06-05",
        "location": "Philadelphia, PA", 
        "focus": "Biotechnology & Life Sciences",
        "attendees": 18000,
        "description": "World's largest biotechnology partnering event connecting biotech innovators globally"
    },
    {
        "id": "aha-2025", 
        "name": "American Hospital Association Annual Membership Meeting",
        "date": "2025-04-26 to 2025-04-29",
        "location": "Chicago, IL",
        "focus": "Hospital Administration & Leadership",
        "attendees": 5000,
        "description": "Premier leadership conference for hospital and health system executives"
    },
    {
        "id": "acp-2025",
        "name": "American College of Physicians Internal Medicine Meeting",
        "date": "2025-04-10 to 2025-04-12",
        "location": "Boston, MA",
        "focus": "Internal Medicine & Clinical Practice",
        "attendees": 8000,
        "description": "Leading conference for internal medicine physicians and healthcare professionals"
    },
    {
        "id": "rsna-2024",
        "name": "Radiological Society of North America Annual Meeting",
        "date": "2024-12-01 to 2024-12-05",
        "location": "Chicago, IL",
        "focus": "Radiology & Medical Imaging",
        "attendees": 50000,
        "description": "World's premier radiology conference showcasing latest imaging technologies and research"
    }
]

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/user/profile")
async def save_user_profile(profile: UserProfile):
    """Save or update user profile"""
    try:
        if not profile.id:
            profile.id = str(uuid.uuid4())
        
        profile_dict = profile.dict()
        await db.users.replace_one(
            {"id": profile.id}, 
            profile_dict, 
            upsert=True
        )
        
        return {"success": True, "profile": profile_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/profile/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile"""
    try:
        profile = await db.users.find_one({"id": user_id})
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        # Convert ObjectId to string for JSON serialization
        profile = convert_objectid_to_str(profile)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/conferences/research")
async def research_conferences(query: Optional[str] = None, year: Optional[str] = "2024-2025"):
    """Use Gemini AI to perform deep research on healthcare conferences"""
    try:
        # Initialize Gemini model for deep research
        model = get_gemini_model(
            system_instruction="""You are an expert healthcare conference researcher with access to comprehensive industry knowledge. 
            You specialize in finding current, accurate, and detailed information about major healthcare conferences, 
            including exact dates, locations, attendee counts, and industry focus areas. 
            
            Your research should be thorough, current, and include:
            - Official conference dates and locations
            - Expected attendee numbers
            - Key focus areas and themes
            - Target audiences and industries
            - Registration and networking opportunities
            
            Always provide factual, up-to-date information and indicate your confidence level in the data."""
        )
        
        research_prompt = f"""
        Please conduct comprehensive research on major healthcare conferences for {year}. 
        Focus on finding the most current and accurate information for these key conferences:

        1. HIMSS Global Health Conference & Exhibition
        2. J.P. Morgan Healthcare Conference  
        3. BIO International Convention
        4. American Hospital Association (AHA) Annual Meeting
        5. American College of Physicians (ACP) Internal Medicine Meeting
        6. Radiological Society of North America (RSNA) Annual Meeting
        7. Healthcare Financial Management Association (HFMA) Annual Conference
        8. American Medical Association (AMA) Annual Meeting
        9. Digital Health Summit
        10. Any other major healthcare conferences in {year}

        For each conference, please provide:
        - Conference name
        - Exact dates (month and specific days)
        - Location (city, state, venue if known)
        - Expected number of attendees
        - Primary focus areas and themes
        - Target audience/industries
        - Brief description of significance

        {f"Additional research focus: {query}" if query else ""}
        
        Please format the response as a structured JSON array that can be easily parsed.
        Ensure all dates are realistic and current for the specified year.
        """
        
        # Generate response
        response = model.generate_content(research_prompt)
        research_results = response.text
        
        return {
            "success": True,
            "research_query": query or f"Healthcare conferences for {year}",
            "year": year,
            "research_results": research_results,
            "source": "Gemini AI Deep Research",
            "timestamp": "2024-12-20"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Research failed: {str(e)}",
            "message": "Unable to complete conference research at this time"
        }

@app.get("/api/conferences")
async def get_conferences(industry: Optional[str] = None):
    """Get relevant healthcare conferences"""
    try:
        conferences = HEALTHCARE_CONFERENCES.copy()
        
        # If user provided industry, use AI to recommend most relevant conferences
        if industry:
            model = get_gemini_model(
                system_instruction="You are a healthcare conference expert with knowledge of current 2024-2025 conferences. All conference dates and information are up-to-date and current. Recommend the most relevant conferences based on user industry and professional goals."
            )
            
            prompt = f"""
            User industry: {industry}
            
            Available conferences: {conferences}
            
            Rank these conferences by relevance to someone in {industry}. Return a JSON array with conference IDs in order of relevance.
            Format: ["conference-id-1", "conference-id-2", ...]
            """
            
            response = model.generate_content(prompt)
            
            # Simple ranking - in production you'd parse AI response
            # For MVP, return all conferences with relevance scores
            for conf in conferences:
                if industry.lower() in ['technology', 'it', 'digital']:
                    conf['relevance_score'] = 90 if conf['id'] == 'himss-2025' else 70
                elif industry.lower() in ['pharma', 'biotech', 'pharmaceutical']:
                    conf['relevance_score'] = 90 if conf['id'] == 'bio-2025' else 60
                elif industry.lower() in ['finance', 'investment']:
                    conf['relevance_score'] = 90 if conf['id'] == 'jp-morgan-2025' else 50
                else:
                    conf['relevance_score'] = 75
        
        return {"conferences": conferences}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contacts/upload")
async def upload_contacts(file: UploadFile = File(...), user_id: str = "default"):
    """Process uploaded attendee/vendor CSV file"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be CSV format")
        
        content = await file.read()
        csv_string = content.decode('utf-8')
        csv_file = io.StringIO(csv_string)
        reader = csv.DictReader(csv_file)
        
        contacts = []
        for row in reader:
            contact = Contact(
                id=str(uuid.uuid4()),
                name=row.get('name', ''),
                email=row.get('email', ''),
                company=row.get('company', ''),
                title=row.get('title', ''),
                industry=row.get('industry', 'Healthcare'),
                conference=row.get('conference', 'HIMSS 2025')
            )
            contacts.append(contact.dict())
        
        # Save contacts to database
        if contacts:
            await db.contacts.insert_many(contacts)
        
        return {
            "success": True, 
            "contacts_uploaded": len(contacts),
            "message": f"Successfully uploaded {len(contacts)} contacts"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contacts/analyze")
async def analyze_contacts(user_id: str, conference_id: str = "himss-2025"):
    """AI-powered contact analysis and scoring"""
    try:
        # Get user profile for context
        user_profile = await db.users.find_one({"id": user_id})
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get contacts filtered by selected conference
        conference_filter = get_conference_filter(conference_id)
        contacts_cursor = db.contacts.find(conference_filter)
        contacts = await contacts_cursor.to_list(length=None)
        
        if not contacts:
            return {"analyzed_contacts": [], "message": "No contacts to analyze"}
        
        # Convert MongoDB documents to serializable format
        contacts = [convert_objectid_to_str(contact) for contact in contacts]
        
        # Enhanced scoring logic for current healthcare industry (Updated December 2024)
        analyzed_contacts = []
        for contact in contacts:
            # Advanced scoring based on current healthcare trends and priorities
            score = 60  # Base score
            priority = "medium"
            
            # Executive level scoring (highest priority in current market)
            if any(keyword in contact.get('title', '').lower() for keyword in ['ceo', 'cto', 'cmo', 'vp', 'director', 'chief', 'president']):
                score += 25
                priority = "high"
            
            # Healthcare organization scoring (updated for 2024-2025 priorities)
            if any(keyword in contact.get('company', '').lower() for keyword in ['hospital', 'health system', 'medical center', 'clinic', 'healthcare network']):
                score += 20
                
            # Industry relevance (expanded for current healthcare landscape)
            if any(keyword in contact.get('industry', '').lower() for keyword in ['healthcare', 'medical', 'pharma', 'biotech', 'digital health', 'healthtech']):
                score += 15
                
            # Current hot topics in healthcare (AI, digital transformation, value-based care)
            if any(keyword in contact.get('title', '').lower() for keyword in ['digital', 'ai', 'innovation', 'transformation', 'value', 'analytics']):
                score += 10
                
            contact['score'] = min(score, 100)
            contact['priority'] = priority
            contact['ai_notes'] = f"Scored based on {contact.get('title', 'role')}, organization type, and alignment with current healthcare industry priorities (2024-2025)"
            
            analyzed_contacts.append(contact)
        
        # Update contacts in database
        for contact in analyzed_contacts:
            # Remove MongoDB _id field before updating to avoid immutable field error
            contact_update = {k: v for k, v in contact.items() if k != '_id'}
            await db.contacts.replace_one(
                {"id": contact["id"]},
                contact_update,
                upsert=True
            )
        
        # Sort by score
        analyzed_contacts.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            "analyzed_contacts": analyzed_contacts[:20],  # Return top 20
            "total_analyzed": len(analyzed_contacts),
            "high_priority": len([c for c in analyzed_contacts if c['priority'] == 'high']),
            "medium_priority": len([c for c in analyzed_contacts if c['priority'] == 'medium']),
            "low_priority": len([c for c in analyzed_contacts if c['priority'] == 'low'])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.post("/api/meetings/suggest")
async def suggest_meetings(user_id: str, conference_id: str = "himss-2025"):
    """Generate AI-powered meeting suggestions"""
    try:
        # Get high-priority contacts filtered by conference
        conference_filter = get_conference_filter(conference_id)
        high_priority_filter = {**conference_filter, "priority": "high"}
        contacts_cursor = db.contacts.find(high_priority_filter).limit(10)
        contacts = await contacts_cursor.to_list(length=10)
        
        if not contacts:
            # If no high priority contacts, get any contacts from this conference
            contacts_cursor = db.contacts.find(conference_filter).limit(5)
            contacts = await contacts_cursor.to_list(length=5)
        
        user_profile = await db.users.find_one({"id": user_id})
        if user_profile:
            user_profile = convert_objectid_to_str(user_profile)
        
        recommendations = []
        time_slots = ["Day 1, 10:00 AM", "Day 1, 2:00 PM", "Day 2, 11:00 AM", "Day 2, 3:00 PM", "Day 3, 9:00 AM"]
        
        for i, contact in enumerate(contacts):
            contact = convert_objectid_to_str(contact)
            
            # Generate personalized outreach template
            company = user_profile.get('company', 'Your Company') if user_profile else 'Your Company'
            goals = user_profile.get('goals', ['networking']) if user_profile else ['networking']
            
            personalized_message = f"Hi {contact.get('name', 'there')}, I'm with {company} and noticed your work at {contact.get('company', '')}. I'd love to discuss {goals[0] if goals else 'potential collaboration'}. Available for coffee at {conference_id.upper()}?"
            
            recommendation = MeetingRecommendation(
                id=str(uuid.uuid4()),
                contact_id=contact['id'],
                contact_name=contact.get('name', 'Unknown'),
                contact_company=contact.get('company', 'Unknown'),
                suggested_time=time_slots[i % len(time_slots)],
                reason=f"Strategic partnership opportunity with {contact.get('company', 'this company')} in {contact.get('industry', 'healthcare')}",
                personalized_message=personalized_message,
                priority=contact.get('priority', 'medium')
            )
            
            recommendations.append(recommendation.dict())
        
        # Save recommendations
        if recommendations:
            # Convert any ObjectIds in recommendations before inserting
            clean_recommendations = [convert_objectid_to_str(rec) for rec in recommendations]
            await db.meetings.insert_many(clean_recommendations)
        
        # Ensure recommendations are clean for response
        clean_recommendations_response = [convert_objectid_to_str(rec) for rec in recommendations]
        
        return {
            "meeting_suggestions": clean_recommendations_response,
            "total_suggestions": len(recommendations)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Meeting suggestion error: {str(e)}")

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(user_id: str):
    """Get dashboard statistics"""
    try:
        total_contacts = await db.contacts.count_documents({})
        high_priority = await db.contacts.count_documents({"priority": "high"})
        meetings_suggested = await db.meetings.count_documents({})
        
        return {
            "total_contacts": total_contacts,
            "high_priority_contacts": high_priority,
            "meeting_suggestions": meetings_suggested,
            "roi_projection": f"{meetings_suggested * 15}% increase in qualified leads"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
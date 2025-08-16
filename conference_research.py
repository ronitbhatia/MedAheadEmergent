#!/usr/bin/env python3
"""
Healthcare Conference Deep Research Tool
Uses Gemini AI to find comprehensive, up-to-date conference information
"""

import asyncio
import os
from dotenv import load_dotenv
try:
    import google.generativeai as genai
except ImportError:
    print("❌ Google Generative AI package not installed.")
    print("Please install it with: pip install google-generativeai")
    exit(1)

# Load environment variables
load_dotenv()

async def deep_research_conferences():
    """Use Gemini AI to perform deep research on healthcare conferences"""
    
    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment variables")
        print("Please set your Gemini API key in the environment or .env file")
        return
    
    try:
        # Configure Gemini AI
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction="""You are an expert healthcare conference researcher with access to comprehensive industry knowledge. 
            You specialize in finding current, accurate, and detailed information about major healthcare conferences, 
            including exact dates, locations, attendee counts, and industry focus areas. 
            
            Your research should be thorough, current, and include:
            - Official conference dates and locations for 2024-2025
            - Expected attendee numbers
            - Key focus areas and themes
            - Target audiences and industries
            - Registration and networking opportunities
            
            Always provide factual, up-to-date information and clearly indicate your confidence level in the data.
            Format responses in clear, structured JSON when possible for easy parsing."""
        )
        
        research_prompt = """
        Please conduct comprehensive research on major healthcare conferences for 2024-2025. 
        Focus on finding the most current and accurate information for these key conferences:

        1. HIMSS Global Health Conference & Exhibition 2025
        2. J.P. Morgan Healthcare Conference 2025
        3. BIO International Convention 2025
        4. American Hospital Association (AHA) Annual Meeting 2025
        5. American College of Physicians (ACP) Internal Medicine Meeting 2025
        6. Radiological Society of North America (RSNA) Annual Meeting 2024
        7. Healthcare Financial Management Association (HFMA) Annual Conference 2025
        8. American Medical Association (AMA) Annual Meeting 2025
        9. Digital Health Summit 2025
        10. Any other major healthcare conferences in 2024-2025

        For each conference, please provide:
        - Conference name and year
        - Exact dates (month and specific days)
        - Location (city, state, venue if known)
        - Expected number of attendees
        - Primary focus areas and themes
        - Target audience/industries
        - Brief description of significance in the healthcare industry
        - Website or registration information if available

        Please format the response as a well-structured JSON array that can be easily parsed.
        Ensure all dates are realistic and current for 2024-2025.
        Include your confidence level for each piece of information (High/Medium/Low).
        """
        
        print("🔍 Starting deep research on healthcare conferences...")
        print("Using Gemini AI to find comprehensive conference information...\n")
        
        # Generate response
        response = model.generate_content(research_prompt)
        research_results = response.text
        
        print("✅ Research completed! Here are the results:\n")
        print("=" * 80)
        print("HEALTHCARE CONFERENCE DEEP RESEARCH RESULTS")
        print("=" * 80)
        print(research_results)
        print("=" * 80)
        
        # Save results to file
        with open('/Users/ronitbhatia/Desktop/MedAhead/MedAheadEmergent/conference_research_results.txt', 'w') as f:
            f.write("Healthcare Conference Deep Research Results\n")
            f.write("Generated using Gemini AI - December 2024\n")
            f.write("=" * 80 + "\n\n")
            f.write(research_results)
        
        print(f"\n📄 Results saved to: conference_research_results.txt")
        
        return research_results
        
    except Exception as e:
        print(f"❌ Research failed: {str(e)}")
        print("Please check your API key and internet connection.")
        return None

async def targeted_research(query: str):
    """Perform targeted research based on specific query"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found")
        return
    
    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction="""You are a healthcare conference research specialist. 
            Provide detailed, accurate information about specific healthcare conferences or topics.
            Focus on current 2024-2025 information."""
        )
        
        research_prompt = f"Research and provide detailed information about: {query}"
        response = model.generate_content(research_prompt)
        research_results = response.text
        
        print(f"🎯 Targeted Research Results for: {query}")
        print("=" * 60)
        print(research_results)
        print("=" * 60)
        
        return research_results
        
    except Exception as e:
        print(f"❌ Targeted research failed: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 Healthcare Conference Deep Research Tool")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  To use this tool, you need to set your GEMINI_API_KEY environment variable.")
        print("You can do this by:")
        print("1. Creating a .env file with: GEMINI_API_KEY=your_api_key_here")
        print("2. Or running: export GEMINI_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://aistudio.google.com/app/apikey")
    else:
        print("\n1. Deep Research (comprehensive conference search)")
        print("2. Targeted Research (specific query)")
        
        choice = input("\nEnter your choice (1 or 2): ").strip()
        
        if choice == "1":
            asyncio.run(deep_research_conferences())
        elif choice == "2":
            query = input("Enter your specific research query: ").strip()
            if query:
                asyncio.run(targeted_research(query))
            else:
                print("❌ Please provide a research query")
        else:
            print("❌ Invalid choice. Please run the script again.")

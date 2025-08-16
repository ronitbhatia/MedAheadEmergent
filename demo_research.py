#!/usr/bin/env python3
"""
Demo script for Healthcare Conference Deep Research Tool
Shows how to use the Gemini API for conference research
"""

import os
import google.generativeai as genai

def demo_research_tool():
    """Demonstrate the research tool functionality"""
    
    print("🚀 Healthcare Conference Deep Research Tool Demo")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("\n💡 To use this tool:")
        print("1. Get your API key from: https://aistudio.google.com/app/apikey")
        print("2. Set it in your environment:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print("3. Or create a .env file with: GEMINI_API_KEY=your-api-key-here")
        return False
    
    print("✅ API key found! Initializing Gemini AI...")
    
    try:
        # Configure Gemini AI
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction="""You are an expert healthcare conference researcher. 
            Provide accurate, current information about major healthcare conferences for 2024-2025.
            Focus on dates, locations, attendee numbers, and industry relevance."""
        )
        
        print("🧠 Model initialized successfully!")
        print("\n🔍 Running sample research query...")
        
        # Sample research query
        research_prompt = """
        Please provide detailed information about the top 5 healthcare conferences in 2025, including:
        
        1. HIMSS Global Health Conference & Exhibition 2025
        2. J.P. Morgan Healthcare Conference 2025  
        3. BIO International Convention 2025
        4. American Hospital Association Annual Meeting 2025
        5. RSNA Annual Meeting 2024
        
        For each conference, provide:
        - Exact dates and location
        - Expected attendees
        - Key focus areas
        - Why it's important for healthcare professionals
        
        Format as a clear, structured response.
        """
        
        # Generate response
        print("⏳ Generating research results...")
        response = model.generate_content(research_prompt)
        
        print("✅ Research completed!\n")
        print("=" * 60)
        print("HEALTHCARE CONFERENCE RESEARCH RESULTS")
        print("=" * 60)
        print(response.text)
        print("=" * 60)
        
        print("\n💾 You can now integrate this research into your application!")
        print("📌 Next steps:")
        print("   1. Use the backend API endpoint: /api/conferences/research")
        print("   2. Update your conference database with this information")
        print("   3. Run targeted queries for specific conference details")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during research: {str(e)}")
        print("Please check your API key and internet connection.")
        return False

def demo_targeted_query():
    """Demo a targeted research query"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        print("\n🎯 Running targeted research query...")
        
        query = "What are the best digital health and AI conferences for 2025?"
        response = model.generate_content(query)
        
        print(f"\n📊 Targeted Query: {query}")
        print("-" * 40)
        print(response.text)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Targeted query failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Run the demo
    success = demo_research_tool()
    
    if success:
        demo_targeted_query()
    
    print("\n🎉 Demo completed!")
    print("📖 Check the other research scripts:")
    print("   - conference_research.py: Full research tool")
    print("   - test_research.py: API endpoint tests")

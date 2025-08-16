#!/usr/bin/env python3
"""
Test script for the Healthcare Conference Research Tool
"""

import requests
import json

def test_research_endpoint():
    """Test the conference research API endpoint"""
    
    # API endpoint (adjust URL as needed)
    api_url = "http://localhost:8000/api/conferences/research"
    
    try:
        print("🧪 Testing Conference Research API Endpoint...")
        
        # Test with general research
        response = requests.post(api_url, params={
            "year": "2024-2025"
        }, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Research Successful!")
            print(f"Research Query: {result.get('research_query')}")
            print(f"Year: {result.get('year')}")
            print(f"Source: {result.get('source')}")
            print("\n📋 Research Results:")
            print(result.get('research_results', 'No results'))
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the backend server is running")
        print("Start the server with: cd backend && python -m uvicorn server:app --reload")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

def test_targeted_research():
    """Test targeted research with specific query"""
    
    api_url = "http://localhost:8000/api/conferences/research"
    
    try:
        print("\n🎯 Testing Targeted Research...")
        
        response = requests.post(api_url, params={
            "query": "Digital health and AI conferences in healthcare 2025",
            "year": "2025"
        }, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Targeted Research Successful!")
            print(f"Query: {result.get('research_query')}")
            print("\n📋 Targeted Results:")
            print(result.get('research_results', 'No results'))
        else:
            print(f"❌ API Error: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Targeted research test failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Healthcare Conference Research Tool - API Tests")
    print("=" * 60)
    
    # Test general research
    test_research_endpoint()
    
    # Test targeted research  
    test_targeted_research()
    
    print("\n" + "=" * 60)
    print("💡 Tips:")
    print("1. Make sure your backend server is running")
    print("2. Ensure GEMINI_API_KEY is set in your environment")
    print("3. Check that all dependencies are installed")

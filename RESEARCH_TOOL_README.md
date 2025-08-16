# Healthcare Conference Deep Research Tool

## 🎯 Overview

This tool uses Google's Gemini AI to perform comprehensive research on healthcare conferences, providing up-to-date information about dates, locations, attendees, and industry focus areas.

## 🚀 Features

- **Deep Research**: Comprehensive analysis of major healthcare conferences
- **Targeted Queries**: Specific research on conference topics or themes  
- **API Integration**: RESTful API endpoint for backend integration
- **Current Information**: Focus on 2024-2025 conference data
- **Structured Output**: JSON-formatted results for easy parsing

## 📋 Setup Instructions

### 1. Get Your Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the generated key

### 2. Set Environment Variable
Choose one of these methods:

**Option A: Export in Terminal**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option B: Create .env File**
```bash
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

**Option C: Add to Shell Profile**
```bash
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
# or ~/.zshrc for zsh
```

### 3. Install Dependencies
```bash
pip install google-generativeai python-dotenv
```

## 🛠️ Usage

### Standalone Research Script
```bash
python conference_research.py
```

### Demo Script (Quick Test)
```bash
python demo_research.py
```

### API Endpoint Testing
```bash
python test_research.py
```

## 🌐 API Endpoints

### Research Conferences
```http
POST /api/conferences/research
```

**Parameters:**
- `query` (optional): Specific research focus
- `year` (optional): Target year (default: "2024-2025")

**Example Request:**
```bash
curl -X POST "http://localhost:8000/api/conferences/research" \
     -H "Content-Type: application/json" \
     -d '{"query": "Digital health conferences", "year": "2025"}'
```

**Example Response:**
```json
{
  "success": true,
  "research_query": "Digital health conferences",
  "year": "2025",
  "research_results": "...",
  "source": "Gemini AI Deep Research",
  "timestamp": "2024-12-20"
}
```

## 📊 Conference Coverage

The research tool focuses on these major healthcare conferences:

1. **HIMSS Global Health Conference & Exhibition**
2. **J.P. Morgan Healthcare Conference**
3. **BIO International Convention**
4. **American Hospital Association (AHA) Annual Meeting**
5. **American College of Physicians (ACP) Internal Medicine Meeting**
6. **Radiological Society of North America (RSNA) Annual Meeting**
7. **Healthcare Financial Management Association (HFMA) Conference**
8. **American Medical Association (AMA) Annual Meeting**
9. **Digital Health Summit**
10. **Additional emerging healthcare conferences**

## 🔧 Integration Examples

### Backend Integration
```python
from backend.server import research_conferences

# Use in your FastAPI application
result = await research_conferences(
    query="AI in healthcare conferences",
    year="2025"
)
```

### Frontend Integration
```javascript
// Call from your React/Vue/Angular app
const response = await fetch('/api/conferences/research', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        query: 'Digital health conferences',
        year: '2025'
    })
});

const data = await response.json();
console.log(data.research_results);
```

## 📝 Sample Queries

- "Major healthcare technology conferences in 2025"
- "Biotech and pharmaceutical conferences with networking opportunities"
- "Medical AI and digital transformation events"
- "Hospital administration and leadership conferences"
- "Radiology and medical imaging conferences"

## 🔒 Security Notes

- **Never commit your API key** to version control
- Use environment variables for production
- Monitor your API usage in Google AI Studio
- Consider rate limiting for production applications

## 🚨 Troubleshooting

### Common Issues

**Error: "GEMINI_API_KEY not found"**
- Solution: Set the environment variable correctly
- Check: `echo $GEMINI_API_KEY` should show your key

**Error: "google-generativeai not installed"**
- Solution: `pip install google-generativeai`

**Error: "API quota exceeded"**
- Solution: Check your Google AI Studio dashboard
- Consider upgrading your API plan

**Error: "Connection timeout"**
- Solution: Check internet connection
- Try again after a few moments

## 📈 Performance Tips

1. **Cache Results**: Store research results to avoid repeated API calls
2. **Batch Queries**: Combine multiple questions in one request
3. **Specific Queries**: More specific questions yield better results
4. **Rate Limiting**: Implement delays between requests if needed

## 🔄 Updates

The tool automatically focuses on current information (2024-2025). For future years:

1. Update the default year parameter
2. Modify the system instructions
3. Update conference focus areas as needed

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Google AI Studio documentation
3. Test with the demo script first
4. Verify API key permissions

## 🎉 Example Output

When working correctly, you'll see research results like:

```
✅ Research completed! Here are the results:

HEALTHCARE CONFERENCE DEEP RESEARCH RESULTS
================================================================================

**HIMSS 2025**
- Dates: March 3-6, 2025
- Location: Las Vegas Convention Center, Las Vegas, NV
- Expected Attendees: 45,000+
- Focus: Health Information Technology, Digital Transformation
- Confidence: High

**J.P. Morgan Healthcare Conference 2025**
- Dates: January 13-16, 2025
- Location: San Francisco, CA
- Expected Attendees: 9,000+
- Focus: Healthcare Investment, Innovation
- Confidence: High

[Additional conferences...]
================================================================================
```

Happy researching! 🎯

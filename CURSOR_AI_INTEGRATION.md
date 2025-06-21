# Crew Schedule Parser API - Cursor AI Integration Guide

This document provides comprehensive information for AI agents (like Cursor AI) to integrate with the Crew Schedule Parser API.

## 🤖 API Overview

**Service Name:** Crew Schedule Parser  
**Base URL:** `https://crew-schedule-parser.onrender.com`  
**Purpose:** Parse airline crew schedules from PDF files into structured JSON data  
**Authentication:** API Key required  

## 🔐 Authentication

**Method:** API Key in header  
**Header Name:** `x-api-key`  
**Value:** User's secret API key (set in environment variables)  

## 📡 API Endpoint

### POST /api/parse

**Purpose:** Parse a crew schedule PDF file and return structured data  

**URL:** `https://crew-schedule-parser.onrender.com/api/parse`  

**Method:** POST  

**Content-Type:** `multipart/form-data`  

**Headers Required:**
```
x-api-key: {USER_API_KEY}
Content-Type: multipart/form-data
```

**Request Body:**
- **Field Name:** `pdfFile`
- **Field Type:** File upload
- **Accepted Format:** PDF files only
- **Description:** Airline crew schedule PDF file (Lufthansa Netline Crewlink format)

## 📊 Response Format

### Success Response (200 OK)
```json
{
  "success": true,
  "data": [
    {
      "Date": "Fri20",
      "Weekday": "Fri", 
      "Day Number": "20",
      "Duty Type": "FLIGHT",
      "Duty Location": "",
      "Check-In Airport": "",
      "Check-In Time": "",
      "Check-Out Time": "",
      "Hotel": "",
      "Flight Number": "OS 231",
      "Departure Airport": "VIE",
      "Departure Time": "1300",
      "Arrival Time": " 1410", 
      "Arrival Airport": "BER",
      "Aircraft": "A220",
      "Requested": "False",
      "Flight Time": "05:45",
      "Duty Time": "09:35", 
      "Rest Time": "",
      "Meals": ""
    }
  ]
}
```

### Error Responses

**401 Unauthorized (Missing/Invalid API Key):**
```json
{
  "success": false,
  "error": "Unauthorized: Invalid API Key"
}
```

**400 Bad Request (No file uploaded):**
```json
{
  "success": false,
  "error": "No file uploaded"
}
```

**500 Internal Server Error (Processing failed):**
```json
{
  "success": false,
  "error": "Error processing file: [detailed error message]"
}
```

## 🛠️ Implementation Examples for AI Agents

### JavaScript/Node.js Implementation
```javascript
async function parseCrewSchedule(pdfFilePath, apiKey) {
  const FormData = require('form-data');
  const fs = require('fs');
  const fetch = require('node-fetch');
  
  const form = new FormData();
  form.append('pdfFile', fs.createReadStream(pdfFilePath));
  
  try {
    const response = await fetch('https://crew-schedule-parser.onrender.com/api/parse', {
      method: 'POST',
      headers: {
        'x-api-key': apiKey,
        ...form.getHeaders()
      },
      body: form
    });
    
    const result = await response.json();
    
    if (result.success) {
      return result.data; // Array of parsed schedule entries
    } else {
      throw new Error(result.error);
    }
  } catch (error) {
    console.error('API Error:', error.message);
    throw error;
  }
}
```

### Python Implementation
```python
import requests

def parse_crew_schedule(pdf_file_path, api_key):
    """
    Parse crew schedule PDF using the API
    
    Args:
        pdf_file_path (str): Path to the PDF file
        api_key (str): API key for authentication
    
    Returns:
        list: Parsed schedule data
    
    Raises:
        Exception: If API request fails
    """
    url = "https://crew-schedule-parser.onrender.com/api/parse"
    
    headers = {
        'x-api-key': api_key
    }
    
    with open(pdf_file_path, 'rb') as file:
        files = {'pdfFile': file}
        
        response = requests.post(url, headers=headers, files=files)
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                return result['data']
            else:
                raise Exception(f"API Error: {result['error']}")
        else:
            raise Exception(f"HTTP Error: {response.status_code}")
```

### cURL Command Template
```bash
curl -X POST \
  -H "x-api-key: YOUR_API_KEY_HERE" \
  -F "pdfFile=@/path/to/schedule.pdf" \
  https://crew-schedule-parser.onrender.com/api/parse
```

## 📋 Data Structure Details

### Parsed Schedule Entry Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `Date` | string | Date in format DayDD | "Fri20" |
| `Weekday` | string | Day of week | "Fri" |
| `Day Number` | string | Day number | "20" |
| `Duty Type` | string | Type of duty | "FLIGHT", "DAYOFF", "C/I", "C/O" |
| `Duty Location` | string | Location of duty | "" |
| `Check-In Airport` | string | Check-in airport code | "VIE" |
| `Check-In Time` | string | Check-in time | "1200" |
| `Check-Out Time` | string | Check-out time | "1800" |
| `Hotel` | string | Hotel information | "Hotel Name" |
| `Flight Number` | string | Flight number | "OS 231" |
| `Departure Airport` | string | Departure airport code | "VIE" |
| `Departure Time` | string | Departure time | "1300" |
| `Arrival Time` | string | Arrival time | " 1410" |
| `Arrival Airport` | string | Arrival airport code | "BER" |
| `Aircraft` | string | Aircraft type | "A220" |
| `Requested` | string | If requested | "True"/"False" |
| `Flight Time` | string | Flight duration | "05:45" |
| `Duty Time` | string | Duty duration | "09:35" |
| `Rest Time` | string | Rest duration | "12:00" |
| `Meals` | string | Meal information | "" |

## 🔍 Common Use Cases for AI Agents

### 1. Schedule Analysis
Parse crew schedules to analyze:
- Flight patterns
- Duty hours
- Rest periods
- Hotel stays
- Aircraft types

### 2. Data Extraction
Extract specific information:
- Flight numbers and routes
- Working hours calculations
- Rest time compliance
- Hotel bookings

### 3. Schedule Comparison
Compare multiple schedules:
- Monthly patterns
- Route frequency
- Duty load analysis

### 4. Report Generation
Generate reports from parsed data:
- Monthly summaries
- Flight statistics
- Duty time reports

## ⚠️ Important Notes for AI Agents

### Rate Limiting
- No explicit rate limits currently implemented
- Recommend reasonable usage (max 1 request per second)
- Large files may take 10-30 seconds to process

### File Handling
- Only PDF files are accepted
- Files are automatically cleaned up after processing
- Maximum file size: Not explicitly limited (reasonable sizes recommended)

### Error Handling
Always implement proper error handling:
1. Check HTTP status code
2. Verify `success` field in response
3. Handle network timeouts
4. Retry logic for temporary failures

### Security
- Never log or expose API keys
- Use environment variables for API key storage
- Validate file types before upload

## 🚀 Getting Started for AI Agents

### Step 1: Obtain API Key
User needs to set up API key in their Render environment:
1. Go to Render Dashboard → Service → Environment
2. Add `API_KEY` variable with secure value
3. Save and redeploy

### Step 2: Test Connection
```bash
curl -X POST \
  -H "x-api-key: test-key" \
  -F "pdfFile=@test.pdf" \
  https://crew-schedule-parser.onrender.com/api/parse
```

### Step 3: Implement Integration
Use the provided code examples above to integrate into your application.

## 📞 Support & Issues

- **GitHub Repository:** https://github.com/tomasslakotko/crapi
- **Live Demo:** https://crew-schedule-parser.onrender.com
- **Issues:** Create GitHub issues for bugs or feature requests

## 📝 API Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response data |
| 400 | Bad Request | Check file upload |
| 401 | Unauthorized | Verify API key |
| 500 | Server Error | Retry or report issue |

---

*This documentation is designed for AI agents to programmatically integrate with the Crew Schedule Parser API. For human-readable documentation, see README.md* 
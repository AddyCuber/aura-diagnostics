# AI-Powered Resume Analysis Setup

## Overview
The resume analysis feature now includes AI-powered scoring and feedback using OpenAI's GPT models for more intelligent and detailed analysis.

## Setup Instructions

### 1. Get OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Create a new API key
4. Copy the API key (starts with `sk-`)

### 2. Configure Environment Variables
1. Open the `.env` file in the project root
2. Replace `your_openai_api_key_here` with your actual OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
3. Save the file
4. Restart the development server

### 3. Features Enabled with AI

#### Enhanced Resume Analysis
- **Intelligent Scoring**: AI analyzes skill relevance, experience quality, and educational alignment
- **Contextual Feedback**: Detailed, actionable insights tailored to specific job requirements
- **Career Guidance**: Strategic advice for skill development and career progression
- **Transferable Skills**: Recognition of skills that may not be exact matches but are relevant

#### Fallback System
- If no OpenAI API key is provided, the system falls back to rule-based analysis
- Ensures the application works even without AI enhancement
- No functionality is lost - AI simply provides better insights

### 4. Usage
1. Upload your resume on the candidate dashboard
2. Enter a job description for matching
3. Click "Analyze Match Score"
4. Receive AI-powered analysis with detailed feedback

### 5. Cost Considerations
- OpenAI API usage is pay-per-use
- Each resume analysis costs approximately $0.01-0.03
- Monitor usage on the OpenAI dashboard
- Set usage limits if needed

## Troubleshooting

### Common Issues
1. **"AI analysis failed"** - Check if API key is valid and has credits
2. **Slow analysis** - OpenAI API calls take 2-5 seconds, this is normal
3. **Fallback to basic analysis** - API key might be missing or invalid

### Support
For issues with the AI integration, check the browser console and server logs for detailed error messages.

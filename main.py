import os
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
import requests
import openai
import uvicorn
from fastapi import FastAPI, Body, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

app = FastAPI(
    title="Marketing Research Agent",
    description="An AI-powered agent for marketing research and analysis",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create templates and static directories if they don't exist
os.makedirs("templates", exist_ok=True)
os.makedirs("static", exist_ok=True)

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# ----------------------------------------------------------------
# 1. Configuration / Environment
# ----------------------------------------------------------------
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY is not set.")
if not TAVILY_API_KEY:
    print("Warning: TAVILY_API_KEY is not set. Search functionality will be limited.")

# Initialize OpenAI client - fixing the initialization to handle version compatibility
try:
    # Try the new client method first
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
except TypeError:
    # Fall back to using the older method if there's a TypeError
    openai.api_key = OPENAI_API_KEY
    openai_client = openai

# ----------------------------------------------------------------
# 2. Tavily AI Search Tool
# ----------------------------------------------------------------
def tavily_ai_search(query: str) -> Dict[str, Any]:
    """
    Perform search using Tavily AI search API.
    
    Args:
        query: The search query
        
    Returns:
        Dictionary containing search results
    """
    try:
        if not TAVILY_API_KEY:
            # Return mock data if no API key is available
            return {
                "results": [
                    {
                        "title": f"Mock result for: {query}",
                        "url": "https://example.com",
                        "content": f"This is a placeholder result for the query: {query}. In a real implementation, this would contain actual search results from Tavily AI."
                    }
                ],
                "query": query
            }
        
        # Try both header formats for Tavily API
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": TAVILY_API_KEY,
            "Authorization": f"Bearer {TAVILY_API_KEY}"  # Adding Bearer token format as well
        }
        
        payload = {
            "query": query,
            "search_depth": "advanced",
            "include_domains": [],
            "exclude_domains": [],
            "max_results": 5
        }
        
        response = requests.post(
            "https://api.tavily.com/search",
            headers=headers,
            json=payload
        )
        
        if response.status_code != 200:
            # Try alternative endpoint format
            alt_response = requests.post(
                "https://api.tavily.com/v1/search",
                headers=headers,
                json=payload
            )
            if alt_response.status_code == 200:
                return alt_response.json()
            raise Exception(f"Tavily API returned status code {response.status_code}: {response.text}")
        
        return response.json()
    
    except Exception as e:
        print(f"Error in Tavily search: {str(e)}")
        # Return an error result
        return {
            "error": str(e),
            "results": [],
            "query": query
        }

def format_tavily_results(search_results: Dict[str, Any]) -> str:
    """
    Format Tavily search results into a readable string.
    
    Args:
        search_results: The raw search results from Tavily
        
    Returns:
        Formatted string of search results
    """
    if "error" in search_results:
        return f"Error in search: {search_results['error']}"
    
    formatted_results = []
    
    for i, result in enumerate(search_results.get("results", []), 1):
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        content = result.get("content", "No content")
        
        formatted_results.append(f"[{i}] {title}\nURL: {url}\n{content}\n")
    
    if not formatted_results:
        return "No search results found."
    
    return "\n".join(formatted_results)

# ----------------------------------------------------------------
# 3. Prompt Building
# ----------------------------------------------------------------
def build_prompt(
    previous_response: str,
    business_name: str,
    website_url: str,
    search_results: str,
) -> str:
    """
    Build the prompt for the OpenAI model.
    
    Args:
        previous_response: Previous conversation context (if any)
        business_name: Name of the business to research
        website_url: Website URL of the business
        search_results: Formatted search results from Tavily
        
    Returns:
        Formatted prompt string
    """
    # Start with any previous context
    context = previous_response + "\n\n" if previous_response else ""
    
    # Build the main prompt
    return f"""{context}You are an expert marketing and research agent specializing in business analysis.

TASK:
Analyze and provide valuable insights for the business: '{business_name}'
Website: '{website_url}'

SEARCH RESULTS:
{search_results}

ANALYSIS STEPS:
1. Identify the business sector, target audience, and value proposition
2. Analyze market positioning based on the search results
3. Evaluate their online presence and marketing strategy
4. Identify potential strengths, weaknesses, opportunities, and threats
5. Extract key insights that could help improve their marketing strategy

FORMAT YOUR RESPONSE AS FOLLOWS:

## BUSINESS OVERVIEW
[Concise summary of the business, its offerings, and target market]

## MARKET POSITIONING
[Analysis of how the business positions itself in its market]

## ONLINE PRESENCE
[Assessment of website, social media, and digital footprint]

## SWOT ANALYSIS
- Strengths: [Key strengths identified]
- Weaknesses: [Areas for improvement]
- Opportunities: [Potential growth areas]
- Threats: [Competitive or market challenges]

## KEY MARKETING INSIGHTS
[3-5 actionable insights that could help improve their marketing strategy]

## SOURCES ANALYSIS
[Brief assessment of the quality and credibility of sources used]

Keep your analysis evidence-based, actionable, and focused on marketing insights that provide genuine value.
"""

# ----------------------------------------------------------------
# 4. Models and API Endpoints
# ----------------------------------------------------------------
class AgentRequest(BaseModel):
    business_name: str
    website_url: str
    previous_response: Optional[str] = ""
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    
class AgentResponse(BaseModel):
    analysis: str
    search_query: str
    model_used: str
    
    # Configure model to disable protected namespace warnings
    model_config = {
        "protected_namespaces": ()
    }

def check_api_keys():
    """Check if required API keys are set and raise an exception if not."""
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable."
        )

@app.post("/run_agent", response_model=AgentResponse)
def run_agent(
    request: AgentRequest = Body(...),
    api_check: None = Depends(check_api_keys)
):
    """
    Run the marketing research agent.
    
    Args:
        request: The agent request containing business information
        
    Returns:
        The agent response containing the analysis
    """
    try:
        # 1) Use Tavily AI search to get additional information
        search_query = f"{request.business_name} company business analysis marketing {request.website_url}"
        search_results_raw = tavily_ai_search(search_query)
        search_results_formatted = format_tavily_results(search_results_raw)

        # 2) Build prompt
        prompt_text = build_prompt(
            previous_response=request.previous_response,
            business_name=request.business_name,
            website_url=request.website_url,
            search_results=search_results_formatted,
        )

        # 3) Call OpenAI
        try:
            # Try the new client method first
            response = openai_client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI marketing research assistant."},
                    {"role": "user", "content": prompt_text},
                ],
                temperature=request.temperature,
            )
            # Extract output text based on the response format
            output_text = response.choices[0].message.content
        except (AttributeError, TypeError):
            # Fall back to the older method
            response = openai_client.ChatCompletion.create(
                model=request.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI marketing research assistant."},
                    {"role": "user", "content": prompt_text},
                ],
                temperature=request.temperature,
            )
            # Extract output text from the older response format
            output_text = response["choices"][0]["message"]["content"].strip()

        # 5) Return formatted response
        return AgentResponse(
            analysis=output_text,
            search_query=search_query,
            model_used=request.model
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )

# ----------------------------------------------------------------
# 5. Health check endpoint
# ----------------------------------------------------------------
@app.get("/health")
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "version": "1.0.0"}

# ----------------------------------------------------------------
# 6. Frontend routes
# ----------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the home page with the agent interface."""
    return templates.TemplateResponse("index.html", {"request": request})

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------------------------------------------
# 7. Run with uvicorn if invoked directly
# ----------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 
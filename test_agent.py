#!/usr/bin/env python
"""
Test script for the Marketing Research Agent.
This script verifies the API is working properly by making a test request.
"""

import requests
import sys
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file if it exists
load_dotenv()

# Default test parameters
TEST_BUSINESS = "Wild Paws"
TEST_WEBSITE = "https://wildpawscolorado.org"
API_URL = "http://localhost:8000"


def test_health():
    """Test the health endpoint to verify the API is running."""
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("✅ API health check passed. The API is running correctly.")
            return True
        else:
            print(f"❌ API health check failed. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed. Error: {str(e)}")
        print("Make sure the API is running with 'python main.py' before testing.")
        return False


def test_agent(business_name=TEST_BUSINESS, website_url=TEST_WEBSITE):
    """Test the agent endpoint with a sample business."""
    try:
        print(f"\nTesting agent with: {business_name} ({website_url})")
        print("This may take a few moments as it performs searches and generates analysis...")
        
        # Check if OpenAI API key is set
        if not os.environ.get("OPENAI_API_KEY"):
            print("⚠️ OPENAI_API_KEY is not set. The test will likely fail.")
        
        # Make the API request
        response = requests.post(
            f"{API_URL}/run_agent",
            json={
                "business_name": business_name,
                "website_url": website_url,
                "model": "gpt-3.5-turbo",
                "temperature": 0.7
            }
        )
        
        # Check response status
        if response.status_code != 200:
            print(f"❌ Agent test failed. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        # Parse and print the response
        result = response.json()
        print("\n✅ Agent test passed! Sample of the analysis:\n")
        
        # Print the first few lines of the analysis for preview
        analysis_lines = result["analysis"].split("\n")
        preview_lines = analysis_lines[:15]  # First 15 lines
        for line in preview_lines:
            print(f"  {line}")
        
        if len(analysis_lines) > 15:
            print(f"\n  ... (analysis continues with {len(analysis_lines) - 15} more lines)")
        
        print(f"\nSearch query used: \"{result['search_query']}\"")
        print(f"Model used: {result['model_used']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Agent test failed. Error: {str(e)}")
        return False


if __name__ == "__main__":
    print("Testing Marketing Research Agent API")
    print("====================================")
    
    # Check if API is running
    if not test_health():
        sys.exit(1)
    
    # Use custom business if provided as command-line arguments
    business_name = TEST_BUSINESS
    website_url = TEST_WEBSITE
    
    if len(sys.argv) >= 3:
        business_name = sys.argv[1]
        website_url = sys.argv[2]
    
    # Run the agent test
    if not test_agent(business_name, website_url):
        sys.exit(1)
    
    print("\nAll tests passed! The Marketing Research Agent is working correctly.")
    print("To run with a different business: python test_agent.py \"Business Name\" \"https://website.com\"") 
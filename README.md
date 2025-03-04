# Marketing Research Agent

A FastAPI application that creates an AI-powered marketing research agent. This agent analyzes businesses by:

1. Accepting user inputs (Business Name, Website URL)
2. Performing web search using Tavily AI Search
3. Building dynamic prompts based on search results
4. Generating insights with OpenAI's GPT models
5. Returning formatted marketing analysis

## Features

- **AI-Powered Analysis**: Utilizes OpenAI's GPT models to analyze businesses
- **Web Search Integration**: Uses Tavily AI Search to gather real-time information
- **Customizable**: Configure model parameters, temperature, and other settings
- **API-First Design**: Simple REST API for easy integration with other applications
- **Well-Structured Output**: Returns analysis in a consistent, formatted structure

## Setup

### Prerequisites

- Python 3.8+ installed
- OpenAI API key
- Tavily API key (optional, but recommended for real search results)

### Installation

1. Clone this repository:
   ```
   git clone [repository-url]
   cd marketing-research-agent
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```

5. Edit the `.env` file with your API keys:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key
   TAVILY_API_KEY=your-tavily-api-key
   ```

## Running the Application

Start the server with:

```
python main.py
```

Or directly with uvicorn:

```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example API Request

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "business_name": "Wild Paws",
    "website_url": "https://wildpawscolorado.org",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7
  }' \
  http://localhost:8000/run_agent
```

### Example API Response

```json
{
  "analysis": "## BUSINESS OVERVIEW\nWild Paws is a non-profit animal rescue organization based in Colorado...",
  "search_query": "Wild Paws company business analysis marketing https://wildpawscolorado.org",
  "model_used": "gpt-3.5-turbo"
}
```

## Extending the Application

### Customizing the Prompt

You can modify the `build_prompt` function in `main.py` to adjust the analysis format or instructions given to the model.

### Adding Additional Tools

The current implementation includes Tavily search. You can extend this by adding additional tools such as:
- Website scrapers
- Social media analyzers
- Competitor analysis tools
- SEO evaluation tools

### Deployment

This application can be deployed to any platform that supports Python/FastAPI applications:
- Heroku
- AWS (EC2, Lambda with API Gateway)
- Google Cloud Run
- Azure App Service
- Digital Ocean App Platform

## License

[Specify your license here] 
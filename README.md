# 🚀 AI Marketing Research Agent

![License](https://img.shields.io/github/license/yourusername/marketing-research-agent)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103%2B-009688)

An AI-powered marketing research tool that leverages OpenAI's GPT models and Tavily AI Search to analyze businesses and generate comprehensive marketing insights.

<div align="center">
  <img src="docs/screenshot.png" alt="AI Marketing Research Agent" width="800px">
  <p><em>Generate in-depth business analysis in seconds with AI</em></p>
</div>

## ✨ Features

- **🧠 AI-Powered Analysis**: Harnesses OpenAI's GPT models to provide deep marketing insights
- **🔍 Intelligent Web Research**: Uses Tavily AI Search to gather real-time information from across the web
- **📊 Structured Reports**: Delivers insights in a consistent, organized format with SWOT analysis, audience insights, and actionable recommendations
- **⚙️ Model Selection**: Choose between different OpenAI models for varying levels of analysis depth
- **🎛️ Customizable Parameters**: Adjust temperature and other settings to control creativity and precision
- **🖥️ Modern Web Interface**: Clean, responsive UI built with Bootstrap for desktop and mobile
- **🔌 API-First Design**: Simple REST API for easy integration with other applications
- **🔐 Secure Configuration**: Environment-based configuration with proper security practices

## 🌟 Why Use This Tool?

Marketing research typically requires hours of manual web browsing, competitor analysis, and insight compilation. This AI-powered agent automates this process, delivering comprehensive reports in minutes that would normally take hours or days of research.

Perfect for:
- **Marketers** seeking quick insights on competitors
- **Entrepreneurs** researching potential markets
- **Product Managers** evaluating business landscapes
- **Consultants** preparing client reports
- **Students** working on business analysis projects

## 🏗️ Architecture

The application follows a modern, modular architecture:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  FastAPI    │────▶│  Business   │────▶│  OpenAI     │
│  Web Server │     │  Logic      │     │  Integration│
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Jinja2     │     │  Tavily     │     │  Response   │
│  Templates  │     │  Search API │     │  Formatting │
└─────────────┘     └─────────────┘     └─────────────┘
```

1. **User Input Layer**: Collects business details via web interface or API
2. **Research Layer**: Gathers information using Tavily AI Search
3. **Analysis Layer**: Processes data with OpenAI's models
4. **Presentation Layer**: Formats insights into structured reports

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- Tavily API key (optional, but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/marketing-research-agent.git
   cd marketing-research-agent
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the web interface**
   Open your browser and navigate to http://localhost:8000

### Docker Deployment

For containerized deployment:

```bash
docker-compose up -d
```

## 📊 Example Usage

### Web Interface

1. Enter the business name (e.g., "Tesla")
2. Provide the website URL (e.g., "https://tesla.com")
3. Select your preferred OpenAI model
4. Adjust the temperature slider for creativity level
5. Click "Analyze Business"

### API

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "business_name": "Tesla",
    "website_url": "https://tesla.com",
    "model": "gpt-4",
    "temperature": 0.7
  }' \
  http://localhost:8000/run_agent
```

## 🧩 How It Works

1. **Data Collection**: The agent accepts a business name and website URL
2. **Web Research**: It performs intelligent searches using Tavily AI to gather relevant information
3. **Prompt Engineering**: The system constructs detailed prompts combining user inputs and search findings
4. **AI Analysis**: OpenAI's models analyze the data, extracting key insights and patterns
5. **Report Generation**: Results are formatted into a comprehensive marketing analysis report

## 🛠️ Customization

### Modifying the Analysis Template

Edit the `build_prompt` function in `main.py` to customize the analysis format:

```python
def build_prompt(
    previous_response: str,
    business_name: str,
    website_url: str,
    search_results: str,
) -> str:
    # Customize the prompt format here
    # ...
```

### Adding Additional Tools

The current implementation can be extended with:
- Website scrapers
- Social media analyzers
- Competitor comparison tools
- SEO evaluation modules
- Image and brand analysis

## 📚 API Documentation

Once running, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) for their powerful GPT models
- [Tavily AI](https://tavily.com/) for their search API
- [FastAPI](https://fastapi.tiangolo.com/) for the efficient web framework
- All open-source contributors who make their work available for projects like this

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/yourusername">Your Name</a></p>
  <p>If you find this project helpful, please consider giving it a ⭐</p>
</div> 
# Agentic Company Researcher Tool Kit

![web ui](<static/ui-1.png>)

A multi-agent tool that generates comprehensive company research reports. The platform uses a pipeline of AI agents to gather, curate, and synthesize information about any company.

## Features

- **Multi-Source Research**: Gathers data from various sources, including company websites, news articles, financial reports, and industry analyses
- **AI-Powered Content Filtering**: Uses Tavily's relevance scoring for content curation
- **Asynchronous Processing**: Efficient polling-based architecture for tracking research progress
- **Dual Model Architecture**:
  - Gemini 2.5 Flash for high-context research synthesis
  - GPT-5.1 for precise report formatting and editing
- **Customizable Reports**: Choose from multiple tones (Objective, Formal, Analytical, Persuasive, Informal, Critical) to tailor the output to your audience.
- **Competitor Deep Dive**: Provide specific competitors for targeted comparative analysis.
- **Modern React Frontend**: Responsive UI with progress tracking, PDF, and Markdown download options.
- **Modular Architecture**: Built using a pipeline of specialized research and processing nodes

## Agent Framework

### Research Pipeline

The platform follows an agentic framework with specialized nodes that process data sequentially:

1. **Research Nodes**:
   - `CompanyAnalyzer`: Researches core business information
   - `IndustryAnalyzer`: Analyzes market position and trends
   - `FinancialAnalyst`: Gathers financial metrics and performance data
   - `NewsScanner`: Collects recent news and developments

2. **Processing Nodes**:
   - `Collector`: Aggregates research data from all analyzers
   - `Curator`: Implements content filtering and relevance scoring
   - `Briefing`: Generates category-specific summaries using Gemini 2.5 Flash
   - `Editor`: Compiles and formats the briefings into a final report using GPT-5.1

   ![web ui](<static/agent-flow.png>)

### Content Generation Architecture

The platform leverages separate models for optimal performance:

1. **Gemini 2.5 Flash** (`briefing.py`):
   - Handles high-context research synthesis tasks
   - Excels at processing and summarizing large volumes of data
   - Used for generating initial category briefings
   - Efficient at maintaining context across multiple documents

2. **GPT-5.1** (`editor.py`):
   - Specializes in precise formatting and editing tasks
   - Handles markdown structure and consistency
   - Superior at following exact formatting instructions
   - Used for:
     - Final report compilation
     - Content deduplication
     - Markdown formatting
     - Real-time report streaming

This approach combines Gemini's strength in handling large context windows with GPT-5.1's precision in following specific formatting instructions.

### Content Curation System

The platform uses a content filtering system in `curator.py`:

1. **Relevance Scoring**:
   - Documents are scored by Tavily's AI-powered search
   - A minimum threshold (default 0.4) is required to proceed
   - Scores reflect relevance to the specific research query
   - Higher scores indicate better matches to the research intent

2. **Document Processing**:
   - Content is normalized and cleaned
   - URLs are deduplicated and standardized
   - Documents are sorted by relevance scores
   - Research runs asynchronously in the background

### Backend Architecture

The platform implements a simple polling-based communication system:

![web ui](<static/ui-2.png>)

1. **Backend Implementation**:
   - Uses FastAPI with async support
   - Research tasks run in background
   - Results are stored and accessed via REST endpoints
   - Simple job status tracking
   
2. **Frontend Integration**:
   - React frontend submits research requests
   - Receives job_id for tracking
   - Polls `/research/{job_id}/report` endpoint
   - Displays final report when complete

3. **API Endpoints**:
   - `POST /research`: Submit new research request
   - `GET /research/{job_id}/report`: Poll for completed report
   - `POST /generate-pdf`: Generate PDF from report content

### Report Customization

When submitting a research request, you can now customize:

1. **Competitors**: Optionally list specific competitors (comma-separated) for focused comparative analysis.
2. **Tone**: Select the tone of the report:
   - **Objective**: Neutral and factual (default)
   - **Formal**: Professional and business-oriented
   - **Analytical**: Data-driven and critical
   - **Persuasive**: Highlight strengths and opportunities
   - **Informal**: Casual and easy to read
   - **Critical**: Focus on risks and challenges

### Export Options

- **PDF**: Download a professionally formatted PDF report.
- **Markdown**: Download the raw markdown file for editing or importing into other tools.

## Setup

### Quick Setup (Recommended)

The easiest way to get started is using the setup script, which automatically detects and uses `uv` for faster Python package installation when available:

1. Clone the repository:
```bash
git clone https://github.com/zaid-24/company-research-tool.git
cd company-research-tool
```

2. Make the setup script executable and run it:
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:

- Detect and use `uv` for faster Python package installation (if available)
- Check for required Python and Node.js versions
- Optionally create a Python virtual environment (recommended)
- Install all dependencies (Python and Node.js)
- Guide you through setting up your environment variables
- Optionally start both backend and frontend servers

> **💡Tip**: Install [uv](https://github.com/astral-sh/uv) for significantly faster Python package installation:
>
> ```bash
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```

You'll need the following API keys ready:
- Tavily API Key
- Google Gemini API Key
- OpenAI API Key
- Google Maps API Key
- MongoDB URI (optional)

### Manual Setup

If you prefer to set up manually, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/zaid-24/company-research-tool.git
cd company-research-tool
```

2. Install backend dependencies:
```bash
# Optional: Create and activate virtual environment
# With uv (faster - recommended if available):
uv venv .venv
source .venv/bin/activate

# Or with standard Python:
# python -m venv .venv
# source .venv/bin/activate

# Install Python dependencies
# With uv (faster):
uv pip install -r requirements.txt

# Or with pip:
# pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd ui
npm install
```

4. **Set up Environment Variables**:

This project requires two separate `.env` files for the backend and frontend.

**For the Backend:**

Create a `.env` file in the project's root directory and add your backend API keys:

```env
TAVILY_API_KEY=your_tavily_key
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key

# Optional: Enable MongoDB persistence
# MONGODB_URI=your_mongodb_connection_string
```

**For the Frontend:**

Create a `.env` file inside the `ui` directory. You can copy the example file first:

```bash
cp ui/.env.development.example ui/.env
```

Then, open `ui/.env` and add your frontend environment variables:

```env
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

### Running the Application

1. Start the backend server (choose one):
```bash
# Option 1: Direct Python Module
python -m application.py

# Option 2: FastAPI with Uvicorn
uvicorn application:app --reload --port 8000
```

2. In a new terminal, start the frontend:
```bash
cd ui
npm run dev
```

3. Access the application at `http://localhost:5173`

## Usage

### Local Development

1. Start the backend server (choose one option):

   **Option 1: Direct Python Module**
   ```bash
   python -m application.py
   ```

   **Option 2: FastAPI with Uvicorn**
   ```bash
   # Install uvicorn if not already installed
   # With uv (faster):
   uv pip install uvicorn
   # Or with pip:
   # pip install uvicorn

   # Run the FastAPI application with hot reload
   uvicorn application:app --reload --port 8000
   ```

   The backend will be available at:
   - API Endpoint: `http://localhost:8000`

2. Start the frontend development server:
   ```bash
   cd ui
   npm run dev
   ```

3. Access the application at `http://localhost:5173`

> **⚡ Performance Note**: If you used `uv` during setup, you'll benefit from significantly faster package installation and dependency resolution. `uv` is a modern Python package manager written in Rust that can be 10-100x faster than pip.

### Deployment Options

The application can be deployed to various cloud platforms. Here are some common options:

#### AWS Elastic Beanstalk

1. Install the EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize EB application:
   ```bash
   eb init -p python-3.11 tavily-research
   ```

3. Create and deploy:
   ```bash
   eb create tavily-research-prod
   ```
Choose the platform that best suits your needs. The application is platform-agnostic and can be hosted anywhere that supports Python web applications.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

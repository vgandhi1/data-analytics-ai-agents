# Analyzer GPT - Digital Data Analyzer

A data analysis application powered by AutoGen agents that can analyze CSV, Excel, and JSON files, generate Python code, and produce visualizations.

![Demo](Data-analysis-agent.gif)

## Features

-   **Data Analysis**: Upload `.csv`, `.xlsx`, or `.json` files.
-   **Natural Language Queries**: Ask questions about your data in plain English.
-   **Automated Code Generation**: Agents generate and execute Python code to solve your queries.
-   **Visualizations**: Generates plots and charts (saved as `output.png`).
-   **Dockerized Architecture**: Runs in a secure Docker environment with a separate frontend and backend.

## Project Structure

-   `streamlit_app.py`: Frontend interface (Streamlit).
-   `api.py`: Backend API (FastAPI) managing agents.
-   `agents/`: AutoGen agent definitions.
-   `team/`: Team orchestration logic.
-   `temp/`: Shared volume for file uploads and analysis outputs (ignored by git).
-   `docker-compose.yml`: Orchestration for frontend and backend services.

## Prerequisites

-   Docker and Docker Compose
-   OpenAI API Key (set in `.env`)

## Setup

1.  **Clone the repository**.
2.  **Create a `.env` file** in the root directory:
    ```bash
    OPENAI_API_KEY=sk-your-api-key-here
    ```
3.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```

## Usage

1.  Open your browser to [http://localhost:8501](http://localhost:8501).
2.  Upload a data file (`.csv`, `.xlsx`, or `.json`).
3.  Enter a task or question (e.g., "Show me the distribution of column X" or "Plot a bar chart of Y vs Z").
4.  The agents will analyze the data and display the result, including any generated charts.

## File Handling

-   Uploaded files are saved to the `temp/` directory.
-   The backend processes the file from this shared directory.
-   Generated images (`output.png`) are saved to `temp/` and displayed in the frontend.

## Development

-   **Frontend**: Streamlit
-   **Backend**: FastAPI + AutoGen
-   **Agents**: Using `autogen-agentchat` with OpenAI models.

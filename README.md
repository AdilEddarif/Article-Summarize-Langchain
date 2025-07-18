Based on the provided report for your article summarizer app and the update that you used ChromaDB instead of Pinecone, here’s a tailored GitHub README file to help others understand and set up your project.

---

# Article Summarizer App

## Overview
This project is an academic research assistance tool designed to help students and researchers synthesize scientific articles efficiently. Faced with the vast quantity of publications, this web application leverages advanced NLP techniques to identify and summarize relevant works in their field.

## Project Details
- **Prepared by**: Hamza Boughanim, Adil Eddarif
- **Technologies Used**: Node.js, Flask, ChromaDB, React, LangChain, GPT-4, PyPDF2, arXiv API, HAL Archives API
- **Purpose**: To create an intuitive web application for searching, summarizing, and visualizing scientific articles.

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Implementation](#implementation)
- [API Endpoints](#api-endpoints)
- [Frontend Components](#frontend-components)
- [Conclusion](#conclusion)
- [Setup Instructions](#setup-instructions)
- [Contributing](#contributing)
- [License](#license)

## Introduction
### Context
The project addresses the challenge of managing the growing volume of scientific publications by providing a tool to quickly synthesize articles from sources like arXiv and HAL Archives.

### Objectives
- Develop a web application that enables users to:
  - Search for articles using keywords, authors, or categories.
  - Retrieve and summarize article content.
  - Visualize key concepts and export results.

## System Architecture
### Overview
The system follows a modern client-server architecture with a clear separation between frontend and backend.

- **Backend**: Handles data extraction, summarization, and storage using Flask and ChromaDB.
- **Frontend**: Provides an intuitive interface built with React for searching and displaying results.

### Backend
- **Responsibilities**:
  - Extracts data from arXiv and HAL APIs.
  - Processes and summarizes articles using LangChain and GPT-4.
  - Stores and retrieves summaries using ChromaDB.

### Frontend
- Designed for usability with features like keyword highlighting, download options, and result sharing.

## Implementation
### Article Extraction
- **arXiv API Integration**:
  - Uses the `arxiv` Python library to search by keywords, authors, or categories.
  - Retrieves metadata (title, authors, abstract, date) and full PDFs.
  - Supports pagination for large result sets.
- **HAL Archives Integration**:
  - Utilizes HAL’s REST API for search and document retrieval.
  - Includes XML parsing, caching, and error handling.

### Article Processing with LangChain and GPT-4
- **Pipeline**:
  1. Text extraction from PDFs using PyPDF2.
  2. Summarization with GPT-4 via LangChain.
  3. Concept extraction and storage in ChromaDB.

## API Endpoints
- **POST /search**: Search for articles.
- **GET /summary/<id>**: Retrieve a specific summary.
- **POST /summarize**: Generate a new summary.
- Built with Flask-RESTful for modularity.

## Frontend Components
- **App**: Root component.
- **SearchBar**: Includes autocomplete and advanced filters (date, domain, author).
- **ResultsList**: Paginated display of search results.
- **SummaryView**: Detailed summary visualization with tag clouds and relevance scoring.

## Conclusion
### Summary
The project successfully delivers a functional tool for academic summarization, integrating multiple APIs and NLP technologies.

### Limitations
- Current dependency on external APIs and models.
- Potential performance issues with large datasets.

### Future Improvements
- Enhance caching mechanisms.
- Add support for additional data sources.
- Optimize summarization speed.

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone https://github.com/yourusername/rattrappage-nlp.git
   cd rattrappage-nlp
   ```

2. **Backend Setup (Flask)**:
   - Navigate to `backend-flask`:
     ```
     cd backend-flask
     ```
   - Create a virtual environment:
     ```
     python -m venv venv
     ```
   - Activate it:
     - Windows: `venv\Scripts\activate`
     - macOS/Linux: `source venv/bin/activate`
   - Install dependencies:
     ```
     pip install flask flask-cors chromadb langchain pypdf2 arxiv
     ```
   - Run the app:
     ```
     python app.py
     ```

3. **Backend Setup (Node.js)**:
   - Navigate to `backend`:
     ```
     cd ..\backend
     ```
   - Install dependencies:
     ```
     npm install
     ```
   - Start the server:
     ```
     node index.js
     ```

4. **Frontend Setup**:
   - Navigate to `frontend`:
     ```
     cd ..\frontend
     ```
   - Install dependencies:
     ```
     npm install
     ```
   - Start the app:
     ```
     npm start
     ```

5. **Configure Environment**:
   - Create a `.env` file in `backend` with API keys or URLs if required (e.g., `FLASK_API_URL=http://localhost:5000`).

## Contributing
Contributions are welcome! Please fork the repository and submit pull requests with detailed descriptions of changes.

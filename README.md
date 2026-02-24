# Meeting Intelligence Pipeline

AI-powered multimodal meeting processing system.

## Overview - Plan

Meeting Intelligence Pipeline is an AI-driven system that processes meeting recordings and transforms unstructured audio into structured, actionable insights.

The long-term vision of this project is to build a multi-agent AI system capable of:
- Transcribing audio
- Extracting structured task assignments
- Summarizing decisions and risks
- Validating outputs using critic agents
- Performing deadline normalization and quality evaluation

The project is built with a production-oriented mindset: separating NLP extraction from business logic and ensuring schema validation of AI outputs.

---

## Current MVP Functionality

The current implementation includes:

### 1. Audio Transcription
- Uses OpenAI speech-to-text model
- Accepts `.mp3` or `.wav` meeting recordings
- Saves transcript to file

### 2. Meeting Summarization
- Generates structured summaries:
  - Meeting goal
  - Key decisions
  - Tasks
  - Risks

### 3. Structured Task Extraction
- Extracts action items using LLM
- Enforces schema validation with Pydantic
- Outputs structured JSON:
  - task
  - assignee
  - deadline
  - confidence score

### 4. Pipeline Architecture
A simple AI processing pipeline:

audio → transcript → summary → structured action items

---

## Planned Extensions

- Multi-agent architecture (Summarizer, Extractor, Critic)
- Deadline normalization logic in Python
- Hallucination detection using embeddings
- Evaluation metrics for action-item accuracy
- REST API interface (FastAPI)
- Vector database integration for meeting memory
- Dashboard for analytics and task insights

---

## Tech Stack

- Python
- OpenAI API (speech-to-text + LLM)
- Pydantic (schema enforcement)

---

## Status

🚧 MVP completed  
🔄 Multi-agent system in progress

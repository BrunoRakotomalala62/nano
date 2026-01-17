# Nano AI API

## Overview
A simple Flask-based API for text generation using models from laozhang.ai.

## Project Structure
- `src/main.py` - Flask server implementation
- `requirements.txt` - Python dependencies

## Running the Application
The application runs on port 5000 using `python src/main.py`.

## API Endpoint
- `GET /api?prompt=<your_prompt>`
  - Returns the AI-generated response in JSON format.

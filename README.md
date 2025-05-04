# Content Publishing Platform

A platform where users can create and publish short blog posts with AI-powered content moderation.

## Features

- Create and edit draft blog posts
- AI-powered content moderation that checks:
  - Banned words/profanity
  - Content length (50-2000 characters)
  - Tone detection (aggressive content, all-caps)
- Clear post workflow: draft → approved/flagged → published
- Detailed feedback for flagged content
- Published posts become read-only
- Python SDK for programmatic access

## Architecture

- **Backend**: FastAPI with SQLite database
- **Frontend**: ReactJS with Axios for API calls
- **SDK**: Generated Python client library using OpenAPI Generator

## Getting Started

### Prerequisites

- Python 3.8 or later
- Node.js 14 or later
- npm 6 or later
- OpenAPI Generator CLI (installed via requirements.txt)

### Setup

1. Clone the repository
2. Run the setup script:
   
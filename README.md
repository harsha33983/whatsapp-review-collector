# WhatsApp Product Review Collector

A full-stack application to collect product reviews via WhatsApp and display them on a React dashboard.

## Features
- **WhatsApp Integration**: Interactive conversation flow to collect reviews via Twilio
- **Backend**: FastAPI with SQLAlchemy and Pydantic for data validation
- **Database**: PostgreSQL (Docker) or SQLite (local development)
- **Frontend**: React (Vite) dashboard to view reviews in real-time
- **Dockerized**: Easy deployment with Docker Compose
- **Local Development**: Can run without Docker for quick testing

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Method 1: Docker (Recommended for Production)](#method-1-docker-recommended-for-production)
  - [Method 2: Local Development (How I Executed)](#method-2-local-development-how-i-executed)
- [Twilio & ngrok Configuration](#twilio--ngrok-configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### For Docker Setup
- Docker & Docker Compose
- Twilio Account (with WhatsApp Sandbox enabled)
- ngrok (for exposing local webhook to internet)

### For Local Development Setup
- Python 3.9+ 
- Node.js 16+ & npm
- Twilio Account (with WhatsApp Sandbox enabled)
- ngrok (for exposing local webhook to internet)

## Project Structure

```
whatsapp-review-collector/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── crud.py                 # Database operations
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Backend Docker configuration
│   ├── routers/
│   │   └── whatsapp.py         # WhatsApp webhook endpoints
│   └── services/
│       └── whatsapp_service.py # WhatsApp conversation logic
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   └── main.jsx            # React entry point
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   └── Dockerfile              # Frontend Docker configuration
├── .env                        # Environment variables (not in git)
├── .env.example                # Example environment variables
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # This file
```

## Setup Instructions

### Method 1: Docker (Recommended for Production)

#### Step 1: Clone and Configure Environment

1. Clone the repository or navigate to the project directory:
   ```bash
   cd whatsapp-review-collector
   ```

2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Twilio credentials:
   ```env
   # Twilio Configuration
   TWILIO_ACCOUNT_SID=your_account_sid_here
   TWILIO_AUTH_TOKEN=your_auth_token_here
   TWILIO_NUMBER=whatsapp:+14155238886

   # Database Configuration (PostgreSQL for Docker)
   DATABASE_URL=postgresql://user:password@db:5432/reviews_db
   ```

#### Step 2: Build and Run with Docker Compose

```bash
docker-compose up --build
```

This will start three services:
- **PostgreSQL Database**: `localhost:5432`
- **Backend API**: `http://localhost:8000`
- **Frontend Dashboard**: `http://localhost:3000`

#### Step 3: Verify Services

- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend Dashboard: http://localhost:3000

---

### Method 2: Local Development (How I Executed)

This is the method I used to run the project locally without Docker.

#### Step 1: Configure Environment Variables

1. Navigate to the project directory:
   ```bash
   cd whatsapp-review-collector
   ```

2. Create a `.env` file in the root directory:
   ```env
   # Twilio Configuration
   TWILIO_ACCOUNT_SID=ACdb87c771fb370bda967e47c5a96817ff
   TWILIO_AUTH_TOKEN=33f4bcc54d81ae91893778a5fabc8e9e
   TWILIO_NUMBER=whatsapp:+12176773930

   # Database Configuration (SQLite for local development)
   DATABASE_URL=sqlite:///./reviews.db
   ```

#### Step 2: Set Up and Run Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the FastAPI backend server:
   ```bash
   uvicorn main:app --reload
   ```

   The backend will start at: **http://localhost:8000**

6. Verify the backend is running:
   - Open http://localhost:8000/docs to see the API documentation
   - You should see the Swagger UI with available endpoints

#### Step 3: Set Up and Run Frontend

1. Open a **new terminal** and navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

   The frontend will start at: **http://localhost:5173** (Vite default) or **http://localhost:3000**

4. Open the frontend in your browser to see the reviews dashboard

#### Step 4: Expose Backend with ngrok

Since WhatsApp webhooks need a public URL, we need to expose the local backend using ngrok.

1. Download ngrok from https://ngrok.com/download (or use the `ngrok.exe` already in the project)

2. In a **new terminal**, run ngrok to expose port 8000:
   ```bash
   ngrok http 8000
   ```

   Or if using the local ngrok.exe:
   ```bash
   .\ngrok.exe http 8000
   ```

3. ngrok will display a forwarding URL like:
   ```
   Forwarding: https://abc123.ngrok-free.app -> http://localhost:8000
   ```

4. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

---

## Twilio & ngrok Configuration

### Step 1: Set Up Twilio WhatsApp Sandbox

1. Log in to your [Twilio Console](https://console.twilio.com/)

2. Navigate to: **Messaging** → **Try it out** → **Send a WhatsApp message**

3. You'll see a WhatsApp Sandbox with:
   - A Twilio WhatsApp number (e.g., `+1 415 523 8886`)
   - A join code (e.g., `join example-word`)

4. Join the sandbox by sending the join code to the Twilio WhatsApp number from your phone

### Step 2: Configure Webhook URL

1. In the Twilio Console, go to: **Messaging** → **Settings** → **WhatsApp Sandbox Settings**

2. In the **"When a message comes in"** field, paste your ngrok URL with the webhook endpoint:
   ```
   https://abc123.ngrok-free.app/whatsapp/webhook
   ```

3. Set the HTTP method to **POST**

4. Click **Save**

### Important Notes:
- **ngrok URLs change** every time you restart ngrok (unless you have a paid plan)
- You'll need to update the Twilio webhook URL each time you restart ngrok
- Keep the ngrok terminal running while testing

---

## Usage

### Testing the WhatsApp Review Flow

1. **Ensure all services are running**:
   - Backend: http://localhost:8000
   - Frontend: http://localhost:5173 or http://localhost:3000
   - ngrok: Forwarding to port 8000

2. **Send a message to the Twilio WhatsApp number** from your phone:
   ```
   Hi
   ```

3. **Follow the conversation flow**:
   ```
   Bot: Which product is this review for?
   You: iPhone 15

   Bot: What's your name?
   You: John Doe

   Bot: Please send your review for iPhone 15
   You: Great phone! Amazing camera quality and battery life.

   Bot: Thank you for your review!
   ```

4. **Check the dashboard**:
   - Open http://localhost:5173 (or http://localhost:3000)
   - You should see the review appear in the table with:
     - Product Name: iPhone 15
     - Customer Name: John Doe
     - Review: Great phone! Amazing camera quality and battery life.
     - Phone Number: Your WhatsApp number
     - Timestamp

### Conversation State Management

The system maintains conversation state for each user:
- **AWAITING_PRODUCT**: Waiting for product name
- **AWAITING_NAME**: Waiting for customer name
- **AWAITING_REVIEW**: Waiting for review text
- **COMPLETED**: Review submitted successfully

---

## API Documentation

### Endpoints

#### 1. WhatsApp Webhook (POST)
```
POST /whatsapp/webhook
```
Receives incoming WhatsApp messages from Twilio and processes the review flow.

#### 2. Get All Reviews (GET)
```
GET /reviews
```
Returns all collected reviews as JSON.

**Response Example**:
```json
[
  {
    "id": 1,
    "product_name": "iPhone 15",
    "customer_name": "John Doe",
    "review_text": "Great phone! Amazing camera quality.",
    "phone_number": "+1234567890",
    "created_at": "2025-11-20T17:30:00"
  }
]
```

### Interactive API Documentation

Visit http://localhost:8000/docs for the interactive Swagger UI where you can:
- View all endpoints
- Test API calls directly
- See request/response schemas

---

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Make sure you've installed dependencies: `pip install -r requirements.txt`

**Problem**: Backend won't start - port 8000 already in use
- **Solution**: Kill the process using port 8000 or change the port:
  ```bash
  uvicorn main:app --reload --port 8001
  ```

**Problem**: Database errors with SQLite
- **Solution**: Delete `reviews.db` and restart the backend to recreate the database

### Frontend Issues

**Problem**: `npm install` fails
- **Solution**: Make sure you have Node.js 16+ installed: `node --version`

**Problem**: Frontend can't connect to backend
- **Solution**: Check that backend is running on http://localhost:8000
- Update the API URL in `frontend/src/App.jsx` if needed

### ngrok Issues

**Problem**: ngrok command not found
- **Solution**: Use the full path to ngrok.exe: `.\ngrok.exe http 8000`

**Problem**: Webhook not receiving messages
- **Solution**: 
  1. Verify ngrok is running and showing the forwarding URL
  2. Check that the Twilio webhook URL is correct (with `/whatsapp/webhook`)
  3. Make sure you've joined the Twilio sandbox
  4. Check backend logs for incoming requests

**Problem**: ngrok URL changed
- **Solution**: Update the webhook URL in Twilio Console with the new ngrok URL

### WhatsApp Issues

**Problem**: Not receiving responses from the bot
- **Solution**:
  1. Check backend logs for errors
  2. Verify Twilio credentials in `.env` are correct
  3. Make sure you've joined the sandbox
  4. Check that ngrok is forwarding to the correct port

**Problem**: "Conversation state not found"
- **Solution**: Send "Hi" to restart the conversation flow

---

## How I Executed the Project

Here's a summary of the exact steps I followed to run this project:

1. **Set up environment variables** in `.env` file with Twilio credentials and SQLite database

2. **Started the backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Started the frontend** (in a new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Exposed backend with ngrok** (in a new terminal):
   ```bash
   .\ngrok.exe http 8000
   ```

5. **Configured Twilio webhook** with the ngrok HTTPS URL + `/whatsapp/webhook`

6. **Tested the flow** by sending messages to the Twilio WhatsApp number

7. **Verified reviews** appeared in the dashboard at http://localhost:5173

---

## Development Tips

### Backend Development
- Use `--reload` flag with uvicorn for auto-restart on code changes
- Check logs in the terminal for debugging
- Use `/docs` endpoint for API testing

### Frontend Development
- Vite provides hot module replacement (HMR) for instant updates
- Check browser console for errors
- Use React DevTools for component debugging

### Database
- SQLite database file (`reviews.db`) is created automatically
- For production, use PostgreSQL with Docker
- Database schema is created automatically on first run

---

## License

This project is for educational purposes.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review the API documentation at http://localhost:8000/docs
3. Check Twilio Console for webhook logs
4. Review backend terminal logs for errors

# Slot Tracker - Railway Fullstack App

## Overview
Full-stack app deployable entirely on Railway.

## Structure
- frontend: Next.js app
- backend: FastAPI API

## Deploy on Railway
1. Push repo to GitHub
2. Create Railway project
3. Deploy both services:
   - frontend: root = frontend
   - backend: root = backend

## Backend start command
uvicorn main:app --host 0.0.0.0 --port $PORT

## Frontend build command
npm install && npm run build

## Frontend start command
npm run start

## Environment Variables
NEXT_PUBLIC_API_URL=<backend-url>

## Features
- Machine heat map
- Real-time ready (WebSockets ready placeholder)
- Spin logging ready

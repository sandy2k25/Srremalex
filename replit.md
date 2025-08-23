# Overview

This project is a voice AI assistant named Alex, built using LiveKit's real-time communication platform. Alex is designed to be a warm and friendly conversational AI assistant created by Stremini AI. The application provides voice-based interactions through a web interface where users can connect and have natural conversations with the AI agent. The system consists of a Flask web server that handles user connections and token generation, a LiveKit voice agent that processes conversations using OpenAI for language modeling, Deepgram for speech-to-text, and ElevenLabs for text-to-speech capabilities.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The web interface is built with vanilla HTML, CSS, and JavaScript, providing a clean and intuitive user experience. The frontend features a responsive design with a voice interface that includes an animated avatar, audio visualizer, and control buttons for microphone and speaker management. The client-side application uses the LiveKit JavaScript SDK to establish WebRTC connections for real-time audio communication.

## Backend Architecture
The backend follows a microservices approach with two main components:

1. **Web Server (Flask)**: Handles HTTP requests, serves the web interface, and generates LiveKit access tokens for user authentication. It provides REST endpoints for token generation and room management.

2. **Voice Agent (Python)**: Built on LiveKit's agents framework, this component handles the core AI conversation logic. It processes incoming audio, converts speech to text, generates AI responses, and converts text back to speech.

## Real-time Communication
The system uses LiveKit as the primary real-time communication infrastructure, providing WebRTC-based audio streaming between users and the AI agent. LiveKit handles room management, participant connections, and media routing.

## AI Services Integration
The voice agent integrates multiple AI services in a pipeline:
- **Speech-to-Text**: Deepgram Nova-2 model for accurate voice recognition
- **Language Model**: OpenAI GPT-4o-mini for natural conversation generation
- **Text-to-Speech**: ElevenLabs with Rachel voice model for natural-sounding responses, with OpenAI TTS as fallback

## Configuration Management
The application uses environment variables and a centralized configuration system that validates API keys and provides sensible defaults for development environments.

# External Dependencies

## Primary Services
- **LiveKit Platform**: Real-time communication infrastructure for WebRTC audio streaming and room management
- **OpenAI API**: GPT-4o-mini model for conversational AI responses
- **Deepgram API**: Nova-2-general model for speech-to-text conversion
- **ElevenLabs API**: Voice synthesis using Rachel voice with eleven_turbo_v2_5 model

## Development Dependencies
- **Flask**: Web framework for serving the frontend and API endpoints
- **LiveKit Python SDK**: Agent framework and real-time communication
- **LiveKit JavaScript SDK**: Client-side WebRTC implementation

## Authentication & Security
- **JWT Tokens**: LiveKit access tokens for secure room access
- **Environment Variables**: Secure API key management
- **WebRTC Security**: Built-in encryption for real-time media streams

## Deployment Configuration
- Default development setup with local LiveKit server (ws://localhost:7880)
- Environment-based configuration for production deployments
- Support for custom room names and participant limits
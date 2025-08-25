# Alex Voice Agent - GitHub Codespaces Setup

This repository is configured to work seamlessly with GitHub Codespaces, providing a complete development environment for the Alex Voice Agent.

## 🚀 Quick Start

1. **Open in Codespaces**: Click the "Code" button and select "Open with Codespaces"
2. **Wait for setup**: The environment will automatically install all dependencies
3. **Configure API keys**: Update `.env` with your API keys (especially `GEMINI_API_KEY`)
4. **Start the application**: Run the development commands below

## 🛠️ Development Commands

### Start the Web Server
```bash
python web_server.py
```
The web interface will be available at `http://localhost:5000`

### Start the Voice Agent
```bash
python -m livekit.agents.cli dev agent.py
```

### Install Additional Dependencies
```bash
# Python packages
pip install <package-name>

# Node.js packages (if needed)
npm install <package-name>
```

## 🔧 Environment Configuration

The development environment includes:
- **Python 3.11** with all required packages
- **Node.js 18** for frontend dependencies
- **VS Code extensions** for Python and JavaScript development
- **Audio processing libraries** for voice functionality
- **Port forwarding** configured for web access

## 🔑 Required API Keys

Update the `.env` file with your API keys:

```env
# Required for Alex's voice functionality
GEMINI_API_KEY=your_gemini_api_key_here

# Optional additional services
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
DEEPGRAM_API_KEY=your_deepgram_key_here
```

## 🌐 Accessing Your Application

Once the services are running:
- **Web Interface**: Available through the forwarded port 5000
- **Agent Status**: Check the terminal output for connection status
- **Logs**: View real-time logs in the terminal

## 🐛 Troubleshooting

### Port Issues
If port 5000 is busy, the application will automatically try other ports. Check the terminal output for the actual port being used.

### Audio Issues
Audio processing is handled server-side through LiveKit, so local audio hardware isn't required for development.

### Dependencies
If you encounter dependency issues, try:
```bash
pip install --upgrade -r requirements.txt
```

## 📝 Development Notes

- The environment includes automatic code formatting with Black
- Linting is enabled with Pylint
- All necessary VS Code extensions are pre-installed
- The workspace is configured for optimal Python and JavaScript development

Happy coding! 🎉
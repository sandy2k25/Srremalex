# GitHub Codespaces Information

## Quick Launch Badge
Add this to your README or documentation to provide a one-click GitHub Codespaces launch:

```markdown
[![Open in GitHub Codespaces](https://img.shields.io/badge/Open%20in-GitHub%20Codespaces-blue?logo=github)](https://codespaces.new/YOUR_USERNAME/YOUR_REPOSITORY_NAME)
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with the actual GitHub repository details.

## Alternative Launch Methods

### From GitHub Web Interface
1. Go to your repository on GitHub
2. Click the green "Code" button
3. Select "Codespaces" tab
4. Click "Create codespace on main"

### From GitHub CLI
```bash
gh codespace create
```

### From VS Code
1. Install the GitHub Codespaces extension
2. Use Command Palette: "Codespaces: Create New Codespace"

## Development Workflow

Once your Codespace is ready:

1. **Environment Setup** (automatic)
   - Python dependencies installed
   - Node.js dependencies installed
   - Development tools configured

2. **Configure API Keys**
   ```bash
   # Edit the .env file with your API keys
   code .env
   ```

3. **Start Development**
   ```bash
   # Terminal 1: Start web server
   python web_server.py
   
   # Terminal 2: Start voice agent
   python -m livekit.agents.cli dev agent.py
   ```

4. **Access Application**
   - Web interface will be available through forwarded ports
   - Check the "Ports" tab in VS Code for the URL

## Codespace Configuration Features

✅ **Pre-configured Development Environment**
- Python 3.11 with all dependencies
- Node.js 18 for frontend tools
- Audio processing libraries
- VS Code extensions for Python/JavaScript

✅ **Port Forwarding**
- Port 5000: Web interface
- Port 7880: LiveKit local server (if used)
- Port 8080: Additional development server

✅ **Environment Variables**
- LiveKit configuration pre-set
- Easy API key management through .env

✅ **Development Tools**
- Black formatter for Python
- Pylint for code quality
- Prettier for JavaScript/JSON
- Debugging support
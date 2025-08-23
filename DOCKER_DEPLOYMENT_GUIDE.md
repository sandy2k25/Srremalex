# 🐳 Deploy Alex with Docker to Hugging Face Spaces

This guide shows you how to deploy Alex using Docker on Hugging Face Spaces. This approach is simpler because it keeps your existing Flask/LiveKit architecture without needing to convert to FastRTC.

## 🎯 Why Docker?

✅ **Keep existing code** - No need to rewrite Flask to FastRTC  
✅ **Simpler setup** - Your current architecture works as-is  
✅ **Full control** - Complete container environment  
✅ **Production ready** - Uses Gunicorn for performance  

## 📁 Files for Docker Deployment

Upload these files to your HF Space (rename by removing `docker_` prefix):

```
your-hf-space/
├── README.md              (use docker_README.md)
├── Dockerfile             (use Dockerfile)
├── requirements.txt       (use docker_requirements.txt)
├── app.py                 (use docker_app.py)
└── static/
    ├── style.css          (use docker_style.css)
    ├── app.js             (use docker_app.js)
    ├── stremini-logo.png  (use docker_stremini-logo.png)
    └── livekit-client.umd.min.js (use docker_livekit-client.umd.min.js)
```

## 🚀 Step-by-Step Deployment

### Step 1: Create Docker Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Configure:
   - **Space name**: `alex-docker-voice-assistant`
   - **License**: MIT
   - **SDK**: **Docker** (important!)
   - **Hardware**: CPU Basic (free)
   - **Visibility**: Public

### Step 2: Prepare Files

**Option A: Web Interface**
1. Upload files one by one through the HF web interface
2. Make sure to rename files (remove `docker_` prefix)
3. Create a `static/` folder and upload the static files there

**Option B: Git Clone**
```bash
# Clone your new space
git clone https://huggingface.co/spaces/YOUR_USERNAME/alex-docker-voice-assistant
cd alex-docker-voice-assistant

# Copy files from your Replit project
cp docker_README.md README.md
cp Dockerfile Dockerfile
cp docker_requirements.txt requirements.txt
cp docker_app.py app.py

# Create static directory and copy files
mkdir -p static
cp docker_style.css static/style.css
cp docker_app.js static/app.js
cp docker_stremini-logo.png static/stremini-logo.png
cp docker_livekit-client.umd.min.js static/livekit-client.umd.min.js

# Commit and push
git add .
git commit -m "Deploy Alex voice assistant with Docker"
git push
```

### Step 3: Set Environment Variables

In your Space settings, add these environment variables:

| Variable | Value | Required |
|----------|-------|----------|
| `GEMINI_API_KEY` | Your Gemini API key | ✅ Yes |
| `LIVEKIT_API_KEY` | `APITMKfqYVjk79h` | ⚠️ Optional (default provided) |
| `LIVEKIT_API_SECRET` | `gCkm5chxks...` | ⚠️ Optional (default provided) |
| `LIVEKIT_URL` | `wss://sr-fa31r2za.livekit.cloud` | ⚠️ Optional (default provided) |

**To set variables:**
1. Go to your Space page
2. Click **"Settings"** tab  
3. Scroll to **"Repository secrets"**
4. Add each environment variable

### Step 4: Build and Deploy

1. **Auto-build**: HF Spaces automatically builds your Docker container
2. **Monitor logs**: Check the "Logs" tab for build progress
3. **Wait for completion**: Takes 3-5 minutes for first build
4. **Access your app**: Available at `https://YOUR_USERNAME-alex-docker-voice-assistant.hf.space`

## 🔧 Key Docker Features

### Port Configuration
- **HF Spaces requirement**: Must use port 7860
- **Automatic handling**: Docker exposes the correct port
- **Production ready**: Uses Gunicorn with multiple workers

### Security
- **Non-root user**: Container runs as user ID 1000 (HF requirement)
- **Clean environment**: Only necessary packages installed
- **Resource limits**: Automatically managed by HF infrastructure

### Performance
- **Gunicorn server**: Production WSGI server with 2 workers
- **Optimized build**: Uses Python 3.11-slim for smaller image
- **Fast startup**: Cached dependencies for quick restarts

## 🎯 Testing Your Deployment

1. **Visit your Space URL**
2. **Test voice connection**: Click "Start Conversation"
3. **Verify Alex responds** with Stremini AI personality
4. **Check all features**: Animated logo, voice detection, branding

## 🔧 Troubleshooting

### Build Issues
**"No module named 'livekit'"**
- Check `requirements.txt` has correct dependencies
- Ensure all files are uploaded properly

**"Port 7860 not accessible"**
- Verify Dockerfile exposes port 7860
- Check app.py runs on `host='0.0.0.0', port=7860`

### Runtime Issues
**"LiveKit connection failed"**
- Verify `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` in environment variables
- Check LiveKit server URL is correct

**"Gemini API error"**
- Ensure `GEMINI_API_KEY` is set correctly
- Verify your Gemini API has available quota

**"Static files not loading"**
- Check `static/` folder structure is correct
- Ensure all static files are uploaded

## 💡 Advantages of Docker Approach

✅ **No code rewriting** - Keep your existing Flask/LiveKit setup  
✅ **Production ready** - Gunicorn server, proper security  
✅ **Familiar architecture** - Same structure you're already using  
✅ **Easy debugging** - Same codebase locally and in production  
✅ **Full control** - Complete container environment customization  

## 🎉 Success!

Your Alex voice assistant is now running on Hugging Face Spaces with Docker! The deployment includes:

- **Professional Flask web server**
- **Real-time LiveKit voice communication** 
- **Beautiful Stremini AI branding**
- **Google Gemini AI integration**
- **Production-grade Docker container**

**Your live URL**: `https://YOUR_USERNAME-alex-docker-voice-assistant.hf.space`

Start chatting with Alex and share your voice assistant with the world! 🎤✨
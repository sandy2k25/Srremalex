# Alex Voice Agent - Render Deployment Guide

## 🚀 Quick Render Deployment

Your Alex Voice Agent is now fully compatible with Render.com! You can deploy both the web application and the LiveKit agent.

## 📁 Files Added for Render

- `render.yaml` - Render service configuration
- `requirements.txt` - Python dependencies
- `Procfile` - Process definitions
- `runtime.txt` - Python version specification

## 🌐 Deployment Options

### ⚠️ **Important: Free Tier Limitation**
Render's free tier **does not support background workers**. The LiveKit agent needs to run separately.

### Option 1: Render Web + Replit Agent (Recommended for Free)

1. **Deploy Frontend to Render**:
   - Push to Git and connect to Render
   - Deploy as web service (frontend + API)
   - **Cost**: Free

2. **Keep Agent on Replit**:
   - Keep the voice agent running here on Replit
   - Users connect to the same LiveKit server
   - **Cost**: Free

### Option 2: Full Render Deployment (Paid Plans)

1. **Web Service** (Free):
   - Frontend and API endpoints

2. **Background Worker** ($7/month):
   - LiveKit agent running 24/7
   - Upgrade to Starter plan required

### Option 3: Alternative Platforms for Agent

**Free Options for Agent:**
- **Railway.app** - $5 credit, supports background services
- **Fly.io** - Free tier with background processes
- **Render cron jobs** - Run agent periodically (limited)
- **Keep on Replit** - Always-on with Replit Core ($20/month)

## 🔧 Environment Variables

Set these in your Render service settings:

| Variable | Description | Required |
|----------|-------------|----------|
| `LIVEKIT_API_KEY` | LiveKit API key | Yes |
| `LIVEKIT_API_SECRET` | LiveKit API secret | Yes |
| `LIVEKIT_URL` | LiveKit server URL | Yes |
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `PORT` | Server port (auto-set by Render) | Auto |

## 📋 Service Configuration

The `render.yaml` creates:

1. **Web Service** (`alex-voice-agent`):
   - Serves the frontend and API endpoints
   - Runs on Render's dynamic port
   - Health check at `/health`

2. **Worker Service** (`alex-livekit-agent`):
   - Runs the voice agent in background
   - Connects to LiveKit for voice processing
   - Handles AI conversations

## 🛠 Key Features

- ✅ **Auto-scaling**: Render handles traffic automatically
- ✅ **SSL/HTTPS**: Free SSL certificates
- ✅ **Custom Domains**: Add your own domain
- ✅ **Health Monitoring**: Built-in health checks
- ✅ **Logs**: Real-time application logs
- ✅ **Zero Downtime**: Automatic deployments

## 🧪 Testing Your Deployment

1. **Frontend**: Visit your Render web service URL
2. **API Test**: Check `https://your-app.onrender.com/api/token`
3. **Health Check**: Visit `https://your-app.onrender.com/health`
4. **Voice Test**: Connect and test voice functionality

## 💡 Render Benefits

- **Always-on**: Background worker keeps agent running 24/7
- **Persistent Connections**: Perfect for LiveKit agents
- **Free Tier**: Great for testing and development
- **Easy Scaling**: Upgrade to paid plans for production

## 🔍 Troubleshooting

### Common Issues

1. **Build Failures**: Check `requirements.txt` dependencies
2. **Port Issues**: Render automatically sets PORT environment variable
3. **Static Files**: App serves files from both `/static` and root
4. **Agent Connection**: Verify LIVEKIT credentials are set

### Debug Steps

1. Check service logs in Render dashboard
2. Verify environment variables are set
3. Test endpoints individually
4. Monitor health check status

## 🎉 Deployment Complete!

Once deployed on Render:
- Your web app will be available at: `https://alex-voice-agent.onrender.com`
- The LiveKit agent runs continuously in the background
- Users can connect and have voice conversations with Alex
- Both services automatically restart if they crash

Perfect for production use with 24/7 availability!
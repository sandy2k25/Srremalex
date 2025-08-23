# Alex Voice Agent - Netlify & Vercel Deployment Guide

This guide explains how to deploy the Alex Voice Agent to both Netlify and Vercel platforms.

## 🚀 Quick Overview

Your app is now compatible with both Netlify and Vercel! The app has been restructured to work as a static frontend with serverless functions for the backend API.

### What's Been Changed

1. **Serverless Functions**: Created Node.js functions to replace Flask endpoints
2. **Static Assets**: Updated paths for static deployment
3. **Configuration Files**: Added platform-specific config files
4. **CORS Support**: Added proper CORS headers for cross-origin requests

## 📁 File Structure

```
/
├── netlify.toml              # Netlify configuration
├── vercel.json              # Vercel configuration  
├── index.html               # Main HTML file (static-ready)
├── style.css                # Styles
├── app.js                   # Frontend JavaScript
├── livekit-client.umd.min.js # LiveKit SDK
├── stremini-logo.png        # Logo asset
├── netlify/functions/       # Netlify serverless functions
│   ├── token.js            # Token generation
│   └── create-room.js      # Room creation
├── api/                     # Vercel serverless functions
│   ├── token.js            # Token generation
│   └── create-room.js      # Room creation
└── package.json            # Node.js dependencies
```

## 🌐 Netlify Deployment

### Option 1: Git Integration (Recommended)

1. **Push to Git**: Commit all files to your Git repository
2. **Connect to Netlify**:
   - Go to [netlify.com](https://netlify.com) and sign in
   - Click "New site from Git"
   - Connect your repository
   - Netlify will auto-detect the `netlify.toml` configuration

3. **Environment Variables** (required):
   - Go to Site settings → Environment variables
   - Add these variables:
     ```
     LIVEKIT_API_KEY=your_api_key
     LIVEKIT_API_SECRET=your_api_secret
     LIVEKIT_URL=your_livekit_url
     GEMINI_API_KEY=your_gemini_api_key
     ```

### Option 2: Drag & Drop

1. **Prepare files**: Ensure all files are in your project root
2. **Deploy**: Drag the entire folder to Netlify's deploy area
3. **Configure**: Manually set environment variables in site settings

### Netlify Features Used

- **Functions**: Automatic Node.js function deployment
- **Redirects**: API routes redirect to functions
- **Headers**: CORS and security headers configured
- **Static hosting**: Frontend files served from root

## ▲ Vercel Deployment

### Option 1: Git Integration (Recommended)

1. **Push to Git**: Commit all files to your Git repository
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com) and sign in
   - Click "Import Project"
   - Connect your repository
   - Vercel will auto-detect the `vercel.json` configuration

3. **Environment Variables**:
   - In project settings, add:
     ```
     LIVEKIT_API_KEY=your_api_key
     LIVEKIT_API_SECRET=your_api_secret
     LIVEKIT_URL=your_livekit_url
     GEMINI_API_KEY=your_gemini_api_key
     ```

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from project directory
vercel

# Follow the prompts to configure
```

### Vercel Features Used

- **API Routes**: Serverless functions in `/api` directory
- **Static Files**: Frontend served from `/static` mapping
- **Headers**: CORS configuration for API routes
- **Build Config**: Static build process configured

## 🔧 Environment Variables

Both platforms need these environment variables:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `LIVEKIT_API_KEY` | LiveKit API key | `APITMKfqYVjk79h` |
| `LIVEKIT_API_SECRET` | LiveKit API secret | `gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA` |
| `LIVEKIT_URL` | LiveKit server URL | `wss://sr-fa31r2za.livekit.cloud` |
| `GEMINI_API_KEY` | Google Gemini API key (required) | *Must be provided* |

⚠️ **Security Note**: Update the default values with your own LiveKit credentials before deploying to production.

## 🤖 LiveKit Agent Deployment

**Important**: The LiveKit agent (`agent.py`) requires a persistent connection and cannot run as a serverless function. For full functionality, you have these options:

### Option 1: Keep Agent on Replit (Recommended)
- Deploy frontend to Netlify/Vercel
- Keep the agent running on Replit
- Users connect to the same LiveKit server from both environments

### Option 2: Deploy Agent Separately
- Use platforms that support persistent connections:
  - Railway.app
  - Render.com
  - DigitalOcean App Platform
  - AWS ECS/Fargate
  - Google Cloud Run (with always-on)

### Option 3: Agent as a Service
- Set up the agent on a VPS or dedicated server
- Use process managers like PM2 or systemd
- Ensure the agent connects to the same LiveKit server

## 📋 API Endpoints

Both deployments provide these endpoints:

- `GET /api/token` - Generate LiveKit access token
- `GET /api/create-room` - Create/prepare a room

### Parameters

**Token Generation** (`/api/token`):
- `identity` (optional): User identity
- `room` (optional): Room name

**Room Creation** (`/api/create-room`):
- `room` (optional): Room name

## 🧪 Testing Your Deployment

1. **Frontend Test**: Open your deployed URL and check the interface loads
2. **API Test**: Check browser network tab for successful API calls
3. **Voice Test**: Test voice connection (requires agent running)

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**: Check that API functions include proper CORS headers
2. **Token Generation Failed**: Verify environment variables are set
3. **Static Assets Not Loading**: Ensure files are in the correct directory
4. **Voice Connection Fails**: Verify LiveKit agent is running and accessible

### Debug Tips

- Check browser console for JavaScript errors
- Verify API endpoints respond in browser network tab
- Test API endpoints directly: `https://yoursite.com/api/token`
- Check platform-specific logs (Netlify Functions or Vercel Functions)

## 🎉 Success!

Your Alex Voice Agent is now ready for production deployment on both Netlify and Vercel!

- **Netlify**: Best for static sites with simple functions
- **Vercel**: Great for React/Next.js and complex serverless needs
- **Both**: Support custom domains, SSL, and global CDN

Choose the platform that best fits your workflow and requirements.
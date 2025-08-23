# 🚀 Deploy Alex to Hugging Face Spaces

This guide will help you deploy your Alex voice assistant to Hugging Face Spaces, making it accessible to users worldwide.

## 📋 What You'll Need

1. **Hugging Face Account** - Sign up at [huggingface.co](https://huggingface.co)
2. **Google Gemini API Key** - Get one from [Google AI Studio](https://aistudio.google.com)
3. **Hugging Face Token** - Generate from your [HF settings](https://huggingface.co/settings/tokens)

## 📁 Files to Upload to Your Space

Copy these files from your Replit project to your new HF Space:

```
your-hf-space/
├── app.py                    (use hf_app.py - rename it)
├── requirements.txt          (use hf_requirements.txt - rename it)
├── README.md                 (use hf_README.md - rename it)
└── stremini-logo.png         (use hf_stremini-logo.png - rename it)
```

## 🛠️ Step-by-Step Deployment

### Step 1: Create Your Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in details:
   - **Space name**: `alex-voice-assistant` (or your choice)
   - **License**: MIT
   - **SDK**: Gradio
   - **Hardware**: CPU Basic (free tier works!)
   - **Visibility**: Public or Private

### Step 2: Upload Files

1. **Clone your new Space** (or use the web interface):
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/alex-voice-assistant
   cd alex-voice-assistant
   ```

2. **Copy and rename files**:
   ```bash
   # From your Replit project, copy these files:
   cp hf_app.py app.py
   cp hf_requirements.txt requirements.txt  
   cp hf_README.md README.md
   cp hf_stremini-logo.png stremini-logo.png
   ```

3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Deploy Alex voice assistant"
   git push
   ```

### Step 3: Configure Environment Variables

In your Space settings, add these **environment variables**:

| Variable | Value | Description |
|----------|-------|-------------|
| `GEMINI_API_KEY` | `your_gemini_api_key` | Google Gemini API key |
| `HF_TOKEN` | `your_hf_token` | Your HF token (for TURN server) |

**To set environment variables:**
1. Go to your Space page
2. Click **"Settings"** tab
3. Scroll to **"Repository secrets"**
4. Add each variable with its value

### Step 4: Wait for Build

1. Your Space will automatically build (takes 2-3 minutes)
2. Check the **"Logs"** tab if there are any issues
3. Once built, your Alex assistant will be live!

## 🎯 Testing Your Deployment

1. **Visit your Space URL**: `https://huggingface.co/spaces/YOUR_USERNAME/alex-voice-assistant`
2. **Click "Start Conversation"** to test voice chat
3. **Verify Alex responds** with his Stremini AI personality
4. **Check branding** - logo and Stremini.site references

## 🔧 Troubleshooting

### Common Issues:

**"Connection failed"**
- Ensure `HF_TOKEN` is set correctly in environment variables
- FastRTC requires TURN servers for Spaces (automatically handled)

**"Gemini API error"**
- Verify `GEMINI_API_KEY` is valid and has credits
- Check Google AI Studio for API quota limits

**"Build failed"**
- Check requirements.txt format
- Ensure all files are properly uploaded
- Review build logs in the Logs tab

**"Audio not working"**
- Browser permissions - allow microphone access
- Try refreshing the page
- FastRTC handles audio processing automatically

## 💡 Customization Tips

### Update Alex's Personality
Edit the `ALEX_CONTEXT` variable in `app.py`:
```python
ALEX_CONTEXT = """
You are Alex, customize this personality...
Created by Sandy from Stremini AI...
"""
```

### Change Branding
- Replace `stremini-logo.png` with your logo
- Update website references in the code
- Modify the CSS styling in `custom_css`

### Add Features
- Integrate additional AI models
- Add voice commands or special responses
- Customize the UI with more branding

## 🌟 Features of Your HF Space

✅ **Real-time voice chat** with sub-second latency  
✅ **Global accessibility** via Cloudflare edge network  
✅ **Professional interface** with Stremini branding  
✅ **Mobile-friendly** - works on all devices  
✅ **Free hosting** on Hugging Face infrastructure  

## 📈 Next Steps

1. **Share your Space** - Get the public URL and share with users
2. **Monitor usage** - Check Space analytics in your HF dashboard  
3. **Iterate and improve** - Add features based on user feedback
4. **Scale up** - Upgrade to better hardware if needed

## 🎉 You're Done!

Your Alex voice assistant is now live on Hugging Face Spaces! Users worldwide can chat with Alex and learn about Stremini AI.

**Space URL**: `https://huggingface.co/spaces/YOUR_USERNAME/alex-voice-assistant`

---

**Need help?** Check the [Hugging Face Spaces documentation](https://huggingface.co/docs/hub/spaces) or reach out to the community!
module.exports = {
  apps: [
    {
      name: 'alex-web-server',
      script: './web_server.py',
      interpreter: 'python3',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 5000,
        LIVEKIT_API_KEY: 'APITMKfqYVjk79h',
        LIVEKIT_API_SECRET: 'gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA',
        LIVEKIT_URL: 'wss://sr-fa31r2za.livekit.cloud',
        GEMINI_API_KEY: 'your_gemini_api_key_here'
      },
      error_file: './logs/web-error.log',
      out_file: './logs/web-out.log',
      log_file: './logs/web-combined.log',
      time: true
    },
    {
      name: 'alex-voice-agent',
      script: 'python',
      args: '-m livekit.agents.cli dev agent.py',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '2G',
      restart_delay: 5000,
      env: {
        NODE_ENV: 'production',
        LIVEKIT_API_KEY: 'APITMKfqYVjk79h',
        LIVEKIT_API_SECRET: 'gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA',
        LIVEKIT_URL: 'wss://sr-fa31r2za.livekit.cloud',
        GEMINI_API_KEY: 'your_gemini_api_key_here',
        PYTHONPATH: '.'
      },
      error_file: './logs/agent-error.log',
      out_file: './logs/agent-out.log',
      log_file: './logs/agent-combined.log',
      time: true
    }
  ]
};
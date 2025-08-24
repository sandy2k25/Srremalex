#!/usr/bin/env python3
"""
Railway agent starter script
This runs the LiveKit agent with proper error handling and restarts
"""
import os
import sys
import time
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_agent():
    """Run the agent with restart capability"""
    while True:
        try:
            logger.info("Starting Alex LiveKit Agent...")
            
            # Run the agent
            result = subprocess.run([
                sys.executable, "agent.py"
            ], check=False)
            
            if result.returncode == 0:
                logger.info("Agent exited normally")
                break
            else:
                logger.error(f"Agent crashed with exit code {result.returncode}")
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
            break
        except Exception as e:
            logger.error(f"Error running agent: {e}")
            
        # Wait before restart
        logger.info("Restarting agent in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    run_agent()
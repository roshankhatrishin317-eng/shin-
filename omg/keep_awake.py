#!/usr/bin/env python3
"""
Compact Python script that continuously monitors and maintains active I/O operations 
within the specified studio workspace directory to prevent the IDE from entering sleep mode.
"""

import os
import time
import threading
from pathlib import Path

# Configuration
WORKSPACE_DIR = "/teamspace/studios/this_studio/omg"
LOG_FILE = "activity.log"
INTERVAL_SECONDS = 30  # Adjust as needed (lower values = more frequent activity)

def touch_file(filepath):
    """Update the access and modification times of a file."""
    with open(filepath, 'a'):
        os.utime(filepath, None)

def background_activity():
    """Perform periodic file system interactions to maintain I/O activity."""
    log_path = os.path.join(WORKSPACE_DIR, LOG_FILE)
    
    while True:
        try:
            # Create/update a log file to maintain I/O activity
            touch_file(log_path)
            
            # Additional minimal I/O operation - read directory contents
            _ = os.listdir(WORKSPACE_DIR)
            
            time.sleep(INTERVAL_SECONDS)
        except Exception as e:
            # Silently handle exceptions to prevent script termination
            time.sleep(INTERVAL_SECONDS)

def main():
    """Main function to start the background activity thread."""
    # Ensure workspace directory exists
    Path(WORKSPACE_DIR).mkdir(parents=True, exist_ok=True)
    
    # Start background activity in a daemon thread
    activity_thread = threading.Thread(target=background_activity, daemon=True)
    activity_thread.start()
    
    print(f"I/O monitoring started. Keeping workspace '{WORKSPACE_DIR}' active...")
    print("Press Ctrl+C to stop.")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping I/O monitoring...")

if __name__ == "__main__":
    main()
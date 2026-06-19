import requests
import json
import time
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_url_here" 
LOG_FILE = "game_output.log"

def send_to_discord(message_content, severity):
    colors = {
        "CRASH": 15158332,   # Red
        "WARNING": 15105570, # Yellow
    }
    
    payload = {
        "embeds": [
            {
                "title": f"Build Alert: {severity}",
                "description": message_content,
                "color": colors.get(severity, 3447003),
                "footer": {
                    "text": f"Engine Stream Pipeline | File: {LOG_FILE}"
                }
            }
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

def monitor_log():
    print(f"🔍 Monitoring {LOG_FILE} for errors and crashes...")
    
    while not os.path.exists(LOG_FILE):
        time.sleep(1)
        
    with open(LOG_FILE, "r") as f:
        # Catch up to the current end of the file
        f.seek(0, os.SEEK_END)
        current_position = f.tell()
        
        try:
            while True:
                # Edge Case 1: Check if the file was wiped/truncated (Game restarted)
                if os.path.getsize(LOG_FILE) < current_position:
                    print("\n Game log was reset. Resetting position.\n")
                    f.seek(0, os.SEEK_SET)
                    current_position = f.tell()
                
                line = f.readline()
                
                if not line:
                    time.sleep(0.1)
                    continue
                    
                # Process the data stream
                if "[CRASH]" in line:
                    print(f"Detected Crash! Alerting Discord.")
                    send_to_discord(line.strip(), "CRASH")
                elif "[WARNING]" in line:
                    print(f"Detected Warning. Alerting Discord.")
                    send_to_discord(line.strip(), "WARNING")
                
                # Update our current bookmark pointer in the file
                current_position = f.tell()
                
        except KeyboardInterrupt:
            # Edge Case 2: Exit on Ctrl+C
            print("\nMonitoring stopped cleanly by user.")


if __name__ == "__main__":
    monitor_log() 

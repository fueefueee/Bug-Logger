import time
import random

LOG_FILE = "game_output.log"

log_messages = [
    "[INFO] Player spawned at coordinates (0, 0, 0).",
    "[INFO] Textures loaded successfully.",
    "[WARNING] High memory usage detected (85% capacity).",
    "[INFO] Enemy AI pathfinding initialized.",
    "[CRASH] Fatal Error: Access violation reading location 0x00000004.",
    "[WARNING] Frame drop detected: dropped 14 frames.",
    "[CRASH] NullReferenceException: Object reference not set to an instance of an object."
]

print(f"Mock Game Started... Writing loops to {LOG_FILE}")
print("Press Ctrl+C to stop.")

# Clean/reset the file on start
with open(LOG_FILE, "w") as f:
    f.write("[INFO] --- GAME LOG INITIALIZED ---\n")

while True:
    # Pick a random log message
    msg = random.choice(log_messages)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    full_line = f"[{timestamp}] {msg}\n"
    
    # Append it to the log file
    with open(LOG_FILE, "a") as f:
        f.write(full_line)
        print(f"Logged: {msg}")
        
    # Wait between 2 to 5 seconds before writing the next event
    time.sleep(random.randint(2, 5))
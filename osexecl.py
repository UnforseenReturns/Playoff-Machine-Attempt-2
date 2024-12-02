import os
import sys
import time

def restart_script():
    print("Restarting script...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    print("Script started.")
    time.sleep(5)  # Wait for 5 seconds to simulate some processing
    restart_script()
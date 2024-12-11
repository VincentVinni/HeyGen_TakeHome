import time
import subprocess
import requests
from threading import Event
from client_library import StatusClient

def test_integration():
    server_process = subprocess.Popen(
        ["python", "server.py"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True
    )
    try:
        time.sleep(2) # start the server, wait for it to start
        try: # check if server is responding 
            r = requests.get("http://localhost:5000/status", timeout=5)
            r.raise_for_status()
            print("[TEST LOG] Server started. (This does not count towards total timeout you've defined) Responded with: ", r.json())
        except Exception as e:
            print("[TEST ERROR] Failed to reach server:", e)
            assert False, "Server did not start or respond correctly."


        client = StatusClient(url="http://localhost:5000/status", initial_delay=1, max_delay=2, timeout=30)

        # Use the client to wait for completion
        try:
            result = client.wait_for_completion(on_poll=on_poll)
            print("[TEST LOG] Final result:", result)
            assert result == "completed", f"Expected 'completed', got '{result}'"
        except Exception as e:
            print("[TEST ERROR] An error occurred during polling:", e)
            assert False, f"Polling failed with error: {e}"

    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()

#helper function to log the status
def on_poll(status):
    print(f"[TEST LOG] Polled status: {status}")

if __name__ == "__main__":
    test_integration()

import time
import requests
from .exceptions import JobError, JobTimeoutError, CancellationError
from .config import DEFAULT_INITIAL_DELAY, DEFAULT_MAX_DELAY, DEFAULT_TIMEOUT

class StatusClient:
    def __init__(self, url, initial_delay=None, max_delay=None, timeout=None):
        # Use default parameters of client defined parameters 
        self.url = url.rstrip("/")
        self.max_delay = max_delay or DEFAULT_MAX_DELAY
        self.initial_delay = initial_delay or DEFAULT_INITIAL_DELAY
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.session = requests.Session()
        self.default_on_on_poll = on_poll

    def get_status(self):
        url = self.url 
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()  
            data = response.json()

            # result not found 
            if "result" not in data:
                raise ValueError("Malformed response: 'result' field missing")

            return data["result"]
        except requests.exceptions.Timeout as e:
            print("Request timed out:", e)
            raise
        except requests.exceptions.RequestException as e:
            print("An HTTP error occurred:", e)
            raise

    def wait_for_completion(self, on_poll=None, delay_increase_rate=2):
        start_time = time.time()
        delay = self.initial_delay

        while True: # Run indefinetely until job is completed or job timeout 
            # Check timeout
            elapsed = time.time() - start_time
            if elapsed > self.timeout:
                raise JobTimeoutError("Timed out waiting for the job to complete.")

            try:
                status = self.get_status()
            except requests.RequestException as e:
                if on_poll:
                    on_poll("Network Error. Retrying...")
                time.sleep(delay)
                delay = min(delay * delay_increase_rate, self.max_delay)
                continue
            
            if on_poll:
                on_poll(status) # LOG Polled Status with custom function
            else:
                self.default_on_on_poll(status)

            # depending on the status, handle request appropriately (completed: job done, erro: raise error, pending: tune polling delay and try again)
            if status == "completed":
                return "completed"
            elif status == "error":
                raise JobError("The job returned error status")
            elif status == "pending":
                time.sleep(delay) # wait for the next poll
                delay = min(delay * delay_increase_rate, self.max_delay)

#helper function to log the status
def on_poll(status):
    print(f"[TEST LOG] Polled status: {status}")
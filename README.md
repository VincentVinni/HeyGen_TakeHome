# HeyGen_TakeHome Assesment 

///// Setup 
1. Enable Python virtual environment and 'pip install' following libraries:
    python -m venv venv
    source venv/bin/activate     # On macOS/Linux
    pip install flask
    pip install python-dotenv
2. Create .env file and add the following variables:
    "COMPLETION_DELAY": 10 
     This variable can be tinkered with and reflects the amount of time the job takes to complete. 
3. Start the server with python server.py

///// Client Library Usage 
1. Create an instance of StatusClient, passing the URL of the endpoint to poll. 
2. (Optional): Pass in initial_delay, max_delay, and timeout arguments. (Not passing in optional arguments will utilize the default values in config.py)
    initial_delay represents the initial delay time between polls, 
    max_delay represents the max delay time between polls
    timeout represents the amount of time before you want to stop polling regardless of whether job is complete 
3. Call the wait_for_completion method to poll the status. Optionally, provide a callback function to log each polling attempt:

///// Example Usage
    def on_poll(status):
        print(f"Polled status: {status}")

    try:
        result = client.wait_for_completion(on_poll=on_poll)
        print(f"Job completed with result: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

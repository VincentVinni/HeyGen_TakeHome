from flask import Flask, jsonify
import time
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

COMPLETION_DELAY = int(os.getenv("COMPLETION_DELAY", 30))

JOB_START_TIME = time.time()

@app.route('/status', methods=['GET'])
def get_status():
    elapsed = time.time() - JOB_START_TIME

    if elapsed < COMPLETION_DELAY:
        result = "pending"
    elif elapsed > COMPLETION_DELAY * 2:
        result = "error"
    else:
        result = "completed"

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

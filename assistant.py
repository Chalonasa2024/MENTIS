import os
from flask import Flask, request, jsonify
from omnidimension import Client

API_KEY = os.getenv("OMNIDIM_API_KEY")
AGENT_ID = int(os.getenv("AGENT_ID", "97209"))

client = Client(API_KEY)

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "running"}

@app.route("/call", methods=["POST"])
def call_api():
    data = request.get_json(silent=True)
    to_number = data.get("phone_number", "").strip()

    if not to_number.startswith("+"):
        return {"error": "Invalid phone number"}, 400

    response = client.call.dispatch_call(
        AGENT_ID,
        to_number=to_number
    )

    return {"success": True, "response": response}

@app.route("/call-ui", methods=["GET", "POST"])
def call_ui():
    if request.method == "POST":
        to_number = request.form.get("phone_number", "")
        response = client.call.dispatch_call(
            AGENT_ID,
            to_number=to_number
        )
        return f"<pre>{response}</pre><a href='/call-ui'>Back</a>"

    return """
    <form method="post">
      <input name="phone_number" placeholder="+919876543210" required>
      <button>Call</button>
    </form>
    """

if __name__ == "__main__":
    app.run()

import os
from flask import Flask, request, jsonify
from omnidimension import Client

# Flask app
app = Flask(__name__)

# Config
API_KEY = os.getenv("OMNIDIM_API_KEY")
AGENT_ID = int(os.getenv("AGENT_ID", "97209"))

client = Client(API_KEY)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://mentis-ai.vercel.app",   # 👈 your React domain
                "http://localhost:5173"           # 👈 local dev (Vite)
            ]
        }
    }
)

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "platform": "vercel"
    })


@app.route("/call", methods=["POST"])
def call_api():
    data = request.get_json(silent=True)

    if not data or "phone_number" not in data:
        return jsonify({"error": "phone_number required"}), 400

    to_number = data["phone_number"].strip()

    if not to_number.startswith("+"):
        return jsonify({"error": "Invalid phone number format"}), 400

    try:
        response = client.call.dispatch_call(
            AGENT_ID,
            to_number=to_number
        )

        return jsonify({
            "success": True,
            "response": response
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/call-ui", methods=["GET", "POST"])
def call_ui():
    if request.method == "POST":
        to_number = request.form.get("phone_number", "").strip()

        try:
            response = client.call.dispatch_call(
                AGENT_ID,
                to_number=to_number
            )
            return f"""
                <h2>✅ Call Sent</h2>
                <pre>{response}</pre>
                <a href="/api/call-ui">Back</a>
            """
        except Exception as e:
            return f"<pre>❌ Error: {e}</pre>"

    return """
        <h2>📞 Call Dispatcher</h2>
        <form method="POST">
            <input name="phone_number" placeholder="+919876543210" required />
            <button type="submit">Call</button>
        </form>
    """

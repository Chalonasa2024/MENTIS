from omnidimension import Client

client = Client("FNekZvViW5gup_NHPpFaHZvVhSVXhzTGxqmzqmMQINw")

to_number = input(
    "Enter phone number with country code (e.g. +919876543210): "
).strip()

if not to_number.startswith("+"):
    print("❌ Invalid phone number format")
    exit()

AGENT_ID = 97209  # must be valid for this API key

try:
    response = client.call.dispatch_call(
        AGENT_ID,
        to_number=to_number   # ✅ correct keyword
    )
    print("✅ Call dispatched successfully")
    print(response)

except Exception as e:
    print("❌ Call failed:", e)

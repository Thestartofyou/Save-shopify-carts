'''

                            Online Python Compiler.
                Code, Compile, Run and Debug python program online.
Write your code in this editor and press "Run" button to execute it.

# Import necessary libraries
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

# Create Flask app
app = Flask(__name__)

# Define webhook endpoint for Twilio to send messages to
@app.route("/sms", methods=["POST"])
def sms_reply():
    # Get incoming message details
    incoming_msg = request.values.get("Body", "").lower().strip()
    sender_phone = request.values.get("From")
    
    # Check if message is a valid cart URL
    if "https://myshopify.com/cart/" in incoming_msg:
        # Send request to Shopify API to retrieve cart data
        cart_url = incoming_msg
        cart_id = cart_url.split("/")[-1]
        shop_url = cart_url.split("/")[2]
        shop_api_url = f"https://{shop_url}/admin/api/2021-09"
        headers = {
            "X-Shopify-Access-Token": "your_access_token_here",
            "Content-Type": "application/json",
        }
        r = requests.get(f"{shop_api_url}/checkouts/{cart_id}.json", headers=headers)
        if r.status_code == 200:
            cart_data = r.json()
            # Send a confirmation message to the customer
            resp = MessagingResponse()
            msg = resp.message(f"Thank you for sending us your cart! We've saved it and will send you a reminder in 24 hours. 😊")
            return str(resp)
        else:
            # Send an error message to the customer if the cart data cannot be retrieved
            resp = MessagingResponse()
            msg = resp.message("Sorry, we couldn't save your cart. Please try again later. 😞")
            return str(resp)
    else:
        # Send a message to the customer to remind them to send a valid cart URL
        resp = MessagingResponse()
        msg = resp.message("Please send us the URL of your Shopify cart to save it! 👍")
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)


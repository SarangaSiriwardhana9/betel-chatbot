from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from utils.betel_chatbot import handle_message

twilio_bp = Blueprint("twilio", __name__)

@twilio_bp.route("/twilio-webhook", methods=["POST"])
def twilio_webhook():
    try:
        # Get message from Twilio WhatsApp
        from_number = request.form.get('From')
        message_body = request.form.get('Body')
        
        print(f"📱 WhatsApp message from: {from_number}")
        print(f"📝 Message: {message_body}")
        
        # Process with your chatbot
        response_data = handle_message(message_body, session_id=from_number)
        
        # Handle different response types
        if isinstance(response_data, dict):
            response_text = response_data.get("reply", "Sorry, something went wrong.")
        else:
            response_text = str(response_data)
        
        # Send back via Twilio
        resp = MessagingResponse()
        resp.message(response_text)
        
        print(f"🤖 Bot response: {response_text}")
        return str(resp)
        
    except Exception as e:
        print(f"❌ Twilio webhook error: {e}")
        resp = MessagingResponse()
        resp.message("Sorry, I'm having technical difficulties. Please try again.")
        return str(resp)
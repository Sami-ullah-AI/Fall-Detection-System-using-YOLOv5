from twilio.rest import Client
import keys
client = Client(keys.account_sid, keys.auth_token)
def notify():
    message = client.messages.create(
        body = "Baga g Has fallen send by system",
        from_= keys.twilio_number,
        to = keys.target_number
        )
print(message.body)
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def send_sms(msg):
    account = "---- Twilio_account -------"
    token = "-------- Twilio_token -------"
    client = Client(account, token)
    list_ctnt = ['0102030405']
    sms = f"{msg} bien été publié sur votre page Facebook"
    try:
        for call in list_ctnt :
            message = client.messages.create(to=f'+225{call}', from_="twilio_phone_number",
            body=sms)
    except TwilioRestException as e:
        pass


if __name__ == "__main__":
    pass

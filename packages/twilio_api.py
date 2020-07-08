from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def send_sms(msg):
    account = "ACd3b64d23e4a4a9872fc1131981acf377"
    token = "f22f10f9942fbc627263c4437564469b"
    client = Client(account, token)
    list_ctnt = ['77865857']
    sms = f"{msg} bien été publié sur votre page Facebook"
    try:
        for call in list_ctnt :
            message = client.messages.create(to=f'+225{call}', from_="+12053950795",
            body=sms)
    except TwilioRestException as e:
        pass


if __name__ == "__main__":
    pass
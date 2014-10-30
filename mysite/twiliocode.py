from twilio import twiml
from django_twilio.decorators import twilio_view

@twilio_view
def reply_to_sms_messages(request):
    r = twiml.Response()
    r.message('Thanks for the SMS message!')
    return r

from twilio.rest import TwilioRestClient

from django_twilio.client import twilio_client


for number in twilio_client.phone_numbers.iter():
    print(number.friendly_name)
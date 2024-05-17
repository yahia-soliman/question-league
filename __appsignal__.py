from appsignal import Appsignal
from os import getenv


appsignal = Appsignal(
    name="Question League",
    active=True,
    push_api_key=getenv("APPSIGNAL_API_KEY"),
)


import requests
def turn_on_off():
    url="https://universal-remote-umber.vercel.app/sendcmd"

    payload={
        "type":"fan_remote",
    "model" :"atomberg",
        "command":"on/off"
    }

    data=requests.post(url,json=payload)
    print(data.status_code)

def speedup():
    url="https://universal-remote-umber.vercel.app/sendcmd"

    payload={
        "type":"fan_remote",
    "model" :"atomberg",
        "command":"speedup"
    }

    data=requests.post(url,json=payload)
    print(data.status_code)

def speeddown():
    url="https://universal-remote-umber.vercel.app/sendcmd"

    payload={
        "type":"fan_remote",
    "model" :"atomberg",
        "command":"speedown"
    }

    data=requests.post(url,json=payload)
    print(data.status_code)

def turn_on_off_ac():
    url="https://universal-remote-umber.vercel.app/sendcmd"

    payload={
        "type":"ac_remote",
    "model" :"lg_window",
        "command":"on"
    }

    data=requests.post(url,json=payload)
    print(data.status_code)

def ac_cool():
    url="https://universal-remote-umber.vercel.app/sendcmd"

    payload={
        "type":"ac_remote",
    "model" :"lg_window",
        "command":"on"
    }


    data=requests.post(url,json=payload)
    print(data.status_code)

def ac_hot():
    url="https://universal-remote-umber.vercel.app/sendcmd"

    payload={
        "type":"ac_remote",
    "model" :"lg_window",
        "command":"on"
    }


    data=requests.post(url,json=payload)
    print(data.status_code)


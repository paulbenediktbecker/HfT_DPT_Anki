import requests
import json 
import urllib.request
from urllib.error import URLError
from progress.bar import IncrementalBar
import os
import subprocess
import smtplib, ssl
import secret


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    try:
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))

        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response['result']
    except URLError:
        print("ANKI NOT ONLINE !")

def export_anki_cards():
    blacklist = ['API_TEST', 'Custom Study Session', 'Default']
    decks = invoke('deckNames') 
    for entry in blacklist:
        decks.remove(entry)
    for count,deck in enumerate(decks):
        print(f"{count}: {deck}")
    input_string = input("please input all indexes of files you want to export, separated by a space")
    chosen_decks_indeces = input_string.split()
    chosen_decks_indeces = [int(x.replace(" ", "")) for x in chosen_decks_indeces]
    filtered_decks = []
    for count, deck in enumerate(decks):
        if count in chosen_decks_indeces:
            filtered_decks.append(deck)
    decks = filtered_decks


    print("Exporting:")
    print(decks)
    path_to_packages = "C:/Users/paulb/git/DHBW_WI_Anki/"
    API_base = {
        "action": "exportPackage",
        "version": 6,
        "params": {
            "deck": "Default",
            "path": "/data/Deck.apkg",
            "includeSched": False
        }
    }
    bar = IncrementalBar('Exporting Decks...', max=len(chosen_decks_indeces))
    for count, deck in enumerate(decks):

        API_base["params"]["deck"] = str(deck)

        path_to_write = os.path.join(os.getcwd()  + "\\" + str(deck) + ".apkg")
        API_base["params"]["path"] = path_to_write
        result = invoke(API_base["action"],  **API_base["params"])
        print(path_to_packages +  str(deck) + ".apkg")
        print(result)

        bar.next()
    bar.finish()


def pull_commit_push():

    commit_message = input("Input commit Message")
    commit_message = "'" + commit_message + "'"

    cmd = "git pull"
    args = cmd.split()
    subprocess.call(args)

    cmd = "git add -A"
    args = cmd.split()
    subprocess.call(args)

    cmd = "git commit -m"
    args = cmd.split()
    args.append(commit_message)
    subprocess.call(args)

    cmd = "git push"
    args = cmd.split()
    subprocess.call(args)

def send_mails():
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email =  secret.mail_login# Enter your address
    
    password = secret.mail_pw
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        for receiver_mail in secret.mails_to_send:
            server.sendmail(sender_email, receiver_email, message)

export_anki_cards()
pull_commit_push()
send_mails()
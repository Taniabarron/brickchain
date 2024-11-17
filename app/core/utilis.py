import base64
import codecs
from hashlib import md5
import json
import re
from mailjet_rest import Client
import requests
from Crypto.Cipher import AES


DATA_FILE = './opt/datos.json'
PHRASE = 'Blockchain'
            
def _get_data_secret(key):
    data = {}
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print('''No se pudo leer el archivo: {}, e: {}'''.format(DATA_FILE, str(e)))
    return data.get(key)

def SendMailMailJet(subject='', body='', email_to=[], email_cc=[], bcc=[], attachments=[]):
    api_key = _get_data_secret('API_KEY_MAILJET')
    api_secret = _get_data_secret('API_SECRET_MAILJET')

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": _get_data_secret('email_from'),
                    "Name": _get_data_secret('email_name')
                },
                "To": email_to, 
                "Cc": email_cc, 
                "Bcc": bcc, 
                "Subject": subject,
                "HTMLPart": body,
                "Attachments": attachments,
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.json()

def render_template(path):
    dir_path = 'app/core/templates/mailing/'+path+'.html'
    f = codecs.open(dir_path, 'r')
    return f.read()

def _checkVarchar(strings):
    e = re.findall("[+,*,$,ç,<,>,;,:,%,&,/,(),=,!,|,#,?,¿,¡,']", str(strings)) #-
    if e:
        response = True
    else:
        response = False        
    return response

def validate_data(data):
    for key, value in data.items():
        print(value)
        if _checkVarchar(value):
            return False  
    return True 

BLOCK_SIZE = 16


def pad(data):
    pad = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + pad * chr(pad)


def unpad(padded):
    pad = ord(chr(padded[-1]))
    return padded[:-pad]


def get_key_iv(password):
    m = md5()
    m.update(password.encode('utf-8'))
    key = m.hexdigest()

    m = md5()
    m.update((password + key).encode('utf-8'))
    iv = m.hexdigest()

    return [key, iv]

def _decrypt(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += '=' * (4 - missing_padding)
    result = base64.b64decode(data).decode('utf-8')
    return result


def _encrypt(data):
    number_bytes = str(data).encode('utf-8')
    result = base64.b64encode(number_bytes).decode('utf-8')
    return result

def _createWallet(owner):
    url_api = "https://apis.bloxtek.com/apis_wallet/v1/wallet/did"
    headers = {"Authorization": "Bearer {}".format("d988a47861c13cdced2622e42fa7489171c274b7be91762e7f6ce210ea20cb5f")}
    dumps = ({
        "ownerName": owner,
    })
    r = requests.post(url=url_api, headers=headers, data=dumps, params=dumps, verify=False)
    data = r.json()
    return data
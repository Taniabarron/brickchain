
import json


DATA_FILE = './opt/datos.json'

def _get_data_secret(key):
    data = {}
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print('''No se pudo leer el archivo: {}, e: {}'''.format(DATA_FILE, str(e)))
    return data.get(key)
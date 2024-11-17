import json
import os
from app.core.utilis import _get_data_secret
from web3 import Web3

# Conectar a una red
# Para una red pública/testnet
    
def create_property(account, property_info):
    rootStock_url = "https://rpc.testnet.rootstock.io/ypZdAcXL0sFL29k8cajLYcdJfufr8U-T"
    #rootStock_url = "https://public-node.testnet.rsk.co"
    
    web3 = Web3(Web3.HTTPProvider(rootStock_url))
    
    raw_address = "0x90D667af5C169dB8fFbD16e9023d191D1509b2fb"

    abi_path = os.path.join('app', 'blockchain', 'abi.json')
    
    with open(abi_path, 'r') as abi_file:
        contract_abi = json.load(abi_file)
    print("ABI cargado exitosamente")

    contract = web3.eth.contract(address=Web3.to_checksum_address(raw_address), abi=contract_abi)

    private_key = _get_data_secret('PRIVATE_KEY')

    tx = contract.functions.createProperty(
        property_info['name'], 
        int(property_info['price']), 
        web3.to_checksum_address(property_info['asset']),
        property_info['tokenUri'], 
        int(property_info['totalAmount']), 
        web3.to_checksum_address(property_info['seller'])
    ).build_transaction({ 'from': account, 
                         'gasPrice': 60000000,
                         'nonce': web3.eth.get_transaction_count(account)})

    print(3)

    # Firma la transacción
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    
    # Envía la transacción
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(tx_hash)
    return web3.to_hex(tx_hash)
from flask import Flask, request, jsonify
from web3 import Web3
import ipfshttpclient
from video_comparison.compare import compare_videos

app = Flask(__name__)

# Connect to local Ethereum node (Ganache)
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
contract_address = '0x857e2f19d6b7b16e7d19d7f7c067a8959996815c'
contract_abi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_ipfsHash",
                "type": "string"
            }
        ],
        "name": "registerVideo",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "videoId",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "ipfsHash",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "uploader",
                "type": "address"
            }
        ],
        "name": "VideoRegistered",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_ipfsHash",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "uploader",
                "type": "address"
            }
        ],
        "name": "verifyVideo",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "name": "videos",
        "outputs": [
            {
                "internalType": "string",
                "name": "ipfsHash",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "uploader",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Convert contract address to checksum address
contract_address = Web3.to_checksum_address(contract_address)

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Connect to IPFS Desktop
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

@app.route('/register', methods=['POST'])
def register_video():
    try:
        ipfs_hash = request.json['ipfs_hash']
        account = request.json['account']
        tx_hash = contract.functions.registerVideo(ipfs_hash).transact({
            'from': account,
            'gas': 1000000
        })
        # Wait for transaction receipt (corrected method)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return jsonify({'status': 'Video registered'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify', methods=['POST'])
def verify_video():
    try:
        ipfs_hash = request.json['ipfs_hash']
        account = request.json['account']
        is_registered = contract.functions.verifyVideo(ipfs_hash, account).call()
        return jsonify({'is_registered': is_registered})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_videos_endpoint():
    try:
        video_path_1 = request.json['video_path_1']
        video_path_2 = request.json['video_path_2']
        result = compare_videos(video_path_1, video_path_2)
        return jsonify({'comparison_result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

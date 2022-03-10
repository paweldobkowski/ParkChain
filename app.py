from flask import Flask, jsonify

from ParkChain import ParkChain

app = Flask(__name__)

parkchain = ParkChain()

@app.route('/', methods=["GET"])
def show_the_chain():
    chain = parkchain.chain

    response = {
        'chain': chain,
        'length': len(chain),
    }

    return jsonify(response), 200

@app.route('/mine', methods=["GET"])
def mine():
    previous_hash = parkchain.get_previous_hash()

    new_block = parkchain.mine_block(previous_hash)

    return new_block

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
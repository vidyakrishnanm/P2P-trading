from brownie import accounts, config, EnergyTrade, network
import csv
import json
import time
import datetime
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("./index.html")


@app.route("/add_order")
def add_order():
    return render_template("./addorder.html")


@app.route("/buyer")
def buyer():
    return render_template("./buyer.html")


@app.route("/seller")
def seller():
    return render_template("./seller.html")

'''
Current code uses existing development accounts. Load your created accounts during private network development as below and change the calling accounts. 
account2 = accounts.load("account_1")
account3 = accounts.load("account_2")
account4 = accounts.load("account_3")
'''

@app.route("/deploy", methods=["GET"])
def trading():
    trading = EnergyTrade.deploy({"from": accounts[0]})
    response = {"status": "Contract deployed"}
    # print(trading.address)
    # print(EnergyTrade.abi)
    print(response)
    return jsonify(response), 200


def countdown(h, m, s):
    total_seconds = h * 3600 + m * 60 + s
    while total_seconds > 0:
        timer = timedelta(seconds=total_seconds)
        print(timer, end="\r")
        time.sleep(1)
        total_seconds -= 1
    print("Transfer Complete")


@app.route("/start", methods=["GET"])
def start():
    timer = countdown(0, 0, 5)
    response = {"timer": timer}
    return jsonify(response), 200


@app.route("/addOffer", methods=["POST"])
def addOffer():
    energy = request.form["energy"]
    price = request.form["price"]
    trading = EnergyTrade[-1]
    transaction = trading.addOffer(energy, price, {"from": accounts[2]})
    transaction.wait(1)
    response = {"energy": energy, "price": price, "status": "success"}
    # return json.dumps(response)
    return jsonify(response), 200


@app.route("/listOffers", methods=["GET"])
def listOffers():
    trading = EnergyTrade[-1]
    offers = trading.listOffers()
    print("Success")
    response = {"offers": offers}
    return jsonify(response), 200


@app.route("/chooseOffer", methods=["POST"])
def chooseOffer():
    id = request.form["offer_id"]
    trading = EnergyTrade[-1]
    transaction = trading.ChooseOffer(id, {"from": accounts[3]})
    transaction.wait(1)
    offer = trading.retreive_offer_by_id(id)
    energy = offer[0]
    price = offer[1]
    response = {"offer_id": id, "energy": energy, "price": price}
    return jsonify(response), 200


@app.route("/buyerConfirm", methods=["POST"])
def buyerConfirm():
    id = request.form["offer_id"]
    print(id)
    trading = EnergyTrade[-1]
    transaction = trading.confirmTx_S2B(id, {"from": accounts[3]})
    transaction.wait(1)
    response = {"status": "Payment done by buyer"}
    print(response)
    return jsonify(response), 200


@app.route("/sellerConfirm", methods=["POST"])
def sellerConfirm():
    id = request.form["offer_id"]
    print(id)
    trading = EnergyTrade[-1]
    transaction = trading.confirmTx_B2S(id, {"from": accounts[2]})
    transaction.wait(1)
    response = {"status": "Seller confirms payment"}
    print(response)
    return jsonify(response), 200


@app.route("/retreiveDetails", methods=["POST"])
def retreiveDetails():
    id = request.form["offer_id"]
    print(id)
    trading = EnergyTrade[-1]
    offers = trading.retreive_final_details(id, {"from": accounts[0]})
    print("Success")
    offered_time = datetime.fromtimestamp(offers[5])
    paid_time = datetime.fromtimestamp(offers[6])
    response = {
        "offer_id": id,
        "final_id": id,
        "seller_address": offers[1],
        "buyer_address": offers[2],
        "energy": offers[3],
        "price": offers[4],
        "offered_time": offered_time,
        "paid_time": paid_time,
        "confirm_buyer": offers[8],
        "confirm_seller": offers[9],
        "confirm_broker": offers[10],
    }
    return jsonify(response), 200


@app.route("/delivered", methods=["POST"])
def delivered():
    id = request.form["offer_id_a"]
    trading = EnergyTrade[-1]
    transaction = trading.finalDelivery(id, {"from": accounts[0]})
    transaction.wait(1)
    response = {"offer_id": id, "status": "Delivery confirmed"}
    print("{status: Delivery confirmed}")
    return jsonify(response), 200


app.run(host="0.0.0.0", port=5001)

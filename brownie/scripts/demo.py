# from datetime import datetime
from brownie import accounts, config, EnergyTrade, network
import csv

import json
import time
import datetime
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template


"""def get_account():
    if network.show_active() == "development":
        return accounts[1]
    else:
        return accounts.add(config["wallets"]["from_key"])
"""

"""
@app.route("/")
def index():
    return json.dumps("Welcome to energy trading platform")
"""
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


@app.route("/deploy", methods=["GET"])
def trading():
    # account = get_account()
    # print(account)
    trading = EnergyTrade.deploy({"from": accounts[0]})
    # transaction = trading.addOffer("100", "130", {"from": accounts[1]})
    # transaction.wait(1)
    response = {"status": "Contract deployed"}
    # print(trading.address)
    # print(EnergyTrade.abi)
    print(response)
    return jsonify(response), 200


def countdown(h, m, s):
    total_seconds = h * 3600 + m * 60 + s
    while total_seconds > 0:
        timer = timedelta(seconds=total_seconds)
        # timer = datetime.datetime.timedelta(seconds=total_seconds)
        print(timer, end="\r")
        time.sleep(1)
        total_seconds -= 1
    print("Transfer Complete")


@app.route("/start", methods=["GET"])
def start():
    timer = countdown(0, 0, 5)
    # timestamp = time.ctime()
    # time.sleep(10)
    response = {"timer": timer}
    return jsonify(response), 200


@app.route("/addOffer", methods=["POST"])
def addOffer():
    energy = request.form["energy"]
    price = request.form["price"]
    trading = EnergyTrade[-1]
    # account = get_account()
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
    # return json.dumps(offers)
    return jsonify(response), 200


@app.route("/chooseOffer", methods=["POST"])
def chooseOffer():
    # account = get_account()
    # req_data = request.get_json(force=True)
    # id = req_data["id"]
    id = request.form["offer_id"]
    trading = EnergyTrade[-1]
    transaction = trading.ChooseOffer(id, {"from": accounts[3]})
    transaction.wait(1)
    offer = trading.retreive_offer_by_id(id)
    energy = offer[0]
    price = offer[1]
    response = {"offer_id": id, "energy": energy, "price": price}
    # return json.dumps(offer)
    return jsonify(response), 200


@app.route("/buyerConfirm", methods=["POST"])
def buyerConfirm():
    # account = get_account()
    # req_data = request.get_json(force=True)
    id = request.form["offer_id"]
    # id = 0
    print(id)
    trading = EnergyTrade[-1]
    transaction = trading.confirmTx_S2B(id, {"from": accounts[3]})
    transaction.wait(1)
    response = {"status": "Payment done by buyer"}
    print(response)
    # return json.dumps(response)
    return jsonify(response), 200


@app.route("/sellerConfirm", methods=["POST"])
def sellerConfirm():
    # account = get_account()
    # req_data = request.get_json(force=True)
    id = request.form["offer_id"]
    print(id)
    trading = EnergyTrade[-1]
    transaction = trading.confirmTx_B2S(id, {"from": accounts[2]})
    transaction.wait(1)
    response = {"status": "Seller confirms payment"}
    print(response)
    return jsonify(response), 200
    # return json.dumps(response)


@app.route("/retreiveDetails", methods=["POST"])
def retreiveDetails():
    id = request.form["offer_id"]
    print(id)
    trading = EnergyTrade[-1]
    offers = trading.retreive_final_details(id, {"from": accounts[0]})
    print("Success")
    offered_time = datetime.fromtimestamp(offers[5])
    paid_time = datetime.fromtimestamp(offers[6])
    # print(offers[5])
    # print(offered_time)
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
    # return json.dumps(offers)
    return jsonify(response), 200


@app.route("/delivered", methods=["POST"])
def delivered():
    # account = get_account()
    # req_data = request.get_json(force=True)
    id = request.form["offer_id_a"]
    trading = EnergyTrade[-1]
    transaction = trading.finalDelivery(id, {"from": accounts[0]})
    transaction.wait(1)
    # final = trading.retreive_final_details(id)
    response = {"offer_id": id, "status": "Delivery confirmed"}
    print("{status: Delivery confirmed}")
    return jsonify(response), 200


app.run(host="0.0.0.0", port=5001)
# app.run()

import os, sys
import time
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from payos import PayOS, ItemData, PaymentData

load_dotenv()

BASE_URL_PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), *['..']*1))
print("Base url project", BASE_URL_PROJECT)
BASE_ANALYSIS_DIR = os.path.join(BASE_URL_PROJECT, 'data')
# PAYOS_CLIENT_ID = os.getenv("PAYOS_CLIENT_ID")
# PAYOS_API_KEY = os.getenv("PAYOS_API_KEY")
# PAYOS_CHECKSUM_KEY = os.getenv("PAYOS_CHECKSUM_KEY")
PAYOS_CLIENT_ID="948b7b46-c9df-4655-bb8b-0593f4e5b514"
PAYOS_API_KEY="5db8cf73-f38f-4907-bdf2-52e8866a6753"
PAYOS_CHECKSUM_KEY="5aab4966d795069ba4c034d224ca5b11eb613056f48d86e5b64d58fc11cf520b"
# WEB_DOMAIN = os.getenv("WEB_DOMAIN")

payos = PayOS(PAYOS_CLIENT_ID, PAYOS_API_KEY, PAYOS_CHECKSUM_KEY)
# WEB_DOMAIN='http://backfriday.beenet.vn'
WEB_DOMAIN= os.getenv("WEB_DOMAIN")

app = Flask(__name__)

@app.route("/")
def display_products():
    try:
        data = pd.read_csv(os.path.join(BASE_ANALYSIS_DIR, 'analysis.csv'))
        products = data.to_dict(orient="records")
    except Exception as e:
        return f"Error loading products: {e}", 500

    return render_template("index.html", products=products)

@app.route("/buy", methods=["POST"])
def buy_product():
    product_name = request.form.get("product_name")
    current_price = request.form.get("current_price")

    return render_template("buy_form.html", product_name=product_name, current_price=current_price)

@app.route("/payment", methods=["POST"])
def create_payment_link():
    try:
        product_name = request.form.get("product_name")
        customer_name = request.form.get("buyerName")
        phone_number = request.form.get("buyerPhone")
        current_price = int(float(request.form.get("current_price")))

        item = ItemData(name=f"{product_name} - {customer_name} ({phone_number})", quantity=1, price=current_price)
        payment_data = PaymentData(
            orderCode=int(time.time()),
            amount=current_price,
            description=f"Payment for {product_name}"[:25],
            items=[item],
            cancelUrl=WEB_DOMAIN,
            returnUrl=WEB_DOMAIN
        )
        payment_link_response = payos.createPaymentLink(payment_data)
    except Exception as e:
        return "Erro: " +  str(e)

    return render_template("payment_qr.html", checkout_url=payment_link_response.checkoutUrl)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

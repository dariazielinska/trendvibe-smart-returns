import pandas as pd


def load_data():
    tickets = pd.read_csv("data/zgloszenia_BOK.csv")
    customers = pd.read_csv("data/klienci_historia.csv")
    products = pd.read_csv("data/katalog_produktow.csv")

    df = tickets.merge(customers, on="CUSTOMER_ID", how="left")
    df = df.merge(products, on="PRODUCT_ID", how="left")

    return df
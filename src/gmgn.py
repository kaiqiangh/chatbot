import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()


class GMGNAPI:
    def __init__(self, chain, timeframe):
        self.chain = chain
        self.timeframe = timeframe
        self.base_url = f"{os.getenv("GMGN_API_URL")}/{chain}/swaps/{timeframe}"

    def get_headers():
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Cookie": "cf_clearance=bMAXOyw0ruZW_fhLSdRsSYOhw_Zw0bM89U.qTbTK6M8-1737109556-1.2.1.1-5onV7V_Or1hkq8AhGCdVtfgr35PHSnQGeujhWOmw5i8RI54uqGPU4u7dImuTNg1Yb8fD2z2aEpT1ixToJ4uzhKV7IaYWHCmedYIA2v.vwVrKkLOCUws5yNu1LG.Xh6RF1ZvG3COwIgWxPT4qJpKbWTV57zkY9CjwxT7Ql5TzkfV0Uz5MXuoIusnW5m98_aS3BjpTh6HfpYM4Djm06eMpSiq6zSNx.Mu4ywzoLDNpV5JaEha.pcTLTFpefbEbWVXyvjtvsJRkkX9b6FXExu6pbGMeJoZpJjmYFRvZr4eXL5FyDidDXaDD6kBnb_TD2UUMsIZE24RJoLlxwC0GyotYYQ;",
        }

    def get_data(self):
        try:
            headers = GMGNAPI.get_headers()
            filters = ["renounced", "not_wash_trading"]
            if self.chain != "sol":
                filters.append("not_honeypot")
                filters.append("verified")

            if self.chain == "sol":
                filters.append("frozen")

            params = {
                "orderby": "swaps",
                "direction": "desc",
                "filters[]": filters,
                "limit": 5,
            }
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching GMGN data: {str(e)}")
            return None

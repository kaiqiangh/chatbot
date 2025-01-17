import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()


class GMGNAPI:
    chain = "sol"
    timeframe = "1h"
    BASE_URL = f"{os.getenv("GMGN_API_URL")}/{chain}/swaps/{timeframe}"

    @staticmethod
    def get_headers():
        return {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Cookie": "cf_clearance=bMAXOyw0ruZW_fhLSdRsSYOhw_Zw0bM89U.qTbTK6M8-1737109556-1.2.1.1-5onV7V_Or1hkq8AhGCdVtfgr35PHSnQGeujhWOmw5i8RI54uqGPU4u7dImuTNg1Yb8fD2z2aEpT1ixToJ4uzhKV7IaYWHCmedYIA2v.vwVrKkLOCUws5yNu1LG.Xh6RF1ZvG3COwIgWxPT4qJpKbWTV57zkY9CjwxT7Ql5TzkfV0Uz5MXuoIusnW5m98_aS3BjpTh6HfpYM4Djm06eMpSiq6zSNx.Mu4ywzoLDNpV5JaEha.pcTLTFpefbEbWVXyvjtvsJRkkX9b6FXExu6pbGMeJoZpJjmYFRvZr4eXL5FyDidDXaDD6kBnb_TD2UUMsIZE24RJoLlxwC0GyotYYQ;",
        }

    @staticmethod
    def get_data():
        try:
            headers = GMGNAPI.get_headers()
            params = {
                "orderby": "swaps",
                "direction": "desc",
                "filters[]": ["renounced", "frozen", "not_wash_trading"],
                "limit": 5,
            }
            response = requests.get(GMGNAPI.BASE_URL, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching GMGN data: {str(e)}")
            return None

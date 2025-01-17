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
            "Cookie": "cf_clearance=D4GNxcYfuX2M1oJx30pCtoRJPJ78t7zlriO4z2w_CgY-1737131518-1.2.1.1-wiQj_F4Yq4cvo9WL0MAIa4DHycxZgygCYZBjwkD4orVwmIY9EZW4Hr4jwwOMSyS6M5c_CyzrtqCbvvle2CCZqV5PyU0vg.uULIu5pp2fjdLQy_WUhCMX2Q6oqJ8yfw4MuFl3m0Cya7yFMjNDMTLpAFxPtRMaCgEHD5_m5QhmCBbLrgtZEtpqUegUSCh4J3.N_hn12TxumBvG0e1QddhBvGSqK.SpBLD_wb_V9FRRd7c7rhyfAXm5CyoOlb0EFbiPzwUNvOCck3wAGSiJbSutS24mGoh5VBBJ1XkQPoMwmyBAt5fj._5PxyMUiGrOX5wqBr9r_gvBKf.4W7FE2BgnhQ;",
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

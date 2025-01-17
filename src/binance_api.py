import requests
import pandas as pd
import streamlit as st


class BinanceAPI:
    BASE_URL = "https://api.binance.com/api/v3"

    @staticmethod
    def check_symbol_exists(symbol):
        try:
            info_url = f"{BinanceAPI.BASE_URL}/exchangeInfo"
            response = requests.get(info_url)
            response.raise_for_status()
            symbols = [s["symbol"] for s in response.json()["symbols"]]
            return f"{symbol}USDT" in symbols
        except Exception as e:
            st.error(f"Error checking trading pair: {str(e)}")
            return False

    @staticmethod
    def get_klines_data(symbol, interval, limit=200):
        try:
            klines_url = f"{BinanceAPI.BASE_URL}/klines"
            params = {"symbol": f"{symbol}USDT", "interval": interval, "limit": limit}
            response = requests.get(klines_url, params=params)
            response.raise_for_status()

            # Process K-line data
            df = pd.DataFrame(
                response.json(),
                columns=[
                    "timestamp",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "close_time",
                    "quote_volume",
                    "trades",
                    "taker_buy_base",
                    "taker_buy_quote",
                    "ignore",
                ],
            )

            # Convert data types
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            for col in ["open", "high", "low", "close", "volume"]:
                df[col] = df[col].astype(float)

            return df
        except Exception as e:
            st.error(f"Error getting K-line data: {str(e)}")
            return None

    @staticmethod
    def get_market_sentiment():
        try:
            info_url = f"{BinanceAPI.BASE_URL}/ticker/24hr"
            response = requests.get(info_url)
            response.raise_for_status()
            data = response.json()
            usdt_pairs = [item for item in data if item["symbol"].endswith("USDT")]
            total_pairs = len(usdt_pairs)
            if total_pairs == 0:
                return "Unable to get USDT trading pair data"

            up_pairs = [
                item for item in usdt_pairs if float(item["priceChangePercent"]) > 0
            ]
            up_percentage = (len(up_pairs) / total_pairs) * 100

            # Classify sentiment
            if up_percentage >= 80:
                sentiment = "extremely optimistic"
            elif up_percentage >= 60:
                sentiment = "optimistic"
            elif up_percentage >= 40:
                sentiment = "neutral"
            elif up_percentage >= 20:
                sentiment = "pessimistic"
            else:
                sentiment = "extremely pessimistic"

            return f"Market sentiment: {sentiment} (upward trading pairs ratio {up_percentage:.2f}%)"
        except Exception as e:
            return f"Error getting market sentiment: {str(e)}"

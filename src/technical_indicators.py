class TechnicalIndicators:
    @staticmethod
    def calculate_indicators(df):
        # Calculate MA20
        df["ma20"] = df["close"].rolling(window=20).mean()

        # Calculate BOLL indicators
        df["boll_mid"] = df["close"].rolling(window=20).mean()
        df["boll_std"] = df["close"].rolling(window=20).std()
        df["boll_up"] = df["boll_mid"] + 2 * df["boll_std"]
        df["boll_down"] = df["boll_mid"] - 2 * df["boll_std"]

        # Calculate MA20 trend
        df["ma20_trend"] = df["ma20"].diff().rolling(window=5).mean()

        return df

    @staticmethod
    def analyze_trend(df):
        current_price = df["close"].iloc[-1]
        ma20_trend = "upward" if df["ma20_trend"].iloc[-1] > 0 else "downward"

        # BOLL support and resistance
        boll_up = df["boll_up"].iloc[-1]
        boll_mid = df["boll_mid"].iloc[-1]
        boll_down = df["boll_down"].iloc[-1]

        return {
            "current_price": current_price,
            "ma20_trend": ma20_trend,
            "support_resistance": {
                "strong_resistance": boll_up,
                "middle_line": boll_mid,
                "strong_support": boll_down,
            },
        }

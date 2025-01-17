class TechnicalIndicators:
    @staticmethod
    def calculate_indicators(df):
        # Calculate MA20
        df["ma20"] = df["close"].rolling(window=20).mean()

        # Calculate BOLL indicators
        df["boll_mid"] = df["close"].rolling(window=20).mean()
        df["boll_std"] = df["close"].rolling(window=20).std()
        df["boll_up"] = df["boll_mid"] + 2 * df["boll_std"]
        df["boll_down"] = df["boll_mid"] - df["boll_std"]

        # Calculate MA20 trend
        df["ma20_trend"] = df["ma20"].diff().rolling(window=5).mean()

        # Calculate RSI
        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # Calculate MACD
        df["ema12"] = df["close"].ewm(span=12, adjust=False).mean()
        df["ema26"] = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = df["ema12"] - df["ema26"]
        df["signal"] = df["macd"].ewm(span=9, adjust=False).mean()

        # Calculate EMA
        df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
        df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

        # Calculate ATR
        df["tr1"] = df["high"] - df["low"]
        df["tr2"] = abs(df["high"] - df["close"].shift())
        df["tr3"] = abs(df["low"] - df["close"].shift())
        df["tr"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
        df["atr"] = df["tr"].rolling(window=14).mean()

        # Drop intermediate columns
        df.drop(columns=["tr1", "tr2", "tr3"], inplace=True)
        df["atr"] = df["tr"].rolling(window=14).mean()

        # Calculate CCI
        tp = (df["high"] + df["low"] + df["close"]) / 3
        df["cci"] = (tp - tp.rolling(window=20).mean()) / (
            0.015 * tp.rolling(window=20).std()
        )

        # Calculate Stochastic Oscillator
        df["low14"] = df["low"].rolling(window=14).min()
        df["high14"] = df["high"].rolling(window=14).max()
        df["%K"] = (df["close"] - df["low14"]) * 100 / (df["high14"] - df["low14"])
        df["%D"] = df["%K"].rolling(window=3).mean()

        # Calculate Fibonacci Retracement Levels
        max_price = df["close"].max()
        min_price = df["close"].min()
        diff = max_price - min_price
        df["fib_23.6"] = max_price - 0.236 * diff
        df["fib_38.2"] = max_price - 0.382 * diff
        df["fib_50.0"] = max_price - 0.5 * diff
        df["fib_61.8"] = max_price - 0.618 * diff
        df["fib_100.0"] = min_price

        return df

    @staticmethod
    def analyse_trend(df):
        current_price = df["close"].iloc[-1]
        ma20_trend = "upward" if df["ma20_trend"].iloc[-1] > 0 else "downward"

        # BOLL support and resistance
        boll_up = df["boll_up"].iloc[-1]
        boll_mid = df["boll_mid"].iloc[-1]
        boll_down = df["boll_down"].iloc[-1]

        # Additional indicators
        rsi = df["rsi"].iloc[-1]
        macd = df["macd"].iloc[-1]
        signal = df["signal"].iloc[-1]
        ema50 = df["ema50"].iloc[-1]
        ema200 = df["ema200"].iloc[-1]
        atr = df["atr"].iloc[-1]
        cci = df["cci"].iloc[-1]
        stochastic_k = df["%K"].iloc[-1]
        stochastic_d = df["%D"].iloc[-1]
        fib_23_6 = df["fib_23.6"].iloc[-1]
        fib_38_2 = df["fib_38.2"].iloc[-1]
        fib_50_0 = df["fib_50.0"].iloc[-1]
        fib_61_8 = df["fib_61.8"].iloc[-1]
        fib_100_0 = df["fib_100.0"].iloc[-1]

        return {
            "current_price": current_price,
            "ma20_trend": ma20_trend,
            "support_resistance": {
                "strong_resistance": boll_up,
                "middle_line": boll_mid,
                "strong_support": boll_down,
            },
            "rsi": rsi,
            "macd": macd,
            "signal": signal,
            "ema50": ema50,
            "ema200": ema200,
            "atr": atr,
            "cci": cci,
            "stochastic": {
                "%K": stochastic_k,
                "%D": stochastic_d,
            },
            "fibonacci": {
                "23.6%": fib_23_6,
                "38.2%": fib_38_2,
                "50.0%": fib_50_0,
                "61.8%": fib_61_8,
                "100.0%": fib_100_0,
            },
        }

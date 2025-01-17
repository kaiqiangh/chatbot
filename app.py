import streamlit as st
from datetime import datetime
from src.crypto_ai import CryptoAI
from src.binance_api import BinanceAPI
from src.technical_indicators import TechnicalIndicators
from src.gmgn import GMGNAPI
from dotenv import load_dotenv
import os

load_dotenv()
# --- Page Config ---
st.set_page_config(
    page_title="Crypto AI Agent", layout="wide", initial_sidebar_state="expanded"
)

# Initialize CryptoAI
crypto_ai = CryptoAI(
    api_key=os.getenv("LLM_API_KEY"),
    model=os.getenv("LLM_MODEL"),
)


# --- Custom CSS & Markdown ---
def load_custom_css():
    with open("src/style.css") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Inject custom CSS
load_custom_css()


def meme_trending_page():
    st.markdown("# Trending Meme Analysis")
    col1, col2 = st.columns(2)
    with col1:
        chain = st.selectbox("Chain", options=["sol", "eth", "base", "bsc"], index=0)

    with col2:
        timeframe = st.selectbox(
            "Timeframe", options=["1m", "5m", "1h", "6h", "24h"], index=1
        )

    gmgn_client = GMGNAPI(chain, timeframe)
    analyze_button = st.button("Start", type="primary")

    if analyze_button:
        data = gmgn_client.get_data()

        with st.spinner(
            f"Analysing Trending Meme Tokens on {chain.upper()} for {timeframe} timeframe..."
        ):
            meme_report = crypto_ai.generate_meme_report(data, chain, timeframe)
            st.write(meme_report, unsafe_allow_html=True)
            st.caption(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def binance_market_analysis():
    st.markdown("# Binance Market Analysis")
    instructions_md = """
        ### Instructions

        - **Enter a symbol** (e.g., BTC, ETH, SOL, etc.).
        - Crypto AI Agent will **automatically analyse** the market status across multiple timeframes:
            1. Provide **trend analysis** and **market sentiment**.
            2. Provide **detailed trading plans**.
            3. Generate tweets with different styles.
    """
    st.markdown(instructions_md)

    col1, col2 = st.columns([2, 1])

    with col1:
        symbol = st.text_input(
            "Enter a Symbol (e.g., BTC, ETH, SOL)", value="BTC"
        ).upper()
    with col2:
        analyze_button = st.button("Start", type="primary")

    st.markdown("---")

    if analyze_button:
        # Check if the token exists
        if BinanceAPI.check_symbol_exists(symbol):
            with st.spinner(f"Analysing market status of {symbol}..."):
                all_timeframe_analysis = {}
                # Get data and analyse for each timeframe
                timeframes = {
                    "5m": {"interval": "5m", "name": "5 minutes"},
                    "15m": {"interval": "15m", "name": "15 minutes"},
                    "1h": {"interval": "1h", "name": "1 hour"},
                    "4h": {"interval": "4h", "name": "4 hours"},
                    "1d": {"interval": "1d", "name": "daily"},
                }
                for tf, info in timeframes.items():
                    df = BinanceAPI.get_klines_data(symbol, info["interval"])
                    if df is not None:
                        df = TechnicalIndicators.calculate_indicators(df)
                        analysis = TechnicalIndicators.analyse_trend(df)
                        all_timeframe_analysis[info["name"]] = analysis
                # Display current price
                current_price = all_timeframe_analysis["daily"]["current_price"]
                st.metric(
                    label=f"Current Price: {symbol}/USDT",
                    value=(
                        f"${current_price:,.8f}"
                        if current_price < 0.1
                        else f"${current_price:,.3f}"
                    ),
                )

                # Generate trading plan
                trading_plan = crypto_ai.generate_trading_plan(symbol)

                # Get and display AI analysis
                st.subheader("Multi-Timeframe Analysis Report")
                analysis = crypto_ai.get_ai_analysis(
                    symbol, all_timeframe_analysis, trading_plan
                )
                st.write(analysis, unsafe_allow_html=True)

                # Add market sentiment
                market_sentiment = BinanceAPI.get_market_sentiment()
                st.markdown("---")
                st.subheader("Market Sentiment")
                st.markdown(market_sentiment)

                # Generate tweets
                st.markdown("---")
                st.subheader("Multi-Style Tweet Suggestions")

                analysis_summary = f"{analysis}\nMarket sentiment: {market_sentiment}"

                # Define all styles
                styles = {"Trader Style": "trader", "Media Style": "media"}

                # Create two-column layout to display tweets
                col1, col2 = st.columns(2)

                # Generate and display tweets for all styles
                for i, (style_name, style) in enumerate(styles.items()):
                    tweet = crypto_ai.generate_tweet(symbol, analysis_summary, style)
                    # Display the first two styles in the left column
                    if i < 1:
                        with col1:
                            st.subheader(f"📝 {style_name}")
                            st.text_area(
                                label="",
                                value=tweet,
                                height=150,
                                key=f"tweet_{style}",
                            )
                    # Display the last two styles in the right column
                    else:
                        with col2:
                            st.subheader(f"📝 {style_name}")
                            st.text_area(
                                label="",
                                value=tweet,
                                height=150,
                                key=f"tweet_{style}",
                            )

                # Add timestamp
                st.caption(
                    f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
        else:
            st.error(
                f"Error: {symbol}USDT trading pair does not exist on Binance, please check if the token code is correct."
            )


def main():
    with st.sidebar:
        st.subheader("Tools")
        page = st.selectbox(
            "Select a tool:", ["Binance Market Analysis", "Trending Meme"]
        )

        st.markdown("---")
        st.subheader("Notes")
        st.write(
            "Please ensure your analysis is for reference only and does not constitute investment advice. The crypto market is highly risky, please make decisions cautiously."
        )

    if page == "Binance Market Analysis":
        binance_market_analysis()
    elif page == "Trending Meme":
        meme_trending_page()

    # Add footer
    st.markdown("---")
    st.caption(
        "Disclaimer: This analysis is for reference only and does not constitute investment advice. The crypto market is highly risky, please make decisions cautiously."
    )


# Run the main function
if __name__ == "__main__":
    main()

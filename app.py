import streamlit as st
from datetime import datetime
import time

from src.crypto_ai import CryptoAI
from src.binance_api import BinanceAPI
from src.technical_indicators import TechnicalIndicators

# --- Page Config ---
st.set_page_config(
    page_title="Crypto AI Agent", layout="wide", initial_sidebar_state="expanded"
)


# --- Custom CSS & Markdown ---
def load_custom_css():
    st.markdown(
        """
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;600&display=swap" rel="stylesheet">
    
    <style>
    /* LIGHTER BACKGROUND - Neon Gradient */
    body {
        background: linear-gradient(135deg, #1a1aff, #00ffff, #ff66ff); /* Neon blue & cyan gradient */
        color: #222222; /* Dark gray for readability */
        font-family: 'Orbitron';
    }

    /* Main Content Container - Glassmorphism */
    .main, .block-container {
        background: rgba(255, 255, 255, 0.8); /* Light frosted glass effect */
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 0 15px rgba(0, 0, 255, 0.3);
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #222222; /* Darker text for contrast */
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Buttons - Neon Glow */
    .stButton button {
        background: linear-gradient(90deg, #ff00ff, #00ffff);
        color: #ffffff;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        cursor: pointer;
        transition: 0.3s ease-in-out;
        box-shadow: 0 0 10px #ff00ff, 0 0 20px #00ffff;
    }
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px #ff00ff, 0 0 30px #00ffff;
    }

    /* Input Fields - Modern Look */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.8);
        color: #222222;
        font-family: 'Orbitron';
        border: 2px solid #00ffff;
        border-radius: 8px;
        padding: 10px;
    }

    /* Sidebar - Glass Panel */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(8px);
        color: #222222;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
    }
    
    /* Sidebar Headers */
    .css-1d391kg .css-1cpxqw2 {
        color: #ff00ff;
        font-weight: bold;
    }
    .css-1d391kg .css-1cpxqw2:hover {
        color: #00ffff;
    }

    /* Sidebar Notes */
    .css-17lntkn {
        color: #444444;
        font-size: 14px;
        font-style: italic;
    }

    /* Divider Line */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, #ff00ff, #00ffff);
        margin: 15px 0;
    }

    /* Animated Glow */
    @keyframes neon-glow {
        0% { text-shadow: 0 0 5px #ff00ff; }
        50% { text-shadow: 0 0 20px #ff00ff; }
        100% { text-shadow: 0 0 5px #ff00ff; }
    }
    h1, h2 {
        animation: neon-glow 1.5s infinite alternate;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )


# Inject custom CSS
load_custom_css()

st.markdown(
    "<h1 style='font-family: Orbitron, sans-serif; text-align: center;'>Crypto AI Agent</h1>",
    unsafe_allow_html=True,
)


def display_instructions():
    instructions_html = """
    <style>
        .orbitron-font {
            font-family: 'Orbitron', sans-serif;
        }
    </style>
    <h2 style='font-family: Orbitron, sans-serif;'>Instructions</h2>
    <div class="orbitron-font">
        <ul>
            <li><strong>Enter the trading symbol</strong> (e.g., BTC, ETH, SOL, etc.).</li>
            <li>The AI Agent will <strong>automatically analyze</strong> the market status across multiple timeframes.</li>
            <li>Provide <strong>professional trend analysis</strong> and predictions.</li>
            <li>Analyze <strong>overall market sentiment</strong>.</li>
            <li>Provide <strong>detailed trading plans</strong>.</li>
            <li>Generate a tweet.</li>
        </ul>
    </div>
    """
    st.markdown(instructions_html, unsafe_allow_html=True)


def solana_meme_page():
    st.title("Solana Meme")
    st.write("This is the Solana Meme page content.")


def main():
    with st.sidebar:
        st.subheader("Pages")
        page = st.selectbox(
            "Select a page:", ["Binance Market Analysis", "Solana Meme"]
        )

        st.markdown("---")
        st.subheader("Notes")
        st.write(
            "Please ensure your analysis is for reference only and does not constitute investment advice. The cryptocurrency market is highly risky, please make decisions cautiously."
        )

    if page == "Binance Market Analysis":
        # Page Title & Description
        st.markdown(
            "<h2 style='font-family: Orbitron, sans-serif; text-align: center;'>Binance Market Analysis</h2>",
            unsafe_allow_html=True,
        )
        display_instructions()
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
                            analysis = TechnicalIndicators.analyze_trend(df)
                            all_timeframe_analysis[info["name"]] = analysis

                    # Display current price
                    current_price = all_timeframe_analysis["daily"]["current_price"]
                    st.metric(
                        label=f"{symbol}/USDT Current Price",
                        value=(
                            f"${current_price:,.8f}"
                            if current_price < 0.1
                            else f"${current_price:,.2f}"
                        ),
                    )

                    # Initialize CryptoAI
                    crypto_ai = CryptoAI(
                        api_key="sk-643fbf4918914ba687f4cd12f2004f50",
                        model="deepseek-chat",
                    )

                    # Generate trading plan
                    trading_plan = crypto_ai.generate_trading_plan(symbol)

                    # Get and display AI analysis
                    st.subheader("Multi-Timeframe Analysis Report")
                    analysis = crypto_ai.get_ai_analysis(
                        symbol, all_timeframe_analysis, trading_plan
                    )
                    st.markdown(analysis)

                    # Add market sentiment
                    market_sentiment = BinanceAPI.get_market_sentiment()
                    st.markdown("---")
                    st.subheader("Overall Market Sentiment")
                    st.write(market_sentiment)

                    # Generate tweets
                    st.markdown("---")
                    st.subheader("Multi-Style Tweet Suggestions")

                    analysis_summary = (
                        f"{analysis}\nMarket sentiment: {market_sentiment}"
                    )

                    # Define all styles
                    styles = {"Trader Style": "trader", "Media Style": "media"}

                    # Create two-column layout to display tweets
                    col1, col2 = st.columns(2)

                    # Generate and display tweets for all styles
                    for i, (style_name, style) in enumerate(styles.items()):
                        tweet = crypto_ai.generate_tweet(
                            symbol, analysis_summary, style
                        )
                        # Display the first two styles in the left column
                        if i < 2:
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
                        f"Analysis time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
            else:
                st.error(
                    f"Error: {symbol}USDT trading pair does not exist on Binance, please check if the token code is correct."
                )
    elif page == "Solana Meme":
        solana_meme_page()

    # Add footer
    st.markdown("---")
    st.caption(
        "Disclaimer: This analysis is for reference only and does not constitute investment advice. The cryptocurrency market is highly risky, please make decisions cautiously."
    )


# Run the main function
if __name__ == "__main__":
    main()

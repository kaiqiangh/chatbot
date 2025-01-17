from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class CryptoAI:
    def __init__(self, api_key, model):
        self.client = OpenAI(api_key=api_key, base_url=os.getenv("LLM_API_URL"))
        self.model = model

    def generate_content(self, prompt, role="user"):
        try:
            response = self.client.chat.completions.create(
                model=self.model, messages=[{"role": role, "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Failed to generate content: {str(e)}"

    def generate_trading_plan(self, symbol):
        prompt = f"""
        Please provide a detailed trend-following trading plan for the {symbol}/USDT trading pair. Include but not limited to entry points, stop-loss points, target prices, and fund management strategies.
        """
        return self.generate_content(prompt)

    def generate_tweet(self, symbol, analysis_summary, style):
        style_prompts = {
            "trader": "in a professional trader tone",
            "media": "in an objective media tone",
        }
        style_prompt = style_prompts.get(style, "")
        prompt = f"""
        {style_prompt} Please write a concise and professional tweet for the {symbol}/USDT trading pair based on the following analysis summary, suitable for posting on Twitter. The tweet should include the current price, market sentiment, main trends, and operational suggestions. Limit to 280 characters.

        Analysis summary:
        {analysis_summary}
        """
        return self.generate_content(prompt)

    def get_ai_analysis(self, symbol, analysis_data, trading_plan):
        prompt = f"""
        As a professional cryptocurrency analyst, please provide a detailed market report based on the following multi-timeframe analysis data for {symbol}:

        Multi-timeframe trend analysis:
        {analysis_data}

        Detailed trading plan:
        {trading_plan}

        Please provide the following analysis (in markdown format):

        ## Market Overview
        [Overall judgment under the multi-timeframe analysis framework]

        ## Trend Analysis
        - Short-term trend (5 minutes - 15 minutes):
        - Medium-term trend (1 hour - 4 hours):
        - Long-term trend (daily):
        - Trend coherence analysis:

        ## Key Levels
        - Major resistance levels:
        - Major support levels:
        - Current price position analysis:

        ## Future Target Predictions
        1. 24-hour target:
        2. 3-day target:
        3. 7-day target:

        ## Operational Suggestions
        - Short-term operations:
        - Medium-term layout:
        - Risk warnings:

        Please ensure the analysis is professional, objective, and pays attention to the relationship between different timeframes.
        """
        return self.generate_content(prompt)

    def generate_meme_report(self, meme_data, chain, timeframe):
        prompt = f"""
                As a professional meme trending token analyst, please provide a detailed market report based on the following data:

                The data of trending meme tokens on the {chain} chain under the {timeframe} timeframe:
                {meme_data}

                Please provide the following analysis (in markdown format) with well-structured analysis of the token's performance and potential future trends:

                ## Market Overview
                - considering key metrics such as price change percentage, trading volume, liquidity, and market capitalization.
                - Evaluate the hot level and its relevance to market momentum.
                - Discuss the buy/sell ratio and what it suggests about market sentiment.
                - Analyze the holder count and distribution, focusing on top 10 holders and their influence.

                ## Trend Analysis
                - Analyze trading activity, including number of swaps and liquidity trends based on multi-timeframe price change data if provided.
                - Assess the impact of whale activity, particularly in relation to bluechip owners and smart degen traders.
                - Consider any significant social sentiment signals, such as the token’s Twitter engagement and Telegram activity.

                ## Risk Assessment
                - Evaluate the token’s contract security, including the impact of renounced minting and freeze account status.
                - Assess potential market manipulation risks, including wash trading and concentration of ownership.
                - Identify any early warning signs that could indicate liquidity risks or developer interventions.

                ## Operational Suggestions
                - Provide strategic recommendations for traders based on current market conditions.
                - Offer guidance for long-term holders, considering factors like liquidity stability and community engagement.
                - Suggest potential catalysts for future price movements, including marketing efforts, exchange listings, or social media campaigns.

                Please ensure the analysis is professional, data-driven, and comprehensive, highlighting any potential opportunities or risks.
            """
        return self.generate_content(prompt)

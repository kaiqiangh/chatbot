from openai import OpenAI


class CryptoAI:
    def __init__(self, api_key, model):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
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

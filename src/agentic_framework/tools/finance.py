from typing import Dict, Any
import yfinance as yf
from agentic_framework.core.tool import Tool

class FundamentalAnalysisTool(Tool):
    """Tool for performing fundamental analysis on a stock ticker."""
    
    def __init__(self):
        super().__init__(
            name="fundamental_analysis",
            description="Get fundamental financial data for a stock ticker (e.g., AAPL, MSFT).",
            category="finance"
        )
    
    async def execute(self, ticker: str, detailed: bool = False) -> Dict[str, Any]:
        """
        Get fundamental analysis data for a ticker.
        
        Args:
            ticker: The stock ticker symbol (e.g., 'AAPL')
            detailed: If True, includes Balance Sheet, Income Statement, and Cash Flow.
            
        Returns:
            Dictionary containing financial info, ratios, and recent news
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract key metrics
            analysis = {
                "symbol": info.get("symbol"),
                "shortName": info.get("shortName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "marketCap": info.get("marketCap"),
                "currentPrice": info.get("currentPrice"),
                "targetMeanPrice": info.get("targetMeanPrice"),
                "recommendationKey": info.get("recommendationKey"),
                "forwardPE": info.get("forwardPE"),
                "dividendYield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
                "businessSummary": info.get("longBusinessSummary"),
            }
            
            if detailed:
                # Add deep financial data (converting DataFrames to dicts)
                try:
                    analysis["balance_sheet"] = stock.balance_sheet.to_dict()
                    analysis["income_statement"] = stock.income_stmt.to_dict()
                    analysis["cash_flow"] = stock.cashflow.to_dict()
                except Exception as e:
                    analysis["financials_error"] = f"Could not retrieve deep financials: {str(e)}"

            # Add recent news if available
            news = stock.news
            if news:
                analysis["recent_news"] = [
                    {
                        "title": item.get("title"),
                        "publisher": item.get("publisher"),
                        "link": item.get("link"),
                        "relatedTickers": item.get("relatedTickers")
                    }
                    for item in news[:3]  # Limit to 3 recent news items
                ]
                
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed for {ticker}: {str(e)}"}

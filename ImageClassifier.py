import streamlit as st
import requests
import json
from datetime import datetime

def main():
    st.title("Stock Details App")
    userInput=st.text_input("Enter a cryptocurrency:")
    if userInput:
        coinsListResponse=requests.get("https://api.coingecko.com/api/v3/coins/list")
        if coinsListResponse.status_code==200:
            jsonResponse=coinsListResponse.json()
            cryptocurrencies=[crypto['name'] for crypto in jsonResponse]
            if any(userInput.lower()==cryptocurrency.lower() for cryptocurrency in cryptocurrencies):
                #Plot the coins price over the last year
                historicalRatesResponse=requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=CAD&days=365&precision=2")
                if historicalRatesResponse.status_code==200:
                    prices=historicalRatesResponse.json()['prices']
                    print(datetime.fromtimestamp(float("1681430400000")).strftime('%Y-%m %H:%M:%S'))
                else:
                    st.error("Error while fetching the historical prices of the cryptocurrency. Please try again.")
            else:
                st.error("Invalid cryptocurrency!")
        else:
            st.error("Error while fetching the valid coins list from API. Please try again.")

if __name__=='__main__':
    main()

# datetimeStr=datetime.fromtimestamp(float("1681516800000")/1000)
# print(datetimeStr.strftime('%Y-%m'))

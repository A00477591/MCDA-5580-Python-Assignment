import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plot
from matplotlib.dates import DateFormatter

def main():
    st.title("Stock Details App")
    userInput=st.text_input("Enter a cryptocurrency:")
    if userInput:
        coinsListResponse=requests.get("https://api.coingecko.com/api/v3/coins/list")
        if coinsListResponse.status_code==200:
            jsonResponse=coinsListResponse.json()
            cryptocurrencies=[(crypto['id'],crypto['name']) for crypto in jsonResponse]
            crypto=next((cryptocurrency for cryptocurrency in cryptocurrencies if userInput.lower()==cryptocurrency[1].lower()),None)
            if crypto:
                #Plot the coins price over the last year
                historicalRatesResponse=requests.get(f"https://api.coingecko.com/api/v3/coins/{crypto[0]}/market_chart?vs_currency=CAD&days=365&precision=2")
                if historicalRatesResponse.status_code==200:
                    priceDetails=historicalRatesResponse.json()['prices']
                    dates,prices=[],[]
                    for priceDetail in priceDetails:
                        dates.append(datetime.fromtimestamp(float(priceDetail[0])/1000).date())
                        prices.append(priceDetail[1])
                    fig,ax=plot.subplots()
                    ax.plot(dates,prices)
                    plot.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))
                    plot.gca().yaxis.set_major_formatter(plot.FuncFormatter(lambda x,_:int(x)))
                    ax.set_xlabel("Dates")
                    ax.set_ylabel("Prices")
                    ax.set_title(userInput+" prices over the last year")
                    st.pyplot(fig)
                    highestPrice=max(prices)
                    lowestPrice=min(prices)
                    st.write(f"<p style='font-size: 24px;'>{userInput} traded the highest on <b>{dates[prices.index(highestPrice)].strftime('%d %B %Y')}</b> at the price <b>{highestPrice}</b></p>",unsafe_allow_html=True)
                    st.write(f"<p style='font-size: 24px;'>{userInput} traded the lowest on <b>{dates[prices.index(lowestPrice)].strftime('%d %B %Y')}</b> at the price <b>{lowestPrice}</b></p>",unsafe_allow_html=True)
                else:
                    st.error("Error while fetching the historical prices of "+userInput+". Please try again.")
            else:
                st.error("Invalid cryptocurrency!")
        else:
            st.error("Error while fetching the valid coins list from API. Please try again.")

if __name__=='__main__':
    main()
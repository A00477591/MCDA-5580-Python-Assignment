from cProfile import label
import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plot
from matplotlib.dates import DateFormatter

def main():
    API_KEY='CG-iAokExJ9Rmts5W5tdN2KjRVw'
    params={'x_cg_demo_api_key':API_KEY}
    apiRequest=requests.Session()
    apiRequest.params.update(params)
    st.title("Coin Comparison App")
    cryptoInput1=st.text_input("Cryptocurrency 1:")
    cryptoInput2=st.text_input("Cryptocurrency 2:")
    options={'1 Week':7,'1 Month':31,'1 Year':365}
    timeframe=st.selectbox("Time period:",list(options.keys()))
    if cryptoInput1 and cryptoInput2:
        coinsListResponse=apiRequest.get("https://api.coingecko.com/api/v3/coins/list")
        if coinsListResponse.status_code==200:
            jsonResponse=coinsListResponse.json()
            cryptocurrencies=[(crypto['id'],crypto['name']) for crypto in jsonResponse]
            crypto1=next((cryptocurrency for cryptocurrency in cryptocurrencies if cryptoInput1.lower()==cryptocurrency[1].lower()),None)
            crypto2=next((cryptocurrency for cryptocurrency in cryptocurrencies if cryptoInput2.lower()==cryptocurrency[1].lower()),None)
            if not(crypto1):
                st.error(cryptoInput1+" is not a valid cryptocurrency")
            elif not(crypto2):
                st.error(cryptoInput2+" is not a valid cryptocurrency")
            else:
                #Plot the coins price over the last year
                historicalRatesResponse1=apiRequest.get(f"https://api.coingecko.com/api/v3/coins/{crypto1[0]}/market_chart?vs_currency=CAD&days={options[timeframe]}&precision=2")
                historicalRatesResponse2=apiRequest.get(f"https://api.coingecko.com/api/v3/coins/{crypto2[0]}/market_chart?vs_currency=CAD&days={options[timeframe]}&precision=2")
                if historicalRatesResponse1.status_code!=200:
                    st.error("Error while fetching the historical prices of "+cryptoInput1+". Please try again.")
                elif historicalRatesResponse2.status_code!=200:
                    st.error("Error while fetching the historical prices of "+cryptoInput2+". Please try again.")
                else:
                    crypto1PriceDetails=historicalRatesResponse1.json()['prices']
                    crypto2PriceDetails=historicalRatesResponse2.json()['prices']
                    dates1,prices1,dates2,prices2=[],[],[],[]
                    for priceDetail in crypto1PriceDetails:
                        dates1.append(datetime.fromtimestamp(float(priceDetail[0])/1000).date())
                        prices1.append(priceDetail[1])
                    for priceDetail in crypto2PriceDetails:
                        dates2.append(datetime.fromtimestamp(float(priceDetail[0])/1000).date())
                        prices2.append(priceDetail[1])
                    fig,ax=plot.subplots()
                    ax.plot(dates1,prices1,label=cryptoInput1)
                    ax.plot(dates2,prices2,label=cryptoInput2)
                    if timeframe=='1 Week':
                        plot.gca().xaxis.set_major_formatter(DateFormatter('%d %b %Y'))
                    elif timeframe=='1 Month':
                        plot.gca().xaxis.set_major_formatter(DateFormatter('%d %b %Y'))
                    else:
                        plot.gca().xaxis.set_major_formatter(DateFormatter('%b %Y'))
                    plot.gca().yaxis.set_major_formatter(plot.FuncFormatter(lambda x,_:int(x)))
                    ax.set_xlabel("Dates")
                    ax.set_ylabel("Prices")
                    ax.set_title(cryptoInput1+" vs "+cryptoInput2+" prices over the past "+timeframe)
                    ax.legend()
                    ax.tick_params(axis='x',labelsize=8)
                    ax.set_xticklabels(ax.get_xticklabels(), rotation=25)
                    st.pyplot(fig)
        else:
            st.error("Error while fetching the valid coins list from API. Please try again.")

if __name__=='__main__':
    main()
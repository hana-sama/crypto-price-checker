import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('暗号通貨、米株価追跡アプリ')

st.sidebar.write("""
# 暗号通貨、米代表銘柄株価
こちらは暗号通貨および米代表銘柄の価格可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")
days = st.sidebar.slider('日数', 1, 100, 50)


@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        ticker = yf.Ticker(tickers[company])
        hist = ticker.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try:
    st.sidebar.write("""
    ## 価格の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定してください。',
        0.0, 3000.0, (0.0, 3000.0))

    st.write(f"""
    ### 過去 **{days}** の価格の推移
    """)

    tickers = {
        'Bitcoin': 'BTC-USD',
        'Ethereum': 'ETH-USD',
        'Cardano': 'ADA-USD',
        'Dogecoin': 'DOGE-USD',
        'Tesla': 'TSLA',
        'Nvdia': 'NVDA',
        'Facebook': 'FB',
        'Alphabet': 'GOOG',
        'Twitter': 'TWTR',
        'Apple': 'AAPL'
    }

    df = get_data(days, tickers)

    companies = st.multiselect(
        '銘柄を選択してください。',
        list(df.index),
        ['Bitcoin', 'Ethereum', 'Cardano', 'Dogecoin', 'Tesla']
    )

    if not companies:
        st.error('少なくとも１銘柄を選択してください。')
    else:
        data = df.loc[companies]
        st.write('### 価格（USD）', data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Prices(USD)'}
            )

    chart = (
        alt.Chart(data)
        .mark_line(opacity=0.8, clip=True)
        .encode(
            x='Date:T',
            y=alt.Y('Prices(USD):Q', stack=None, scale=alt.Scale(domain=[0, 3000])),
            color='Name:N'
        )
    )
    st.altair_chart(chart, use_container_width=True)
except:
    st.error('おっと！なにかエラーが起きているようです。')

import streamlit as st
import time
import requests
import yfinance as yf
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# إعدادات الصفحة الخارجية
st.set_page_config(page_title="لوحة مراقبة الذهب الفوري", layout="wide")

# السطر السحري لفرض التنسيق العربي الصحيح (RTL) ومنع تشوه النصوص
st.markdown(
    """
    <style>
    .stApp { direction: RTL; text-align: right; }
    .stMetric { text-align: right; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>⚡ منظومة المراقبة والمضاربة اللحظية للذهب الفوري</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>تحليل متجدد لتدفقات السيولة، الأخبار، وشارت الشموع اليابانية للذهب الفوري (Spot Gold)</p>", unsafe_allow_html=True)

def get_market_data():
    try:
        tickers = {
            "Gold": "XAUUSD=X",       # الذهب الفوري الصافي (Spot Gold)
            "DXY": "DX-Y.NYB",        # مؤشر الدولار
            "US10Y": "^TNX",          # عوائد السندات الأمريكية 10 سنوات
            "NVDA": "NVDA"            # سهم نفيديا (مؤشر الهامش في التكنولوجيا)
        }
        data = {}
        for name, ticker in tickers.items():
            t = yf.Ticker(ticker)
            hist = t.history(period="5d") # استخدام نطاق أوسع لضمان توفر البيانات في الإجازة
            data[name] = hist['Close'].iloc[-1]
            if name == "Gold":
                data["Gold_High"] = hist['High'].iloc[-1]
                data["Gold_Low"] = hist['Low'].iloc[-1]
        return data
    except:
        return None

def get_gold_candles():
    """
    سحب بيانات الشموع اليابانية للذهب الفوري بنطاق يومي مستقر لا يعلق في العطلات
    """
    try:
        t = yf.Ticker("XAUUSD=X")
        df = t.history(period="5d") # جلب آخر 5 أيام تداول بنطاق يومي آمن
        return df
    except:
        return None

def get_crypto_panic_index():
    try:
        url = "https://alternative.me"
        response = requests.get(url).json()
        value = response['data']['value']
        classification = response['data']['value_classification']
        translations = {
            "Extreme Fear": "خوف شديد", "Fear": "خوف",
            "Neutral": "محايد (استقرار الثقة)", "Greed": "جشع (عودة الثقة)",
            "Extreme Greed": "جشع شديد"
        }
        status_ar = translations.get(classification, "محايد")
        return value, status_ar
    except:
        return "50", "محايد"

def get_breaking_news_rss():
    try:
        url = "https://reutersagency.com"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        articles = []
        items = soup.find_all('item')
        for item in items[:5]:
            articles.append(item.title.text)
        return articles
    except:
        return ["تعذر الاتصال بخلاصة الأخبار الفورية حالياً"]

market = get_market_data()
news = get_breaking_news_rss()
panic_val, panic_status = get_crypto_panic_index()
df_candles = get_gold_candles()

if market:
    danger_words = ["margin call", "rate hike", "liquidation", "debt crisis", "fed hawkish", "france"]
    margin_risk_detected = any(any(word in title.lower() for word in danger_words) for title in news)
    
    # حساب المستويات الفنية اليومية للذهب الفوري (Pivot Point)
    pivot = (market['Gold_High'] + market['Gold_Low'] + market['Gold']) / 3
    r1 = (2 * pivot) - market['Gold_Low']
    s1 = (2 * pivot) - market['Gold_High']
    
    # تحديد القرار المضاربي بناءً على إغلاق الجمعة
    if market['DXY'] > 105 and market['Gold'] < 4000:
        if margin_risk_detected:
            decision_text = "❌ إشارة: نداءات هامش نشطة (Margin Calls)! الدولار يلتهم السيولة. انتظر قاع 3,950$ ولا تشتري الآن."
            decision_color = "#FF4B4B"
        else:
            decision_text = "⚠️ إشارة: الذهب تحت الـ 4000$ والدولار مرتفع، ترقب سلوك السعر عند الدعم الحالي."
            decision_color = "#FFA500"
    elif market['DXY'] < 104 and market['Gold'] >= 3950:
        decision_text = f"🟢 إشارة شراء: انحسار موجة الذعر وهبوط الدولار. عودة الثقة للسوق حول مستوى {panic_val} ({panic_status}). فرصة ارتداد صاعد قوية للذهب الفوري."
        decision_color = "#00D26A"
    else:
        decision_text = f"🔵 إشارة: الأسواق مستقرة في نطاق عرضي بإغلاق الأسبوع ومؤشر الخوف عند {panic_val} ({panic_status}) بانتظار افتتاح الغد والقرار الفاصل يوم الأربعاء."
        decision_color = "#0080FF"

    # عرض الأسعار الفورية في كروت منسقة وثابتة
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(label="✨ الذهب الفوري (Spot)", value=f"{market['Gold']:.2f} $")
    col2.metric(label="💵 مؤشر الدولار (DXY)", value=f"{market['DXY']:.2f}")
    col3.metric(label="📈 سندات أمريكا 10Y", value=f"{market['US10Y']:.2f} %")
    col4.metric(label="🤖 سهم نفيديا AI", value=f"{market['NVDA']:.2f} $")
    col5.metric(label="😨 مؤشر ذعر الأسواق", value=f"{panic_val} ({panic_status})")
    
    st.markdown("---")
    st.markdown(f"<div style='background-color:{decision_color}; padding:15px; border-radius:10px; text-align:center; color:white; font-size:20px; font-weight:bold; direction: rtl;'>{decision_text}</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- قسم شارت الشموع اليابانية التفاعلي الآمن والمصحح ---
    if df_candles is not None and not df_candles.empty:
        st.subheader("📊 شارت الشموع اليابانية للذهب الفوري (آخر إغلاقات الأسبوع):")
        
        fig = go.Figure(data=[go.Candlestick(
            x=df_candles.index,
            open=df_candles['Open'],
            high=df_candles['High'],
            low=df_candles['Low'],
            close=df_candles['Close'],
            increasing_line_color='#00D26A',  # الشموع الصاعدة بالأخضر
            decreasing_line_color='#FF4B4B',  # الشموع الهابطة بالأحمر
            name="الذهب الفوري"
        )])
        
        # دمج خطوط الدعم والمقاومة والنقطة المحورية أفقياً
        fig.add_hline(y=r1, line_dash="dash", line_color="#FF4B4B", annotation_text=f"مقاومة R1 ({r1:.2f}$)", annotation_position="top left")
        fig.add_hline(y=pivot, line_dash="dash", line_color="#0080FF", annotation_text=f"المحور Pivot ({pivot:.2f}$)", annotation_position="top left")
        fig.add_hline(y=s1, line_dash="dash", line_color="#00D26A", annotation_text=f"دعم S1 ({s1:.2f}$)", annotation_position="bottom left")
        
        fig.update_layout(
            template="plotly_dark",
            xaxis_rangeslider_visible=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")
    
    st.subheader("📰 آخر العواجل الاقتصادية من رويترز:")
    for title in news:
        st.markdown(f"• {title}")
        
    st.caption(f"آخر تحديث تلقائي آمن للموقع: {time.strftime('%H:%M:%S')}")

time.sleep(30)
st.rerun()

import streamlit as st
import time
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from datetime import datetime

# إعدادات الصفحة الخارجية
st.set_page_config(page_title="منظومة مراقبة الذهب بالذكاء الاصطناعي", layout="wide")

# فرض التنسيق العربي الصحيح (RTL)
st.markdown(
    """
    <style>
    .stApp { direction: RTL; text-align: right; }
    .stMetric { text-align: right; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>🧠 منظومة الذهب المدعومة بالذكاء الاصطناعي اللحظي</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>تحليل سياقي متقدم لعواجل الأسواق وتصريحات القادة بغض النظر عن الكلمات المفتاحية</p>", unsafe_allow_html=True)

def get_market_data():
    try:
        tickers = {"Gold": "GC=F", "DXY": "DX-Y.NYB", "US10Y": "^TNX", "NVDA": "NVDA"}
        data = {}
        for name, ticker in tickers.items():
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            data[name] = hist['Close'].iloc[-1]
            if name == "Gold":
                data["Gold_High"] = hist['High'].iloc[-1]
                data["Gold_Low"] = hist['Low'].iloc[-1]
                data["Gold_Open"] = hist['Open'].iloc[-1]
        return data
    except:
        return None

def get_breaking_news_rss():
    try:
        url = "https://reutersagency.com"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, features="xml")
        articles = []
        for item in soup.find_all('item')[:5]:
            articles.append(item.title.text)
        return articles
    except:
        return ["تعذر الاتصال بخلاصة الأخبار الفورية حالياً"]

def analyze_news_with_ai(news_list):
    """
    إرسال الأخبار وتصريحات القادة لنموذج ذكاء اصطناعي مالي مجاني ومفتوح في سوريا
    لتحليل السياق وفهم الأخطار بدون الاعتماد على كلمات مفتاحية جامدة
    """
    # ندمج الأخبار في نص واحد ليحللها الذكاء معاً للسرعة الاختزالية
    full_text = " | ".join(news_list)
    
    # استخدام نموذج تصنيف مالي مفتوح ومجاني من Hugging Face ولا يحتاج مفاتيح خاصة
    api_url = "https://huggingface.co"
    
    # تعريف فئات الخطر التي نريد من الذكاء الاصطناعي فرز الأخبار بناءً عليها
    candidate_labels = ["financial panic or interest rates", "war or geopolitical conflict", "inflation or economic debt crisis", "normal business news"]
    
    payload = {
        "inputs": full_text,
        "parameters": {"candidate_labels": candidate_labels}
    }
    
    try:
        # إرسال الطلب للخادم السحابي المجاني
        response = requests.post(api_url, json=payload, timeout=5)
        result = response.json()
        
        # جلب الفئة الأعلى احتمالاً الفائزة بتحليل الذكاء الاصطناعي
        top_label = result['labels'][0]
        top_score = result['scores'][0]
        
        # إذا كانت نسبة ثقة الذكاء الاصطناعي أعلى من 40%، نعتمد تصنيفه الذكي
        if top_score > 0.40:
            if top_label == "financial panic or interest rates": return "financial"
            elif top_label == "war or geopolitical conflict": return "geopolitical"
            elif top_label == "inflation or economic debt crisis": return "macro"
            
        return "normal"
    except:
        # في حال حدوث بطء في شبكة الإنترنت بسوريا، يعود الكود تلقائياً للنظام الهجين لحمايتك
        return "normal"

market = get_market_data()
news = get_breaking_news_rss()

if market:
    # تشغيل مستشار الذكاء الاصطناعي اللحظي لقراءة سياق الأخبار والتصريحات المفاجئة
    ai_analysis = analyze_news_with_ai(news)
    
    # قياس التذبذب السعري الحاد المفاجئ كمؤشر أمان ميكانيكي موازي للذكاء
    price_deviation = abs(market['Gold'] - market['Gold_Open'])
    volatile_emergency = price_deviation > 15.0

    # عرض الأسعار الرئيسية
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="✨ الذهب الفوري", value=f"{market['Gold']:.2f} $")
    col2.metric(label="💵 مؤشر الدولار (DXY)", value=f"{market['DXY']:.2f}")
    col3.metric(label="📈 سندات أمريكا 10Y", value=f"{market['US10Y']:.2f} %")
    col4.metric(label="🤖 سهم نفيديا AI", value=f"{market['NVDA']:.2f} $")
    
    st.markdown("---")

    # --- لوحة اتخاذ القرار الشرطية بناءً على تحليل الذكاء الاصطناعي اللحظي ---
    if ai_analysis == "financial" or volatile_emergency:
        st.markdown(
            f"<div style='background-color:#FF4B4B; padding:15px; border-radius:10px; text-align:center; color:white; font-size:20px; font-weight:bold; direction: rtl;'>"
            f"🧠 تحليل الذكاء الاصطناعي: رصد خطر مالي أو تسييل سيولة فوري في الساحة الاقتصادية الآن!<br>"
            f"التكتيك المضاربي: ترقب مستويات الاستسلام البيعي عند القاع الاستراتيجي 3,950$ إلى 3,942$. لا تندفع بالشراء المتسرع."
            f"</div>", unsafe_allow_html=True
        )
    elif ai_analysis == "geopolitical":
        st.markdown(
            f"<div style='background-color:#FF8C00; padding:15px; border-radius:10px; text-align:center; color:white; font-size:20px; font-weight:bold; direction: rtl;'>"
            f"🧠 تحليل الذكاء الاصطناعي: رصد خطر جيوسياسي، تصريحات قادة، أو تصعيد عسكري مفاجئ في العواجل!<br>"
            f"التكتيك المضاربي: الذهب مهيأ لقفزات سعرية سريعة كملاذ آمن. تجنب صفقات البيع تماماً وحافظ على التمركز الشرائي."
            f"</div>", unsafe_allow_html=True
        )
    elif ai_analysis == "macro":
        st.markdown(
            f"<div style='background-color:#FFD700; padding:15px; border-radius:10px; text-align:center; color:black; font-size:20px; font-weight:bold; direction: rtl;'>"
            f"🧠 تحليل الذكاء الاصطناعي: رصد اضطراب اقتصادي كلي (تضخم، تصريحات ديون، أو جمارك مفاجئة)!<br>"
            f"التكتيك المضاربي: تراجع القوة الشرائية يدعم الذهب على المدى المتوسط. راقب الثبات فوق النقطة المحورية لليوم لتأكيد الدخول."
            f"</div>", unsafe_allow_html=True
        )
    else:
        # الوضع الطبيعي العادي الموزع على الفترات الثلاث في حال استقرار الأجواء سياقياً
        pivot = (market['Gold_High'] + market['Gold_Low'] + market['Gold']) / 3
        r1, s1 = (2 * pivot) - market['Gold_Low'], (2 * pivot) - market['Gold_High']
        r2, s2 = pivot + (market['Gold_High'] - market['Gold_Low']), pivot - (market['Gold_High'] - market['Gold_Low'])
        current_hour = datetime.now().hour
        
        tab1, tab2, tab3 = st.tabs(["🕒 التحليل الصباحي (الأوروبي)", "🌤️ منتصف اليوم (الأمريكي)", "🌌 التحليل المسائي (الإغلاق)"])
        
        with tab1:
            st.markdown("### 📋 تقرير الفترة الصباحية (ثابت)")
            st.write(f"**نقطة الارتكاز المحورية لليوم:** {pivot:.2f} $")
            st.write(f"**كمين الشراء الصباحي (S1):** {s1:.2f} $")
            st.write(f"**مستهدف البيع الصباحي (R1):** {r1:.2f} $")

        with tab2:
            st.markdown("### 📋 تقرير فترة منتصف اليوم (سيولة نيويورك والـ AI)")
            st.write(f"**نطاق حماية الجلسة الأمريكية (S2):** {s2:.2f} $")
            st.write(f"**أقصى مستهدف صاعد متوقع (R2):** {r2:.2f} $")

        with tab3:
            st.markdown("### 📋 التقييم المسائي وإغلاق المحافظ")
            if market['Gold'] > 4000:
                st.success("🟢 الذهب مستقر فوق الدعم النفسي 4000$. إشارة أمان نسبي للاحتفاظ بالمراكز.")
            else:
                st.warning("⚠️ الذهب تحت مستويات 4000$. يفضل تسييل جزء من العقود لتجنب فجوات الافتتاح الليلية.")

    st.markdown("---")
    
    st.subheader("📰 خلاصة عواجل رويترز الاقتصادية وتصريحات الأسواق:")
    for title in news:
        st.markdown(f"• {title}")
            
    st.caption(f"آخر تحديث تلقائي مدعوم بالذكاء الاصطناعي للموقع: {time.strftime('%H:%M:%S')}")

time.sleep(30)
st.rerun()

import streamlit as st
from textblob import TextBlob

st.set_page_config(
    page_title="Fake Review Detector",
    page_icon="🔍",
    layout="centered"
)

# Cyber Glassy Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap');

    .stApp {
        background-color: #050510;
        background-image: 
            radial-gradient(ellipse at 20% 50%, rgba(0, 255, 255, 0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(123, 47, 247, 0.08) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(0, 200, 255, 0.04) 0%, transparent 50%);
        background-attachment: fixed;
    }

    /* Grid lines background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }

    /* Header container */
    .cyber-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem;
        margin-bottom: 1rem;
        position: relative;
    }

    /* Glassy card behind header */
    .cyber-header-card {
        background: linear-gradient(135deg, 
            rgba(0, 255, 255, 0.04) 0%, 
            rgba(123, 47, 247, 0.06) 50%,
            rgba(0, 200, 255, 0.04) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 255, 0.15);
        border-radius: 20px;
        padding: 2rem 2rem 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 
            0 0 30px rgba(0, 255, 255, 0.05),
            0 0 60px rgba(123, 47, 247, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        overflow: hidden;
    }

    /* Glowing top border */
    .cyber-header-card::before {
        content: '';
        position: absolute;
        top: 0; left: 10%; right: 10%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00ffff, #7b2ff7, #00ffff, transparent);
    }

    /* Corner accents */
    .cyber-header-card::after {
        content: '';
        position: absolute;
        top: 8px; left: 8px;
        width: 20px; height: 20px;
        border-top: 2px solid rgba(0, 255, 255, 0.6);
        border-left: 2px solid rgba(0, 255, 255, 0.6);
        border-radius: 2px;
    }

    .corner-br {
        position: absolute;
        bottom: 8px; right: 8px;
        width: 20px; height: 20px;
        border-bottom: 2px solid rgba(123, 47, 247, 0.6);
        border-right: 2px solid rgba(123, 47, 247, 0.6);
        border-radius: 2px;
    }

    /* Badge above title */
    .cyber-badge {
        display: inline-block;
        background: rgba(0, 255, 255, 0.08);
        border: 1px solid rgba(0, 255, 255, 0.25);
        border-radius: 20px;
        padding: 4px 16px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 3px;
        color: rgba(0, 255, 255, 0.7);
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    /* Main title */
    .cyber-title {
        font-family: 'Orbitron', monospace;
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00ffff 0%, #a78bfa 50%, #00d2ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 2px;
        line-height: 1.2;
        margin-bottom: 0.4rem;
        text-shadow: none;
        filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.3));
    }

    /* Glowing underline */
    .cyber-underline {
        width: 80px;
        height: 2px;
        background: linear-gradient(90deg, #00ffff, #7b2ff7);
        margin: 0.6rem auto 1rem;
        border-radius: 2px;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }

    /* Subtitle */
    .cyber-subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1rem;
        color: rgba(180, 180, 220, 0.7);
        letter-spacing: 1px;
        line-height: 1.6;
        max-width: 480px;
        margin: 0 auto 1.2rem;
    }

    /* Stats row in header */
    .cyber-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }
    .cyber-stat {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.78rem;
        color: rgba(0, 255, 255, 0.5);
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .cyber-stat span {
        color: rgba(0, 255, 255, 0.8);
        font-weight: 600;
    }

    /* Result cards */
    .verdict-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    .trustworthy {
        background: linear-gradient(135deg, rgba(15,61,31,0.8), rgba(26,107,53,0.8));
        border: 1px solid #2ecc71;
        color: #2ecc71;
        box-shadow: 0 0 20px rgba(46, 204, 113, 0.15);
    }
    .biased {
        background: linear-gradient(135deg, rgba(61,46,15,0.8), rgba(107,82,26,0.8));
        border: 1px solid #f39c12;
        color: #f39c12;
        box-shadow: 0 0 20px rgba(243, 156, 18, 0.15);
    }
    .fake {
        background: linear-gradient(135deg, rgba(61,15,15,0.8), rgba(107,26,26,0.8));
        border: 1px solid #e74c3c;
        color: #e74c3c;
        box-shadow: 0 0 20px rgba(231, 76, 60, 0.15);
    }

    /* Metric boxes */
    .metric-box {
        background: linear-gradient(135deg, rgba(0,255,255,0.04), rgba(123,47,247,0.06));
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        border: 1px solid rgba(0, 255, 255, 0.12);
        backdrop-filter: blur(10px);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.03);
    }
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #00d2ff;
    }
    .metric-label {
        font-size: 0.75rem;
        color: rgba(150, 150, 200, 0.7);
        margin-top: 4px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* Phrase tags */
    .phrase-tag {
        display: inline-block;
        background: rgba(0, 255, 255, 0.06);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 20px;
        padding: 5px 14px;
        margin: 4px;
        color: #00d2ff;
        font-size: 0.85rem;
        backdrop-filter: blur(5px);
    }

    /* Text area */
    .stTextArea textarea {
        background-color: rgba(10, 10, 30, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: rgba(200, 200, 255, 0.9) !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* Button */
    .stButton button {
        background: linear-gradient(90deg, #00d2ff, #7b2ff7) !important;
        border: none !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Divider */
    hr {
        border-color: rgba(0, 255, 255, 0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cyber Theme Header
st.markdown("""
    <div class="cyber-header-card">
        <div class="corner-br"></div>
        <div class="cyber-badge">🛡️ AI Powered Analysis</div>
        <div class="cyber-title">FAKE REVIEW<br>DETECTOR</div>
        <div class="cyber-underline"></div>
        <div class="cyber-subtitle">
            Paste any product review from Amazon, Flipkart or Google
            and our AI will analyze its trustworthiness instantly.
        </div>
        <div class="cyber-stats">
            <div class="cyber-stat">⚡ <span>NLP</span> Powered</div>
            <div class="cyber-stat">🎯 <span>Real-time</span> Analysis</div>
            <div class="cyber-stat">🔒 <span>100%</span> Private</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Input
review = st.text_area("", placeholder="Paste your Amazon, Flipkart or Google review here...", height=200)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analyze_btn = st.button("🔍 Analyze Review", use_container_width=True)

if analyze_btn:
    if review:
        blob = TextBlob(review)

        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        noun_phrases = blob.noun_phrases
        word_count = len(review.split())

        product_keywords = ["battery", "screen", "camera", "quality", "delivery",
                           "packaging", "size", "weight", "price", "material",
                           "display", "sound", "performance", "build", "design",
                           "charging", "speed", "memory", "storage", "colour"]

        review_lower = review.lower()
        feature_mentions = sum(1 for keyword in product_keywords if keyword in review_lower)

        subjectivity_penalty = subjectivity * 50
        feature_bonus = feature_mentions * 15
        word_count_bonus = min(word_count * 0.3, 15)
        trust_score = int(40 - subjectivity_penalty + feature_bonus + word_count_bonus)
        trust_score = max(0, min(100, trust_score))

        st.markdown("---")

        if trust_score >= 60:
            st.markdown(f'<div class="verdict-card trustworthy">✅ Trustworthy Review — {trust_score}/100</div>', unsafe_allow_html=True)
        elif trust_score >= 35:
            st.markdown(f'<div class="verdict-card biased">⚠️ Slightly Biased Review — {trust_score}/100</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="verdict-card fake">❌ Potential Fake Review — {trust_score}/100</div>', unsafe_allow_html=True)

        st.markdown("### 📊 Trust Meter")
        st.progress(trust_score / 100)

        st.markdown("---")

        st.markdown("### 🔎 Detailed Breakdown")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{word_count}</div><div class="metric-label">Word Count</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{round(polarity, 2)}</div><div class="metric-label">Polarity</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{round(subjectivity, 2)}</div><div class="metric-label">Subjectivity</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-box"><div class="metric-value">{feature_mentions}</div><div class="metric-label">Features Found</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("### 📌 Key Phrases Detected")
        if noun_phrases:
            tags_html = "".join([f'<span class="phrase-tag">• {phrase}</span>' for phrase in noun_phrases])
            st.markdown(tags_html, unsafe_allow_html=True)
        else:
            st.markdown('<p style="color:rgba(0,255,255,0.4)">No specific phrases found — suspicious!</p>', unsafe_allow_html=True)

    else:
        st.warning("⚠️ Please paste a review first!")
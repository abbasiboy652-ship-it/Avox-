import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage

# ऐप का नाम और लुक
st.set_page_config(page_title="Avox", page_icon="🔊")
st.title("🔊 Avox")
st.caption("Tera Personal AI Bhai")

# सर्च टूल (रियल टाइम वेब सर्च + सोर्स)
search_tool = DuckDuckGoSearchRun()

# चैट हिस्ट्री स्टोर करने के लिए
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी चैट दिखाओ
for msg in st.session_state.messages:
    if msg.type == "human":
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

# साइडबार - हिस्ट्री, न्यू चैट, प्रोजेक्ट्स (बाद में पूरा कर लेंगे)
with st.sidebar:
    st.header("📂 Menu")
    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.write("📌 Projects (Jald hi aayega)")
    st.write("🕒 History (Jald hi aayega)")

# नीचे चैट इनपुट
if prompt := st.chat_input("Bolo bhai, kya haal hai?"):
    # यूजर का मैसेज दिखाओ और स्टोर करो
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # थोड़ा सोचने का लोडर
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hu..."):
            
            # अगर सवाल में मौसम, न्यूज़, फैक्ट जैसा लगे तो सर्च करो
            lower_prompt = prompt.lower()
            if any(word in lower_prompt for word in ["temperature", "mausam", "taapmaan", "news", "kitna", "kaise", "kya hai", "batao", "today", "abhi"]):
                # वेब सर्च करो
                result = search_tool.run(prompt)
                response = f"{result}\n\n🔗 Source: DuckDuckGo Search se"
            else:
                # नॉर्मल फ्रेंडली जवाब (यहाँ सिंपल रूल बेस्ड, बाद में बड़ा AI ऐड कर लेंगे)
                if "joke" in lower_prompt or "has" in lower_prompt:
                    response = "Ek joke sun: Wifi ka password kya hai? \n'12345678' \nKyunki lazy log hi hack karte hain! 😂😂"
                elif "kaise ho" in lower_prompt or "haal" in lower_prompt:
                    response = "Badhiya bhai! Tu bata, kya chal raha hai? 😎"
                elif "thanks" in lower_prompt or "shukriya" in lower_prompt:
                    response = "Koi baat nahi bhai, anytime! ❤️"
                else:
                    response = "Bhai ye toh thoda tough sawal hai... abhi main seekh raha hu! Thodi der mein aur smart ban jaunga 😅\nTu kuch aur puch na!"

        # AI का जवाब दिखाओ और स्टोर करो
        st.write(response)
        st.session_state.messages.append(AIMessage(content=response))

import streamlit as st
import pandas as pd
import os
import urllib.parse

st.set_page_config(page_title="FarmMarket", page_icon="🌾", layout="wide")
# --- BIG ATTRACTIVE APP NAME ---
st.markdown("""
<style>
    /* Make the whole app background light */
    .stApp {
        background-color: #F8FFF8;
    }
    /* Big FarmMarket Logo */
    .big-logo {
        font-size: 68px !important;
        font-weight: 900;
        text-align: center;
        color: #1A7F37;
        line-height: 1.0;
        margin-top: -10px;
        margin-bottom: 0px;
        letter-spacing: -1px;
        text-shadow: 2px 2px 0px #D9F99D;
    }
    .big-logo span {
        color: #F59E0B;
    }
    /* Slogan under logo */
    .slogan {
        font-size: 20px !important;
        font-weight: 600;
        text-align: center;
        color: #444444;
        margin-top: 5px;
        margin-bottom: 20px;
    }
    /* Make all buttons green and bigger */
    .stButton > button {
        background-color: #1A7F37 !important;
        color: white !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 8px 20px !important;
        border: none !important;
    }
    /* Make all headers bigger */
    h2 {
        font-size: 32px !important;
        color: #1A7F37 !important;
    }
    h3 {
        font-size: 24px !important;
    }
</style>
<div class="big-logo">🌾 Farm<span>Market</span></div>
<div class="slogan">Buy Farm Inputs • Sell Your Produce • No Middleman</div>
""", unsafe_allow_html=True)
# --- SAVE FILE FOR PRODUCE ---
FILE = "produce.csv"
if not os.path.exists(FILE):
    pd.DataFrame(columns=["Name","Crop","Qty","Price","Location","Phone"]).to_csv(FILE, index=False)

# --- CART ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- SHOP WHATSAPP NUMBER - CHANGE TO YOURS ---
SHOP_WHATSAPP = "2348133685928"  # Your number without + , e.g. 234803...

menu = st.sidebar.selectbox("Menu", ["🏠 Home", "🛒 Buy Farm Inputs", "🌽 Sell Farm Produce", "🧺 My Cart"])

# --- PRODUCTS WITH REAL PICTURES ---
inputs = [
    {"name": "Maize Seeds - 5kg", "price": 25000, "seller": "Agro Shop Lagos", "img": "https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=500"},
    {"name": "NPK Fertilizer - 50kg", "price": 55000, "seller": "Agro Shop Lagos", "img": "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=500"},
    {"name": "Herbicide - 1 Litre", "price": 12000, "seller": "Agro Shop Ibadan", "img": "https://images.unsplash.com/photo-1589923188900-85dae523342b?w=500"},
    {"name": "Tomato Seeds - 100g", "price": 8000, "seller": "Agro Shop Abeokuta", "img": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=500"},
    {"name": "Cutlass / Hoe Set", "price": 15000, "seller": "Agro Shop Abeokuta", "img": "https://images.unsplash.com/photo-1615729947596-a598e5de0ab3?w=500"},
    {"name": "Poultry Feed - 25kg", "price": 22000, "seller": "Agro Shop Epe", "img": "https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=500"},
]

if menu == "🏠 Home":
    st.write("Welcome! Buy farm inputs cheap, and sell your harvest direct to buyers. No middleman.")
    st.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1000", caption="Fresh from Nigerian Farms")
    st.subheader("🔥 Latest Produce For Sale")
    df = pd.read_csv(FILE)
    if len(df) == 0:
        st.info("No produce posted yet. Be the first to post!")
    else:
        for i, row in df.tail(3).iterrows():
            st.write(f"**{row['Crop']}** - {row['Qty']} | ₦{row['Price']:,} | {row['Location']} | Seller: {row['Name']}")
            wa_link = f"https://wa.me/{row['Phone']}?text=" + urllib.parse.quote(f"Hello {row['Name']}, I want to buy your {row['Crop']}")
            st.markdown(f"[💬 Chat Seller on WhatsApp]({wa_link})")
            st.divider()

elif menu == "🛒 Buy Farm Inputs":
    st.header("Buy Farm Inputs")
    search = st.text_input("Search inputs e.g. fertilizer, seeds")
    for item in inputs:
        if search.lower() not in item["name"].lower() and search != "":
            continue
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(item["img"], width=200)
        with col2:
            st.subheader(item["name"])
            st.write(f"₦{item['price']:,} | Seller: {item['seller']}")
            if st.button("Add to Cart 🛒", key=item["name"]):
                st.session_state.cart.append(item)
                st.success(f"Added {item['name']}")
        st.divider()

elif menu == "🌽 Sell Farm Produce":
    st.header("Sell Your Produce - Post Free")
    with st.form("sell_form"):
        name = st.text_input("Your Name")
        crop = st.selectbox("Crop", ["Yam", "Cassava", "Maize", "Tomatoes", "Pepper", "Rice", "Plantain", "Eggs", "Fish", "Chicken"])
        qty = st.text_input("Quantity e.g. 10 bags, 50kg")
        price = st.number_input("Price per bag/kg (₦)", min_value=100)
        location = st.text_input("Your Location e.g. Epe, Lagos")
        phone = st.text_input("WhatsApp Number e.g. 2348031234567 (start with 234)")
        submitted = st.form_submit_button("Post My Produce")
        if submitted:
            if name and phone and qty:
                new = pd.DataFrame([[name, crop, qty, price, location, phone]], columns=["Name","Crop","Qty","Price","Location","Phone"])
                new.to_csv(FILE, mode="a", header=False, index=False)
                st.success(f"Done! Your {crop} is now live in the market!")
            else:
                st.error("Please fill Name, Quantity and Phone")

    st.subheader("All Produce In Market")
    df = pd.read_csv(FILE)
    for i, row in df.iterrows():
        st.write(f"**{row['Crop']}** - {row['Qty']} | ₦{row['Price']:,} | {row['Location']} | {row['Name']}")
        wa_link = f"https://wa.me/{row['Phone']}?text=" + urllib.parse.quote(f"Hello {row['Name']}, I want to buy your {row['Crop']} - {row['Qty']} for ₦{row['Price']}")
        st.markdown(f"[💬 Chat Seller on WhatsApp]({wa_link})")
        st.divider()

elif menu == "🧺 My Cart":
    st.header("My Cart")
    if len(st.session_state.cart) == 0:
        st.info("Your cart is empty. Go to Buy Farm Inputs to add.")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"{item['name']} - ₦{item['price']:,}")
            total += item["price"]
        st.subheader(f"Total: ₦{total:,}")
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()
        # WhatsApp Checkout
        msg = "Hello, I want to order:\n"
        for item in st.session_state.cart:
            msg += f"- {item['name']} - ₦{item['price']}\n"
        msg += f"Total: ₦{total}"
        wa_link = f"https://wa.me/{SHOP_WHATSAPP}?text=" + urllib.parse.quote(msg)
        st.markdown(f"[✅ Checkout on WhatsApp]({wa_link})")
        st.write("Clicking will open WhatsApp with your order ready to send.")
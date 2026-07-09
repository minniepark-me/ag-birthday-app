import streamlit as st
import random
import time
import base64
import os
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(
    page_title="Happy Belated Birthday, Ag!", 
    page_icon="💝", 
    layout="centered"
)

# 2. Custom CSS for Maroon Background, Gold Text, and Glass Boxes
st.markdown("""
    <style>
    /* COMBINED BACKGROUND: Emojis on top, Maroon Gradient on bottom */
    [data-testid="stAppViewContainer"] {
        background-color: #4A0E2E !important;
        background-image: 
            url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Ctext x='10' y='30' font-size='15' opacity='0.15'%3E🎁%3C/text%3E%3Ctext x='70' y='80' font-size='20' opacity='0.15'%3E🎂%3C/text%3E%3Ctext x='40' y='110' font-size='15' opacity='0.15'%3E🎉%3C/text%3E%3Ctext x='90' y='20' font-size='18' opacity='0.15'%3E✨%3C/text%3E%3C/svg%3E"), 
            linear-gradient(135deg, #4A0E2E 0%, #2A081A 100%) !important;
        background-size: 120px 120px, 100% 100% !important;
        animation: floatEmojis 20s linear infinite !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    @keyframes floatEmojis {
        0% { background-position: 0px 0px, 0 0; }
        100% { background-position: 120px 120px, 0 0; }
    }

    /* FORCE ALL TEXT to a soft Cream/Gold — anchored to the stable .stApp class
       (present across virtually all Streamlit versions) instead of data-testid
       attributes, which get renamed between releases. */
    .stApp,
    .stApp * {
        color: #f5f5dc !important;
        font-family: 'Trebuchet MS', sans-serif !important;
    }

    /* Headers specific Gold — placed AFTER the blanket rule so it wins */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp h1 *, .stApp h2 *, .stApp h3 *, .stApp h4 *, .stApp h5 *, .stApp h6 * {
        text-align: center;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.8); 
        color: #d4af37 !important; /* Rich Gold */
    }

    /* Buttons keep bright white bold text, also after the blanket rule */
    .stApp button,
    .stApp button p,
    .stApp button span,
    .stApp button div {
        color: #ffffff !important;
        font-weight: bold;
    }

    /* Dividers styled to match the gold glass theme */
    .stApp hr {
        border-color: rgba(212, 175, 55, 0.5) !important;
    }

    /* The Boxes: Dark Frosted Glass with GOLD BORDERS THAT POP.
       Covers old class-based containers, new data-testid wrappers, and expanders. */
    .stApp [data-testid="stVerticalBlockBorderWrapper"],
    .stApp div[data-testid^="stVerticalBlock"][class*="border"],
    .stApp [data-testid="stContainer"],
    .stApp [data-testid="stExpander"],
    .stApp div[class*="border"][class*="stVerticalBlock"] {
        background: linear-gradient(145deg, rgba(255,255,255,0.16), rgba(255,255,255,0.04)) !important; /* Much stronger frosted glass — clearly visible against dark maroon */
        backdrop-filter: blur(16px) saturate(180%) !important; 
        -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
        border: 3px solid #ffdb70 !important; /* Brighter gold border */
        border-radius: 18px !important;
        box-shadow: 
            0 0 30px 10px rgba(212, 175, 55, 0.65),
            inset 0 0 40px rgba(255, 255, 255, 0.1) !important; /* Strong glowing shadow + inner glass glow */
        padding: 14px !important;
        transition: box-shadow 0.3s ease-in-out;
    }

    .stApp [data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 
            0 0 28px 8px rgba(212, 175, 55, 0.6),
            inset 0 0 30px rgba(212, 175, 55, 0.12) !important;
    }

    /* Glass vibe for info/warning/error boxes too */
    .stApp [data-testid="stAlert"],
    .stApp [data-testid="stAlertContentInfo"],
    .stApp [data-testid="stAlertContentError"] {
        background: rgba(40, 5, 5, 0.55) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 14px !important;
        box-shadow: 0 0 15px 4px rgba(212, 175, 55, 0.35) !important;
    }

    /* Buttons get a subtle glass/gold touch on their border too */
    .stApp button {
        border: 2px solid rgba(212, 175, 55, 0.6) !important;
        box-shadow: 0 0 10px 2px rgba(212, 175, 55, 0.25) !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. State Management Setup
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False
if "current_message" not in st.session_state:
    st.session_state.current_message = "Click a button below to unpack a special birthday surprise!"
    st.session_state.current_category = "🎁 Welcome"
if "snack_rain_key" not in st.session_state:
    st.session_state.snack_rain_key = 0

# ==========================================
# THE SECURITY GATE (BOUNCER)
# ==========================================
if not st.session_state.access_granted:
    st.title("🛑 Security Checkpoint")
    st.markdown("<p style='color: #ffcc80 !important; font-size: 1.05rem !important;'>Before you can enter this peaceful space, I need to verify your identity.</p>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #ff8a65 !important;'>Question: Are you a clingy person, someone who loves loud places, or someone trying to call me on the phone?</h3>", unsafe_allow_html=True)
    
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Yes, that sounds like me", use_container_width=True):
            st.error("🚨 ACCESS DENIED. Go away. This is a peaceful zone only.")
    with col_no:
        if st.button("No, I hate all of those things.", type="primary", use_container_width=True):
            st.session_state.access_granted = True
            st.rerun()
            
    # Stop the app from loading the rest of the page until they pass!
    st.stop()


# ==========================================
# MAIN APP (Only visible if access is granted)
# ==========================================

# HIDDEN BACKGROUND MUSIC SCRIPT — skipped whenever Campfire Mode is on,
# so it never overlaps with the campfire audio
if not st.session_state.get("campfire_mode_toggle", False):
    try:
        with open("song.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay loop hidden>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
    except Exception:
        pass # Will gracefully skip if song.mp3 is not added yet

# 4. The Memory & Compliment Database
AMAZING_TRAITS = [
    "One of my favorite things about you is your incredibly kind heart and love for your own space.",
    "You have this amazing ability to make me feel better no matter what is going on.",
    "You are brilliant, beautiful, adventurous, and absolutely unstoppable!"
]

LONG_DISTANCE_LOVE = [
    "We might be continents apart, but you are always close to my heart.",
    "I love that we can go without talking for a bit, and then pick right back up like no time has passed.",
    "India and Africa are far apart, but our friendship easily bridges the gap."
]

FUTURE_WISHES = [
    "I can't wait for the day we finally get to go camping and celebrate together in person!",
    "Wishing you a year filled with as much joy, peace, and snacks as you bring to my life.",
    "No matter what happens this year, I will always be in your corner cheering you on."
]

all_messages = {
    "✨ Why You're Amazing": AMAZING_TRAITS,
    "🌍 Long-Distance Bond": LONG_DISTANCE_LOVE,
    "🚀 Wishes for You": FUTURE_WISHES
}

# 5. The Website Header
st.title("🎂 Happy Belated Birthday, Silver (My favorite Ag)! 🎈")

# Center the picture — circular portrait framed in a glowing gold ring
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
photo_path = None
for fname in ["ag_picture.jpg", "ag_picture.jpeg", "ag_picture.png", "ag_picture.JPG", "ag_picture.PNG"]:
    candidate = os.path.join(BASE_DIR, fname)
    if os.path.exists(candidate):
        photo_path = candidate
        break

if photo_path:
    with open(photo_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    mime = "image/png" if photo_path.lower().endswith(".png") else "image/jpeg"
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin: 25px 0;">
            <img src="data:{mime};base64,{img_b64}" style="
                width: clamp(160px, 60vw, 280px);
                height: clamp(160px, 60vw, 280px);
                object-fit: cover;
                border-radius: 50%;
                border: 5px solid #ffdb70;
                box-shadow: 0 0 25px 8px rgba(212,175,55,0.55), 0 0 55px rgba(212,175,55,0.3);
            ">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("📸 Add 'ag_picture.jpg' to your folder to see her picture here!")
    # Debug helper: show what's actually in the folder so we can see what's really there
    try:
        files_here = os.listdir(BASE_DIR)
        image_like = [f for f in files_here if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        st.caption(f"Looking in: {BASE_DIR}")
        if image_like:
            st.caption(f"Image files found here: {', '.join(image_like)} — none named exactly 'ag_picture.jpg'")
        else:
            st.caption("No .jpg/.jpeg/.png files found in this folder at all.")
    except Exception:
        pass

intro_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; padding: 0; font-family: 'Trebuchet MS', sans-serif; background: transparent; }
  p { color: #ffccbc; font-size: 1.3rem; text-align: center; line-height: 1.5; margin: 0; }

  @media (max-width: 480px) {
    p { font-size: 1rem; }
  }
</style>
</head>
<body>
  <p>I might have been down with a fever on your actual birthday, but our friendship deserves to be celebrated every single day. Identity Verified. Welcome to your peaceful space, Ag.</p>
  <script>
    function reportHeight() {
      const height = document.body.scrollHeight;
      window.parent.postMessage({type: "streamlit:setFrameHeight", height: height}, "*");
    }
    window.addEventListener("load", reportHeight);
    new ResizeObserver(reportHeight).observe(document.body);
    setTimeout(reportHeight, 100);
  </script>
</body>
</html>
"""
components.html(intro_html, height=80, scrolling=False)

# THE SILVER SURVIVAL GUIDE (Likes & Dislikes) — rendered as a real embedded HTML
# component instead of st.markdown, since that's the only method proven to
# actually respect custom colors on this setup (see color_test.html)
st.write("### The 'Silver' Survival Guide 📖")

survival_guide_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; padding: 0; font-family: 'Trebuchet MS', sans-serif; background: transparent; }
  .row { display: flex; gap: 16px; }
  .col { flex: 1; min-width: 0; }
  .box {
      background: linear-gradient(145deg, rgba(255,255,255,0.16), rgba(255,255,255,0.04));
      border: 3px solid #ffdb70;
      border-radius: 18px;
      box-shadow: 0 0 30px 10px rgba(212,175,55,0.5), inset 0 0 40px rgba(255,255,255,0.08);
      padding: 16px 20px;
      box-sizing: border-box;
  }
  .label-love { color: #ff2d78; font-weight: bold; font-size: 1.15rem; margin: 0 0 10px 0; }
  .label-not { color: #40c4ff; font-weight: bold; font-size: 1.15rem; margin: 0 0 10px 0; }
  .item-love { color: #ffe0ec; font-size: 1.05rem; margin: 8px 0; }
  .item-not { color: #d4f1ff; font-size: 1.05rem; margin: 8px 0; }

  /* Mobile: stack the two boxes instead of squeezing them side-by-side */
  @media (max-width: 480px) {
    .row { flex-direction: column; }
    .box { padding: 12px 16px; }
    .label-love, .label-not { font-size: 1.05rem; margin-bottom: 6px; }
    .item-love, .item-not { font-size: 0.95rem; margin: 5px 0; }
  }
</style>
</head>
<body>
  <div class="row">
    <div class="col">
      <div class="box">
        <p class="label-love">💖 LOVES:</p>
        <p class="item-love">🍷 Maroon Color</p>
        <p class="item-love">🐺 Husky Men &amp; Dogs</p>
        <p class="item-love">👯‍♀️ Her close friends</p>
        <p class="item-love">🍕 Snacks &amp; Adventures</p>
        <p class="item-love">🏕️ Camping &amp; Her Space</p>
      </div>
    </div>
    <div class="col">
      <div class="box">
        <p class="label-not">🚫 ABSOLUTELY NOT:</p>
        <p class="item-not">📞 Phone Calls</p>
        <p class="item-not">📢 Loud places &amp; people</p>
        <p class="item-not">🥶 Cold Weather</p>
        <p class="item-not">🛑 Disturbance</p>
        <p class="item-not">🙅‍♀️ Clingy People</p>
      </div>
    </div>
  </div>
  <script>
    function reportHeight() {
      const height = document.body.scrollHeight;
      window.parent.postMessage({type: "streamlit:setFrameHeight", height: height}, "*");
    }
    window.addEventListener("load", reportHeight);
    new ResizeObserver(reportHeight).observe(document.body);
    setTimeout(reportHeight, 100);
  </script>
</body>
</html>
"""

components.html(survival_guide_html, height=280, scrolling=False)

st.divider()

# 6. The Dual Action Buttons
col_smile, col_snack = st.columns(2)

with col_smile:
    if st.button("💝 Generate a Smile for Ag 💝", type="primary", use_container_width=True):
        st.balloons()
        category = random.choice(list(all_messages.keys()))
        message = random.choice(all_messages[category])
        st.session_state.current_message = message
        st.session_state.current_category = category

with col_snack:
    if st.button("🥨 Deploy Emergency Snacks 🥨", type="secondary", use_container_width=True):
        snack = random.choice(["🥨 A giant warm pretzel!", "🍕 Extra cheesy pizza!", "🍟 Crispy hot fries!", "🍫 A massive chocolate bar!", "🍿 Sweet & salty popcorn!"])
        st.session_state.current_message = f"Dropping in {snack} Enjoy your peaceful snack time."
        st.session_state.current_category = "🤤 Snack Emergency Resolved"
        
        # Change the key every time she clicks, forcing the browser to replay the animation!
        st.session_state.snack_rain_key = random.randint(1, 100000)

# Only show the snack animation if the snack button was just pressed
if "Snack Emergency" in st.session_state.current_category:
    # We use the unique key in the class name to force it to run every single time
    key = st.session_state.snack_rain_key
    st.markdown(f"""
    <style>
    .snack-emoji-{key} {{
        position: fixed;
        top: -10%;
        z-index: 999999;
        font-size: 4rem;
        animation: snackFall-{key} 3s linear forwards;
    }}
    @keyframes snackFall-{key} {{
        0% {{ transform: translateY(0) rotate(0deg); opacity: 1; }}
        100% {{ transform: translateY(110vh) rotate(360deg); opacity: 0; }}
    }}
    .snack-emoji-{key}:nth-child(1) {{ left: 10%; animation-duration: 2.5s; }}
    .snack-emoji-{key}:nth-child(2) {{ left: 30%; animation-duration: 3.2s; animation-delay: 0.2s; }}
    .snack-emoji-{key}:nth-child(3) {{ left: 50%; animation-duration: 2.8s; animation-delay: 0.1s; }}
    .snack-emoji-{key}:nth-child(4) {{ left: 70%; animation-duration: 3.5s; animation-delay: 0.3s; }}
    .snack-emoji-{key}:nth-child(5) {{ left: 90%; animation-duration: 2.7s; }}
    </style>
    <div class="snack-emoji-{key}">🍕</div>
    <div class="snack-emoji-{key}">🍟</div>
    <div class="snack-emoji-{key}">🥨</div>
    <div class="snack-emoji-{key}">🍫</div>
    <div class="snack-emoji-{key}">🍿</div>
    """, unsafe_allow_html=True)


# 7. Showing the Message
st.markdown(f"<h3 style='color: #f4c95d !important;'>Current Vibe: {st.session_state.current_category}</h3>", unsafe_allow_html=True)

vibe_box_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{ margin: 0; padding: 0; font-family: 'Trebuchet MS', sans-serif; background: transparent; }}
  .box {{
      background: linear-gradient(145deg, rgba(255,255,255,0.16), rgba(255,255,255,0.04));
      border: 3px solid #ffdb70;
      border-radius: 18px;
      box-shadow: 0 0 30px 10px rgba(212,175,55,0.5), inset 0 0 40px rgba(255,255,255,0.08);
      padding: 20px;
      box-sizing: border-box;
  }}
  p {{
      color: #ffd54f;
      font-style: italic;
      text-align: center;
      font-size: 1.4rem;
      margin: 0;
      line-height: 1.5;
  }}

  /* Mobile: slightly smaller text and tighter padding so long messages fit */
  @media (max-width: 480px) {{
    .box {{ padding: 14px; }}
    p {{ font-size: 1.1rem; }}
  }}
</style>
</head>
<body>
  <div class="box">
    <p>"{st.session_state.current_message}"</p>
  </div>
  <script>
    function reportHeight() {
      const height = document.body.scrollHeight;
      window.parent.postMessage({type: "streamlit:setFrameHeight", height: height}, "*");
    }
    window.addEventListener("load", reportHeight);
    new ResizeObserver(reportHeight).observe(document.body);
    setTimeout(reportHeight, 100);
  </script>
</body>
</html>
"""
components.html(vibe_box_html, height=120, scrolling=False)

st.divider()

# 8. Campfire Mode
campfire_mode = st.toggle("🏕️ Enable Campfire Mode (Cozy Peace)", key="campfire_mode_toggle")
if campfire_mode:
    try:
        with open("campfire.mp3", "rb") as f:
            campfire_data = f.read()
            campfire_b64 = base64.b64encode(campfire_data).decode()
            st.markdown(
                f"""
                <audio autoplay loop hidden>
                <source src="data:audio/mp3;base64,{campfire_b64}" type="audio/mp3">
                </audio>
                """,
                unsafe_allow_html=True
            )
    except Exception:
        st.caption("(Add 'campfire.mp3' to your folder to hear the fire!)")
    
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://media.giphy.com/media/ynx1sj5Wz2atO/giphy.gif" width="300" style="border-radius: 15px; border: 2px solid #d4af37; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);">
        </div>
        <br>
        <p style="text-align: center !important; color: #81d4fa !important;"><i>Stay warm, bestie.</i></p>
        """, 
        unsafe_allow_html=True
    )

st.divider()

# 9. Custom Footer
footer_html = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { margin: 0; padding: 0; font-family: 'Trebuchet MS', sans-serif; background: transparent; }
  p { color: #ce93d8; font-size: 1.15rem; font-style: italic; text-align: center; margin: 0; }

  @media (max-width: 480px) {
    p { font-size: 0.9rem; }
  }
</style>
</head>
<body>
  <p>Made with 💖 by your Meghyung (aka Megha Prasad) for my dear Silver Ag ✨</p>
  <script>
    function reportHeight() {
      const height = document.body.scrollHeight;
      window.parent.postMessage({type: "streamlit:setFrameHeight", height: height}, "*");
    }
    window.addEventListener("load", reportHeight);
    new ResizeObserver(reportHeight).observe(document.body);
    setTimeout(reportHeight, 100);
  </script>
</body>
</html>
"""
components.html(footer_html, height=50, scrolling=False)

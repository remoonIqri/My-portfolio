# ==========================================
# IMPORTS
# ==========================================
import streamlit as st
import re
from supabase import create_client, Client

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(
    page_title="Iqratun Nesa Remoon | Portfolio",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# SUPABASE CONNECTION
# ==========================================
@st.cache_resource
def init_supabase() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        return None

supabase = init_supabase()

# ==========================================
# DEFAULT CONFIGURATION
# ==========================================
DEFAULT_PROFILE = {
    "name": "Iqratun Nesa Remoon",
    "title": "IT Networking & Infrastructure Enthusiast",
    "bio": "I am Iqratun Nesa Remoon from Chattogram, Bangladesh. I am currently learning Cybersecurity and building my knowledge in IT networking and infrastructure. I have been working with networking concepts such as IP addressing and subnetting, routing, VLANs, router configuration, SSH, port security and access control. I use Cisco Packet Tracer to practice network configuration and topology design, and I am continuously exploring IT infrastructure and cybersecurity concepts.",
    "location": "Chattogram, Bangladesh",
    "email": "remooniqra@gmail.com",
    "profile_image": "https://raw.githubusercontent.com/oksajid1411-coder/Iqra-portfolio/300d7d25ad394851b2fa33f8459b65ea997c82d5/1000243092.jpg",
    "experience_years": "Beginner Level",
    "current_focus": "Cybersecurity, IT Networking & Infrastructure"
}

# ==========================================
# DATABASE FUNCTIONS
# ==========================================
def fetch_data(table_name, order_col="display_order"):
    if not supabase:
        return []
    try:
        res = supabase.table(table_name).select("*").order(order_col, desc=False).execute()
        return res.data
    except Exception as e:
        st.error(f"Error fetching from {table_name}: {e}")
        return []

def get_profile():
    if not supabase:
        return DEFAULT_PROFILE
    try:
        res = supabase.table("profiles").select("*").limit(1).execute()
        if res.data:
            return res.data[0]
        return DEFAULT_PROFILE
    except Exception:
        return DEFAULT_PROFILE

def update_profile(data):
    if not supabase:
        return False
    try:
        prof = get_profile()
        if "id" in prof:
            supabase.table("profiles").update(data).eq("id", prof["id"]).execute()
        else:
            supabase.table("profiles").insert(data).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error updating profile: {e}")
        return False

# ==========================================
# STYLING
# ==========================================
css_style = """
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
        font-weight: 600;
    }
    .accent-text {
        color: #38bdf8;
    }
    .card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s, border-color 0.2s;
    }
    .card:hover {
        border-color: #38bdf8;
    }
    .badge {
        background-color: #0284c7;
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .badge-secondary {
        background-color: #334155;
        color: #cbd5e1;
    }
    .profile-img-container {
        border-radius: 50%;
        border: 3px solid #38bdf8;
        padding: 5px;
        width: 200px;
        height: 200px;
        overflow: hidden;
        margin: 0 auto;
    }
    .profile-img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
    }
    .timeline-item {
        border-left: 2px solid #38bdf8;
        padding-left: 20px;
        margin-left: 10px;
        margin-bottom: 25px;
        position: relative;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
"""

st.markdown(css_style, unsafe_allow_html=True)

# ==========================================
# NAVIGATION & HEADER
# ==========================================
profile_data = get_profile()

st.sidebar.title(profile_data.get("name", "Portfolio"))
st.sidebar.caption(profile_data.get("title", ""))

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "About", "Skills", "Projects", "Areas of Interest", "Experience", "Learning Journey", "Contact", "Admin Panel"]
)

# ==========================================
# HOME PAGE
# ==========================================
if menu == "Home":
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        img_url = profile_data.get("profile_image")
        if img_url:
            name_val = profile_data.get("name")
            html_img = f'<div class="profile-img-container"><img src="{img_url}" alt="{name_val}"></div>'
            st.markdown(html_img, unsafe_allow_html=True)
            
    with col2:
        st.title(profile_data.get("name"))
        st.subheader(f":blue[{profile_data.get('title')}]")
        st.markdown(f"**Focus:** {profile_data.get('current_focus')}")
        st.markdown(f"📍 {profile_data.get('location')}")
        st.markdown("> *\"Learning, building, and exploring the world of networking, IT infrastructure, and cybersecurity.\"*")

    st.markdown("---")
    st.header("Core Learning Areas")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        net_card = """<div class="card">
    <h3>🌐 Networking</h3>
    <ul>
        <li>IP Addressing & Subnetting</li>
        <li>Routing & VLANs</li>
        <li>Router Configuration</li>
        <li>Cisco Packet Tracer</li>
    </ul>
    <span class="badge">Practical Practice</span>
</div>"""
        st.markdown(net_card, unsafe_allow_html=True)
        
    with c2:
        sec_card = """<div class="card">
    <h3>🔒 Network Security</h3>
    <ul>
        <li>Port Security</li>
        <li>SSH Configuration</li>
        <li>ACLs (Beginner)</li>
        <li>Access Control Concepts</li>
    </ul>
    <span class="badge">Currently Learning</span>
</div>"""
        st.markdown(sec_card, unsafe_allow_html=True)
        
    with c3:
        infra_card = """<div class="card">
    <h3>⚙️ IT Infrastructure</h3>
    <ul>
        <li>MikroTik Basics</li>
        <li>EtherChannel (Beginner)</li>
        <li>Network Topology Design</li>
        <li>Infrastructure Fundamentals</li>
    </ul>
    <span class="badge">Exploring</span>
</div>"""
        st.markdown(infra_card, unsafe_allow_html=True)

# ==========================================
# ABOUT PAGE
# ==========================================
elif menu == "About":
    st.title("About Me")
    
    col1, col2 = st.columns([1, 2], gap="medium")
    
    with col1:
        img_url = profile_data.get("profile_image")
        if img_url:
            st.image(img_url, use_column_width=True)
        st.markdown(f"**Location:** {profile_data.get('location')}")
        st.markdown(f"**Status:** {profile_data.get('experience_years')}")
        
    with col2:
        st.subheader(profile_data.get("name"))
        st.write(f"**{profile_data.get('title')}**")
        st.write(profile_data.get("bio"))

# ==========================================
# SKILLS PAGE
# ==========================================
elif menu == "Skills":
    st.title("Skills & Competencies")
    skills = fetch_data("skills")
    if not skills:
        st.info("No skills listed.")
    else:
        cols = st.columns(3)
        for idx, skill in enumerate(skills):
            with cols[idx % 3]:
                sk_name = skill.get("name")
                sk_cat = skill.get("category")
                sk_lvl = skill.get("level")
                skill_card = f'<div class="card"><h4>{sk_name}</h4><p><span class="badge-secondary">{sk_cat}</span></p><p><strong>Level:</strong> <span class="accent-text">{sk_lvl}</span></p></div>'
                st.markdown(skill_card, unsafe_allow_html=True)

# ==========================================
# PROJECTS PAGE
# ==========================================
elif menu == "Projects":
    st.title("Projects & Lab Simulations")
    projects = fetch_data("projects")
    if not projects:
        st.info("No projects added yet.")
    else:
        for proj in projects:
            p_title = proj.get("title")
            p_cat = proj.get("category")
            with st.expander(f"📌 {p_title} ({p_cat})"):
                st.write(proj.get("description"))

# ==========================================
# AREAS OF INTEREST PAGE
# ==========================================
elif menu == "Areas of Interest":
    st.title("Areas of Interest & Focus")
    services = fetch_data("services")
    if not services:
        st.info("No interest areas listed.")
    else:
        for srv in services:
            s_title = srv.get("title")
            s_desc = srv.get("description")
            srv_card = f'<div class="card"><h3>{s_title}</h3><p>{s_desc}</p></div>'
            st.markdown(srv_card, unsafe_allow_html=True)

# ==========================================
# EXPERIENCE PAGE
# ==========================================
elif menu == "Experience":
    st.title("Practice & Experience")
    exps = fetch_data("experience")
    if not exps:
        st.info("No experience entries listed.")
    else:
        for exp in exps:
            e_pos = exp.get("position")
            e_org = exp.get("organization")
            exp_card = f'<div class="timeline-item"><h4>{e_pos}</h4><p><strong>{e_org}</strong></p></div>'
            st.markdown(exp_card, unsafe_allow_html=True)

# ==========================================
# LEARNING JOURNEY PAGE
# ==========================================
elif menu == "Learning Journey":
    st.title("Learning Journey")
    journey = fetch_data("learning_journey")
    if not journey:
        st.info("No milestones listed.")
    else:
        for item in journey:
            j_title = item.get("title")
            j_desc = item.get("description")
            j_card = f'<div class="timeline-item"><h4>{j_title}</h4><p>{j_desc}</p></div>'
            st.markdown(j_card, unsafe_allow_html=True)

# ==========================================
# CONTACT PAGE
# ==========================================
elif menu == "Contact":
    st.title("Contact & Socials")
    st.markdown(f"**Email:** [{profile_data.get('email')}](mailto:{profile_data.get('email')})")
    st.markdown(f"**Location:** {profile_data.get('location')}")

# ==========================================
# ADMIN PANEL
# ==========================================
elif menu == "Admin Panel":
    st.title("Admin Dashboard")
    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False
        
    if not st.session_state["admin_authenticated"]:
        admin_code = st.text_input("Enter Admin Code", type="password")
        if st.button("Unlock"):
            expected_code = st.secrets.get("ADMIN_CODE", "admin123")
            if admin_code == expected_code:
                st.session_state["admin_authenticated"] = True
                st.success("Authenticated successfully.")
                st.rerun()
            else:
                st.error("Invalid Admin Code.")
    else:
        if st.button("Logout"):
            st.session_state["admin_authenticated"] = False
            st.rerun()
            
        st.subheader("Edit Profile Data")
        prof = get_profile()
        
        with st.form("profile_form"):
            name = st.text_input("Name", value=prof.get("name", ""))
            title = st.text_input("Title", value=prof.get("title", ""))
            current_focus = st.text_input("Current Focus", value=prof.get("current_focus", ""))
            location = st.text_input("Location", value=prof.get("location", ""))
            email = st.text_input("Email", value=prof.get("email", ""))
            profile_image = st.text_input("Profile Image URL", value=prof.get("profile_image", ""))
            experience_years = st.text_input("Experience Status", value=prof.get("experience_years", ""))
            bio = st.text_area("Bio", value=prof.get("bio", ""))
            
            if st.form_submit_button("Save Profile"):
                data = {
                    "name": name, "title": title, "current_focus": current_focus,
                    "location": location, "email": email, "profile_image": profile_image,
                    "experience_years": experience_years, "bio": bio
                }
                if update_profile(data):
                    st.success("Profile updated successfully!")
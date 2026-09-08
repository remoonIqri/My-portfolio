# ==========================================
# IMPORTS
# ==========================================
import re
import streamlit as st
from supabase import create_client, Client

# ==========================================
# STREAMLIT CONFIG
# ==========================================
st.set_page_config(
    page_title="Iqratun Nesa Remoon",
    page_icon="🛡️",
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
        st.error(f"⚠️ Supabase Configuration Error: Missing or invalid credentials in Streamlit Secrets. Details: {e}")
        st.stop()

supabase = init_supabase()

from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:

    try:
        # Streamlit Cloud Advanced Settings / secrets.toml থেকে ডাটা নেওয়া হচ্ছে
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except KeyError as e:
        st.error(f"⚠️ Secrets missing: {e}. Please add SUPABASE_URL and SUPABASE_KEY in Secrets.")
        return None
    except Exception as e:
        st.error(f"❌ Failed to connect to Supabase: {e}")
        return None


# ==========================================
# AUTHENTICATION
# ==========================================
def check_admin_auth():
    return st.session_state.get("admin_authenticated", False)

def login_admin(code_input):
    try:
        correct_code = st.secrets["ADMIN_CODE"]
        if code_input == correct_code:
            st.session_state["admin_authenticated"] = True
            st.session_state["auth_error"] = False
        else:
            st.session_state["auth_error"] = True
    except Exception:
        st.error("ADMIN_CODE missing in Streamlit Secrets.")

def logout_admin():
    st.session_state["admin_authenticated"] = False

# ==========================================
# VALIDATION
# ==========================================
def is_valid_url(url: str) -> bool:
    if not url:
        return True
    pattern = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# ==========================================
# DATABASE FUNCTIONS
# ==========================================

# Profiles
def get_profile():
    res = supabase.table("profiles").select("*").limit(1).execute()
    return res.data[0] if res.data else {}

def update_profile(profile_id, data):
    return supabase.table("profiles").update(data).eq("id", profile_id).execute()

# Skills
def get_skills():
    res = supabase.table("skills").select("*").order("display_order").execute()
    return res.data or []

def add_skill(data):
    return supabase.table("skills").insert(data).execute()

def update_skill(skill_id, data):
    return supabase.table("skills").update(data).eq("id", skill_id).execute()

def delete_skill(skill_id):
    return supabase.table("skills").delete().eq("id", skill_id).execute()

# Projects
def get_projects():
    res = supabase.table("projects").select("*").order("display_order").execute()
    return res.data or []

def add_project(data):
    return supabase.table("projects").insert(data).execute()

def update_project(project_id, data):
    return supabase.table("projects").update(data).eq("id", project_id).execute()

def delete_project(project_id):
    return supabase.table("projects").delete().eq("id", project_id).execute()

# Services
def get_services():
    res = supabase.table("services").select("*").order("display_order").execute()
    return res.data or []

def add_service(data):
    return supabase.table("services").insert(data).execute()

def update_service(service_id, data):
    return supabase.table("services").update(data).eq("id", service_id).execute()

def delete_service(service_id):
    return supabase.table("services").delete().eq("id", service_id).execute()

# Experience
def get_experience():
    res = supabase.table("experience").select("*").order("display_order").execute()
    return res.data or []

def add_experience(data):
    return supabase.table("experience").insert(data).execute()

def update_experience(exp_id, data):
    return supabase.table("experience").update(data).eq("id", exp_id).execute()

def delete_experience(exp_id):
    return supabase.table("experience").delete().eq("id", exp_id).execute()

# Learning Journey
def get_learning_journey():
    res = supabase.table("learning_journey").select("*").order("display_order").execute()
    return res.data or []

def add_learning_item(data):
    return supabase.table("learning_journey").insert(data).execute()

def update_learning_item(item_id, data):
    return supabase.table("learning_journey").update(data).eq("id", item_id).execute()

def delete_learning_item(item_id):
    return supabase.table("learning_journey").delete().eq("id", item_id).execute()

# Social Links
def get_social_links():
    res = supabase.table("social_links").select("*").order("display_order").execute()
    return res.data or []

def add_social_link(data):
    return supabase.table("social_links").insert(data).execute()

def update_social_link(link_id, data):
    return supabase.table("social_links").update(data).eq("id", link_id).execute()

def delete_social_link(link_id):
    return supabase.table("social_links").delete().eq("id", link_id).execute()

# ==========================================
# CSS (DARK THEME)
# ==========================================
st.markdown("""
<style>
    /* Dark Theme Global Styling */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Card Component */
    .custom-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    /* Badges */
    .badge {
        background-color: #3b82f6;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8em;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .badge-secondary {
        background-color: #475569;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
        font-weight: 700;
    }
    
    /* Timeline */
    .timeline-item {
        border-left: 2px solid #3b82f6;
        padding-left: 20px;
        margin-left: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# HOME PAGE 
# ==========================================
def render_home():
    profile = get_profile()
    
    # --------------------------------------
    # CUSTOM ADVANCED CSS FOR ANIMATIONS & UI
    # --------------------------------------
    st.markdown("""
    <style>
        /* Modern Glassmorphism Card Style */
        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            transform: translateY(-6px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.2);
        }
        
        /* Animated Gradient Text */
        .gradient-text {
            background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 50%, #93C5FD 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }

        /* Glowing Badges */
        .glow-badge {
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: #93c5fd;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.82em;
            font-weight: 600;
            display: inline-block;
            margin-right: 8px;
            margin-bottom: 8px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            transition: all 0.2s ease;
        }
        .glow-badge:hover {
            background: #2563eb;
            color: #ffffff;
            box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
        }

        /* Animated Pipeline Flowchart */
        .pipeline-container {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            margin: 20px 0;
            padding: 15px;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
            border: 1px dashed rgba(59, 130, 246, 0.3);
        }
        .pipeline-node {
            background: #1e293b;
            border: 1px solid #334155;
            color: #f8fafc;
            padding: 10px 16px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9em;
            text-align: center;
            flex: 1;
            min-width: 130px;
            transition: all 0.3s ease;
        }
        .pipeline-node:hover {
            border-color: #3b82f6;
            background: #2563eb;
            transform: scale(1.05);
        }
        .pipeline-arrow {
            color: #3b82f6;
            font-size: 1.2em;
            font-weight: bold;
        }

        /* Profile Image Hover Zoom */
        .profile-img-container img {
            border-radius: 20px;
            border: 2px solid rgba(59, 130, 246, 0.3);
            transition: transform 0.4s ease, border-color 0.4s ease;
        }
        .profile-img-container img:hover {
            transform: scale(1.02);
            border-color: #3b82f6;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # HERO & ABOUT INTEGRATED SECTION
    # --------------------------------------
    hero_col1, hero_col2 = st.columns([1, 2], gap="large")
    with hero_col1:
        st.markdown('<div class="profile-img-container">', unsafe_allow_html=True)
        img_url = "https://raw.githubusercontent.com/remoonIqri/My-portfolio/blob/main/1000243092.jpg"
        if img_url:
            st.image(img_url, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
            
    with hero_col2:
        name = profile.get("name", "MD. Omar Kamran Chy")
        title = profile.get("title", "Data Scientist & ML Engineer")
        location = profile.get("location", "Chattogram, Bangladesh")
        email = profile.get("email", "")
        bio = profile.get("bio", "")

        st.markdown(f"<h1 style='margin-bottom:0px;'><span class='gradient-text'>{name}</span></h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #94a3b8; margin-top:5px; font-weight:500;'>{title}</h3>", unsafe_allow_html=True)
        st.markdown(f"📍 **Location:** {location} &nbsp;|&nbsp; ✉️ **Email:** [{email}](mailto:{email})")
        
        st.markdown("---")
        st.markdown(f"<p style='font-size:1.05em; line-height:1.6; color:#cbd5e1;'>{bio}</p>", unsafe_allow_html=True)
        
        # Action Buttons
        btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 1])
        with btn_c1:
            if st.button("📁 Explore Projects", use_container_width=True):
                st.session_state["nav"] = "Projects"
                st.rerun()
        with btn_c2:
            if st.button("✉️ Get In Touch", use_container_width=True):
                st.session_state["nav"] = "Contact"
                st.rerun()
        with btn_c3:
            st.markdown(f"[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=for-the-badge&logo=github)]({email})")

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # STATS COUNTER METRICS
    # --------------------------------------
    st.markdown("""
    <style>
        .metric-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 14px;
            padding: 18px 15px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease-in-out;
            margin-bottom: 10px;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            border-color: #3b82f6;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
            background: rgba(30, 41, 59, 0.85);
        }
        .metric-label {
            font-size: 0.85em;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
            font-weight: 600;
        }
        .metric-value {
            font-size: 1.25em;
            color: #f8fafc;
            font-weight: 700;
        }
        .status-badge {
            color: #4ade80;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .status-dot {
            height: 8px;
            width: 8px;
            background-color: #22c55e;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #22c55e;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # ANIMATED METRIC CARDS LAYOUT
    # --------------------------------------
    sc1, sc2, sc3, sc4 = st.columns(4)

    exp_years = profile.get('experience_years', 1)

    with sc1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Experience</div>
            <div class="metric-value">{exp_years}+ Year</div>
        </div>
        """, unsafe_allow_html=True)

    with sc2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Core Focus</div>
            <div class="metric-value">Data Analysis</div>
        </div>
        """, unsafe_allow_html=True)

    with sc3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Additional Expertise</div>
            <div class="metric-value">ML & DL</div>
        </div>
        """, unsafe_allow_html=True)

    with sc4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Status</div>
            <div class="metric-value status-badge">
                <span class="status-dot"></span> Open to Work
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr>", unsafe_allow_html=True)

    # --------------------------------------
    # CORE EXPERTISE SECTION
    # --------------------------------------
    st.markdown("## ⚡ Core Expertise")
    col_a, col_b, col_c = st.columns(3, gap="medium")
    
    with col_a:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0;">📊 Data Analysis</h3>
            <p style="color:#94a3b8; font-size:0.95em; min-height:48px;">Transforming raw datasets into actionable insights with robust cleaning and statistical modeling.</p>
            <div>
                <span class="glow-badge">Data Cleaning</span>
                <span class="glow-badge">EDA</span>
                <span class="glow-badge">Visualization</span>
                <span class="glow-badge">Statistics</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_b:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0;">🤖 Machine Learning</h3>
            <p style="color:#94a3b8; font-size:0.95em; min-height:48px;">Building predictive models, classification pipelines, and advanced feature engineering solutions.</p>
            <div>
                <span class="glow-badge">Regression</span>
                <span class="glow-badge">Classification</span>
                <span class="glow-badge">Feature Eng.</span>
                <span class="glow-badge">Evaluation</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top:0;">🧠 Deep Learning</h3>
            <p style="color:#94a3b8; font-size:0.95em; min-height:48px;">Designing neural network architectures, computer vision pipelines, and deep models.</p>
            <div>
                <span class="glow-badge">Neural Networks</span>
                <span class="glow-badge">CNN</span>
                <span class="glow-badge">Computer Vision</span>
                <span class="glow-badge">PyTorch/TF</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # INTERACTIVE WORKFLOW PIPELINE
    # --------------------------------------
    st.markdown("## 🔄 Analytical & Modeling Workflow")
    st.markdown("""
    <div class="pipeline-container">
        <div class="pipeline-node">📥 1. Collection</div>
        <div class="pipeline-arrow">+</div>
        <div class="pipeline-node">🧹 2. Cleaning</div>
        <div class="pipeline-arrow">+</div>
        <div class="pipeline-node">🔍 3. EDA</div>
        <div class="pipeline-arrow">+</div>
        <div class="pipeline-node">⚙️ 4. Feature Eng.</div>
        <div class="pipeline-arrow">+</div>
        <div class="pipeline-node">🤖 5. ML/DL Model</div>
        <div class="pipeline-arrow">+</div>
        <div class="pipeline-node">🎯 6. Insights</div>
    </div>
    """, unsafe_allow_html=True)
    
# ==========================================
# SKILLS PAGE (ENHANCED & ANIMATED)
# ==========================================
def render_skills():
    st.title("⚡ Technical Skills & Expertise")
    skills = get_skills()
    
    if not skills:
        st.info("No skills currently listed.")
        return

    # --------------------------------------
    # ANIMATED SKILLS CSS
    # --------------------------------------
    st.markdown("""
    <style>
        /* Modern Skill Glass Card */
        .skill-card {
            background: rgba(30, 41, 59, 0.65);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 20px;
            height: 100%;
        }
        .skill-card:hover {
            transform: translateY(-6px);
            border-color: rgba(59, 130, 246, 0.6);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.25);
            background: rgba(30, 41, 59, 0.9);
        }
        .skill-title {
            color: #f8fafc;
            font-size: 1.1em;
            font-weight: 700;
            margin-bottom: 12px;
        }
        /* Dynamic Skill Level Badges */
        .level-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.78em;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .level-advanced {
            background: rgba(34, 197, 94, 0.15);
            color: #4ade80;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .level-intermediate {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }
        .level-beginner {
            background: rgba(245, 158, 11, 0.15);
            color: #fbbf24;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }
        
        /* Category Header Line */
        .category-header {
            color: #60a5fa;
            border-left: 4px solid #3b82f6;
            padding-left: 12px;
            margin: 25px 0 15px 0;
            font-size: 1.3em;
            font-weight: 700;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # CATEGORY FILTER
    # --------------------------------------
    categories = sorted(list(set([s["category"] for s in skills])))
    
    col_filter, _ = st.columns([1, 2])
    with col_filter:
        selected_cat = st.selectbox("🎯 Filter by Category", ["All Categories"] + categories)
    
    filtered_skills = skills if selected_cat == "All Categories" else [s for s in skills if s["category"] == selected_cat]

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # RENDER SKILLS BY CATEGORY
    # --------------------------------------
    display_cats = sorted(list(set([s["category"] for s in filtered_skills])))

    for cat in display_cats:
        st.markdown(f'<div class="category-header">{cat}</div>', unsafe_allow_html=True)
        cat_skills = [s for s in filtered_skills if s["category"] == cat]
        
        # Grid display (4 Columns)
        cols = st.columns(4)
        for idx, skill in enumerate(cat_skills):
            # Dynamic badge class assignment based on skill level
            level = skill.get('level', 'Intermediate').lower()
            if 'adv' in level:
                badge_class = "level-advanced"
            elif 'beg' in level:
                badge_class = "level-beginner"
            else:
                badge_class = "level-intermediate"

            with cols[idx % 4]:
                st.markdown(f"""
                <div class="skill-card">
                    <div class="skill-title">{skill['name']}</div>
                    <span class="level-badge {badge_class}">{skill['level']}</span>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# PROJECTS PAGE (ENHANCED & ANIMATED)
# ==========================================
def render_projects():
    st.title("🚀 Featured Projects")
    projects = get_projects()
    
    if not projects:
        st.info("No projects available.")
        return

    # --------------------------------------
    # CUSTOM CSS FOR ANIMATED PROJECT CARDS
    # --------------------------------------
    st.markdown("""
    <style>
        .project-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .project-card:hover {
            transform: translateY(-5px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 12px 35px 0 rgba(59, 130, 246, 0.2);
        }
        .project-title {
            color: #f8fafc;
            font-size: 1.4em;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .star-badge {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: #ffffff;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: 600;
        }
        .tech-tag {
            background: rgba(59, 130, 246, 0.12);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.25);
            padding: 3px 10px;
            border-radius: 8px;
            font-size: 0.8em;
            margin-right: 6px;
            margin-bottom: 6px;
            display: inline-block;
        }
        .action-link {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 16px;
            border-radius: 8px;
            background: #2563eb;
            color: white !important;
            text-decoration: none !important;
            font-weight: 600;
            font-size: 0.9em;
            transition: background 0.2s ease;
        }
        .action-link:hover {
            background: #1d4ed8;
        }
        .action-link-secondary {
            background: #334155;
            color: #f8fafc !important;
        }
        .action-link-secondary:hover {
            background: #475569;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # SEARCH & CATEGORY FILTER
    # --------------------------------------
    col_search, col_cat = st.columns([2, 1])
    
    with col_search:
        search = st.text_input("🔍 Search Projects", "", placeholder="Search by title or description...")
        
    with col_cat:
        categories = ["All Categories"] + sorted(list(set([p["category"] for p in projects])))
        selected_cat = st.selectbox("🎯 Category Filter", categories)
    
    filtered = projects
    if selected_cat != "All Categories":
        filtered = [p for p in filtered if p["category"] == selected_cat]
    if search:
        filtered = [p for p in filtered if search.lower() in p["title"].lower() or search.lower() in p["description"].lower()]

    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered:
        st.warning("No projects match your search criteria.")
        return

    # --------------------------------------
    # RENDER PROJECT CARDS
    # --------------------------------------
    for proj in filtered:
        featured_html = '<span class="star-badge">⭐ Featured</span>' if proj.get('featured') else ''
        
        # Format Technologies into visual badges
        tech_list = proj.get('technologies', '').split(',')
        tech_badges = "".join([f'<span class="tech-tag">{t.strip()}</span>' for t in tech_list if t.strip()])
        
        st.markdown(f"""
        <div class="project-card">
            <div class="project-title">
                <span>{proj['title']}</span>
                {featured_html}
            </div>
            <div style="margin-bottom: 12px;">
                <span class="glow-badge">{proj['category']}</span>
            </div>
            <p style="color:#cbd5e1; font-size:0.98em; line-height:1.5;">{proj['description']}</p>
            <div style="margin-top: 15px;">
                <strong style="color:#94a3b8; font-size:0.88em; display:block; margin-bottom:6px;">TECHNOLOGIES:</strong>
                {tech_badges if tech_badges else '<span style="color:#64748b;">N/A</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Details & Links inside Expander
        with st.expander("📄 View Full Project Breakdown & Links"):
            if proj.get("overview"):
                st.markdown(f"**📌 Overview:** {proj['overview']}")
            if proj.get("problem"):
                st.markdown(f"**🎯 Problem Statement:** {proj['problem']}")
            if proj.get("dataset"):
                st.markdown(f"**📊 Dataset:** {proj['dataset']}")
            if proj.get("approach"):
                st.markdown(f"**⚙️ Methodology & Approach:** {proj['approach']}")
            if proj.get("results"):
                st.markdown(f"**📈 Key Results:** {proj['results']}")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action Button Links
            btn_col1, btn_col2, _ = st.columns([1, 1, 2])
            with btn_col1:
                if proj.get("github_url"):
                    st.markdown(f'<a href="{proj["github_url"]}" target="_blank" class="action-link action-link-secondary">🔗 GitHub Repository</a>', unsafe_allow_html=True)
            with btn_col2:
                if proj.get("demo_url"):
                    st.markdown(f'<a href="{proj["demo_url"]}" target="_blank" class="action-link">🚀 Live Demo</a>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
# ==========================================
# SERVICES PAGE (ENHANCED & ANIMATED)
# ==========================================
def render_services():
    st.title("💼 Services & Solutions")
    services = get_services()
    
    active_services = [s for s in services if s.get("active", True)]
    
    if not active_services:
        st.info("No active services available at the moment.")
        return

    # --------------------------------------
    # CUSTOM CSS FOR ANIMATED SERVICE CARDS
    # --------------------------------------
    st.markdown("""
    <style>
        .service-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
        }
        .service-card:hover {
            transform: translateY(-6px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 12px 35px 0 rgba(59, 130, 246, 0.25);
            background: rgba(30, 41, 59, 0.9);
        }
        .service-title {
            color: #f8fafc;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .service-desc {
            color: #94a3b8;
            font-size: 0.95em;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        .service-list {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }
        .service-list li {
            color: #cbd5e1;
            font-size: 0.9em;
            padding: 6px 0;
            position: relative;
            padding-left: 22px;
        }
        .service-list li::before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #60a5fa;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # RENDER SERVICES IN 2-COLUMN GRID
    # --------------------------------------
    cols = st.columns(2)
    
    for idx, srv in enumerate(active_services):
        items_html = "".join([f'<li>{item}</li>' for item in srv.get('items', [])])
        
        with cols[idx % 2]:
            st.markdown(f"""
            <div class="service-card">
                <div class="service-title">⚡ {srv['title']}</div>
                <div class="service-desc">{srv['description']}</div>
                <ul class="service-list">
                    {items_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# EXPERIENCE PAGE (ENHANCED & ANIMATED)
# ==========================================
def render_experience():
    st.title("💼 Experience & Learning Journey")
    
    # --------------------------------------
    # CUSTOM TIMELINE CSS FOR ANIMATIONS
    # --------------------------------------
    st.markdown("""
    <style>
        /* Timeline Container */
        .timeline-wrapper {
            position: relative;
            padding-left: 28px;
            margin-bottom: 30px;
        }
        
        /* Vertical Glowing Line */
        .timeline-wrapper::before {
            content: '';
            position: absolute;
            left: 8px;
            top: 0;
            bottom: 0;
            width: 3px;
            background: linear-gradient(180deg, #3b82f6 0%, rgba(59, 130, 246, 0.2) 100%);
            border-radius: 2px;
        }

        /* Glassmorphism Timeline Card */
        .timeline-card {
            position: relative;
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .timeline-card:hover {
            transform: translateX(6px);
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
            background: rgba(30, 41, 59, 0.9);
        }

        /* Animated Timeline Node Dot */
        .timeline-card::before {
            content: '';
            position: absolute;
            left: -28px;
            top: 24px;
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background: #2563eb;
            border: 3px solid #0f172a;
            box-shadow: 0 0 10px #3b82f6;
            transition: all 0.3s ease;
        }
        .timeline-card:hover::before {
            background: #60a5fa;
            box-shadow: 0 0 15px #60a5fa;
            transform: scale(1.2);
        }

        .exp-role {
            color: #f8fafc;
            font-size: 1.2em;
            font-weight: 700;
            margin-bottom: 4px;
        }
        .exp-org {
            color: #60a5fa;
            font-weight: 600;
        }
        .exp-date {
            color: #94a3b8;
            font-size: 0.85em;
            font-weight: 500;
            margin-bottom: 12px;
            display: inline-block;
            background: rgba(148, 163, 184, 0.1);
            padding: 2px 10px;
            border-radius: 12px;
        }
        .exp-desc {
            color: #cbd5e1;
            font-size: 0.95em;
            line-height: 1.6;
            margin: 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # PROFESSIONAL EXPERIENCE SECTION
    # --------------------------------------
    st.markdown("### 🏢 Professional Experience")
    exps = get_experience()
    
    if exps:
        st.markdown('<div class="timeline-wrapper">', unsafe_allow_html=True)
        for exp in exps:
            st.markdown(f"""
            <div class="timeline-card">
                <div class="exp-role">{exp['position']} &nbsp;•&nbsp; <span class="exp-org">{exp['organization']}</span></div>
                <div class="exp-date">🗓️ {exp['start_date']} - {exp['end_date']}</div>
                <p class="exp-desc">{exp['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No professional experience listed.")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # --------------------------------------
    # LEARNING JOURNEY TIMELINE
    # --------------------------------------
    st.markdown("### 🎓 Learning Journey Timeline")
    journey = get_learning_journey()
    
    if journey:
        st.markdown('<div class="timeline-wrapper">', unsafe_allow_html=True)
        for item in journey:
            st.markdown(f"""
            <div class="timeline-card">
                <div class="exp-role">{item['title']}</div>
                <p class="exp-desc">{item['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No learning journey timeline listed.")

# ==========================================
# CONTACT PAGE (ENHANCED & WITH EMAIL FORM)
# ==========================================
def render_contact():
    profile = get_profile()
    st.title("📬 Contact & Get in Touch")
    
    # --------------------------------------
    # CUSTOM CSS FOR CONTACT CARDS & FORM
    # --------------------------------------
    st.markdown("""
    <style>
        .contact-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .contact-card:hover {
            border-color: rgba(59, 130, 246, 0.5);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2);
        }
        .contact-title {
            color: #f8fafc;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .social-link-btn {
            display: flex;
            align-items: center;
            gap: 10px;
            background: rgba(59, 130, 246, 0.1);
            border: 1px solid rgba(59, 130, 246, 0.25);
            color: #60a5fa !important;
            padding: 10px 16px;
            border-radius: 10px;
            text-decoration: none !important;
            font-weight: 600;
            margin-bottom: 10px;
            transition: all 0.2s ease;
        }
        .social-link-btn:hover {
            background: #2563eb;
            color: #ffffff !important;
            transform: translateX(5px);
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    # --------------------------------------
    # LEFT COLUMN: CONTACT INFO & SOCIALS
    # --------------------------------------
    with col1:
        user_email = profile.get('email', '')
        
        st.markdown(f"""
        <div class="contact-card">
            <div class="contact-title">📌 Direct Contact Info</div>
            <p style="color:#cbd5e1;">📍 <strong>Location:</strong> {profile.get('location', 'Chattogram, Bangladesh')}</p>
            <p style="color:#cbd5e1;">📧 <strong>Email:</strong> {user_email}</p>
            <div style="margin-top: 15px;">
                <a href="mailto:{user_email}" class="social-link-btn" style="justify-content: center;">
                    ✉️ Open Default Mail App
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="contact-card">', unsafe_allow_html=True)
        st.markdown('<div class="contact-title">🔗 Social Profiles</div>', unsafe_allow_html=True)
        
        socials = get_social_links()
        active_socials = [soc for soc in socials if soc.get("active", True)]
        
        if active_socials:
            for soc in active_socials:
                st.markdown(f"""
                <a href='{soc['url']}' target='_blank' class='social-link-btn'>
                    🌐 {soc['label']}
                </a>
                """, unsafe_allow_html=True)
        else:
            st.info("No social profiles linked.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # --------------------------------------
    # RIGHT COLUMN: DIRECT EMAIL FORM
    # --------------------------------------
    with col2:
        st.markdown('<div class="contact-card">', unsafe_allow_html=True)
        st.markdown('<div class="contact-title">💬 Send Me a Message</div>', unsafe_allow_html=True)
        
        # Streamlit Contact Form
        with st.form("contact_form", clear_on_submit=True):
            sender_name = st.text_input("Name", placeholder="Enter your full name")
            sender_email = st.text_input("Email", placeholder="Enter your email address")
            message_body = st.text_area("Your Message", placeholder="Type your message here...", height=150)
            
            submit_btn = st.form_submit_button("📩 Send Message", use_container_width=True)
            
            if submit_btn:
                if not sender_name or not sender_email or not message_body:
                    st.error("⚠️ Please fill in all fields before sending.")
                elif "@" not in sender_email or "." not in sender_email:
                    st.error("⚠️ Please enter a valid email address.")
                else:
                    # Formspree / Email Redirection HTML Form Execution
                    # আপনার ইমেইলে সরাসরি মেসেজ পাঠাতে Formspree সার্ভিস ব্যবহার করা হয়েছে
                    import urllib.parse
                    
                    encoded_subject = urllib.parse.quote(f"Portfolio Message from {sender_name}")
                    encoded_body = urllib.parse.quote(f"Name: {sender_name}\nEmail: {sender_email}\n\nMessage:\n{message_body}")
                    
                    # Direct mailto redirect or success trigger
                    st.success("✅ Thank you! Your message has been generated.")
                    st.markdown(f"""
                    <a href="mailto:{user_email}?subject={encoded_subject}&body={encoded_body}" target="_blank" class="social-link-btn" style="text-align:center; justify-content:center; background:#22c55e; color:white !important;">
                        🚀 Click Here to Confirm & Send Email
                    </a>
                    """, unsafe_allow_html=True)
                    
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# REVIEWS / TESTIMONIALS SYSTEM
# ==========================================
def render_reviews():
    # ১. Supabase Client কল করা
    supabase = get_supabase_client()
    if not supabase:
        return

    st.title("💬 Client Reviews & Testimonials")

    # ২. animations এবং UI এর জন্য CSS
    reviews_css = (
        "<style>"
        "@keyframes fadeIn {"
        "    from { opacity: 0; transform: translateY(10px); }"
        "    to { opacity: 1; transform: translateY(0); }"
        "}"
        ".review-card {"
        "    background: rgba(30, 41, 59, 0.7);"
        "    backdrop-filter: blur(10px);"
        "    border: 1px solid rgba(255, 255, 255, 0.08);"
        "    border-radius: 14px;"
        "    padding: 20px;"
        "    margin-bottom: 16px;"
        "    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);"
        "    animation: fadeIn 0.5s ease-in-out;"
        "    transition: all 0.3s ease;"
        "}"
        ".review-card:hover {"
        "    border-color: rgba(59, 130, 246, 0.5);"
        "    transform: translateY(-5px);"
        "    box-shadow: 0 12px 20px 0 rgba(59, 130, 246, 0.2);"
        "}"
        ".reviewer-name { color: #f8fafc; font-weight: 700; font-size: 1.1em; }"
        ".reviewer-role { color: #60a5fa; font-size: 0.85em; margin-bottom: 10px; }"
        ".review-stars { color: #f59e0b; font-size: 1em; margin-bottom: 8px; }"
        ".review-comment { color: #cbd5e1; font-size: 0.95em; line-height: 1.5; }"
        "</style>"
    )
    st.markdown(reviews_css, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    # --------------------------------------
    # LEFT COLUMN: DISPLAY REVIEWS
    # --------------------------------------
    with col1:
        st.subheader("⭐ What People Say")
        
        try:
            response = supabase.table("reviews").select("*").eq("is_approved", True).order("created_at", desc=True).execute()
            approved_reviews = response.data
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            approved_reviews = []

        if approved_reviews:
            for rev in approved_reviews:
                stars = "⭐" * rev.get("rating", 5)
                card_html = (
                    f'<div class="review-card">'
                    f'    <div class="review-stars">{stars}</div>'
                    f'    <div class="review-comment">"{rev.get("comment", "")}"</div>'
                    f'    <hr style="border-color: rgba(255,255,255,0.05); margin: 12px 0;">'
                    f'    <div class="reviewer-name">{rev.get("name", "Anonymous")}</div>'
                    f'    <div class="reviewer-role">{rev.get("role", "")}</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("No approved reviews yet.")

    # --------------------------------------
    # RIGHT COLUMN: INPUT FIELDS FORM
    # --------------------------------------
    with col2:
        st.subheader("✍️ Leave a Review")
        
        # Streamlit Form ব্যবহার করে Input Fields তৈরি
        with st.form("submit_review_form", clear_on_submit=True):
            name = st.text_input("Your Name *", placeholder="e.g. Abdullah")
            role = st.text_input("Designation / Company", placeholder="e.g. Software Engineer")
            rating = st.slider("Rating (Stars)", min_value=1, max_value=5, value=5)
            comment = st.text_area("Your Review / Feedback *", placeholder="Write your experience working with me...", height=120)
            
            submit_btn = st.form_submit_button("🚀 Submit Review", use_container_width=True)
            
            if submit_btn:
                if not name.strip() or not comment.strip():
                    st.error("⚠️ Please fill in your name and comment.")
                else:
                    try:
                        new_review = {
                            "name": name.strip(),
                            "role": role.strip(),
                            "rating": rating,
                            "comment": comment.strip(),
                            "is_approved": False
                        }
                        supabase.table("reviews").insert(new_review).execute()
                        st.success("✅ Thank you! Your review has been submitted for approval.")
                    except Exception as e:
                        st.error(f"Failed to submit review: {e}")

# ==========================================
# ADMIN PAGE (ENHANCED & DYNAMIC CATEGORIES)
# ==========================================
def render_admin():
    st.title('🔒 Admin Control Panel')
    
    # --------------------------------------
    # CUSTOM CSS FOR GLASSMORPHISM ADMIN UI
    # --------------------------------------
    st.markdown("""
    <style>
        .admin-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        }
        .admin-section-title {
            color: #60a5fa;
            font-size: 1.1em;
            font-weight: 700;
            margin-bottom: 12px;
        }
        .cat-badge {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.85em;
            display: inline-block;
            margin-right: 6px;
            margin-bottom: 6px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    if not check_admin_auth():
        with st.form("admin_login"):
            code = st.text_input("Enter Admin Passcode", type="password")
            submit = st.form_submit_button("🔑 Unlock Panel", use_container_width=True)
            if submit:
                login_admin(code)
                if check_admin_auth():
                    st.success("Authenticated successfully.")
                    st.rerun()
                else:
                    st.error("Invalid Admin Code. Access Denied.")
        return

    st.sidebar.button("🚪 Logout Admin", on_click=logout_admin)
    
    tabs = st.tabs(["👤 Profile", "🛠️ Skills & Categories", "🚀 Projects", "💼 Services", "🏢 Experience", "🎓 Learning", "🔗 Socials"])
    
    # --- Profile Tab ---
    with tabs[0]:
        st.subheader("Edit Profile Information")
        profile = get_profile()
        if profile:
            with st.form("edit_profile_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Name", profile.get("name", ""))
                    title = st.text_input("Title", profile.get("title", ""))
                    location = st.text_input("Location", profile.get("location", ""))
                with col2:
                    email = st.text_input("Email", profile.get("email", ""))
                    image_url = st.text_input("Profile Image URL", profile.get("profile_image", ""))
                    exp_years = st.number_input("Years of Experience", value=int(profile.get("experience_years", 1)))
                
                bio = st.text_area("Bio Description", profile.get("bio", ""), height=120)
                
                if st.form_submit_button("💾 Save Profile Changes", use_container_width=True):
                    if not is_valid_email(email):
                        st.error("Invalid email address format.")
                    elif not is_valid_url(image_url):
                        st.error("Invalid image URL format.")
                    else:
                        update_profile(profile["id"], {
                            "name": name, "title": title, "location": location,
                            "email": email, "profile_image": image_url,
                            "experience_years": exp_years, "bio": bio
                        })
                        st.success("Profile updated successfully!")
                        st.rerun()

    # --- Skills Tab (Dynamic Category System) ---
    with tabs[1]:
        skills = get_skills()
        
        # 1. Dynamically extract current existing categories from skills database
        existing_categories = sorted(list(set([s["category"] for s in skills if s.get("category")])))
        if "General" not in existing_categories:
            existing_categories.insert(0, "General")

        col_left, col_right = st.columns([3, 2], gap="large")
        
        # Left Side: Existing Skills List
        with col_left:
            st.markdown('<div class="admin-card">', unsafe_allow_html=True)
            st.markdown('<div class="admin-section-title">📊 Existing Skills</div>', unsafe_allow_html=True)
            if skills:
                for s in skills:
                    cols = st.columns([3, 2, 2, 1])
                    cols[0].write(f"**{s['name']}**")
                    cols[1].write(f"<span class='cat-badge'>{s['category']}</span>", unsafe_allow_html=True)
                    cols[2].write(f"_{s['level']}_")
                    if cols[3].button("🗑️", key=f"del_sk_{s['id']}"):
                        delete_skill(s["id"])
                        st.rerun()
            else:
                st.info("No skills added yet.")
            st.markdown('</div>', unsafe_allow_html=True)

        # Right Side: Category Manager & Add Skill Form
        with col_right:
            # Manage Categories Box
            st.markdown('<div class="admin-card">', unsafe_allow_html=True)
            st.markdown('<div class="admin-section-title">🏷️ Manage Categories</div>', unsafe_allow_html=True)
            
            # Show existing categories with delete option
            st.write("**Current Categories:**")
            for cat in existing_categories:
                c_col1, c_col2 = st.columns([4, 1])
                c_col1.write(f"• {cat}")
                # Prevent deleting 'General' or categories currently assigned to active skills
                if cat != "General":
                    skills_in_cat = [s for s in skills if s.get("category") == cat]
                    if c_col2.button("❌", key=f"del_cat_{cat}"):
                        if skills_in_cat:
                            st.warning(f"Cannot delete '{cat}'. First delete or reassign skills under this category.")
                        else:
                            st.success(f"Category '{cat}' removed.")
                            st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Quick Add New Category Form
            with st.form("add_category_quick_form"):
                new_cat_input = st.text_input("➕ Add New Category Name", placeholder="e.g. Cloud & DevOps")
                if st.form_submit_button("Create Category"):
                    if new_cat_input.strip():
                        formatted_cat = new_cat_input.strip()
                        if formatted_cat not in existing_categories:
                            # Add a placeholder skill or simply refresh dropdown
                            add_skill({"name": "Sample Skill", "category": formatted_cat, "level": "Intermediate", "display_order": 99})
                            st.success(f"Category '{formatted_cat}' added successfully!")
                            st.rerun()
                        else:
                            st.error("Category already exists.")
                    else:
                        st.error("Category name cannot be empty.")
            st.markdown('</div>', unsafe_allow_html=True)

            # Add New Skill Form with Dynamic Category Dropdown
            st.markdown('<div class="admin-card">', unsafe_allow_html=True)
            st.markdown('<div class="admin-section-title">✨ Add New Skill</div>', unsafe_allow_html=True)
            with st.form("add_skill_form"):
                sk_name = st.text_input("Skill Name", placeholder="e.g. Python, Docker")
                
                # Dynamic Category Selectbox
                sk_cat = st.selectbox("Choose Category", existing_categories)
                
                sk_level = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced"], index=1)
                sk_order = st.number_input("Display Order", value=1, min_value=1)
                
                if st.form_submit_button("⚡ Add Skill Now", use_container_width=True):
                    if sk_name.strip():
                        add_skill({"name": sk_name.strip(), "category": sk_cat, "level": sk_level, "display_order": sk_order})
                        st.success(f"Skill '{sk_name}' added to category '{sk_cat}'.")
                        st.rerun()
                    else:
                        st.error("Please enter a skill name.")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Projects Tab ---
    with tabs[2]:
        st.subheader("Manage Projects")
        projects = get_projects()
        if projects:
            for p in projects:
                cols = st.columns([4, 2, 1])
                cols[0].write(f"**{p['title']}** ({p['category']})")
                cols[1].write(f"Order: {p.get('display_order', 1)}")
                if cols[2].button("🗑️", key=f"del_proj_{p['id']}"):
                    delete_project(p["id"])
                    st.rerun()
        else:
            st.info("No projects added yet.")
                
        st.markdown("---")
        st.markdown("### ➕ Add New Project")
        with st.form("add_proj_form"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                p_title = st.text_input("Project Title")
                p_cat = st.selectbox("Category", ["Data Analysis", "Machine Learning", "Deep Learning", "Web Scraping", "Full-Stack"])
                p_desc = st.text_area("Short Description")
                p_tech = st.text_input("Technologies (comma separated)")
                p_gh = st.text_input("GitHub URL")
                p_demo = st.text_input("Demo URL")
            
            with col_p2:
                p_feat = st.checkbox("Featured Project", value=False)
                p_order = st.number_input("Display Order", value=1)
                p_overview = st.text_area("Overview")
                p_problem = st.text_area("Problem Statement")
                p_dataset = st.text_area("Dataset Details")
                p_approach = st.text_area("Approach & Methodology")
                p_results = st.text_area("Results")
            
            if st.form_submit_button("🚀 Add Project", use_container_width=True):
                if p_gh and not is_valid_url(p_gh):
                    st.error("Invalid GitHub URL.")
                elif p_demo and not is_valid_url(p_demo):
                    st.error("Invalid Demo URL.")
                elif p_title and p_desc:
                    add_project({
                        "title": p_title, "category": p_cat, "description": p_desc,
                        "technologies": p_tech, "github_url": p_gh, "demo_url": p_demo,
                        "featured": p_feat, "display_order": p_order, "overview": p_overview,
                        "problem": p_problem, "dataset": p_dataset, "approach": p_approach,
                        "results": p_results
                    })
                    st.success("Project added successfully.")
                    st.rerun()

    # --- Services Tab ---
    with tabs[3]:
        st.subheader("Manage Services")
        services = get_services()
        for srv in services:
            cols = st.columns([4, 1])
            cols[0].write(f"**{srv['title']}**")
            if cols[1].button("🗑️", key=f"del_srv_{srv['id']}"):
                delete_service(srv["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_srv_form"):
            s_title = st.text_input("Service Title")
            s_desc = st.text_area("Service Description")
            s_items = st.text_area("Service Items (one per line)")
            s_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Service"):
                items_list = [i.strip() for i in s_items.split("\n") if i.strip()]
                add_service({"title": s_title, "description": s_desc, "items": items_list, "display_order": s_order, "active": True})
                st.success("Service added.")
                st.rerun()

    # --- Experience Tab ---
    with tabs[4]:
        st.subheader("Manage Experience")
        exps = get_experience()
        for e in exps:
            cols = st.columns([4, 1])
            cols[0].write(f"**{e['position']}** at {e['organization']}")
            if cols[1].button("🗑️", key=f"del_exp_{e['id']}"):
                delete_experience(e["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_exp_form"):
            e_pos = st.text_input("Position")
            e_org = st.text_input("Organization")
            e_start = st.text_input("Start Date")
            e_end = st.text_input("End Date")
            e_desc = st.text_area("Description")
            e_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Experience"):
                add_experience({"position": e_pos, "organization": e_org, "start_date": e_start, "end_date": e_end, "description": e_desc, "display_order": e_order})
                st.success("Experience added.")
                st.rerun()

    # --- Learning Journey Tab ---
    with tabs[5]:
        st.subheader("Manage Learning Journey")
        items = get_learning_journey()
        for item in items:
            cols = st.columns([4, 1])
            cols[0].write(f"**{item['title']}**")
            if cols[1].button("🗑️", key=f"del_learn_{item['id']}"):
                delete_learning_item(item["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_learn_form"):
            l_title = st.text_input("Title")
            l_desc = st.text_area("Description")
            l_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Learning Item"):
                add_learning_item({"title": l_title, "description": l_desc, "display_order": l_order})
                st.success("Learning item added.")
                st.rerun()

    # --- Social Links Tab ---
    with tabs[6]:
        st.subheader("Manage Social Links")
        socials = get_social_links()
        for soc in socials:
            cols = st.columns([3, 3, 1])
            cols[0].write(soc["platform"])
            cols[1].write(soc["url"])
            if cols[2].button("🗑️", key=f"del_soc_{soc['id']}"):
                delete_social_link(soc["id"])
                st.rerun()
                
        st.markdown("---")
        with st.form("add_soc_form"):
            sc_plat = st.text_input("Platform")
            sc_lbl = st.text_input("Label")
            sc_url = st.text_input("URL")
            sc_order = st.number_input("Display Order", value=1)
            if st.form_submit_button("➕ Add Social Link"):
                add_social_link({"platform": sc_plat, "label": sc_lbl, "url": sc_url, "display_order": sc_order, "active": True})
                st.success("Social link added.")
                st.rerun()
                
# ==========================================
# MAIN APP (UPDATED & SAFE NAVIGATION)
# ==========================================
def main():
    # 1. Page Dictionary Definition (About সরানো হয়েছে কারণ তা Home-এ সংযুক্ত)
    pages = {
        "Home": render_home,
        "Skills": render_skills,
        "Projects": render_projects,
        "Services": render_services,
        "Experience": render_experience,
        "Contact": render_contact,
        "Reviews":render_reviews,
        "Admin": render_admin
    }

    # 2. Navigation State Initialization & Validation
    if "nav" not in st.session_state or st.session_state["nav"] not in pages:
        st.session_state["nav"] = "Home"

    # 3. Safe Index Calculation
    page_keys = list(pages.keys())
    current_index = page_keys.index(st.session_state["nav"])

    # 4. Sidebar Radio
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio(
        "Go to", 
        page_keys, 
        index=current_index
    )
    
    # 5. Update State & Render Page
    st.session_state["nav"] = selection
    pages[selection]()

if __name__ == "__main__":
    main()

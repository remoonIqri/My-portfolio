# ==========================================
# IMPORTS
# ==========================================
import streamlit as st
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
    except Exception:
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
    except Exception:
        return []

def get_profile():
    if not supabase:
        return DEFAULT_PROFILE
    try:
        res = supabase.table("profiles").select("*").limit(1).execute()
        if res.data and len(res.data) > 0:
            return res.data[0]
        return DEFAULT_PROFILE
    except Exception:
        return DEFAULT_PROFILE

def update_profile(data):
    if not supabase:
        return False
    try:
        prof = get_profile()
        if isinstance(prof, dict) and "id" in prof:
            supabase.table("profiles").update(data).eq("id", prof["id"]).execute()
        else:
            supabase.table("profiles").insert(data).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error updating profile: {e}")
        return False

def insert_data(table_name, data):
    if not supabase:
        return False
    try:
        supabase.table(table_name).insert(data).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error inserting into {table_name}: {e}")
        return False

def delete_data(table_name, item_id):
    if not supabase:
        return False
    try:
        supabase.table(table_name).delete().eq("id", item_id).execute()
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error deleting from {table_name}: {e}")
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
    ["Home", "Skills", "Projects", "Experience", "Learning Journey", "Contact", "Admin Panel"]
)

# ==========================================
# HOME PAGE
# ==========================================
if menu == "Home":
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        img_url = profile_data.get("profile_image")
        if img_url:
            try:
                st.image(img_url, use_container_width=True)
            except Exception:
                st.warning("Profile image could not be loaded.")
            
    with col2:
        st.title(profile_data.get("name"))
        st.subheader(f":blue[{profile_data.get('title')}]")
        st.markdown(f"**Current Focus:** {profile_data.get('current_focus')}")
        st.markdown(f"**Experience Status:** {profile_data.get('experience_years')}")
        st.markdown(f"📍 {profile_data.get('location')}")
        st.markdown("> *\"Learning, building, and exploring the world of networking, IT infrastructure, and cybersecurity.\"*")

    st.markdown("---")
    
    st.header("About Me")
    bio_text = profile_data.get("bio", "")
    st.markdown(f"""
    <div class="card">
        <p style="font-size: 1.05rem; line-height: 1.6;">{bio_text}</p>
    </div>
    """, unsafe_allow_html=True)

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
# SKILLS PAGE
# ==========================================
elif menu == "Skills":
    st.title("Skills & Competencies")
    skills = fetch_data("skills")
    
    if not skills:
        skills = [
            {"name": "IP Addressing & Subnetting", "category": "Networking", "level": "Intermediate"},
            {"name": "VLANs & Routing", "category": "Networking", "level": "Intermediate"},
            {"name": "Cisco Packet Tracer", "category": "Tools", "level": "Practical"},
            {"name": "Port Security & SSH", "category": "Security", "level": "Beginner"},
            {"name": "Router & Switch Config", "category": "Networking", "level": "Intermediate"},
            {"name": "Network Topology Design", "category": "Infrastructure", "level": "Beginner"}
        ]
        
    cols = st.columns(3)
    for idx, skill in enumerate(skills):
        with cols[idx % 3]:
            sk_name = skill.get("name", "")
            sk_cat = skill.get("category", "")
            sk_lvl = skill.get("level", "")
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
            p_title = proj.get("title", "Project")
            p_cat = proj.get("category", "General")
            with st.expander(f"📌 {p_title} ({p_cat})"):
                st.write(proj.get("description", ""))

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
            e_pos = exp.get("position", "")
            e_org = exp.get("organization", "")
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
            j_title = item.get("title", "")
            j_desc = item.get("description", "")
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
        col_logout, col_empty = st.columns([1, 5])
        with col_logout:
            if st.button("Logout"):
                st.session_state["admin_authenticated"] = False
                st.rerun()
                
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Profile", "Skills", "Projects", "Experience", "Learning Journey"])

        # TAB 1: PROFILE EDIT
        with tab1:
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
                        st.rerun()

        # TAB 2: MANAGE SKILLS
        with tab2:
            st.subheader("Add New Skill")
            with st.form("add_skill_form"):
                sk_name = st.text_input("Skill Name")
                sk_cat = st.text_input("Category (e.g. Networking, Security, Tools)")
                sk_lvl = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced", "Practical"])
                sk_order = st.number_input("Display Order", value=1, step=1)
                
                if st.form_submit_button("Add Skill"):
                    if sk_name:
                        new_skill = {"name": sk_name, "category": sk_cat, "level": sk_lvl, "display_order": sk_order}
                        if insert_data("skills", new_skill):
                            st.success(f"Added skill: {sk_name}")
                            st.rerun()
                    else:
                        st.warning("Skill name is required.")

            st.markdown("---")
            st.subheader("Existing Skills")
            skills_list = fetch_data("skills")
            if skills_list:
                for item in skills_list:
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.write(f"**{item.get('name')}** ({item.get('category')}) - *{item.get('level')}*")
                    with c2:
                        if st.button("Delete", key=f"del_sk_{item.get('id')}"):
                            if delete_data("skills", item.get('id')):
                                st.success("Deleted!")
                                st.rerun()
            else:
                st.info("No skills found in database.")

        # TAB 3: MANAGE PROJECTS
        with tab3:
            st.subheader("Add New Project")
            with st.form("add_project_form"):
                p_title = st.text_input("Project Title")
                p_cat = st.text_input("Category (e.g. Packet Tracer, Security Lab)")
                p_desc = st.text_area("Description")
                p_order = st.number_input("Display Order", value=1, step=1)
                
                if st.form_submit_button("Add Project"):
                    if p_title:
                        new_proj = {"title": p_title, "category": p_cat, "description": p_desc, "display_order": p_order}
                        if insert_data("projects", new_proj):
                            st.success(f"Added project: {p_title}")
                            st.rerun()
                    else:
                        st.warning("Project title is required.")

            st.markdown("---")
            st.subheader("Existing Projects")
            projects_list = fetch_data("projects")
            if projects_list:
                for item in projects_list:
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.write(f"**{item.get('title')}** ({item.get('category')})")
                    with c2:
                        if st.button("Delete", key=f"del_proj_{item.get('id')}"):
                            if delete_data("projects", item.get('id')):
                                st.success("Deleted!")
                                st.rerun()
            else:
                st.info("No projects found in database.")

        # TAB 4: MANAGE EXPERIENCE
        with tab4:
            st.subheader("Add New Experience")
            with st.form("add_exp_form"):
                e_pos = st.text_input("Position / Role")
                e_org = st.text_input("Organization / Details")
                e_order = st.number_input("Display Order", value=1, step=1)
                
                if st.form_submit_button("Add Experience"):
                    if e_pos:
                        new_exp = {"position": e_pos, "organization": e_org, "display_order": e_order}
                        if insert_data("experience", new_exp):
                            st.success("Added experience!")
                            st.rerun()
                    else:
                        st.warning("Position is required.")

            st.markdown("---")
            st.subheader("Existing Experience")
            exp_list = fetch_data("experience")
            if exp_list:
                for item in exp_list:
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.write(f"**{item.get('position')}** - {item.get('organization')}")
                    with c2:
                        if st.button("Delete", key=f"del_exp_{item.get('id')}"):
                            if delete_data("experience", item.get('id')):
                                st.success("Deleted!")
                                st.rerun()
            else:
                st.info("No experience entries found in database.")

        # TAB 5: MANAGE LEARNING JOURNEY
        with tab5:
            st.subheader("Add Learning Journey Milestone")
            with st.form("add_lj_form"):
                j_title = st.text_input("Milestone Title")
                j_desc = st.text_area("Description")
                j_order = st.number_input("Display Order", value=1, step=1)
                
                if st.form_submit_button("Add Milestone"):
                    if j_title:
                        new_item = {"title": j_title, "description": j_desc, "display_order": j_order}
                        if insert_data("learning_journey", new_item):
                            st.success("Added milestone!")
                            st.rerun()
                    else:
                        st.warning("Title is required.")

            st.markdown("---")
            st.subheader("Existing Milestones")
            journey_list = fetch_data("learning_journey")
            if journey_list:
                for item in journey_list:
                    c1, c2 = st.columns([4, 1])
                    with c1:
                        st.write(f"**{item.get('title')}**")
                    with c2:
                        if st.button("Delete", key=f"del_lj_{item.get('id')}"):
                            if delete_data("learning_journey", item.get('id')):
                                st.success("Deleted!")
                                st.rerun()
            else:
                st.info("No learning journey items found in database.")

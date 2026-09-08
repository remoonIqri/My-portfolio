# ==========================================
# IMPORTS
# ==========================================
import re
import html
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
def get_supabase_client() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]

        if not url or not key:
            raise ValueError("SUPABASE_URL or SUPABASE_KEY is empty.")

        return create_client(url, key)

    except KeyError as e:
        st.error(
            f"⚠️ Missing Streamlit Secret: {e}. "
            "Please add SUPABASE_URL and SUPABASE_KEY."
        )
        st.stop()

    except Exception as e:
        st.error(f"❌ Failed to connect to Supabase: {e}")
        st.stop()


supabase = get_supabase_client()


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
            return True

        st.session_state["auth_error"] = True
        return False

    except KeyError:
        st.error("⚠️ ADMIN_CODE is missing in Streamlit Secrets.")
        return False


def logout_admin():
    st.session_state["admin_authenticated"] = False


# ==========================================
# VALIDATION
# ==========================================
def is_valid_url(url: str) -> bool:
    if not url:
        return True

    pattern = re.compile(
        r"^(?:http|https|ftp)://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+"
        r"(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
        r"localhost|"
        r"\d{1,3}(?:\.\d{1,3}){3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE
    )

    return re.match(pattern, url) is not None


def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def safe_text(value):
    return html.escape(str(value)) if value is not None else ""


# ==========================================
# DATABASE FUNCTIONS
# ==========================================

# ------------------------------------------
# PROFILE
# ------------------------------------------
def get_profile():
    try:
        res = (
            supabase
            .table("profiles")
            .select("*")
            .order("created_at", desc=False)
            .limit(1)
            .execute()
        )
        return res.data[0] if res.data else {}

    except Exception as e:
        st.error(f"Unable to load profile: {e}")
        return {}


def update_profile(profile_id, data):
    return (
        supabase
        .table("profiles")
        .update(data)
        .eq("id", profile_id)
        .execute()
    )


# ------------------------------------------
# SKILLS
# ------------------------------------------
def get_skills():
    res = (
        supabase
        .table("skills")
        .select("*")
        .order("display_order")
        .execute()
    )
    return res.data or []


def add_skill(data):
    return supabase.table("skills").insert(data).execute()


def update_skill(skill_id, data):
    return (
        supabase
        .table("skills")
        .update(data)
        .eq("id", skill_id)
        .execute()
    )


def delete_skill(skill_id):
    return (
        supabase
        .table("skills")
        .delete()
        .eq("id", skill_id)
        .execute()
    )


# ------------------------------------------
# PROJECTS
# ------------------------------------------
def get_projects():
    res = (
        supabase
        .table("projects")
        .select("*")
        .order("display_order")
        .execute()
    )
    return res.data or []


def add_project(data):
    return supabase.table("projects").insert(data).execute()


def update_project(project_id, data):
    return (
        supabase
        .table("projects")
        .update(data)
        .eq("id", project_id)
        .execute()
    )


def delete_project(project_id):
    return (
        supabase
        .table("projects")
        .delete()
        .eq("id", project_id)
        .execute()
    )


# ------------------------------------------
# SERVICES
# ------------------------------------------
def get_services():
    res = (
        supabase
        .table("services")
        .select("*")
        .order("display_order")
        .execute()
    )
    return res.data or []


def add_service(data):
    return supabase.table("services").insert(data).execute()


def update_service(service_id, data):
    return (
        supabase
        .table("services")
        .update(data)
        .eq("id", service_id)
        .execute()
    )


def delete_service(service_id):
    return (
        supabase
        .table("services")
        .delete()
        .eq("id", service_id)
        .execute()
    )


# ------------------------------------------
# EXPERIENCE
# ------------------------------------------
def get_experience():
    res = (
        supabase
        .table("experience")
        .select("*")
        .order("display_order")
        .execute()
    )
    return res.data or []


def add_experience(data):
    return supabase.table("experience").insert(data).execute()


def update_experience(exp_id, data):
    return (
        supabase
        .table("experience")
        .update(data)
        .eq("id", exp_id)
        .execute()
    )


def delete_experience(exp_id):
    return (
        supabase
        .table("experience")
        .delete()
        .eq("id", exp_id)
        .execute()
    )


# ------------------------------------------
# LEARNING JOURNEY
# ------------------------------------------
def get_learning_journey():
    res = (
        supabase
        .table("learning_journey")
        .select("*")
        .order("display_order")
        .execute()
    )
    return res.data or []


def add_learning_item(data):
    return (
        supabase
        .table("learning_journey")
        .insert(data)
        .execute()
    )


def update_learning_item(item_id, data):
    return (
        supabase
        .table("learning_journey")
        .update(data)
        .eq("id", item_id)
        .execute()
    )


def delete_learning_item(item_id):
    return (
        supabase
        .table("learning_journey")
        .delete()
        .eq("id", item_id)
        .execute()
    )


# ------------------------------------------
# SOCIAL LINKS
# ------------------------------------------
def get_social_links():
    res = (
        supabase
        .table("social_links")
        .select("*")
        .order("display_order")
        .execute()
    )
    return res.data or []


def add_social_link(data):
    return supabase.table("social_links").insert(data).execute()


def update_social_link(link_id, data):
    return (
        supabase
        .table("social_links")
        .update(data)
        .eq("id", link_id)
        .execute()
    )


def delete_social_link(link_id):
    return (
        supabase
        .table("social_links")
        .delete()
        .eq("id", link_id)
        .execute()
    )


# ------------------------------------------
# REVIEWS
# ------------------------------------------
def get_approved_reviews():
    res = (
        supabase
        .table("reviews")
        .select("*")
        .eq("is_approved", True)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def get_all_reviews():
    res = (
        supabase
        .table("reviews")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def add_review(data):
    return supabase.table("reviews").insert(data).execute()


def approve_review(review_id):
    return (
        supabase
        .table("reviews")
        .update({"is_approved": True})
        .eq("id", review_id)
        .execute()
    )


def delete_review(review_id):
    return (
        supabase
        .table("reviews")
        .delete()
        .eq("id", review_id)
        .execute()
    )


# ==========================================
# GLOBAL CSS
# ==========================================
st.markdown(
    """
<style>

.stApp {
    background-color: #0f172a;
    color: #f8fafc;
}

.custom-card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 24px;
    margin-bottom: 20px;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 6px;
    border: none;
    padding: 8px 16px;
    font-weight: 500;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

h1, h2, h3 {
    color: #f8fafc !important;
    font-weight: 700;
}

.glass-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-5px);
    border-color: rgba(59,130,246,0.5);
}

.gradient-text {
    background: linear-gradient(
        135deg,
        #60A5FA 0%,
        #3B82F6 50%,
        #93C5FD 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

.glow-badge {
    background: linear-gradient(
        135deg,
        #1e3a8a 0%,
        #1e40af 100%
    );
    color: #93c5fd;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.82em;
    font-weight: 600;
    display: inline-block;
    margin-right: 8px;
    margin-bottom: 8px;
    border: 1px solid rgba(59,130,246,0.3);
}

.metric-card {
    background: rgba(30,41,59,0.6);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 14px;
    padding: 18px 15px;
    text-align: center;
    margin-bottom: 10px;
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
    font-size: 1.2em;
    color: #f8fafc;
    font-weight: 700;
}

.skill-card {
    background: rgba(30,41,59,0.65);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
}

.skill-title {
    color: #f8fafc;
    font-size: 1.1em;
    font-weight: 700;
    margin-bottom: 12px;
}

.level-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.78em;
    font-weight: 600;
}

.level-advanced {
    background: rgba(34,197,94,0.15);
    color: #4ade80;
}

.level-intermediate {
    background: rgba(59,130,246,0.15);
    color: #60a5fa;
}

.level-beginner {
    background: rgba(245,158,11,0.15);
    color: #fbbf24;
}

.category-header {
    color: #60a5fa;
    border-left: 4px solid #3b82f6;
    padding-left: 12px;
    margin: 25px 0 15px;
    font-size: 1.3em;
    font-weight: 700;
}

.project-card,
.service-card,
.contact-card,
.timeline-card {
    background: rgba(30,41,59,0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
}

.project-title {
    color: #f8fafc;
    font-size: 1.4em;
    font-weight: 700;
    margin-bottom: 10px;
}

.tech-tag {
    background: rgba(59,130,246,0.12);
    color: #60a5fa;
    border: 1px solid rgba(59,130,246,0.25);
    padding: 3px 10px;
    border-radius: 8px;
    font-size: 0.8em;
    margin-right: 6px;
    margin-bottom: 6px;
    display: inline-block;
}

.service-title,
.contact-title {
    color: #f8fafc;
    font-size: 1.3em;
    font-weight: 700;
    margin-bottom: 12px;
}

.service-desc {
    color: #94a3b8;
    line-height: 1.5;
}

.service-list {
    list-style: none;
    padding-left: 0;
}

.service-list li {
    color: #cbd5e1;
    padding: 6px 0 6px 22px;
    position: relative;
}

.service-list li::before {
    content: "✓";
    position: absolute;
    left: 0;
    color: #60a5fa;
    font-weight: bold;
}

.timeline-wrapper {
    position: relative;
    padding-left: 28px;
}

.timeline-wrapper::before {
    content: '';
    position: absolute;
    left: 8px;
    top: 0;
    bottom: 0;
    width: 3px;
    background: linear-gradient(
        180deg,
        #3b82f6 0%,
        rgba(59,130,246,0.2) 100%
    );
    border-radius: 2px;
}

.timeline-card {
    position: relative;
}

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
}

.exp-role {
    color: #f8fafc;
    font-size: 1.2em;
    font-weight: 700;
}

.exp-org {
    color: #60a5fa;
}

.exp-date {
    color: #94a3b8;
    font-size: 0.85em;
    display: inline-block;
    background: rgba(148,163,184,0.1);
    padding: 2px 10px;
    border-radius: 12px;
    margin: 8px 0;
}

.exp-desc {
    color: #cbd5e1;
    line-height: 1.6;
}

.review-card {
    background: rgba(30,41,59,0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================
# HOME PAGE
# ==========================================
def render_home():

    profile = get_profile()
    skills = get_skills()
    projects = get_projects()

    if not profile:
        st.warning("Profile information is not available.")
        return

    name = profile.get("name", "Iqratun Nesa Remoon")
    title = profile.get("title", "IT Infrastructure Enthusiast")
    location = profile.get("location", "Chattogram, Bangladesh")
    email = profile.get("email", "")
    bio = profile.get("bio", "")
    image_url = "https://raw.githubusercontent.com/remoonIqri/My-portfolio/main/1000243092.jpg"
    github_url = ""
    linkedin_url = ""

    socials = get_social_links()

    for social in socials:
        platform = social.get("platform", "").lower()

        if platform == "github":
            github_url = social.get("url", "")

        elif platform == "linkedin":
            linkedin_url = social.get("url", "")

    # --------------------------------------
    # HERO
    # --------------------------------------
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        if image_url:
            st.image(
                image_url,
                use_container_width=True
            )

    with col2:

        st.markdown(
            f"""
            <h1>
                <span class="gradient-text">
                    {safe_text(name)}
                </span>
            </h1>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h3 style="color:#94a3b8 !important;">
                {safe_text(title)}
            </h3>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            📍 **Location:** {safe_text(location)}
            &nbsp; | &nbsp;
            ✉️ **Email:** [{safe_text(email)}](mailto:{email})
            """
        )

        st.markdown("---")

        st.markdown(
            f"""
            <p style="
                font-size:1.05em;
                line-height:1.7;
                color:#cbd5e1;
            ">
                {safe_text(bio)}
            </p>
            """,
            unsafe_allow_html=True
        )

        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button(
                "📁 Explore Projects",
                use_container_width=True
            ):
                st.session_state["nav"] = "Projects"
                st.rerun()

        with b2:
            if st.button(
                "✉️ Get In Touch",
                use_container_width=True
            ):
                st.session_state["nav"] = "Contact"
                st.rerun()

        with b3:
            if github_url:
                st.markdown(
                    f"""
                    <a href='{github_url}'
                       target='_blank'
                       style='
                       display:block;
                       text-align:center;
                       background:#334155;
                       color:white;
                       padding:10px;
                       border-radius:8px;
                       text-decoration:none;
                       font-weight:600;'>
                       🔗 GitHub
                    </a>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------
    # STATS
    # --------------------------------------
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Skills</div>
                <div class="metric-value">
                    {len(skills)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Projects</div>
                <div class="metric-value">
                    {len(projects)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Core Focus</div>
                <div class="metric-value">
                    Cyber Security
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with s4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Focus Area</div>
                <div class="metric-value">
                    Networking
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br><hr>", unsafe_allow_html=True)

    # --------------------------------------
    # CORE EXPERTISE
    # --------------------------------------
    st.markdown("## ⚡ Core Expertise")

    expertise = [
        (
            "🌐 Networking",
            "Developing practical networking knowledge with routing, VLAN, Inter-VLAN and network simulation.",
            ["Routing", "VLAN & Inter-VLAN", "Cisco Packet Tracer"]
        ),
        (
            "🖧 Network Infrastructure",
            "Learning network infrastructure and configuration using MikroTik and related networking concepts.",
            ["MikroTik", "Network Infrastructure", "Configuration"]
        ),
        (
            "🛡️ Network Security",
            "Building foundational network security knowledge through SSH, ACL and Port Security.",
            ["SSH", "ACL", "Port Security"]
        )
    ]

    cols = st.columns(3)

    for i, item in enumerate(expertise):

        title_text, description, badges = item

        with cols[i]:
            badge_html = "".join(
                f'<span class="glow-badge">{safe_text(b)}</span>'
                for b in badges
            )

            st.markdown(
                f"""
                <div class="glass-card">
                    <h3>{title_text}</h3>
                    <p style="
                        color:#94a3b8;
                        line-height:1.6;
                    ">
                        {safe_text(description)}
                    </p>
                    {badge_html}
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------
    # LEARNING WORKFLOW
    # --------------------------------------
    st.markdown("## 🔄 Learning & Security Workflow")

    st.markdown(
        """
        <div class="glass-card">
            <div style="
                display:flex;
                flex-wrap:wrap;
                gap:10px;
                align-items:center;
                justify-content:center;
            ">

                <div class="glow-badge">
                    📚 Learn
                </div>

                <strong>→</strong>

                <div class="glow-badge">
                    🧪 Practice
                </div>

                <strong>→</strong>

                <div class="glow-badge">
                    🌐 Configure
                </div>

                <strong>→</strong>

                <div class="glow-badge">
                    🛡️ Secure
                </div>

                <strong>→</strong>

                <div class="glow-badge">
                    🎯 Improve
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# SKILLS PAGE
# ==========================================
def render_skills():

    st.title("⚡ Technical Skills")

    skills = get_skills()

    if not skills:
        st.info("No skills currently listed.")
        return

    categories = sorted(
        list(
            set(
                s.get("category", "")
                for s in skills
                if s.get("category")
            )
        )
    )

    selected_cat = st.selectbox(
        "🎯 Filter by Category",
        ["All Categories"] + categories
    )

    if selected_cat == "All Categories":
        filtered_skills = skills
    else:
        filtered_skills = [
            s for s in skills
            if s.get("category") == selected_cat
        ]

    display_categories = sorted(
        list(
            set(
                s.get("category", "")
                for s in filtered_skills
            )
        )
    )

    for category in display_categories:

        st.markdown(
            f"""
            <div class="category-header">
                {safe_text(category)}
            </div>
            """,
            unsafe_allow_html=True
        )

        category_skills = [
            s for s in filtered_skills
            if s.get("category") == category
        ]

        cols = st.columns(4)

        for index, skill in enumerate(category_skills):

            level = skill.get(
                "level",
                "Intermediate"
            )

            level_lower = level.lower()

            if "advanced" in level_lower:
                badge = "level-advanced"
            elif "beginner" in level_lower:
                badge = "level-beginner"
            else:
                badge = "level-intermediate"

            with cols[index % 4]:

                st.markdown(
                    f"""
                    <div class="skill-card">
                        <div class="skill-title">
                            {safe_text(skill.get("name", ""))}
                        </div>

                        <span class="level-badge {badge}">
                            {safe_text(level)}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ==========================================
# PROJECTS PAGE
# ==========================================
def render_projects():

    st.title("🚀 Projects")

    projects = get_projects()

    if not projects:
        st.info("No projects available.")
        return

    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "🔍 Search Projects",
            placeholder="Search by title or description..."
        )

    with col2:

        categories = sorted(
            list(
                set(
                    p.get("category", "")
                    for p in projects
                )
            )
        )

        selected_category = st.selectbox(
            "🎯 Category",
            ["All Categories"] + categories
        )

    filtered = projects

    if selected_category != "All Categories":
        filtered = [
            p for p in filtered
            if p.get("category") == selected_category
        ]

    if search:

        query = search.lower()

        filtered = [
            p for p in filtered
            if query in p.get("title", "").lower()
            or query in p.get("description", "").lower()
        ]

    if not filtered:
        st.warning("No projects match your search.")
        return

    for project in filtered:

        featured = (
            " ⭐ Featured"
            if project.get("featured")
            else ""
        )

        technologies = project.get(
            "technologies",
            ""
        )

        tech_html = "".join(
            f'<span class="tech-tag">{safe_text(t.strip())}</span>'
            for t in technologies.split(",")
            if t.strip()
        )

        st.markdown(
            f"""
            <div class="project-card">

                <div class="project-title">
                    {safe_text(project.get("title", ""))}
                    {featured}
                </div>

                <span class="glow-badge">
                    {safe_text(project.get("category", ""))}
                </span>

                <p style="
                    color:#cbd5e1;
                    line-height:1.6;
                ">
                    {safe_text(project.get("description", ""))}
                </p>

                <div>
                    <strong style="color:#94a3b8;">
                        TECHNOLOGIES
                    </strong>
                    <br>
                    {tech_html if tech_html else "N/A"}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander(
            "📄 View Full Project Breakdown & Links"
        ):

            fields = [
                ("📌 Overview", "overview"),
                ("🎯 Problem Statement", "problem"),
                ("📊 Dataset", "dataset"),
                ("⚙️ Approach", "approach"),
                ("📈 Results", "results")
            ]

            for label, key in fields:

                value = project.get(key)

                if value:
                    st.markdown(
                        f"**{label}:** {safe_text(value)}"
                    )

            github = project.get("github_url")
            demo = project.get("demo_url")

            b1, b2 = st.columns(2)

            with b1:

                if github:
                    st.markdown(
                        f"""
                        <a href='{github}'
                           target='_blank'
                           style='
                           display:block;
                           text-align:center;
                           padding:10px;
                           background:#334155;
                           color:white;
                           border-radius:8px;
                           text-decoration:none;'>
                           🔗 GitHub Repository
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

            with b2:

                if demo:
                    st.markdown(
                        f"""
                        <a href='{demo}'
                           target='_blank'
                           style='
                           display:block;
                           text-align:center;
                           padding:10px;
                           background:#2563eb;
                           color:white;
                           border-radius:8px;
                           text-decoration:none;'>
                           🚀 Live Demo
                        </a>
                        """,
                        unsafe_allow_html=True
                    )


# ==========================================
# SERVICES PAGE
# ==========================================
def render_services():

    st.title("💼 Services & Solutions")

    services = get_services()

    active_services = [
        s for s in services
        if s.get("active", True)
    ]

    if not active_services:
        st.info("No active services available.")
        return

    cols = st.columns(2)

    for index, service in enumerate(active_services):

        items = service.get("items", [])

        items_html = "".join(
            f"<li>{safe_text(item)}</li>"
            for item in items
        )

        with cols[index % 2]:

            st.markdown(
                f"""
                <div class="service-card">

                    <div class="service-title">
                        ⚡ {safe_text(service.get("title", ""))}
                    </div>

                    <div class="service-desc">
                        {safe_text(service.get("description", ""))}
                    </div>

                    <ul class="service-list">
                        {items_html}
                    </ul>

                </div>
                """,
                unsafe_allow_html=True
            )


# ==========================================
# EXPERIENCE PAGE
# ==========================================
def render_experience():

    st.title("💼 Experience & Learning Journey")

    # --------------------------------------
    # EXPERIENCE
    # --------------------------------------
    st.markdown("### 🏢 Experience")

    experiences = get_experience()

    if experiences:

        st.markdown(
            '<div class="timeline-wrapper">',
            unsafe_allow_html=True
        )

        for exp in experiences:

            st.markdown(
                f"""
                <div class="timeline-card">

                    <div class="exp-role">
                        {safe_text(exp.get("position", ""))}
                        <span class="exp-org">
                            • {safe_text(exp.get("organization", ""))}
                        </span>
                    </div>

                    <div class="exp-date">
                        🗓️ {safe_text(exp.get("start_date", ""))}
                        -
                        {safe_text(exp.get("end_date", ""))}
                    </div>

                    <p class="exp-desc">
                        {safe_text(exp.get("description", ""))}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    else:
        st.info("No experience listed.")

    st.markdown("---")

    # --------------------------------------
    # LEARNING JOURNEY
    # --------------------------------------
    st.markdown("### 🎓 Learning Journey")

    journey = get_learning_journey()

    if journey:

        st.markdown(
            '<div class="timeline-wrapper">',
            unsafe_allow_html=True
        )

        for item in journey:

            st.markdown(
                f"""
                <div class="timeline-card">

                    <div class="exp-role">
                        {safe_text(item.get("title", ""))}
                    </div>

                    <p class="exp-desc">
                        {safe_text(item.get("description", ""))}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    else:
        st.info("No learning journey listed.")


# ==========================================
# REVIEWS PAGE
# ==========================================
def render_reviews():

    st.title("⭐ Reviews")

    reviews = get_approved_reviews()

    if reviews:

        for review in reviews:

            rating = int(
                review.get("rating", 5)
            )

            stars = "⭐" * rating

            st.markdown(
                f"""
                <div class="review-card">

                    <h3>
                        {safe_text(review.get("name", ""))}
                    </h3>

                    <p style="color:#60a5fa;">
                        {safe_text(review.get("role", ""))}
                    </p>

                    <p>{stars}</p>

                    <p style="
                        color:#cbd5e1;
                        line-height:1.6;
                    ">
                        {safe_text(review.get("comment", ""))}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info(
            "No approved reviews available yet."
        )

    st.markdown("---")

    st.markdown("### ✍️ Leave a Review")

    with st.form(
        "public_review_form",
        clear_on_submit=True
    ):

        name = st.text_input(
            "Your Name"
        )

        role = st.text_input(
            "Role / Position (Optional)"
        )

        rating = st.slider(
            "Rating",
            min_value=1,
            max_value=5,
            value=5
        )

        comment = st.text_area(
            "Your Review"
        )

        submitted = st.form_submit_button(
            "⭐ Submit Review",
            use_container_width=True
        )

        if submitted:

            if not name.strip():
                st.error("Please enter your name.")

            elif not comment.strip():
                st.error("Please write a review.")

            else:

                try:

                    add_review(
                        {
                            "name": name.strip(),
                            "role": role.strip(),
                            "rating": rating,
                            "comment": comment.strip(),
                            "is_approved": False
                        }
                    )

                    st.success(
                        "✅ Review submitted. "
                        "It will appear after approval."
                    )

                except Exception as e:
                    st.error(
                        f"Unable to submit review: {e}"
                    )


# ==========================================
# CONTACT PAGE
# ==========================================
def render_contact():

    profile = get_profile()

    st.title("📬 Contact & Get in Touch")

    if not profile:
        st.warning("Profile data unavailable.")
        return

    email = profile.get("email", "")
    location = profile.get(
        "location",
        "Chattogram, Bangladesh"
    )

    col1, col2 = st.columns(
        [1, 1],
        gap="large"
    )

    # --------------------------------------
    # CONTACT INFO
    # --------------------------------------
    with col1:

        st.markdown(
            f"""
            <div class="contact-card">

                <div class="contact-title">
                    📌 Direct Contact Info
                </div>

                <p style="color:#cbd5e1;">
                    📍 <strong>Location:</strong>
                    {safe_text(location)}
                </p>

                <p style="color:#cbd5e1;">
                    📧 <strong>Email:</strong>
                    {safe_text(email)}
                </p>

                <a href="mailto:{email}"
                   style="
                   display:block;
                   text-align:center;
                   background:#2563eb;
                   color:white;
                   padding:10px;
                   border-radius:8px;
                   text-decoration:none;
                   font-weight:600;">
                   ✉️ Open Mail App
                </a>

            </div>
            """,
            unsafe_allow_html=True
        )

        socials = get_social_links()

        st.markdown(
            '<div class="contact-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="contact-title">🔗 Social Profiles</div>',
            unsafe_allow_html=True
        )

        for social in socials:

            if social.get("active", True):

                st.markdown(
                    f"""
                    <a href='{social.get('url', '')}'
                       target='_blank'
                       style='
                       display:block;
                       background:rgba(59,130,246,0.1);
                       color:#60a5fa;
                       padding:10px 16px;
                       border-radius:10px;
                       margin-bottom:10px;
                       text-decoration:none;
                       font-weight:600;'>
                       🌐 {safe_text(social.get('label', ''))}
                    </a>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # --------------------------------------
    # EMAIL FORM
    # --------------------------------------
    with col2:

        st.markdown(
            '<div class="contact-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="contact-title">💬 Send a Message</div>',
            unsafe_allow_html=True
        )

        with st.form(
            "contact_form",
            clear_on_submit=True
        ):

            sender_name = st.text_input(
                "Name",
                placeholder="Enter your full name"
            )

            sender_email = st.text_input(
                "Email",
                placeholder="Enter your email address"
            )

            message = st.text_area(
                "Your Message",
                height=150
            )

            submit = st.form_submit_button(
                "📩 Generate Email",
                use_container_width=True
            )

            if submit:

                if not sender_name.strip():
                    st.error("Please enter your name.")

                elif not is_valid_email(
                    sender_email.strip()
                ):
                    st.error(
                        "Please enter a valid email."
                    )

                elif not message.strip():
                    st.error(
                        "Please enter your message."
                    )

                else:

                    import urllib.parse

                    subject = urllib.parse.quote(
                        f"Portfolio Message from {sender_name}"
                    )

                    body = urllib.parse.quote(
                        f"Name: {sender_name}\n"
                        f"Email: {sender_email}\n\n"
                        f"Message:\n{message}"
                    )

                    mailto = (
                        f"mailto:{email}"
                        f"?subject={subject}"
                        f"&body={body}"
                    )

                    st.success(
                        "Your email is ready."
                    )

                    st.markdown(
                        f"""
                        <a href='{mailto}'
                           target='_blank'
                           style='
                           display:block;
                           text-align:center;
                           background:#22c55e;
                           color:white;
                           padding:12px;
                           border-radius:8px;
                           text-decoration:none;
                           font-weight:700;'>
                           🚀 Open Email & Send
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ==========================================
# ADMIN PAGE
# ==========================================
def render_admin():

    st.title("🔒 Admin Control Panel")

    if not check_admin_auth():

        with st.form("admin_login"):

            code = st.text_input(
                "Enter Admin Passcode",
                type="password"
            )

            submit = st.form_submit_button(
                "🔑 Unlock Panel",
                use_container_width=True
            )

            if submit:

                if login_admin(code):

                    st.success(
                        "Authenticated successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid Admin Code."
                    )

        return

    if st.sidebar.button("🚪 Logout Admin"):
        logout_admin()
        st.rerun()

    tabs = st.tabs(
        [
            "👤 Profile",
            "🛠️ Skills",
            "🚀 Projects",
            "💼 Services",
            "🏢 Experience",
            "🎓 Learning",
            "🔗 Socials",
            "⭐ Reviews"
        ]
    )

    # ======================================
    # PROFILE
    # ======================================
    with tabs[0]:

        st.subheader(
            "Edit Profile Information"
        )

        profile = get_profile()

        if profile:

            with st.form("edit_profile_form"):

                c1, c2 = st.columns(2)

                with c1:

                    name = st.text_input(
                        "Name",
                        profile.get("name", "")
                    )

                    title = st.text_input(
                        "Title",
                        profile.get("title", "")
                    )

                    location = st.text_input(
                        "Location",
                        profile.get("location", "")
                    )

                with c2:

                    email = st.text_input(
                        "Email",
                        profile.get("email", "")
                    )

                    image_url = st.text_input(
                        "Profile Image URL",
                        profile.get("profile_image", "")
                    )

                    exp_years = st.number_input(
                        "Years of Experience",
                        min_value=0,
                        value=int(
                            profile.get(
                                "experience_years",
                                1
                            )
                        )
                    )

                bio = st.text_area(
                    "Bio",
                    profile.get("bio", ""),
                    height=180
                )

                save = st.form_submit_button(
                    "💾 Save Profile",
                    use_container_width=True
                )

                if save:

                    if not is_valid_email(email):
                        st.error(
                            "Invalid email address."
                        )

                    elif image_url and not is_valid_url(
                        image_url
                    ):
                        st.error(
                            "Invalid image URL."
                        )

                    elif not name.strip():
                        st.error(
                            "Name cannot be empty."
                        )

                    else:

                        update_profile(
                            profile["id"],
                            {
                                "name": name.strip(),
                                "title": title.strip(),
                                "location": location.strip(),
                                "email": email.strip(),
                                "profile_image": image_url.strip(),
                                "experience_years": exp_years,
                                "bio": bio.strip()
                            }
                        )

                        st.success(
                            "Profile updated successfully!"
                        )

                        st.rerun()

    # ======================================
    # SKILLS
    # ======================================
    with tabs[1]:

        st.subheader("Manage Skills")

        skills = get_skills()

        # Existing skills
        if skills:

            for skill in skills:

                c1, c2, c3, c4 = st.columns(
                    [3, 3, 2, 1]
                )

                c1.write(
                    f"**{skill.get('name', '')}**"
                )

                c2.write(
                    skill.get("category", "")
                )

                c3.write(
                    skill.get("level", "")
                )

                if c4.button(
                    "🗑️",
                    key=f"delete_skill_{skill['id']}"
                ):

                    delete_skill(
                        skill["id"]
                    )

                    st.rerun()

        else:
            st.info("No skills added.")

        st.markdown("---")

        # Add skill
        st.markdown("### ➕ Add Skill")

        existing_categories = sorted(
            list(
                set(
                    s.get("category")
                    for s in skills
                    if s.get("category")
                )
            )
        )

        with st.form("add_skill_form"):

            skill_name = st.text_input(
                "Skill Name"
            )

            category = st.text_input(
                "Category",
                placeholder="e.g. Network Security"
            )

            level = st.selectbox(
                "Level",
                [
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ]
            )

            display_order = st.number_input(
                "Display Order",
                min_value=1,
                value=1
            )

            submit = st.form_submit_button(
                "➕ Add Skill",
                use_container_width=True
            )

            if submit:

                if not skill_name.strip():
                    st.error(
                        "Skill name cannot be empty."
                    )

                elif not category.strip():
                    st.error(
                        "Category cannot be empty."
                    )

                else:

                    add_skill(
                        {
                            "name": skill_name.strip(),
                            "category": category.strip(),
                            "level": level,
                            "display_order": display_order
                        }
                    )

                    st.success(
                        "Skill added successfully."
                    )

                    st.rerun()

    # ======================================
    # PROJECTS
    # ======================================
    with tabs[2]:

        st.subheader("Manage Projects")

        projects = get_projects()

        if projects:

            for project in projects:

                c1, c2 = st.columns(
                    [4, 1]
                )

                c1.write(
                    f"**{project.get('title', '')}** "
                    f"({project.get('category', '')})"
                )

                if c2.button(
                    "🗑️",
                    key=f"delete_project_{project['id']}"
                ):

                    delete_project(
                        project["id"]
                    )

                    st.rerun()

        else:
            st.info("No projects added yet.")

        st.markdown("---")

        st.markdown(
            "### ➕ Add New Project"
        )

        with st.form("add_project_form"):

            title = st.text_input(
                "Project Title"
            )

            category = st.text_input(
                "Project Category",
                placeholder="e.g. Personal, Networking"
            )

            description = st.text_area(
                "Short Description"
            )

            technologies = st.text_input(
                "Technologies",
                placeholder="Cisco Packet Tracer, MikroTik"
            )

            github = st.text_input(
                "GitHub URL"
            )

            demo = st.text_input(
                "Demo URL"
            )

            featured = st.checkbox(
                "Featured Project"
            )

            display_order = st.number_input(
                "Display Order",
                min_value=1,
                value=1
            )

            overview = st.text_area(
                "Overview"
            )

            problem = st.text_area(
                "Problem Statement"
            )

            dataset = st.text_area(
                "Dataset"
            )

            approach = st.text_area(
                "Approach"
            )

            results = st.text_area(
                "Results"
            )

            submit = st.form_submit_button(
                "🚀 Add Project",
                use_container_width=True
            )

            if submit:

                if not title.strip():
                    st.error(
                        "Project title is required."
                    )

                elif not description.strip():
                    st.error(
                        "Project description is required."
                    )

                elif github and not is_valid_url(
                    github
                ):
                    st.error(
                        "Invalid GitHub URL."
                    )

                elif demo and not is_valid_url(
                    demo
                ):
                    st.error(
                        "Invalid Demo URL."
                    )

                else:

                    add_project(
                        {
                            "title": title.strip(),
                            "category": category.strip(),
                            "description": description.strip(),
                            "overview": overview.strip() or None,
                            "problem": problem.strip() or None,
                            "dataset": dataset.strip() or None,
                            "approach": approach.strip() or None,
                            "technologies": technologies.strip() or None,
                            "results": results.strip() or None,
                            "github_url": github.strip() or None,
                            "demo_url": demo.strip() or None,
                            "featured": featured,
                            "display_order": display_order
                        }
                    )

                    st.success(
                        "Project added successfully."
                    )

                    st.rerun()

    # ======================================
    # SERVICES
    # ======================================
    with tabs[3]:

        st.subheader("Manage Services")

        services = get_services()

        for service in services:

            c1, c2 = st.columns(
                [4, 1]
            )

            c1.write(
                f"**{service.get('title', '')}**"
            )

            if c2.button(
                "🗑️",
                key=f"delete_service_{service['id']}"
            ):

                delete_service(
                    service["id"]
                )

                st.rerun()

        st.markdown("---")

        with st.form("add_service_form"):

            title = st.text_input(
                "Service Title"
            )

            description = st.text_area(
                "Description"
            )

            items = st.text_area(
                "Items - one per line"
            )

            display_order = st.number_input(
                "Display Order",
                min_value=1,
                value=1
            )

            submit = st.form_submit_button(
                "➕ Add Service"
            )

            if submit:

                item_list = [
                    item.strip()
                    for item in items.split("\n")
                    if item.strip()
                ]

                if not title.strip():
                    st.error(
                        "Service title is required."
                    )

                elif not description.strip():
                    st.error(
                        "Service description is required."
                    )

                else:

                    add_service(
                        {
                            "title": title.strip(),
                            "description": description.strip(),
                            "items": item_list,
                            "display_order": display_order,
                            "active": True
                        }
                    )

                    st.success(
                        "Service added."
                    )

                    st.rerun()

    # ======================================
    # EXPERIENCE
    # ======================================
    with tabs[4]:

        st.subheader("Manage Experience")

        experiences = get_experience()

        for exp in experiences:

            c1, c2 = st.columns(
                [4, 1]
            )

            c1.write(
                f"**{exp.get('position', '')}** "
                f"at {exp.get('organization', '')}"
            )

            if c2.button(
                "🗑️",
                key=f"delete_exp_{exp['id']}"
            ):

                delete_experience(
                    exp["id"]
                )

                st.rerun()

        st.markdown("---")

        with st.form("add_experience_form"):

            position = st.text_input(
                "Position"
            )

            organization = st.text_input(
                "Organization"
            )

            start_date = st.text_input(
                "Start Date"
            )

            end_date = st.text_input(
                "End Date"
            )

            description = st.text_area(
                "Description"
            )

            display_order = st.number_input(
                "Display Order",
                min_value=1,
                value=1
            )

            submit = st.form_submit_button(
                "➕ Add Experience"
            )

            if submit:

                if not position.strip():
                    st.error(
                        "Position is required."
                    )

                elif not organization.strip():
                    st.error(
                        "Organization is required."
                    )

                elif not start_date.strip():
                    st.error(
                        "Start date is required."
                    )

                elif not end_date.strip():
                    st.error(
                        "End date is required."
                    )

                elif not description.strip():
                    st.error(
                        "Description is required."
                    )

                else:

                    add_experience(
                        {
                            "position": position.strip(),
                            "organization": organization.strip(),
                            "start_date": start_date.strip(),
                            "end_date": end_date.strip(),
                            "description": description.strip(),
                            "display_order": display_order
                        }
                    )

                    st.success(
                        "Experience added."
                    )

                    st.rerun()

    # ======================================
    # LEARNING
    # ======================================
    with tabs[5]:

        st.subheader(
            "Manage Learning Journey"
        )

        journey = get_learning_journey()

        for item in journey:

            c1, c2 = st.columns(
                [4, 1]
            )

            c1.write(
                f"**{item.get('title', '')}**"
            )

            if c2.button(
                "🗑️",
                key=f"delete_learning_{item['id']}"
            ):

                delete_learning_item(
                    item["id"]
                )

                st.rerun()

        st.markdown("---")

        with st.form("add_learning_form"):

            title = st.text_input(
                "Title"
            )

            description = st.text_area(
                "Description"
            )

            display_order = st.number_input(
                "Display Order",
                min_value=1,
                value=1
            )

            submit = st.form_submit_button(
                "➕ Add Learning Item"
            )

            if submit:

                if not title.strip():
                    st.error(
                        "Title is required."
                    )

                elif not description.strip():
                    st.error(
                        "Description is required."
                    )

                else:

                    add_learning_item(
                        {
                            "title": title.strip(),
                            "description": description.strip(),
                            "display_order": display_order
                        }
                    )

                    st.success(
                        "Learning item added."
                    )

                    st.rerun()

    # ======================================
    # SOCIALS
    # ======================================
    with tabs[6]:

        st.subheader(
            "Manage Social Links"
        )

        socials = get_social_links()

        for social in socials:

            c1, c2, c3 = st.columns(
                [2, 4, 1]
            )

            c1.write(
                social.get("platform", "")
            )

            c2.write(
                social.get("url", "")
            )

            if c3.button(
                "🗑️",
                key=f"delete_social_{social['id']}"
            ):

                delete_social_link(
                    social["id"]
                )

                st.rerun()

        st.markdown("---")

        with st.form("add_social_form"):

            platform = st.text_input(
                "Platform",
                placeholder="GitHub"
            )

            label = st.text_input(
                "Label",
                placeholder="GitHub Profile"
            )

            url = st.text_input(
                "URL"
            )

            display_order = st.number_input(
                "Display Order",
                min_value=1,
                value=1
            )

            active = st.checkbox(
                "Active",
                value=True
            )

            submit = st.form_submit_button(
                "➕ Add Social Link"
            )

            if submit:

                if not platform.strip():
                    st.error(
                        "Platform is required."
                    )

                elif not label.strip():
                    st.error(
                        "Label is required."
                    )

                elif not url.strip():
                    st.error(
                        "URL is required."
                    )

                else:

                    if (
                        not url.startswith("mailto:")
                        and not is_valid_url(url)
                    ):
                        st.error(
                            "Invalid URL."
                        )

                    else:

                        add_social_link(
                            {
                                "platform": platform.strip(),
                                "label": label.strip(),
                                "url": url.strip(),
                                "display_order": display_order,
                                "active": active
                            }
                        )

                        st.success(
                            "Social link added."
                        )

                        st.rerun()

    # ======================================
    # REVIEWS ADMIN
    # ======================================
    with tabs[7]:

        st.subheader(
            "⭐ Review Management"
        )

        reviews = get_all_reviews()

        if not reviews:

            st.info(
                "No reviews submitted yet."
            )

        else:

            for review in reviews:

                review_id = review["id"]
                approved = review.get(
                    "is_approved",
                    False
                )

                st.markdown(
                    f"""
                    <div class="review-card">

                        <h3>
                            {safe_text(review.get("name", ""))}
                        </h3>

                        <p style="color:#60a5fa;">
                            {safe_text(review.get("role", ""))}
                        </p>

                        <p>
                            {"⭐" * int(review.get("rating", 5))}
                        </p>

                        <p style="
                            color:#cbd5e1;
                            line-height:1.6;
                        ">
                            {safe_text(review.get("comment", ""))}
                        </p>

                        <p>
                            Status:
                            <strong>
                                {
                                    "Approved"
                                    if approved
                                    else "Pending"
                                }
                            </strong>
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                c1, c2 = st.columns(2)

                with c1:

                    if not approved:

                        if st.button(
                            "✅ Approve",
                            key=f"approve_{review_id}"
                        ):

                            approve_review(
                                review_id
                            )

                            st.success(
                                "Review approved."
                            )

                            st.rerun()

                with c2:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_review_{review_id}"
                    ):

                        delete_review(
                            review_id
                        )

                        st.success(
                            "Review deleted."
                        )

                        st.rerun()


# ==========================================
# MAIN APP
# ==========================================
def main():

    pages = {
        "Home": render_home,
        "Skills": render_skills,
        "Projects": render_projects,
        "Services": render_services,
        "Experience": render_experience,
        "Reviews": render_reviews,
        "Contact": render_contact,
        "Admin": render_admin
    }

    if (
        "nav" not in st.session_state
        or st.session_state["nav"] not in pages
    ):
        st.session_state["nav"] = "Home"

    page_keys = list(pages.keys())

    current_index = page_keys.index(
        st.session_state["nav"]
    )

    st.sidebar.title("🛡️ Navigation")

    selection = st.sidebar.radio(
        "Go to",
        page_keys,
        index=current_index
    )

    st.session_state["nav"] = selection

    pages[selection]()


# ==========================================
# RUN
# ==========================================
if __name__ == "__main__":
    main()

import hashlib
import hmac
import secrets
from dataclasses import dataclass

import streamlit as st
import streamlit.components.v1 as components

ROLES = [
    "super_admin",
    "admin",
    "cs_lead",
    "cs_agent",
    "affiliate_manager",
    "it",
    "engineering",
    "viewer",
]

ROLE_RANK = {role: index for index, role in enumerate(ROLES)}


@dataclass
class User:
    email: str
    full_name: str
    role: str
    password_hash: str
    salt: str
    iterations: int = 210_000


def pbkdf2_hash(password: str, salt: str, iterations: int = 210_000) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), iterations).hex()


def make_user(email: str, full_name: str, role: str, plain_password: str) -> User:
    salt = secrets.token_hex(16)
    return User(
        email=email,
        full_name=full_name,
        role=role,
        salt=salt,
        password_hash=pbkdf2_hash(plain_password, salt),
    )


def verify_password(user: User, password: str) -> bool:
    expected = pbkdf2_hash(password, user.salt, user.iterations)
    return hmac.compare_digest(user.password_hash, expected)


DEMO_USERS = {
    "owner@withelara.com": make_user("owner@withelara.com", "Platform Owner", "super_admin", "demo1234"),
    "salma@withelara.com": make_user("salma@withelara.com", "Salma", "cs_lead", "demo1234"),
    "roaa@withelara.com": make_user("roaa@withelara.com", "Roaa", "cs_agent", "demo1234"),
    "shelby@withelara.com": make_user("shelby@withelara.com", "Shelby", "affiliate_manager", "demo1234"),
    "info@withelara.com": make_user("info@withelara.com", "Info Inbox", "admin", "demo1234"),
}

RESOURCES = [
    {
        "name": "Intake Questionnaire",
        "url": "https://docs.google.com/spreadsheets/d/1Lt0roLGLJocjb5r7qkm91Z1IBBUDo0u2K8uyk-2I22Q/edit?pli=1&gid=132844709#gid=132844709",
        "embed_url": "https://docs.google.com/spreadsheets/d/1Lt0roLGLJocjb5r7qkm91Z1IBBUDo0u2K8uyk-2I22Q/preview",
        "category": "CS Workflow",
        "min_role": "cs_agent",
        "desc": "Live intake sheet for onboarding and case kickoff.",
    },
    {
        "name": "Meds Storage Instructions",
        "url": "https://docs.google.com/spreadsheets/d/1BIIDiCuqwuEiQED-yErBATd2W3rwQt3EESZ3INp4SFk/edit?gid=1979052169#gid=1979052169",
        "embed_url": "https://docs.google.com/spreadsheets/d/1BIIDiCuqwuEiQED-yErBATd2W3rwQt3EESZ3INp4SFk/preview",
        "category": "CS Workflow",
        "min_role": "cs_agent",
        "desc": "Medication handling and storage rules for CS operations.",
    },
    {
        "name": "FAQ",
        "url": "https://docs.google.com/document/d/1HW-0Ubc2IWQ34enuQB9QqG7iVvSYCdDn/edit",
        "embed_url": "https://docs.google.com/document/d/1HW-0Ubc2IWQ34enuQB9QqG7iVvSYCdDn/preview",
        "category": "Knowledge Base",
        "min_role": "cs_agent",
        "desc": "Frequently asked questions for customer support.",
    },
    {
        "name": "Med Training",
        "url": "https://docs.google.com/document/d/15G0Dq_PBOo45XsXVCJdWxlfIC5Ab2XbZ/edit",
        "embed_url": "https://docs.google.com/document/d/15G0Dq_PBOo45XsXVCJdWxlfIC5Ab2XbZ/preview",
        "category": "Knowledge Base",
        "min_role": "cs_agent",
        "desc": "Medication training and internal playbook notes.",
    },
    {
        "name": "Communication Standards",
        "url": "https://docs.google.com/document/d/10NxCAFk_i_6vao90B0M-i-RU7bmJE_TsKVjAcBtM-G4/edit?tab=t.0",
        "embed_url": "https://docs.google.com/document/d/10NxCAFk_i_6vao90B0M-i-RU7bmJE_TsKVjAcBtM-G4/preview",
        "category": "Knowledge Base",
        "min_role": "cs_agent",
        "desc": "Tone, quality bar, and communication guardrails.",
    },
    {
        "name": "Upsell Playbook",
        "url": "https://docs.google.com/document/d/1LzTseXMGf6ApXwkZ3LG77S1-s78UOZSq/edit",
        "embed_url": "https://docs.google.com/document/d/1LzTseXMGf6ApXwkZ3LG77S1-s78UOZSq/preview",
        "category": "Sales",
        "min_role": "cs_agent",
        "desc": "Approved scripts and prompts for upsell opportunities.",
    },
    {
        "name": "Pricing",
        "url": "https://affiliate.withelara.com/resources",
        "embed_url": "https://affiliate.withelara.com/resources",
        "category": "Sales",
        "min_role": "affiliate_manager",
        "desc": "Pricing and affiliate-facing resource center.",
    },
]


def can_access(user_role: str, min_role: str) -> bool:
    return ROLE_RANK[user_role] <= ROLE_RANK[min_role]


def inject_styles() -> None:
    st.markdown(
        """
        <style>
          .stApp {background: radial-gradient(1200px 600px at -10% -20%, #232935, #0f1115 60%);}
          .block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1180px;}
          .apple-hero {
            background: linear-gradient(135deg, rgba(255,255,255,.15), rgba(255,255,255,.03));
            border: 1px solid rgba(255,255,255,.18);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 20px 60px rgba(0,0,0,.28);
            margin-bottom: 1rem;
          }
          .apple-hero h1 {font-size: 2.05rem; letter-spacing: -0.03em; margin: 0; color: #f5f5f7; font-weight: 640;}
          .apple-hero p {margin: .35rem 0 0; color: #c8c8cf; font-size: 1rem;}
          .toolbar {display:flex; gap:.55rem; flex-wrap:wrap; margin-top:.9rem;}
          .pill {display:inline-flex; align-items:center; gap:.35rem; border-radius:999px; border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.06); color:#e6e6ee; padding:.32rem .7rem; font-size:.8rem;}
          .glass {
            border: 1px solid rgba(255,255,255,.12);
            background: linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,.02));
            border-radius: 18px;
            padding: .95rem;
          }
          .tool {border-left: 4px solid #4ade80; margin:.5rem 0; padding:.75rem .9rem; border-radius:12px; background:rgba(255,255,255,.04);}
          .tool.locked {border-left-color:#fb7185;}
          .tool h4 {margin:.05rem 0; color:#f3f4f6; font-weight:600;}
          .tool p {margin:.1rem 0 0; color:#aeb1bd; font-size:.88rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str, role: str | None = None) -> None:
    badges = ""
    if role:
        badges = f'<div class="toolbar"><span class="pill">Role: {role}</span><span class="pill">Mode: Unified Workspace</span><span class="pill">Design: Apple-style</span></div>'
    st.markdown(f'<div class="apple-hero"><h1>{title}</h1><p>{subtitle}</p>{badges}</div>', unsafe_allow_html=True)


def show_login() -> None:
    inject_styles()
    render_hero("Unified Role-Based Hub", "Single login for website, extension, and admin workflows.")
    col1, col2 = st.columns([1.8, 1])

    with col1:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        with st.form("login"):
            email = st.text_input("Email").strip().lower()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in")
        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            user = DEMO_USERS.get(email)
            if user and verify_password(user, password):
                st.session_state.user = user
                st.rerun()
            st.error("Invalid credentials")

    with col2:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown("#### Demo access")
        st.caption("Password for all demo accounts")
        st.code("demo1234")
        st.caption("owner@withelara.com")
        st.caption("info@withelara.com")
        st.markdown('</div>', unsafe_allow_html=True)


def show_workspace(user: User) -> None:
    inject_styles()
    render_hero(f"Welcome, {user.full_name}", "Internal control center for CS, affiliate, and leadership operations.", user.role)

    with st.sidebar:
        st.subheader("Session")
        st.write(user.email)
        st.write(f"Role: {user.role}")
        if st.button("Log out"):
            st.session_state.pop("user", None)
            st.rerun()

    tabs = st.tabs(["Dashboard", "Resources Webview", "System"])

    with tabs[0]:
        st.subheader("Access Matrix")
        tools = [
            ("Snippets", "Use and manage approved snippets.", "cs_agent"),
            ("Ticketing", "Create and triage operations tickets.", "cs_agent"),
            ("Admin Dashboard", "Manage users, approvals, and settings.", "admin"),
            ("Leadership Analytics", "Read-only leadership metrics and visibility.", "viewer"),
            ("Contracts Calculator", "Affiliate pricing and contract workflows.", "affiliate_manager"),
        ]
        for name, desc, min_role in tools:
            allowed = can_access(user.role, min_role)
            cls = "tool" if allowed else "tool locked"
            state = "Accessible" if allowed else "Locked"
            st.markdown(
                f'<div class="{cls}"><h4>{name} · {state}</h4><p>{desc} (min role: {min_role})</p></div>',
                unsafe_allow_html=True,
            )

    with tabs[1]:
        st.subheader("Embedded Resources")
        visible = [r for r in RESOURCES if can_access(user.role, r["min_role"])]
        selection = st.selectbox("Select resource", [r["name"] for r in visible])
        selected = next(r for r in visible if r["name"] == selection)

        meta1, meta2 = st.columns([3, 2])
        with meta1:
            st.markdown(f"### {selected['name']}")
            st.caption(selected["desc"])
        with meta2:
            st.caption(f"Category: {selected['category']}")
            st.caption(f"Required role: {selected['min_role']}")

        components.iframe(selected["embed_url"], height=780, scrolling=True)
        st.caption("If this content is blocked by provider iframe policy, use direct fallback below.")
        st.link_button("Open fallback page", selected["url"])

    with tabs[2]:
        st.subheader("Platform modules")
        st.code(
            "\n".join(
                [
                    "database/01_unified_schema.sql",
                    "database/02_seed_initial_users.sql",
                    "database/03_optional_migrate_data.sql",
                    "extension/manifest.json",
                    "extension/popup.html",
                    "extension/popup.js",
                ]
            )
        )


st.set_page_config(page_title="Unified Hub", page_icon="🧩", layout="wide")

if "user" not in st.session_state:
    show_login()
else:
    show_workspace(st.session_state.user)

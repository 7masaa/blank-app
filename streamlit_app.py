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
        .hero {padding: 1.25rem 1.5rem; border-radius: 16px; background: linear-gradient(120deg,#10223d,#1f3f73); color: white; margin-bottom: 1rem;}
        .hero h1 {margin: 0; font-size: 2.2rem;}
        .hero p {margin: .4rem 0 0 0; opacity: .9;}
        .card {padding: 1rem; border: 1px solid rgba(160,160,180,.35); border-radius: 14px; background: rgba(18,22,34,.55); min-height: 160px;}
        .badge {display:inline-block; padding: .2rem .55rem; border-radius: 999px; background: rgba(75,155,255,.2); color: #7fb6ff; font-size: .8rem; margin-bottom: .5rem;}
        .tool {padding: .75rem 1rem; border-radius: 12px; margin: .4rem 0; background: rgba(20,26,42,.5);}
        .ok {border-left: 4px solid #20c997;}
        .lock {border-left: 4px solid #ff7676;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_login() -> None:
    inject_styles()
    st.markdown('<div class="hero"><h1>Unified Role-Based Hub</h1><p>Single login for website, extension, and admin workflows.</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("login"):
            email = st.text_input("Email").strip().lower()
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in")

        if submitted:
            user = DEMO_USERS.get(email)
            if user and verify_password(user, password):
                st.session_state.user = user
                st.rerun()
            st.error("Invalid credentials")
    with col2:
        st.info("Demo password: `demo1234`")
        st.caption("Try: owner@withelara.com or info@withelara.com")


def show_workspace(user: User) -> None:
    inject_styles()
    st.markdown(
        f'<div class="hero"><h1>Welcome, {user.full_name}</h1><p>Role: {user.role} • Unified workspace active</p></div>',
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.subheader("Session")
        st.write(user.email)
        st.write(f"Role: {user.role}")
        if st.button("Log out"):
            st.session_state.pop("user", None)
            st.rerun()

    tabs = st.tabs(["Dashboard", "Resources Webview", "System"])

    with tabs[0]:
        st.subheader("Role-gated tools")
        tools = [
            ("Snippets", "cs_agent"),
            ("Ticketing", "cs_agent"),
            ("Admin Dashboard", "admin"),
            ("Leadership Analytics", "viewer"),
            ("Contracts Calculator", "affiliate_manager"),
        ]
        for tool, min_role in tools:
            allowed = can_access(user.role, min_role)
            css = "ok" if allowed else "lock"
            label = "Accessible" if allowed else "Locked"
            st.markdown(
                f'<div class="tool {css}"><strong>{tool}</strong> • {label} <span style="opacity:.7">(min role: {min_role})</span></div>',
                unsafe_allow_html=True,
            )

    with tabs[1]:
        st.subheader("Embedded resources (webview)")
        visible = [r for r in RESOURCES if can_access(user.role, r["min_role"])]
        names = [r["name"] for r in visible]
        chosen_name = st.selectbox("Choose resource", names, index=0)
        selected = next(r for r in visible if r["name"] == chosen_name)

        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"### {selected['name']}")
            st.caption(selected["desc"])
        with c2:
            st.markdown(f"**Category:** {selected['category']}")
            st.markdown(f"**Min role:** `{selected['min_role']}`")

        st.caption("If a provider blocks iframe rendering, use fallback open button below.")
        components.iframe(selected["embed_url"], height=760, scrolling=True)
        st.link_button("Open direct page (fallback)", selected["url"])

    with tabs[2]:
        st.subheader("Implemented modules")
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

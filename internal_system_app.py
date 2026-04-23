import hashlib
import hmac
import secrets
from dataclasses import dataclass

import streamlit as st

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
}

RESOURCES = [
    {
        "name": "Intake Questionnaire",
        "url": "https://docs.google.com/spreadsheets/d/1Lt0roLGLJocjb5r7qkm91Z1IBBUDo0u2K8uyk-2I22Q/edit?pli=1&gid=132844709#gid=132844709",
        "category": "CS Workflow",
        "min_role": "cs_agent",
    },
    {
        "name": "Meds Storage Instructions",
        "url": "https://docs.google.com/spreadsheets/d/1BIIDiCuqwuEiQED-yErBATd2W3rwQt3EESZ3INp4SFk/edit?gid=1979052169#gid=1979052169",
        "category": "CS Workflow",
        "min_role": "cs_agent",
    },
    {
        "name": "FAQ",
        "url": "https://docs.google.com/document/d/1HW-0Ubc2IWQ34enuQB9QqG7iVvSYCdDn/edit",
        "category": "Knowledge Base",
        "min_role": "cs_agent",
    },
    {
        "name": "Med Training",
        "url": "https://docs.google.com/document/d/15G0Dq_PBOo45XsXVCJdWxlfIC5Ab2XbZ/edit",
        "category": "Knowledge Base",
        "min_role": "cs_agent",
    },
    {
        "name": "Communication Standards",
        "url": "https://docs.google.com/document/d/10NxCAFk_i_6vao90B0M-i-RU7bmJE_TsKVjAcBtM-G4/edit?tab=t.0",
        "category": "Knowledge Base",
        "min_role": "cs_agent",
    },
    {
        "name": "Upsell Playbook",
        "url": "https://docs.google.com/document/d/1LzTseXMGf6ApXwkZ3LG77S1-s78UOZSq/edit",
        "category": "Sales",
        "min_role": "cs_agent",
    },
    {
        "name": "Pricing",
        "url": "https://affiliate.withelara.com/resources",
        "category": "Sales",
        "min_role": "affiliate_manager",
    },
]


def can_access(user_role: str, min_role: str) -> bool:
    return ROLE_RANK[user_role] <= ROLE_RANK[min_role]


def show_login() -> None:
    st.title("Unified Role-Based Hub")
    st.caption("Single login for website + extension + admin workflows.")
    with st.form("login"):
        email = st.text_input("Email").strip().lower()
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")

    st.info("Demo users all use password: demo1234")

    if submitted:
        user = DEMO_USERS.get(email)
        if user and verify_password(user, password):
            st.session_state.user = user
            st.rerun()
        st.error("Invalid credentials")


def show_workspace(user: User) -> None:
    st.title("Unified Role-Based Hub")
    st.success(f"Signed in as {user.full_name} ({user.role})")

    with st.sidebar:
        st.header("Session")
        st.write(user.email)
        if st.button("Log out"):
            st.session_state.pop("user", None)
            st.rerun()

    tabs = st.tabs(["Workspace", "CS Resources", "Architecture"])

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
            icon = "✅" if allowed else "🔒"
            st.write(f"{icon} {tool} (min role: {min_role})")

    with tabs[1]:
        st.subheader("Customer Support resources")
        st.caption("Google Docs/Sheets are linked as cards and open in a new tab.")
        visible = [r for r in RESOURCES if can_access(user.role, r["min_role"])]
        by_category = {}
        for item in visible:
            by_category.setdefault(item["category"], []).append(item)

        for category, entries in by_category.items():
            st.markdown(f"### {category}")
            for entry in entries:
                st.markdown(f"- [{entry['name']}]({entry['url']})")

    with tabs[2]:
        st.subheader("Implemented foundation")
        st.code(
            "\n".join(
                [
                    "database/01_unified_schema.sql",
                    "database/02_seed_initial_users.sql",
                    "database/03_optional_migrate_data.sql",
                    "extension/manifest.json",
                    "extension/popup.html",
                ]
            )
        )


st.set_page_config(page_title="Unified Hub", page_icon="🧩", layout="wide")

if "user" not in st.session_state:
    show_login()
else:
    show_workspace(st.session_state.user)

import streamlit as st
import hashlib
import time
import pandas as pd

# Function to generate hash for each entry
def generate_hash(entry):
    entry_string = f"{entry['entry_no']}{entry['name']}{entry['contact']}{entry['package']}{entry['months']}{entry['timestamp']}{entry['previous_hash']}"
    return hashlib.sha256(entry_string.encode()).hexdigest()

# Function to create a new ledger entry
def create_ledger_entry(entry_no, name, contact, package, months, previous_hash):
    return {
        "entry_no": entry_no,
        "name": name,
        "contact": contact,
        "package": package,
        "months": months,
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "previous_hash": previous_hash
    }

# Initialize session state for the ledger
if 'ledger' not in st.session_state:
    genesis_entry = create_ledger_entry(0, "Genesis", "0000000000", "None", 0, "0")
    st.session_state.ledger = [genesis_entry]

# Function to add member to the ledger
def add_member(name, contact, package, months):
    previous_entry = st.session_state.ledger[-1]
    new_entry_no = previous_entry["entry_no"] + 1
    new_hash = generate_hash(previous_entry)

    new_entry = create_ledger_entry(new_entry_no, name, contact, package, months, new_hash)
    st.session_state.ledger.append(new_entry)

# --- Streamlit UI ---
st.title("🏋️ Gym Membership Ledger")
st.subheader("➕ Add New Member Entry")

with st.form("member_form"):
    name = st.text_input("Member Name")
    contact = st.text_input("Contact Number")
    package = st.selectbox("Select Package", ["Yoga + Gym", "Personal Trainer", "Swimming Only", "Zumba", "Crossfit", "Monthly Plan", "Annual Plan"])
    months = st.number_input("Membership Duration (in months)", min_value=1, max_value=24, step=1)

    submitted = st.form_submit_button("Add Member")
    if submitted:
        if name and contact:
            add_member(name, contact, package, months)
            st.success(f"Member '{name}' added to the ledger!")
        else:
            st.warning("Please fill in all required fields.")

st.subheader("📋 Ledger Records")

# Display the ledger as a DataFrame
df = pd.DataFrame(st.session_state.ledger)
st.dataframe(df[["entry_no", "name", "contact", "package", "months", "timestamp", "previous_hash"]], use_container_width=True)

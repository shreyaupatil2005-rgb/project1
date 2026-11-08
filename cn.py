import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="AI Network Anomaly Detection",
    page_icon="🌐",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🌐 AI-Based Network Anomaly Detection System")
st.write(
    "An AI-powered system that analyzes network traffic "
    "and identifies unusual network activity."
)

# ---------------- GENERATE DATA ----------------
np.random.seed(42)

normal = pd.DataFrame({
    "Packet Size": np.random.normal(500, 80, 500),
    "Packet Rate": np.random.normal(50, 8, 500),
    "Connection Duration": np.random.normal(30, 5, 500),
    "Failed Connections": np.random.normal(2, 1, 500)
})

anomaly = pd.DataFrame({
    "Packet Size": np.random.normal(1500, 200, 50),
    "Packet Rate": np.random.normal(150, 20, 50),
    "Connection Duration": np.random.normal(5, 1, 50),
    "Failed Connections": np.random.normal(15, 3, 50)
})

data = pd.concat([normal, anomaly], ignore_index=True)

# Make sure values are positive
data["Packet Size"] = data["Packet Size"].clip(lower=1)
data["Packet Rate"] = data["Packet Rate"].clip(lower=1)
data["Connection Duration"] = data["Connection Duration"].clip(lower=1)
data["Failed Connections"] = data["Failed Connections"].clip(lower=0)

# ---------------- MACHINE LEARNING ----------------
features = [
    "Packet Size",
    "Packet Rate",
    "Connection Duration",
    "Failed Connections"
]

X = data[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    contamination=0.09,
    random_state=42
)

model.fit(X_scaled)

prediction = model.predict(X_scaled)

data["Status"] = np.where(
    prediction == -1,
    "Anomaly",
    "Normal"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Controls")

show_anomalies = st.sidebar.checkbox(
    "Show only anomalies",
    value=False
)

# ---------------- STATISTICS ----------------
total = len(data)
normal_count = len(data[data["Status"] == "Normal"])
anomaly_count = len(data[data["Status"] == "Anomaly"])

st.subheader("📊 Network Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Traffic", total)

with col2:
    st.metric("Normal Traffic", normal_count)

with col3:
    st.metric("Anomalies", anomaly_count)

with col4:
    percentage = (anomaly_count / total) * 100
    st.metric("Anomaly Rate", f"{percentage:.1f}%")

# ---------------- ALERT ----------------
if anomaly_count > 0:
    st.warning(
        f"🚨 Warning: {anomaly_count} unusual network activities detected!"
    )
else:
    st.success("✅ Network traffic appears normal.")

st.divider()

# ---------------- DATA TABLE ----------------
st.subheader("📋 Network Traffic Analysis")

if show_anomalies:
    display_data = data[data["Status"] == "Anomaly"]
else:
    display_data = data

st.dataframe(
    display_data,
    use_container_width=True,
    height=350
)

# ---------------- ANOMALY TABLE ----------------
st.subheader("🚨 Detected Anomalies")

anomalies = data[data["Status"] == "Anomaly"]

st.dataframe(
    anomalies,
    use_container_width=True,
    height=250
)

# ---------------- GRAPH 1 ----------------
st.subheader("📈 Packet Size Analysis")

fig1, ax1 = plt.subplots(figsize=(10, 4))

ax1.hist(
    data[data["Status"] == "Normal"]["Packet Size"],
    bins=25,
    alpha=0.7,
    label="Normal"
)

ax1.hist(
    data[data["Status"] == "Anomaly"]["Packet Size"],
    bins=25,
    alpha=0.7,
    label="Anomaly"
)

ax1.set_xlabel("Packet Size")
ax1.set_ylabel("Number of Connections")
ax1.set_title("Normal vs Anomalous Packet Size")
ax1.legend()

st.pyplot(fig1)

# ---------------- GRAPH 2 ----------------
st.subheader("📊 Network Traffic Pattern")

fig2, ax2 = plt.subplots(figsize=(10, 4))

normal_data = data[data["Status"] == "Normal"]
anomaly_data = data[data["Status"] == "Anomaly"]

ax2.scatter(
    normal_data["Packet Rate"],
    normal_data["Packet Size"],
    alpha=0.5,
    label="Normal"
)

ax2.scatter(
    anomaly_data["Packet Rate"],
    anomaly_data["Packet Size"],
    alpha=0.8,
    label="Anomaly"
)

ax2.set_xlabel("Packet Rate")
ax2.set_ylabel("Packet Size")
ax2.set_title("Network Traffic Classification")
ax2.legend()

st.pyplot(fig2)

# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "AI-Based Network Anomaly Detection System | "
    "Python • Scikit-learn • Streamlit"
)
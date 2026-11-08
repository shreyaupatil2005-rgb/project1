import streamlit as st
import psutil
import pandas as pd
import time
from datetime import datetime


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Network Traffic Analyzer",
    page_icon="🌐",
    layout="wide"
)


# =====================================================
# TITLE
# =====================================================

st.title("🌐 Network Traffic Analyzer")

st.write(
    "Monitor network interfaces, data transfer, "
    "upload speed, download speed, and network activity."
)


# =====================================================
# FUNCTIONS
# =====================================================

def bytes_to_mb(value):
    """Convert bytes to megabytes."""
    return value / (1024 * 1024)


def bytes_to_gb(value):
    """Convert bytes to gigabytes."""
    return value / (1024 * 1024 * 1024)


def get_network_data():
    """Get current network statistics."""

    stats = psutil.net_io_counters(pernic=True)

    rows = []

    for interface, data in stats.items():

        rows.append({
            "Interface": interface,
            "Bytes Sent": data.bytes_sent,
            "Bytes Received": data.bytes_recv,
            "Packets Sent": data.packets_sent,
            "Packets Received": data.packets_recv,
            "Errors In": data.errin,
            "Errors Out": data.errout,
            "Dropped In": data.dropin,
            "Dropped Out": data.dropout
        })

    return pd.DataFrame(rows)


# =====================================================
# INITIAL NETWORK DATA
# =====================================================

current_data = get_network_data()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("⚙️ Settings")

refresh_time = st.sidebar.slider(
    "Refresh interval (seconds)",
    min_value=1,
    max_value=10,
    value=2
)

show_details = st.sidebar.checkbox(
    "Show detailed interface data",
    value=True
)


# =====================================================
# TOTAL NETWORK STATISTICS
# =====================================================

total_sent = current_data["Bytes Sent"].sum()
total_received = current_data["Bytes Received"].sum()

total_packets_sent = current_data["Packets Sent"].sum()
total_packets_received = current_data["Packets Received"].sum()

total_errors = (
    current_data["Errors In"].sum()
    + current_data["Errors Out"].sum()
)

total_dropped = (
    current_data["Dropped In"].sum()
    + current_data["Dropped Out"].sum()
)


# =====================================================
# MAIN METRICS
# =====================================================

st.subheader("📊 Network Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📥 Data Received",
        f"{bytes_to_gb(total_received):.2f} GB"
    )

with col2:
    st.metric(
        "📤 Data Sent",
        f"{bytes_to_gb(total_sent):.2f} GB"
    )

with col3:
    st.metric(
        "📥 Packets Received",
        f"{total_packets_received:,}"
    )

with col4:
    st.metric(
        "📤 Packets Sent",
        f"{total_packets_sent:,}"
    )


# =====================================================
# NETWORK STATUS
# =====================================================

st.divider()

st.subheader("🟢 Network Status")

if len(current_data) > 0:

    st.success(
        f"Network monitoring is active. "
        f"{len(current_data)} network interface(s) detected."
    )

else:

    st.warning(
        "No network interfaces were detected."
    )


# =====================================================
# SPEED MEASUREMENT
# =====================================================

st.subheader("⚡ Current Network Speed")

speed_placeholder = st.empty()

if "previous_sent" not in st.session_state:
    st.session_state.previous_sent = total_sent
    st.session_state.previous_received = total_received
    st.session_state.previous_time = time.time()

else:

    current_time = time.time()

    time_difference = (
        current_time - st.session_state.previous_time
    )

    if time_difference > 0:

        upload_speed = (
            total_sent - st.session_state.previous_sent
        ) / time_difference

        download_speed = (
            total_received
            - st.session_state.previous_received
        ) / time_difference

        upload_mbps = (
            upload_speed * 8 / (1024 * 1024)
        )

        download_mbps = (
            download_speed * 8 / (1024 * 1024)
        )

        speed_col1, speed_col2 = speed_placeholder.columns(2)

        with speed_col1:

            st.metric(
                "⬇️ Download Speed",
                f"{download_mbps:.2f} Mbps"
            )

        with speed_col2:

            st.metric(
                "⬆️ Upload Speed",
                f"{upload_mbps:.2f} Mbps"
            )

        st.session_state.previous_sent = total_sent
        st.session_state.previous_received = total_received
        st.session_state.previous_time = current_time


# =====================================================
# INTERFACE DATA
# =====================================================

if show_details:

    st.divider()

    st.subheader("📋 Network Interface Details")

    display_data = current_data.copy()

    display_data["Sent (MB)"] = (
        display_data["Bytes Sent"]
        / (1024 * 1024)
    ).round(2)

    display_data["Received (MB)"] = (
        display_data["Bytes Received"]
        / (1024 * 1024)
    ).round(2)

    display_data = display_data[
        [
            "Interface",
            "Sent (MB)",
            "Received (MB)",
            "Packets Sent",
            "Packets Received",
            "Errors In",
            "Errors Out",
            "Dropped In",
            "Dropped Out"
        ]
    ]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# TRAFFIC GRAPH
# =====================================================

st.divider()

st.subheader("📈 Network Traffic")

chart_data = pd.DataFrame({
    "Traffic": [
        bytes_to_mb(total_received),
        bytes_to_mb(total_sent)
    ]
}, index=[
    "Received",
    "Sent"
])

st.bar_chart(chart_data)


# =====================================================
# PACKET INFORMATION
# =====================================================

st.subheader("📦 Packet Information")

packet_col1, packet_col2, packet_col3 = st.columns(3)

with packet_col1:

    st.metric(
        "Packets Received",
        f"{total_packets_received:,}"
    )

with packet_col2:

    st.metric(
        "Packets Sent",
        f"{total_packets_sent:,}"
    )

with packet_col3:

    st.metric(
        "Total Packets",
        f"{total_packets_received + total_packets_sent:,}"
    )


# =====================================================
# ERRORS AND DROPPED PACKETS
# =====================================================

st.subheader("⚠️ Network Errors")

error_col1, error_col2 = st.columns(2)

with error_col1:

    st.metric(
        "Network Errors",
        f"{total_errors:,}"
    )

with error_col2:

    st.metric(
        "Dropped Packets",
        f"{total_dropped:,}"
    )


# =====================================================
# LAST UPDATED
# =====================================================

st.divider()

st.caption(
    "Last updated: "
    + datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

st.caption(
    "Network Traffic Analyzer | "
    "Python + Streamlit + Psutil"
)


# =====================================================
# REFRESH BUTTON
# =====================================================

if st.button("🔄 Refresh Network Data"):

    st.rerun()
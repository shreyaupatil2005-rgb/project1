import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pandas as pd


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Network Topology Visualizer",
    page_icon="🌐",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "devices" not in st.session_state:
    st.session_state.devices = [
        {"name": "Router", "type": "Router"},
        {"name": "Switch", "type": "Switch"},
        {"name": "PC-1", "type": "Computer"},
        {"name": "PC-2", "type": "Computer"},
        {"name": "Server", "type": "Server"}
    ]

if "connections" not in st.session_state:
    st.session_state.connections = [
        ("Router", "Switch"),
        ("Switch", "PC-1"),
        ("Switch", "PC-2"),
        ("Switch", "Server")
    ]


# =========================================================
# FUNCTIONS
# =========================================================

def get_device_names():
    return [device["name"] for device in st.session_state.devices]


def device_exists(name):
    return name in get_device_names()


def draw_topology():

    devices = st.session_state.devices
    connections = st.session_state.connections

    if len(devices) == 0:
        st.info("No devices available. Add a device from the sidebar.")
        return

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    # -----------------------------------------------------
    # Arrange devices
    # -----------------------------------------------------

    positions = {}

    # Router
    routers = [d for d in devices if d["type"] == "Router"]

    # Switches
    switches = [d for d in devices if d["type"] == "Switch"]

    # Servers
    servers = [d for d in devices if d["type"] == "Server"]

    # Computers
    computers = [d for d in devices if d["type"] == "Computer"]

    # Other devices
    others = [
        d for d in devices
        if d["type"] not in ["Router", "Switch", "Server", "Computer"]
    ]

    # Place routers at top
    for i, device in enumerate(routers):
        x = 5 + (i - (len(routers) - 1) / 2) * 2
        positions[device["name"]] = (x, 8.5)

    # Place switches
    for i, device in enumerate(switches):
        x = 5 + (i - (len(switches) - 1) / 2) * 3
        positions[device["name"]] = (x, 6.5)

    # Place computers
    for i, device in enumerate(computers):
        x = 1.5 + i * (7 / max(1, len(computers) - 1))
        if len(computers) == 1:
            x = 5
        positions[device["name"]] = (x, 3)

    # Place servers
    for i, device in enumerate(servers):
        x = 3 + i * 4
        positions[device["name"]] = (x, 1)

    # Place other devices
    for i, device in enumerate(others):
        x = 2 + i * 2
        positions[device["name"]] = (x, 5)

    # -----------------------------------------------------
    # Draw connections first
    # -----------------------------------------------------

    for device1, device2 in connections:

        if device1 in positions and device2 in positions:

            x1, y1 = positions[device1]
            x2, y2 = positions[device2]

            ax.plot(
                [x1, x2],
                [y1, y2],
                linewidth=2
            )

    # -----------------------------------------------------
    # Draw devices
    # -----------------------------------------------------

    device_styles = {
        "Router": {
            "marker": "s",
            "size": 900,
            "color": "#4CAF50"
        },
        "Switch": {
            "marker": "s",
            "size": 900,
            "color": "#2196F3"
        },
        "Computer": {
            "marker": "o",
            "size": 750,
            "color": "#FF9800"
        },
        "Server": {
            "marker": "D",
            "size": 800,
            "color": "#9C27B0"
        }
    }

    for device in devices:

        name = device["name"]
        device_type = device["type"]

        x, y = positions[name]

        style = device_styles.get(
            device_type,
            {
                "marker": "o",
                "size": 700,
                "color": "#607D8B"
            }
        )

        ax.scatter(
            x,
            y,
            s=style["size"],
            marker=style["marker"],
            color=style["color"],
            edgecolors="black",
            linewidths=1.5,
            zorder=3
        )

        ax.text(
            x,
            y - 0.65,
            name,
            ha="center",
            va="top",
            fontsize=10,
            fontweight="bold"
        )

        ax.text(
            x,
            y + 0.65,
            device_type,
            ha="center",
            va="bottom",
            fontsize=8
        )

    ax.set_title(
        "Network Topology",
        fontsize=18,
        fontweight="bold"
    )

    st.pyplot(fig)


# =========================================================
# HEADER
# =========================================================

st.title("🌐 Network Topology Visualizer")

st.write(
    "Visualize routers, switches, computers, servers, "
    "and their network connections."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Network Controls")


# =========================================================
# ADD DEVICE
# =========================================================

st.sidebar.subheader("➕ Add Device")

device_name = st.sidebar.text_input(
    "Device Name",
    placeholder="Example: PC-3"
)

device_type = st.sidebar.selectbox(
    "Device Type",
    [
        "Router",
        "Switch",
        "Computer",
        "Server"
    ]
)

if st.sidebar.button("Add Device", use_container_width=True):

    device_name = device_name.strip()

    if device_name == "":
        st.sidebar.error("Please enter a device name.")

    elif device_exists(device_name):
        st.sidebar.error("Device already exists.")

    else:

        st.session_state.devices.append(
            {
                "name": device_name,
                "type": device_type
            }
        )

        st.sidebar.success(
            f"{device_name} added successfully."
        )


# =========================================================
# ADD CONNECTION
# =========================================================

st.sidebar.subheader("🔗 Add Connection")

names = get_device_names()

if len(names) >= 2:

    device1 = st.sidebar.selectbox(
        "From",
        names,
        key="connection_from"
    )

    device2 = st.sidebar.selectbox(
        "To",
        names,
        key="connection_to"
    )

    if st.sidebar.button(
        "Connect Devices",
        use_container_width=True
    ):

        if device1 == device2:

            st.sidebar.error(
                "A device cannot connect to itself."
            )

        elif (
            device1,
            device2
        ) in st.session_state.connections or (
            device2,
            device1
        ) in st.session_state.connections:

            st.sidebar.warning(
                "These devices are already connected."
            )

        else:

            st.session_state.connections.append(
                (device1, device2)
            )

            st.sidebar.success(
                "Devices connected successfully."
            )

else:

    st.sidebar.info(
        "Add at least two devices."
    )


# =========================================================
# REMOVE DEVICE
# =========================================================

st.sidebar.subheader("🗑️ Remove Device")

if names:

    remove_device = st.sidebar.selectbox(
        "Select Device",
        names,
        key="remove_device"
    )

    if st.sidebar.button(
        "Remove Device",
        use_container_width=True
    ):

        st.session_state.devices = [
            device
            for device in st.session_state.devices
            if device["name"] != remove_device
        ]

        st.session_state.connections = [
            connection
            for connection in st.session_state.connections
            if remove_device not in connection
        ]

        st.sidebar.success(
            f"{remove_device} removed."
        )


# =========================================================
# RESET NETWORK
# =========================================================

st.sidebar.subheader("🔄 Reset")

if st.sidebar.button(
    "Reset Network",
    use_container_width=True
):

    st.session_state.devices = [
        {"name": "Router", "type": "Router"},
        {"name": "Switch", "type": "Switch"},
        {"name": "PC-1", "type": "Computer"},
        {"name": "PC-2", "type": "Computer"},
        {"name": "Server", "type": "Server"}
    ]

    st.session_state.connections = [
        ("Router", "Switch"),
        ("Switch", "PC-1"),
        ("Switch", "PC-2"),
        ("Switch", "Server")
    ]

    st.sidebar.success("Network reset successfully.")


# =========================================================
# STATISTICS
# =========================================================

st.subheader("📊 Network Statistics")

total_devices = len(st.session_state.devices)
total_connections = len(st.session_state.connections)

router_count = sum(
    1 for d in st.session_state.devices
    if d["type"] == "Router"
)

switch_count = sum(
    1 for d in st.session_state.devices
    if d["type"] == "Switch"
)

computer_count = sum(
    1 for d in st.session_state.devices
    if d["type"] == "Computer"
)

server_count = sum(
    1 for d in st.session_state.devices
    if d["type"] == "Server"
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Devices",
        total_devices
    )

with col2:
    st.metric(
        "Connections",
        total_connections
    )

with col3:
    st.metric(
        "Computers",
        computer_count
    )

with col4:
    st.metric(
        "Servers",
        server_count
    )


# =========================================================
# TOPOLOGY
# =========================================================

st.subheader("🖥️ Network Diagram")

draw_topology()


# =========================================================
# DEVICE TABLE
# =========================================================

st.subheader("📋 Connected Devices")

device_table = pd.DataFrame(
    st.session_state.devices
)

if not device_table.empty:

    device_table.index = range(
        1,
        len(device_table) + 1
    )

    st.dataframe(
        device_table,
        use_container_width=True
    )


# =========================================================
# CONNECTION TABLE
# =========================================================

st.subheader("🔗 Network Connections")

if st.session_state.connections:

    connection_table = pd.DataFrame(
        st.session_state.connections,
        columns=["Device 1", "Device 2"]
    )

    connection_table.index = range(
        1,
        len(connection_table) + 1
    )

    st.dataframe(
        connection_table,
        use_container_width=True
    )

else:

    st.info("No connections available.")


# =========================================================
# LEGEND
# =========================================================

st.subheader("📖 Device Types")

legend_col1, legend_col2, legend_col3, legend_col4 = st.columns(4)

with legend_col1:
    st.write("🟩 **Router**")

with legend_col2:
    st.write("🟦 **Switch**")

with legend_col3:
    st.write("🟠 **Computer**")

with legend_col4:
    st.write("🟣 **Server**")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Network Topology Visualizer | "
    "Python + Streamlit + Matplotlib"
)
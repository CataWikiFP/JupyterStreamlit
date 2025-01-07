import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Load data
packages_df = pd.read_csv("COMPLETE_pkgs_in_USE.csv")
apps_users_serials_df = pd.read_csv("apps_users_serials_COMPLETE.csv")

# Data preprocessing
apps_users_serials_df['Application Title'] = apps_users_serials_df['Application Title'].astype(str)
apps_users_serials_df['Serial Number'] = apps_users_serials_df['Serial Number'].astype(str)

packages_df['occurrences_in_Application_Title'] = packages_df['coresponding_pkg_name'].apply(
    lambda x: apps_users_serials_df['Application Title'].str.contains(x, case=False).sum()
)

# Streamlit Sidebar
st.sidebar.title("Dashboard Settings")
min_occurrences = st.sidebar.slider(
    "Minimum Occurrences", 
    min_value=1, 
    max_value=int(packages_df['occurrences_in_Application_Title'].max()), 
    value=1, 
    step=1
)

# Main Dashboard: Plotting Occurrences of Packages
st.title("Package Occurrences in Application Titles")
filtered_df = packages_df[packages_df['occurrences_in_Application_Title'] >= min_occurrences]
filtered_df = filtered_df.sort_values(by='occurrences_in_Application_Title', ascending=False)

if not filtered_df.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(filtered_df['coresponding_pkg_name'], filtered_df['occurrences_in_Application_Title'])
    ax.set_xlabel('Package Names')
    ax.set_ylabel('Occurrences in Application Title')
    ax.set_title(f'Occurrences of Package Names (Min Occurrences: {min_occurrences})')
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()

    # Add annotations to bars
    for bar, app_title in zip(bars, filtered_df['coresponding_pkg_name']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, app_title, ha='center', va='bottom', fontsize=8, rotation=90)

    st.pyplot(fig)
else:
    st.write("No packages meet the minimum occurrence threshold.")

# Dropdown to display serial numbers for an application
st.title("Serial Numbers by Application")
application_titles = sorted(apps_users_serials_df['Application Title'].unique())
selected_app = st.selectbox("Select an Application", options=application_titles)

filtered_app_df = apps_users_serials_df[apps_users_serials_df['Application Title'] == selected_app]

if not filtered_app_df.empty:
    st.write(f"### Serial Numbers for Application: {selected_app}")
    for serial in filtered_app_df['Serial Number'].unique():
        st.markdown(f"- **{serial}**")
else:
    st.write(f"No serial numbers found for application: **{selected_app}**.")

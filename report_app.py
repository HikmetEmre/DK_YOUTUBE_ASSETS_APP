import streamlit as st
import pandas as pd
import numpy as np

#### Page Config ###
st.set_page_config(
    page_title="DK YOUTUBE DATA ANALYSIS APP",
    page_icon="https://img.freepik.com/premium-photo/youtube-logo-video-player-3d-design-video-media-player-interface_41204-12379.jpg",
    menu_items={
        "Get help": "mailto:hikmetemreguler@gmail.com",
        "About": "For More Information\n" + "https://github.com/HikmetEmre/City_Estimator"
    }
)

# Title of the app
st.title("**:red[DK YOUTUBE MUSIC ASSET REPORTING]** ")


### Adding Image ###
st.image("https://raw.githubusercontent.com/HikmetEmre/DK_YOUTUBE_ASSETS_APP/main/YOUTUBE%20ASSET%20DATA%20MANIPULATION%20APP.png")


# Step 1: Upload multiple CVs
uploaded_files = st.file_uploader("Upload multiple CV CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    # Step 2: Read the data
    dfs = []
    for uploaded_file in uploaded_files:
        # Adjust skiprows and low_memory parameters if necessary
        if 'df1.csv' in uploaded_file.name:
            df = pd.read_csv(uploaded_file, low_memory=False)
        elif 'df2.csv' in uploaded_file.name:
            df = pd.read_csv(uploaded_file, skiprows=1, low_memory=False)
        else:
            df = pd.read_csv(uploaded_file, low_memory=False)  # Default behavior for other files
        dfs.append(df)
    
    # Concatenate dataframes
    if len(dfs) > 0:
        df_music = pd.concat(dfs, ignore_index=True)
        
        # Display the first few rows of the concatenated dataframe
        st.write("First few rows of the concatenated dataframe:")
        st.dataframe(df_music.head())
        
        # Sum of 'Partner Revenue' column
        if 'Partner Revenue' in df_music.columns:
            total_partner_revenue = df_music['Partner Revenue'].sum()
            st.write(f"Sum of 'Partner Revenue' column: {total_partner_revenue}")
        else:
            st.write("'Partner Revenue' column not found in the uploaded CSV files.")
    else:
        st.write("No dataframes to concatenate.")
else:
    st.write("Please upload CSV files to proceed.")

import streamlit as st
import pandas as pd
import numpy as np
import os
os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '1000'
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
        
        # Step 3: Select and filter specific columns
        df_music = df_music[['Country', 'Custom ID','Asset ID', 'Asset Channel ID', 'Partner Revenue','Asset Labels']]
        df_music['Custom ID'] = df_music['Custom ID'].astype(str).str.lower()
        df_music = df_music[df_music['Partner Revenue'] > 0]
        
        # Step 4: Define the custom mapping function
        def map_custom_id(value):
            if 'hittmuzik' in value:
                return 'Hitt Music'
            elif 'hitt_'in value:
                return 'Hitt Music'
            elif 'atlanta' in value:
                return 'Atlanta Yapım'
            elif 'guven' in value:
                return 'Guven Production'
            elif 'tolga' in value:
                return 'Tolga Ornek'
            elif 'munev' in value:
                return 'Munevver Oshan'
            elif 'daphne' in value:
                return 'Daphne Media'
            elif 'istanbulplak' in value:
                return 'İstanbul Plak'
            elif 'muzikbir' in value:
                return 'MuzikBir'
            elif any(substring in value for substring in ('beng', 'mura', 'film', 'guve', 'egec', 'volk', 'ayla', 'snap', 'yonc', 'ozle', 'zeki', 'koli', 'ozge', 'dicl', 'isil', 'burh', 'fuly', 'sina', 'feri', 'fha_', 'ahiy', 'merz', 'gokc')):
                return 'Yek Music'
            elif 'incir' in value:
                return 'Yek Music'
            elif 'cocuk' in value:
                return 'MuzikBir'
            return value

        # Apply the custom function to the 'Custom ID' column
        df_music['Custom ID'] = df_music['Custom ID'].apply(lambda x: map_custom_id(x))

        # Update specific 'Custom ID' based on 'Asset Labels'
        df_music.loc[df_music['Asset Labels'] == 'Merzigo', 'Custom ID'] = 'Yek Music'

        # List of values to filter
        values_producers = ['MuzikBir', 'Hitt Music', 'İstanbul Plak', 'Yek Music', 'Atlanta Yapım', 'Guven Production', 'Munevver Oshan', 'Tolga Ornek', 'Daphne Media']

        # Filter the DataFrame
        filtered_df_for_revenue = df_music[df_music['Custom ID'].isin(values_producers)]
        filtered_df_unlabel = df_music[~df_music['Custom ID'].isin(values_producers)]

        # Display the first few rows of the unlabelled dataframe
        st.write("First few rows of the unlabelled dataframe:")
        st.dataframe(filtered_df_unlabel.head(8))

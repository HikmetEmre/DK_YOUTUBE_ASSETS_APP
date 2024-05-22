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

## WARNING ABOUT CSV FILES ###
st.markdown("** Before you upload csv files here make the BIG Music Asset file name as :red[df1] and the Small Premium Music Asset file name as :red[df2]**. ")

st.markdown("**After this uploading complete the software is going to complete all the data analysis step by step!**.")

# Step 1: Upload multiple CSVs
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

        # New step: Update 'Custom ID' based on 'Asset Labels'
        asset_label_to_custom_id = {
            'Akbaş Müzik': 'Daphne Media',
            'Alim Yapım': 'Yek Music',
            'Alov Music': 'Yek Music',
            'Atlanta Film Yapım': 'Atlanta Yapım',
            'Ayaz Babayev': 'Yek Music',
            'Daphne Media': 'Daphne Media',
            'Dj Woywodo': 'Yek Music',
            'Dj Xonano': 'Yek Music',
            'DMC': 'Hitt Music',
            'Elçin Meherremov': 'Yek Music',
            'Fexri Elesgerli': 'Yek Music',
            'Gig Music': 'Yek Music',
            'Güven Prodüksiyon': 'Guven Production',
            'Hitt Müzik': 'Hitt Music',
            'İstanbul Plak': 'İstanbul Plak',
            'Media Show': 'Yek Music',
            'Murat Dalkılıç': 'Yek Music',
            'Nuray Meherov': 'Yek Music',
            'Rahman Aliyev': 'Yek Music',
            'Seymur Memmedov': 'Yek Music',
            'Stüdyo Net': 'Munevver Oshan',
            'Xeyal Huseyn': 'Yek Music',
            'Xumar Qedimova': 'Yek Music',
            'Zenfira İbrahimova': 'Yek Music',
            'Bengu': 'Yek Music',
            'Arda Han': 'Yek Music',
            'Duygu': 'Yek Music',
            'Elçin Orçun': 'Yek Music',
            'MMD': 'Yek Music',
            'Ege Can Sal': 'Yek Music',
            'Volkan Konak': 'Yek Music',
            'Snapmuse': 'Yek Music',
            'Yonca Lodi': 'Yek Music',
            'Özlem Ağrı': 'Yek Music',
            'Zeki Güner': 'Yek Music',
            'Koliva': 'Yek Music',
            'Özge Fışkın': 'Yek Music',
            'Dicle Olcay': 'Yek Music',
            'Işıl Ayman': 'Yek Music',
            'Burhan Bayar': 'Yek Music',
            'Fulya Koç': 'Yek Music',
            'Sinan Akçıl': 'Yek Music',
            'Feride Hilal Akın': 'Yek Music',
            'Ahiyan': 'Yek Music',
            'Merzigo': 'Yek Music',
            'Gökçe Türk': 'Yek Music',
            'Süreç Medya': 'MuzikBir',
            'Atalay Prodüksiyon': 'MuzikBir',
            'Atalay Production': 'MuzikBir',
            'Berekat Yayınevi': 'MuzikBir',
            'Fahrettin Tiryaki Music': 'MuzikBir',
            'Marmara Müzik': 'MuzikBir',
            'Metropol Müzik': 'MuzikBir',
            'Metropol Müzik Yapım': 'MuzikBir',
            'Asır Ajans': 'MuzikBir',
            'Hayal Evim Müzik': 'MuzikBir',
            'HB Müzik': 'MuzikBir',
            'Işık Yapım': 'MuzikBir',
            'Nasihat Yayınları': 'MuzikBir',
            'Vuqarlı Media': 'MuzikBir',
            'Tolga Örnek': 'Tolga Ornek',
            'Reyhani Yapım': 'MuzikBir',
            'Alvarlı Efe Hazretleri Vakfı': 'MuzikBir',
            'Mortaza Ayrumlu': 'MuzikBir',
            'Asim Rasimoglu': 'MuzikBir',
            'Dj Kamran MM': 'MuzikBir',
            'Elcin Celilli': 'MuzikBir',
            'Emir Tovuzlu': 'MuzikBir',
            'Ferhad Bicare': 'MuzikBir',
            'Ferid Ehmedzade': 'MuzikBir',
            'Ferrux Haşimi': 'MuzikBir',
            'Mahmud Mikayilli': 'MuzikBir',
            'Mardan Asgar': 'MuzikBir',
            'Mojtaba Agharezaei': 'MuzikBir',
            'Murad Elizade': 'MuzikBir',
            'Murad Imisli': 'MuzikBir',
            'Nurlan Goranboylu': 'MuzikBir',
            'Rovsen Sani': 'MuzikBir',
            'Simral Ferid': 'MuzikBir',
            'Ziya Selimov': 'MuzikBir',
            'Genç Müzik Yapım': 'Muz

ikBir',
            'Mehriban Aslan': 'MuzikBir',
            'İlqar Vuqarlı': 'MuzikBir',
            'Hüseyin Ali': 'MuzikBir',
            'Müzikbir': 'MuzikBir'
        }

        # Apply the mapping to the 'Custom ID' column based on 'Asset Labels'
        df_music['Custom ID'] = df_music.apply(
            lambda row: asset_label_to_custom_id[row['Asset Labels']] if row['Asset Labels'] in asset_label_to_custom_id else row['Custom ID'],
            axis=1
        )

        # List of values to filter
        values_producers = ['MuzikBir', 'Hitt Music', 'İstanbul Plak', 'Yek Music', 'Atlanta Yapım', 'Guven Production', 'Munevver Oshan', 'Tolga Ornek', 'Daphne Media']

        # Filter the DataFrame
        filtered_df_for_revenue = df_music[df_music['Custom ID'].isin(values_producers)]
        filtered_df_unlabel = df_music[~df_music['Custom ID'].isin(values_producers)]

        if not filtered_df_unlabel.empty:
            total_unidentified_revenue = filtered_df_unlabel['Partner Revenue'].sum()
            st.write(f"The Total Revenue of Unidentified Data: {total_unidentified_revenue}")
            
            # Display the first few rows of the unlabelled dataframe
            st.write("First few rows of the unlabelled dataframe:")
            st.dataframe(filtered_df_unlabel)
                
            unknown_asset_ids = filtered_df_unlabel['Asset ID'].tolist()
            st.write(f"Unknown Asset ID's of This Month: {unknown_asset_ids}")
        else:
            st.write("There is no unidentified data for this month!")

        # Rename the 'Custom ID' column to 'Producers'
        filtered_df_for_revenue.rename(columns={'Custom ID': 'Producers'}, inplace=True)

        # Group by 'Producers' and sum 'Partner Revenue'
        revenue_summary = filtered_df_for_revenue.groupby('Producers')['Partner Revenue'].sum()

        # Sort the result by the summed 'Partner Revenue' in descending order
        revenue_summary = revenue_summary.sort_values(ascending=False)

        # Print the revenue summary in a clearer format
        st.write("### Revenue Summary by Producers")
        st.write(revenue_summary)

        # Optionally, display the summary as a styled table for better readability
        st.table(revenue_summary.reset_index())

        # Optionally, add a bar chart for visual representation
        st.bar_chart(revenue_summary)

        # Filter the DataFrame for US tax
        filtered_df_for_usa_tax = filtered_df_for_revenue[filtered_df_for_revenue['Country'] == 'US']

        # Group by 'Producers' and sum 'Partner Revenue', then calculate 10% tax
        tax_summary = filtered_df_for_usa_tax.groupby('Producers')['Partner Revenue'].sum() * 0.10

        # Sort the result by the summed 'Partner Revenue' in descending order
        tax_summary = tax_summary.sort_values(ascending=False)

        # Print the tax summary in a clearer format
        st.write("### US Tax Summary by Producers (10% of Partner Revenue)")
        st.write(tax_summary)

        # Optionally, display the summary as a styled table for better readability
        st.table(tax_summary.reset_index())

        # Optionally, add a bar chart for visual representation
        st.bar_chart(tax_summary)
       

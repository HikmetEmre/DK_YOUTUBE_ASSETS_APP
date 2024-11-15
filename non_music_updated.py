import streamlit as st
import pandas as pd
import numpy as np
import os

os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '1000'

#### Page Config ###
st.set_page_config(
    page_title="DK YOUTUBE DATA ANALYSIS APP",
    page_icon="https://icones.pro/wp-content/uploads/2021/02/youtube-logo-icone-bleue.png",
    menu_items={
        "Get help": "mailto:hikmetemreguler@gmail.com",
        "About": "For More Information\n" + "https://github.com/HikmetEmre/City_Estimator"
    }
)

# Title of the app
st.title("**:blue[DK YOUTUBE NON MUSIC ASSET REPORTING]** ")

### Adding Image ###
st.image("https://raw.githubusercontent.com/HikmetEmre/DK_YOUTUBE_ASSETS_APP/main/YOUTUBE%20ASSET%20DATA%20MANIPULATION_image_2.png")

## WARNING ABOUT CSV FILES ###
st.subheader("**:red[WARNING PLEASE READ THE DESCRIPTION BELOW!!]**")
st.markdown("**Before you upload csv files here make the BIG NON-MUSIC Asset file name as :blue[df1] and the Small Premium NON-MUSIC Assets FILES name as :red[df2] and :red[df3].**")

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
        elif 'df3.csv' in uploaded_file.name:
            df = pd.read_csv(uploaded_file, skiprows=1, low_memory=False)
        else:
            df = pd.read_csv(uploaded_file, low_memory=False)  # Default behavior for other files
        dfs.append(df)

    
    # Concatenate dataframes
    if len(dfs) > 0:
        df_music = pd.concat(dfs, ignore_index=True)
        
        # Step 3: Select and filter specific columns
        df_music = df_music[['Country','Asset Title', 'Custom ID','Asset ID', 'Asset Channel ID', 'Partner Revenue','Asset Labels']]
        df_music['Custom ID'] = df_music['Custom ID'].astype(str).str.lower()
        df_music = df_music[df_music['Partner Revenue'] > 0]
        
        # Step 4: Define the custom mapping function

        def assign_producer(custom_id):
            if 'tolga' in custom_id:
                return 'Tolga Ornek'
            elif 'anibera' in custom_id:
                return 'Anibera Tv'
            elif 'boyutfilm' in custom_id:
                return 'Boyut Film'
            elif 'muhtesemfilm' in custom_id:
                return 'Muhtesem Film'
            elif 'nuribilgeceylan' in custom_id:
                return 'Nuri Bilge Ceylan'
            elif 'zekidemirkubuz' in custom_id:
                return 'Zeki Demirkubuz'
            elif '35mm_enkolaytarifler' in custom_id:
                return '35mm'
            elif 'limityapim' in custom_id:
                return 'Limit Yapım'
            elif 'muzikbir' in custom_id:
                return 'MuzikBir'
            elif 'mnsfilm' in custom_id:
                return 'Mns Film'
            elif 'ubay' in custom_id:
                return 'Ubay'
            elif 'documentarytv_' in custom_id:
                return 'DocumentaryTv'
            else:
                producer_list = ['akillibidik', 'easyenglishathome', 'sifirbir', 'sokagincocuklari', 'ungfilm', 
                                 'venharsagiroglu', 'hicdizisi', 'claudiaroberts', 'Ailin', 'GiantsofHistory', 'metinyegin','ubay','Documentary Tv']
                for producer in producer_list:
                    if producer in custom_id:
                        return 'Daphne'
                return custom_id  # or whatever default value you want to assign

        # Apply the custom function to the 'Custom ID' column
        df_music['Custom ID'] = df_music['Custom ID'].apply(assign_producer)

        # New step: Update 'Custom ID' based on 'Asset Labels'
        asset_label_to_custom_id = {
            'Nuri Bilge Ceylan': 'Nuri Bilge Ceylan',
            'Tolga Örnek': 'Tolga Ornek',
            'Boyut Film': 'Boyut Film',
            'Anibera TV': 'Anibera TV',
            'Atlanta Film Yapım': 'Atlanta Yapım',
            'Muhteşem Film': 'Muhtesem Film',
            'Daphne Media': 'Daphne',
            'Mns Film': 'Mns Film',
            'Müzikbir': 'MuzikBir',
            'Zeki Demirkubuz': 'Zeki Demirkubuz',
            'Limit Yapım': 'Limit Yapım',
            'Sıfır Bir': 'Daphne',
            'Akıllı Bıdık': 'Daphne',
            'Ubay': 'Ubay',
            'DocumentaryTV: 'Documentary Tv'
        }

        # Apply the mapping to the 'Custom ID' column based on 'Asset Labels'
        df_music['Custom ID'] = df_music.apply(
            lambda row: asset_label_to_custom_id[row['Asset Labels']] if row['Asset Labels'] in asset_label_to_custom_id else row['Custom ID'],
            axis=1
        )

        # List of values to filter
        values_producers = ['Tolga Ornek', 'Boyut Film', 'Muhtesem Film', 'Anibera TV', 'Mns Film', 'MuzikBir', 'Daphne', 'Nuri Bilge Ceylan', 'Zeki Demirkubuz','Limit Yapım','Ubay']

        # Filter the DataFrame
        filtered_df_for_revenue = df_music[df_music['Custom ID'].isin(values_producers)]
        filtered_df_unlabel = df_music[~df_music['Custom ID'].isin(values_producers)]

        total_revenue_of_month = df_music['Partner Revenue'].sum()
        st.write('The Total Income of This Month :', total_revenue_of_month)

        if not filtered_df_unlabel.empty:
            total_unidentified_revenue = filtered_df_unlabel['Partner Revenue'].sum()
            st.write(f"The Total Revenue of Unidentified Data: {total_unidentified_revenue}")
            
            # Display the first few rows of the unlabelled dataframe
            st.write("First few rows of the unlabelled dataframe:")
            st.dataframe(filtered_df_unlabel)
                
            unknown_asset_ids = filtered_df_unlabel['Asset ID'].unique().tolist()
            st.write(f"Unknown Asset ID's of This Month: {unknown_asset_ids}")
        else:
            st.write("There is no unidentified data for this month!")

        # Rename the 'Custom ID' column
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
       
        # Add a subheader for the final dashboard
        st.subheader("**:red[FINAL DASHBOARD!!]**")

        # Create the final DataFrame
        final_df = revenue_summary.reset_index()
        final_df.columns = ['Producers', 'Total Revenue']

        # Add USA TAX column from tax_summary
        final_df = final_df.merge(tax_summary.reset_index(), on='Producers', how='left')
        final_df.columns = ['Producers', 'Total Revenue', 'USA TAX']

        # Fill NaN values in 'USA TAX' with 0 (in case there are producers with no USA TAX)
        final_df['USA TAX'] = final_df['USA TAX'].fillna(0)

        # Calculate Net Revenue
        final_df['Net Revenue'] = final_df['Total Revenue'] - final_df['USA TAX']

        # Calculate DK Payment based on the producer
        percentage_dict = {
            'MuzikBir': 0.05, 
            'Zeki Demirkubuz': 0.20, 
            'Nuri Bilge Ceylan': 0.20, 
            'Muhtesem Film': 0.20, 
            'Mns Film': 0.20, 
            'Boyut Film': 0.20, 
            'Anibera TV': 0.20, 
            'Tolga Ornek': 0.20,
            'Limit Yapım': 0.20,
            'Ubay': 0.20,
            'Daphne': 1,
            'Documentary Tv': 0.20
        }

        # Function to calculate DK Payment
        def calculate_dk_payment(producer, net_revenue):
            return net_revenue * percentage_dict.get(producer, 0)

        # Apply the function to calculate DK Payment
        final_df['DK Payment'] = final_df.apply(lambda row: calculate_dk_payment(row['Producers'], row['Net Revenue']), axis=1)

        # Calculate Producers Payment
        final_df['Producers Payment'] = final_df['Net Revenue'] - final_df['DK Payment']

        # Display the final DataFrame
        st.write("### Final Dashboard")
        st.dataframe(final_df)

        # Optionally, display the final DataFrame as a styled table for better readability
        st.table(final_df)

        # Optionally, add a bar chart for visual representation of Total Revenue, USA TAX, Net Revenue, DK Payment, and Producers Payment
        st.write("### Revenue Breakdown by Producers")
        st.bar_chart(final_df.set_index('Producers')[['Total Revenue', 'USA TAX', 'Net Revenue', 'DK Payment', 'Producers Payment']])

        #  For identifying Asset Owners From Asset ID and adding new customers

    st.write("### Input **:red[Asset Channel ID]** of **:blue[Unknown Asset ID's]**  to see who uploaded!!")
    asset_channel_id = st.text_input("Enter Asset Channel ID")
    if asset_channel_id:
        # Filter the DataFrame based on the input Asset Channel ID
        df_for_find = df_music[df_music['Asset Channel ID'] == asset_channel_id]
        # Further filter rows where 'Custom ID' and 'Asset Labels' are not None
        df_for_find = df_for_find[df_for_find['Custom ID'].notna() & df_for_find['Asset Labels'].notna()]
        # Display the first 8 rows of the filtered DataFrame
        st.write("Matching Rows:")
        st.dataframe(df_for_find.head(8)[['Custom ID', 'Asset Labels']])

    st.header("Add New Customer")
    new_custom_id = st.text_input("Enter Custom ID")
    new_asset_label = st.text_input("Enter Asset Labels")
    new_producer = st.text_input("Enter Producer")
    if st.button("Add Customer"):
        if new_custom_id and new_asset_label and new_producer:
            asset_label_to_custom_id[new_asset_label] = new_producer
            st.write("New customer added successfully.")
        else:
            st.write("Please fill in all fields.")

# Step 5: Create a selectbox to filter data by producer

    unique_producers =  filtered_df_for_revenue['Producers'].unique()
    selected_producer = st.selectbox('Select a producer', unique_producers)

    if selected_producer:
            filtered_data =  filtered_df_for_revenue[filtered_df_for_revenue['Producers'] == selected_producer]
            total_revenue = filtered_data['Partner Revenue'].sum()

            st.write(f"Total revenue for {selected_producer}: ${total_revenue:.2f}")

            st.dataframe(filtered_data)

            # New step: Provide download option for filtered data
            csv_file = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download filtered data as CSV",
                data=csv_file,
                file_name=f'{selected_producer}_data.csv',
                mime='text/csv'
            )
    else :
        st.write("Please select a producer from the dropdown.")             

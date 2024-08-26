import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Step 1: Data cleaning function

def clean_city_state_country(df):
    df['BADD4'] = df['BADD4'].str.upper()
    df['STATE'] = df['STATE'].str.upper()
    df['COUNTRY'] = df['COUNTRY'].str.upper()
    # Combined replacement dictionary for city, state, and country
    replace_dict = {
        'BADD4': {
            'NEW DELHI': 'DELHI',
            'WEST DELHI': 'DELHI',
            'NORTH WEST DELHI': 'DELHI',
            'SOUTH DELHI': 'DELHI',
            'EAST DELHI': 'DELHI',
            'NORTH DELHI': 'DELHI',
            'CENTRAL DELHI': 'DELHI',
            'SOUTH WEST DELHI': 'DELHI',
            'NORTH EAST DELHI': 'DELHI',
            'NORTH  WEST  DELHI': 'DELHI',
            'SOUTH  DELHI': 'DELHI',
            'WESTDELHI': 'DELHI',
            'CALCUTTA': 'KOLKATA',
            'BANGALORE': 'BENGALURU',
            'BOMBAY': 'MUMBAI',
            'MUMBAI SUBURBAN': 'MUMBAI',
            'KANDIVALI EAST MUMBAI': 'MUMBAI',
            'NAVI MUMBAI': 'NAVI MUMBAI',
            'NAVIMUMBAI': 'NAVI MUMBAI'
        },
        'STATE': {
            'TAMILNADU': 'TAMIL NADU',
            'MAHARASTRA': 'MAHARASHTRA',
            'MAHARSHTRA': 'MAHARASHTRA'
        },
        'COUNTRY': {
            'India': 'INDIA',
            'india': 'INDIA',
            '85': 'INDIA'
        }
    }

    # Apply the replacement for each relevant column
    for column, replacements in replace_dict.items():
        df[column] = df[column].replace(replacements)
    
    return df



def clean_data(df):
    # Correct misspellings in city names
    #standardized_city_list = [...]  # Your standardized city list here
    #df['BADD4'] = df['BADD4'].apply(lambda x: correct_city_name(x, standardized_city_list))
    
    # Convert OPENDT to datetime
    df['OPENDT'] = pd.to_datetime(df['OPENDT'], errors='coerce')
    df['BADD4'] = df['BADD4'].str.upper()
    df['STATE'] = df['STATE'].str.upper()
    df['COUNTRY'] = df['COUNTRY'].str.upper()

    return df


# Step 2: Pie chart for 'COUNTRY' and 'BEN_POSI'

def create_pie_chart(df):
#    df = df[df['COUNTRY'].str.upper() != 'INDIA']
    country_data = df.groupby('COUNTRY')['BEN_POSI'].sum().reset_index()
    fig = px.pie(country_data, values='BEN_POSI', names='COUNTRY', color_discrete_sequence=px.colors.colorbrewer.Pastel1)
    return fig


def create_country_scatter_chart_without_india(df):
    df2 = df[df['COUNTRY'] != 'INDIA']
    df2 = df2[df2['COUNTRY'] != 'india']
    # Step 1: Group by 'COUNTRY' and sum 'BEN_POSI'
    country_data = df2.groupby('COUNTRY')['BEN_POSI'].sum().reset_index()

    # Step 2: Create the Dot Plot
    fig = px.scatter(country_data, x='COUNTRY', y='BEN_POSI',
                    size='BEN_POSI',  # Size of dots based on 'BEN_POSI'
                    color='COUNTRY',  # Color dots by country
                    color_discrete_sequence=px.colors.qualitative.D3,  # Use a custom color palette
                    title="Sum of BEN_POSI by Country"
                    )

    # Step 3: Customize the Chart
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Sum of BEN_POSI",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)", 
        paper_bgcolor="rgba(0,0,0,0)",
        
        title_font=dict(size=24, color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridwidth=0.5, 
                gridcolor="rgba(0,0,0,0.3)")
    )

    return fig

# Step 3: Bar chart for top banks
def create_top_banks_chart(df):
    top_banks = df['BANK_NAME'].value_counts().nlargest(5).reset_index()
    top_banks.columns = ['BANK_NAME', 'Count']
    fig = px.bar(top_banks, x='BANK_NAME', y='Count',color = 'BANK_NAME', title='Top 5 Banks by Count')
    return fig

# Step 4: Bar chart for top investors
def create_top_investors_chart(df):
    top_investors = df.groupby('HOLD1')['BEN_POSI'].sum().nlargest(5).reset_index()
    fig = px.bar(top_investors, x='HOLD1', y='BEN_POSI', color = 'HOLD1', title='Top 5 Investors by Sum of BEN_POSI')
    return fig

# Step 5: Track changes in 'BEN_POSI' and 'HOLD1' from a new Excel file
def track_changes(df, new_df):
    merged_df = pd.merge(df[['HOLD1', 'BEN_POSI']], new_df[['HOLD1', 'BEN_POSI']], on='HOLD1', how='outer', suffixes=('_old', '_new'))
    merged_df['BEN_POSI_Change'] = merged_df['BEN_POSI_new'] - merged_df['BEN_POSI_old']
    return merged_df

# Additional KPIs: Top 5 States, Top 5 Cities, Top 10 Investors
def create_top_states_chart(df):
    top_states = df['STATE'].value_counts().nlargest(5).reset_index()
    top_states.columns = ['STATE', 'Count']
    fig = px.bar(top_states, x='STATE', y='Count', color = 'STATE',title='Top 5 States by Count', color_discrete_sequence=px.colors.colorbrewer.Pastel1)
    return fig

def create_top_cities_chart(df):
    top_cities = df['BADD4'].value_counts().nlargest(5).reset_index()
    top_cities.columns = ['City', 'Count']
    fig = px.bar(top_cities, x='City', y='Count', 
                 title='Top 5 Cities by Count',
                 color = 'City',
                  color_discrete_sequence=px.colors.colorbrewer.Pastel1)
    return fig

def create_top_investors_ben_posi_chart(df):
    top_investors_ben_posi = df.groupby('HOLD1')['BEN_POSI'].sum().nlargest(10).reset_index()
    fig = px.bar(top_investors_ben_posi, x='HOLD1', y='BEN_POSI', title='Top 10 Investors by Sum of BEN_POSI',color = 'HOLD1', color_discrete_sequence=px.colors.colorbrewer.Pastel1)
    
    return fig

# Streamlit App Layout
st.title("Investor Relations Dashboard")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx","xls"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = clean_data(df)
    clean_city_state_country

    st.header("Pie Chart: Country Distribution")
    st.plotly_chart(create_pie_chart(df))
    
    st.header("Pie Chart: Country Distribution without INDIA")
    st.plotly_chart(create_country_scatter_chart_without_india(df))



    st.header("Top 5 Banks by Count")
    st.plotly_chart(create_top_banks_chart(df))

    st.header("Top 5 Investors by Sum of BEN_POSI")
    st.plotly_chart(create_top_investors_chart(df))

    st.header("Top 5 States by Count")
    st.plotly_chart(create_top_states_chart(df))

    st.header("Top 5 Cities by Count")
    st.plotly_chart(create_top_cities_chart(df))

    st.header("Top 10 Investors by Sum of BEN_POSI")
    st.plotly_chart(create_top_investors_ben_posi_chart(df))

    st.header("Upload New Excel File to Track Changes in BEN_POSI")
    new_file = st.file_uploader("Upload the new Excel file", type=["xlsx","xls"])
    
    if new_file:
        new_df = pd.read_excel(new_file)
        new_df = clean_data(new_df)
        changes_df = track_changes(df, new_df)
        st.write("Changes in BEN_POSI and HOLD1")
        st.dataframe(changes_df)

st.sidebar.header("Dashboard Settings")
# Add additional settings here if needed

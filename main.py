import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


def clean_city_state_country(df):

    replace_dict_city = {
        'NEW DELHI': 'DELHI',
        'WEST DELHI': 'DELHI',
        'NORTH WEST DELHI':'DELHI',
        'SOUTH DELHI':'DELHI',
        'EAST DELHI':'DELHI',
        'NORTH DELHI':'DELHI',
        'CENTRAL DELHI':'DELHI',
        'SOUTH WEST DELHI':'DELHI',
        'NORTH EAST DELHI':'DELHI',
        'NORTH  WEST  DELHI':'DELHI',
        'SOUTH  DELHI':'DELHI',
        'WESTDELHI':'DELHI',

        'CALCUTTA': 'KOLKATA',
        'BANGALORE': 'BENGALURU',

        'BOMBAY': 'MUMBAI',
        'MUMBAI SUBURBAN':'MUMBAI',
        'KANDIVALI EAST MUMBAI':'MUMBAI',

        'NAVI MUMBAI':'NAVI MUMBAI',
        'NAVIMUMBAI':'NAVI MUMBAI',
        
    }

    df['BADD4'] = df['BADD4'].replace(replace_dict_city)

    replace_dict_state = {
    'TAMIL NADU':'TAMIL NADU',
    'TAMILNADU':'TAMIL NADU',
    'TAMIL NADU':'TAMIL NADU',

    'MAHARASHTRA':'MAHARASHTRA',

    'MAHARASTRA':'MAHARASHTRA',
    'MAHARSHTRA':'MAHARASHTRA'

    }

    df['STATE'] = df['STATE'].replace(replace_dict_state)


    replace_dict_country = {

    'INDIA':'INDIA',
    'India':'INDIA',
    'india':'INDIA',
    '85':'INDIA'

    }

    df['COUNTRY'] = df['COUNTRY'].replace(replace_dict_country)

    return df





def clean_data(df):
    # Correct misspellings in city names
    #standardized_city_list = [...]  # Your standardized city list here
    #df['BADD4'] = df['BADD4'].apply(lambda x: correct_city_name(x, standardized_city_list))
    
    # Convert OPENDT to datetime
    df['OPENDT'] = pd.to_datetime(df['OPENDT'], errors='coerce')

    return df

def correct_city_name(city_name, city_list, threshold=80):
    from rapidfuzz import process, fuzz
    match, score = process.extractOne(city_name, city_list, scorer=fuzz.ratio)
    if score >= threshold:
        return match
    return city_name



def create_investor_bar_chart(df):
    investor_data = df.groupby('HOLD1')['BEN_POSI'].sum().nlargest(10)
    
    fig, ax = plt.subplots()
    ax.bar(investor_data.index, investor_data.values, color='lightgreen')
    ax.set_title('Top 10 Investors by Total BEN_POSI')
    ax.set_ylabel('Total BEN_POSI')
    ax.set_xlabel('Investor Name')
    ax.set_xticklabels(investor_data.index, rotation=45, ha='right')
    
    st.pyplot(fig)

def create_bank_bar_chart(df):
    bank_data = df['BANK_NAME'].value_counts().head(10)
    
    fig, ax = plt.subplots()
    ax.bar(bank_data.index, bank_data.values, color='skyblue')
    ax.set_title('Top 10 Banks by Number of Accounts')
    ax.set_ylabel('Number of Accounts')
    ax.set_xlabel('Bank Name')
    ax.set_xticklabels(bank_data.index, rotation=45, ha='right')
    
    st.pyplot(fig)


def create_country_pie_chart(df):
    df_filtered = df[df['COUNTRY'] != 'INDIA']
    country_data = df_filtered.groupby('COUNTRY')['BEN_POSI'].agg(['count', 'sum'])
    
    # Define pastel colors
    pastel_colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF', '#B4A7D6', '#D5A6BD']
    
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(country_data['sum'], labels=country_data.index, autopct='%1.1f%%', startangle=140, colors=pastel_colors)
    ax.set_title('Distribution of BEN_POSI by Country (Excluding India)')
    
    st.pyplot(fig)





def main():
    st.title("Investor Relations Dashboard")

    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls", "csv"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        df = clean_city_state_country(df)
        df = clean_data(df)

        st.subheader("Pie Chart: BEN_POSI Distribution by Country")
        create_country_pie_chart(df)

        st.subheader("Bar Chart: Top Banks")
        create_bank_bar_chart(df)

        st.subheader("Bar Chart: Top Investors")
        create_investor_bar_chart(df)

if __name__ == "__main__":
    main()

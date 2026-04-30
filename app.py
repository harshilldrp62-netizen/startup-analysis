import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.set_page_config(layout='wide',page_title='StartUp Analysis')
df = pd.read_csv("new_startup_funding.csv")
df['Date'] = pd.to_datetime(df['Date'],errors='coerce')
df['month'] = df['Date'].dt.month_name().str[:3]
df['year'] = df['Date'].dt.year

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
df['InvestmentnType'] = df['InvestmentnType'].replace('Seed\\\\nFunding','Seed Funding')
df['InvestmentnType'] = df['InvestmentnType'].replace('Private\\\\nEquity','Private Equity')


# Investors Details - Function
def load_investor_details(investor): 
    
    st.title(investor)
    st.subheader("Investor's Most Recent Investments")
    st.dataframe(df[df['Investors Name'].str.contains(investor)].head(5)[['Date','Name','vertical','Investors Name','InvestmentnType','Amount']])
    st.subheader("Investor's Biggest Investment")
    biggest_invest = df[df['Investors Name'].str.contains(investor)].groupby('Name')['Amount'].sum().sort_values(ascending=False).head()

    st.dataframe(biggest_invest)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("Graph of Top 5 Investments",text_alignment='justify')
        fig,ax = plt.subplots()
        ax.bar(biggest_invest.index,biggest_invest.values)
        st.pyplot(fig)
    with col2:
        st.subheader('Investor Generally Invests in : ',text_alignment='justify')
        general_series = df[df['Investors Name'].str.contains(investor)].groupby('vertical')['Amount'].sum()
        fig1,ax1 = plt.subplots()
        ax1.pie(general_series.values,labels=general_series.index,autopct='%0.01f%%')
        st.pyplot(fig1)
    with col1:
        st.subheader("Stages (Round)",text_alignment='justify')
        stages_series = df[df['Investors Name'].str.contains(investor)].groupby('InvestmentnType')['Amount'].sum()
        fig2,ax2 = plt.subplots()
        ax2.pie(stages_series.values,labels=stages_series.index,autopct='%0.01f%%')
        st.pyplot(fig2)
    with col2:
        st.subheader('Investor Generally Invests in : ',text_alignment='justify')
        cities_series = df[df['Investors Name'].str.contains(investor)].groupby('city')['Amount'].sum()
        fig3,ax3 = plt.subplots()
        ax3.pie(cities_series.values,labels=cities_series.index,autopct='%0.01f%%')
        st.pyplot(fig3)
    with col1:
        st.subheader("Every Year Investment",text_alignment='justify')
        df['year'] = df['Date'].dt.year
        yearly_inv_series = df[df['Investors Name'].str.contains(investor)].groupby('year')['Amount'].sum()
        fig4,ax4 = plt.subplots()
        ax4.plot(yearly_inv_series.index,yearly_inv_series.values)
        st.pyplot(fig4)
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Investor'])

# Overall Analysis Function:
def overall_analysis():
    col1,col2 = st.columns(2)
    
    with col1:
        st.subheader("Total Amount Invested")
        total = round(df['Amount'].sum())
        st.metric('Total',str(total) + ' Cr')
    with col2:
        st.subheader("Maximum Amount Invested By A StartUp")
        maximum_inv = df.groupby('Name')['Amount'].max().sort_values(ascending=False).values[0]
        st.metric('Maximum',str(maximum_inv) + ' Cr')
    with col1:
        st.subheader("Average Investments Done By Startups")
        average_inv = round(df.groupby('Name')['Amount'].sum().mean(),2)
        st.metric('Average',str(average_inv) + ' Cr')
    with col2:
        st.subheader("Total Funded Startups")
        total_start = df['Name'].nunique()
        st.metric('Total',str(total_start) + ' Startups')
    with col1:
        st.subheader("MoM Chart for Investment Amount",text_alignment='justify')
        
        monthly_invest = df.groupby('month')['Amount'].sum()
        
        fig5,ax5 = plt.subplots()
        ax5.plot(monthly_invest.index,monthly_invest.values)
        ax5.set_xlabel('Months')
        ax5.set_ylabel('Amount')
        st.pyplot(fig5)
    with col2:
        st.subheader("MoM Chart for Investment Count",text_alignment='justify')

        monthly_count = df.groupby('month')['Amount'].count()

        fig6,ax6 = plt.subplots()
        ax6.plot(monthly_count.index,monthly_count.values)
        ax6.set_xlabel('Months')
        ax6.set_ylabel('Count')
        st.pyplot(fig6)
    with col1:
        st.subheader("Sector wise Investment Amount Pie Chart (Top 5)",text_alignment='justify')

        sector_wise_amount = df.groupby('InvestmentnType')['Amount'].sum().sort_values(ascending=False).head(5)
        fig7,ax7 = plt.subplots()
        ax7.pie(sector_wise_amount.values,labels=sector_wise_amount.index,autopct='%0.1f%%')
        st.pyplot(fig7)
    with col2:
        st.subheader("Sector wise Investment Count Pie Chart (Top 5)",text_alignment='justify')

        sector_wise_count = df.groupby('InvestmentnType')['Amount'].count().sort_values(ascending=False).head(5)
        fig8,ax8 = plt.subplots()
        ax8.pie(sector_wise_count.values,labels=sector_wise_count.index,autopct='%0.1f%%')
        st.pyplot(fig8)
    st.subheader("Types of Funding")
    st.dataframe(pd.DataFrame(df['InvestmentnType'].unique(),columns=['Funding type']))
    st.write("Total Number of Fundings are :",df['InvestmentnType'].nunique())

    st.subheader("City Wise Funding",text_alignment='justify')
    citywise_funding = df.groupby('city')['Amount'].sum()
    st.dataframe(citywise_funding)
    col3,col4 = st.columns(2)
    with col3:
        st.subheader("Yearly Top Startups")
        grouped = df.groupby(['year','Name'])['Amount'].sum().sort_values(ascending=False)
        st.dataframe(grouped.groupby(level='year').nth(0))
    with col4:
        st.subheader("Overall Top Startups")
        overall_top = df.groupby('Name')['Amount'].sum().sort_values(ascending=False).head(5)
        st.dataframe(overall_top)

if option == 'Overall Analysis':
    st.title('Overall Analysis',text_alignment='center')
    btn0 = st.sidebar.button("Show Overall Analysis")
    if btn0:
        overall_analysis()
    

elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(list(set(df['Investors Name'].str.split(',').sum()))))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
    
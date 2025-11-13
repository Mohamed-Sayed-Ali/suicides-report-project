import pandas as pd
import numpy as np
import plotly.express as px 
import streamlit as st

st.set_page_config(layout= 'wide', page_title='Suicides Rate  EDA')

html_title = """<h1 style="color:white;text-align:center;">Suicides Rate Exploratory Data Analysis </h1>"""
st.markdown(html_title, unsafe_allow_html=True)

st.image('https://static1.bigstockphoto.com/3/0/8/large1500/8033710.jpg')

df = pd.read_csv('cleaned_suicides.csv', index_col= 0)

page = st.sidebar.radio('Pages', ['Home', "KPI's Dashboard", "Suicides Report"])

if page=='Home':
    st.subheader('Dataset Overview')
    st.dataframe(df)
    st.subheader('display the number of the Rows and Columns')
    st.write(f'Number Of Rows : {df.shape[0]}')
    st.write(f'Number Of columns :{df.shape[1]}')
    st.write('---')
    import streamlit as st

    def main():
        st.title("Suicide Dataset Column Descriptions")
        columns = [
            "country", "year", "sex", "age", "suicides_no", "population",
            "suicides/100k pop", "country-year", "gdp_for_year ($)",
            "gdp_per_capita ($)", "generation", "suicide_rate"
        ]
        descriptions = {
            "country": "Name of the country where the data was recorded.",
            "year": "The year of observation.",
            "sex": "Gender category (male or female).",
            "age": "Age group (e.g., '15-24 years', '75+ years').",
            "suicides_no": "Total number of suicide cases in that demographic group.",
            "population": "Population count for the demographic group.",
            "suicides/100k pop": "Suicide rate per 100,000 population.",
            "country-year": "Concatenation of country and year (e.g., 'Albania1987').",
            "gdp_for_year ($)": "Total GDP for the country that year (formatted as a string with commas, e.g., '1,234,567,890').",
            "gdp_per_capita ($)": "GDP per capita in USD.",
            "generation": "Demographic generation label (e.g., 'Boomers', 'Millennials').",
            "suicide_rate": "Suicide rate expressed as a percentage (suicides_no / population × 100)."
        }
        selected_column = st.sidebar.selectbox("Select Column", columns)
        st.header(selected_column)
        st.write(descriptions[selected_column])
        if selected_column == "country":
            st.write("Example: Albania, France, India")
        elif selected_column == "year":
            st.write("Example: 1987, 2000, 2015")
        elif selected_column == "sex":
            st.write("Example: male, female")
        elif selected_column == "age":
            st.write("Example: 15-24 years, 75+ years")
        elif selected_column == "suicides_no":
            st.write("Example: 23, 150, 420")
        elif selected_column == "population":
            st.write("Example: 1,000, 150,000, 2,500,000")
        elif selected_column == "suicides/100k pop":
            st.write("Example: 5.12, 20.5, 35.8")
        elif selected_column == "country-year":
            st.write("Example: Albania1987, India2005")
        elif selected_column == "gdp_for_year ($)":
            st.write("Example: 1,234,567,890, 987,654,321")
        elif selected_column == "gdp_per_capita ($)":
            st.write("Example: 8370, 25000, 50000")
        elif selected_column == "generation":
            st.write("Example: Boomers, Generation X, Millennials")
        elif selected_column == "suicide_rate":
            st.write("Example: 0.50%")

    if __name__ == "__main__":
        main()

if page == "KPI's Dashboard":

    # Basic KPIs
    total_country=df.country.nunique()
    Max_suicides=df.groupby('country')['suicides_no'].sum().max()
    Min_suicides=df.groupby('country')['suicides_no'].sum().min()
    avg_suicides_per_sex = df.groupby('sex')['suicides/100k pop'].count().mean()
    avg_suicides_per_country = df.groupby('country')['suicides/100k pop'].count().mean()
    # Display KPIs in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Country", f"{total_country:,}")
    col2.metric("Max_suicides", f"{Max_suicides:,.2f}")
    col3.metric("Min_suicides", f"{Min_suicides:,}")

    col4,col5=st.columns(2)
    col4.metric("Avg Suicides Per Sex", f"{avg_suicides_per_sex:.2f}")
    col5.metric("Avg Suicides Per Country",f"{avg_suicides_per_country:,.2f}")
    st.write('---')
    st.subheader('📈 Total country gdp_per_capita($)')
    country_gdp = df.groupby('country')['gdp_per_capita ($)'].sum().reset_index()
    st.plotly_chart(px.bar(data_frame=country_gdp,x='country',y='gdp_per_capita ($)',color_discrete_sequence=['blue'],text_auto=True,title='country gdp_per_capita($)').update_xaxes(categoryorder='max descending'))
    st.write('---')
    st.subheader('💳 Suicides Rate Per Sex')
    sex_rate=df.groupby('sex')['suicide_rate'].sum().reset_index().sort_values(by='suicide_rate',ascending=False)
    st.plotly_chart(px.bar(data_frame=sex_rate,x='sex',y='suicide_rate',title='Suicides_Rate per Sex',text_auto=True,color_discrete_sequence=['red']))
    st.write('---')
    st.subheader('🔥 Average Suicide Rate per 100k Age')
    age=df.groupby('age')['suicides/100k pop'].mean().round(2).reset_index()
    st.plotly_chart(px.bar(data_frame=age,x='age',y='suicides/100k pop',color_discrete_sequence=['yellow'],text_auto=True,title='Average Suicide Rate per 100k Age'))
if page=='Suicides Report':
    all_year=df.year.unique().tolist()+['All Year']
    year=st.sidebar.selectbox("year",all_year)
    if year !='All Year':
        df=df[df.year==year]
    st.subheader('Filtered Data')
    st.dataframe(df)   
    st.write('---')
    st.subheader("🔥 Top Country by gdp_per_capita($)")
    Top_N=st.sidebar.slider('Top N',min_value=1,max_value=30,value=5)
    country_count=df.groupby('country')['gdp_per_capita ($)'].sum().reset_index().head(Top_N)  
    st.plotly_chart(px.bar(data_frame=country_count,x='country',y='gdp_per_capita ($)',color_discrete_sequence=['blue'],text_auto=True,title='country gdp_per_capita($)').update_xaxes(categoryorder='max descending'))

import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/5/55/Olympic_rings_with_transparent_rims.svg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis','Athlete-wise Analysis')
)

# Show full preprocessed data (for debugging or viewing)
# You can remove/comment this in production
st.dataframe(df)

if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years, countries = helper.country_year_list(df)
    select_year = st.sidebar.selectbox("Select Year", years)
    select_country = st.sidebar.selectbox("Select Country", countries)

    medal_tally = helper.fetch_medal_tally(df,select_year,select_country)
    if select_year == 'overall' and select_country == 'overall':
        st.title('Overall Tally')
    if select_year != 'overall' and select_country == 'overall':
        st.title('Medal Tally in ' + select_country == 'overall')
    if select_year == 'overall' and select_country != 'overall':
        st.title(select_country + 'overall performance')
    if select_year != 'overall' and select_country != 'overall':
        st.title(select_country + 'performance in ' + str(select_year) + "olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    edition = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(edition)

    with col2:
        st.header('Hosts')
        st.title(cities)

    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)

    with col2:
        st.header('Name')
        st.title(athletes)

    with col3:
        st.header('region')
        st.title(nations)

    nation_over_time = helper.data_over_time(df,'region')
    fig = px.line(nation_over_time, x="Edition", y="region")
    st.title("Participation Nation Over the Year")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events Over the Year")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time,x="Edition", y="Name")
    st.title("Athletes Over the Year")
    st.plotly_chart(fig)

    st.title("No of Events over time")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax=sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
    st.pyplot(fig)


    st.title("most successful athlete")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')
    selected_sport=st.selectbox('Select Sport',sport_list)
    x=helper.most_sucessful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country wise analysis")
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select Country',country_list)
    country_df=helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country+"Medal Tally Over the Year")
    st.plotly_chart(fig)


    st.title("Top 10 athlete of" + selected_country)
    top10_df=helper.most_sucessful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    # Extracting age data
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    # Creating the distribution plot
    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
        show_hist=False,
        show_rug=False
    )

    # Displaying the plot
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    st.title("men-vs-women participation over the years")
    final=helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)



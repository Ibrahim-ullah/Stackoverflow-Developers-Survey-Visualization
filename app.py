import streamlit as st
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np
import operator
import pandas as pd
import plotly.offline as py
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
from plotly import tools
from plotly.tools import FigureFactory as ff
import pycountry
import random
import squarify
from collections import Counter
import warnings
warnings.filterwarnings('ignore')
import altair as alt
from functions import *
    






color_brewer = ['#57B8FF','#B66D0D','#009FB7','#FBB13C','#FE6847','#4FB5A5','#8C9376','#F29F60','#8E1C4A','#85809B','#515B5D','#9EC2BE','#808080','#9BB58E','#5C0029','#151515','#A63D40','#E9B872','#56AA53','#CE6786','#449339','#2176FF','#348427','#671A31','#106B26','008DD5','#034213','#BC2F59','#939C44','#ACFCD9','#1D3950','#9C5414','#5DD9C1','#7B6D49','#8120FF','#F224F2','#C16D45','#8A4F3D','#616B82','#443431','#340F09']





st.title("Stackoverflow Developer Survey")
st.markdown("This dashboard provides analyses of the developer for a particular country")\
    
    



@st.cache(persist = True)
def load_data(nrows):
    data1 = pd.read_csv("data/data1.csv",nrows=nrows)
    data2 = pd.read_csv("data/data2.csv",nrows=nrows)
    frames = [data1, data2]
    data = pd.concat(frames, axis=0, join='outer', ignore_index=False, keys=None,
          levels=None, verify_integrity=False, copy=True)
    return data


data= load_data(10000)
copy_data = data.copy()



# Sidebar for which country to select
st.header("Select the country you want to perform analysis on")
select = st.sidebar.selectbox("Select the country",['United States','United Kingdom','Banlgadesh','South Africa','Kenya',
'Nigeria','India','Spain','Croatia','Netherlands','Israel','Sweden','Chile','Australia','Greece','Poland','Belgium',
'Argentina','Germany','Russian Federation','Indonesia','Ireland','France','Ukraine','Denmark','Dominican Republic',
'China','Latvia','Algeria','Colombia','Japan','Finland','Romania','Brazil','Bulgaria','Nepal','Canada',
'Jordan','Pakistan','Portugal','Italy','New Zealand','Turky','Czech Republic','Egypt','Austria','Thailand','Slovakia',
'Lebanon','South Korea','United Arab Emirates','Qatar','Bosnia and Herzegovina','Malaysia','Mexico','Serbia','Philippines'])

    
    




agree = st.checkbox('Did you select the country you want to see analysis for otherwise the default countries analysis will be shown')
if agree:
    df= data[data['Country'] == select]

    st.header("Male and Female who code as a Hobby")
    data_hobby = df[['Hobby','Gender']].dropna()

    trace1 = go.Bar(
        x=['Female', 'Male'],
        y=[data_hobby[(data_hobby['Gender'] == 'Female') & (data_hobby['Hobby'] == 'Yes')].count()[0], data_hobby[(data_hobby['Gender'] == 'Male') & (data_hobby['Hobby'] == 'Yes')].count()[0]],
        name='Yes',
        opacity=0.6
)
    trace2 = go.Bar(
        x=['Female', 'Male'],
        y=[data_hobby[(data_hobby['Gender'] == 'Female') & (data_hobby['Hobby'] == 'No')].count()[0], data_hobby[(data_hobby['Gender'] == 'Male') & (data_hobby['Hobby'] == 'No')].count()[0]],
        name='No',
        opacity=0.6
)

    data_combined_hobby = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
)

    fig = go.Figure(data=data_combined_hobby, layout=layout)
    st.plotly_chart(fig)
    

    st.subheader("How much people earn in your country")
    plt.hist(df['ConvertedSalary'],bins=5)
    plt.ticklabel_format(useOffset=False)
    plt.xlabel('Salary')
    plt.ylabel('Number of people')
    st.pyplot()
    
  
    
    st.subheader("Treemap of Employment in your country")
    treemap('Employment',df)
    

    st.subheader("Treemap of FormalEducation in your country")
    treemap('FormalEducation',df)

    


    st.subheader("How many respondants contribute to the opensource community")
    simple_graph('OpenSource',df,'pie')

    st.subheader("Favourite IDE's By Developer")
    simple_graph('IDE',df,'barh',10)

    st.subheader("How many times Developers Checkin code")
    simple_graph('CheckInCode',df,'barv',10)

    st.subheader("Different types of roles Developers have")
    simple_graph('DevType',df,'barv',10)

    st.subheader("Top 10 version control software")
    simple_graph('VersionControl',df,'barh',10)

    st.subheader("How many people use monitor")
    simple_graph('NumberMonitors',df,'barv',10)

    st.subheader("How productive developers are")
    simple_graph('TimeFullyProductive',df,'barv',10)

    st.subheader("Do you feel a sense of keenship towards other developer")
    simple_graph('AgreeDisagree1',df,'barv',10)

    st.subheader("Do you think you compete with your peer")
    simple_graph('AgreeDisagree2',df,'barv',10)

    
    st.subheader("Do you think you are not as good as most of your peer's in programming")
    simple_graph('AgreeDisagree3',df,'barv',10)


    st.subheader("Top 10 languages worked in the year 2018")
    viz_chart_languageworkedwith(df,'LanguageWorkedWith')

    st.subheader("Top 10 languages to work with in the year 2019")
    viz_chart(df,'LanguageDesireNextYear')

    st.subheader("Top 10 Databases worked in the year 2018")
    viz_chart(df,"DatabaseWorkedWith")

    st.subheader("Top 10 Desired Databases to work with in the year 2019")
    viz_chart(df,"DatabaseDesireNextYear")


    st.subheader("Top 10 platforms worked in the year 2018")
    viz_chart(df,'PlatformWorkedWith')

    st.subheader("Top 10 Desired Platforms to work with in the year 2019")
    viz_chart(df,'PlatformDesireNextYear')
   

    
    st.header("Time takes to get a job after a Bootcamp")
    pie_with_percentage(df,"TimeAfterBootcamp")
    
    st.header("Job Satisfaction")
    pie_with_percentage(df,"JobSatisfaction")
    
    st.header("Career Satisfaction")
    pie_with_percentage(df,"CareerSatisfaction")
    
    st.header("Future Aspirations")
    pie_with_percentage(df,"HopeFiveYears")
    
    st.header("Job Search Status")
    pie_with_percentage(df,"JobSearchStatus")
     
    st.header("Last New Job")
    pie_with_percentage(df,"LastNewJob")
    
    st.header("Time since last CV update")
    pie_with_percentage(df,"UpdateCV")
    
    
    st.header("Salary Type")
    pie_with_percentage(df,"SalaryType")
    
    
    
    
    st.header("What do developes look for when assessing a job")
    factor_list = ["The industry that I'd be working in","The financial performance or funding status of the company or organization","The specific department or     team I'd be working on","The languages, frameworks, and other technologies I'd be working with","The compensation and benefits offered","The office environment     or company culture","The opportunity to work from home/remotely","Opportunities for professional development","The diversity of the company or     organization","How widely used or impactful the product or service I'd be working on is"]
    mean_list = [df["AssessJob{}".format(i)].dropna().mean() for i in range(1,11)]
    assess_job = pd.DataFrame()
    assess_job["Factors"] = factor_list
    assess_job["Mean_Score"] = mean_list
    assess_job["Rank"] = assess_job["Mean_Score"].rank()
    df_accessjobs = assess_job.sort_values("Rank")

    trace1 = go.Table(
            header=dict(values=df_accessjobs.columns,
                    fill = dict(color='#C2D4FF'),
            align = ['left'] * 5),
        cells=dict(values=[df_accessjobs.Factors, df_accessjobs.Mean_Score, df_accessjobs.Rank],
                       fill = dict(color='#F5F8FF'),
                       align = ['left'] * 5))

    d = [trace1]

    st.plotly_chart(d)
    
    
    st.header("What kind of benefits do the developers want?")
    factor_list = ["Salary and/or bonuses","Stock options or shares","Health insurance","Parental leave","Fitness or wellness benefit","Retirement or pension         savings","Company-provided meals or snacks","Computer/office equipment allowance","Childcare benefit","Transportation benefit","Conference or education         budget"]
    mean_list = [df["AssessBenefits{}".format(i)].dropna().mean() for i in range(1,12)]
    assess_benefits = pd.DataFrame()
    assess_benefits["Factors"] = factor_list
    assess_benefits["Mean_Score"] = mean_list
    assess_benefits["Rank"] = assess_benefits["Mean_Score"].rank()
    df_accessbenefits = assess_benefits.sort_values("Rank")

    trace1 = go.Table(
            header=dict(values=df_accessbenefits.columns,
                    fill = dict(color='#AC68CC'),
                    align = ['left'] * 5),
            cells=dict(values=[df_accessbenefits.Factors, df_accessbenefits.Mean_Score, df_accessbenefits.Rank],
                       fill = dict(color='#D6B4E7'),
                       align = ['left'] * 5))

    d = [trace1]
    st.plotly_chart(d)
    

    st.header("Effect of Formal Education in Job Satisfaction")
    effect_of_jobsatisfaction(df,"FormalEducation")

    st.header("Effect of Company Size in Job Satisfaction")
    effect_of_jobsatisfaction(df,"CompanySize")
    
    st.header("Effect of Future Goals in Job Satisfaction")
    effect_of_jobsatisfaction(df,"HopeFiveYears")
    
    
    st.header("Effect of Coding Experience in Job Satisfaction")
    effect_of_jobsatisfaction(df,"YearsCoding")
    
    st.header("Effect of Age in Job Satisfaction")
    effect_of_jobsatisfaction(df,"Age")
    
    
    st.header("Is AI Dangerous")
    pie_with_percentage(df,"AIDangerous")
    
    st.header("What is the future of AI")
    pie_with_percentage(df,"AIFuture")
    
    
    
    
agree = st.checkbox('Do you want to see the analysis for developer all over the world')
if agree:
    
    st.header("Male and Female who code as a Hobby")
    data_hobby = data[['Hobby','Gender']].dropna()

    trace1 = go.Bar(
        x=['Female', 'Male'],
        y=[data_hobby[(data_hobby['Gender'] == 'Female') & (data_hobby['Hobby'] == 'Yes')].count()[0], data_hobby[(data_hobby['Gender'] == 'Male') & (data_hobby['Hobby'] == 'Yes')].count()[0]],
        name='Yes',
        opacity=0.6
)
    trace2 = go.Bar(
        x=['Female', 'Male'],
        y=[data_hobby[(data_hobby['Gender'] == 'Female') & (data_hobby['Hobby'] == 'No')].count()[0], data_hobby[(data_hobby['Gender'] == 'Male') & (data_hobby['Hobby'] == 'No')].count()[0]],
        name='No',
        opacity=0.6
)

    data_combined_hobby = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
)

    fig = go.Figure(data=data_combined_hobby, layout=layout)
    st.plotly_chart(fig)
    

    st.subheader("How much people earn in your country")
    plt.hist(data['ConvertedSalary'],bins=5)
    plt.ticklabel_format(useOffset=False)
    plt.xlabel('Salary')
    plt.ylabel('Number of people')
    st.pyplot()
    
    #Treemap of Developers all over the world
    #which indicates the number of developer needed in a single country
    st.subheader("Treemap of Developers all over the world")
    treemap('Country',copy_data)
    
    
    st.subheader("Treemap of Employment in your country")
    treemap('Employment',data)
    

    st.subheader("Treemap of FormalEducation in your country")
    treemap('FormalEducation',data)

    


    st.subheader("How many respondants contribute to the opensource community")
    simple_graph('OpenSource',data,'pie')

    st.subheader("Favourite IDE's By Developer")
    simple_graph('IDE',data,'barh',10)

    st.subheader("How many times Developers Checkin code")
    simple_graph('CheckInCode',data,'barv',10)

    st.subheader("Different types of roles Developers have")
    simple_graph('DevType',data,'barv',10)

    st.subheader("Top 10 version control software")
    simple_graph('VersionControl',data,'barh',10)

    st.subheader("How many people use monitor")
    simple_graph('NumberMonitors',data,'barv',10)

    st.subheader("How productive developers are")
    simple_graph('TimeFullyProductive',data,'barv',10)

    st.subheader("Do you feel a sense of keenship towards other developer")
    simple_graph('AgreeDisagree1',data,'barv',10)

    st.subheader("Do you think you compete with your peer")
    simple_graph('AgreeDisagree2',data,'barv',10)

    
    st.subheader("Do you think you are not as good as most of your peer's in programming")
    simple_graph('AgreeDisagree3',data,'barv',10)


    st.subheader("Top 10 languages worked in the year 2018")
    viz_chart_languageworkedwith(data,'LanguageWorkedWith')

    st.subheader("Top 10 languages to work with in the year 2019")
    viz_chart(data,'LanguageDesireNextYear')

    st.subheader("Top 10 Databases worked in the year 2018")
    viz_chart(data,"DatabaseWorkedWith")

    st.subheader("Top 10 Desired Databases to work with in the year 2019")
    viz_chart(data,"DatabaseDesireNextYear")


    st.subheader("Top 10 platforms worked in the year 2018")
    viz_chart(data,'PlatformWorkedWith')

    st.subheader("Top 10 Desired Platforms to work with in the year 2019")
    viz_chart(data,'PlatformDesireNextYear')
    
    st.subheader("Mean salary in different countries")
    trace1 = {"x": [copy_data["ConvertedSalary"][copy_data["Country"]==i].mean() for i in copy_data["Country"].value_counts().index],
          "y": copy_data["Country"].value_counts().index,
          "marker": {"color": "pink", "size": 12},
          "mode": "markers",
          "name": "Mean Salary",
          "type": "scatter"
    }

    d = [trace1]
    layout = {"title": "Mean salary in different countries",
          "xaxis": {"title": "Converted Salary", },
          "yaxis": {"title": "Country"},
          "height":3500,
          "margin":dict(l=300)
         }

    fig = go.Figure(data=d, layout=layout)
    st.plotly_chart(fig)
    
    st.header("Time takes to get a job after a Bootcamp")
    pie_with_percentage(data,"TimeAfterBootcamp")
    
    st.header("Job Satisfaction")
    pie_with_percentage(data,"JobSatisfaction")
    
    st.header("Career Satisfaction")
    pie_with_percentage(data,"CareerSatisfaction")
    
    st.header("Future Aspirations")
    pie_with_percentage(data,"HopeFiveYears")
    
    st.header("Job Search Status")
    pie_with_percentage(data,"JobSearchStatus")
     
    st.header("Last New Job")
    pie_with_percentage(data,"LastNewJob")
    
    st.header("Time since last CV update")
    pie_with_percentage(data,"UpdateCV")
    
    
    st.header("Salary Type")
    pie_with_percentage(data,"SalaryType")
    
    
    
    
    st.header("What do developes look for when assessing a job")
    factor_list = ["The industry that I'd be working in","The financial performance or funding status of the company or organization","The specific department or     team I'd be working on","The languages, frameworks, and other technologies I'd be working with","The compensation and benefits offered","The office environment     or company culture","The opportunity to work from home/remotely","Opportunities for professional development","The diversity of the company or     organization","How widely used or impactful the product or service I'd be working on is"]
    mean_list = [data["AssessJob{}".format(i)].dropna().mean() for i in range(1,11)]
    assess_job = pd.DataFrame()
    assess_job["Factors"] = factor_list
    assess_job["Mean_Score"] = mean_list
    assess_job["Rank"] = assess_job["Mean_Score"].rank()
    df_accessjobs = assess_job.sort_values("Rank")

    trace1 = go.Table(
            header=dict(values=df_accessjobs.columns,
                    fill = dict(color='#C2D4FF'),
            align = ['left'] * 5),
        cells=dict(values=[df_accessjobs.Factors, df_accessjobs.Mean_Score, df_accessjobs.Rank],
                       fill = dict(color='#F5F8FF'),
                       align = ['left'] * 5))

    d = [trace1]

    st.plotly_chart(d)
    
    
    st.header("What kind of benefits do the developers want?")
    factor_list = ["Salary and/or bonuses","Stock options or shares","Health insurance","Parental leave","Fitness or wellness benefit","Retirement or pension         savings","Company-provided meals or snacks","Computer/office equipment allowance","Childcare benefit","Transportation benefit","Conference or education         budget"]
    mean_list = [data["AssessBenefits{}".format(i)].dropna().mean() for i in range(1,12)]
    assess_benefits = pd.DataFrame()
    assess_benefits["Factors"] = factor_list
    assess_benefits["Mean_Score"] = mean_list
    assess_benefits["Rank"] = assess_benefits["Mean_Score"].rank()
    df_accessbenefits = assess_benefits.sort_values("Rank")

    trace1 = go.Table(
            header=dict(values=df_accessbenefits.columns,
                    fill = dict(color='#AC68CC'),
                    align = ['left'] * 5),
            cells=dict(values=[df_accessbenefits.Factors, df_accessbenefits.Mean_Score, df_accessbenefits.Rank],
                       fill = dict(color='#D6B4E7'),
                       align = ['left'] * 5))

    d = [trace1]
    st.plotly_chart(d)
    

    st.header("Effect of Formal Education in Job Satisfaction")
    effect_of_jobsatisfaction(data,"FormalEducation")

    st.header("Effect of Company Size in Job Satisfaction")
    effect_of_jobsatisfaction(data,"CompanySize")
    
    st.header("Effect of Future Goals in Job Satisfaction")
    effect_of_jobsatisfaction(data,"HopeFiveYears")
    
    
    st.header("Effect of Coding Experience in Job Satisfaction")
    effect_of_jobsatisfaction(data,"YearsCoding")
    
    st.header("Effect of Age in Job Satisfaction")
    effect_of_jobsatisfaction(data,"Age")
    
    
    st.header("Is AI Dangerous")
    pie_with_percentage(data,"AIDangerous")
    
    st.header("What is the future of AI")
    pie_with_percentage(data,"AIFuture")

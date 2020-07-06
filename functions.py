import streamlit as st
import numpy as np
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
    
    
color_brewer = ['#57B8FF','#B66D0D','#009FB7','#FBB13C','#FE6847','#4FB5A5','#8C9376','#F29F60','#8E1C4A','#85809B','#515B5D','#9EC2BE','#808080','#9BB58E','#5C0029','#151515','#A63D40','#E9B872','#56AA53','#CE6786','#449339','#2176FF','#348427','#671A31','#106B26','008DD5','#034213','#BC2F59','#939C44','#ACFCD9','#1D3950','#9C5414','#5DD9C1','#7B6D49','#8120FF','#F224F2','#C16D45','#8A4F3D','#616B82','#443431','#340F09']    
    
 
    
 
def remove_coma(val):
    value = val.replace(",","")
    return value

def random_colors(number_of_colors):
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
    return color

def remove_coma(val):
    value = val.replace(",","")
    return value

def get_list(col_name):
    full_list = ";".join(col_name)
    each_word = full_list.split(";")
    each_word = Counter(each_word).most_common()
    return pd.DataFrame(each_word)

def calculate_percent(val):
    return val/ len(df) *100


def simple_graph(dataframe,df,type_of_graph, top = 0):
    data_frame = df[dataframe].value_counts()
    layout = go.Layout()
    
    if type_of_graph == 'barh':
        top_category = get_list(df[dataframe].dropna())
        if top !=None:
            data = [go.Bar(
                x=top_category[1].head(top),
                y=top_category[0].head(top),
                orientation = 'h',
                marker=dict(color=random_colors(10), line=dict(color='rgb(8,48,107)',width=1.5,)),
                opacity = 0.6
            )]
        else:
            data = [go.Bar(
            x=top_category[1],
            y=top_category[0],
            orientation = 'h',
            marker=dict(color=random_colors(10), line=dict(color='rgb(8,48,107)',width=1.5,)),
            opacity = 0.6
        )]

    elif type_of_graph == 'barv':
        top_category = get_list(df[dataframe].dropna())
        if top !=None:
            data = [go.Bar(
                x=top_category[0].head(top),
                y=top_category[1].head(top),
                marker=dict(color=random_colors(10), line=dict(color='rgb(8,48,107)',width=1.5,)),
                opacity = 0.6
        )]
        else:
            data = [go.Bar(
                x=top_category[0],
                y=top_category[1],
                marker=dict(color=random_colors(10), line=dict(color='rgb(8,48,107)',width=1.5,)),
                opacity = 0.6
            )]      

    elif type_of_graph == 'pie':
        data = [go.Pie(
            labels = data_frame.index,
            values = data_frame.values,
            marker = dict(colors = random_colors(20)),
            textfont = dict(size = 20)
        )]
    
    elif type_of_graph == 'pie_':
        data = [go.Pie(
            labels = data_frame.index,
            values = data_frame.values,
            marker = dict(colors = random_colors(20)),
            textfont = dict(size = 20)
        )]
        layout = go.Layout(legend=dict(orientation="h"), autosize=False,width=700,height=700)
        pass
    
    fig = go.Figure(data = data, layout = layout)
    st.plotly_chart(fig)
    
def viz_chart_languageworkedwith(df,col):
    data = get_list(df[col].dropna())
    data = data[:10]
    data = data.reindex(index=data.index[::-1])

    size = np.array(data[1]*0.01)
    trace0 = go.Scatter(
        x=data[0],
        y=data[1],
        mode='markers',
        marker=dict(color = random_colors(10),size= size)
    )

    data = [trace0] 
    st.plotly_chart(data) 

   
def viz_chart(df,col):
    data = get_list(df[col].dropna())
    data = data[:10]
    data = data.reindex(index=data.index[::-1])

    size = np.array(data[1]*0.025)
    trace0 = go.Scatter(
        x=data[0],
        y=data[1],
        mode='markers',
        marker=dict(color = random_colors(10),size= size)
    )

    data = [trace0] 
    st.plotly_chart(data)
    
def treemap(col_name,df):
    color_brewer = ['#57B8FF','#B66D0D','#009FB7','#FBB13C','#FE6847','#4FB5A5','#8C9376','#F29F60','#8E1C4A','#85809B','#515B5D','#9EC2BE','#808080','#9BB58E','#5C0029','#151515','#A63D40','#E9B872','#56AA53','#CE6786','#449339','#2176FF','#348427','#671A31','#106B26','008DD5','#034213','#BC2F59','#939C44','#ACFCD9','#1D3950','#9C5414','#5DD9C1','#7B6D49','#8120FF','#F224F2','#C16D45','#8A4F3D','#616B82','#443431','#340F09']    
    country = df[col_name].dropna()
    for i in country.unique():
        if country[country == i].count() < 600:
            country[country == i] = 'Others'
    x = 0.
    y = 0.
    width = 50.
    height = 50.
    type_list = country.value_counts().index
    values = country.value_counts().values
    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)
   
       # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = color_brewer
    shapes = []
    annotations = []
    counter = 0
   
    for r in rects:
        shapes.append( 
           dict(
               type = 'rect', 
               x0 = r['x'], 
               y0 = r['y'], 
               x1 = r['x']+r['dx'], 
               y1 = r['y']+r['dy'],
               line = dict( width = 1 ),
               fillcolor = color_brewer[counter]
           ) 
       )
        annotations.append(
           dict(
               x = r['x']+(r['dx']/2),
               y = r['y']+(r['dy']/2),
               text = "{}".format(type_list[counter]),
               showarrow = False
       )
       )
        counter = counter + 1
        if counter >= len(color_brewer):
            counter = 0
   
       # For hover text
    trace0 = go.Scatter(
    x = [ r['x']+(r['dx']/2) for r in rects ], 
    y = [ r['y']+(r['dy']/2) for r in rects ],
    text = [ str(v) for v in values ], 
    mode = 'text',
    )
   
    layout = dict(
           height=600, 
           width=850,
           xaxis=dict(showgrid=False,zeroline=False),
           yaxis=dict(showgrid=False,zeroline=False),
           shapes=shapes,
           annotations=annotations,
           hovermode='closest',
           font=dict(color="#FFFFFF"),
           margin = go.Margin(
           l=0,
           r=0,
           pad=0
           )
           )
   
       # With hovertext
    figure = dict(data=[trace0], layout=layout)
    st.plotly_chart(figure)
    
    
def pie_with_percentage(df,col_name):
    color_brewer = ['#57B8FF','#B66D0D','#009FB7','#FBB13C','#FE6847','#4FB5A5','#8C9376','#F29F60','#8E1C4A','#85809B','#515B5D','#9EC2BE','#808080','#9BB58E','#5C0029','#151515','#A63D40','#E9B872','#56AA53','#CE6786','#449339','#2176FF','#348427','#671A31','#106B26','008DD5','#034213','#BC2F59','#939C44','#ACFCD9','#1D3950','#9C5414','#5DD9C1','#7B6D49','#8120FF','#F224F2','#C16D45','#8A4F3D','#616B82','#443431','#340F09']
    random.shuffle(color_brewer)
    fig = {
          "data": [
            {
              "values": df[col_name].dropna().value_counts().values,
              "labels": df[col_name].dropna().value_counts().index,
              "domain": {"x": [0, .95]},
              "name": col_name,
              "hoverinfo":"label+percent+name",
              "hole": 0.9,
              "type": "pie",
              "marker": {"colors": [i for i in reversed(color_brewer)]},
              "textfont": {"color": "#FFFFFF"}}],
      "layout": {
            "title":"Time to get a job since  bootcamp?",
            "paper_bgcolor": "#D3D3D3",
            "plot_bgcolor": "#D3D3D3",
            "annotations": [
            {
                "font": {
                    "size": 20
                },
                "showarrow": False,
                "text": "Amount of time",
                "x": 0.47,
                "y": 0.5
            }
        ],
    "legend": dict(orientation="h")
    }
}
    st.plotly_chart(fig)
    
    
    
def effect_of_jobsatisfaction(df,col_name):
    trace1 = go.Bar(
        y=df[col_name][df["JobSatisfaction"] == "Extremely dissatisfied"].value_counts().index,
        x=df[col_name][df["JobSatisfaction"] == "Extremely dissatisfied"].value_counts().values,
        name='Extremely dissatisfied',
        orientation = 'h',
        marker = dict(
        color = 'rgba(246, 78, 139, 0.6)',
        line = dict(
            color = 'rgba(246, 78, 139, 1.0)',
            width = 3)
    )
)
    trace2 = go.Bar(
        y=df[col_name][df["JobSatisfaction"] == "Moderately dissatisfied"].value_counts().index,
        x=df[col_name][df["JobSatisfaction"] == "Moderately dissatisfied"].value_counts().values,name='Moderately dissatisfied',orientation = 'h',
        marker = dict(
        color = 'rgba(58, 71, 80, 0.6)',
        line = dict(
            color = 'rgba(58, 71, 80, 1.0)',
            width = 3)
    )
)
    trace3 = go.Bar(
        y=df[col_name][df["JobSatisfaction"] == "Slightly dissatisfied"].value_counts().index,
        x=df[col_name][df["JobSatisfaction"] == "Slightly dissatisfied"].value_counts().values,
        name='Slightly dissatisfied',
        orientation = 'h',
        marker = dict(
        color = 'rgba(255, 225, 79, 0.6)',
        line = dict(
            color = 'rgba(255, 225, 79, 1.0)',
            width = 3)
    )
)
    trace4 = go.Bar(
        y=df[col_name][df["JobSatisfaction"] == "Neither satisfied nor dissatisfied"].value_counts().index,
        x=df[col_name][df["JobSatisfaction"] == "Neither satisfied nor dissatisfied"].value_counts().values,name='Neither satisfied nor dissatisfied',
        orientation = 'h',
        marker = dict(
        color = 'rgba(180, 49, 49, 0.6)',
        line = dict(
            color = 'rgba(180, 49, 49, 1.0)',
            width = 3)
    )
)
    trace5 = go.Bar(
        y=df[col_name][df["JobSatisfaction"] == "Slightly satisfied"].value_counts().index,
        x=df["FormalEducation"][df["JobSatisfaction"] == "Slightly satisfied"].value_counts().values,name='Slightly satisfied',orientation = 'h',
        marker = dict(
        color = 'rgba(49, 102, 191, 0.6)',
        line = dict(
            color = 'rgba(49, 102, 191, 1.0)',
            width = 3)
    )
)
    trace6 = go.Bar(
        y=df[col_name][df["JobSatisfaction"] == "Moderately satisfied"].value_counts().index,
        x=df["FormalEducation"][df["JobSatisfaction"] == "Moderately satisfied"].value_counts().values,
        name='Moderately satisfied',
        orientation = 'h',
        marker = dict(
        color = 'rgba(245, 157, 22, 0.6)',
        line = dict(
            color = 'rgba(245, 157, 22, 1.0)',
            width = 3)
    )
)
    trace7 = go.Bar(
        y=df[col_name][df["JobSatisfaction"] == "Extremely satisfied"].value_counts().index,
        x=df[col_name][df["JobSatisfaction"] == "Extremely satisfied"].value_counts().values,
       name='Extremely satisfied',
        orientation = 'h',
        marker = dict(
        color = 'rgba(158, 251, 71, 0.6)',
        line = dict(
            color = 'rgba(158, 251, 71, 1.0)',
            width = 3)
    )
)

    d = [trace1, trace2,trace3,trace4,trace5,trace6,trace7]
    layout = go.Layout(
        barmode='stack',
        margin=go.Margin(
        l=240
    ),
        title="Effect of formal education on job satisfaction"
)

    fig = go.Figure(data=d, layout=layout)
    st.plotly_chart(fig)

   
   
   
   
   
   
   

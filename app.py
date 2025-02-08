import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import dash_daq as daq
from plotly.subplots import make_subplots

data_cplus_orig: pd.DataFrame = pd.read_csv("c_plus.csv")
data_cplus = data_cplus_orig[(data_cplus_orig["Year"] >= 1900)]
data_a_orig: pd.DataFrame = pd.read_csv("Australia.csv")
data_a = data_a_orig[(data_a_orig["Year"] >= 1900)]


color_map = {  
    'Invalid': '#E15F99',     
    'Summer': '#705EFF',      
    'Winter': '#4FCF91',      
    'Spring': '#E0533D',      
    'Autumn': '#A94DFF',         
}

color_map_fatal = {
    'Y': '#705EFF',
    'N': '#E0533D',
    'Unknown': '#4FCF91', 
        
}

color_map_activity = {
    'Unknown': '#705EFF', 
    'Swimming': '#E0533D', 
    'Surfing': '#4FCF91', 
    'Fishing': '#A94DFF',
    'Diving': '#F3A356',
    'Bathing': '#5FD2F4',
        
}

color_gender = {
    'M': '#705EFF',
    'UnknownN': '#E0533D',
    'F': '#4FCF91', 
        
}


# For the mini sunbursts
australiadc = data_a.fillna({'State': 'Unknown', 'Gender': 'Unknown', 'Activity': 'Unknown',"Fatal":"Unknown"})
filter = ['Swimming', 'Diving',"Fishing","Surfing","Bathing","Unknown"]
filtered_rows =  australiadc[australiadc['Activity'].isin(filter)]
df_merged = filtered_rows[['State', 'Activity',"Gender","Fatal","Season","Type"]]
   
# For the bar plots
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[
        [{"type": "xy"}, {"type": "xy"}],  # Row 1
        [{"type": "xy"},{"type": "xy"}]  # Row2
    ]
)

# Count Activity
filtera = ["Bathing", "Diving", "Fishing", "Surfing", "Swimming", "Unknown"]
filtered_rowsa =  data_a[data_a['Activity'].isin(filtera)]

data_activity = {
    "Activity": ["Bathing", "Diving", "Fishing", "Surfing", "Swimming", "Unknown"],
    "Counts": [0, 0, 0, 0, 0, 0]
}

df_activity = pd.DataFrame(data_activity)

i=0
for i in range(len(filtera)):
    counts = (filtered_rowsa['Activity'] == filtera[i]).sum()
    df_activity.loc[i, "Counts"] = counts
    
# Count Fatal
filterf = ["Y","N","Unknown"]
filtered_rowsf =  data_a[data_a['Fatal'].isin(filterf)]

data_fatal = {
    "Fatal": ["Yes", "No", "Unknown"],
    "Counts": [0, 0, 0]
}

df_fatal = pd.DataFrame(data_fatal)

i=0
for i in range(len(filterf)):
    counts = (filtered_rowsf['Fatal'] == filterf[i]).sum()
    df_fatal.loc[i, "Counts"] = counts
    
# Count State
filters = ["New South Wales","Northern Territory","Queensland","South Australia","Tasmania","Torres Strait","Victoria","Western Australia"]
filtered_rowss =  data_a[data_a['State'].isin(filters)]

data_state = {
    "State": ["New South Wales","Northern Territory","Queensland","South Australia","Tasmania","Torres Strait","Victoria","Western Australia"],
    "Counts": [0, 0, 0, 0, 0, 0, 0, 0]
}

df_state = pd.DataFrame(data_state)

i=0
for i in range(len(filters)):
    counts = (filtered_rowss['State'] == filters[i]).sum()
    df_state.loc[i, "Counts"] = counts

# Count Season
filterse = ["Spring","Winter","Summer","Autumn"]
filtered_rowsse =  data_a[data_a['Season'].isin(filterse)]

data_season = {
    "Season": ["Spring","Winter","Summer","Autumn"],
    "Counts": [0,0,0,0]
}

df_season = pd.DataFrame(data_season)

i=0
for i in range(len(filterse)):
    counts = (filtered_rowsse['Season'] == filterse[i]).sum()
    df_season.loc[i, "Counts"] = counts

# Activity
bar_fig1 = px.bar(df_activity.sort_values(by='Counts', ascending=False), x='Activity', y='Counts')
for trace in bar_fig1.data:
    
    bar_fig1.update_traces(
        hovertemplate="Activity: %{x}<br>" +
                  "Counts: %{y}<extra></extra>" )
    
    fig.add_trace(trace, row=1, col=1)
        


# Fatal
bar_fig2 = px.bar(df_fatal.sort_values(by='Counts', ascending=False), x='Fatal', y='Counts',)
for trace in bar_fig2.data:
    
    bar_fig2.update_traces(
        hovertemplate="Fatal: %{x}<br>" +
                  "Counts: %{y}<extra></extra>" )
    
    fig.add_trace(trace, row=1, col=2)
 
# State        
bar_fig4 = px.bar(df_state.sort_values(by='Counts', ascending=False), x='State', y="Counts")
for trace in bar_fig4.data:
    
    bar_fig4.update_traces(
        hovertemplate="State: %{x}<br>" +
                  "Counts: %{y}<extra></extra>" )
    
    fig.add_trace(trace, row=2, col=1)    
        
# Season
bar_fig3 = px.bar(df_season.sort_values(by='Counts', ascending=False), x='Season', y="Counts")
for trace in bar_fig3.data:
    
    bar_fig3.update_traces(
        hovertemplate="Season: %{x}<br>" +
                  "Counts: %{y}<extra></extra>" )
    
    fig.add_trace(trace, row=2, col=2)
        

fig_ = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=("Gender and Activity", "Fatal and Activity", "Type and Activity", "State and Activity"),
    specs=[
        [{"type": "Domain"}, {"type": "Domain"}],  # Row 1
        [{"type": "Domain"},{"type": "Domain"}]  # Row2
    ]
)

# Gender, Activity
suny = px.sunburst(
    df_merged,
    path=['Gender',"Activity"],  # Hierarchical levels for the chart
    title="Sunburst Chart",
    color='Gender',
    width=200,
    height=200,
)

suny2 = px.sunburst(
    df_merged,
    path=['Fatal',"Activity"],  # Hierarchical levels for the chart
    title="Sunburst Chart",
    color='Fatal',
    width=100,
    height=100,
)

# Type, Activity
australiadc = data_a.fillna({'State': 'Unknown', 'Gender': 'Unknown', 'Activity': 'Unknown',"Fatal":"Unknown"})
filter = ['Swimming', 'Diving',"Fishing","Surfing","Bathing","Unknown"]
filtered_rows =  australiadc[australiadc['Activity'].isin(filter)]
df_merged = filtered_rows[['State', 'Activity',"Gender","Fatal","Season","Type"]]
filter3 = ['Provoked', 'Unprovoked',"Invalid"]
filtered_rows3 =  df_merged[df_merged['Type'].isin(filter3)]                                                 
df_merged3 = filtered_rows3[['State', 'Activity',"Gender","Fatal","Season","Type"]]

suny3 = px.sunburst(
    df_merged3,
    path=['Type',"Activity"],  # Hierarchical levels for the chart
    title="Sunburst Chart",
    color='Type',
    color_discrete_map=color_map,
    width=100,
    height=100,
)

suny4 = px.sunburst(
    df_merged,
    path=['Season',"Activity"],  # Hierarchical levels for the chart
    title="Sunburst Chart",
    color='Season',
    width=100,
    height=100,
)
    
    
for trace in suny.data:
        fig_.add_trace(trace, row=1, col=1)
        
for trace in suny2.data:
        fig_.add_trace(trace, row=1, col=2)  

for trace in suny3.data:
        fig_.add_trace(trace, row=2, col=1)          

for trace in suny4.data:
        fig_.add_trace(trace, row=2, col=2)    

# For the large sunburst
fig_2 = make_subplots(
    rows=1,
    cols=1,
    specs=[
        [{"type": "Domain"}]  # Row2
    ]
)

sunyl = px.sunburst(
    df_merged,
    path=['Season',"State"],  # Hierarchical levels for the chart
    color_discrete_map=color_map,
    color='Season',
    width=100,
    height=100,
)


for trace in sunyl.data:
        fig_2.add_trace(trace, row=1, col=1)


# Count Species
filterspe = ["Unknown, length given","Unknown","White shark","Bronze whaler","Tiger shark","Wobbegong shark","Bull shark","Grey nurse shark","Invalid"]
filtered_rowsspe =  data_a[data_a['Species'].isin(filterspe)]
season_countsspe = filtered_rowsspe.groupby("Species").size()

data_species = {
    "Species": ["Unknown, length given","Bronze whaler","Bull shark","Grey nurse shark","Tiger shark","Unknown","White shark","Wobbegong shark","Invalid"],
    "Counts": [248, 71, 44, 41, 59, 464, 186, 56,101]
}

fig10 = px.pie(data_species, values='Counts', names='Species', color_discrete_sequence=["#600021", "#A60C2E", "#CA5F4E","#EAA681","#F8DCC6","#e3d5bf"])
    
available_years = data_cplus["Year"].unique()
labels = ["Spring", "Summer", "Autumn","Winter"]

map5 = px.scatter_mapbox(
        data_a,
        lat='Latitude',
        lon='Longitude',
        hover_name='Location',
        zoom=3,
        color="Season",
        mapbox_style='open-street-map',  # You can change the map style
)
    
map5.update_layout(
        autosize=True,
         title_text='Map Australia',
            width=900,height=650,
         )
    
# Output Season
filter2 = ['Summer', 'Autumn',"Spring","Winter"]
filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
column = filtered_rows2.loc[:, "Season"]
season_counts = column.value_counts()

output_values = season_counts.to_string(index=False)



# Initialize the Dash app
app = dash.Dash(__name__)


# Layout for the dashboard
app.layout = html.Div([

   html.Div([
       html.Div([
           html.P('Shark attacks global overview and target country Australia'),
       ]) ,
       
       html.Img(src=r'assets/shark.png', alt='image', className='menu_top_img'),
   ], className='menu_top' ),
   
   
   
html.Div([   
   
   
    
    dcc.Tabs([
        dcc.Tab(label='Overview', className='tabs1', children=[
           
            html.Div([  # first two graphs
           
            html.Div([

            dcc.Graph(id='graph'),
            dcc.Slider(
            id='year-range-slider',
            min=min(available_years),
            max=max(available_years),
            value=1900,
            marks = {int(year): str(year) if year in {1900,1950,2000,2024} else "" for year in available_years},
            tooltip={"placement": "bottom", "always_visible": True}, 
            included=True,
            className="custom-slider",
            step=None
        ), 
            
        html.Label('Main countries:'),
        dcc.Checklist(
            id="check",
            options=[{"label": "USA, Australia, South Africa", "value": "linear"}],
            value=["linear"],
        ), dcc.Markdown("This map sums up all the occurences from year to year. From year to year you can see USA, Australia and South Africa to be the predominant countries. With the deactivation of the so called key players all the remaining countries become more visible. In conjunction, seeing the size of the bubbles gives evidence of equal growth per year, which is also the sum of all counts. The main idea is to show growth and relationship.", dangerously_allow_html=True, className="markdown-style2"),
        
            ], className='div1'), # end of div
            
            
            html.Div([
                dcc.Graph(id='graph2', className='six columns'), dcc.Markdown("This graph represents the map in bars. Marked with white lines one can see the growth of the key players as one can perseve them in the map. With or without the key players again one can study the growth and relationship. If required, one can zoom into the very dense white lines in each bar.", className="markdown-style"),

        
            ], className='div1'),   # end of div

             ], style={ 'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-left': '0px', 'margin-right': '0px','vertical-align': 'middle'}),
             # end of two graphs
            
  
            html.Div([  # next two graphs
           
            html.Div([

            dcc.Graph(id='graph3', className='six columns'),
            dcc.Slider(
            id='year-range-slider3',
            min=min(available_years),
            max=max(available_years),
            value=1900,
            marks = {int(year): str(year) if year in {1900,1950,2000,2024} else "" for year in available_years},
            tooltip={"placement": "bottom", "always_visible": True}, 
            included=False,
            className="custom-slider",
            step=None
        ), dcc.Markdown("This map shows the occurrences in a year. To the side one can also see which country has occurrences, marked with a coloured circle. The main idea of this is to show that the mentioned key players from above have less weight in a single year, the size of the bubble gives evidence of the same counts per year. The idea again is to show growth and relationship.", className="markdown-style2"), 
            
            
            ],  className='div1'), # end of div
            
            
            html.Div([
                
            dcc.Graph(id='graph4', className='six columns'), dcc.Markdown("This non cumulative bar does the same as the cumulative bar but in conjunction with the non cumulative map. The main idea is the same and in addition counts are visible.", className="markdown-style2"),
            
        
            ], className='div1'),   # end of div

             ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-left': '0px', 'margin-right': '0px','vertical-align': 'middle'}),
            # end of next two graphs
            
            ]), # End of Tab 1
        
        
         # Start od Tab 2 
        dcc.Tab(label='Australia 1', className='tabs2', children=[
            html.Div([
                
               
                html.Div([
                
                dcc.Graph(id='graph5'),
                dcc.Tooltip(id="graph-tooltip"),
                
                        
    html.Div(
    children=[

        html.Div("Gender", style={"display": "inline-block", "margin-right": "10px"}),
        daq.ToggleSwitch(id="toggle2", value=False, style={"display": "inline-block"}, color="#FF5733", className='output_div2'), # Gender
        html.Div("Fatal:", style={"display": "inline-block", "margin-right": "10px"}),
        daq.ToggleSwitch(id="toggle3", value=False, style={"display": "inline-block"}, color="#FF5733", className='output_div2'), # Fatal
        html.Div("Activity:", style={"display": "inline-block", "margin-right": "10px"}),
        daq.ToggleSwitch(id="toggle4", value=False, style={"display": "inline-block"}, color="#FF5733", className='output_div2'), # Activity
       html.Div(id='output-div', className='output_div'), 
       
                dcc.Checklist(
                    id="check_color",
                    className='light',
                    options=[{"label": "Light", "value": "col"}],
                    value=["col"],
                ),
        
    ],
    style={"text-align": "center"}, 

    
),        dcc.Markdown("The main idea of this map is to show the occurrences for each season, gender, fatal (whether one has died) and activity. For better view switch the light on or off. Bellow the toggle buttons one can see the counts (see the legend for order). Please also click into the legend to make the occurrences appear or disappear. By zooming out, one can also see a density map. Here density is made visible by the clustering of points, also the formation of lines along the coastline. The selection of two toggle switches will reset the chart to the default setting which is the season.  ", className="markdown-style", dangerously_allow_html=True),

                ], className='div1'),
                
    html.Div([
        
        dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
            
        dcc.Tab(label='One sunburst', value='tab-1-example-graph', children=[
           
            dcc.Graph(id='graph13',     style={
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
        "height": "50vh"  # Full viewport height for vertical centering
    }, figure=fig_2),
        
            ]),
        
        dcc.Tab(label='Four sunbursts', value='tab-2-example-graph', children=[
            
            dcc.Graph(id='graph6'),
            
            ]),
    ]), dcc.Markdown("The main idea of these sunburst charts is to show count and relationship. Please click into the center of sunburst charts to make it fan out or fan in. The &#34;One sunburst&#34; tab presents one sunburst, which will change accordingly to the change of the toggle switches of the scatter map to the left. The &#34;Four sunbursts&#34; tab presents four sunburst charts which are unlinked to the toggle switches of the scatter map.", className="markdown-style"),
                    
                
                    ],className='div1'), # end of div            
                

        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-left': '0px', 'margin-right': '0px','vertical-align': 'middle'}), 
        
        
    html.Div([
                
               
html.Div([
    
    
    dcc.Graph(id='graph7'),  dcc.Markdown("The main idea of this treemap is to show the predominant activity and whether it is provoked, unprovoked, invalid, unknown. Please click into the treemap to make content expand.", className="markdown-style"),
    
    ],className='div1'), # end of div


html.Div([
        
    dcc.Graph(id='graph8', figure=fig),  dcc.Markdown("The main idea of these bar charts is to show the counts and support the other charts, the map, the sunbursts and the treemap.", className="markdown-style"),

    
    ],className='div1'), # end of div
   
        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-left': '0px', 'margin-right': '0px','vertical-align': 'middle'}), 
        

        ]), # End of Tab 2
        
        # Start od Tab 3
        dcc.Tab(label='Australia 2', className='tabs3', children=[
            html.Div([
                
                html.Div([
                
                dcc.Graph(id='graph12'),
                
        dcc.Markdown("The main idea of this pie chart is to view the most predominant shark specie around Australia. Although a shark attack is a shark attack, it might be of help to understand what to expect. Also taking the habitat into consideration, it is very possible that some of the species are more predominant than others around Australia. For some of the activities the physical strength or generally the superiority of a specie can be considered. This study is out-of-scope for this task.", className="markdown-style"),

                ], className='div1'),
                
              html.Div([
              html.Img(src=r'assets/shark_species3.png', alt='image', className='img_species'),
              
      dcc.Markdown("The main idea of this image is to view the physical presence of the specie. Comparing a human diver to the grey nurse shark gives a better idea of their sizes. As the Wobbegongs shark (carpet shark) would move on grounds, surfers could be less affected. Also depending on the amount of fishing and protection of a specie, other specie can become more dominant in an area.", className="markdown-style"),

              ], className='div1'),     
                
        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-left': '0px', 'margin-right': '0px','vertical-align': 'middle'}), 
        

        ]), # End of Tab 3
    
        # Start od Tab 4
        dcc.Tab(label='About', className='tabs', children=[
            html.Div([
                
                html.Div([
        dcc.Markdown("<b>Sources:</b><br>Maven Analytics. Shark Attacks. https://mavenanalytics.io/data-playground?order=date_added%2Cdesc&search=shark <br>(Access 01.09.2024)<br>Shark Research Institute. Global Shark Attach File. https://www.sharkattackfile.net/ (Access 10.10.2024)<br>OpenRefine. https://openrefine.org/ (Access 10.10.2024)<br>Dash Python User Guide. https://dash.plotly.com/ (Access 10.10.2024)<br>Shark Images. Google (Access 10.10.2024)<br>", className="markdown-style2",dangerously_allow_html=True),

                ], className='div1'),
                
              html.Div([

              
      dcc.Markdown("<b>Sources:</b><br>For description of used python code for generation of new data, please lookup the document.", className="markdown-style2",dangerously_allow_html=True),

              ], className='div1'),     
                
        ], style={'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-left': '0px', 'margin-right': '0px','vertical-align': 'middle'}), 
        

        ]), # End of Tab 4
    
    ],  className='tabs'), # end of tabs
    ], style={ 'display': 'flex', 'flex-direction': 'row', 'gap': '10px', 'margin-left': '0px', 'margin-right': '0px','vertical-align': 'middle'}), # end of third div

],
    
    style={
    'display': 'flex',
    'justify-content': 'center',
    'align-items': 'center',
    'text-align': 'center',
    'flex-direction': 'column',
    'zoom': '0.8'  # Zoom out
}
    
    ) # end of first div

# Callbacks for updating the first two graphs in "Overview"
@app.callback(
    [Output('graph', 'figure'), Output('graph2', 'figure')],
    [Input('check', 'value'), Input('year-range-slider', 'value')]
    
)

def update_map(selected_categories, year_range):
    fig = px.scatter_geo(data_cplus[(data_cplus['Year'] == year_range)], locations="Iso_alpha-3", color="Continent",
                      hover_name="Country", size="Cumulative Occurrences",
                      custom_data=data_cplus[(data_cplus['Year'] == year_range)],
                      projection="natural earth") 
    
    fig.update_geos(
    showcountries=True,           # Show country boundaries
    countrycolor="black",          # Color of country borders
    countrywidth=0.3               # Width of country borders
)
    
    
    fig.update_layout(
            title_text='Cumulative Map',
            width=900,height=500,
       
            )
    
    fig.update_traces(
    hovertemplate="Continent: %{customdata[5]}<br>" +
                  "Country: %{customdata[1]}<br>" +
                  "Cumulative Occurences: %{customdata[4]}<br>" +
                  "Occurences: %{customdata[3]}<br>" +
                  "Year: %{customdata[0]}<extra></extra>"
)
    bar1 = px.bar(data_cplus[(data_cplus['Year'] == year_range)].sort_values(by=["Cumulative Occurrences","Country"]), x="Cumulative Occurrences", y="Continent", orientation='h',
                  
                  custom_data=data_cplus[(data_cplus['Year'] == year_range)])
    bar=bar1    
    bar.update_layout(
            title_text='Cumulative Bar',
            barcornerradius=10,
            yaxis={'categoryorder':'total ascending'},
            width=700,height=450,
            
)
        
    bar.update_traces(
    hovertemplate="Continent: %{customdata[5]}<br>" +
                  "Country: %{customdata[1]}<br>" +
                  "Cumulative Occurences: %{customdata[4]}<br>" +
                  "Occurences: %{customdata[3]}<br>" +
                  "Year: %{customdata[0]}<extra></extra>" )
        
    
    
    if "linear" not in selected_categories:
        countries = ["Australia", "USA", "South Africa"]
        filtered_df = data_cplus[~data_cplus["Country"].isin(countries)]
        fig = px.scatter_geo(filtered_df[(data_cplus['Year'] == year_range)], locations="Iso_alpha-3", color="Continent",
                          hover_name="Country", size="Cumulative Occurrences",
                          projection="natural earth",
                          custom_data=filtered_df[(data_cplus['Year'] == year_range)])   
        fig.update_layout(
            title_text='Cumulative Map',
            )
        fig.update_geos(
        showcountries=True,           # Show country boundaries
        countrycolor="black",          # Color of country borders
        countrywidth=0.3               # Width of country borders
    )
        
        fig.update_traces(
        hovertemplate="Continent: %{customdata[5]}<br>" +
                      "Country: %{customdata[1]}<br>" +
                      "Cumulative Occurences: %{customdata[4]}<br>" +
                      "Occurences: %{customdata[3]}<br>" +
                      "Year: %{customdata[0]}<extra></extra>" )
    
        bar_df = data_cplus[~data_cplus["Country"].isin(countries)]
        bar = px.bar(bar_df[(bar_df['Year'] == year_range)].sort_values(by=["Cumulative Occurrences","Country"]), x="Cumulative Occurrences", y="Continent", orientation='h',
                     
                     custom_data=bar_df[(bar_df['Year'] == year_range)])
            
        bar.update_layout(
                title_text='Cumulative Map',
                barcornerradius=10,
                yaxis={'categoryorder':'total ascending'},
                width=700,height=450,
                )
        
        bar.update_traces(
        hovertemplate="Continent: %{customdata[5]}<br>" +
                  "Country: %{customdata[1]}<br>" +
                  "Cumulative Occurences: %{customdata[4]}<br>" +
                  "Occurences: %{customdata[3]}<br>" +
                  "Year: %{customdata[0]}<extra></extra>" )

        
        
    return fig, bar


# Callbacks for updating the next two graphs in "Overview"
@app.callback(
    [Output('graph3', 'figure'), Output("graph4","figure")],
    [Input('year-range-slider3', 'value')]
    
)

def update_map3(year_range3):
    filtered_df3 = data_cplus[data_cplus['Year'] == year_range3]
    
    fig3 = px.scatter_geo(filtered_df3, locations="Iso_alpha-3", color="Country",
                      hover_name="Country", size="Occurrences",
                      projection="natural earth",
                      custom_data=filtered_df3)   

    
    fig3.update_layout(
        title_text='Non-cumulative Map',
        width=900,height=700,
            )
    
    fig3.update_geos(
    showcountries=True,           # Show country boundaries
    countrycolor="black",          # Color of country borders
    countrywidth=0.3               # Width of country borders
)
    
    
    fig3.update_traces(
    hovertemplate="Continent: %{customdata[5]}<br>" +
                  "Country: %{customdata[1]}<br>" +
                  "Occurences: %{customdata[3]}<br>" +
                  "Year: %{customdata[0]}<extra></extra>" )
    
    bar2 = px.bar(data_cplus[(data_cplus['Year'] == year_range3)].sort_values(by=["Occurrences","Country"]), x="Occurrences", y="Continent", orientation='h', text_auto='Occurrences',
                  custom_data=data_cplus[(data_cplus['Year'] == year_range3)])
        
    bar2.update_layout(
            title_text='Non-cumulative Bar',
            barcornerradius=10,
            yaxis={'categoryorder':'total ascending'},
            width=700,height=450,)
        
    bar2.update_traces(
        hovertemplate="Continent: %{customdata[5]}<br>" +
                  "Country: %{customdata[1]}<br>" +
                  "Occurences: %{customdata[3]}<br>" +
                  "Year: %{customdata[0]}<extra></extra>" )

    
    return fig3, bar2


# Map and Sunbursts
@app.callback(
   [Output('graph5', 'figure'),Output('graph6', 'figure'), Output('graph13', 'figure'), Output('toggle2', 'value'), Output('toggle3', 'value'), Output('toggle4', 'value'), Output('output-div', 'children')],
    [Input('check_color', 'value'),Input('toggle2', 'value'),Input('toggle3', 'value'), Input('toggle4', 'value')]
)

def update_map5(input_color, input_toggle2, input_toggle3, input_toggle4):
    
    map5 = px.scatter_mapbox(
        data_a,
        lat='Latitude',
        lon='Longitude',
        hover_name='Location',
        zoom=3,
        color="Season",
        mapbox_style='open-street-map',  # You can change the map style
        
)
    
    map5.update_layout(
        hovermode="closest",
        autosize=True,
         title_text='Map Australia',
            width=900,height=650,
         )
    

    # Output Season
    filter2 = ['Summer', 'Autumn',"Spring","Winter"]
    filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
    column = filtered_rows2.loc[:, "Season"]
    season_counts = column.value_counts()

    output_values = season_counts.to_string(index=False)
    

    # Gender, Fatal, Activity with Light
    # Gender AND Fatal, back to default
    if "col" in input_color and input_toggle2 and input_toggle3:
        map5 = px.scatter_mapbox(
            data_a,
            lat='Latitude',
            lon='Longitude',
            hover_name='Location',
            zoom=3,
            color="Season",
            mapbox_style='open-street-map',  # You can change the map style
            custom_data=data_a[['Location', 'Season', 'Gender', 'Fatal', 'Species', 'Activity']]
            )
        
        # Output Season
        filter2 = ['Summer', 'Autumn',"Spring","Winter"]
        filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
        column = filtered_rows2.loc[:, "Season"]
        season_counts = column.value_counts()

        output_values = season_counts.to_string(index=False)
        
        
        map5.update_layout(
                    title_text='Map Australia',
                    width=900,height=650,
                    mapbox_style='open-street-map',)
        
        input_toggle2 = False
        input_toggle3 = False
        input_toggle4 = False
        
        sunyl = px.sunburst(
            df_merged,
            path=['Season',"State"],  # Hierarchical levels for the chart
            title="Season and State",
            color_discrete_map=color_map,
            color='Season',
        )
        
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Season and State',)
        
    # Gender AND Activity, back to default
    if "col" in input_color and input_toggle2 and input_toggle4:
        map5 = px.scatter_mapbox(
                data_a,
                lat='Latitude',
                lon='Longitude',
                hover_name='Location',
                zoom=3,
                color="Season",
                mapbox_style='open-street-map',  # You can change the map style
                )
        # Output Season
        filter2 = ['Summer', 'Autumn',"Spring","Winter"]
        filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
        column = filtered_rows2.loc[:, "Season"]
        season_counts = column.value_counts()
        output_values = season_counts.to_string(index=False)
        
        map5.update_layout(
                        title_text='Map Australia',
                        width=900,height=650,
                        mapbox_style='open-street-map',)
        input_toggle2 = False
        input_toggle3 = False
        input_toggle4 = False
        
        sunyl = px.sunburst(
            df_merged,
            path=['Season',"State"],  # Hierarchical levels for the chart
            title="Season and State",
            color_discrete_map=color_map,
            color='Season',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Season adn State',)
            
    # Fatal AND Activity, back to default
    if "col" in input_color and input_toggle3 and input_toggle4:
        map5 = px.scatter_mapbox(
                      data_a,
                      lat='Latitude',
                      lon='Longitude',
                      hover_name='Location',
                      zoom=3,
                      color="Season",
                      mapbox_style='open-street-map',  # You can change the map style
                      )
        # Output Season
        filter2 = ['Summer', 'Autumn',"Spring","Winter"]
        filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
        column = filtered_rows2.loc[:, "Season"]
        season_counts = column.value_counts()
        output_values = season_counts.to_string(index=False)
                  
                  
        map5.update_layout(
                              title_text='Map Australia',
                              width=900,height=650,
                              mapbox_style='open-street-map',)
        input_toggle2 = False
        input_toggle3 = False
        input_toggle4 = False      
        
        sunyl = px.sunburst(
            df_merged,
            path=['Season',"State"],  # Hierarchical levels for the chart
            title="Season and State",
            color_discrete_map=color_map,
            color='Season',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Season and State',)
            
            
     # Gender 
    if "col" in input_color and input_toggle2:
        map5 = px.scatter_mapbox(
                     data_a,
                     lat='Latitude',
                     lon='Longitude',
                     hover_name='Location',
                     zoom=3,
                     color="Gender",
                     mapbox_style='open-street-map',  # You can change the map style
                     )
                 
        # Output Gender
        filter2 = ['M', 'Unknown',"F"]
        filtered_rows2 =  data_a[data_a['Gender'].isin(filter2)]
        column = filtered_rows2.loc[:, "Gender"]
        season_counts = column.value_counts()
        output_values = season_counts.to_string(index=False)
                 
        map5.update_layout(
                             title_text='Map Australia',
                             width=900,height=650,
                             mapbox_style='open-street-map',)
        
        sunyl = px.sunburst(
            df_merged,
            path=["Gender","Fatal"],  # Hierarchical levels for the chart
            title="Gender and Fatal",
            color_discrete_map=color_gender,
            color='Gender',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Gender and Fatal',)
                 
    # Fatal 
    if "col" in input_color and input_toggle3:
        map5 = px.scatter_mapbox(
                        data_a,
                        lat='Latitude',
                        lon='Longitude',
                        hover_name='Location',
                        zoom=3,
                        color="Fatal",
                        mapbox_style='open-street-map',  # You can change the map style
                    )
                
        # Output Fatal
        filter2 = ['N', 'Y',"Unknown"]
        filtered_rows2 =  data_a[data_a['Fatal'].isin(filter2)]
        column = filtered_rows2.loc[:, "Fatal"]
        season_counts = column.value_counts()
                    
        output_values = season_counts.to_string(index=False)
                
        map5.update_layout(
                            title_text='Map Australia',
                            width=900,height=650,
                            mapbox_style='open-street-map',)
        
        sunyl = px.sunburst(
            df_merged,
            path=["Fatal","Activity"],  # Hierarchical levels for the chart
            title="Fatal and Activity",
            color_discrete_map=color_map_fatal,
            color='Fatal',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Fatal and Activity',)
                
    # Activity 
    if "col" in input_color and input_toggle4:
        filter = ['Diving', 'Fishing',"Surfing","Unknown","Bathing","Swimming"]
        filtered_rows =  data_a[data_a['Activity'].isin(filter)]
        sorted_df = filtered_rows.sort_values(by="Activity", ascending=False)
        map5 = px.scatter_mapbox(
                        sorted_df,
                        lat='Latitude',
                        lon='Longitude',
                        hover_name='Location',
                        zoom=3,
                        color="Activity",
                        mapbox_style='open-street-map',  # You can change the map style
                        )
                    
        # Output Actvity
        filter2 = ['Unknown', 'Swimming',"Surfing","Fishing","Diving","Bathing"]
        filtered_rows2 =  data_a[data_a['Activity'].isin(filter2)]
        column = filtered_rows2.loc[:, "Activity"]
        custom_order = ['Unknown', 'Swimming',"Surfing","Fishing","Diving","Bathing"]
        season_counts = filtered_rows2.groupby("Activity").size()
        season_counts = season_counts.reindex(filter2, fill_value=0)

        output_values = season_counts.values
        output_values = "Activity " + " ".join(map(str, output_values))
        
        map5.update_layout(dragmode="zoom")
        map5.show(config={"scrollZoom": True})
                  
        map5.update_layout(
                                title_text='Map Australia',
                                width=900,height=650,
                                mapbox_style='open-street-map',)


        sunyl = px.sunburst(
            df_merged,
            path=["Activity","Gender"],  # Hierarchical levels for the chart
            title="Activity and Gender",
            color_discrete_map=color_map_activity,
            color='Activity',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Activity and Gender',)           

    # Gender, Fatal, Activity without Light
    # Gender AND Fatal, back to default
    if "col" not in input_color and input_toggle2 and input_toggle3:
        map5 = px.scatter_mapbox(
            data_a,
            lat='Latitude',
            lon='Longitude',
            hover_name='Location',
            zoom=3,
            color="Season",
            mapbox_style='carto-darkmatter',  # You can change the map style
            )
        
        # Output Season
        filter2 = ['Summer', 'Autumn',"Spring","Winter"]
        filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
        column = filtered_rows2.loc[:, "Season"]
        season_counts = column.value_counts()

        output_values = season_counts.to_string(index=False)
        
        
        map5.update_layout(
                    title_text='Map Australia',
                    width=900,height=650,
                    mapbox_style='carto-darkmatter',)
        
        input_toggle2 = False
        input_toggle3 = False
        input_toggle4 = False
        
        sunyl = px.sunburst(
            df_merged,
            path=['Season',"State"],  # Hierarchical levels for the chart
            title="Season and State",
            color_discrete_map=color_map,
            color='Season',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Season and State',)
        
    # Gender AND Activity, back to default
    if "col" not in input_color and input_toggle2 and input_toggle4:
        map5 = px.scatter_mapbox(
                data_a,
                lat='Latitude',
                lon='Longitude',
                hover_name='Location',
                zoom=3,
                color="Season",
                mapbox_style='carto-darkmatter',  # You can change the map style
                )
        # Output Season
        filter2 = ['Summer', 'Autumn',"Spring","Winter"]
        filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
        column = filtered_rows2.loc[:, "Season"]
        season_counts = column.value_counts()
        output_values = season_counts.to_string(index=False)
        
        map5.update_layout(
                        title_text='Map Australia',
                        width=900,height=650,
                        mapbox_style='carto-darkmatter',)
        input_toggle2 = False
        input_toggle3 = False
        input_toggle4 = False
        
        sunyl = px.sunburst(
            df_merged,
            path=['Season',"State"],  # Hierarchical levels for the chart
            title="Season and State",
            color_discrete_map=color_map,
            color='Season',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Season and State',)
            
    # Fatal AND Activity, back to default
    if "col" not in input_color and input_toggle3 and input_toggle4:
        map5 = px.scatter_mapbox(
                      data_a,
                      lat='Latitude',
                      lon='Longitude',
                      hover_name='Location',
                      zoom=3,
                      color="Season",
                      mapbox_style='carto-darkmatter',  # You can change the map style
                      )
        # Output Season
        filter2 = ['Summer', 'Autumn',"Spring","Winter"]
        filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
        column = filtered_rows2.loc[:, "Season"]
        season_counts = column.value_counts()
        output_values = season_counts.to_string(index=False)
                  
                  
        map5.update_layout(
                              title_text='Map Australia',
                              width=900,height=650,
                              mapbox_style='carto-darkmatter',)
        input_toggle2 = False
        input_toggle3 = False
        input_toggle4 = False   
        
        sunyl = px.sunburst(
            df_merged,
            path=['Season',"State"],  # Hierarchical levels for the chart
            title="Season and State",
            color_discrete_map=color_map,
            color='Season',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Season and State',)



    
    fig_.update_layout(
                    width=900,height=650,
                    mapbox_style='carto-darkmatter',)
            
            
     # Gender 
    if "col" not in input_color and input_toggle2:
        map5 = px.scatter_mapbox(
                     data_a,
                     lat='Latitude',
                     lon='Longitude',
                     hover_name='Location',
                     zoom=3,
                     color="Gender",
                     mapbox_style='carto-darkmatter',  # You can change the map style
                     )
                 
        # Output Gender
        filter2 = ['M', 'Unknown',"F"]
        filtered_rows2 =  data_a[data_a['Gender'].isin(filter2)]
        column = filtered_rows2.loc[:, "Gender"]
        season_counts = column.value_counts()
        output_values = season_counts.to_string(index=False)
                 
        map5.update_layout(
                             title_text='Map Australia',
                             width=900,height=650,
                             mapbox_style='carto-darkmatter',)
        
        sunyl = px.sunburst(
            df_merged,
            path=["Gender","Fatal"],  # Hierarchical levels for the chart
            title="Gender and Fatal",
            color_discrete_map=color_gender,
            color='Gender',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Gender and Fatal',)
                 
    # Fatal 
    if "col" not in input_color and input_toggle3:
        map5 = px.scatter_mapbox(
                        data_a,
                        lat='Latitude',
                        lon='Longitude',
                        hover_name='Location',
                        zoom=3,
                        color="Fatal",
                        mapbox_style='carto-darkmatter',  # You can change the map style
                    )
                
        # Output Fatal
        filter2 = ['N', 'Y',"Unknown"]
        filtered_rows2 =  data_a[data_a['Fatal'].isin(filter2)]
        column = filtered_rows2.loc[:, "Fatal"]
        season_counts = column.value_counts()
                    
        output_values = season_counts.to_string(index=False)
                
        map5.update_layout(
                            title_text='Map Australia',
                            width=900,height=650,
                            mapbox_style='carto-darkmatter',)  
        
        sunyl = px.sunburst(
            df_merged,
            path=["Fatal","Activity"],  # Hierarchical levels for the chart
            title="Fatal and Activity",
            color_discrete_map=color_map_fatal,
            color='Fatal',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Fatal and Activity',)
                
    # Activity 
    if "col" not in input_color and input_toggle4:
        filter = ['Diving', 'Fishing',"Surfing","Unknown","Bathing","Swimming"]
        filtered_rows =  data_a[data_a['Activity'].isin(filter)]
        sorted_df = filtered_rows.sort_values(by="Activity", ascending=False)
        map5 = px.scatter_mapbox(
                        sorted_df,
                        lat='Latitude',
                        lon='Longitude',
                        hover_name='Location',
                        zoom=3,
                        color="Activity",
                        mapbox_style='carto-darkmatter',  # You can change the map style
                        )
                    
        # Output Activity
        filter2 = ['Unknown', 'Swimming',"Surfing","Fishing","Diving","Bathing"]
        filtered_rows2 =  data_a[data_a['Activity'].isin(filter2)]
        column = filtered_rows2.loc[:, "Activity"]
        custom_order = ['Unknown', 'Swimming',"Surfing","Fishing","Diving","Bathing"]
        season_counts = filtered_rows2.groupby("Activity").size()
        season_counts = season_counts.reindex(filter2, fill_value=0)

        output_values = season_counts.values
        output_values = "Activity " + " ".join(map(str, output_values))
                    
        map5.update_layout(
                                title_text='Map Australia',
                                width=900,height=650,
                                mapbox_style='carto-darkmatter',)
        
        sunyl = px.sunburst(
            df_merged,
            path=["Activity","Gender"],  # Hierarchical levels for the chart
            title="Activity and Gender",
            color_discrete_map=color_map_activity,
            color='Activity',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Activity and Gender',)


    # No light and no values
    if "col" not in input_color and not input_toggle2 and not input_toggle3 and not input_toggle4:
        map5 = px.scatter_mapbox(
            data_a,
            lat='Latitude',
            lon='Longitude',
            hover_name='Location',
            zoom=3,
            color="Season",
            mapbox_style='carto-darkmatter',  # You can change the map style
            )
        
        # Output Season
        filter2 = ['Summer', 'Autumn',"Spring","Winter"]
        filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
        column = filtered_rows2.loc[:, "Season"]
        season_counts = column.value_counts()

        output_values = season_counts.to_string(index=False)
        
        
        map5.update_layout(
                    title_text='Map Australia',
                    width=900,height=650,
                    mapbox_style='carto-darkmatter',)
        
        sunyl = px.sunburst(
            df_merged,
            path=['Season',"State"],  # Hierarchical levels for the chart
            title="Season and State",
            color_discrete_map=color_map,
            color='Season',
        )
        
        fig_2.data = []

        for trace in sunyl.data:
                fig_2.add_trace(trace, row=1, col=1)
                

        fig_2.update_layout(
                        title_text='Season and State',)
        
        
    # Light and no values
    if "col" in input_color and not input_toggle2 and not input_toggle3 and not input_toggle4:
            map5 = px.scatter_mapbox(
                data_a,
                lat='Latitude',
                lon='Longitude',
                hover_name='Location',
                zoom=3,
                color="Season",
                mapbox_style='open-street-map',  # You can change the map style
                )
            
            # Output Season
            filter2 = ['Summer', 'Autumn',"Spring","Winter"]
            filtered_rows2 =  data_a[data_a['Season'].isin(filter2)]
            column = filtered_rows2.loc[:, "Season"]
            season_counts = column.value_counts()

            output_values = season_counts.to_string(index=False)
            
            
            map5.update_layout(
                        title_text='Map Australia',
                        width=900,height=650,
                        mapbox_style='open-street-map',)
            
            input_toggle2 = False
            input_toggle3 = False
            input_toggle4 = False   
            
            sunyl = px.sunburst(
                df_merged,
                path=['Season',"State"],  # Hierarchical levels for the chart
                title="Season and State",
                color_discrete_map=color_map,
                color='Season',
            )
            
            fig_2.data = []

            for trace in sunyl.data:
                    fig_2.add_trace(trace, row=1, col=1)
                    

            fig_2.update_layout(
                            title_text='Season and State',)



    
    fig_.update_layout(
                    width=900,height=650,)
    
    

    return map5,fig_,fig_2, input_toggle2, input_toggle3, input_toggle4, output_values

# Callbacks for updating the next two graphs in "Australia 1"
@app.callback(
   [Output('graph7', 'figure'),Output('graph8', 'figure')],
    [Input('graph7', 'figure'),Input('graph8', 'figure')]
    
)

def update_map6(input2, input3):
    
    australiadc = data_a.fillna({'State': 'Unknown', 'Gender': 'Unknown', 'Activity': 'Unknown'})
    filter = ['Swimming', 'Diving',"Fishing","Surfing","Bathing","Unknown"]
    filtered_rows =  australiadc[australiadc['Activity'].isin(filter)]
    filter3 = ['Invalid','Provoked',"Unprovoked","Unknown","Unverified"]
    filtered_rows2 =  filtered_rows[filtered_rows['Type'].isin(filter3)]
    
    df_merged = filtered_rows2[['State', 'Activity',"Gender","Type","Season"]]
    
    fig8 = px.treemap(df_merged, path=["Activity", "Type"],
                 color="Activity",)
    
    
              
    fig8.update_layout(
                    title_text='Treemap Australia',
                    width=700,height=650,)

    
    fig.update_layout(
                    title_text='Bar Australia',
                    width=900,height=650,)
    
    
    
    return fig8,fig

# Callbacks for updating the next two graphs in "Australia 2"
@app.callback(
   Output('graph12', 'figure'),
    Input('graph12', 'figure')
    
)

def update_map7(input1):
    
    fig10.update_layout(
                    title_text='Pie Chart Australia',
                    width=700,height=500,)

    return fig10


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=8056)

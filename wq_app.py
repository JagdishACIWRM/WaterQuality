import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.figure_factory as ff
import plotly.express as px
from st_aggrid import AgGrid,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from PIL import Image

# Define filename, sheet name and page name
excel_file = 'obs_water_quality.xlsx'
sheet_obs_details = 'obs_details'
sheet_name = 'Location_Summary'
sheet_avg_max_min_std_name = 'Loc_Avg_min_max_stddev'

page_title = 'ACIWRM-Water Quality Dashboard'
image = Image.open('KWRIS_logo.png')
st.set_page_config(page_title=page_title, page_icon=":bar_chart:", layout="wide")
st.image(image)
st.title(":bar_chart: Water Quality Dashboard")
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

# ---- READ EXCEL ----
@st.cache
def get_data_obs_details_from_excel():
    df = pd.read_excel(io=excel_file,sheet_name=sheet_obs_details,usecols="A:AM",)
    # df['obs_Date'] = pd.to_datetime(df['obs_Date']).dt.date
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df_obs_details = get_data_obs_details_from_excel()
df_obs_details.round(3)

def get_data_from_excel():
    df = pd.read_excel(io=excel_file,sheet_name=sheet_name,usecols="A:AE",)
    # df['obs_Date'] = pd.to_datetime(df['obs_Date']).dt.date
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()

def get_data_avg_max_min_std():
    df_avg_max_min_std = pd.read_excel(io=excel_file,sheet_name=sheet_avg_max_min_std_name,usecols="A:AE",)
    # df['obs_Date'] = pd.to_datetime(df['obs_Date']).dt.date
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df_avg_max_min_std

df_avg_max_min_std = get_data_avg_max_min_std()
df_avg_max_min_std.round(3)

# ---- SIDEBAR ----
st.sidebar.header("Select Source:")
# Source and Location Selection
source_name=df["wq_sourcecode"].unique()
sourceName = st.sidebar.selectbox("Select the Data Source:",options=source_name,)
df_source = df.query("wq_sourcecode == @sourceName" )
location_name=df_source["location_name"].unique()
locationName = st.sidebar.selectbox("Select the Location:",options=location_name,)

kpi = st.sidebar.selectbox("Select the Indicator:",
options=
("pH","Electrical.Conductivity.(EC)","Total.Dissolved.solids.(TDS)","Total.Suspended.solids.(TSS)","Nitrogen.Ammonia(NH3)","Nitrate(NO3)",
"Phosphorus(P)","DO","COD","BOD","Total.Alkalinity.as.CaCO3","Total.Hardness.as.CaCO3","Calcium(Ca)","Magnesium(Mg)","Sodium(Na)",
"Potassium(K)","Chloride(Cl)","Sulphate(SO4)","Carbonate(CO3)","Bicarbonate(HCO3)","RSC_meq","SAR",
"Fluoride(F)","Boron(B)","Iron(Fe)","Total_coliform_MPN","Faecal_coliform_MPN")
)

df_obs_details_selection = df_obs_details.query("wq_sourcecode == @sourceName  & location_name == @locationName" )
df_avg_max_min_std_selection=df_avg_max_min_std.query("wq_sourcecode == @sourceName  & location_name == @locationName" )
df_selection = df_source.query("location_name == @locationName" )
txtobscount=len(df_selection)


# Set all labels
chart_indicator = "avg_"+kpi
chart_title = "<b> "+ kpi +" <b>"+ "value pertaining to:"+"<b>"+locationName+"<b>"
box_chart_title = "<b> Fluctuation of "+ kpi +" <b>"+ "value pertaining to:"+"<b>"+locationName+"<b>"
location_avg_summary_title = "Water yearwise, season wise Average for : "+locationName + " for " + kpi
location_avg_summary_chart = "Water yearwise, season wise Average Chart for : " + kpi + " at "+locationName 
location_box_summary_chart = "Water yearwise, fluctuation of observation for : " + kpi + " at "+locationName 
test_data_title = "Detailed Dataset: "+locationName 
test_data_summary_title = "Minimum, Maximum, Average and Std. Dev of all indicators for : "+locationName 
about_page= "Data Source and report developed by:"


df_avg= df_avg_max_min_std.query("""wq_sourcecode == @sourceName  & location_name == @locationName & title == "Average" """ )
df_max= df_avg_max_min_std.query("""wq_sourcecode == @sourceName  & location_name == @locationName & title == "Maximum" """ )
df_min= df_avg_max_min_std.query("""wq_sourcecode == @sourceName  & location_name == @locationName & title == "Minimum" """ )
df_std= df_avg_max_min_std.query("""wq_sourcecode == @sourceName  & location_name == @locationName & title == "Standard Deviation" """ )

txtavgkpi= round(((df_avg[[kpi]]).iat[0,0]),4)
txtmaxkpi= round(((df_max[[kpi]]).iat[0,0]),4)
txtminkpi= round(((df_min[[kpi]]).iat[0,0]),4)
txtstdkpi= round(((df_std[[kpi]]).iat[0,0]),4)

fig_px_bar_by_Obs_Year = px.bar(df_selection,x="obsYear",y=chart_indicator,color="obsSeason",
 barmode='group',orientation="v",title=chart_title,template="plotly_white",
   labels={'obsYear':'Water Year','obsSeason':'Season'}
   )
fig_px_bar_by_Obs_Year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", xaxis_tickangle=-45, xaxis={'categoryorder':'category ascending'}
)

fig_px_box_by_Obs_Year = px.box(df_selection, x="obsYear",y=chart_indicator,title=box_chart_title)
fig_px_box_by_Obs_Year.update_layout(
    plot_bgcolor="rgba(233,233,233,233)", 
    paper_bgcolor="rgba(156,156,156,156)", 
    xaxis_tickangle=-45, xaxis={'categoryorder':'category ascending'}
)

## Layout
## -------------
col1, col2, col3,col4,col5 = st.columns(5)
col1.metric(locationName+ "No of Obs:",txtobscount)
col2.metric("Average : "+kpi+" ",txtavgkpi)
col3.metric("Maximum : "+kpi+" ", txtmaxkpi)
col4.metric("Minimum : "+kpi+" ", txtminkpi)
col5.metric("Std. Variance : "+kpi + " ", txtstdkpi)

with st.expander(location_avg_summary_chart, expanded=True):
    st.plotly_chart(fig_px_bar_by_Obs_Year)

with st.expander(location_box_summary_chart, expanded=True):
    st.plotly_chart(fig_px_box_by_Obs_Year)

with st.expander(location_avg_summary_title, expanded=True):
    # Grid 1 - Display
    # based on https://www.youtube.com/watch?v=F54ELJwspos
    # 
    gd = GridOptionsBuilder.from_dataframe(df_selection)
    gd.configure_selection(selection_mode='multiple',use_checkbox=True)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_pagination(enabled=True)
    gridoptions = gd.build()
    grid_from = AgGrid(df_selection,gridOptions=gridoptions,
                        update_mode= GridUpdateMode.SELECTION_CHANGED,
                        height = 300,
                        allow_unsafe_jscode=True,
                        theme = 'fresh')

    # we will not be using following functionality
    # ============================================
    # st.subheader("Output")
    # Grid To - Highlight
    # grid_to = AgGrid(df_sel)
    sel_row = grid_from["selected_rows"] # Type -> List
    df_sel = pd.DataFrame (sel_row) # Convert list to dataframe


with st.expander(test_data_title, expanded=True):
    # Grid 1 - Display
    # based on https://www.youtube.com/watch?v=F54ELJwspos
    # 
    gd = GridOptionsBuilder.from_dataframe(df_obs_details_selection)
    gd.configure_selection(selection_mode='multiple',use_checkbox=True)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_pagination(enabled=True)
    gridoptions = gd.build()
    grid_from = AgGrid(df_obs_details_selection,gridOptions=gridoptions,
                        update_mode= GridUpdateMode.SELECTION_CHANGED,
                        height = 300,
                        allow_unsafe_jscode=True,
                        theme = 'fresh')

    # we will not be using following functionality
    # ============================================
    # st.subheader("Output")
    # Grid To - Highlight
    # grid_to = AgGrid(df_sel)
    sel_row = grid_from["selected_rows"] # Type -> List
    df_sel = pd.DataFrame (sel_row) # Convert list to dataframe
    

with st.expander(test_data_summary_title, expanded=True):
    # Grid 1 - Display
    # based on https://www.youtube.com/watch?v=F54ELJwspos
    # 
    gd = GridOptionsBuilder.from_dataframe(df_avg_max_min_std_selection)
    gd.configure_selection(selection_mode='multiple',use_checkbox=True)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_pagination(enabled=True)
    gridoptions = gd.build()
    grid_from = AgGrid(df_avg_max_min_std_selection,gridOptions=gridoptions,
                        update_mode= GridUpdateMode.SELECTION_CHANGED,
                        height = 300,
                        allow_unsafe_jscode=True,
                        theme = 'fresh')

    # we will not be using following functionality
    # ============================================
    # st.subheader("Output")
    # Grid To - Highlight
    # grid_to = AgGrid(df_sel)
    sel_row = grid_from["selected_rows"] # Type -> List
    df_sel = pd.DataFrame (sel_row) # Convert list to dataframe



with st.expander(about_page,expanded=False):   
    st.write("NHP Water Quality Data from WATER QUALITY ASSESSMENT REPORT OF 10 MONITORING STATIONS PERTAINING TO SOUTHERN KARNATAKA RIVERS UNDER NHP")
    st.write("file name: 'NHP 2000-2020 report.pdf' file")
#    st.write("--------------------------------------------------------------------------------------------------------------")
    st.write("PDS Water Quality Data from REPORT ON STUDY OF RIVER WATER SAMPLES AT VARIOUS SITES IN SOUTHERN KARNATAKA 'PDS 10 years 2012-2021.pdf' file ")
#    st.write("--------------------------------------------------------------------------------------------------------------")
    st.write("Thanks to : KARNATAKA ENGINEERING RESEARCH STATION KRISHNARAJASAGARA")
    st.write("Web Report Developed by Jagdish Damania <jagdish.damania@samarthainfo.com>")
# st.write("[Data Source](https://kwris.aciwrm.org/)")

# Reference
# ---------
# Source: https://www.youtube.com/watch?v=AiECtbkLFD8
# Source: https://www.youtube.com/watch?v=Sb0A9i6d320

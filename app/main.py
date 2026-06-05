import sys
import os
sys.path.append(
   os.path.abspath(
      os.path.join(os.path.dirname(__file__), "..")
   )
)
import pandas as pd
import streamlit as st
#For Image
import base64
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    

from backend.collision import calculate_distance
from backend.recommendation import show_recommendation
from backend.risk import get_risk_level,calculate_risk_score
import plotly.graph_objects as go
#Title

st.set_page_config(
  page_title="OrbitaSafe AI",
  page_icon="assets/satellite.png",
  layout="wide"
)
# Dark Theme CSS
bg_image = get_base64("assets/R.jpg")

st.markdown(f"""
<style>
.status-bar{{
    margin-top:10px;
    padding:10px;
    border-radius:10px;
    background:rgba(0,255,100,0.1);
    color:#00ff88;
}}

/* NEW CODE START For remove extra white header*/

header {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

#MainMenu {{
    visibility: hidden;
}}

[data-testid="stHeader"] {{
    display: none;
}}

[data-testid="stToolbar"] {{
    display: none;
}}

.block-container {{
    padding-top: 0rem !important;
}}

/* NEW CODE END For reove white header*/
.stApp{{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}}

.stApp::before {{
    content:"";
    position:fixed;
    top:0;
    left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,0.93);
    z-index:-1;
}}

h1, h2, h3 {{
    color:white !important;
    text-shadow:0 0 15px rgba(0,0,0,0.9);
}}

p, label {{
    color:#f5f5f5 !important;
}}

[data-testid="stSidebar"] {{
    background:rgba(0,0,0,0.55);
    backdrop-filter:blur(12px);
    border-right:1px solid rgba(255,255,255,0.1);
}}

[data-testid="metric-container"] {{
    background:rgba(0,0,0,0.55) !important;
    border:1px solid rgba(255,255,255,0.2);
    padding:15px;
    border-radius:18px;
    backdrop-filter:blur(10px);
}}

[data-testid="stMetricValue"] {{
    color:#00d4ff !important;
    font-size:42px !important;
    font-weight:bold !important;
    text-shadow:0 0 15px rgba(0,212,255,0.8);
}}

[data-testid="stMetricLabel"] {{
    color:white !important;
    font-weight:bold !important;
}}


.topbar{{
    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:15px 30px;

    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(12px);

    border-radius:18px;
    margin-bottom:20px;

    border:1px solid rgba(255,255,255,0.1);
}}

.logo{{
    font-size:28px;
    font-weight:bold;
    color:white;
}}

.menu{{
    display:flex;
    gap:20px;
    color:white;
}}
.risk-box{{
    background:rgba(0,0,0,0.65);
    padding:20px;
    border-radius:15px;
    border:1px solid rgba(255,255,255,0.15);
    backdrop-filter:blur(10px);
    margin-top:15px;
    margin-bottom:20px;
}}

.risk-title{{
    color:#ff4d4d;
    font-size:28px;
    font-weight:bold;
}}

.risk-text{{
    color:white;
    font-size:18px;
    font-weight:600;
}}
.status-bar {{
    margin-top:10px;
    margin-bottom:20px;
    padding:12px 18px;
    border-radius:12px;
    background:rgba(0,0,0,0.65);
    color:#00ff88 !important;
    font-weight:bold;
    text-shadow:0 0 10px rgba(0,255,136,0.7);
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<h1 style="
font-size:72px;
font-weight:900;
color:white;
text-shadow:0 0 25px #00d4ff;
">
               OrbitaSafe AI
</h1>
""", unsafe_allow_html=True)

st.image("assets/satellite.png", width=80)
st.write("NASA-inspired satellite collision prediction system")


#Satellite Control sidebar
#st.sidebar.header("Satellite Controls")
#sat_x=st.sidebar.slider("Sattellite X", 0, 10, 1)
#sat_y=st.sidebar.slider("Sattellite Y", 0, 10, 4)


#CSV file upload from browser
uploaded_file=st.sidebar.file_uploader("upload Debris CSV", 
type=["csv"]
)
if uploaded_file is not None:
  df=pd.read_csv(uploaded_file)
  debris_x=df["x"].tolist()
  debris_y=df["y"].tolist()
#CSV file upload from data
else:
  df=pd.read_csv("data/debris.csv")
  debris_x=df["x"].tolist()
  debris_y=df["y"].tolist()

##Mutiple Satellite
sat_x=[1,4,7]
sat_y=[4,6,2]
current_sat_x=sat_x[0]
current_sat_y=sat_y[0]

## Data from Onlinne
from backend.realdata import get_starlink_data
active_data=get_starlink_data()
#Data flitch test
st.write(len(active_data))
##sidebar Metrics
st.sidebar.metric("Total Satellites", len(sat_x))
st.sidebar.metric("Total Debris", len(debris_x))
st.sidebar.metric("Real Active Satellites",len(active_data))


#Creat Graph
fig= go.Figure()
#Satellite point on Graph
fig.add_trace(go.Scatter(
    x=sat_x,
    y=sat_y,
    mode='lines+markers',
    marker=dict(size=12),
    name='Satellite'
        ))
#Debris Poinnt on Grap
fig.add_trace(go.Scatter(
    x=debris_x,
    y=debris_y,
    mode='markers',
    marker=dict(size=15),
    name='Debris'
        ))


# Graph title
fig.update_layout(
   title="Orbital Object Visualization",
   xaxis_title= "X Position",
   yaxis_title= "y Position",
   paper_bgcolor="#0e1117",
   plot_bgcolor="#0e1117",
   font=dict(color="white"),
   xaxis=dict(showgrid=False),
   yaxis=dict(showgrid=False)
)


#Find the distance Satellite and debris for multiple debris
min_distance=999

for i in range(len(debris_x)):
   distance=calculate_distance(
     current_sat_x,
     current_sat_y,
     debris_x[i],
     debris_y[i]
   )
   if distance < min_distance:
    min_distance=distance
    nearest_x=debris_x[i]
    nearest_y=debris_y[i]
st.write("Nearest Distance:",round(min_distance,2))
risk_score= calculate_risk_score(min_distance)
risk_level= get_risk_level(risk_score)
st.sidebar.metric("Risk Score", f"{risk_score:.0f}%")
st.metric("Collision Risk Score", f"{risk_score:.0f}%")

###Risk level coloring
if risk_score >= 70:
    st.markdown(
    f"""
    <div style="
    background:rgba(255,0,0,0.25);
    border:2px solid #ff4d4d;
    color:white;
    padding:15px;
    border-radius:15px;
    font-size:30px;
    font-weight:900;
    text-shadow:0 0 10px rgba(0,0,0,0.9);
    ">
    🚨 {risk_level}
    </div>
    """,
    unsafe_allow_html=True
)

elif risk_score >= 40:
    st.markdown(
        f"""
        <div style="
        color:#ffcc00;
        font-size:32px;
        font-weight:bold;
        text-shadow:0 0 20px #ffcc00;
        margin-top:10px;">
        ⚠️ {risk_level}
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    st.markdown(
        f"""
        <div style="
        color:#00ff88;
        font-size:32px;
        font-weight:bold;
        text-shadow:0 0 20px #00ff88;
        margin-top:10px;">
        ✅ {risk_level}
        </div>
        """,
        unsafe_allow_html=True
    )


st.progress(int(risk_score)) #risk progress bar
show_recommendation(risk_score)

#Collision line
fig.add_shape(
  type="line",
  x0=current_sat_x,
  y0=current_sat_y,
  x1=nearest_x,
  y1=nearest_y,
  line=dict(
        color="red",
        width=4,
        dash="dot"
        )
  )

#Warning circle zone
fig.add_shape(
  type="circle",
  xref="x",
  yref="y",
  x0=current_sat_x - 1,
  y0=current_sat_y - 1,
  x1=current_sat_x + 1,
  y1=current_sat_y + 1,
  line=dict(color="orange",width=3, dash="dash")
)
##Top dashboard CARD
st.markdown("## 📊 Mission Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Satellites", len(sat_x))
col2.metric("Debris Objects", len(debris_x))
col3.metric("Nearest Distance", round(min_distance, 2))

##seperate container for graph
with st.container():
    st.markdown("## 🛰️ Orbital Threat Visualization")
    st.plotly_chart(fig, use_container_width=True)

##CSV preview table
st.markdown("## 📄 Debris Data Preview")
st.dataframe(df)

st.markdown("</div>", unsafe_allow_html=True)
##Footer
st.markdown("---")
st.caption("OrbitaSafe AI | Built with Python, Streamlit & Plotly")






  
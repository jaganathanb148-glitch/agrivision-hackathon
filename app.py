import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AgriVision", page_icon="🌾", layout="wide")

st.title("🌾 AgriVision")
st.subheader("Satellite-Based Crop Health Monitoring System")
st.caption("Hackathon prototype for Agricultural Sustainability – Problem 3.1")

# Demo field dataset. Replace with real Sentinel-2-derived values when connected to GEE.
data = pd.DataFrame({
    "Field": ["Field A", "Field B", "Field C", "Field D", "Field E", "Field F"],
    "Latitude": [13.08, 13.09, 13.07, 13.10, 13.06, 13.11],
    "Longitude": [80.27, 80.29, 80.26, 80.25, 80.30, 80.28],
    "NDVI": [0.78, 0.62, 0.41, 0.29, 0.71, 0.52],
    "NDRE": [0.46, 0.38, 0.24, 0.15, 0.42, 0.30],
    "Previous_NDVI": [0.75, 0.67, 0.48, 0.44, 0.69, 0.55]
})

def classify(ndvi):
    if ndvi >= 0.60:
        return "Healthy"
    elif ndvi >= 0.40:
        return "Moderate"
    return "Stressed"

data["Health"] = data["NDVI"].apply(classify)
data["NDVI Change"] = data["NDVI"] - data["Previous_NDVI"]

st.sidebar.header("🌱 Field Filter")
selected = st.sidebar.multiselect(
    "Select health classes",
    ["Healthy", "Moderate", "Stressed"],
    default=["Healthy", "Moderate", "Stressed"]
)
view = data[data["Health"].isin(selected)]

c1,c2,c3,c4 = st.columns(4)
c1.metric("Fields shown", len(view))
c2.metric("Healthy", int((view.Health=="Healthy").sum()))
c3.metric("Moderate", int((view.Health=="Moderate").sum()))
c4.metric("Stressed", int((view.Health=="Stressed").sum()))

st.divider()

left,right = st.columns([1.25,1])
with left:
    st.subheader("🗺️ Crop Health Map")
    fig = px.scatter_map(
        view, lat="Latitude", lon="Longitude",
        color="Health", size="NDVI", hover_name="Field",
        hover_data=["NDVI","NDRE","NDVI Change"],
        zoom=11, height=500,
        color_discrete_map={"Healthy":"green","Moderate":"orange","Stressed":"red"}
    )
    fig.update_layout(map_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("📊 Crop Health Distribution")
    counts = data["Health"].value_counts().reindex(["Healthy","Moderate","Stressed"]).fillna(0).reset_index()
    counts.columns=["Health","Fields"]
    fig2=px.bar(counts,x="Health",y="Fields",text="Fields",
                color="Health",
                color_discrete_map={"Healthy":"green","Moderate":"orange","Stressed":"red"})
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2,use_container_width=True)

st.subheader("📈 NDVI Change Through Time")
trend = data[["Field", "Previous_NDVI", "NDVI"]].melt("Field", var_name="Period", value_name="NDVI_Value")
fig3=px.bar(trend,x="Field",y="NDVI_Value",color="Period",barmode="group")
st.plotly_chart(fig3,use_container_width=True)

st.subheader("📋 Field-Level Analysis")
st.dataframe(
    data[["Field","NDVI","NDRE","Previous_NDVI","NDVI Change","Health"]],
    use_container_width=True, hide_index=True
)

st.subheader("🤖 Decision Support")
for _,r in data.iterrows():
    if r["Health"]=="Stressed":
        st.error(f"🔴 {r['Field']}: Crop stress detected. Prioritize field inspection and check water/nutrient conditions.")
    elif r["Health"]=="Moderate":
        st.warning(f"🟡 {r['Field']}: Moderate stress. Monitor the field and compare the next satellite observation.")
    else:
        st.success(f"🟢 {r['Field']}: Healthy vegetation condition.")

st.info("Prototype note: the displayed values are synthetic demonstration data. In a production deployment, NDVI/NDRE would be generated from Sentinel-2 imagery, consistent with the hackathon problem statement.")

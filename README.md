# 🌾 AgriVision — Satellite-Based Crop Health Monitoring

## Hackathon Problem
Agricultural Sustainability – **3.1 Crop Health Monitoring System**.

The challenge asks for a satellite-based crop-health monitoring system using NDVI/NDRE or other vegetation indices, crop-health classes, temporal comparison, and stressed-field identification.

## Solution
AgriVision demonstrates the workflow:

Satellite imagery → vegetation indices → crop-health classification → interactive map/dashboard → decision support.

### Classes
- 🟢 Healthy: NDVI ≥ 0.60
- 🟡 Moderate: 0.40–0.59
- 🔴 Stressed: NDVI < 0.40

These thresholds are prototype/demo thresholds and should be calibrated for the crop, season, region, and real satellite data before operational use.

## Important data note
The included values are **synthetic demonstration data** so the prototype can run immediately without external credentials. The hackathon document lists Sentinel-2 and NDVI/NDRE as suitable inputs. For a production version, connect the app to Google Earth Engine/Sentinel-2 processing.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy
Use Streamlit Community Cloud:
1. Push `app.py` and `requirements.txt` to a public GitHub repository.
2. Create a new app in Streamlit Community Cloud.
3. Select the repository, branch, and `app.py`.
4. Deploy and copy the public URL.

## 2–3 minute demo
1. Introduce the crop-health problem.
2. Show the dashboard KPIs.
3. Explain the map's green/orange/red field classes.
4. Show NDVI/NDRE and previous-vs-current NDVI.
5. Click/filter health classes.
6. Show the decision-support recommendations.
7. State that the prototype can be connected to Sentinel-2/GEE for real imagery.

## Architecture
Data source → Image processing → NDVI/NDRE → Health classification → Interactive map → Recommendation.

## Team
Solo participant.

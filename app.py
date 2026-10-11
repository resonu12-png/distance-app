%%writefile app.py
import streamlit as st
from geopy.geocoders import Nominatim
import requests
import time

st.set_page_config(page_title="Know The Distance", page_icon="📍")
st.title("📍 Know The Distance App (Free Version)")
st.write("Bina kisi API Key ke map aur distance nikalein!")

st.header("1. Origin (Jahan se doori mapni hai)")
col1, col2 = st.columns(2)
with col1:
    origin_school = st.text_input("School (Origin)", placeholder="e.g., UPG RAJKIYEKRIT HIGH SCHOOL ASEHAAR")
    origin_block = st.text_input("Block (Origin)", placeholder="e.g., Panki")
with col2:
    origin_district = st.text_input("District (Origin)", placeholder="e.g., Palamu")

st.header("2. Destination (Jahan tak doori mapni hai)")
col3, col4 = st.columns(2)
with col3:
    dest_school = st.text_input("School (Destination)", placeholder="e.g., UPG HS DHANBAD")
    dest_block = st.text_input("Block (Destination)", placeholder="e.g., DHANBAD")
with col4:
    dest_district = st.text_input("District (Destination)", placeholder="e.g., DHANBAD")

if st.button("Calculate Distance 🚗"):
    if not origin_school or not dest_school:
        st.warning("Kripya dono jagah ke details enter karein.")
    else:
        with st.spinner("Location dhundh raha hai aur distance calculate kar raha hai..."):
            try:
                geolocator = Nominatim(user_agent="distance_calculator_jharkhand")
                
                # Origin Location aur Map Link generate karna
                origin_query = f"{origin_school}, {origin_block}, {origin_district}, Jharkhand, India"
                loc1 = geolocator.geocode(origin_query)
                map_url_1 = f"https://www.google.com/maps/search/?api=1&query={origin_school.replace(' ', '+')}+{origin_block}+{origin_district}+Jharkhand"
                
                if not loc1: 
                    loc1 = geolocator.geocode(f"{origin_block}, {origin_district}, Jharkhand, India")
                    st.info(f"⚠️ {origin_school} map par exact nahi mila, isliye {origin_block} area se doori map rahe hain. 👉 [📍 Click here to Check School on Map]({map_url_1})")
                else:
                    st.info(f"✅ {origin_school} ki exact location mil gayi! 👉 [📍 Click here to View on Map]({map_url_1})")
                
                time.sleep(1)
                
                # Destination Location aur Map Link generate karna
                dest_query = f"{dest_school}, {dest_block}, {dest_district}, Jharkhand, India"
                loc2 = geolocator.geocode(dest_query)
                map_url_2 = f"https://www.google.com/maps/search/?api=1&query={dest_school.replace(' ', '+')}+{dest_block}+{dest_district}+Jharkhand"

                if not loc2:
                    loc2 = geolocator.geocode(f"{dest_block}, {dest_district}, Jharkhand, India")
                    st.info(f"⚠️ {dest_school} map par exact nahi mila, isliye {dest_block} area se doori map rahe hain. 👉 [📍 Click here to Check School on Map]({map_url_2})")
                else:
                    st.info(f"✅ {dest_school} ki exact location mil gayi! 👉 [📍 Click here to View on Map]({map_url_2})")

                if loc1 and loc2:
                    url = f"http://router.project-osrm.org/route/v1/driving/{loc1.longitude},{loc1.latitude};{loc2.longitude},{loc2.latitude}?overview=false"
                    r = requests.get(url)
                    data = r.json()
                    
                    if data.get("code") == "Ok":
                        dist_meters = data["routes"][0]["distance"]
                        dur_seconds = data["routes"][0]["duration"]
                        
                        dist_km = round(dist_meters / 1000, 2)
                        dur_mins = round(dur_seconds / 60)
                        
                        st.success(f"✅ Distance Calculated Successfully!\n\n🛣️ **Total Driving Distance:** {dist_km} km \n\n⏱️ **Estimated Time:** {dur_mins} minutes")
                    else:
                        st.error("Rasta nahi mila. Driving root map par available nahi hai.")
                else:
                    st.error("Kripya address check karein, location map par nahi mili.")
            except Exception as e:
                st.error(f"Error: Map server se connect nahi ho paya. Dobara try karein.")

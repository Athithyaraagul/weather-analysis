import requests
import pandas as pd
import streamlit as st
import plotly.express as px

API_KEY = "openweathermap_api_key"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"

def fetch_forecast_data(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching data for {city}: {response.status_code}")
        return None

def main():
    st.title("Weather EDA: Temperature, Humidity, and Precipitation")

    city = st.text_input("Enter the city name:")

    if city:
        forecast_data = fetch_forecast_data(city)

        if forecast_data:
            forecast_list = forecast_data['list']
            df = pd.DataFrame([
                {
                    'Date': item['dt_txt'].split(" ")[0],  
                    'Temperature': item['main']['temp'],
                    'Humidity': item['main']['humidity'],
                    'Precipitation': item['pop'] * 100  
                }
                for item in forecast_list
            ])

            # Group by Date and calculate daily averages
            daily_avg = df.groupby('Date').mean().reset_index()

            # Daily averages in a table
            st.write("### Daily Average Weather Data:")
            st.dataframe(daily_avg)

            # Average Temperature
            st.write("### Average Temperature (°C) for the Next Week")
            fig_temp = px.line(
                daily_avg,
                x="Date",
                y="Temperature",
                title="Average Daily Temperature",
                labels={"Temperature": "Temperature (°C)", "Date": "Date"},
                markers=True
            )
            st.plotly_chart(fig_temp, use_container_width=True)

            # Average Precipitation
            st.write("### Average Precipitation (%) for the Next Week")
            fig_precip = px.bar(
                daily_avg,
                x="Date",
                y="Precipitation",
                title="Average Daily Precipitation",
                labels={"Precipitation": "Precipitation (%)", "Date": "Date"},
            )
            st.plotly_chart(fig_precip, use_container_width=True)

            # Average Humidity
            st.write("### Average Humidity (%) for the Next Week")
            fig_humidity = px.line(
                daily_avg,
                x="Date",
                y="Humidity",
                title="Average Daily Humidity",
                labels={"Humidity": "Humidity (%)", "Date": "Date"},
                markers=True
            )
            st.plotly_chart(fig_humidity, use_container_width=True)

            # Downloadable data
            st.write("### Download Data")
            csv = daily_avg.to_csv(index=False)
            st.download_button(
                label="Download Weather Data as CSV",
                data=csv,
                file_name=f"{city}_weather_forecast.csv",
                mime="text/csv",
            )

# Run the app
if __name__ == "__main__":
    main()
import requests
import plotly.express as px
import csv
import pandas as pd


def get_weather_for_locations(coordinates_dict):
    weather_dict = {}
    for location, coordinates in coordinates_dict.items():
        lat, lng = coordinates
        api_key = '<Opensky API key>'
        api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&units=imperial'
        response = requests.get(api_url)
        data = response.json()
        weather_data = data
        weather_dict[location] = weather_data
    return weather_dict


def csv_to_coordinates_dictionary(file_path):
    coordinates_dict = {}
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row
        for row in reader:
            location = row[0]
            lat = (float(row[-2]))
            long = (float(row[-1]))
            coordinates_dict[location] = (lat, long)
    return coordinates_dict


def plot(weather_data_dict):
    locations = []
    latitudes = []
    longitudes = []
    temperatures = []
    weather_conditions = []
    for location, weather_data in weather_data_dict.items():
        locations.append(location)
        latitudes.append(weather_data['coord']['lat'])
        longitudes.append(weather_data['coord']['lon'])
        temperatures.append(weather_data['main']['temp'])
        weather_conditions.append(weather_data['weather'][0]['main'])
    df = pd.DataFrame({
        'location': locations,
        'latitude': latitudes,
        'longitude': longitudes,
        'temperature': temperatures,
        'weather_condition': weather_conditions
    })

    print(df)

    fig = px.scatter_geo(df, text='location',
                         lat='latitude',
                         lon='longitude',
                         color='temperature'
                         )
    fig.update_geos(
        visible=False, resolution=110, scope="usa",
        showcountries=True, countrycolor="Black",
        showsubunits=True, subunitcolor="Black"
    )
    fig.update_layout(height=300, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


coordinates_dict = csv_to_coordinates_dictionary('ski_resorts.csv')
weather_data_dict = get_weather_for_locations(coordinates_dict)
plot(weather_data_dict)

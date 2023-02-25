from flask import Flask, jsonify, request, render_template
import pandas as pd
from transliterate import translit


# Load the GeoNames database
geonames_df = pd.read_csv('RU.txt', delimiter='\t', encoding='utf-8', header=None, names=[
    'geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude',
    'feature_class', 'feature_code', 'country_code', 'cc2', 'admin1_code',
    'admin2_code', 'admin3_code', 'admin4_code', 'population', 'elevation',
    'dem', 'timezone', 'modification_date'])

# Create a Flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Define the route for getting city information by geonameid
@app.route('/city/', methods=['GET'])
def get_city_info():
    # Get the geonameid from the query parameters
    geonameid = request.args.get('id', type=int)

    # If no geonameid is provided, return a 400 error
    if not geonameid:
        return jsonify({'error': 'GeonameID parameter is missing.'}), 400

    # Get the row corresponding to the geonameid
    city_row = geonames_df[geonames_df['geonameid'] == geonameid]

    # If the geonameid does not exist in the database, return a 404 error
    if city_row.empty:
        return jsonify({'error': 'City not found.'}), 404

    # Extract the relevant information from the row
    name = city_row['name'].values[0]
    country_code = city_row['country_code'].values[0]
    latitude = city_row['latitude'].values[0]
    longitude = city_row['longitude'].values[0]

    # Return the information as a JSON object
    return jsonify({
        'name': name,
        'country_code': country_code,
        'latitude': latitude,
        'longitude': longitude
    })

# Define a helper function to retrieve a page of cities/towns from the DataFrame
def get_cities(page=1, per_page=10):
    start = (page - 1) * per_page
    end = start + per_page
    return geonames_df.iloc[start:end].to_dict(orient='records')

# Define a route for the API endpoint that returns a page of cities/towns
@app.route('/cities', methods=['GET'])
def cities():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    cities = get_cities(page=page, per_page=per_page)
    return jsonify(cities)

@app.route('/citifind', methods=['GET'])
def get_find_info():
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    city1 = translit(city1,'ru',reversed=True)
    city2 = translit(city2, 'ru', reversed=True)

    city1_row = geonames_df[geonames_df['name'] == city1]
    city2_row = geonames_df[geonames_df['name'] == city2]
    city1_row = city1_row.sort_values(by='population', ascending=False)
    city2_row = city2_row.sort_values(by='population', ascending=False)


    if city1_row.empty:
        return jsonify({'error': 'City not found.'}), 404
    if city2_row.empty:
        return jsonify({'error': 'City not found.'}), 404

    name1 = city1_row['name'].values[0]
    country_code1 = city1_row['country_code'].values[0]
    latitude1 = city1_row['latitude'].values[0]
    longitude1 = city1_row['longitude'].values[0]
    timezone1 = city1_row['timezone'].values[0]
    population1 = int(city1_row['population'].values[0])

    name2 = city2_row['name'].values[0]
    country_code2 = city2_row['country_code'].values[0]
    latitude2 = city2_row['latitude'].values[0]
    longitude2 = city2_row['longitude'].values[0]
    timezone2 = city2_row['timezone'].values[0]
    population2 = int(city2_row['population'].values[0])

    if city1_row['latitude'].values[0] < city2_row['latitude'].values[0]:
        futher = f"{city2_row['name'].values[0]} is further north than {city1_row['name'].values[0]}"
    else:
        futher = f"{city1_row['name'].values[0]} is further north than {city2_row['name'].values[0]}"

    if city1_row['timezone'].values[0] == city2_row['timezone'].values[0]:
        timezone = 'same time zone'
    else:
        timezone = 'different  time zone'

    # Return the information as a JSON object
    return jsonify({
        'city1': {
            'name': name1,
            'country_code': country_code1,
            'latitude': latitude1,
            'longitude': longitude1,
            'timezone' : timezone1,
            'population' : population1,
        },
        'city2': {
            'name': name2,
            'country_code': country_code2,
            'latitude': latitude2,
            'longitude': longitude2,
            'timezone': timezone2,
            'population' : population2
        },
        'Info': {
            'futher': futher,
            'timezone': timezone
        }
    })
# Run the app
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)

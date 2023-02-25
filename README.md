GeoNames API
This is a web application that provides access to data from the GeoNames database. The application provides three API endpoints:

/city/: Returns information about a city or town with the specified GeoNames ID.
/cities: Returns a page of cities/towns, where the page number and number of items per page can be specified using query parameters.
/citifind: Returns information about two cities/towns specified by their names in Cyrillic characters, including their latitude and longitude, time zone, population, and distance from the equator.
Dependencies
The following Python packages are required to run the application:

Flask
pandas
transliterate
You can install these packages using pip:

python
Copy code
pip install flask pandas transliterate
Usage
To start the application, run the following command in your terminal:

python
Copy code
python app.py
This will start the application on port 8000. You can access the API endpoints using your web browser or a tool like Postman.

Here are some examples of how to use the API endpoints:

http://127.0.0.1:8000/cities?page=2&per_page=5
http://127.0.0.1:8000/cities
http://127.0.0.1:8000/city/?id=451747
http://127.0.0.1:8000/citifind?city1=Moscow&city2=Saint%20Petersburg
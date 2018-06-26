Overview: Build a database of airports, including the airport contact details, and enable access to the database using a RESTful API.

When airportDB is run, a pymong DB call "Airports" is filled with relevant information. A text-file must be provided which contains 
specially formatted coordinates of desired locations. The format is as so: 34.22;32.32;500 (<Longitude>;<Latitude>;<Radius meters>). 
This represents a circle centered around 34.22,32.32 with a radius of 500 meters. With this information, the airMap API will return information regarding airports within those locations. From that set of data, the airport's name, location, and phone number will be extracted and inserted into a pymongo db.

When the tornadoServer file is run, an HTTP server will be created. This can be reached using the url: http://localhost:8888. Within the submit input, a user can inout the name of an airport, and if that airport exists within the pymongo db, its phone number will be returned. 

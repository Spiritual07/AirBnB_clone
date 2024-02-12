# AirBnB clone - The console

****Description****

As a component of the ALX School Full-Stack Software Engineer program, this project marks the initial stride in constructing a comprehensive web application—a replica of AirBnB. The project's inception involves crafting a bespoke command-line interface for data administration and establishing the fundamental classes for data storage. Through console commands, users can seamlessly generate, modify, and remove objects, alongside overseeing file storage operations. Leveraging JSON serialization/deserialization, the system ensures persistent storage across sessions.

****Usage****

The console works both in interactive mode and non-interactive mode, much like a Unix shell. It prints a prompt (hbnb) and waits for the user for input.

****Command	Example****

Run the console	./console.py
Quit the console	(hbnb) quit
Display the help for a command	(hbnb) help <command>
Create an object (prints its id)	(hbnb) create <class>
Show an object	(hbnb) show <class> <id> or (hbnb) <class>.show(<id>)
Destroy an object	(hbnb) destroy <class> <id> or (hbnb) <class>.destroy(<id>)
Show all objects, or all instances of a class	(hbnb) all or (hbnb) all <class>
Update an attribute of an object	(hbnb) update <class> <id> <attribute name> "<attribute value>" or (hbnb) <class>.update(<id>, <attribute name>, "<attribute value>")
Non-interactive mode example

$ echo "help" | ./console.py
(hbnb)

Documented commands (type help <topic>):

========================================

EOF  all  count  create  destroy  help  quit  show  update

****Models****

The folder models contains all the classes used in this project.

****Files, Description and Attributes****

***base_model.py:*** BaseModel class for all the other classes	id. The attributes are created_at and updated_at

***user.py:*** User class for future user information. The attributes are email, password, first_name and last_name

***amenity.py:*** Amenity class for future amenity information. The attributes is name

***city.py:*** City class for future location information. The attributes are state_id and name

***state.py:*** State class for future location information. The attributes is	name

***place.py:*** Place class for future accomodation information. The attributes are city_id, user_id, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude and amenity_ids

***review.py:*** Review class for future user/host review information. The attributes are place_id, user_id and text

****File storage****

The folder engine manages the serialization and deserialization of all the data, following a JSON format.

A FileStorage class is defined in file_storage.py with methods to follow this flow: <object> -> to_dict() -> <dictionary> -> JSON dump -> <json string> -> FILE -> <json string> -> JSON load -> <dictionary> -> <object>

The init.py file contains the instantiation of the FileStorage class called storage, followed by a call to the method reload() on that instance. This allows the storage to be reloaded automatically at initialization, which recovers the serialized data.

****Tests****

All the code is tested with the unittest module. The test for the classes are in the test_models folder.

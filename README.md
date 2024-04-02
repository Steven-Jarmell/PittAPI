# Pitt API

![Build Status](https://travis-ci.org/Pitt-CSC/PittAPI.svg?branch=master)
![License](https://img.shields.io/badge/license-GPLv2-blue.svg)
![Python Version](https://img.shields.io/badge/python-%3E%3D%203.6-green.svg)

Made by Ritwik Gupta at the University of Pittsburgh in an effort to get
more open data from Pitt.

## Usage examples

```python
from PittAPI import course, dining, lab, laundry, library, news, people, shuttle, textbook

### Courses
# Will return a dictionary of all CS courses
cs_subject = course.get_subject_courses(subject='CS')
courses_dict = cs_subject.courses

# Will return a list of sections of a course during a given term
cs_course = course.get_course_details(term='2244', subject='CS', course='1501')
section_list = cs_course.sections

### Textbook
# Will return a list of dictionaries containing textbooks for a class
# term number comes from pitt.verbacompare.com
small_dict = textbook.get_textbook(term="3150", department="CS", course="445", instructor="RAMIREZ")

### Library
# Will return a dictionary containing results from query
big_dict = library.get_documents(query="computer")

### News
# Will return a list of dictionaries containing news from main news feed
medium_dict = news.get_news()

### Laundry
# Will return a dictionary with amount of washers and dryers
# in use vs. total washers and dryers at building
small_dict = laundry.get_status_simple(building_name="TOWERS")

### Computer Lab
# Will return a dictionary with status of the lab, and amount
# of machines with a certain OS
small_dict = lab.get_status(lab_name="ALUMNI")

### Shuttle
# Will return a list of dictionaries containing routes of shuttles
big_dict = shuttle.get_routes()

### People
# Will return a list of people based on the query
list_of_peeps = people.get_person(query="Smith")

### Dining
# Will return a dictionary of dictionaries containing each dining location,
# with its name, its open/closed status, and open times (if it exists)
medium_dict = dining.get_locations()
medium_dict = dining.get_locations_by_status(status="open")
medium_dict = dining.get_locations_by_status(status="closed")
# Will return a single dictionary of a dining location,
# with its name, its open/closed status, and open times (if it exists)
one = dining.get_location_by_name("taco_bell-schenley_cafe")
two = dining.get_location_by_name("cup_&_chaucer-hillman")
```

## Local Setup

### Prerequisites
- Install Python **3.12**  

### Steps  
1. Run `python --version` to ensure you are working with Python 3.12.  
2. Run `python -m venv env` to create the virtual environment.  
3. Activate the virtual environment according to your host OS. You should see `(env)` on the very left of your terminal. 
- Windows: `./env/Scripts/activate`
- MacOS/Linux: `source venv/bin/activate`
4. Install dependencies with `pip install -r requirements.txt`

## Tests

Run tests with
  ``pytest --cov=pittapi tests/``

## License

This project is licensed under the terms of the [GPLv2 license](/LICENSE)

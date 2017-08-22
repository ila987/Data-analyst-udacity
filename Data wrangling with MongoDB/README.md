# Open street data wrangling 


Project part of my Udacity certification as Data Analyst. 
In this project I have analysed the OpenStreet data of my own town, Milan in Italy, using the link in the section "Sources".


## To run the code

This project requires Python 2.7 and the following Python libraries installed:

NumPy
Pandas
matplotlib
scikit-learn
You will also need to have software installed to run and execute an iPython Notebook as well as MongoDB locally on your machine.

Udacity recommends our students install Anaconda, a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.

You can open the .html file to have an idea of what has been done. To check the detailed analysis the py files:
- audit.py: this file reads the osm files and looks for anomalies in the data
- shape_json.py: this function reads the complete osm files, it corrects the point found in the audit part and it creates a json file that can be used to load it to the DB
- queries.py: this files runs some queries over the MongoDB
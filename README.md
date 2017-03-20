# dand-p3-openstreetmap

Udacity DAND Project 3 – Wrangle OpenStreetMap Data

This is my submission for Project 3 ('Wrangle OpenStreetMap Data') on Udacity's Data Analyst Nanodegree. The project brief asked the student to download a dataset from [OpenStreetMap](www.openstreetmap.org) and use data wrangling/munging techniques to assess the quality of the data and make improvements where necessary. The data was then to be loaded into either a SQL or MongoDB database and queried to discover insights.

The intended project outcomes were to demonstrate the student's ability to:
- Assess the quality of the data for validity, accuracy, completeness, consistency and uniformity
- Parse and gather data from popular file formats such as .json, .xml, .csv, .html
- Process data from many files and very large files that can be cleaned with spreadsheet programs
- Learn how to store, query, and aggregate data using MongoDB or SQL

List of files:
- 'OSM_sampling.py': Python script to create a sample of a given OSM (XML) file.
- 'central_London_sample.osm': Sample of the dataset created using 'OSM_sampling.py' with k=100
- 'audit_address.py': Python file containing functions for auditing and cleaning street and post code data.
- 'update.py': Python file containing functions for cleaning 'amenity', 'shop', 'cuisine' and 'type' data
- 'data.py': Python script to process data from a given OSM (XML) file. The script iteratively parses the XML data, cleans any values as required (using 'update.py') and outputs five CSV files containing data split by XML element type. 
- 'schema.py': Schema of the desired data structure for use with the optional validation function provided with 'data.py'.
- 'schema.sql': Schema of the desired data structure for use with SQLite.
- 'import.sql': SQL script to import data from the five CSV files into the correct tables in SQLite
- 'pie_helper.py': Python file containing functions to create labels for Matplotlib pie charts
- 'P3 - Exploring the data.ipynb': Jupyter notebook file documenting the initial data exploration
- 'P3 (Wrangle OpenStreetMap Data) - submission.ipynb': Jupyter notebook file containing project submission
- 'dand-env-mac.yaml' - relevant Conda environment file (note Python version is 2.7)

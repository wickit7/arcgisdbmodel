# ArcGIS Data Model Creation with JSON (arcgisdbmodel)
The [create_db_model.py](create_db_model.py) script is designed to create and update an ArcGIS geodatabase data model based on a JSON input file. This allows for easy modification and extension of the data model using additional JSON files at a later time.

Creating a data model using a JSON file has several advantages over manual creation in ArcGIS Pro. Here are some of them:
- **Time-saving**: Creating a data model using a JSON file is faster than manual creation in ArcGIS Pro because you can create the entire model in one go, rather than having to create each component one by one.
- **Reusability**: Once you have created a data model using a JSON file, you can reuse it multiple times, simply by modifying the file rather than recreating the model from scratch.
- **Flexibility**: JSON is a flexible format that allows you to easily add, remove, or modify components of the data model as needed.
- **Traceability**: By documenting changes to the data model in JSON files, you can easily track the evolution of the model over time and understand the reasoning behind each change.
- **Collaboration**: JSON files can be easily shared and edited by multiple people, making it easier to collaborate on the creation and modification of the data model.

## Getting Started
To get started with creating an ArcGIS data model using JSON, you'll need the following:
- [ArcGIS Pro](https://pro.arcgis.com/de/pro-app/latest/get-started/download-arcgis-pro.htm) installed on your machine
- The [create_db_model.py](create_db_model.py) script
- A JSON file describing the data model → example json files can be found in the [tutorial](tutorial) folder
- A target [geodatabase](https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/overview/an-overview-of-creating-geodatabases.htm) in which the data model is to be created: A file geodatabase (.gdb) or an enterprise geodatabase such as SQL Server (.sde), Oracle, or PostgreSQL.

## Usage
To create or update an ArcGIS data model based on a JSON input file, run the "create_db_model.py" script with the path to the JSON file as a command-line argument:

> python create_db_model.py data_model.json

## Tutorials
Example json files and instruction README files can be found in the folder [tutorial](tutorial).

In  [tutorial 1](tutorial/tutorial_1/INSTRUCTIONS_TUTORIAL_1.md), the focus is on the following elements:
- create coded value domain
- create range domain
- create dataset
- create feature class
- create attribute rule (uniquie value constraint)
- create relationship (1:n)
- update feature class
    - add field
    - calculate field

## Paramters
The JSON schema and the set of JSON parameters that can be used are described in the README file [PARAMETERS.md](PARAMETERS.md).

## Data models
A collection of data models can be found in the folder [datamodels](datamodels). 

**You are welcome to place your own data models here so that they can be used by the community.**

## Contributing
Contributions to this project are welcome! If you have any suggestions or bug reports, please open an issue or pull request on GitHub.


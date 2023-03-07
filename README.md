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

### Tutorial 1
In  [tutorial 1 - Location with assets](tutorial/tutorial_1/INSTRUCTIONS_TUTORIAL_1.md), a basic data model is created for managing locations with related asstes.

The focus is on the following elements:
- general settings
- environment settings
- coded value domain
- range domain
- dataset
- feature class
- attribute rule (uniquie value constraint)
- relationship "One to Many" (1:n)
- update feature class
    - add field
    - calculate field

### Tutorial 2
In  [tutorial 2 - Location Management](tutorial/tutorial_2/INSTRUCTIONS_TUTORIAL_2.md), a data model is created for managing restaurants, shops and event places with related areas.

In this tuorial, the focus is on the following elements:
- subtypes
- domain depending on subtypes
- relation depending on subtypes

### Tutorial 3
In  [tutorial 3 - Event Management](tutorial/tutorial_3/INSTRUCTIONS_TUTORIAL_3.md), a data model is created for managing event locations and the related events. An event location can have multiple events and an event can take place at multiple event locations.

In this tutorial, the focus is on the following element:
- "Many to Many"-Relationship (n:m) with attributed fields


### Tutorial 4
In  [tutorial 4](tutorial/tutorial_4/INSTRUCTIONS_TUTORIAL_4.md), a data model is created in which a complex attribute rule is used.

The focus is on the following element:
- Attribute rule that contains multiple feature classes

## Paramters
The JSON schema and the set of JSON parameters that can be used are described in the README file [PARAMETERS.md](PARAMETERS.md).

## Data Models
A collection of data models can be found in the folder [datamodels](datamodels). 

**You are welcome to place your own data models here so that they can be used by the community.**

## Contributing
Contributions to this project are welcome! If you have any suggestions or bug reports, please open an issue or pull request on GitHub.

## License
This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE.txt) file for more information.

## Acknowledgements
This project includes the arcpy package from Esri (Copyright © 1995-2022 Esri), which is subject to its own license terms. Please refer to the Esri license agreement for more information.


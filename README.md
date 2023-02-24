# ArcGIS Data Model Creation with JSON (arcgisdbmodel)
The "create_db_model.py" script is designed to create and update an ArcGIS geodatabase data model based on a JSON input file. This allows for easy modification and extension of the data model using additional JSON files at a later time.

Creating a data model using a JSON file has several advantages over manual creation in ArcGIS Pro. Here are some of them:
- Time-saving: Creating a data model using a JSON file is faster than manual creation in ArcGIS Pro because you can create the entire model in one go, rather than having to create each component one by one.
- Reusability: Once you have created a data model using a JSON file, you can reuse it multiple times, simply by modifying the file rather than recreating the model from scratch.
- Flexibility: JSON is a flexible format that allows you to easily add, remove, or modify components of the data model as needed.
- Traceability: By documenting changes to the data model in JSON files, you can easily track the evolution of the model over time and understand the reasoning behind each change.
- Collaboration: JSON files can be easily shared and edited by multiple people, making it easier to collaborate on the creation and modification of the data model.

## Getting Started
To get started with creating an ArcGIS data model using JSON, you'll need the following:
- ArcGIS Pro installed on your machine
- The "create_db_model.py" script
- A JSON file describing the data model
- A target geodatabase in which the data model is to be created: A file geodatabase (.gdb) or an enterprise geodatabase such as SQL Server (.sde), Oracle, or PostgreSQL.

## Usage
To create or update an ArcGIS data model based on a JSON input file, run the "create_db_model.py" script with the path to the JSON file as a command-line argument:

> python create_db_model.py data_model.json

## Paramters
The JSON schema and the set of JSON parameters that can be used are described in the README file [PARAMETERS.md](PARAMETERS.md).

## Tutorial
A sample JSON file and a README file with instructions can be found in the "tutorial" folder.

## Contributing
Contributions to this project are welcome! If you have any suggestions or bug reports, please open an issue or pull request on GitHub.


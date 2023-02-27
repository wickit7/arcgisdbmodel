# Tutorial 1 - Location with assets

## Introduction
In this tutorial, the data model shown in the figure below is created using JSON. The focus is on the following elements:
- create coded value domain
- create range domain
- create dataset
- create feature class
- create attribute rule (uniquie value constraint)
- create relationship (1:n)
- update feature class
    - add field
    - calculate field

### Overview data model
<img  src="..\img\tutorial_1_datamodel.jpg" width=100% height=100%>

### Example data
<img  src="..\img\tutorial_1_map.PNG" width=60% height=60%>

## Create datamodel
The datamodel is created with the JSON file [tutorial_1_create.json](tutorial_1_create.json). 
### general settings
In the general settings, the path to the log file, the path to the database and other properties are specified. The meaning of all parameters can be found in the [PARAMETERS.md](..\..\PARAMETERS.md) readme file.
- LogFolder: 	The path to the log file.
- LogVersion: The path to the folder where the log file is to be created.
- Conpath: The path to the folder where the geodatabase or the geodatabase connection file is located.
- DBName: The name of the database or connection file including the file extension. 
- Overwrite: Specify whether existing elements in the geodatabase are to be overwritten. 
- DeleteAllExisting: Specify whether all existing elements should be deleted before the new elements are created.
- SpatialReferenceName: The name of the spatial reference system, i.e. "CH1903+ LV95" for Switzerland.

```json
{
	"LogFolder": "Logs",
	"LogVersion": "v01",
	"Conpath": "C:/Temp/tutorial_1",
	"DBName": "infrastructure_management.gdb",
	"Overwrite": "True",
	"DeleteAllExisting": "True",
	"SpatialReferenceName": "CH1903+ LV95",
  
```
### coded value domains
For the feture class "asset", two coded value domains with certain possible values are needed. In the feature class "Fields"-section the corresponding field of the feature class is linked to the domain.
To create the coded value domains, the following parameters are used:
- domain_name: The name of the domain. 
- domain_description: The description of the domain. (optional)	
- field_type: The type of attribute domain to be created (data type of the "code").
- domain_type: The type of the domain.	
- DomainValues: A dictionary with "code:code_description" pairs.

```json
	"Domains": [{ 
          "domain_name": "AssetType",
          "domain_description": "Type of the asset", 
          "field_type": "SHORT",
          "domain_type": "CODED",
          "DomainValues": {"0":"unknown", "1":"street light", "2":"traffic signal", "3":"fire hydrant"}
          },
          { 
          "domain_name": "AssetStatus",
          "domain_description": "Status of the asset", 
          "field_type": "SHORT",
          "domain_type": "CODED",
          "DomainValues": {"0":"unknown", "1":"operational", "2":"under repair", "3":"out of service"}
          },
```
### range value domain
In contrast to the coded value domain, the minimum and maximum value of the range must be specified.  
- DomainRange: A dictionary with min and max values. 

```json
          {
            "domain_name": "AssetHeight",
            "domain_description": "Value between 0 und 100", 
            "field_type": "DOUBLE",
            "domain_type": "RANGE",
            "DomainRange": {"min_value":"0", "max_value":"100"}
          }
       ],

```

### dataset
The dataset is specified by defining the name.
- out_name: The name of the domain.

```json
	"Datasets": [{
				"out_name": "INFRASTRUCTURE"
			}
		],
```

### feature classes
The feature classes are created by defining general settings, fields and attribute rules.
In this case, the follwing parameters are used to define general settings:
- out_name: The name of the feature class.
- geometry_type: The geometry type, which is in this case is Polygon.
- out_dataset: The name of the output data set in which the feature class is to be created.
- GlobalID: Specify whether the feature class shuold have a GlobalID field.	The field is not defined in the "Fields" section, it will be created automatically.
- EditorTracking: Specify whether editor tracking should be activated for the feature class. The fields "CREATED_USER", "CREATED_DATE", "LAST_EDITED_USER", "LAST_EDITED_DATE" are created.
- EnableAttachments: Specify whether upload attachments should be enabled for the feature class.

```json
	"Features": [
				{
					"out_name": "LOCATION",
					"geometry_type": "POLYGON",
					"out_dataset": "INFRASTRUCTURE",
					"GlobalID": "True",
					"EditorTracking": "True",
					"EnableAttachments": "False",
```

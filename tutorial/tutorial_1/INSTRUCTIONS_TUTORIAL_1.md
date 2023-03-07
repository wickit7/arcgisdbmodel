# Tutorial 1 - Location with assets

## Introduction
- A general description of how to use the script to create a data model with JSON is found in the [README.md](../../README.md) file.
- The meaning of all parameters can be found in the [PARAMETERS.md](../../PARAMETERS.md) file.

In this tutorial, the data model shown in the figure below is created using JSON. The focus is on the following elements:
- general settings
- environment settings
- create coded value domain
- create range domain
- create dataset
- create feature class
- create attribute rule (uniquie value constraint)
- create relationship (1:n)
- update feature class
    - add field
    - calculate field

### Overview Data Model
<img  src="..\img\tutorial_1_datamodel.jpg" width=100% height=100%>

## Create Data Model
The datamodel is created with the JSON file [tutorial_1_create.json](tutorial_1_create.json). 
### General Settings
In the general settings, the path to the log file, the path to the database and other properties are specified.
- **LogFolder**: The path to the log file.
- **LogVersion**: The path to the folder where the log file is to be created.
- **Conpath**: The path to the folder where the geodatabase or the geodatabase connection file is located.
- **DBName**: The name of the database or connection file including the file extension. 
- **Overwrite**: Specify whether existing elements in the geodatabase are to be overwritten. 
- **DeleteAllExisting**: Specify whether all existing elements should be deleted before the new elements are created.
- **SpatialReferenceName**: The name of the spatial reference system, i.e. "CH1903+ LV95" for Switzerland.

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

### Environment Settings
The default environment settings can be optionally adjusted, i.e. the XY Tolerance and the XY Resolution. 

```json
	"EnvironmentSettings":{
		"xy_tolerance": "0.0004 Meters",
		"xy_resolution": "0.00005 Meters"
		},
  
```
### Coded Value Domains
For the feture class "asset", two coded value domains with certain possible values are needed. In the feature class "Fields"-section the corresponding field of the feature class is linked to the domain.
To create the coded value domains, the following parameters are used:
- **domain_name**: The name of the domain. 
- **domain_description**: The description of the domain. (optional)	
- **field_type**: The type of attribute domain to be created (data type of the "code").
- **domain_type**: The type of the domain.	
- **DomainValues**: A dictionary with "code:code_description" pairs.

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
### Range Value Domain
In contrast to the coded value domain, the minimum and maximum value of the range must be specified.  
- **DomainRange**: A dictionary with min and max values. 

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

### Dataset
The dataset is specified by defining the name.
- **out_name**: The name of the domain.

```json
	"Datasets": [{
				"out_name": "INFRASTRUCTURE"
			}
		],
```

### Feature Class LOCATION - General Settings
The feature classes are created by defining general settings, fields and attribute rules.
Here, the follwing parameters are used to define general settings:
- **out_name**: The name of the feature class.
- **geometry_type**: The geometry type, which is in this case is Polygon.
- **out_dataset**: The name of the output data set in which the feature class is to be created.
- **GlobalID**: Specify whether the feature class shuold have a GlobalID field.	The field is not defined in the "Fields" section, it will be created automatically.
- **EditorTracking**: Specify whether editor tracking should be activated for the feature class. The fields "CREATED_USER", "CREATED_DATE", "LAST_EDITED_USER", "LAST_EDITED_DATE" are created.
- **EnableAttachments**: Specify whether upload attachments should be enabled for the feature class.

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

### Feature Class LOCATION - Fields
The follwing parameters are used to create the fields of the feature classes:
- **field_name**: The name of the field. 
- **field_type**: The field type.
- **field_length**: The field length for the fields of type text. (optional)
- **field_alias**: The alternate name for the field. 

```json
					"Fields": [{
						"field_name": "LocationID",
						"field_type": "LONG",
						"field_alias": "Location ID"
						},
						{
						"field_name": "NAME",
						"field_type": "TEXT",
						"field_length": "40",
						"field_alias": "Location Name"
						},
						{
						"field_name": "DESCRIPTION",
						"field_type": "TEXT",
						"field_length": "512",
						"field_alias": "Description"
						},
							{
						"field_name": "ADDRESS",
						"field_type": "TEXT",
						"field_length": "255",
						"field_alias": "Address"
						},
						{
						"field_name": "CITY",
						"field_type": "TEXT",
						"field_length": "255",
						"field_alias": "City"
						},
						{
						"field_name": "ZIP_CODE",
						"field_type": "TEXT",
						"field_length": "4",
						"field_alias": "Zip Code"
						}						
					],
```

### Feature Class LOCATION - Attribute Rules
An attribute rule is created to prevent the user from defining the same "LocationID" for two different features.
- **name**: The name of the rule.
- **type**: The type of the rule. 
- **script_expression**: An Arcade script expression. 
- **triggering_events**: Secify when the rule is triggered.
- **description**: The description of the rule.
- **error_number**: An error number that is returned when the rule is violated.
- **error_message**: An error message returned if the rule is violated.

```json

					"AttributeRules": [
						{
						"name": "UNIQUE_LOCATION_ID",
						"type": "CONSTRAINT",
						"script_expression":"var orgID = $originalFeature.LocationID;  var newID = $feature.LocationID;  if (newID==orgID) {   return true;  } else {   var location_fc = FeatureSetbyName($datastore, 'LOCATION', ['LocationID', 'GlobalID'], false);  var location_fc_filter = filter(location_fc, 'LocationID = @newID'); if (count(location_fc_filter) > 1) {     return false; } else {     return true;      } }",
						"triggering_events": "INSERT;UPDATE",
						"description": "Checking if location with the entered LocationID does already exist",
						"error_number": "1",
						"error_message": "The entered Location ID does already exist!"
						}
					]	
				},
```	

### Feature Class ASSET
In the same way, the feature class ASSET is created. To assign a domain to a field, the parameter "field_domain is used".
- **field_domain**: The name of the domain to be used for the field.

```json
				{
					"out_name": "ASSET",
					"geometry_type": "POINT",
					"out_dataset": "INFRASTRUCTURE",
					"GlobalID": "True",
					"EditorTracking": "True",
					"EnableAttachments": "True",
					"Fields": [{
						"field_name": "AssetID",
						"field_type": "LONG",
						"field_alias": "Asset ID"
						},
						{
						"field_name": "TYPE",
						"field_type": "SHORT",
						"field_domain": "AssetType",
						"field_alias": "Asset Type"
						},
						{
						"field_name": "DESCRIPTION",
						"field_type": "TEXT",
						"field_length": "512",
						"field_alias": "Description"
						},
						{
						"field_name": "MANUFACTURER",
						"field_type": "TEXT",
						"field_length": "255",
						"field_alias": "Manufacturer"
						},		
						{
						"field_name": "STATUS",
						"field_type": "SHORT",
						"field_domain": "AssetStatus",
						"field_alias": "Status"
						},
						{
						"field_name": "HEIGHT",
						"field_type": "DOUBLE",
						"field_domain": "AssetHeight",
						"field_alias": "Asset Height"
						},
						{
						"field_name": "FEATURELINK",
						"field_type": "GUID",
						"field_alias": "Location Reference"
						}						
					],
					"AttributeRules": [
						{
						"name": "UNIQUE_ASSET_ID",
						"type": "CONSTRAINT",
						"script_expression":"var orgID = $originalFeature.AssetID;  var newID = $feature.AssetID;  if (newID==orgID) {   return true;  } else {   var asset_fc = FeatureSetbyName($datastore, 'ASSET', ['AssetID', 'GlobalID'], false);  var asset_fc_filter = filter(asset_fc, 'AssetID = @newID'); if (count(asset_fc_filter) > 1) {     return false; } else {     return true;      } }",
						"triggering_events": "INSERT;UPDATE",
						"description": "Checking if asset with the entered AssetID does already exist",
						"error_number": "1",
						"error_message": "The entered Asset ID does already exist!"
						}
					]			
				}
				],

```


### Relationship Class
Finally, the follwoing parameters are used to define the "One to Many"-realtionship between LOCATION and ASSET.
- **origin_table**: The name of the source table or feature class.
- **destination_table**: The name of the destination table or feature class.
- **out_relationship_class**: The name of relationship class to be created.
- **relationship_type**: The relationship type.
- **forward_label**: The name to identify the relationship when navigationg from the origin table to the destination table. 
- **backward_label**: The name to identify the relationship when navigationg from the destination table to the origin table.
- **message_direction**: The message direction. Here, the assets should be deleted if the parent object location is deleted.
- **cardinality**: The cardinality of the relationship.	
- **origin_primary_key**: The primary key (field name) in the source table.
- **origin_foreign_key**: The field name in the destiation table that stores the primary key of the source table.

```json
	"Relations": [{
					"origin_table": "LOCATION",
					"destination_table": "ASSET",
					"out_relationship_class": "LOCATION_ASSET_REL",
					"relationship_type": "COMPOSITE",
					"forward_label": "Loction has Assets",
					"backward_label": "Asset belongs to a location",
					"message_direction": "FORWARD",
					"cardinality": "ONE_TO_MANY",
					"origin_primary_key": "GlobalId",
					"origin_foreign_key": "FEATURELINK"				
				}
			]	
}
```

## Update Data Model
The data model is updated with the JSON file [tutorial_1_update.json](tutorial_1_update.json).

At a later stage, there is a requirement to add a new attribute STATE to the feature class LOCATION. The existing data entries are to be populated with the value "Switzerland". A simple calculation expression is used to create a value that will populate existing rows.  As you can see, the "LogVersion" is set to "v02" and "DeleteAllExisting" is set to "False". 

```json
{
	"LogFolder": "Logs",
	"LogVersion": "v02",
	"Conpath": "C:/Temp/tutorial_1",
	"DBName": "infrastructure_management.gdb",
	"Overwrite": "True",
	"DeleteAllExisting": "False",
	"SpatialReferenceName": "CH1903+ LV95",
	"UpdateFeatures": [{
		"in_table": "LOCATION",
		"AddFields": [
			{
			"field_name": "STATE",
			"field_type": "TEXT",
			"field_length": "255",
			"field_alias": "State"
			}			
			],
		"CalculateFields": [
			{
			"field": "STATE",
			"expression": "'Switzerland'"
			}
			]
		}]	
}

```

## Example Data
<img  src="..\img\tutorial_1_map.PNG" width=60% height=60%>



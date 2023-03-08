# Tutorial 4 - Relationship editing with attribute rules

## Introduction
- A general description of how to use the script to create a data model with JSON is found in the [README.md](../../README.md) file.
- The meaning of all parameters can be found in the [PARAMETERS.md](../../PARAMETERS.md) file.

In this tutorial, the data model shown in the figure below is created using JSON. The focus is on the following elements:
- Attribute rules to edit related feature classes
- Attribute rule that contains multiple feature classes

Actually, it is not necessary to edit the related features using attribute rules, as this is done by the relationship class. For example in ArcGIS Pro editing tools are available that allow the editing of feature relationships. 
In certain web applications (e.g. Web AppBuilder) such editing tools are not or not yet available. In this case editing realtionships with attribute rules can be an alternative. 


### Overview Data Model
<img  src="..\img\tutorial_4_datamodel.jpg" width=100% height=100%>

## Create Data Model
The datamodel is created with the JSON file [tutorial_1_create.json](tutorial_1_create.json). 
### General Settings
In the general settings, the path to the log file, the path to the database and other properties are specified (see tutorial 1).

```json
{
    "LogFolder":"Logs",
    "LogVersion":"v01",
    "Conpath":"C:/Temp/tutorial_4",
    "DBName":"asset_management.gdb",
    "Overwrite":"True",
    "DeleteAllExisting":"True",
    "SpatialReferenceName":"CH1903+ LV95",
  
```

### Coded Value Domain
For the feature class "asset", a coded value domains with certain possible values is created (see tutorial 1).


```json
    "Domains":[
        {
            "domain_name":"AssetType",
            "domain_description":"Type of the asset",
            "field_type":"SHORT",
            "domain_type":"CODED",
            "DomainValues":{
                "0":"unknown",
                "1":"street light",
                "2":"traffic signal",
                "3":"fire hydrant"
            }
        }
    ],
```

### Dataset
The dataset is specified by defining the name.

```json
	"Datasets": [{
				"out_name": "INFRASTRUCTURE"
			}
		],
```

### Feature Class LOCATION
The feature classes is created by defining general settings and fields (see tutorial 1).

```json
    "Features":[
        {
            "out_name":"LOCATION",
            "geometry_type":"POLYGON",
            "out_dataset":"INFRASTRUCTURE",
            "GlobalID":"True",
            "EditorTracking":"False",
            "EnableAttachments":"False",
            "Fields":[
                {
                    "field_name":"LocationID",
                    "field_type":"LONG",
                    "field_alias":"Location ID"
                },
                {
                    "field_name":"NAME",
                    "field_type":"TEXT",
                    "field_length":"40",
                    "field_alias":"Location Name"
                },
                {
                    "field_name":"DESCRIPTION",
                    "field_type":"TEXT",
                    "field_length":"512",
                    "field_alias":"Description"
                }
            ]
        },
```

### Feature Class ASSET
In the same way, the feature class ASSET is created. 
```json
        {
            "out_name":"ASSET",
            "geometry_type":"POINT",
            "out_dataset":"INFRASTRUCTURE",
            "GlobalID":"True",
            "EditorTracking":"False",
            "EnableAttachments":"False",
            "Fields":[
                {
                    "field_name":"AssetID",
                    "field_type":"LONG",
                    "field_alias":"Asset ID"
                },
                {
                    "field_name":"LocationID",
                    "field_type":"LONG",
                    "field_alias":"Location ID"
                },
                {
                    "field_name":"TYPE",
                    "field_type":"SHORT",
                    "field_domain":"AssetType",
                    "field_alias":"Asset Type"
                },
                {
                    "field_name":"FEATURELINK",
                    "field_type":"GUID",
                    "field_alias":"Location Reference"
                }
            ],
            "AttributeRules":[
                {
                    "name":"UPDATE_FEATURELINK",
                    "type":"CALCULATION",
                    "script_expression":"var origID = $originalFeature.LocationID;  var newID = $feature.LocationID;  if (newID != origID) { if (IsEmpty(newID)) return NULL;     var parent_fc = FeatureSetByName($datastore,'LOCATION',['LocationID', 'GlobalID'],false);      var parent_selection = Filter(parent_fc, 'LocationID = @newID');      if (Count(parent_selection)>0) {          return First(parent_selection).GlobalID;     } else  {          return {'errorMessage': 'There is no parent feature (location) with this LocationID!'};     }  } else {     return $feature.FEATURELINK; } ",
                    "triggering_events":"UPDATE",
                    "description":"Update FEATURELINK of the child object (asset) with the GlobalID of the parent feature (location) by entering the LocationID",
                    "field":"FEATURELINK",
                    "exclude_from_client_evaluation":"EXCLUDE"
                },
                {
                    "name":"UPDATE_LocationID",
                    "type":"CALCULATION",
                    "script_expression":"var origFeaturelink = $originalFeature.FEATURELINK;  var newFeaturelink = $feature.FEATURELINK;  if (newFeaturelink != origFeaturelink){     if (IsEmpty(newFeaturelink)) return NULL;     var parent_fc = FeatureSetByName($datastore,'LOCATION',['LocationID', 'GlobalID'],false);      var parent_selection = Filter(parent_fc, 'GlobalID = @newFeaturelink');      if (Count(parent_selection)>0) {          return First(parent_selection).LocationID      } else {          return {'errorMessage': 'No referenced parent feature (location) could be found!'}      }  } else {     return $feature.LocationID }",
                    "triggering_events":"INSERT;UPDATE",
                    "description":"Update LocationID with the LocationID of the parent feature (location) when creating the child object (asset)",
                    "field":"LocationID",
                    "exclude_from_client_evaluation":"EXCLUDE"
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
- **forward_label**: The name to identify the relationship when navigating from the origin table to the destination table. 
- **backward_label**: The name to identify the relationship when navigating from the destination table to the origin table.
- **message_direction**: The message direction. Here, the assets should be deleted if the parent object location is deleted.
- **cardinality**: The cardinality of the relationship.	
- **origin_primary_key**: The primary key (field name) in the source table.
- **origin_foreign_key**: The field name in the destiation table that stores the primary key of the source table.

```json
    "Relations":[
        {
            "origin_table":"LOCATION",
            "destination_table":"ASSET",
            "out_relationship_class":"LOCATION_ASSET_REL",
            "relationship_type":"COMPOSITE",
            "forward_label":"Loction has Assets",
            "backward_label":"Asset belongs to a location",
            "message_direction":"FORWARD",
            "cardinality":"ONE_TO_MANY",
            "origin_primary_key":"GlobalId",
            "origin_foreign_key":"FEATURELINK"
        }
    ],
```

## Attribute rule depending on multiple feature classes
The data model is updated with the JSON file [tutorial_1_update.json](tutorial_1_update.json).

At a later stage, there is a requirement to add a new attribute STATE to the feature class LOCATION. The existing data entries are to be populated with the value "Switzerland". A simple calculation expression is used to create a value that will populate existing rows.  As you can see, the "LogVersion" is set to "v02" and "DeleteAllExisting" is set to "False". 

```json
    "UpdateFeatures":[
        {
            "in_table":"LOCATION",
            "AttributeRules":[
                {
                    "name":"UPDATE_LocationID_CHILD",
                    "type":"CALCULATION",
                    "script_expression":"var origID =  $originalFeature.LocationID; var newID = $feature.LocationID; if (newID==origID) {     return origID; } else {     var updates = [];     var counter = 0;     var globalId = $feature.globalid;     var child_fc = FeatureSetbyName($datastore, 'ASSET', ['FEATURELINK', 'LocationID', 'GlobalID'], false);     var child_selection = filter(child_fc, 'FEATURELINK = @globalId');     if (count(child_selection) > 0) {         for (var child in child_selection) {             updates[counter] = {'globalID': child.GlobalID,                                 'attributes': {                                     'LocationID': newID                                     }                                 };            counter++;         }     return {'result': newID,             'edit':[{'className': 'Asset',                      'updates': updates}]};    } else {         return newID;    } } ",
                    "triggering_events":"INSERT;UPDATE",
                    "description":"Update  'LocationID' of all child objects (assets) when 'LocatonID' of parent object (location) changes",
                    "field":"LocationID",
                    "exclude_from_client_evaluation":"EXCLUDE"
                }
            ]
        }
    ]
}

```

## Example Data
<img  src="..\img\tutorial_4_map.PNG" width=60% height=60%>


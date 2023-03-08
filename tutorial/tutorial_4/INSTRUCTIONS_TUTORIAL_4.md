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
<img  src="..\img\tutorial_4_datamodel.jpg" width=80% height=80%>

## Create Data Model
The datamodel is created with the JSON file [tutorial_4_create.json](tutorial_4_create.json). 
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
The feature class is created by defining general settings and fields (see tutorial 1).

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
In the same way, the feature class ASSET is created. Additionally attribute rules are created, that allow editing realted data without special editing tools.

**Attribute Rule "UPDATE_FEATURELINK"**
This attribute rule is used to automatically update the field "FEATURELINK" of the child objects "ASSET" with the GlobalID of the parent feature "LOCATION" when the  LocationID in the parent feature "LOCATION" is edited.

**Attribute Rule "UPDATE_LocationID"**
This attribute rule is used to automatically update the field "LocationID" with the LocationID of the parent feature "Location" when a child object "ASSET" is created with editing tools for editing feature relationships (e.g. in ArcGIS Pro), where the "FEATURELINK" is filled in automatically.

- **script_expression**: An [Arcade script expression](https://pro.arcgis.com/en/pro-app/latest/help/data/geodatabases/overview/attribute-rule-script-expression.htm). 

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
A "One to Many"-realtionship class is created between LOCATION and ASSET (see tutorial 1).

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
The attribute rule that depends on the feature classes "LOCATION" and "ASSET" must be included in the "UpdateFeatures" section of the JSON file, so it is created when the feature classes already exist. The Attribute rule **"UPDATE_LocationID_CHILD"** updates the "LocationID" of all child fetures "ASSET" when the value of the "LocationID" is edited in the parent feature "LOCATION".

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
<img  src="..\img\tutorial_4_map.PNG" width=80% height=80%>


# Tutorial 5 - Estimation of road construction costs

## Introduction
- A general description of how to use the script to create a data model with JSON is found in the [README.md](../../README.md) file.
- The meaning of all parameters can be found in the [PARAMETERS.md](../../PARAMETERS.md) file.

In this tutorial, the data model shown in the figure below is created using JSON. The data model is used to estimate road construction costs depending on the road material.

The focus is on the following element:
- Attribute rules depending on subtypes

### Overview Data Model
<img  src="..\img\tutorial_5_datamodel.jpg" width=30% height=30%>

## Create Data Model
The datamodel is created with the JSON file [tutorial_5_create.json](tutorial_5_create.json). 

### General Settings, Datset
The general settings and a dataset are specified in the first part of the JSON (see tutorial 1).

```json
{
   "LogFolder":"Logs",
   "LogVersion":"v01",
   "Conpath":"C:/Temp/tutorial_5",
   "DBName":"road_management.gdb",
   "Overwrite":"True",
   "DeleteAllExisting":"True",
   "SpatialReferenceName":"CH1903+ LV95",
   "Datasets":[
      {
         "out_name":"ROAD_MANAGEMENT"
      }
   ],
  
```

### Feature Class ROAD
The feature class "ROAD" is created by defining general settings, subtypes, fields and attribute rules (see tutorial 2).
- **subtype**: This parameter specifies for which subtype the rule is to be active.

**Attribute Rule "CALCULATE_COST_1"**: The attribute rule is used to estimate the cost of road surfaces to be built with asphalt. It is assumed that 1m<sup>2</sup> of road construction costs 60$.

**Attribute Rule "CALCULATE_COST_2"**: The attribute rule is used to estimate the cost of road surfaces to be built with concrete. It is assumed that 1m<sup>2</sup> of road construction costs 80$.

**Attribute Rule "CALCULATE_COST_3"**: The attribute rule is used to estimate the cost of road surfaces to be built with cobblestone. It is assumed that 1m<sup>2</sup> of road construction costs 100$.

```json
,
   "Features":[
      {
         "out_name":"ROAD",
         "geometry_type":"POLYGON",
         "out_dataset":"ROAD_MANAGEMENT",
         "GlobalID":"True",
         "EditorTracking":"False",
         "EnableAttachments":"False",
         "Subtypes":{
            "field_name":"TYP",
            "SubtypeValues":{
               "1":"Asphalt",
               "2":"Concrete",
               "3":"Cobblestone"
            },
            "DefaultSubtypeCode":"1"
         },
         "Fields":[
            {
               "field_name":"NAME",
               "field_type":"TEXT",
               "field_length":"40",
               "field_alias":"Name"
            },
            {
               "field_name":"DESCRIPTION",
               "field_type":"TEXT",
               "field_length":"512",
               "field_alias":"Description"
            },
            {
               "field_name":"COST",
               "field_type":"DOUBLE",
               "field_alias":"Cost"
            }
		],
		"AttributeRules": [
			{
			"name": "CALCULATE_COST_1",
			"type": "CALCULATION",
			"script_expression":"return $feature['Shape_Area']*60",
			"triggering_events": "INSERT;UPDATE",
			"description": "Calculation of costs based on area and cost per square metre for asphalt",
			"field": "COST",
			"subtype": "Asphalt"
			},
			{
			"name": "CALCULATE_COST_2",
			"type": "CALCULATION",
			"script_expression":"return $feature['Shape_Area']*80",
			"triggering_events": "INSERT;UPDATE",
			"description": "Calculation of costs based on area and cost per square metre for concrete",
			"field": "COST",
			"subtype": "Concrete"
			},
			{
			"name": "CALCULATE_COST_3",
			"type": "CALCULATION",
			"script_expression":"return $feature['Shape_Area']*100",
			"triggering_events": "INSERT;UPDATE",
			"description": "Calculation of costs based on area and cost per square metre for cobblestone",
			"field": "COST",
			"subtype": "Cobblestone"
			}
		]
	}
	]
```

## Example Data
<img  src="..\img\tutorial_5_map.PNG" width=70% height=70%>


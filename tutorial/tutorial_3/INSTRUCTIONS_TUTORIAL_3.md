# Tutorial 3 - Event Management (Many to Many-Relationship)

## Introduction
- A general description of how to use the script to create a data model with JSON is found in the [README.md](../../README.md) file.
- The meaning of all parameters can be found in the [PARAMETERS.md](../../PARAMETERS.md) file.

In this tutorial, the data model shown in the figure below is created using JSON. The data model is used to manage event locations and the associated events.
An event location can have multiple events and an event can take place at multiple event locations.

The focus is on the following elements:
- Table
- Relationship "Many to Many" (n:m) with attributed fields

### Overview Data Model
<img  src="..\img\tutorial_3_datamodel.jpg" width=100% height=100%>

## Create Data Model
The datamodel is created with the JSON file [tutorial_3_create.json](tutorial_3_create.json). 
### General Settings
In the general settings, the path to the log file, the path to the database and other properties are specified.

```json
{
   "LogFolder":"Logs",
   "LogVersion":"v01",
   "Conpath":"C:/Temp/tutorial_3",
   "DBName":"event_management.gdb",
   "Overwrite":"True",
   "DeleteAllExisting":"True",
   "SpatialReferenceName":"CH1903+ LV95",
  
```

### Dataset
The dataset is specified by defining the name.

```json
   "Datasets":[
      {
         "out_name":"EVENT_MANAGEMENT"
      }
   ],
```

### Feature Class
The feature classe LOCATION is created by defining general settings and fields.

```json
   "Features":[
      {
         "out_name":"LOCATION",
         "geometry_type":"POINT",
         "out_dataset":"EVENT_MANAGEMENT",
         "GlobalID":"True",
         "EditorTracking":"True",
         "EnableAttachments":"True",
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
               "field_name":"OWNER",
               "field_type":"TEXT",
               "field_length":"255",
               "field_alias":"Owner"
            },
            {
               "field_name":"DESCRIPTION",
               "field_type":"TEXT",
               "field_length":"512",
               "field_alias":"Description"
            }
		]
	}],
```


### Table
The table EVENT is created by defining general settings and fields.

```json
	"Tables": [{	
         "out_name":"EVENT",
         "geometry_type":"POINT",
         "out_dataset":"EVENT_MANAGEMENT",
         "GlobalID":"True",
         "EditorTracking":"True",
         "EnableAttachments":"True",
         "Fields":[
            {
               "field_name":"EventID",
               "field_type":"LONG",
               "field_alias":"Event ID"
            },
            {
               "field_name":"NAME",
               "field_type":"TEXT",
               "field_length":"40",
               "field_alias":"Event Name"
            },
            {
               "field_name":"ORGANIZER",
               "field_type":"TEXT",
               "field_length":"255",
               "field_alias":"Organizer"
            },
            {
               "field_name":"DESCRIPTION",
               "field_type":"TEXT",
               "field_length":"512",
               "field_alias":"Description"
            }
		]
	}],
```

### Relationship Class "Many to Many"
Finally, the follwoing parameters are used to define the "Many to Many"-relationship between LOCATION and EVENT.
- **origin_table**: The name of the source table or feature class.
- **destination_table**: The name of the destination table or feature class.
- **out_relationship_class**: The name of relationship class to be created.
- **relationship_type**: The relationship type.
- **forward_label**: The name to identify the relationship when navigating from the origin table to the destination table. 
- **backward_label**: The name to identify the relationship when navigating from the destination table to the origin table.
- **message_direction**: The message direction.
- **cardinality**: The cardinality of the relationship.	
- **origin_primary_key**: The primary key (field name) in the source table.
- **origin_foreign_key**: The field name in the relationship class (in case of "Many to Many"-relation) that stores the primary key of the source table.
- **destination_primary_key**: The primary key (field name) in the destination table.
- **destination_foreign_key**: The field name in the relationship class that stores the primary key of the destination table.
- **AttributedFields**: A list of fields to be added to the relationship class.

```json
	"Relations": [{
					"origin_table": "EVENT",
					"destination_table": "LOCATION",
					"out_relationship_class": "EVENT_LOCATION_REL",
					"relationship_type": "SIMPLE",
					"forward_label": "Event has Locations",
					"backward_label": "Location has Events",
					"message_direction": "NONE",
					"cardinality": "MANY_TO_MANY",
					"origin_primary_key": "GlobalId",
					"origin_foreign_key": "FEATURELINK_EVENT",
					"destination_primary_key": "GlobalId",
					"destination_foreign_key": "FEATURELINK_LOCATION",					
					"AttributedFields":[{
						"field_name": "START_DATE",
						"field_type": "DATE",
						"field_alias":"Start Date"
						},
						{
						"field_name": "END_DATE",
						"field_type": "DATE",
						"field_alias":"End Date"
						}	
					]	
				}
			]	
}
```

## Example Data
<img  src="..\img\tutorial_3_map.PNG" width=60% height=60%>


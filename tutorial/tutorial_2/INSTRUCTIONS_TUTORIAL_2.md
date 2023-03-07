# Tutorial 2 - Location Management (Subtypes)

## Introduction
- A general description of how to use the script to create a data model with JSON is found in the [README.md](../../README.md) file.
- The meaning of all parameters can be found in the [PARAMETERS.md](../../PARAMETERS.md) file.

In this tutorial, the focus is on the following elements:
- subtypes
- domain depending on subtypes
- relation depending on subtypes

### Overview Data Model v01
<img  src="..\img\tutorial_2_datamodel_v01.jpg" width=80% height=80%>

## Create Data Model
The datamodel is created with the JSON file [tutorial_2_create.json](tutorial_2_create.json). 

### General Settings
In the general settings, the path to the log file, the path to the database and other properties are specified (see tutorial 1).

```json
{
   "LogFolder":"Logs",
   "LogVersion":"v01",
   "Conpath":"C:/Temp/tutorial_2",
   "DBName":"location_management.gdb",
   "Overwrite":"True",
   "DeleteAllExisting":"True",
   "SpatialReferenceName":"CH1903+ LV95",
  
```

### Coded Value Domains
For each subtype of the feature class "LOCATION", a different coded value domain with certain possible values is needed (see tutorial 1).

```json
   "Domains":[
      {
         "domain_name":"ShopType",
         "domain_description":"Type of the shop",
         "field_type":"SHORT",
         "domain_type":"CODED",
         "DomainValues":{
            "1":"Clothing store",
            "2":"Bookstore",
            "3":"Electronic store",
            "4":"Toy store",
            "5":"Gift shop",
            "6":"Convenience store",
            "7":"Pet store",
            "8":"Furniture store",
            "9":"Jewlery store",
            "10":"Health and beauty store",
            "99":"Others"
         }
      },
      {
         "domain_name":"RestaurantType",
         "domain_description":"Type of the restaurant",
         "field_type":"SHORT",
         "domain_type":"CODED",
         "DomainValues":{
            "1":"Fast food restaurant",
            "2":"Fine dining restaurant",
            "3":"Cafe or coffee shop",
            "4":"Street vendor",
            "5":"Bar or pub",
            "6":"Bakery or pastry shop",
            "7":"Ice cream or dessert shop",
            "99":"Others"
         }
      },
      {
         "domain_name":"EventType",
         "domain_description":"Type of the event",
         "field_type":"SHORT",
         "domain_type":"CODED",
         "DomainValues":{
            "1":"Music concerts",
            "2":"Festivals",
            "3":"Sports matches",
            "4":"Art exhibitions",
            "5":"Trade shows",
            "6":"Movie screenings",
            "7":"Charity events",
            "8":"Food fairs and competitions",
            "9":"Conferences",
            "10":"Theater performances",
            "99":"Others"
         }
      }
   ],
```

### Dataset
The feature classes will be stored in the dataset "LOCATION_MANAGEMENT".

```json
	"Datasets": [{
				"out_name": "LOCATION_MANAGEMENT"
			}
		],
```

### Feature Class LOCATION
The feature class "Location" is created by defining general settings, subtypes and fields.

The following parameters are used to define the subtypes and to assign the domains to the corresponding subtypes:
- **Subtypes**: A dictionary with subtypes to be created for the feature class.
- **Subtypes/field_name**: The name of the field in which the subtype value is stored.
- **Subtypes/SubtypeValues**: A dictionary with pairs of "Code:Code_description" defining the subtypes.
- **Subtypes/DefaultSubtypeCode**: The code of the subtype to be used as the default.
- **FieldDomainSubtype**:  A list of domain assignments depending on the subtypes.
- **FieldDomainSubtype/field_domain**: The name of the domain to be used for the field and the specific subtype.
- **FieldDomainSubtype/subtype_code**:  Assign the domain to a specific subtype with "code:code_description" pairs (separated by ";" if a domain is to be used for multiple subtypes).

```json
   "Features":[
      {
         "out_name":"LOCATION",
         "geometry_type":"POINT",
         "out_dataset":"LOCATION_MANAGEMENT",
         "GlobalID":"True",
         "EditorTracking":"True",
         "EnableAttachments":"True",
         "Subtypes":{
            "field_name":"TYP",
            "SubtypeValues":{
               "1":"Shop",
               "2":"Restaurant",
               "3":"Event"
            },
            "DefaultSubtypeCode":"1"
         },
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
            },
            {
               "field_name":"SERVICE_TYPE",
               "field_type":"SHORT",
               "FieldDomainSubtype":[
                  {
                     "field_domain":"ShopType",
                     "subtype_code":"1: Shop"
                  },
                  {
                     "field_domain":"RestaurantType",
                     "subtype_code":"2: Restaurant"
                  },
                  {
                     "field_domain":"EventType",
                     "subtype_code":"3: Event"
                  }
               ]
            }
		]
	}
	]
}
```

## Update Data Model
The data model is updated with the JSON file [tutorial_2_update.json](tutorial_2_update.json).

At a later stage, it will be necessary to add a new feature class in which the occupied areas of the locations can be stored.

### Overview Data Model v02
<img  src="..\img\tutorial_2_datamodel_v02.jpg" width=80% height=80%>

### Feature Class LOCATION_AREA
The feature class "LOCATION_AREA" has the subtypes "ShopArea", "RestaurantArea" and "EventArea".

```json
{
	"LogFolder": "Logs",
	"LogVersion": "v02",
	"Conpath": "C:/Temp/tutorial_2",
	"DBName": "location_management.gdb",
	"Overwrite": "True",
	"DeleteAllExisting": "False",
	"SpatialReferenceName": "CH1903+ LV95",
	"Features":[
			{
				"out_name": "LOCATION_AREA",
				"geometry_type": "POLYGON",
				"out_dataset": "LOCATION_MANAGEMENT",
				"GlobalID": "True",
				"EditorTracking": "True",
				"Subtypes":{
					"field_name": "TYP",
					"SubtypeValues": {"1": "ShopArea", "2":"RestaurantArea", "3": "EventArea"}
					},					
				"Fields": [
					{
					"field_name": "NUMBER",
					"field_type": "LONG",
					 "field_alias":"Number"

					},
					{
					   "field_name":"DESCRIPTION",
					   "field_type":"TEXT",
					   "field_length":"512",
					   "field_alias":"Description"
					},
					{
					"field_name": "FEATURELINK",
					"field_type": "GUID"
					}
				]
			}
		],

```

### Relationship Class depending on subtypes
The relationship between "LOCATION" and "LOCATION_AREA" depends on the subtypes.

The following parameters are used to define the relation depending on the subtypes:
- **Rules**: A list of rules is used to define the relationship for certain subtypes.
- **Rules/origin_subtype**: The subtype of the source table for which the rule is to apply.
- **Rules/destination_subtype**: The subtype of the destination table for which the rule is to apply.
- **Rules/destination_minimum**: The minimum number of child objects (target objects) that the parent object (source object) must have.
(optional)
- **Rules/destination_maximum**: The maximum number of child objects (target objects) that the parent object (source object) must have.
(optional)

```json
	"Relations": [{
					"origin_table": "LOCATION",
					"destination_table": "LOCATION_AREA",
					"out_relationship_class": "LOCATION_LOCATION_AREA_REL",
					"relationship_type": "COMPOSITE",
					"forward_label": "Location has areas",
					"backward_label": "Area belongs to a location",
					"message_direction": "FORWARD",
					"cardinality": "ONE_TO_MANY",
					"origin_primary_key": "GlobalId",
					"origin_foreign_key": "FEATURELINK",
					"Rules":[
						{
						"origin_subtype": "Shop",
						"destination_subtype": "ShopArea",
						"destination_minimum": "0",
						"destination_maximum": "100"
						},
						{
						"origin_subtype": "Restaurant",
						"destination_subtype": "RestaurantArea",
						"destination_minimum": "0",
						"destination_maximum": "100"
						},
						{
						"origin_subtype": "Event",
						"destination_subtype": "EventArea",
						"destination_minimum": "0",
						"destination_maximum": "100"
						}
					]
				}
			]	
}
```

## Example Data
<img  src="..\img\tutorial_2_map.PNG" width=60% height=60%>



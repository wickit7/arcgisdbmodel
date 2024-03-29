# JSON file input parameters
- A general description of how to use the script to create a data model with JSON is found in the [README.md](../../README.md) file.
- Example JSON files are found in the [tutorial](tutorial) folder.
- The implemented functions (e.g. "add_field()") include all parameters of the corresponding ArcGIS function (e.g. "AddField()") and possibly  additional parameters.


| Parameter Name|    Description    | Example |
| --- | --- | --- |
| LogFolder | The path to the folder where the log file is to be created. (mandatory) | "C:/tutorial/Logs" |
| LogVersion | A string that is used as postfix for the log file name. (mandatory) | "v01" |
| Conpath | The path to the folder where the geodatabase or the geodatabase connection file is located. (mandatory) | "C:/tutorial" |
| DBName | The name of the database or connection file including the file extension. (mandatory) | "event.gdb" or "event.owner.test.sde" |
| Overwrite | The ArcGIS Environment Setting "overwrite". (mandatory) | "True" or "False" |
| DeleteAllExisting | Specify whether all existing objects in the database should be deleted beforehand. (optional) | "True" or "False"(default)|
| SpatialReferenceName | The name of the spatial reference system. → [https://epsg.io/](https://epsg.io/) (mandatory)| "CH1903+ LV95"(default) |
| **EnvironmentSettings** | A dictionary with [ArcGIS Environment](https://pro.arcgis.com/en/pro-app/latest/tool-reference/appendices/spatial-reference-and-geoprocessing.htm) settings (some settings are only applied to feature classes within datasets). (optional)| --- |
| EnvironmentSettings/xy_tolerance | see in the ArcGIS documentation | "0.0004 Meters" |
| EnvironmentSettings/xy_resolution | see in the ArcGIS documentation | "0.00005 Meters" |
| EnvironmentSettings/xy_domain | see in the ArcGIS documentation | "-180 -90 180 90" |
| EnvironmentSettings/output_z_flag | see in the ArcGIS documentation | "Enabled" |
| EnvironmentSettings/z_resolution | see in the ArcGIS documentation | "0.02 Meters" |
| EnvironmentSettings/z_domain | see in the ArcGIS documentation | "0 25000" |
| EnvironmentSettings/output_z_value | see in the ArcGIS documentation | "100" |
| EnvironmentSettings/output_m_flag | see in the ArcGIS documentation | "Enabled" |
| EnvironmentSettings/m_tolerance | see in the ArcGIS documentation | "0.02" |
| EnvironmentSettings/m_resolution | see in the ArcGIS documentation | "0.002" |
| EnvironmentSettings/m_domain | see in the ArcGIS documentation | "0 10000000" |
| **Domains**  | A list of domains to be created → see Esri doc arcpy.management.CreateDomain. (optional) | --- |
| Domains/domain_name | The name of the domain. (mandatory)| "Type_Event" |
| Domains/domain_description | The description of the domain. (optional)| "Type_Event" |
| Domains/field_type | The type of attribute domain to be created. (mandatory) | "SHORT" |
| Domains/domain_type | The type of the domain. |  "CODED"(default) or "RANGE" |
| Domains/* | All other parameters of "arcpy.management.CreateDomain" can be used. (optional) | --- |
| Domains/DomainValues | A dictionary with "code:code_description" pairs. (mandatory if domain_type = "CODED")| {"0":"unknown", "1":"public", "2":"private"} 
| Domains/DomainRange | A dictionary with min and max values. (mandatory if domain_type = "RANGE")| {"min_value":"0", "max_value":"100"} |
|  **Datasets**  | A list of datasets to be created → see Esri documentation arcpy.management.CreateFeatureDataset. (optional) | --- |
| Datasets/out_name | The name of the dataset to be created. (mandatory)| "EVENT" |
| **Features** | A list of feature classes to be created → see Esri doc arcpy.management.CreateFeatureclass. (optional)  | --- |
| Features/out_name | The name of the feature class. (mandatory) | "EVENTLOCATION" |
| Features/geometry_type | The geometry type. (mandatory) | "POINT" |
| Features/out_dataset | The name of the output dataset in which the feature class is to be stored. (optional) | "EVENT" |
| Features/* | All other parameters of "arcpy.management.CreateFeatureclass" can be used. (optional) | "True" or "False"(default)|
| Features/GlobalID | Specify whether the feature class should have a GlobalID field. | --- |
| Features/EditorTracking | Specify whether editor tracking should be activated and the corresponding fields ("CREATED_USER",  "CREATED_DATE", "LAST_EDITED_USER", "LAST_EDITED_DATE") should be added.  | "True" or "False"(default) |
| Features/EnableAttachments | Specify whether adding attachments should be activated. | "True" or "False"(default) |
| Features/**Subtypes** | A dictionary with subtypes to be created for the feature class. (optional) | --- |
| Features/Subtypes/field_name | The name of the subtype field to be created. (mandatory) → automatically creates a field of type "SHORT" → If another field type (e.g. LONG) should be used, use the field name of the corresponding field in the "Features/Fields" section (if attribute rules are implemented for subtypes, than use "LONG" instead of "SHORT"!). | --- |
| Features/Subtypes/SubtypeValues | A dictionary with "Code:Code_description" pairs. (mandatory) |  {"0":"unknown", "1": "concert", "2":"political", "3": "other"} |
| Features/Subtypes/DefaultSubtypeCode | The code of the subtype to be used as the default. (optional) |  "1" |
| Features/**Fields** | A list of fields to be added. Do not add the EditorTracking fields, GlobalId and Subtype field here! (optional) | --- |
| Features/Fields/field_name | The name of the field. (mandatory) |  "TYPE" |
| Features/Fields/field_type | The field type. (mandatory) |  "SHORT" |
| Features/Fields/field_domain | The name of the domain to be used for the field. (optional) |  "Event_Type" |
| Features/Fields/**FieldDomainSubtype** | A list of domain mappings depending on subtypes. (mandatory) |  --- |
| Features/Fields/FieldDomainSubtype/field_domain | The name of the domain to be used for the field and the specific subtype. (mandatory) |  "Event_Type" |
| Features/Fields/FieldDomainSubtype/subtype_code | If the domain is to be used only for specific subtype(s), "code:code_description" pairs separated by ";" have to be defined. (mandatory) |  "1:concert;2:political" |
| Features/Fields/* | All other parameters of "arcpy.management.AddField " can be used. (optional) | --- |
| Features/**AttributeRules** | List with attribute rules for the feature class → see arcpy.management.AddAttributeRule. (optional) | --- |
| Features/AttributeRules/name | The name of the rule. (mandatory) | "CALCULATE_AREA" |
| Features/AttributeRules/type | The type of the rule. (mandatory) | "CALCULATION" or "CONSTRAINT" or "VALIDATION" |
| Features/AttributeRules/script_expression | An Arcade script expression. (mandatory) | "return Round(Area($feature, 'square-meters'),0)" |
| Features/AttributeRules/field | The name of an existing field to which the rule is applied. (optional) | "CALCULATE_AREA" |
| Features/AttributeRules/triggering_events | Specify when the rule is triggered. (optional) | "INSERT;UPDATE" |
| Features/AttributeRules/subtype | The subtype to which the rule is to be applied. (optional) | "concert" |
| Features/AttributeRules/description | The description of the rule. (optional) | "calculate rounded area" |
| Features/AttributeRules/* | All other parameters of "arcpy.management.AddAttributeRule " can be used. (optional)  | --- |
| **Tables** | List of tables to be created → Analogous to features, but without geometry_type and out_dataset → see Esri doc arcpy.management.CreateTable. (optional)  | --- |
| **Relations** | List of relationship classes to be created → see arcpy.management.CreateRelationshipClass (optional)  | --- |
| Relations/origin_table | The name of the source table or feature class. (mandatory)  | "EVENT" |
| Relations/destination_table | The name of the destination table or feature class. (mandatory)  | "INFRASTRUCTURE" |
| Relations/out_relationship_class | The name of the relationship class to be created. (mandatory)  | "EVENT_INFRASTRUCTURE_REL" |
| Relations/relationship_type | The relationship type. (mandatory) (mandatory)  | "SIMPLE"(independent objects) or "COMPOSITE"(dependent objects parent-to-child) |
| Relations/forward_label | The name to identify the relationship when navigating from the origin table to the destination table. (mandatory)  | "Event has infrastructure elements" |
| Relations/backward_label | The name to identify the relationship when navigating from the destination table to the origin table. (mandatory) | "Infrastructure element belongs to event" |
| Relations/message_direction | The message direction. (optional) | "FORWARD"  |
| Relations/cardinality | The cardinality of the relationship. | "MANY_TO_MANY" or "ONE_TO_ONE"(default) or "ONE_TO_MANY"  |
| Relations/origin_primary_key | The primary key (field name) in the source table. (mandatory)  | "GlobalId" |
| Relations/origin_foreign_key | The field name in the destination table in case of "1:n" cardinality, or the relationship class table in case of "n:m" cardinatily, that stores the primary key of the source table. (mandatory)| "EVENT_REF" |
| Relations/destination_primary_key | The primary key in the destination table. (optional)  | "GlobalId" |
| Relations/destination_foreign_key | The field name in the relationship class table that stores the primary key of the destination table.  (optional)  | "INFRASTRUCTURE_REF" |
| Relations/**AttributedFields** | List of fields to be added to the relationship class. (optional)  | --- |
| Relations/AttributedFields/* | The same parameters as in the section "Fields". (optional)  | --- |
| Relations/**Rules** | List of rules to add to the relationship class (mainly used to define relationship for certain subtypes) → see arcpy.management.AddRuleToRelationshipClass. (optional)  | --- |
| Relations/Rules/origin_subtype | The subtype of the source table for which the rule is to apply.  | "concert" |
| Relations/Rules/destination_subtype | The subtype of the destination table for which the rule is to apply. | "stage" |
| Relations/Rules/* | All other parameters of "arcpy.management.AddRuleToRelationshipClass" can be used. (optional) | --- |
| **UpdateFeatures**| A list of existing feature classes to be updated. (optional) | --- |
| UpdateFeatures/in_table | The name of the existing table or feature class. (mandatory) | --- |
| UpdateFeatures/**AttributeRules** | If a rule affects more than one table, it cannot be created until both tables have been created → List in the JSON section "UpdateFeatures" instead of "Features". (optional) | --- |
| UpdateFeatures/AttributeRules/* | The same parameters as in the section "Features/AttributeRules". | --- |
| UpdateFeatures/**AddFields** | A list of fields to be added. | --- |
| UpdateFeatures/AddFields/* | The same parameters as in the section "Features/AddFields". | --- |
| UpdateFeatures/**CalculateFields** | A list of dictionaries with parameters of the function "arcpy.management.CalculateField" (without the parameter in_table). (optional) | --- |
| UpdateFeatures/CalculateFields/field | The field that will be updated with the new calculation. (mandatory)| "xCentroid" |
| UpdateFeatures/CalculateFields/expression | The calculation expression. (mandatory)| "!SHAPE.CENTROID.X!" |
| UpdateFeatures/CalculateFields/* | All other parameters of the function "arcpy.management.CalculateField" (optional)| {expression_type:"PYTHON3"} |
| **UpdateTables**| A list of existing tables to be updated. Analog to "UpdateFeatures" (optional) | --- |
| UpdateFeatures/DeleteFields | A list with field names to be deleted. | ["country","address" ] |
| **UpdateDomains**| A list of existing domains to be updated. (optional) | --- |
| UpdateDomains/domain_name| The name of the existing domain. (optional) | "Type_Event" |
| UpdateDomains/**AddCodedValues**| A list of codes to be added. | --- |
| UpdateDomains/AddCodedValues/code| The code to be added. | "3" |
| UpdateDomains/AddCodedValues/code_description|The code description to the code. | "organisation" |
| DeleteFeatures | A list of feature classes and tables to be deleted. (optional) | ["Feature_Class_1","Feature_Class_2"]|
| DeleteDatasets | A list of feature datasets to be deleted. (optional) | ["Dataset_1","Dataset_2"]|
| DeleteDomains | A list of domains to be deleted. (optional) | ["Domain_1","Domain_2"]|
| DeleteAllDomains | Specify if all existing domains should be deleted. (optional) | "True" or "False"|







# JSON file input parameters

- The implemented functions (e.g. "add_field()") include all parameters of the corresponding ArcGIS function (e.g. "AddField()") and possibly  additional parameters starting with "slu_". In the following table not all parameters of the arcgis functions are listed. For example, in the section "Fields" all ArcGIS parameters of the function "arcpy.management.AddField" can be specified. The table refers to the ArcGIS function in each case.
- An example JSON file is found in the "tutorial" folder.


| Parameter Name|    Description    | Example |
| --- | --- | --- |
| LogFolder | The path to the log file. (mandatory) | "C:/tutorial/Logs" |
| LogVersion | String that is used as postfix for the log file name. (mandatory) | "v01" |
| Conpath | The path to folder with the geodatabase. (mandatory) | "C:/tutorial" |
| DBName | The name of the database including the file extension. (mandatory) | "event.gdb" or "event.owner.test.sde" |
| Overwrite | The ArcGIS Environment Setting "overwrite". (mandatory) | "True" or "False" |
| DeleteAllExisting | Specify whether all existing objects in the database should be deleted beforehand. (optional) | "True" or "False"(default)|
| SpatialReferenceName | The spatial reference system name. | "CH1903+ LV95"(default) |
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
| **Domains**  | List of domains to be created → see Esri doc arcpy.management.CreateDomain. (optional) | --- |
| Domains/domain_name | The name of the domain. (mandatory)| "Type_Event" |
| Domains/domain_description | The description of the domain. (optional)| "Type_Event" |
| Domains/field_type | The type of attribute domain to be created. (mandatory) | "SHORT" |
| Domains/domain_type | The type of the domain. |  "CODED"(default) or "RANGE" |
| Domains/* | All other parameters of "arcpy.management.CreateDomain" can be used. (optional) | --- |
| Domains/DomainValues | A dictionary with "code:code_description" pairs. (mandatory if domain_type = "CODED")| {"0":"unknown", "1":"public", "2":"private"} |
| Domains/DomainRange | A dictionary with min and max values. (mandatory if domain_type = "RANGE"| {"min_value":"0", "max_value":"100"} |
|  **Datasets**  | List of datasets to be created → see Esri documentation arcpy.management.CreateFeatureDataset. (optional) | --- |
| Datasets/out_name | The name of the dataset to be created. (mandatory)| "EVENT" |
| **Features** | List of feature classes to be created → see Esri doc arcpy.management.CreateFeatureclass. (optional)  | --- |
| Features/out_name | The name of the feature class. (mandatory) | "EVENTLOCATION" |
| Features/geometry_type | The geometry type. (mandatory) | "POINT" |
| Features/out_dataset | The name of the output data set in which the feature class is to be stored. (optional) | "EVENT" |
| Features/* | All other parameters of "arcpy.management.CreateFeatureclass" can be used. (optional) | "True" or "False"(default)|
| Features/GlobalID | Specify whether the feature class shuold have a GlobalID field. | --- |
| Features/EditorTracking | Specify wheter editor tracking should be activated and the corresponding fields ("CREATED_USER",  "CREATED_DATE", "LAST_EDITED_USER", "LAST_EDITED_DATE") added.  | "True" or "False"(default) |
| Features/EnableAttachments | Specify wheter adding attachments should be activated. | "True" or "False"(default) |
| Features/**Subtypes** | A dictonary with subtypes to be created for the feature class. (optional) | --- |
| Features/Subtypes/field_name | The name of the subtype field to be created. (mandatory) → automatically creates a field of type "SHORT" → If another field type (e.g. LONG) should be used, use the field name of the corresponding field in the "Features/Fields" section (if attribute rules are implemented for subtypes, than use "LONG" instead of "SHORT"!). | --- |
| Features/Subtypes/SubtypeValues | Dictionary with "Code:Code_description" pairs. (mandatory) |  {"0":"unknown", "1": "concert", "2":"political", "3": "other"} |
| Features/Subtypes/DefaultSubtypeCode | Code of the subtype to be used as the default. (optional) |  "1" |
| Features/**Fields** | List of fields to be added. Do not add the EditorTracking fields, GlobalId, Subtype field here! (optional) | --- |
| Features/Fields/field_name | The name of the field. (mandatory) |  "TYPE" |
| Features/Fields/field_type | The field type. (mandatory) |  "SHORT" |
| Features/Fields/field_domain | The name of the domain to be used for the field (optional) |  "Event_Type" |
| Features/Fields/**FieldDomainSubtype** | The name of the field. (mandatory) |  --- |
| Features/Fields/FieldDomainSubtype/field_domain | The name of the domain to be used for the field and subtype. (mandatory) |  "Event_Type" |
| Features/Fields/FieldDomainSubtype/subtype_code | If the domain is to be used only for specific subtype(s) "code:code_description" pairs seperated by ";" have to be defined. (mandatory) |  "1:concert;2:political" |
| Features/Fields/* | All other parameters of "arcpy.management.AddField " can be used. (optional) | --- |
| Features/**AttributeRules** | List with attribute rules for the feature class → see arcpy.management.AddAttributeRule. (optional) | --- |



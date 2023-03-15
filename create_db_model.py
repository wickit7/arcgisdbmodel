# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name: create_db_model
#
# Purpose: Script to create and update an ArcGIS data model based on a JSON input file. 
# The implemented functions (e.g. "add_field()") include all parameters of the corresponding 
# ArcGIS functions (e.g. "AddField()") and possibly  additional parameters starting with "slu_". 
# The implemented functions follow the naming convention "lowercase_underscore" in contrast to 
# ArcGIS functions which have the naming convention "CapitalizedWord".
#
# Author: Timo Wicki, City of Lucerne
#
# Created: 02.01.2023
# -----------------------------------------------------------------------------
import sys, os, logging, json, time
import arcpy

def init_logging(file)  -> None:
    """Initialises logging to a file and on the console.

    Required:
        file -- The path to the log file.
    """
    global logger
    logger = logging.getLogger('myapp')
    # logging to file
    hdlr = logging.FileHandler(file, mode='w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    # logging to console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    logger.setLevel(logging.INFO)

def search(file, text) -> int:
    """Search for a specific string in a file.

    Required:
        file -- The path to the file (e.g. log file).
        text -- The string which is to be searched for.

    Return:
        cnt -- The number of occurrences of the string in the file.
    """
    cnt = 0
    with open(file) as f:
        for line in f:
            if text in line.lower():
                cnt=cnt+1
        return cnt


def field_exists(in_table, field_name) -> bool:
    """Checks whether the field exists.

    Required:
        in_table -- The Name of the table or the feature-class.
        field_name -- The Name of the field.
    """
    field_names = [field.name for field in arcpy.ListFields(in_table)]
    if field_name in field_names:
        return True
    else:
        return False

def contains_umlaut(name: str) -> bool:
    """Checks if a string contains a umlaut (ö, ä, ü).

    Required:
        name -- A string.

    Return:
        True: If there is a umlaut in the string.
        False: If there is no umlaut in the string.
    """
    umlauts = ['ü', 'ä', 'ö']
    for char in name:
        if char.lower() in umlauts:
           return True

    return False

def filter_dict(dic, dic_type = None) -> dict:
    """Filters a dictionary so that it contains only relevant data.

    Required:
        dic -- The dictionary that is to be filtered.

    Optional:
        dic_type -- "None": Removes all dictionary keys which have the value "" or None.
                    "feature": Filters the dictionary additionally so that it can be used for the function create_feature_class.
                    "table": Filters the dictionary additionally so it can be used for the function create_table.

    Return:
        dic_filtered -- The filtered dictionary.
    """
    dic = {k: v for k, v in dic.items() if v is not None and len(str(v))>0}
    dic_filtered = dic.copy()

    if dic_type == "feature":
        parameters_create_feature = ["out_path", "out_name", "geometry_type", "template",
                                     "has_m", "has_z", "spatial_reference", "config_keyword", "spatial_grid_1",
                                     "spatial_grid_2", "spatial_grid_3", "out_alias", "out_dataset"]
        for parameter in dic:
            if parameter not in parameters_create_feature:
                dic_filtered.pop(parameter)

    elif dic_type == "table":
        parameters_create_table = ["out_path", "out_name", "template","config_keyword"]
        for parameter in dic:
            if parameter not in parameters_create_table:
                dic_filtered.pop(parameter)

    return dic_filtered

def get_spatial_reference(spatial_reference, vcs = None):
    """Returns the spatial reference system if it is valid.

    Required:
        spatial_reference -- The name of the coordinate system (e.g. "CH1903+ LV95").
    Optional:
        vcs -- The name of the vertical coordinate system.

    Raises:
        ValueError: If the given spatial_reference is invalid.

    Return:
        sr: The ArcGIS spatial reference.
    """
    try:
        if vcs:
            sr = arcpy.SpatialReference(spatial_reference, vcs)
        else:
            sr = arcpy.SpatialReference(spatial_reference)
        return sr

    except Exception:
        e = sys.exc_info()[1]
        raise ValueError(f'spatial_reference "{spatial_reference}" is invalid: {e.args[0]}')

def delete_all(in_workspace)-> None:
    """Delete all existing features, tables, datasets and domains.

    Required:
        in_workspace -- The path to the workspace (gdb, sde connection file).
    """
    #arcpy.env.workspace = in_workspace
    #arcpy.env.overwriteOutput = True
    
    fc_list = arcpy.ListFeatureClasses()
    tables = arcpy.ListTables()
    ds_list = arcpy.ListDatasets()
    all_domains = arcpy.da.ListDomains(in_workspace)

    # delete feature classes
    for fc in fc_list:
        try:
            logger.info(f'The feature class "{fc}" will be deleted')
            arcpy.management.Delete(fc)
        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'The existing feature class "{fc}" could not '
                         f'be deletd: {e.args[0]}')

    # delete tables
    for table in tables:
        try:
            logger.info(f'The table "{table}" will be deleted')
            arcpy.management.Delete(table)
        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'The existing table "{table}" could not '
                         f'be deleted: {e.args[0]}')

    # delete datasets
    for ds in ds_list:
        try:
            logger.info(f'The datasets "{ds}" will be deleted')
            arcpy.management.Delete(ds)
        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'The existing dataset "{ds}" could not '
                         f'be deleted: {e.args[0]}')

    # delete domain
    for domain in all_domains:
        try:
            logger.info(f'The domain "{domain.name}" will be deleted')
            arcpy.management.DeleteDomain(in_workspace, domain.name)
        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'The existing domain "{domain.name}" could not '
                         f'be deleted: {e.args[0]}')

def delete_all_domain(in_workspace)-> None:
    """Delete all existing domains.

    Required:
        in_workspace -- The path to workspace (gdb, sde connection file).
    """
    all_domains = arcpy.da.ListDomains(in_workspace)

    # delete domain
    for domain in all_domains:
        try:
            logger.info(f'The domain "{domain.name}" will be deleted')
            remove_domain_from_fields(domain.name)
            arcpy.management.DeleteDomain(in_workspace, domain.name)
        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'The existing domain "{domain.name}" could not '
                         f'be deleted: {e.args[0]}')

def delete_domain(in_workspace, domain_name):
    """Delete a domain (see Esri arcpy.management.DeleteDomain).

    Required:
    in_workspace -- The path to workspace (gdb, sde connection file).
    domain_name -- The name of the domain.
    """   
    # delete domain
    try:
        logger.info(f'The domain "{domain_name}" will be deleted')
        remove_domain_from_fields(domain_name)
        arcpy.management.DeleteDomain(in_workspace, domain_name)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The existing domain "{domain_name}" could not '
                    f'be deleted: {e.args[0]}')

def delete_item(in_data, data_type=None)-> None:
    """Delete item, tables, datasets (see Esri arcpy.management.Delete).

    Required:
        in_data -- The input data to be deleted.

    Optional:
        data_type -- The type of data to be deleted (e.g. "FeatureClass" oder "FeatureDataset").

    """
    # delete item
    try:
        logger.info(f'Item "{in_data}" will be deleted')
        arcpy.management.Delete(in_data, data_type)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The existing Item "{in_data}" could not be '
                     f'deleted: {e.args[0]}')

def create_domain(in_workspace, domain_name, domain_description = None, field_type = "SHORT",
                  domain_type = "CODED", **kwargs)-> None:
    """Create a domain (see Esri arcpy.management.CreateDomain).

    Required:
        in_workspace -- The path to the workspace( gdb, sde connection file).
        domain_name -- The name of the domain.

    Optional:
        domain_description -- The description of the domain.
        field_type -- Specifies the type of attribute domain that will be created.
        domain_type -- Specifies the domain type that will be created.
        **kwargs -- Additional parameters for the function arcpy.management.CreateDomain.
    """

    # check naming convention
    if contains_umlaut(domain_name):
        logger.warning(f'"{domain_name}" contains an Umlaut!')
    # if not domain_name.isupper():
    #     logger.warning(f'"{domain_name}" is not in capital letters!')

    # check if the domain already exists
    all_domains = arcpy.da.ListDomains(in_workspace)
    all_domain_names = []
    for domain in all_domains:
        all_domain_names.append(domain.name)
    if domain_name in all_domain_names:
        try:
            logger.info(f'The existing domain "{domain_name}" will be deleted')
            remove_domain_from_fields(domain_name)
            arcpy.management.DeleteDomain(in_workspace, domain_name)
        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'The existing domain "{domain_name}" could not '
                         f'be deleted: {e.args[0]}')
            return

    # create domain
    try:
        logger.info(f'The domain "{domain_name}" will be created')
        arcpy.management.CreateDomain(in_workspace, domain_name, domain_description,
                                      field_type, domain_type, **kwargs)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The domain "{domain_name}" could not be created: {e.args[0]}')
        return

def add_coded_value_to_domain(in_workspace, domain_name, slu_domain_dict = None, **kwargs)-> None:
    """Add coded value to domain (see Esri arcpy.management.AddCodedValueToDomain).
    In contrast to the ESRI function, a dictionary with the codes as keys and the code_descriptions as values
    can be used as input parameter, which allows to add several values to the domain at the same time.

    Required:
        in_workspace -- The path to the workspace (gdb, sde connection file).
        domain_name -- The name of the domain.

    Optional:
        slu_domain_dict -- Dictionary with the codes as the keys and the descriptions as the values.
        **kwargs -- Additional parameters for the function arcpy.management.AddCodedValueToDomain.
                    Instead of a dictionary, the parameter "code" and "code_description" can 
                    be used as input.
    """
    if slu_domain_dict:
        # adding codes and values contained in the dictionary
        try:
            logger.info(f'Coded values are added to the domain "{domain_name}"')
            for code in slu_domain_dict:
                arcpy.management.AddCodedValueToDomain(in_workspace, domain_name,
                                                       code, slu_domain_dict[code])
        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'No values could be added to the domain "{domain_name}": {e.args[0]}')
            return
    else:
        # adding code and code_description
        try:
            logger.info(f'Coded value is added to the domain "{domain_name}"')
            arcpy.management.AddCodedValueToDomain(in_workspace, domain_name, **kwargs)

        except Exception:
            e = sys.exc_info()[1]
            logger.error(f'No values could be added to the domain "{domain_name}": {e.args[0]}')
            return

def set_value_for_range_domain(in_workspace, domain_name, min_value, max_value)-> None:
    """Add values to a domain of the type Range (see Esri arcpy.management.SetValueForRangeDomain).

    Required:
        in_workspace -- The path to the workspace (gdb, sde connection file).
        domain_name -- The name of the domain.
        min_value -- The minimum value of the range domain.
        max_value -- The maximum value of the range domain.
    """
    # add values
    try:
        logger.info(f'Adding values to the domain "{domain_name}"')
        arcpy.management.SetValueForRangeDomain(in_workspace, domain_name, min_value, max_value)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'No values could be added to the domain "{domain_name}": {e.args[0]}')
        return

def remove_domain_from_fields(domain_name):
    """Removes domain assignment from all fields that use the domain (see Esri arcpy.management.RemoveDomainFromField).

    Required:
        domain_name -- The name of the domain
    """
    datasets = arcpy.ListDatasets(feature_type = "Feature")
    datasets = [''] + datasets if datasets is not None else []
    for ds in datasets:
        for fc in arcpy.ListFeatureClasses(feature_dataset = ds):
            for field in arcpy.ListFields(fc):
                if field.domain and field.domain == domain_name:
                    try:
                        logger.info(f'Removing domain "{domain_name}" from the field "{field.name}" '
                                    f'in the feature class "{fc}"')
                        arcpy.management.RemoveDomainFromField(fc, field.name)

                    except Exception:
                        e = sys.exc_info()[1]
                        logger.error(f'Domain "{domain_name}" could not be removed from the field "{field.name}" '
                                     f'in the feature class "{fc}" : {e.args[0]}')

        if not ds:
            for tb in arcpy.ListTables():
                for field in arcpy.ListFields(tb):
                    if field.domain and field.domain == domain_name:
                        try:
                            logger.info(f'Removing domain "{domain_name}" from the "{field.name}" '
                                        f'in the table "{tb}"')
                            arcpy.management.RemoveDomainFromField(tb, field.name)

                        except Exception:
                            e = sys.exc_info()[1]
                            logger.error(f'Domain "{domain_name}" could not be removed from the field "{field.name}" '
                                         f'in the table "{tb}": {e.args[0]}')

def create_feature_dataset(out_dataset_path, out_name, spatial_reference = 'CH1903+ LV95',
                        slu_overwrite = True)-> None:
    """Create a feature dataset (see Esri arcpy.management.CreateFeatureDataset).

    Required:
        out_dataset_path -- The path to the workspace (gdb, sde connection file).
        out_name -- The name of the dataset.
    Optional:
        spatial_reference -- The name of the spatial reference system.
        slu_overwrite -- If an existing dataset is to be overwritten (True or False).
    """
    # check naming convention
    if contains_umlaut(out_name):
        logger.warning(f'"The dataset {out_name}" contains an Umlaut!')
    # if not out_name.isupper():
    #     logger.warning(f'"The dataset {out_name}" is not in capital letters!')

    # check if the dataset already exists (not working!?)
    out_dataset = os.path.join(out_dataset_path, out_name)
    if arcpy.Exists(out_dataset):
        if slu_overwrite:
            logger.info(f'Existing dataset "{out_name}" will be deleted')
            arcpy.management.Delete(out_dataset)
        else:
            logger.warning(f'Existing dataset "{out_name}" will not be deleted')
            return

    # create a dataset
    try:
        logger.info(f'The dataset "{out_name}" will be created')
        arcpy.management.CreateFeatureDataset(out_dataset_path, out_name, spatial_reference)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The dataset "{out_name}" could not be created: {e.args[0]}')

def create_feature_class(out_path, out_name, geometry_type, spatial_reference = 'CH1903+ LV95',
                         out_dataset = None, slu_overwrite = True, **kwargs) -> None:
    """Create a feature class (see documentation of Esri).

    Required:
        out_path -- The path to the workspace (gdb, sde connection file).
        out_name -- The name of the output feature class.
        geometry_type -- The geometry type.

    Optional:
        spatial_reference -- The name of the spatial reference system.
        out_dataset -- The name of the dataset in which the feature class will be created.
        slu_overwrite -- If an existing feature class is to be overwritten (True or False).
        **kwargs -- Additional parameters for the function arcpy.management.CreateFeatureclass (e.g. "has_z").
    """
    # check naming convention
    if contains_umlaut(out_name):
        logger.warning(f'The feature class name "{out_name}" contains an Umlaut!')
    # if not out_name.isupper():
    #     logger.warning(f'The feature class name "{out_name}" is not in capital letters!')

    # check if feature class is to be created in a dataset
    if out_dataset:
        out_path = os.path.join(out_path, out_dataset)
    else:
        out_path = out_path

    # check if the feature class already exists
    out_feature = os.path.join(out_path, out_name)
    if arcpy.Exists(out_feature):
        if slu_overwrite:
            logger.info(f'Existing feature class "{out_name}" will be deleted')
            arcpy.management.Delete(out_feature)
        else:
            logger.warning(f'Existing feature class "{out_name}" will not be overwritten')
            return

    # create feature class
    try:
        logger.info(f'The feature class "{out_name}" will be created')
        arcpy.management.CreateFeatureclass(
            out_path = out_path, out_name = out_name, geometry_type = geometry_type,
            spatial_reference = spatial_reference, **kwargs
            )

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The feature class "{out_name}" could not be created: {e.args[0]}')

def create_table(out_path, out_name, slu_overwrite = True, **kwargs) -> None:
    """create a table (see documentation of Esri).

    Required:
        out_path -- The path to the workspace (gdb, sde connection file).
        out_name -- The name of the output table.

    Optional:
        slu_overwrite -- If an existing table is to be overwritten (True or False).
        **kwargs -- Additional parameters for the function arcpy.management.CreateTable.
    """

    # check naming convention
    if contains_umlaut(out_name):
        logger.warning(f'The table name "{out_name}" contains an Umlaut!')
    # if not out_name.isupper():
    #     logger.warning(f'The table name "{out_name}" is not in capital letters!')

    # check if the table already exists (not working!?)
    out_table = os.path.join(out_path, out_name)
    if arcpy.Exists(out_table):
        if slu_overwrite:
            logger.info(f'The existing table "{out_name}" will be deleted')
            arcpy.management.Delete(out_table)
        else:
            logger.warning(f'The existing table "{out_table}" will not be overwritten')
            return

    # crate table
    try:
        logger.info(f'The table "{out_name}" will be created')
        arcpy.management.CreateTable(out_path = out_path, out_name = out_name, **kwargs)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The table "{out_name}" could not be created: {e.args[0]}')

def add_field(in_table, field_name, field_type, **kwargs):
    """Adding a field to a table or a feature class (see documentation of Esri)

    Required:
        in_table -- The name of the table or the feature class.
        field_name -- The name of the field.
        field_type -- The type of the field.

    Optional:
        field_domain -- The name of the domain to be assigned to the field.
        **kwargs -- Additonal parameters for the function arcpy.management.AddField.
    """
    # check naming convention
    if contains_umlaut(field_name):
        logger.warning(f'The field name "{field_name}" contains an Umlaut!')
    # if not field_name.isupper():
    #     logger.warning(f'The field name "{field_name}" is not in capital letters!')
    # Add field
    try:
        logger.info(f'Adding the field "{field_name}"')
        arcpy.management.AddField(in_table = in_table, field_name = field_name,
                                field_type = field_type, **kwargs)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'Error when creating the field "{field_name}": {e.args[0]}')

def delete_field(in_table, field_name):
    """Deleting a field from a table or a feature class (see documentation of Esri).

    Required:
        in_table -- The name of the table or the feature class.
        field_name -- The name of the field to be deleted.
    """

    try:
        logger.info(f'Feld "{field_name}" will be deleted')
        arcpy.management.DeleteField(in_table, field_name)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'Error when deleting the field "{field_name}": {e.args[0]}')

def calculate_field(in_table, field, expression, **kwargs):
    """ Calculates the values of a field for a feature class, feature layer, 
    or raster (see documentation of Esri).

    Required:
        in_table -- The name of the table or feature class.
        field -- The name of the field.
        expression -- The simple calculation expression used to create a value that will populate the selected rows.

    Optional:
        **kwargs -- Additional parameters for the function arcpy.management.CalculateField.
    """
    # Get a list of fields in the feature class or table
    if not field_exists(in_table, field):
        logger.warning(f'The field "{field}" does not exist and will be created.')

    try:
        logger.info(f'Calculate field "{field}"')
        arcpy.management.CalculateField(in_table = in_table, field = field, 
                                        expression = expression, **kwargs)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'Error when calculating the field "{field}": {e.args[0]}')

def assign_domain_to_field(in_table, field_name, domain_name, subtype_code = None):
    """Assign a domain to a field (see documentation of Esri).

    Required:
        in_table -- The name of the table or the feature class.
        field_name -- The name of the field.
        field_domain -- The name of the domain.

    Optional:
        subtype_code -- Subtypes for which the domain applies e.g. "1: Event;2: Boulevard".
    """
    # assign domain
    try:
        if subtype_code:
            logger.info(f'The domain "{domain_name}" will be assigned to the field "{field_name}" '
                        f'for the subtype "{subtype_code}"')
            arcpy.management.AssignDomainToField(in_table, field_name, domain_name, subtype_code)
        else:
            logger.info(f'The domain "{domain_name}" will be assigned to the field "{field_name}"')
            arcpy.management.AssignDomainToField(in_table, field_name, domain_name)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The domain"{domain_name}" could not be assigned to the field "{field_name}": '
                     f'{e.args[0]}')

def create_subtype_field(in_table, field_name):
    """Create a subtype field. In contrast to the function arcpy.management.SetSubtypeField,
    the field is newly created, if it does not exist already.

    Required:
        in_table -- The name of the table or feature class.
        field_name -- The field name of the subtype field to be created.
    """
    # add a field of type "SHORT" 
    if not field_exists(in_table, field_name):
        add_field(in_table, field_name, "SHORT")

    # create subtype field
    try:
        logger.info(f'The field "{field_name}" will be defined as subtype field')
        arcpy.management.SetSubtypeField(in_table = in_table, field = field_name)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The field "{field_name}" could not be defined as subtype field: '
                     f'{e.args[0]}')

def add_subtype(in_table, subtype_code, subtype_description):
    """Adding a subtype to a feature class or a table (see documentation of Esri).

    Required:
        in_table -- The name of the table or feature class.
        subtype_code -- Unique integer value.
        subtype_description -- The subtype description.
    """
    # create subtype
    try:
        logger.info(f'The subtype "{subtype_code}":"{subtype_description}" will be created')
        arcpy.management.AddSubtype(in_table = in_table, subtype_code = subtype_code,
                                    subtype_description = subtype_description)
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The subtype "{subtype_code}":"{subtype_description}" could not be created: '
                     f'{e.args[0]}')

def add_global_id(in_dataset):
    """Adding a GlobalId to a feature class or table (see documentation of Esri)

    Required:
        in_dataset -- The name of the table or feature class
    """
    try:
        logger.info(f'Adding GlobalID to "{in_dataset}"')
        arcpy.management.AddGlobalIDs(in_dataset)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'GlobalID could not be added to "{in_dataset}": '
                     f'{e.args[0]}')

def set_default_subtype(in_table, subtype_code):
    """Set a subtype as default (see documentation of Esri).

    Required:
        in_table -- The name of the table or feature class.
        subtype_code -- The subtype code to be used as a default (e.g. "1").
    """
    try:
        logger.info(f'Set subtype "{subtype_code}" in "{in_table}" as default')
        arcpy.management.SetDefaultSubtype(in_table, subtype_code)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The subtpye "{subtype_code}" could not be set as default in the table "{in_table}": '
                     f'{e.args[0]}')

def enable_editor_tracking(in_dataset, creator_field = "CREATED_USER", creation_date_field = "CREATED_DATE",
                          last_editor_field = "LAST_EDITED_USER", last_edit_date_field = "LAST_EDITED_DATE",
                          add_fields = "NO_ADD_FIELDS", record_dates_in = "UTC"):
    """Activating editor tracking (see documentation of Esri).

    Required:
        in_dataset -- The name of the table or feature class.

    Optional:
        Additional parameters for the function arcpy.management.EnableEditorTracking.
    """
    try:
        logger.info(f'Activate editor tracking in "{in_dataset}"')
        arcpy.management.EnableEditorTracking(
                            in_dataset, creator_field, creation_date_field, last_editor_field,
                            last_edit_date_field, add_fields, record_dates_in
                            )
    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'Editor tracking could not be activated in "{in_dataset}": '
                     f'{e.args[0]}')

def enable_attachments(in_dataset):
    """Activate attachments (see documentation of Esri).

    Required:
        in_dataset -- The name of the table or feature class.
    """
    try:
        logger.info(f'Activate attachments in "{in_dataset}"')
        arcpy.management.EnableAttachments(in_dataset)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'Attachments could not be activated in "{in_dataset}": '
                     f'{e.args[0]}')

def add_attribute_rule(in_table, name, type, script_expression, **kwargs):
    """Adding attribute rule (see documentation of Esri).

    Required:
        in_table -- The name of the table or feature class.
        name -- The name of the rule.
        type -- The type of the rule.
        script_expression -- The arcade expression to define the rule.

    Optional:
        **kwargs -- Additional parameters for the function arcpy.management.AddAttributeRule
    """
    try:
        logger.info(f'Adding attribute rule "{name}" to "{in_table}"')
        arcpy.management.AddAttributeRule(in_table, name, type, script_expression, **kwargs)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'Attribute rule "{name}" could not be added to "{in_table}": '
                     f'{e.args[0]}')

def create_relationship_class(origin_table, destination_table, out_relationship_class,
                              slu_overwrite = True, **kwargs) -> None:
    """Create a realationship class (see documentation of Esri)

    Required:
        origin_table -- The table or feature class that is assigned to the target table.
        destination_table -- The table that is assigned to the source table.
        out_relationship_class -- The output relationship class.

    Optional:
        slu_overwrite -- If an existing table is to be overwritten (True or False).
        **kwargs -- Additional parameters of the function arcpy.management.CreateRelationshipClass
    """
    # check naming convention
    if contains_umlaut(out_relationship_class):
        logger.warning(f'The name of the relationship class "{out_relationship_class}" contains an Umlaut!')
    #if not out_relationship_class.isupper():
    #    logger.warning(f'The name of the relationship class "{out_relationship_class}" is in capital letters!')

    # check if the relationship class already exists (not working!?)
    if arcpy.Exists(out_relationship_class):
        if slu_overwrite:
            logger.info(f'Existing relationship class "{out_relationship_class}" will be deleted')
            arcpy.management.Delete(out_relationship_class)
        else:
            logger.warning(f'Existing relationship class "{out_relationship_class}" will not be overwritten')
            return

    # Feature erstellen
    try:
        logger.info(f'The relationship class "{out_relationship_class}" will be created')
        arcpy.management.CreateRelationshipClass(origin_table = origin_table, destination_table = destination_table,
                                                 out_relationship_class = out_relationship_class, **kwargs)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The realtionship class "{out_relationship_class}" could not be created: {e.args[0]}')

def add_rule_to_relationship_class(in_rel_class, **kwargs):
    """Add a rule to a realtionship class (see Esri arcpy.management.AddRuleToRelationshipClass)
    For example, it is possible to add a rule to specify that the relationship is only set for a certain subtype.

    Required:
        in_rel_class -- The name of the relationship class.

    Optional:
        **kwargs -- Additional parameters for the function arcpy.management.AddAttributeRule.
    """
    try:
        logger.info(f'Adding a rule to the relationship class "{in_rel_class}"')
        arcpy.management.AddRuleToRelationshipClass(in_rel_class, **kwargs)

    except Exception:
        e = sys.exc_info()[1]
        logger.error(f'The rule could not be added to the relationship class "{in_rel_class}": '
                     f'{e.args[0]}')

# Main module: Check input parameters and call functions
def main(conpath, db_name, overwrite, spatial_reference_name, environment_settings,
         delete_existing, domains, datasets, features, tables, relations, update_features, update_domains, 
         delete_features, delete_datasets, delete_domains, delete_all_domains, stage) -> None:
    """Check input parameters and call functions

    """
    # define the path to the workspace (sde connection file oder gdb)
    if stage:
        if "." in db_name:
            # Assumption: db_name has the file ending included
            db_fullname = db_name
        else:
            # Assumption: db_name ends as following, depending on the server stage (default at city of Lucerne)
            if stage == 'TEST':
                    db_fullname = db_name + '.owner.test.sde'
            elif stage == 'INTE':
                    db_fullname = db_name + '.owner.inte.sde'
            elif stage == 'PROD':
                    db_fullname = db_name + '.owner.prod.sde'
            else:
                # Assumption: Esri file geodatabse (.gdb)
                db_fullname = db_name + '.gdb'
    else:
        db_fullname = db_name
    workspace = os.path.join(conpath, db_fullname)

    # check if path exists
    # Assumption: if it does not end with ".gdb" it's a file and not a folder
    if ".gdb" in db_fullname:
        if not os.path.isdir(workspace):
            logger.error(f'workspace "{workspace}" does not exist!')
            raise ValueError(f'Workspace "{workspace}" does not exist!')
    else:
        if not os.path.isfile(workspace):
            logger.error(f'Workspace "{workspace}" does not exist!')
            raise ValueError(f'Workspace "{workspace}" does not exist!')

    # set workspace
    arcpy.env.workspace = workspace

    # check spatial reference system
    spatial_reference = get_spatial_reference(spatial_reference_name)

    # set env setting overwrite
    if overwrite == 'True':
        overwrite = True
        arcpy.env.overwriteOutput = True
    else:
        overwrite = False
        arcpy.env.overwriteOutput = False

    # set additional env settings 
    if environment_settings:
        logger.info("Adjust default environment settings")
        if 'xy_tolerance' in environment_settings:
            arcpy.env.XYTolerance = environment_settings['xy_tolerance']
        if 'xy_resolution' in environment_settings:
            arcpy.env.XYResolution = environment_settings['xy_resolution']
        if 'xy_domain' in environment_settings:
            arcpy.env.XYDomain = environment_settings['xy_domain']
        if 'output_z_flag' in environment_settings:
            arcpy.env.outputZFlag = environment_settings['output_z_flag']       
        if 'z_tolerance' in environment_settings:
            arcpy.env.ZTolerance = environment_settings['z_tolerance']
        if 'z_resolution' in environment_settings:
            arcpy.env.ZResolution = environment_settings['z_resolution']
        if 'z_domain' in environment_settings:
            arcpy.env.ZDomain = environment_settings['z_domain']
        if 'output_z_value' in environment_settings:
            arcpy.env.outputZValue = environment_settings['output_z_value']  
        if 'output_m_flag' in environment_settings:
            arcpy.env.outputMFlag = environment_settings['output_m_flag']
        if 'm_tolerance' in environment_settings:
            arcpy.env.MTolerance = environment_settings['m_tolerance']
        if 'm_resolution' in environment_settings:
            arcpy.env.MResolution = environment_settings['m_resolution']
        if 'm_domain' in environment_settings:
            arcpy.env.MDomain = environment_settings['m_domain'] 

    # remove existing feature datasets, feature classes, tables and domains
    if delete_existing == 'True':
        logger.info("Delete all existing data")
        delete_all(workspace)

    # create domains
    if domains:
        for dic in domains:
            # filter dictionary (if "" oder None)
            dic_filtered = filter_dict(dic)
            # call functions with correct parameters
            if dic_filtered['domain_type'] == "CODED":
                # extract DomainValues from dictionary
                domain_values = dic_filtered.pop('DomainValues')
                # create domain
                create_domain(workspace, **dic_filtered)
                # adding domain values
                add_coded_value_to_domain(workspace, dic_filtered['domain_name'], domain_values)
            elif dic_filtered['domain_type'] == "RANGE":
                domain_range = dic_filtered.pop('DomainRange')
                # creating domain
                create_domain(workspace, **dic_filtered)
                # adding domain values
                set_value_for_range_domain(workspace, dic_filtered['domain_name'],
                                           domain_range["min_value"], domain_range["max_value"])

    # creating dataset
    if datasets:
        for dic in datasets:
            # filter dictionary
            dic_filtered = filter_dict(dic)
            # adding additional parameters
            dic_filtered['spatial_reference'] = spatial_reference
            dic_filtered['slu_overwrite'] = overwrite
            # creating dataset
            create_feature_dataset(workspace, **dic_filtered)

    # creating feature classes
    if features:
        for dic in features:
            # filter dictionary
            dic_filtered = filter_dict(dic)
            # filter dictionary for create_feature_class
            dic_create_feature = filter_dict(dic_filtered, "feature")
            # adding additional parameters
            dic_create_feature['spatial_reference'] = spatial_reference
            dic_create_feature['slu_overwrite'] = overwrite
            # creating feature class
            create_feature_class(workspace, **dic_create_feature)
            # add GlobalIDs
            if 'GlobalID' in dic_filtered and dic_filtered['GlobalID'] == 'True':
                add_global_id(dic_filtered['out_name'])
            # add subtypes
            if 'Subtypes' in dic_filtered:
                dic_subtype = dic_filtered['Subtypes']
                create_subtype_field(dic_filtered['out_name'], dic_subtype['field_name'])
                for code in dic_subtype['SubtypeValues']:
                    add_subtype(dic_filtered['out_name'], code, dic_subtype['SubtypeValues'][code])
                if 'DefaultSubtypeCode' in dic_subtype:
                    set_default_subtype(dic_filtered['out_name'], dic_subtype['DefaultSubtypeCode'])
            # add fields
            if 'Fields' in dic_filtered:
                for dic_field in dic_filtered['Fields']:
                    field_domain_subtypes = None
                    if "FieldDomainSubtype" in dic_field:
                        field_domain_subtypes = dic_field.pop('FieldDomainSubtype')
                    # add Fields
                    add_field(dic_filtered['out_name'], **dic_field)
                    # add domains to subtypes
                    if field_domain_subtypes:
                        for dic_domain in field_domain_subtypes:
                            assign_domain_to_field(dic_filtered['out_name'], dic_field['field_name'],
                                                   dic_domain['field_domain'], dic_domain['subtype_code'])
            # add editor tracking including editor tracking fields
            if 'EditorTracking' in dic_filtered and dic_filtered['EditorTracking'] == 'True':
                enable_editor_tracking(in_dataset = dic_filtered['out_name'], add_fields = "ADD_FIELDS")
            # enable attachments
            if 'EnableAttachments' in dic_filtered and dic_filtered['EnableAttachments'] == 'True':
                enable_attachments(dic_filtered['out_name'])
            # add attribute rules
            if 'AttributeRules' in dic_filtered:
                for dic_rule in dic_filtered['AttributeRules']:
                    add_attribute_rule(dic_filtered['out_name'], **dic_rule)

    # creating table
    if tables:
        for dic in tables:
            # filter dictionary
            dic_filtered = filter_dict(dic)
            # filter dictionary for create_table
            dic_create_table = filter_dict(dic_filtered, "table")
            # create table
            create_table(workspace, **dic_create_table)
            # add GlobalIDs
            if 'GlobalID' in dic_filtered and dic_filtered['GlobalID'] == 'True':
                add_global_id(dic_filtered['out_name'])
            # add subtypes
            if 'Subtypes' in dic_filtered:
                dic_subtype = dic_filtered['Subtypes']
                create_subtype_field(dic_filtered['out_name'], dic_subtype['field_name'])
                for code in dic_subtype['SubtypeValues']:
                    add_subtype(dic_filtered['out_name'], code, dic_subtype['SubtypeValues'][code])
                if 'DefaultSubtypeCode' in dic_subtype:
                    set_default_subtype(dic_filtered['out_name'], dic_subtype['DefaultSubtypeCode'])
            # add fields
            if 'Fields' in dic_filtered:
                for dic_field in dic_filtered['Fields']:
                    field_domain_subtypes = None
                    if "FieldDomainSubtype" in dic_field:
                        field_domain_subtypes = dic_field.pop('FieldDomainSubtype')
                    # add fields
                    add_field(dic_filtered['out_name'], **dic_field)
                    # add domains to subtypes
                    if field_domain_subtypes:
                        for dic_domain in field_domain_subtypes:
                            assign_domain_to_field(dic_filtered['out_name'], dic_field['field_name'],
                                                   dic_domain['field_domain'], dic_domain['subtype_code'])
            # add editor tracking including editor tracking Felder
            if 'EditorTracking' in dic_filtered and dic_filtered['EditorTracking'] == 'True':
                enable_editor_tracking(in_dataset = dic_filtered['out_name'], add_fields = "ADD_FIELDS")
            # enable attachments
            if 'EnableAttachments' in dic_filtered and dic_filtered['EnableAttachments'] == 'True':
                enable_attachments(dic_filtered['out_name'])
            # add attribute rules
            if 'AttributeRules' in dic_filtered:
                for dic_rule in dic_filtered['AttributeRules']:
                    add_attribute_rule(dic_filtered['out_name'], **dic_rule)

    # creating realationship class
    if relations:
        for dic in relations:
            # filter dictionary
            dic_filtered = filter_dict(dic)
            # adding additional parameters
            dic_filtered['slu_overwrite'] = overwrite
            # remove parameters from dictionary that are not used for create_relationship_class
            attributed_fields = None
            if 'AttributedFields' in dic_filtered:
                attributed_fields = dic_filtered.pop('AttributedFields')
                # adding parameter to allow realtionship class having fields
                dic_filtered['attributed'] = 'ATTRIBUTED'
            rules = None
            if 'Rules' in dic_filtered:
                rules = dic_filtered.pop('Rules')
            # create relationship class
            create_relationship_class(**dic_filtered)
            # add fields
            if attributed_fields:
                for dic_field in attributed_fields:
                    field_domain_subtypes = None
                    if "FieldDomainSubtype" in dic_field:
                        field_domain_subtypes = dic_field.pop('FieldDomainSubtype')
                    # add fields
                    add_field(dic_filtered['out_relationship_class'], **dic_field)
                    # ad domains to subtypes
                    if field_domain_subtypes:
                        for dic_domain in field_domain_subtypes:
                            assign_domain_to_field(dic_filtered['out_relationship_class'], dic_field['field_name'],
                                                   dic_domain['field_domain'], dic_domain['subtype_code'])
            if rules:
                for dic_rule in rules:
                    add_rule_to_relationship_class(dic_filtered['out_relationship_class'], **dic_rule)

    # delete feature classes
    if delete_features:
        for fc in delete_features:
            delete_item(fc,"FeatureClass")

    # delete datasets
    if delete_datasets:
        for ds in delete_datasets:
            delete_item(ds,"FeatureDataset")

    # delete domains
    if delete_domains:
        for dm in delete_domains:
            delete_domain(workspace, dm)

    # delete all domains
    if delete_all_domains == "True":  
        delete_all_domain(workspace)

    # update feature class
    if update_features:
        for dic in update_features:
            # filter dictionary (if "" oder None)
            dic_filtered = filter_dict(dic)
            # add attribute rules
            if 'AttributeRules' in dic_filtered:
                for dic_rule in dic_filtered['AttributeRules']:
                    add_attribute_rule(dic_filtered['in_table'], **dic_rule)
            # add fields
            if 'AddFields' in dic_filtered:
                for dic_field in dic_filtered['AddFields']:
                    field_domain_subtypes = None
                    if "FieldDomainSubtype" in dic_field:
                        field_domain_subtypes = dic_field.pop('FieldDomainSubtype')
                    # add fields
                    add_field(dic_filtered['in_table'], **dic_field)
                    # add domains to subtypes
                    if field_domain_subtypes:
                        for dic_domain in field_domain_subtypes:
                            assign_domain_to_field(dic_filtered['in_table'], dic_field['field_name'],
                                                   dic_domain['field_domain'], dic_domain['subtype_code'])
            # delete fields
            if 'DeleteFields' in dic_filtered:
                # delete Fields
                delete_field(dic_filtered['in_table'], dic_filtered['DeleteFields'])

            # calculate fields
            if 'CalculateFields' in dic_filtered:
                for dic_field in dic_filtered['CalculateFields']:
                    # calculate fields
                    calculate_field(dic_filtered['in_table'], **dic_field)
    # update domains
    if update_domains:
        for dic in update_domains:
            # add value to CODED-domain
            for dic_code in dic["AddCodedValues"]:
                dic_code_value = {dic_code['code']:dic_code['code_description']}
                add_coded_value_to_domain(workspace, dic['domain_name'], dic_code_value)
    

if __name__ == "__main__":
    # path to the input JSON-file
    paramFile = arcpy.GetParameterAsText(0)
    #paramFile = r'C:\Datamodels\event_test.json'

    if paramFile:
        # read the json-file
        with open(paramFile, encoding='utf-8') as f:
            data = json.load(f)
            logfolder = data["LogFolder"]
            logversion = data["LogVersion"]
            conpath = data["Conpath"]
            db_name = data["DBName"]
            overwrite = data["Overwrite"]
            if "SpatialReferenceName" in data:
                spatial_reference_name = data["SpatialReferenceName"]
            else:
                spatial_reference_name = "CH1903+ LV95"
            if "EnvironmentSettings" in data:
                environment_settings = data["EnvironmentSettings"]
            else:
                environment_settings = None
            if "DeleteAllExisting" in data:
                delete_existing = data["DeleteAllExisting"]
            else:
                delete_existing = "False"
            if "Domains" in data:
                domains = data["Domains"]
            else:
                domains = None
            if "Datasets" in data:
                datasets = data["Datasets"]
            else:
                datasets = None
            if "Features" in data:
                features = data["Features"]
            else:
                features = None
            if "Tables" in data:
                tables = data["Tables"]
            else:
                tables = None
            if "Relations" in data:
                relations = data["Relations"]
            else:
                relations = None
            if "UpdateFeatures" in data:
                update_features = data["UpdateFeatures"]
            else:
                update_features = None
            if "UpdateDomains" in data:
                update_domains = data["UpdateDomains"]
            else:
                update_domains = None
            if "DeleteFeatures" in data:
                delete_features = data["DeleteFeatures"]
            else:
                delete_features = None
            if "DeleteDatasets" in data:
                delete_datasets = data["DeleteDatasets"]
            else:
                delete_datasets = None
            if "DeleteDomains" in data:
                delete_domains = data["DeleteDomains"]
            else:
                delete_domains = None
            if "DeleteAllDomains" in data:
                delete_all_domains = data["DeleteAllDomains"]
            else:
                delete_all_domains = "False"
            # instead of the previously implemented parameter "Environment", the parameter "Stage" is used
            if "Stage" in data:
                stage = data["Stage"]
            else:
                stage = None
            # parameter "Environment" maybe still used in an old version of a JSON-file
            if not stage:
                if "Environment" in data:
                    stage = data["Environment"]
    else:
        print('No Parameter-JSON file specified!')
        sys.exit()

    # check if logfolder exists
    if not os.path.isdir(logfolder):
        try:
            print(f'Creating a log folder: {logfolder}')
            os.makedirs(logfolder)
        except:
            raise ValueError(f'The logfolder "{logfolder}" does not exist and could not be created!')

    # initialise logging
    filename = db_name + '_' + logversion + '.log'
    log = os.path.join(logfolder, filename)
    init_logging(log)

    logger.info('****************************************************************')
    logger.info(f'Start logging: {time.ctime()}')
    start_time = time.time()

    # Main
    main(conpath, db_name, overwrite, spatial_reference_name, environment_settings, delete_existing, 
         domains, datasets, features, tables, relations, update_features, update_domains, delete_features, 
         delete_datasets, delete_domains, delete_all_domains, stage)
    
    # end logging
    end_time = time.time()
    i_error = search(log, "error")
    i_warning = search(log, "warning")
    logger.info("Datamodel created in " + str(round(end_time - start_time)) + " sec.")
    logger.info(f'# {i_error} errors found')
    logger.info(f'# {i_warning} warnings found')
    logger.info(f'End time: {time.ctime()}')
    logger.info('****************************************************************\n')

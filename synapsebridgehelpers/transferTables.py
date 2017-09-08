import synapseclient
import synapsebridgehelpers
import numpy as np
import pandas as pd

def transferTables(syn,sourceProjId, uploadProjId, extId_Str = '', simpleNameFilters =[], healthCodeList=None):
    """ This function transfers tables from a source project to the upload project (target project) 
    sorted by external Ids which contain extId_Str, group tables with simpleNameFilters, also can filter
    tables by healthcodes and then group by activity"""

    # List of tables sorted by activity using get_tables from synapsebridgehelper.tableHelpers
    all_tables = synapsebridgehelpers.get_tables(syn, sourceProjId, simpleNameFilters)
    
    # Converting the external IDs to healthcodes, as some people might have joined the clinical study later on
    if extId_Str != '':
        all_tables_list = list(all_tables['table.id'])
        res = synapsebridgehelpers.externalIds2healthCodes(syn,all_tables_list)
        res = res[res['externalId'].str.contains(extId_Str)]
        healthCodeList = list(res['healthCode'])
        extId_Str = ''

    tables_list = synapsebridgehelpers.filterTablesByActivity(all_tables,healthCodes = healthCodeList)        
    
    # Iterate over each activity in tables_list
    for activity_ in tables_list:
        print(activity_)
        
        # Initializing list of all table ids corresponding to that activity 
        df_main =[]
        
        # appending the sorted tables corresponding to that activity
        for table_index in range(0, len(activityTableIds)):
            result = synapsebridgehelpers.tableWithFileIds(syn,table_id = activityTableIds[table_index], healthcodes = healthCodeList)
            df = result['df']
            cols = result['cols']
            df_main.append(df)
        
        df_main = pd.concat(df_main)
        
#         # If different datatypes happen while merging tables this will change the column type in the resulting dataframe
#         # The following code sets it right and casts the data into its original form / form that syn.store would accept
#         # (for FILEHANDLEID type columns, the input needs to be an integer)
#         for col in cols:
#             if col.columnType == 'STRING': 
#                 df_main[col.name] = [str(item) if item==item else '' for item in df_main[col.name]]
#             elif col.columnType == 'INTEGER':
#                 df_main[col.name] = [int(item) if item==item else '' for item in df_main[col.name]]
#             elif col.columnType == 'FILEHANDLEID':
#                 df_main[col.name] = [int(item) if (item!='' and item==item) else '' for item in df_main[col.name]]
#             else:
#                 df_main[col.name] = [item if item==item else '' for item in df_main[col.name]]
        
#         # Correcting the order of the columns while uploading
#         df_main = df_main[[col.name for col in cols]]


        # Updaing schema and uploading
        schema = synapseclient.Schema(name=activity_, columns=cols, parent=uploadProjId)
        table = synapseclient.Table(schema, df_main)
        table = syn.store(table)
        table = syn.setProvenance(table.schema.id , activity = synapseclient.activity.Activity(used = all_tables[activity_]))

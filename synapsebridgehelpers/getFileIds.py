import synapseclient
import numpy as np
import pandas as pd
from synapseutils.copy import copyFileHandles

def copyFileIdsInBatch(syn,table_id,fileIds):
    """Outputs a dict(map) of the given fileId list to the output of copyFileHandles
    Will drop nas in the input fileIds, returns an empty map if the column is
    NOT of type FILEHANDLEID"""
    
    fileIds = fileIds.dropna().drop_duplicates().astype(int)
    len_fIds = len(fileIds)
    newIds = []

    # The check for 100 is because copyFileHandles cannot handle more than 100 requests at a time
    # The check for 0 is for empty colunms
    
    if len_fIds <= 100 and len_fIds>0:
        tempIds = copyFileHandles(syn, fileIds, ['TableEntity']*len_fIds,[table_id]*len_fIds, [None]*len_fIds, [None]*len_fIds)
        tempIds = [x['newFileHandle']['id'] for x in tempIds['copyResults']]
        newIds = newIds + tempIds
    else:
        start_pos = 0
        while start_pos < len_fIds:
            curr_len = min(100, len_fIds-start_pos)
            tempIds = copyFileHandles(syn, fileIds[start_pos:min(len_fIds, start_pos+100)], 
                                  ['TableEntity']*curr_len,[table_id]*curr_len, 
                                  [None]*curr_len,[None]*curr_len)
            tempIds = [x['newFileHandle']['id'] for x in tempIds['copyResults']]
            newIds = newIds + tempIds
            start_pos = start_pos+100

    # Map the fileIds to corresponding newIds
    newIds = [int(new_id) for new_id in newIds]
    idMap = dict(zip(fileIds,newIds))
    return idMap
    

def tableWithFileIds(syn,table_id, healthcodes=None):
    """ Returns a dict like {'df': dataFrame, 'cols': correspoding columns with tags} with actual fileHandleIds,
    also has an option to filter table given a list of healthcodes """
    
    # Getting cols from current table id
    cols = list(syn.getTableColumns(table_id))

    # Finding column names in the current table that have FILEHANDLEIDs as their type
    cols_filehandleids = [col.name for col in cols if col.columnType == 'FILEHANDLEID']

    # Grabbing results
    if healthcodes == None:
        results = syn.tableQuery('select * from %s' %(table_id))
    else:
        healthcodes = '(\''+'\',\''.join(healthcodes)+'\')'
        results = syn.tableQuery('select * from %s where healthCode in %s' %(table_id, healthcodes))

    # Store the results as a dataframe
    df = results.asDataFrame()
    cols = synapseclient.as_table_columns(df)

    # Iterate for each element(column) that has columntype FILEHANDLEID 
    for element in cols_filehandleids:
        df[element] = df[element].map(copyFileIdsInBatch(syn,table_id,df[element]))
        df[element] = [int(x) if x==x else '' for x in df[element]]
        
    return {'df' : df, 'cols' : cols}

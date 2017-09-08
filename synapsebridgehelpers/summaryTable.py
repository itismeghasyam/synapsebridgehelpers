import synapsebridgehelpers
import synapseclient
import pandas as pd

def summaryTable(syn, projectId, columns = []):
    """Outputs a concatenated table containing the given
    list of columns from the given projectId. If no columns 
    are given, then all columns are considered
    
    NOTE: When giving a column, note that it needs to be 
    present in all the tables of the given Project, otherwise
    the function will throw an error
    
    Arguments:
    - syn: a Synapse client object
    - projectID: synapse ID of the project we want to summarize
    - columns: list of columns we want in the summary table"""
    
    all_tables = synapsebridgehelpers.get_tables(syn, projectId)
    df_list = []
    columns_str = ','.join(columns)
    columns_str = '*' if columns_str == '' else columns_str # If empty then we choose all columns
    for table_id in all_tables['table.id']:
        df = syn.tableQuery('select %s from %s' %(columns_str,table_id))
        df = df.asDataFrame()
        schema = syn.get(table_id)
        df['originalTableName'] = [schema.name for count in range(0,df.shape[0])]
        df['originalTableId'] = [schema.id for count in range(0,df.shape[0])]
        df_list.append(df)
    df_main = pd.concat(df_list)    
    return df_main

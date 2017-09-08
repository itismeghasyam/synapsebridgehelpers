import synapsebridgehelpers
       
def filterTablesByActivity(syn, tables, healthCodes = None):
    """ Given a dataframe containing columns table.id and simpleName
    this function groups all tables according to their simpleNames while 
    filtering the tables that contain the given healthCodes. When no healthCodes 
    are given, the grouping is done just by simpleName
    
    Arguments:
    - tables: a dataframe of tables containing the columns table.id and simpleName
    - healthCodes: list of healthCodes to filter the tables by"""
        
    if healthCodes == None:
        table_activities = dict(tables.groupby(by='simpleName')['table.id'].apply(list))
        return table_activities
    else:
        res = synapsebridgehelpers.find_tables_with_data(syn=syn, healthCodes=healthCodes, tables=tables)
        res = res[res['healthCodeCounts']>0]
        table_activities = dict(res.groupby(by='simpleName')['table.id'].apply(list))
        return table_activities

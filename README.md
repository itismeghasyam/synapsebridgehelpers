# synapsebridgeHelpers

This package contains helper functions for dealing with data in Synapse that has been generated from bridge apps.

The goal is to provide

* Code for extracting subset of data from an existing project based on externalIds or healthCodes
* Code for finding data that match a specific identifier
* Generic code for running feature extractions in batch


###Finding data for specific set of individuals
Individuals are identified by healthCodes in bridge but can optionally be associated with a externalId.  But since the externalId doesn't have to be associated with every record (e.g. if the recordId is assigned after data has been contributed) we provide ways of identifying the healthCodes associated with an externalId anywhere in a list of tables.

```
import synapseclient, synapsebridgehelpers
syn = synapseclient.login()

tables = synapsebridgehelpers.get_tables(syn, 'syn3270406')
idMap = synapsebridgehelpers.externalIds2healthCodes(syn, tables['table.id'])
```

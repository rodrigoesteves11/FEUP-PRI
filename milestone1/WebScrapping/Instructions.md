# Instructions

In order to make the data compatible with Apache Solr follow the following steps.

## Step 1 - Join Json Parts

All the separate json files will be joined into a single file, run the **dataSpecification.py** program, in order to output a single file: **json_global.json**.


## Step 2 - Change Json Structure

Run the jupyter notebook **flatenningData.ipynb**. This program, changes the Json structure, in order to make it compatible with Apache Solr. It outputs the **transformed_species.json** file. 
# Makefile

# Default core name (can be overridden)
CORE_NAME ?= speciesv2

# Docker container name
CONTAINER_NAME ?= meic_solr

.PHONY: createCore deleteCore

# make createCore CORE_NAME=speciesv5
# Target to create a Solr core
createCore:
	sudo docker exec $(CONTAINER_NAME) bin/solr create_core -c $(CORE_NAME)

# make createCore CORE_NAME=speciesv5
# Target to delete a Solr core
deleteCore:
	sudo docker exec $(CONTAINER_NAME) bin/solr delete -c $(CORE_NAME)

# Allocates synonyms to solr
uploadSynonyms:
	sudo docker cp milestone2/schemas/kingdom_synonyms.txt meic_solr:/var/solr/data/$(CORE_NAME)/conf
	sudo docker cp milestone2/schemas/cs_synonyms.txt meic_solr:/var/solr/data/$(CORE_NAME)/conf
	sudo docker cp milestone2/schemas/intro_section_synonyms.txt meic_solr:/var/solr/data/$(CORE_NAME)/conf

# Allocates advanced schema to solr
uploadSchema:
	curl -X POST -H 'Content-type:application/json' --data-binary "@milestone2/schemas/advanced_schema.json" http://localhost:8983/solr/$(CORE_NAME)/schema

# Allocates documents to solr
uploadDocuments:
	curl -X POST -H 'Content-type:application/json' --data-binary "@milestone1/WebScrapping/transformed_species_data.json" http://localhost:8983/solr/$(CORE_NAME)/update?commit=true
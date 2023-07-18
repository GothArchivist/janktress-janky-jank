# This SQL query was developed to find all top container and digital object instances attached to a parent archival object in ASpace. Version of ASpace is yale-rebased-v3.3.1 (so basically 3.3.1)
SELECT SUBSTRING(resource.identifier, 1,14), resource.title AS collection, ao.title AS ao_title, ao.parent_id, ao.id AS item_id, 
CONCAT(ao.id,',') as ingest_id, #ingest_id concat is because this is partially created for ingesting media and metadata into Aviary in bulk, which uses a CSV style form in the user interface.
do.title AS do_title,
tc.barcode, sc.indicator_2 
FROM archival_object ao
LEFT JOIN resource ON ao.root_record_id=resource.id
LEFT JOIN instance ON ao.id=instance.archival_object_id
LEFT JOIN instance_do_link_rlshp idlr ON instance.id=idlr.instance_id
LEFT JOIN digital_object do ON idlr.digital_object_id=do.id
LEFT JOIN sub_container sc ON instance.id=sc.instance_id
LEFT JOIN top_container_link_rlshp tclr ON sc.id=tclr.sub_container_id
LEFT JOIN top_container tc ON tclr.top_container_id=tc.id
#WHERE ao.parent_id=
#WHERE ao.parent_id IN ()

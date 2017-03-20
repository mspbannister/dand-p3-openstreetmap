.mode csv
.import nodes.csv nodes1
.import ways.csv ways1
.import nodes_tags.csv nodes_tags1
.import ways_tags.csv ways_tags1
.import ways_nodes.csv ways_nodes1

BEGIN TRANSACTION;
INSERT INTO nodes SELECT * FROM nodes1;
INSERT INTO nodes_tags SELECT * FROM nodes_tags1;
INSERT INTO ways SELECT * FROM ways1;
INSERT INTO ways_nodes SELECT * FROM ways_nodes1;
INSERT INTO ways_tags SELECT * FROM ways_tags1;

DROP table nodes1;
DROP table nodes_tags1;
DROP table ways1;
DROP table ways_nodes1;
DROP table ways_tags1;

COMMIT;
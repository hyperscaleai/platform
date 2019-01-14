### Hive
  
CREATE EXTERNAL TABLE ngrams
(gram string, year int, occurrences bigint, pages bigint, books bigint)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'
STORED AS SEQUENCEFILE
LOCATION 's3://datasets.elasticmapreduce/ngrams/books/20090715/eng-1M/1gram/';
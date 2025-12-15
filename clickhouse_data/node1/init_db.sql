CREATE DATABASE IF NOT EXISTS shard;


CREATE TABLE IF NOT EXISTS shard.user_events (
    user_event_tag String,
    user_id String,
    event_time DateTime
)
ENGINE=ReplicatedMergeTree('/clickhouse/tables/shard1/user_events', 'replica_1')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY (user_id, event_time);


CREATE TABLE IF NOT EXISTS default.user_events (
    user_event_tag String,
    user_id String,
    event_time DateTime
)
ENGINE = Distributed('company_cluster', '', user_events, rand());


CREATE TABLE IF NOT EXISTS shard.film_events (
    film_event_tag String,
    film_id String,
    user_id String,
    event_time DateTime
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/shard1/film_events', 'replica_1')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY (film_id, event_time);


CREATE TABLE IF NOT EXISTS default.film_events (
    film_event_tag String,
    film_id String,
    user_id String,
    event_time DateTime
)
ENGINE = Distributed('company_cluster', '', film_events, rand());

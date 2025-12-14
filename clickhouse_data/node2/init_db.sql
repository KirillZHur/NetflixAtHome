CREATE DATABASE IF NOT EXISTS replica;


CREATE TABLE IF NOT EXISTS replica.user_events (
    user_event_tag String,
    user_id String,
    event_time DateTime
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/shard1/user_events', 'replica_2')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY (user_id, event_time);


CREATE TABLE IF NOT EXISTS replica.film_events (
    film_event_tag String,
    film_id String,
    user_id String,
    event_time DateTime
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/shard1/film_events', 'replica_2')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY (film_id, event_time);

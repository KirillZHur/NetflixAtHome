-- 1. USERS (TEMP)

DROP TEMPORARY TABLE IF EXISTS tmp_users;

CREATE TEMPORARY TABLE tmp_users
(
    user_id UUID
) ENGINE = Memory;

INSERT INTO tmp_users
SELECT generateUUIDv4()
FROM numbers(10000);


-- 2. USER EVENTS

-- user_registered (1 per user)
INSERT INTO default.user_events
SELECT
    'user_registered',
    toString(user_id),
    toDateTime('2025-09-01') + rand() % (92 * 86400)
FROM tmp_users;


-- user_login (~30 per user)
INSERT INTO default.user_events
SELECT
    'user_login',
    toString(user_id),
    toDateTime('2025-09-01') + rand() % (92 * 86400)
FROM tmp_users
ARRAY JOIN range(30) AS login_idx;



-- 3. FILMS (TEMP)
DROP TEMPORARY TABLE IF EXISTS tmp_films;

CREATE TEMPORARY TABLE tmp_films
(
    film_id UUID
) ENGINE = Memory;

INSERT INTO tmp_films
SELECT generateUUIDv4()
FROM numbers(500);


-- 4. FILM EVENTS

-- film_visited
INSERT INTO default.film_events
WITH
    (SELECT groupArray(user_id) FROM tmp_users) AS user_ids,
    (SELECT groupArray(film_id) FROM tmp_films) AS film_ids
SELECT
    'film_visited',
    toString(film_ids[(n.number % length(film_ids)) + 1]),
    toString(user_ids[(n.number % length(user_ids)) + 1]),
    toDateTime('2025-09-01') + rand() % (92 * 86400)
FROM numbers(500000) AS n;


-- start_watching_film
INSERT INTO default.film_events
WITH
    (SELECT groupArray(user_id) FROM tmp_users) AS user_ids,
    (SELECT groupArray(film_id) FROM tmp_films) AS film_ids
SELECT
    'start_watching_film',
    toString(film_ids[(n.number % length(film_ids)) + 1]),
    toString(user_ids[(n.number % length(user_ids)) + 1]),
    toDateTime('2025-09-01') + rand() % (92 * 86400)
FROM numbers(300000) AS n;


-- finished_watching_film
INSERT INTO default.film_events
WITH
    (SELECT groupArray(user_id) FROM tmp_users) AS user_ids,
    (SELECT groupArray(film_id) FROM tmp_films) AS film_ids
SELECT
    'finished_watching_film',
    toString(film_ids[(n.number % length(film_ids)) + 1]),
    toString(user_ids[(n.number % length(user_ids)) + 1]),
    toDateTime('2025-09-01') + rand() % (92 * 86400)
FROM numbers(180000) AS n;


-- 5. CLEANUP

DROP TEMPORARY TABLE IF EXISTS tmp_users;
DROP TEMPORARY TABLE IF EXISTS tmp_films;

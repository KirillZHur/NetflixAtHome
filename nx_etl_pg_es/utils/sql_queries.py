def get_max_time_across_tables(redis_date: str) -> str:
    return f"""
        SELECT max(max_mod) as new_date
        FROM (
            SELECT max(updated_at) as max_mod
            FROM public.film_works
            WHERE updated_at > '{redis_date}'::timestamp
            UNION
            SELECT max(g.updated_at) as max_mod
            FROM public.genres g
            JOIN public.genre_film_work gfw ON g.id = gfw.genre_id
            WHERE g.updated_at > '{redis_date}'::timestamp
            UNION
            SELECT max(p.updated_at) as max_mod
            FROM public.persons p
            JOIN public.person_film_work gfw ON p.id = gfw.person_id
            WHERE p.updated_at > '{redis_date}'::timestamp
        ) AS max_mod_across_tables
    """


def get_filmworks(redis_date: str) -> str:
    return f"""
        SELECT
            fw.id,
            fw.title,
            fw.description,
            fw.rating AS imdb_rating,
            fw.type,
            fw.preview_s3_key AS preview,
            fw.video_s3_key AS video,
            coalesce(array_agg(DISTINCT g.name), '{{}}') AS genres,
            coalesce(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'actor'), '{{}}') AS actors_names,
            coalesce(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'writer'), '{{}}') AS writers_names,
            coalesce(array_agg(DISTINCT p.full_name) FILTER (WHERE pfw.role = 'director'), '{{}}') AS directors_names,
            coalesce(json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'director'), '[]') AS directors,
             coalesce(json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'), '[]') AS actors,
             coalesce(json_agg(
                DISTINCT jsonb_build_object(
                    'id', p.id,
                    'name', p.full_name
                )
            ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'), '[]') AS writers
        FROM public.film_works fw
        LEFT JOIN public.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN public.persons p ON p.id = pfw.person_id
        LEFT JOIN public.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN public.genres g ON g.id = gfw.genre_id
        WHERE fw.updated_at > '{redis_date}'::timestamp or
              p.updated_at > '{redis_date}'::timestamp or
              g.updated_at > '{redis_date}'::timestamp
        GROUP BY fw.id
    """


def get_genres(redis_date: str) -> str:
    return f"""
        SELECT
            g.id,
            g.name,
            g.description
        FROM public.genres g
        WHERE g.updated_at > '{redis_date}'::timestamp
        GROUP BY g.id
    """


def get_persons(redis_date: str) -> str:
    return f"""
        WITH pfw_agg AS (
            SELECT
                pfw.person_id,
                pfw.film_work_id,
                array_agg(DISTINCT pfw.role) AS roles
            FROM public.person_film_work pfw
            GROUP BY pfw.person_id, pfw.film_work_id
        )
        SELECT
            pfw.person_id as id,
            p.full_name as name,
            coalesce(
                json_agg(DISTINCT
                    jsonb_build_object(
                        'id', pfw.film_work_id,
                        'roles', pfw.roles
                )
            ), '[]') AS films
        FROM pfw_agg AS pfw
        JOIN public.persons p ON p.id = pfw.person_id
        WHERE p.updated_at > '{redis_date}'::timestamp
        GROUP BY pfw.person_id, p.full_name;
    """


quaries_by_index: dict = {
    "movies": get_filmworks,
    "genres": get_genres,
    "persons": get_persons,
}

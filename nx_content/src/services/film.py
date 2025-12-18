from db.elastic import get_elastic
from models.response_models import FilmWork
from services.abstract_models import ServiceManager, Storage
from services.utils.paginator_ import get_offset
from services.utils.s3 import build_s3_url

from src.models.entity_models import SimpleFilmWork


class FilmService:
    def __init__(self, storage: Storage):
        self.storage = storage

    @staticmethod
    def _with_media(source: dict) -> dict:
        if not source:
            return source

        updated = dict(source)

        preview_url = build_s3_url(source.get("preview"))
        if preview_url:
            updated["preview"] = preview_url

        return updated

    async def get_by_id(self, film_id: str) -> FilmWork | None:
        film = await self._get_film_from_storage(film_id)

        if not film:
            return None

        return film

    async def search_films(
        self, get_query: str | None, page_number: int, page_size: int
    ) -> list[FilmWork] | None:
        offset = get_offset(page_number, page_size)

        search_query = {
            "from": offset,
            "size": page_size,
        }

        if get_query:
            wildcard_value = f"*{get_query.lower()}*"
            search_query["query"] = {
                "wildcard": {
                    "title.raw": {"value": wildcard_value, "case_insensitive": True}
                }
            }
        else:
            search_query["query"] = {"match_all": {}}

        result = await self.storage.search(index="movies", body=search_query)

        hits = result.get("hits", {}).get("hits", [])

        if not hits:
            return None

        return [FilmWork(**self._with_media(hit["_source"])) for hit in hits]

    async def sorted_films(
        self,
        sort: str,
        genre: str | None,
        page_number: int,
        page_size: int,
    ) -> list[FilmWork] | None:
        sort_order = "desc" if sort[0] == "-" else "asc"
        sort = sort.lstrip("-")

        offset = get_offset(page_number, page_size)

        search_query = {
            "from": offset,
            "size": page_size,
            "sort": [{sort: {"order": sort_order}}],
            "query": {"bool": {"must": [], "filter": []}},
        }

        if genre:
            search_query["query"]["bool"]["filter"].append({"term": {"genres": genre}})

        result = await self.storage.search(index="movies", body=search_query)

        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            return None

        return [FilmWork(**self._with_media(hit["_source"])) for hit in hits]

    async def _get_films_by_person(self, person_id: int) -> list[FilmWork] | None:
        search_query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "nested": {
                                "path": "directors",
                                "query": {"term": {"directors.id": person_id}},
                            }
                        },
                        {
                            "nested": {
                                "path": "actors",
                                "query": {"term": {"actors.id": person_id}},
                            }
                        },
                        {
                            "nested": {
                                "path": "writers",
                                "query": {"term": {"writers.id": person_id}},
                            }
                        },
                    ]
                }
            }
        }
        result = await self.storage.search(index="movies", body=search_query)
        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            return None

        return [FilmWork(**hit["_source"]) for hit in hits]

    async def _get_film_from_storage(self, film_id: str) -> FilmWork | None:
        try:
            doc = await self.storage.get(index="movies", id=film_id)
        except Exception:
            return None
        return FilmWork(**self._with_media(doc["_source"]))

    async def get_films_by_ids(self, film_ids: list[str]) -> list[FilmWork]:
        search_query = {
            "query": {"bool": {"filter": [{"terms": {"id": film_ids}}]}},
            "size": len(film_ids),
        }

        result = await self.storage.search(index="movies", body=search_query)
        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            return []

        result: list[SimpleFilmWork] = []
        for hit in hits:
            source = self._with_media(hit["_source"])
            result.append(
                SimpleFilmWork(
                    id=source["id"],
                    imdb_rating=source["imdb_rating"],
                    title=source["title"],
                    preview=source.get("preview"),
                    video=source.get("video"),
                )
            )
        return result


film_service = ServiceManager(FilmService, get_elastic)

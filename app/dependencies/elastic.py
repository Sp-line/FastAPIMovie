from typing import Annotated, TypeAlias

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from elastic.country import CountryElasticSyncer
from elastic.elasticsearch import es_helper
from elastic.genre import GenreElasticSyncer
from elastic.person import PersonElasticSyncer


def get_elasticsearch() -> AsyncElasticsearch:
    return es_helper.client()


AsyncElasticDep: TypeAlias = Annotated[AsyncElasticsearch, Depends(get_elasticsearch)]


def get_country_es_syncer(elastic: AsyncElasticDep) -> CountryElasticSyncer:
    return CountryElasticSyncer(elastic)


def get_genre_es_syncer(elastic: AsyncElasticDep) -> GenreElasticSyncer:
    return GenreElasticSyncer(elastic)


def get_person_es_syncer(elastic: AsyncElasticDep) -> PersonElasticSyncer:
    return PersonElasticSyncer(elastic)


CountryElasticSyncerDep: TypeAlias = Annotated[CountryElasticSyncer, Depends(get_country_es_syncer)]
GenreElasticSyncerDep: TypeAlias = Annotated[GenreElasticSyncer, Depends(get_genre_es_syncer)]
PersonElasticSyncerDep: TypeAlias = Annotated[PersonElasticSyncer, Depends(get_person_es_syncer)]

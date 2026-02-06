from elasticsearch import AsyncElasticsearch

from elastic.documents import Movie, Country, Genre, Person


async def documents_init(client: AsyncElasticsearch) -> None:
    await Movie.init(using=client)
    await Country.init(using=client)
    await Genre.init(using=client)
    await Person.init(using=client)
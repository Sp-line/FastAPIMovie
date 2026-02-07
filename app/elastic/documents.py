from datetime import datetime

from elasticsearch.dsl import AsyncDocument, Integer, Text, Keyword, M, mapped_field, Date


class Movie(AsyncDocument):
    id: M[int] = mapped_field(Integer())
    title: M[str] = mapped_field(Text(analyzer="english", fields={"keyword": Keyword()}))
    slug: M[str] = mapped_field(Keyword())
    duration: M[int] = mapped_field(Integer())
    release_year: M[int] = mapped_field(Integer())
    poster_url: M[str | None] = mapped_field(Keyword())
    premiere_date: M[datetime | None] = mapped_field(Date())
    age_rating: M[str | None] = mapped_field(Keyword())
    description: M[str | None] = mapped_field(Text(analyzer="english"))

    genre_ids: M[list[int]] = mapped_field(Keyword())
    country_ids: M[list[int]] = mapped_field(Keyword())
    person_ids: M[list[int]] = mapped_field(Keyword())

    class Index:
        name = "movies"


class Country(AsyncDocument):
    id: M[int] = mapped_field(Integer())
    slug: M[str] = mapped_field(Keyword())
    name: M[str] = mapped_field(Text(analyzer="standard", fields={"keyword": Keyword()}))

    class Index:
        name = "countries"


class Genre(AsyncDocument):
    id: M[int] = mapped_field(Integer())
    slug: M[str] = mapped_field(Keyword())
    name: M[str] = mapped_field(Text(analyzer="english", fields={"keyword": Keyword()}))

    class Index:
        name = "genres"


class Person(AsyncDocument):
    id: M[int] = mapped_field(Integer())
    slug: M[str] = mapped_field(Keyword())
    full_name: M[str] = mapped_field(Text(analyzer="standard", fields={"keyword": Keyword()}))

    class Index:
        name = "persons"

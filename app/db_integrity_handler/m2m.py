from constants.db import PostgresErrorCode
from db_integrity_handler.base import TableErrorHandler
from exceptions.db import UniqueException, RelatedObjectNotFoundException
from schemas.db import ConstraintRule

uq_country_movie = ConstraintRule(
    name="uq_country_movie",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "movie_country_associations", "country_id", "movie_id"
    )
)

fk_movie_country_associations_country_id_countries = ConstraintRule(
    name="fk_movie_country_associations_country_id_countries",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="country_id",
        table_name="countries"
    )
)

fk_movie_country_associations_movie_id_movies = ConstraintRule(
    name="fk_movie_country_associations_movie_id_movies",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="movie_id",
        table_name="movies"
    )
)

movie_country_error_handler = TableErrorHandler(
    uq_country_movie,
    fk_movie_country_associations_country_id_countries,
    fk_movie_country_associations_movie_id_movies
)


uq_movie_genre = ConstraintRule(
    name="uq_movie_genre",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "movie_genre_associations", "genre_id", "movie_id"
    )
)

fk_movie_genre_associations_genre_id_genres = ConstraintRule(
    name="fk_movie_genre_associations_genre_id_genres",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="genre_id",
        table_name="genres"
    )
)

fk_movie_genre_associations_movie_id_movies = ConstraintRule(
    name="fk_movie_genre_associations_movie_id_movies",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="movie_id",
        table_name="movies"
    )
)

movie_genre_error_handler = TableErrorHandler(
    uq_movie_genre,
    fk_movie_genre_associations_genre_id_genres,
    fk_movie_genre_associations_movie_id_movies
)


uq_movie_person_role = ConstraintRule(
    name="uq_movie_person_role",
    error_code=PostgresErrorCode.UNIQUE_VIOLATION,
    exception=UniqueException(
        "movie_person_associations", "person_id", "movie_id", "role"
    )
)

fk_movie_person_associations_person_id_persons = ConstraintRule(
    name="fk_movie_person_associations_person_id_persons",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="person_id",
        table_name="persons"
    )
)

fk_movie_person_associations_movie_id_movies = ConstraintRule(
    name="fk_movie_person_associations_movie_id_movies",
    error_code=PostgresErrorCode.FOREIGN_KEY_VIOLATION,
    exception=RelatedObjectNotFoundException(
        field_name="movie_id",
        table_name="movies"
    )
)

movie_person_error_handler = TableErrorHandler(
    uq_movie_person_role,
    fk_movie_person_associations_person_id_persons,
    fk_movie_person_associations_movie_id_movies
)
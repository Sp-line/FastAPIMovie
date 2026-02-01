from fastapi import APIRouter

from core.config import settings
from .country import router as country_router
from .genres import router as genres_router
from .movie import router as movie_router
from .movie_country import router as movie_country_router
from .movie_genre import router as movie_genre_router
from .movie_person import router as movie_person_router
from .movie_shot import router as movie_shot_router
from .person import router as person_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(country_router, prefix="/countries", tags=["Countries"])
router.include_router(genres_router, prefix="/genres", tags=["Genres"])
router.include_router(movie_router, prefix="/movies", tags=["Movies"])
router.include_router(person_router, prefix="/persons", tags=["Persons"])
router.include_router(movie_shot_router, prefix="/movie-shots", tags=["Movie-Shots"])
router.include_router(movie_country_router, prefix="/movie-country-associations", tags=["Movie-Country-Associations"])
router.include_router(movie_genre_router, prefix="/movie-genre-associations", tags=["Movie-Genre-Associations"])
router.include_router(movie_person_router, prefix="/movie-person-associations", tags=["Movie-Person-Associations"])

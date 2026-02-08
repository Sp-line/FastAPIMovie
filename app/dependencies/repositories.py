from dishka import Provider, Scope, provide

from repositories.country import CountryRepository
from repositories.genre import GenreRepository
from repositories.m2m import MovieCountryRepository, MovieGenreRepository, MoviePersonRepository
from repositories.movie import MovieRepository
from repositories.movie_shot import MovieShotRepository
from repositories.person import PersonRepository
from repositories.signals import SignalUnitOfWork
from repositories.unit_of_work import UnitOfWork
from signals.event_session import EventSession


class RepositoryProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_uow(self, session: EventSession) -> UnitOfWork:
        return UnitOfWork(session)

    @provide
    def get_signal_uow(self, session: EventSession) -> SignalUnitOfWork:
        return SignalUnitOfWork(session)

    get_movie_repo = provide(MovieRepository)
    get_person_repo = provide(PersonRepository)
    get_genre_repo = provide(GenreRepository)
    get_country_repo = provide(CountryRepository)
    get_movie_shot_repo = provide(MovieShotRepository)

    get_movie_country_repo = provide(MovieCountryRepository)
    get_movie_genre_repo = provide(MovieGenreRepository)
    get_movie_person_repo = provide(MoviePersonRepository)
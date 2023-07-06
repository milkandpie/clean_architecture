from typing import Type, Dict

from clean_architecture.applications import RepositoryInjector, Repository


class InMemoryRepositoryInjector(RepositoryInjector):
    def __init__(self, pairs: Dict[Type[Repository], Repository] = None):
        self.__repository_concreate_pairs = pairs or {}

    def get_concreate(self, repository_type: Type[Repository]):
        concreate = self.__repository_concreate_pairs.get(repository_type)
        if not concreate:
            raise Exception('Not registered abstract repository')

        return concreate

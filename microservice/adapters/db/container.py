from dependency_injector import containers, providers


class DB(containers.DynamicContainer):
    config = providers.Configuration()

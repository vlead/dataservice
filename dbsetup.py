from src.app import create_app
from src.db import *
import src.config as config


def create_integration_levels():
    int_levels = (0, 1, 2, 3, 4, 5, 6)
    for level in int_levels:
        int_level = IntegrationLevel(level=level)
        int_level.save()


def create_hosting_platforms():
    platforms = ('IIIT', 'BADAL', 'AWS', 'ELSE')
    for plat in platforms:
        platform = HostingPlatform(name=plat)
        platform.save()


def create_type_of_labs():
    types = ('Simulation', 'Remote Triggered',
             'Simulation and Remote Triggered', 'Pilot Phase')
    for type in types:
        lab_type = TypeOfLab(type=type)
        lab_type.save()


if __name__ == "__main__":
    db.create_all(app=create_app(config))
    create_integration_levels()
    create_hosting_platforms()
    create_type_of_labs()

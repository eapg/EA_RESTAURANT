#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='migrations', url='postgresql://postgres:1234@localhost/ea_restaurant', debug='False')

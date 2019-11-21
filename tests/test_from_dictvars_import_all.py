

globals_names = set(globals().keys())

from dictvars import *


def test_import_all():
    dictvars_names = {'dictvars', 'varsnamed', 'compact'}
    additional_names = {'globals_names', 'test_import_all'}
    globals_should_be = globals_names | dictvars_names | additional_names

    assert set(globals().keys()) == globals_should_be

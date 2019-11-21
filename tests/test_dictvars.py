
from pytest import raises


some_global_var = 'a global var'
leaked_global_var = None


def test_dictvars_local():

    from dictvars import dictvars

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        return dictvars(ds)

    rv = doublesum(3, 5)
    assert isinstance(rv, dict)
    assert set(rv.keys()) == {'ds'}
    assert rv['ds'] == 16


def test_dictvars_outer():

    from dictvars import dictvars

    outer = 'outer variable'

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        return dictvars(ds, outer)

    rv = doublesum(3, 5)
    assert set(rv.keys()) == {'ds', 'outer'}
    assert rv['ds'] == 16
    assert rv['outer'] == outer


def test_dictvars_global():

    from dictvars import dictvars

    outer = 'outer variable'

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        return dictvars(ds, outer, some_global_var)

    rv = doublesum(3, 5)
    assert set(rv.keys()) == {'ds', 'outer', 'some_global_var'}
    assert rv['ds'] == 16
    assert rv['outer'] == outer
    assert rv['some_global_var'] == some_global_var


def test_dictvars_local_leak():

    from dictvars import dictvars

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        leaked_local = ds
        return dictvars(ds)

    rv = doublesum(3, 5)
    assert isinstance(rv, dict)
    assert set(rv.keys()) == {'ds', 'leaked_local'}
    assert rv['ds'] == 16
    assert rv['ds'] == rv['leaked_local']


def test_dictvars_global_leak():

    from dictvars import dictvars

    outer = 'outer variable'
    global leaked_global_var
    leaked_global_var = some_global_var

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        return dictvars(ds, outer, some_global_var)

    rv = doublesum(3, 5)
    assert set(rv.keys()) == {'ds', 'outer', 'some_global_var',
                              'leaked_global_var'}
    assert rv['ds'] == 16
    assert rv['outer'] == outer
    assert rv['leaked_global_var'] == some_global_var
    assert rv['some_global_var'] == some_global_var


def test_varsnamed_local():

    from dictvars import varsnamed

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        return varsnamed('ds')

    rv = doublesum(3, 5)
    assert isinstance(rv, dict)
    assert set(rv.keys()) == {'ds'}
    assert rv['ds'] == 16


def test_varsnamed_outer():

    from dictvars import varsnamed

    outer = 'outer variable'

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        return varsnamed('ds', 'outer')

    # currently varsnamed doesn't work with implicit nonlocals
    with raises(NameError):
        rv = doublesum(3, 5)


def test_varsnamed_outer_nonlocal():

    from dictvars import varsnamed

    outer = 'outer variable'

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        nonlocal outer
        return varsnamed('ds', 'outer')

    rv = doublesum(3, 5)
    assert set(rv.keys()) == {'ds', 'outer'}
    assert rv['ds'] == 16
    assert rv['outer'] == outer


def test_varsnamed_global():

    from dictvars import varsnamed

    outer = 'outer variable'

    def doublesum(a, b):
        da = a*2
        db = b*2
        ds = da + db
        nonlocal outer
        return varsnamed('ds', 'outer', 'some_global_var')

    rv = doublesum(3, 5)
    assert set(rv.keys()) == {'ds', 'outer', 'some_global_var'}
    assert rv['ds'] == 16
    assert rv['outer'] == outer
    assert rv['some_global_var'] == some_global_var

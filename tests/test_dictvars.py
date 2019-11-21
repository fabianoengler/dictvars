
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


def test_dictvars_local_kwargs():

    from dictvars import dictvars

    def somefunc():
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        non_leak = b
        return dictvars(a, e, renamed=b, d=d)

    rv = somefunc()
    assert set(rv.keys()) == {'a', 'e', 'renamed', 'd'}
    assert rv['renamed'] == 2


def test_dictvars_outer_kwargs():

    from dictvars import dictvars

    outer1 = 'outer variable 1'
    outer2 = 'outer variable 2'
    outer3 = 'outer variable 3'

    def somefunc():
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        non_leak = b
        return dictvars(a, e, outer1, renamed=b, d=d, outer_ren=outer3)

    rv = somefunc()
    assert set(rv.keys()) == {'a', 'e', 'outer1', 'renamed', 'd', 'outer_ren'}
    assert rv['outer1'] == outer1
    assert rv['outer_ren'] == outer3


def test_dictvars_global_kwargs():

    from dictvars import dictvars

    def somefunc():
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        non_leak = b
        return dictvars(a, e, global_renamed=some_global_var)

    rv = somefunc()
    assert set(rv.keys()) == {'a', 'e', 'global_renamed'}
    assert rv['global_renamed'] == some_global_var


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

# hypothesis_1085_repro

This repo is a reproduction of [issue 1085 for Hypothesis](https://github.com/HypothesisWorks/hypothesis-python/issues/1085).

## Details
* Install requirements into a virtualenv or whatever you're using for dependency management via requirements.txt. This includes coverage, py.test, and hypothesis.

### Source
Take a peek inside of the source code (`repro_package`). You'll see there are two files:

* `hit_by_unittest.py` - contains a method called sum which is tested by files in the `tests` folder.
* `not_hit_by_unittest.py` - contains a method call diff, which is never imported or tested by any of the tests in the `tests` folder.

### Tests
There are two test files:
* `test_no_hypothesis.py` - contains a unittest.TestCase which tests `sum` on a basic case; does not use hypothesis.
* `test_hypothesis.py` - contains a unittest.TestCase which tests `sum` using hypothesis with an integers strategy. **Currently, this code is commented out**.

## Repro
Since the contents of `test_hypothesis.py` are commented out, if you run the following:

```bash
$ coverage run --source repro_package/ -m pytest tests
coverage report
```

You get: 

```bash
$ coverage run --source repro_package/ -m pytest tests
====================================================================================== test session starts =======================================================================================
platform darwin -- Python 3.6.4, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /Users/johnnygoodnow/Documents/git/hypothesis_1085_repro, inifile:
plugins: hypothesis-3.44.22
collected 1 item

tests/test_no_hypothesis.py .                                                                                                                                                              [100%]

==================================================================================== 1 passed in 0.01 seconds ====================================================================================

$ coverage report
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
repro_package/__init__.py                  0      0   100%
repro_package/hit_by_unittest.py           2      0   100%
repro_package/not_hit_by_unittest.py       2      2     0%
----------------------------------------------------------
TOTAL                                      4      2    50%
```

**Note how `not_hit_by_unittest.py` is included in the coverage at 0% cover**. This is because it is listed in the unexecuted files in coverage's source directory, which is only run after the test. Because of the bug in hypothesis 1085, you'll see below how this file will not be included.

Now, if you uncomment out the file `test_hypothesis` (feel free to move the file in and out of the test directory to go back and forth between these two states), you get the following (same commands as above):

```bash
$ coverage run --source repro_package/ -m pytest tests
====================================================================================== test session starts =======================================================================================
platform darwin -- Python 3.6.4, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
rootdir: /Users/johnnygoodnow/Documents/git/hypothesis_1085_repro, inifile:
plugins: hypothesis-3.44.22
collected 2 items

tests/test_hypothesis.py .                                                                                                                                                                 [ 50%]
tests/test_no_hypothesis.py .                                                                                                                                                              [100%]

==================================================================================== 2 passed in 0.18 seconds ====================================================================================

$ coverage report
Name                               Stmts   Miss  Cover
------------------------------------------------------
repro_package/__init__.py              0      0   100%
repro_package/hit_by_unittest.py       2      0   100%
------------------------------------------------------
TOTAL                                  2      0   100%
```

And there you have it :).

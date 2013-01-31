Initial setup:

  $ [ -n "$PYTHON" ] || PYTHON="`which python`"
  $ export PYTHONPATH=$TMPDIR
  $ cd ${TESTDIR}/../../../
  $ $PYTHON setup.py develop --install-dir=$TMPDIR > /dev/null 2>&1
  $ alias future_url="$TMPDIR/future_url"

Test normal behavior without write:

  $ cd $TESTDIR/../test_project
  $ future_url -q

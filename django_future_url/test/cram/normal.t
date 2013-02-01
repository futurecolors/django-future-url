Initial setup:

  $ [ -n "$PYTHON" ] || PYTHON="`which python`"
  $ export PYTHONPATH=$TMPDIR
  $ cd ${TESTDIR}/../../../
  $ $PYTHON setup.py develop --install-dir=$TMPDIR > /dev/null 2>&1
  $ alias future_url="$TMPDIR/future_url"

Test normal behavior without write:

  $ cd $TESTDIR/../test_project
  $ future_url
  Files needing modification:
  template.html
      Proposed replace: {% url someview %} -> {% url 'someview' %}
      Need to add {% load url from future %}
  templates/comma.html
      Comma separated attributes in url tag are no longer supported.
      Proposed replace: {% url path.to.view arg, arg2 %} -> {% url 'path.to.view' arg arg2 %}
      Need to add {% load url from future %}
  No actual changes made. Run future_url --write to fix files right now.

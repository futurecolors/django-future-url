Initial setup:

  $ [ -n "$PYTHON" ] || PYTHON="`which python`"
  $ export PYTHONPATH=$TMPDIR
  $ cd ${TESTDIR}/../../../
  $ $PYTHON setup.py develop --install-dir=$TMPDIR > /dev/null 2>&1
  $ alias future_url="$TMPDIR/future_url"
  $ cp -R $TESTDIR/../test_project $TMPDIR/test_project

Test --write behavior:

  $ cd $TMPDIR/test_project
  $ future_url --write
  Files needing modification:
  template.html
      Proposed replace: {% url someview %} -> {% url 'someview' %}
      Need to add {% load url from future %}
      File updated
  templates/comma.html
      Comma separated attributes in url tag are no longer supported.
      Proposed replace: {% url path.to.view arg, arg2 %} -> {% url 'path.to.view' arg arg2 %}
      Need to add {% load url from future %}
      File updated

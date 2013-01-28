Initial setup:

  $ alias future_url="$TESTDIR/../../bin/future_url"
  $ cp -R $TESTDIR/../test_project $TMPDIR/test_project

Test --write --verbose behavior:

  $ cd $TMPDIR/test_project
  $ future_url --write --verbose
  template.html
  Proposed replace: {% url someview %} -> {% url 'someview' %}
  Need to add {% load url from future %}
  File updated
  
  
  templates/recursive.html
  
  
  Finished





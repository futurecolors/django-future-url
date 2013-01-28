Initial setup:

  $ alias future_url="$TESTDIR/../../bin/future_url"

Test --verbose behavior without write:

  $ cd $TESTDIR/../test_project
  $ future_url --verbose
  template.html
  Proposed replace: {% url someview %} -> {% url 'someview' %}
  Need to add {% load url from future %}
  
  
  templates/recursive.html
  
  
  Finished




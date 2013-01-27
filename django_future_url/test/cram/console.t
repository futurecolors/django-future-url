Initial setup:

  $ alias future_url="$TESTDIR/../../bin/future_url"
  $ export PATH=/Users/prophet/projects/django-future-url/:$PATH

Test simple behavior:

  $ cd $TESTDIR/../test_project
  $ future_url --verbose
  template.html
  replaced: {% url someview %} -> {% url 'someview' %}
  Added {% load url from future %}
  
  
  templates/recursive.html
  
  
  Finished




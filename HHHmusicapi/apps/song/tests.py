from django.test import TestCase

# Create your tests here.
kwargs = {"allow_blank3": 'aaaaa',
            "allow_blank1": 'bbbbb',
            "allow_blank2": 'ccccc',
          }
allow_blank = kwargs.pop('allow_blank')
print(allow_blank)
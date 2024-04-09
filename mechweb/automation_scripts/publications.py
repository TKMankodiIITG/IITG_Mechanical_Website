# Now you should be able to import the mechweb module
import sys
print(f"system Paths:{sys.path}") 
from mechweb.models import FacultyPage
# import requests

def updateGoogleScholarPublications():
    try: 
        all_faculty_data = FacultyPage.objects.all()
        for faculty_data in all_faculty_data:
            print(f"Google Scholar Publications for {faculty_data}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")

# updateGoogleScholarPublications()
from mechweb.models import FacultyPage
from urllib.parse import urlparse, parse_qs
from django.core.cache import cache
import requests

def updateGoogleScholarPublications():
    try: 
        all_faculty_data = FacultyPage.objects.all()
        for faculty_data in all_faculty_data:
            print(f"Google Scholar Publications for  {faculty_data}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")

updateGoogleScholarPublications()
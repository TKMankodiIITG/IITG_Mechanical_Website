from mechweb.models import FacultyPage

def updateGoogleScholarPublications():
    print("Professor name,Professor Email,Google Scholar Profile")
    try: 
        all_faculty_data = FacultyPage.objects.all()
        for faculty_data in all_faculty_data:
            if faculty_data.google_scholar_profile_link:
                print(f"{faculty_data},{faculty_data.email_id},{faculty_data.google_scholar_profile_link}")
            else:
                print(f"{faculty_data},{faculty_data.email_id}, No Google Scholar Profile")

    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")


updateGoogleScholarPublications()
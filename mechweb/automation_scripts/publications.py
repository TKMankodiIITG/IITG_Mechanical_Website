
# This is cron job page to add research paper publiucations to professors Page

from mechweb.models import FacultyPage,PublicationHomePage,PublicationPage,PublicationPageFaculty
from urllib.parse import urlparse, parse_qs
from django.core.cache import cache
from scholarly import scholarly
from django.utils.text import slugify
import json
import csv
import time
import datetime
def updateGoogleScholarLinks():
    try:
        csv_file_path = 'mechweb/automation_scripts/Data for the nW/GoogleScholarLinks.csv'
        all_faculty_data = FacultyPage.objects.all()

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                for faculty_data in all_faculty_data:            
                    if(faculty_data.email_id == row["Professor Email"]):
                        # print(f'{faculty_data.email_id} has google scholar profile link {row["Google Scholar Profile"]}')
                        faculty_data.google_scholar_profile_link = row["Google Scholar Profile"]
                        faculty_data.save()
                        # print(faculty_data.google_scholar_profile_linkyy)
                        break
                
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        
def checkGoogleScholarProfile():
    ##This function can be used to print the csv of professor's google scholar links
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
        
        
        
def checking_currect_professors():
    print("Professor name,Professor Email,Google Scholar Profile")
    try: 
        all_faculty_data = FacultyPage.objects.all()
        current_faculty_list = []
        today = datetime.date.today() 
        for fac in all_faculty_data:
            try:
                if fac.leaving_date and today < fac.leaving_date:
                    current_faculty_list.append(fac)
                if not fac.leaving_date:
                    current_faculty_list.append(fac)
                if fac.on_visit:
                    current_faculty_list.remove(fac)
            except Exception as error:
                print(f"error: {error}")
        count=0
        for faculty_data in current_faculty_list:
            print(f"{faculty_data}: lien-{faculty_data.on_lien} visit-{faculty_data.on_visit} depute-{faculty_data.on_depute}")
            count+=1
            # print(f"leaving year-{faculty_data.leaving_date}")
            print(f"{faculty_data.leaving_date} current time-{today}")
            # if faculty_data.google_scholar_profile_link:
            #     print(f"{faculty_data},{faculty_data.id}")
            # else:
            #     print(f"{faculty_data},{faculty_data.email_id}, No Google Scholar Profile")
        print(f"total faculty count---------------------------------{count}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")
        
        

def updateGoogleScholarPublications():
    try: 
        all_faculty_data = FacultyPage.objects.all()
        current_faculty_list = []
        today = datetime.date.today() 
        for fac in all_faculty_data:
            try:
                if fac.leaving_date and today < fac.leaving_date:
                    current_faculty_list.append(fac)
                if not fac.leaving_date:
                    current_faculty_list.append(fac)
                if fac.on_visit:
                    current_faculty_list.remove(fac)
            except Exception as error:
                print(f"error: {error}")
        for faculty_data in current_faculty_list:
            # if faculty_data.google_scholar_profile_link and not PublicationPageFaculty.objects.filter(faculty_id=faculty_data.id).exists():
            if faculty_data.google_scholar_profile_link:
                print(f"------------------------fetching publications of {faculty_data} ----------------------------")
                parsed_url = urlparse(faculty_data.google_scholar_profile_link)
                query_params = parse_qs(parsed_url.query)
                user_id = query_params.get('user', [''])[0]
                author = scholarly.search_author_id(user_id)
                # scholarly.pprint(scholarly.fill(author, sections=['publications']))
                result = scholarly.fill(author, sections=[])
                publications_list=result['publications']
                sorted_publications_list = sorted(publications_list, key=lambda pub: int(pub['bib']['pub_year']) if 'bib' in pub and 'pub_year' in pub['bib'] else 0, reverse=True)
                delete_publications_of_professor(faculty_data.id)
                for publication in sorted_publications_list[:5]:
                #     # print(publication)
                    # print(f"Publication Title: {publication['bib']['title']}")
                    
                    title= publication['bib']['title']
                    pub_year= publication['bib']['pub_year']
                    # search_query = scholarly.search_pubs(title)
                    # publication_details=next(search_query)
                    # abstract=publication_details['bib']['abstract']
                    # download_link=publication_details['pub_url']
                    # pub_journal=publication_details['bib']['venue']
                    # citations=str(publication_details['num_citations'])
                    # add_publication(title,pub_year,faculty_data.id,abstract,download_link,pub_journal,citations)
                    add_publication_without_details(title,pub_year,faculty_data.id)
                    # time.sleep(2)
                # result=json.dumps(result).strip()
                
                # print(result2)
                

    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")

def add_publication_without_details(title,pub_year,faculty_id):
    try:
        # Generate slug from the title
        slug = slugify(title)
        publication_home = PublicationHomePage.objects.all()[0]
        # Create a new PublicationPage instance
        publication = PublicationPage(
            title=title,
            name=title,
            pub_type='2',
            pub_year=int(pub_year),
            slug=slug,
            depth=0 
        )
        publication_home.add_child(instance=publication)
        publication_home.save()
        # Associate the faculty with the publication
        PublicationPageFaculty.objects.create(
            page=publication,
            faculty_id=faculty_id,
            research_statement="Publications"
        )

        print(f"Publication '{publication.name}' added successfully with associated faculty id={faculty_id}.")

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")

def add_publication(title,pub_year,faculty_id,abstract,download_link,pub_journal,citations):
    try:
        # Generate slug from the title
        slug = slugify(title)
        publication_home = PublicationHomePage.objects.all()[0]
        # Create a new PublicationPage instance
        publication = PublicationPage(
            title=title,
            name=title,
            pub_type='2',
            pub_year=int(pub_year),
            abstract=abstract,
            download_link=download_link,
            pub_journal=pub_journal,
            citations=citations,
            slug=slug,
            depth=0 
        )
        publication_home.add_child(instance=publication)
        publication_home.save()
        # Associate the faculty with the publication
        PublicationPageFaculty.objects.create(
            page=publication,
            faculty_id=faculty_id,
            research_statement="Publications"
        )

        print(f"Publication '{publication.name}' added successfully with associated faculty id={faculty_id}.")

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")

def delete_publications_of_professor(professor_id):
    try:
        # Retrieve all PublicationPageFaculty instances associated with the professor
        publications = PublicationPageFaculty.objects.filter(faculty_id=professor_id)

        # Delete all associated publications
        for publication in publications:
            publication.page.delete()  # Delete the associated publication page

        print(f"All publications of professor {professor_id} have been deleted.")

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        
# updateGoogleScholarLinks()

def print_publications_of_professor(professor_id):
    try:
        # Retrieve all PublicationPageFaculty instances associated with the professor
        publications = PublicationPageFaculty.objects.filter(faculty_id=professor_id)

        # Print all associated publications
        if publications.exists():
            find_professor_with_id(professor_id)
            for publication in publications:
                # Print details of each publication
                print(f"Publication Name: {publication.page.name}")
                print(f"Publication Path: {publication.page.path}")
                print(f"Publication Year: {publication.page.pub_year}")
                print(f"Publication Type: {publication.page.pub_type}")
                # Print more details as needed
                print("----------------------------------------")
        else:
            print(f"No publications found for professor {professor_id}")

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        

def find_professor_with_id(professor_id):
    try:
        professor = FacultyPage.objects.get(id=professor_id)
        print(f"Professor with ID {professor_id} found.")
        print(f"Professor Name: {professor}")
        print(f"Professor Email: {professor.email_id}")
        if(professor.google_scholar_profile_link):
            print(f"Professor Google Scholar Profile: {professor.google_scholar_profile_link}")
        # Print more details as needed
    except Exception as e:
        print(f"Error: {e}")
def  delete_publication_by_title(title):
    try:
        publication = PublicationPage.objects.get(title=title)
        publication.delete()
        print(f"Publication '{title}' has been deleted successfully.")

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        
def delete_all_publications_of_faculty_with_google_scholar_link():
    try:
        all_faculty_data = FacultyPage.objects.all()
        for faculty_data in all_faculty_data:
            if faculty_data.google_scholar_profile_link:
                print(f"deleting all publications of {faculty_data}- {faculty_data.id}")
                delete_publications_of_professor(faculty_data.id)
                print(f"deleted all publications of {faculty_data}- {faculty_data.id}")
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {e}")

    
print("------------------------------------------------NEW DATA------------------------------------------------")
# checkGoogleScholarProfile()
# delete_all_publications_of_faculty_with_google_scholar_link()
updateGoogleScholarPublications()
# checkAllPublicationsWithFaculty()
# delete_publications_of_professor(2121)
print("------------------------------------------------NEW DATA------------------------------------------------")
# print_publications_of_professor(2123)
# checking_currect_professors()
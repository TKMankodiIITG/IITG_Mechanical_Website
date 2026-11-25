from django.shortcuts import render
from .models import MechHomePage
# Create your views here.
import pandas as pd
from django.http import HttpResponse
from mechweb.models import PublicationPage  # Adjust import according to your project structure

def download_excel(request):
    from_month = request.GET.get('from')
    to_month = request.GET.get('to')

    if not from_month or not to_month:
        return HttpResponse("Missing 'from' or 'to' parameter", status=400)

    # Filter publications by year
    # publications = PublicationPage.objects.filter(pub_year__startswith=year)
    # print(publications)
    # Create a DataFrame
    # data = {
    #     'Sl. No': [i + 1 for i in range(len(publications))],
    #     'Year': [pub.pub_year for pub in publications],
    #     'Author(s)': [pub.alt_people_text for pub in publications],
    #     'Title': [pub.name for pub in publications],
    #     'Journal': [pub.pub_journal for pub in publications]
    # }
    # df = pd.DataFrame(data)

    # Create an HTTP response with the CSV file
    response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = f'attachment; filename="publications_{year}.csv"'

    # Write the DataFrame to CSV
    # df.to_csv(path_or_buf=response, index=False)

    return response



# from wagtail.contrib.modeladmin.options import ModelAdmin
# from .models import Person

# class PersonAdmin(ModelAdmin):
#     model = Person
#     list_display = ('first_name', 'last_name')
	
from django.http import HttpResponseRedirect
from django.urls import reverse



def login_view(request):
    return HttpResponseRedirect(reverse('social:begin', args=['azuread-tenant-oauth2']))


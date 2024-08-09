from django import forms



class JobSearchForm(forms.Form):
    job_name = forms.CharField(
        label='Job Title',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),required=False
    )
    location = forms.CharField(
        label='Location',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),required=False
    )


class JobSearchTechnoparkForm(forms.Form):
    job_name = forms.CharField(
        label='Job Title',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter job title'}),required=False
    )
    company = forms.CharField(
        label='Company Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),required=False
    )
   
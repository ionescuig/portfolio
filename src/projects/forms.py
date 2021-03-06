from django import forms

from .models import Project, Images, CV


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'description_more', 'technologies', 'position', 'link_host', 'link_github', 'visible']
        error_messages = {
            'title': {
                'unique': 'Title already exists!'
            },
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['technologies'].widget.attrs['placeholder'] =\
            'Separate items by comma, include "-" for version. Ex: python-3.6,django-2.1,html-,css-'
        self.fields['link_host'].widget.attrs['placeholder'] = 'https://www.example.com'
        self.fields['link_github'].widget.attrs['placeholder'] = 'https://www.example.com'

        # make a list of available positions
        total_projects = Project.objects.all().count()
        titles_list = list(Project.objects.all().values_list('title', flat=True).order_by('position'))
        choices_titles_list = []
        for elem in titles_list:
            choices_titles_list.append('%s: %s' % (Project.objects.values_list('position', flat=True).get(title=elem),
                                                   elem))
        # check if existing project
        if not self.instance.position:
            position_list = [x for x in range(1, total_projects+2)]
            choices_titles_list += ['%s: New Project' % (total_projects + 1)]
        else:
            position_list = [x for x in range(1, total_projects+1)]

        # the form position will a ChoiceField
        # offer the choice to pick from list of projects
        choices = map(lambda x, y: (x, y), position_list, choices_titles_list)
        self.fields['position'] = forms.ChoiceField(choices=choices, required=True)

        # check if existing or new project
        # for new project, initial position will be the no of project + 1
        if not self.instance.position:
            self.initial['position'] = total_projects + 1


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = '__all__'

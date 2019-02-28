from django import forms
from.models import Project, Images, CV


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'position', 'link_host', 'link_github']
        error_messages = {
            'title': {
                'unique': 'Title already exists!'
            },
        }

    def __init__(self, *args, **kwargs):
        # make a list of available positions for the new project
        total_projects = Project.objects.all().count()
        position_list = [x for x in range(1, total_projects+2)]
        titles_list = list(Project.objects.all().values_list('title', flat=True).order_by('position'))

        choices_titles_list = []
        for elem in titles_list:
            choices_titles_list.append('%s: %s' % (Project.objects.values_list('position', flat=True).get(title=elem),
                                                   elem))
        choices_titles_list += ['%s: New Project' % (total_projects + 1)]

        choices = map(lambda x, y: (x, y), position_list, choices_titles_list)

        # update the position field with the new list
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['position'] = forms.ChoiceField(choices=choices, required=True)
        self.initial['position'] = total_projects + 1


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']


class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = '__all__'

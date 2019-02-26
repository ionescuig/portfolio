from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, TemplateView
from django.shortcuts import render

from .forms import CVForm, ImagesForm, ProjectForm
from .models import CV, Images, Project


class LandingView(TemplateView):
    template_name = 'projects/underconstruction.html'


@login_required
def createproject(request):
    image_form_set = modelformset_factory(Images, form=ImagesForm, extra=6)
    # 'extra' means the number of photos that you can upload     ^

    if request.method == 'POST':
        # create new project
        projectForm = ProjectForm(request.POST)
        formset = image_form_set(request.POST, request.FILES, queryset=Images.objects.none())

        if projectForm.is_valid() and formset.is_valid():
            project_form = projectForm.save(commit=False)
            project_form.user = request.user
            project_form.save()

            for form in formset.cleaned_data:
                # this helps not to crash if the user do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(project=project_form, image=image)
                    photo.save()
            messages.success(request, 'Project saved!!!')
            return HttpResponseRedirect('/')
        else:
            print(projectForm.errors, formset.errors)
    else:
        projectForm = ProjectForm()
        formset = image_form_set(queryset=Images.objects.none())
    return render(request, 'projects/create_project.html', {'projectForm': projectForm, 'formset': formset})

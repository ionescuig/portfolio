from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, Http404
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView, DetailView, ListView, View
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import CVForm, ImagesForm, ProjectForm
from .models import CV, Images, Project


class HomeView(TemplateView):
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

            # update positions for projects starting with the new project's desired position
            position = project_form.position
            total_positions = Project.objects.all().count()
            if position <= total_positions:
                projects_for_update = Project.objects.filter(position__gte=position)
                for proj in projects_for_update:
                    proj.update_position(1)

            project_form.save()

            for form in formset.cleaned_data:
                # this helps not to crash if the user do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(project=project_form, image=image)
                    photo.save()
            messages.success(request, 'Project saved!!!')
            return HttpResponseRedirect('/projects/')
        else:
            print(projectForm.errors, formset.errors)
    else:
        projectForm = ProjectForm()
        formset = image_form_set(queryset=Images.objects.none())
    return render(request, 'projects/project_create.html', {'projectForm': projectForm, 'formset': formset})


class DetailProjectView(DetailView):
    form_class = ProjectForm
    template_name = 'projects/project_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(DetailProjectView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        return Project.objects.all()


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    form_class = ProjectForm
    template_name = 'projects/project_update.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UpdateProjectView, self).get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        return Project.objects.all()


class ListProjectView(ListView):
    def get_queryset(self):
        return Project.objects.all().order_by('position')


class DeleteProjectView(LoginRequiredMixin, DeleteView):
    template_name = 'projects/project_delete.html'
    success_url = reverse_lazy('projects:project_list')

    def get_object(self, queryset=None):
        obj = super(DeleteProjectView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_queryset(self):
        return Project.objects.all()


class DeleteImageView(LoginRequiredMixin, DeleteView):
    template_name = 'projects/image_delete.html'
    success_url = reverse_lazy('projects:project_list')
    # success_url = reverse_lazy('projects:project_detail', kwargs={'slug': slug})

    def get_object(self, queryset=None):
        obj = super(DeleteImageView, self).get_object()
        print('>>> path: ', obj.image.path)
        return obj

    def get_context_data(self, **kwargs):
        context = super(DeleteImageView, self).get_context_data()
        print(context)
        return context

    def get_queryset(self):
        return Images.objects.all()

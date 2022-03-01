from django.shortcuts import (render, redirect)
from apps.store import models
from apps.user import forms


def index(request):
    reviews = models.Review.objects.all().order_by('pk')[:10]
    recipes = models.Recipe.objects.all()
    botanicals = models.Botanical.objects.all()

    form = forms.ContactForm(request.POST)
    context = dict(reviews=reviews, recipes=recipes, form=form, botanicals=botanicals)
    if request.method == 'POST':
        if not form.is_valid():
            context['form'] = form
            render(request, 'base.html', context=context)
        else:
            _ = form.save()
            form.send_email()
            return redirect('/')

    return render(request, 'base.html', context=context)

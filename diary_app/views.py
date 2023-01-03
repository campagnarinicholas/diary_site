from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, TemplateView
from django.http import HttpResponseRedirect
from .models import EntryType, Entry
from .forms import EntryTypeForm, EntryForm
from .tables import EntryTable
from django.utils import timezone

signin_url = 'diary_app:signin'

def signup(request):
    if request.user.is_authenticated:
        return redirect('diary_app/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            #login(request, user)
            return redirect('../')
        else:
            return render(request, 'diary_app/signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'diary_app/signup.html', {'form': form})

def signin(request):
    if request.user.is_authenticated:
        return render(request, 'diary_app/index.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/diary_app')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'diary_app/signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'diary_app/signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('../')

# Home page
@login_required(login_url='./signin')
def home(request):
    entry_types = EntryType.objects.filter(user=request.user)
    entries = [ Entry.objects.filter(entry_type=entry_type) for entry_type in entry_types ]
    
    return render(request, 'diary_app/home.html', {'entry_types':entry_types, 'entries':entries})

@login_required(login_url=signin_url)
def stopwatch(request, pk):
    entry_type = EntryType.objects.get(pk=pk)
    return render(request, 'diary_app/stopwatch.html', {"entry_type": entry_type})

@login_required(login_url=signin_url)
def send_stopwatch_time(request, pk, seconds):
    entry_type = EntryType.objects.get(pk=pk)
    length_in_hours = seconds / 60 / 60
    entry = Entry(started_at=timezone.now(), length=length_in_hours, entry_type=entry_type)
    entry.save()

    return render(request, 'diary_app/stopwatch.html', 
    {
        "entry_type": entry_type,
        "entry_created": entry
    }
    )

@login_required(login_url='./signin')
def entry_list(request):
    # Filter for relevant entry_types
    entry_types = EntryType.objects.filter(user=request.user)
    table = EntryTable(Entry.objects.filter(entry_type__in=list(entry_types)))

    return render(request, "diary_app/entry_list.html",
    {
        "table": table
    })

@login_required(login_url='./signin')
def entry_type_entry_list(request, pk):
    # Only show entries from this entry_type
    entry_type = EntryType.objects.get(user=request.user, pk=pk)
    entries = Entry.objects.filter(entry_type=entry_type)

    # Get relevant info from entries such as average
    total = sum(entry.length for entry in entries)
    entries_this_week = [entry for entry in entries if (timezone.now() - entry.started_at).days < 7]
    day_sums = []
    dates = []
    for i in range(0, 8):
        date = timezone.now() - timezone.timedelta(i)
        entry_length_on_day_i = [entry.length for entry in entries_this_week if abs(date - entry.started_at) <= timezone.timedelta(.5) ]
        dates.append(f"{date.month}-{date.day}")
        day_sum = sum(entry_length_on_day_i)
        day_sums.append(day_sum)
    sessions_this_week = len(entries_this_week)
    hours_this_week = sum(entry.length for entry in entries_this_week)
    if(sessions_this_week > 0):
        weekly_avg_length = round(hours_this_week / sessions_this_week, 1)
    else:
        weekly_avg_length = 0

    table = EntryTable(entries)

    return render(request, "diary_app/entry_type_entry_list.html",
    {
        "table": table,
        "total": total,
        "type_pk": pk,
        "weekly_avg_length": weekly_avg_length,
        "sessions_this_week": sessions_this_week,
        "hours_this_week": hours_this_week,
        "entry_type": entry_type,
        "day_sums": day_sums,
        "dates": dates
    })

@login_required(login_url='./signin')
def delete_entry(request, pk):
    entry = Entry.objects.filter(pk=pk)
    entry.delete()

    next = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(next)

class EntryTypeCreateView(CreateView):
    "View for creating a MyModel belonging to the current user."
    model = EntryType
    form_class = EntryTypeForm
    success_url = '../'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(EntryTypeCreateView,
                        self).get_form_kwargs(*args, **kwargs)
        # Pass the current user to the form constructor
        form_kwargs['user'] = self.request.user
        return form_kwargs

class EntryTypeDetailView(DetailView):
    model = EntryType
    template_name = 'diary_app/entry_type.html'

class EntryTypeListView(ListView):
    model = EntryType
    template_name = 'diary_app/entry_list.html'

class EntryCreateView(CreateView):
    "View for creating a MyModel belonging to the current user."
    model = Entry
    form_class = EntryForm
    success_url = '../'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(EntryCreateView,
                        self).get_form_kwargs(*args, **kwargs)
        # Pass the current user to the form constructor
        form_kwargs['user'] = self.request.user
        form_kwargs['pk'] = self.kwargs.get('pk')
        return form_kwargs

    def get_initial(self):
        pk = self.kwargs.get('pk')
        return self.form_class.get_initial( pk )

class EntryListView(ListView):
    model = Entry
    template_name = 'diary_app/entry_list.html'

class EntryTypeChartView(TemplateView):
    template_name = 'diary_app/entry_type_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context["entries"] = Entry.objects.filter(entry_type__id=pk)
        return context

class EntryChartView(TemplateView):
    template_name = 'diary_app/entries_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry_type_set = EntryType.objects.filter(user=self.request.user)
        entry_types, entry_lengths = [], []
        for entry_type in entry_type_set:
            entry_types.append(entry_type.name)
            entries = Entry.objects.filter(entry_type=entry_type)
            size = 0
            for entry in entries:
                size += entry.length
            entry_lengths.append( size )

        context["entry_type_names"] = entry_types
        context["entry_lengths"] = entry_lengths
        
        entry_types = EntryType.objects.filter(user=self.request.user)
        context['entry_types'] = entry_types

        return context
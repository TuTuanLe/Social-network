from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Relationship
from .forms import ProfileModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
import networkx as nx
# Create your views here.

@login_required
def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/myprofile.html', context)

@login_required
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {
        'qs': results,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)

@login_required
def accept_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profiles:my-invites-view')

@login_required
def reject_invatation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles:my-invites-view')

@login_required
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    qs2 = User.objects.all()
    context = {'qs': qs,'qs2': qs2}

    return render(request, 'profiles/to_invite_list.html', context)

@login_required
def profiles_list_view(request):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)    
        qs2 = User.objects.all()
        qsdegree =[]
        data =[]
        direction=[]
        print(data)
        for i in qs2:
            temp = i.id +1
            usera = Profile.objects.get(id=temp)
            print(temp,"  ",i.username,"  ")
            print("\t============== list user no friends =================")
            user_accept= Profile.objects.get_all_friend_accepted(usera.user)
            for user_ac in user_accept:
                print("\t\t",user_ac.id ,"  ",user_ac.user)
                direction.append(temp)
                direction.append(user_ac.id)
                data.append(direction)
                direction=[]

            print("\t============== list user send =======================")
            user_send= Profile.objects.get_all_friend_send(usera.user)
            for user_as in user_send:
                print("\t\t",user_as.id ,"  ",user_as.user)
                direction.append(temp)
                direction.append(user_as.id)
                data.append(direction)
                direction=[]
        
        df=  pd.DataFrame(data)
        print(df)
        us_graph = nx.from_pandas_edgelist(df, source=0,target=1,create_using=nx.DiGraph)
        degree =  nx.closeness_centrality(us_graph)
        print('closeness_centrality ', degree)
        for i in sorted(degree, key = degree.get, reverse=True):
            print(i, degree[i])
            if int(i) != int(self.request.user.id) +1:
                qsdegree.append(Profile.objects.get(id=i))

        print("2222222222222222",self.request.user.id)
        print(qsdegree)
        
        # print(qs)
        return qsdegree

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail.html'

    # def get_object(self):
    #     slug = self.kwargs.get('slug')
    #     profile = Profile.objects.get(slug=slug)
    #     return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context

class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        print(qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

@login_required
def send_invatation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')
    
@login_required
def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile-view')


    
    

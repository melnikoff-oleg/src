from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from users.models import CustomUser, Survey, Chat3, Problem
from django.utils.safestring import mark_safe
import json

# Create your views here.

def index(request):
    # Отрисовка HTML-шаблона index.html с данными внутри 
    return render(
        request,
        'index.html',
        context = {'data' : 'ok'},
    )

def wrapper(request):
    return render(
        request,
        'wrapper.html',
        context = {'data' : 'ok'},
    )

class QuestionRate():
    def __init__(self, question, rate):
        self.question = question
        self.rate = rate

class SurveyToPrint():
    def __init__(self, survey):
        self.pk = survey.pk

        self.question_rates = []
        rate = survey.rate
        p = ['Оцените от 1 до 10 качество предоставленного вам в аренду помещения', 'Оцените от 1 до 10 комфортность и лёгкость выполнения условий заключённого контракта по аренде', 'Оцените от 1 до 10 вероятность что вы работали бы с этим арендодателем, если бы заранее знали что дела будут идти так как идут', 'Оцените от 1 до 10 соотношение цена/качество предоставленного вам в аренду помещения', ' Оцените от 1 до 10 степень вежливости и открытости вашего арендодателя', 'Оцените от 1 до 10 насколько в целом Вы довольны нынешним положением дел', 'Оцените от 1 до 10 качество коммуникаций', 'Оцените от 1 до 10 вероятность того, что Вы порекомендуете другу арендовать помещение в вашем ТЦ', 'Оцените от 1 до 10 насколько арендованная площадь оправдала ваши ожидания', 'Оцените от 1 до 10 охраняемость ТЦ']
        for i in range(10):
            self.question_rates.append(QuestionRate(p[9 - i], rate % 10 + 1))
            rate //= 10
        self.question_rates.reverse()

def account(request):

    if 'problem' in request.POST.keys():
        problem = Problem()
        problem.text = request.POST.get('problem')
        problem.save()

    if 'review_fict' in request.POST.keys():
        survey_pk = int(request.POST.get('pk'))
        survey = Survey.objects.get(pk=survey_pk)
        survey.review = request.POST.get('review_fict')
        survey.save()

    if 'rate_fict' in request.POST.keys():
        survey_pk = int(request.POST.get('pk'))
        survey = Survey.objects.get(pk=survey_pk)
        survey.rate = int(request.POST.get('rate_fict', 10))
        survey.save()

    user = request.user
    list_of_surveys = request.user.surveys.all()
    a = len(list_of_surveys) + 1
    a //= 2
    b = len(list_of_surveys) - a
    first_part = []
    for i in range(a):
        first_part.append(list_of_surveys[i])
    second_part = []
    for i in range(a, a + b):
        second_part.append(list_of_surveys[i])
    
    all_surveys_to_print = []
    for i in list_of_surveys:
        all_surveys_to_print.append(SurveyToPrint(i))

    if 'password' in request.POST.keys():
        user.set_password(request.POST.get('password'))

    user.save()
    return render(
        request,
        'account.html',
        context = {'account': True, 'first_part': first_part, 'second_part': second_part, 'all_surveys_to_print': all_surveys_to_print},
    )

def reviews(request, id):
    id = int(id)
    landlord = CustomUser.objects.get(pk=id)
    surveys = landlord.surveys.all()
    all_reviews = []
    for i in surveys:
        all_reviews.append(i.review)
    clients = landlord.clients.all()
    
    a = len(all_reviews) + 1
    a //= 2
    b = len(all_reviews) - a
    first_part = []
    for i in range(a):
        first_part.append(all_reviews[i])
    second_part = []
    for i in range(a, a + b):
        second_part.append(all_reviews[i])
    return render(
        request,
        'reviews.html',
        context = {'account': False, 'landlord': landlord, 'first_part': first_part, 'second_part': second_part},
    )

def chats_moderator(request):
    return render(
        request,
        'chats_moderator.html',
        context = {'account': False, 'data' : 'ok'},
    )

def account_moderator(request):
    user = request.user
    if 'review_fict' in request.POST.keys():
        survey_pk = int(request.POST.get('pk'))
        survey = Survey.objects.get(pk=survey_pk)
        survey.review = request.POST.get('review_fict')
        survey.is_accepted = True
        deleting = request.POST.get('deleting', 'false')
        if deleting == 'true':
            survey.customuser_set.clear()
        survey.save()

    list_of_surveys_with_done = request.user.surveys.all()
    list_of_surveys = []
    for i in list_of_surveys_with_done:
        if not i.is_accepted:
            list_of_surveys.append(i)
    a = len(list_of_surveys) + 1
    a //= 2
    b = len(list_of_surveys) - a
    first_part = []
    for i in range(a):
        first_part.append(list_of_surveys[i])
    second_part = []
    for i in range(a, a + b):
        second_part.append(list_of_surveys[i])
    
    all_surveys_to_print = []
    for i in list_of_surveys:
        all_surveys_to_print.append(SurveyToPrint(i))

    if 'password' in request.POST.keys():
        user.set_password(request.POST.get('password'))

    user.save()
    return render(
        request,
        'account_moderator.html',
        context = {'account': True, 'first_part': first_part, 'second_part': second_part, 'all_surveys_to_print': all_surveys_to_print},
    )

def chat_members(request, id):
    id = int(id)
    landlord = CustomUser.objects.get(pk=id)

    clients = landlord.clients.all()
    renters = []
    for i in clients:
        if i.is_renter:
            renters.append(i)
        else:
            moderator = i
    return render(
        request,
        'chat_members.html',
        context = {'account': False, 'landlord': landlord, 'moderator': moderator, 'renters': renters},
    )

def chats_test(request):
    user = request.user
    if user.is_moderator:
        return chats_moderator(request)
    if user.is_first:
        user.is_first = False
        user.save()
        return render(request, 'survey.html')
    review = request.POST.get('review', '')
    if review != '':
        user.name = request.POST.get('rate_fict', 10)
        surveys = user.surveys.all()
        if len(surveys) > 0:
            anketa = surveys[0]
            anketa.review = review
            anketa.rate = request.POST.get('rate_fict', 10)
            anketa.save()
        else:
            anketa = Survey()
            anketa.review = review
            anketa.rate = request.POST.get('rate_fict', 10)
            anketa.save()
            user.surveys.add(anketa)
        user.save()
    return render(request, 'chats_test.html', context = {'account': False, 'data' : 'ok'})

def survey(request):
    return render(
        request,
        'survey.html',
        context = {'data' : 'ok'},
    )

def chats(request):
    user = request.user
    #пришел со страницы входа
    if request.POST['from'] == 'login':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
        else:
            # Return an 'invalid login' error message.
            return render(
                request,
                'index.html',
                context = {'data' :  mark_safe(json.dumps('invalid'))}
                )
    
    if user is not None:
        if len(user.surveys.all()) == 0:
            if(request.POST['from'] == 'login'):
                return redirect("http://127.0.0.1:8000/questionnaire/")
            #заполнил анкету и отправляет ее нам
            else:
                return register_survey(request)
        else:
            return chatspage(request, user)


@login_required
def register_survey(request):
    user = request.user
    survey = Survey.objects.create(
        user_pk = user.pk,
        landlord_pk = request.POST['landlord_pk'],
        placementValue =  request.POST['placementValue'],
        contractConditionsValue =  request.POST['contractConditionsValue'],
        futureParthershipValue =  request.POST['futureParthershipValue'],
        qualityValue =  request.POST['qualityValue'],
        politenessValue =  request.POST['politenessValue'],
        currentSituationValue =  request.POST['currentSituationValue'],
        communicationValue =  request.POST['communicationValue'],
        recommendationValue =  request.POST['recommendationValue'],
        expectationsValue = request.POST['expectationsValue'],
        safetyValue =  request.POST['safetyValue'],
        review = request.POST['review'],
    ) 
    user.surveys.add(survey)

    return chatspage(request, user)

@login_required
def chatspage(request, user):
    chats_list = []
    if user.is_renter:
        for landlord in user.clients.all():
            chat = landlord.chat3
            #А если чат не нашелся???
            chat_size = len(chat.users.all())
            chats_list.append({ 'chat_name' : chat.name, 'chat_pk': chat.pk, 'landlord_pk' : landlord.pk, 'chat_size' : chat_size})
        #print(chats_list)
        return render(
            request,
            'chats.html', 
            context = {'chats_list' : chats_list, 'username' : user.name}
        )

@login_required
def survey(request):
    #нужно передавать pk (имя) арендатора, которое будет отображаться в верху анкеты
    user = request.user
    landlord = user.clients.all()[0]
    return render(
        request,
        'questionnaire.html', context={'landlord_name' : landlord.name}
    )

# {% for key in {{chat}}.keys() %}
#     {if {{key}} == "chat_name" %}
#         <h3>{{value}}</h3>
#     {% endif %}
#     {if {{chat[key]}} == "chat_size" %}
#         <span>{{value}} арендатора, ?? в чате</span>
#     {% endif %}
# {% endfor %}

# @login_required
# def room(request, user_pk):
#     our_user = request.user
#     list = []
#     for chat in our_user.chats.all():
#         list.append( { 'name': chat.name, 'pk' : chat.pk } )
#     return render(request, 'chat/room.html', {
#         'user_pk' : mark_safe(json.dumps(user_pk)),
#         'email' : mark_safe(json.dumps(request.user.email)),
#         'chats' : mark_safe(json.dumps(list))
#     })
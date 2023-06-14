import requests
from pathlib import Path
from shutil import rmtree
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from PIL import Image
from .forms import *
import qrcode
from django.db.models import Avg
import plotly.graph_objs as go
import pandas as pd
from django.core.files import File
from io import BytesIO
from django.contrib.auth.models import User
from segno import helpers
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic  import UpdateView, DeleteView


def read_png(cartoon,model,number):
    try:
        cartoon_vxod = r'C:\Users\79045\Desktop\python\Sber_otzov\SBER_OT\otzovik\media\shab\vixod.png'
        org_img = Image.open(cartoon_vxod)
        org_img_vxod = Image.open(cartoon)
        org_img_vxod = org_img_vxod.resize((470, 470))
        result = Image.new("RGBA", (org_img.size), (0, 0, 0, 0))
        result.paste(org_img, (0, 0))
        result.paste(org_img_vxod, (50, 100))
        result.save(f'media/qr_codes/{model}_{number}.png')

    except IOError:
        print('Couldn\'t read {}'.format(cartoon))

def dashboard(request, number):
    # Получение данных из базы данных
    anketa = Anketa.objects.get(user=request.user)
    opros_data = Opros.objects.filter(number=number).values()


    #df = pd.DataFrame.from_records(opros_data)

    # Рассчет средней арифметической оценки по каждому критерию
    avg_number1 = Opros.objects.filter(number=number).aggregate(avg=Avg('number1'))['avg']
    avg_number2 = Opros.objects.filter(number=number).aggregate(avg=Avg('number2'))['avg']
    avg_number3 = Opros.objects.filter(number=number).aggregate(avg=Avg('number3'))['avg']
    avg_number4 = Opros.objects.filter(number=number).aggregate(avg=Avg('number4'))['avg']
    avg_number5 = Opros.objects.filter(number=number).aggregate(avg=Avg('number5'))['avg']

    # Рассчет общего рейтинга автомобиля

    total_rating = (avg_number1 + avg_number2 + avg_number3 + avg_number4 + avg_number5) / 5


    # Создание визуализаций
    fig = go.Figure()

    # Добавление графиков или других элементов в дашборд
    fig.add_trace(go.Bar(x=[f'{anketa.number1}'], y=[avg_number1], name=f'{anketa.number1}'))
    fig.add_trace(go.Bar(x=[f'{anketa.number2}'], y=[avg_number2], name=f'{anketa.number2}'))
    fig.add_trace(go.Bar(x=[f'{anketa.number3}'], y=[avg_number3], name= f'{anketa.number3}'))
    fig.add_trace(go.Bar(x=[f'{anketa.number4}'], y=[avg_number4], name=f'{anketa.number4}'))
    #fig.add_trace(go.Bar(x=[f'{anketa.number5}'], y=[avg_number5], name=f'{anketa.number5}'))
    fig.add_trace(go.Bar(x=['Общий рейтинг'], y=[total_rating], name='Общий рейтинг'))

    # Настройка макета дашборда
    fig.update_layout(
        title='Дашборд автомобиля ' + number,
        xaxis_title='Критерий',
        yaxis_title='Оценка',
        barmode='stack'
    )

    # Преобразование графика в HTML-код
    div = fig.to_html(full_html=False)

    # Отображение дашборда на веб-странице
    return div
def delete_all_anketas(request):
    Anketa.objects.filter(user = request.user).delete()
    return redirect('home')
class TransportUpdateView(UpdateView):
    model = Transport
    template_name = 'transport_update.html'
    form_class = TransportForm

class TransportDeleteView(DeleteView):
    model = Transport
    success_url = '/transport/'
    template_name = 'transport_delete.html'

class HomeUpdateView(UpdateView):
    model = Anketa
    template_name = 'home_update.html'
    success_url = ''
    form_class = AnketaForm

class HomeDeleteView(DeleteView):
    model = Opros
    success_url = '/'
    template_name = 'home_delete.html'
class PersonalUpdateView(UpdateView):
    model = Personal
    template_name = 'personal_update.html'
    success_url = '/personal'
    form_class = PersonalForm

class PersonalDeleteView(DeleteView):
    model = Personal
    success_url = '/personal'
    template_name = 'personal_delete.html'
try:
    P=[Opros.objects.values_list('number', flat=True).distinct()[0]]
except:
    P=[]
@login_required
def home(request):
    global P
    numbers = Opros.objects.values_list('number', flat=True).distinct()


    if request.method == 'POST':
        num = request.POST.get("num")

        P=[]
        if num in Transport.number:
            P.append(num)
        else:
            pass
        form = AnketaForm(request.POST)
        if form.is_valid():
            try:
                user = request.user
                number1 = form.cleaned_data['number1']
                number2 = form.cleaned_data['number2']
                number3 = form.cleaned_data['number3']
                number4 = form.cleaned_data['number4']
                number5 = form.cleaned_data['number5']
                dop1 = form.cleaned_data['dop1']
                dop2 = form.cleaned_data['dop2']
                dop3 = form.cleaned_data['dop3']
                dop4 = form.cleaned_data['dop4']
                dop5 = form.cleaned_data['dop5']
                Anketa.objects.create(user=user,
                                      number1=number1,
                                      number2=number2,
                                      number3=number3,
                                      number4=number4,
                                      number5=number5,
                                      dop1 = dop1,
                                      dop2 = dop2,
                                      dop3 = dop3,
                                      dop4 = dop4,
                                      dop5 = dop5,
                                    )
            except:
                return redirect('home')
            return redirect('home')
    else:
        form = AnketaForm()
    if len(P)!=0 and None not in P:
        dashboard_html = dashboard(request, P[0])
    else:
        dashboard_html = None
    anketa = Anketa.objects.filter(user=request.user)
    opros = Opros.objects.filter(user=request.user)

    return render(request, 'home.html', {
        'form': form,
        'anketa': anketa,
        'opros': opros,
        'dash': dashboard_html,
        'numbers': numbers,

    })


@login_required
def transport(request):
    qr_image = True
    if request.method == 'POST':
        form = TransportForm(request.POST)
        if form.is_valid():
            user = request.user
            model = form.cleaned_data['model']
            number = form.cleaned_data['number']
            #qrcode = helpers.make_mecard(user, reading=None, email=None, phone=None, videophone=None, memo=None, nickname=None, birthday=None, url="https://metanit.com/python/recipes/4.1.php", pobox=None, roomno=None, houseno=None, city=None, prefecture=None, zipcode=None, country=None)            #qrcode = segno.make_qr("https://metanit.com/python/recipes/4.1.php")            qr_image = True            url = "http://127.0.0.1:8000/anketa/"            otzov_by = f'{user},{number}'            qr = qrcode.QRCode(version=1,                error_correction=qrcode.constants.ERROR_CORRECT_L,                box_size=10,                border=4,            )
            qr_image = True
            url = "http://127.0.0.1:8000/anketa/"
            otzov_by = f'{user},{number}'
            data = url + "?otzov_by=" + otzov_by
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            data = url + "?otzov_by=" + otzov_by
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(f'media/qr/{model}_{number}.png')
            img = f'media/qr/{model}_{number}.png'
            read_png(img,model,number)

            #img_norm = (f'media/qr/{model}_{number}.png')

            Transport.objects.create(user=user,                                     model=model,                                     number=number,                                     image=f'../media/qr_codes/{model}_{number}.png'                                     )
            # for path in Path('media/qr').glob('*'):            #   if path.is_dir():            #       rmtree(path)            #   else:            #       path.unlink()            return redirect('transport')
    else:
        form = TransportForm()
    transport = Transport.objects.filter(user=request.user)
    return render(request, 'transport.html', {'form': form, 'transport': transport})
@login_required
def personal(request):
    if request.method == 'POST':
        form = PersonalForm(request.POST)
        # print(form.data)
        # user1 = request.user
        # print(user1)
        if form.is_valid():
            # try:
            user = request.user
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            job = form.cleaned_data['job']
            date_of_dirth = form.cleaned_data['date_of_dirth']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']

            Personal.objects.create(user=user,
                                    name=name,
                                    last_name=last_name,
                                    email=email,
                                    job=job,
                                    date_of_dirth=date_of_dirth,
                                    phone=phone
                                    )

            return redirect('personal')
            # except:
            # form.add_error(None, 'Ошибка добавления поста')
    else:
        form = PersonalForm()
    personal = Personal.objects.filter(user=request.user)

    return render(request, 'personal.html', {'form': form, 'personal': personal})


def anketa(request):
    url_referer = request.META.get('QUERY_STRING')
    url_referer = url_referer
    a = url_referer.find('=')
    b = url_referer.find(',')
    user = url_referer[a+1:b]
    username = user
    number = url_referer[b+1::]
    #user = 'Andrew'
    if request.method == 'POST':
        number = request.POST.get('number')
        otzov_by = request.POST.get('otzov_by')

        form = OprosForm(request.POST)
        # print(form.data)
        # user1 = request.user
        # print(user1)
        if form.is_valid():
            # try:
            text = form.cleaned_data['text']
            number1 = form.cleaned_data['number1']
            number2 = form.cleaned_data['number2']
            number3 = form.cleaned_data['number3']
            number4 = form.cleaned_data['number4']
            number5 = form.cleaned_data['number5']

            #user = url_referer[a + 1:b]


            Opros.objects.create(text=text,
                                 number1 = number1,
                                 number2 = number2,
                                 number3 = number3,
                                 number4 = number4,
                                 number5 = number5,
                                 number = number,
                                 user=otzov_by
                                 )
            return redirect('bay')
            # except:
            # form.add_error(None, 'Ошибка добавления поста')
    else:
        otzov_by = username
        number = number
        form = OprosForm()
    opros = Opros.objects.filter(user = user)
    anketa = Anketa.objects.filter(user = user)
    return render(request, 'anketa.html', {'form': form, 'opros': opros, 'anketa': anketa, 'url': number, 'otzov_by':otzov_by, 'number':number})

@login_required
def support(request):
    return render(request, 'support.html', locals())

def bay(request):
    return render(request, 'bay.html', locals())

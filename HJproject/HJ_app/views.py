from django.shortcuts import render, redirect
from HJ_app.models import Godok, SeoulCenter, SeoulElder, SeoulPeople, SeoulHospital,\
    SeoulHospitalAd
import pandas as pd
import folium
import json
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.http.response import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
import random
UPLOAD_DIR="C:\work\psou\HJproject\HJ_app\media\images"



# Create your views here.
# def mainFunc(request):
#     godok = Godok.objects.all().values()
#     center = SeoulCenter.objects.all().values()
#     elder = SeoulElder.objects.all().values()
#     people = SeoulPeople.objects.all().values()
#
#     """
#     DB 데이터 print 확인
#     print(godok)
#     print(center)
#     print(elder)
#     print(people)
#     """
#
#     godok_df = pd.DataFrame.from_records(godok)
#     godok_df.columns = ['번호', '년도', '사망자수']
#     print(godok_df)
#
#     center_df = pd.DataFrame.from_records(center)
#     center_df.columns = ['번호', '년도', '자치구명', '노인복지관', '경로당', '노인교실']
#     print(center_df)
#
#     elder_df = pd.DataFrame.from_records(elder)
#     elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
#     print(elder_df)
#
#     people_df = pd.DataFrame.from_records(people)
#     people_df.columns = ['번호', '기간', '자치구명', '전체인구', '65세이상 노인']
#     print(people_df)
#
#     return render(request, 'main.html')


def mainFunc(request):
    map = folium.Map(location=[37.541, 126.986], zoom_start=11, tiles='cartodbpositron')

    # 독거노인
    elder = SeoulElder.objects.all().values()
    elder_df = pd.DataFrame.from_records(elder)
    elder_df.columns = ['번호', '기간', '자치구명', '기초생활수급', '저소득', '일반']
    elder_df = elder_df[elder_df.기간 == 2020]
    elder_df = elder_df[['자치구명', '기초생활수급', '저소득', '일반']]
    elder_df['합'] = elder_df.sum(axis=1)
    # print(elder_df)
    
    hospital_ad = SeoulHospitalAd.objects.order_by("?")
    print(hospital_ad) # 데이터 확인
    
    try:
        # 요양병원
        hp = SeoulHospital.objects.all().values()
        hp_df = pd.DataFrame.from_records(hp)
        #hp_df.columns = ['번호', '여부', '전화', '주소', '이름', '종류', '위도', '경도', 'url']
        hp_df.columns = ['번호', '이름', '비밀번호', '여부', '주소', '전화', '종류', '위도', '경도', 'url', '회원가입여부']
    
        # # 광고배너
        # ad = SeoulHospitalAd.objects.all().values()
        # # ad = SeoulHospitalAd.objects.all()
        # ad_df = pd.DataFrame.from_records(ad)
        # ad_df.columns = ['번호', '이름', '주소', '전화', 'url', 'image', 'comment']
        # print(ad_df)
        #
        # # 광고 표시할 병원 랜덤으로 뽑기
        # ad_list = []
        # for i in range(0, len(ad_df)): 
        #     ad_list.append(ad_df.iloc[i])
        #
        # ad_list_ran = random.sample(ad_list, 1)
        # print(ad_list_ran, type(ad_list_ran))
        
    except Exception as e:
        print('err : ', e)

    # 서울 행정구
    with open('C:\ACON\Pywork\psou\HJproject\geo.json', mode='rt', encoding='utf-8') as f:
        geo = json.loads(f.read()) # json 파일 로드
        f.close()

    folium.Choropleth(
        geo_data = geo,
        data = elder_df, 
        columns=('자치구명', '합'), 
        key_on='feature.properties.name',
        fill_color='PuBu',
        legend_name='독거노인 인구수',
    ).add_to(map)

    # 구별 테두리
    folium.GeoJson(geo).add_to(map)

 
    # 마커 표시
    
    for i in range(0, len(hp_df)):
        popup = folium.Popup("<i><a href="+hp_df['url'][i]+">"+hp_df['이름'][i]+"</a></i>", max_width=300)
        icon = folium.Icon(color = 'lightred', icon = 'glyphicon glyphicon-plus')
        folium.Marker([hp_df['위도'][i], hp_df['경도'][i]], popup = popup, icon = icon).add_to(map)

    maps = map._repr_html_()

    # 로그인 세션 받기
    h_name = request.session.get('login')
    
    
    # return render(request, 'main.html', {'m' : maps, 'login' : h_name})
    return render(request, 'main.html', {'m' : maps, 'login' : h_name, 'ad' : hospital_ad})

# 병원 등록
def RegisteredFunc(request): 
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    elif request.method == 'POST':
        h_name = request.POST.get('h_name')
        h_pass = request.POST.get('h_pass')
        h_open = request.POST.get('h_open')
        h_addr = request.POST.get('h_addr')
        h_tel = request.POST.get('h_tel')
        h_kind = request.POST.get('h_kind')
        h_url = request.POST.get('h_url')
        SeoulHospital(
            h_name=h_name,
            h_pass=h_pass,
            h_open = h_open,
            h_addr = h_addr,
            h_tel = h_tel,
            h_kind = h_kind,
            h_wi = 84.416992,
            h_kung = 116.583585,
            h_url = h_url,
            is_confirmed = 0
        ).save()
        return render(request, 'create_hospital_done.html')

# 로그인 
def LoginFunc(request):
    if request.method == 'GET':
        return render(request, 'loginF.html')
    
    elif request.method == 'POST':
        context = {}
        try:
            h_n = request.POST.get('h_name')
            h_p = request.POST.get('h_pass')
            
            if SeoulHospital.objects.get(h_name=h_n, h_pass=h_p):
                hpt = SeoulHospital.objects.get(h_name=h_n, h_pass=h_p)
            
                if hpt: # 회원인 병원
                    if hpt.is_confirmed == 1: # 회면이면서 허가 받은 병원                    
                        request.session['login'] = hpt.h_name
                        return redirect('/')
                    else: # 회원이면서 허가 받지 못 한 병원
                        context['error'] = "아직 허가되지 않은 병원입니다.\
                        조금만 더 대기해주세요!"
                        return render(request, 'create_hospital_done.html', {'context' : context})
                
        except:
            context = "비밀번호가 같지 않거나, 등록되지 않은 병원입니다. 회원가입 신청 부탁드립니다."
            return render(request, 'loginF.html', {'context' : context})
        
def LogoutFunc(request):
    if 'login' in request.session: 
        del request.session['login'] 
        return redirect('/')

def adFFunc(request):
    if request.method == 'GET':
        if 'login' in request.session:
            h_name = request.session.get('login')
            hpt = SeoulHospital.objects.get(h_name=h_name)
        return render(request, 'adF.html', {'hpt' : hpt})
    #and request.FILES.get['h_image']
    elif request.method == 'POST' :
        h_name = request.POST.get('h_name')
        h_addr = request.POST.get('h_addr')
        h_tel = request.POST.get('h_tel')
        h_url = request.POST.get('h_url')
        h_image = request.FILES.get('h_image')
        h_comment = request.POST.get('h_comment')
        print(h_name, h_addr, h_tel, h_url, h_image, h_comment)
        return redirect('/')
    
def upload_success(request):
    if request.method == 'GET':
        if 'login' in request.session:
            h_name = request.session.get('login')
            hpt = SeoulHospital.objects.get(h_name=h_name)
        return render(request, 'adF.html', {'hpt' : hpt})
    #and request.FILES.get['h_image']
    elif request.method == 'POST' :
        h_name = request.POST.get('h_name')
        h_addr = request.POST.get('h_addr')
        h_tel = request.POST.get('h_tel')
        h_url = request.POST.get('h_url')
        h_comment = request.POST.get('h_comment')
        
        if 'h_image' in request.FILES:
            h_image = request.FILES['h_image']
            fp = open("%s\%s" % (UPLOAD_DIR, h_image), 'wb+')
            for chunk in h_image.chunks():
                fp.write(chunk)
            fp.close()
        
        SeoulHospitalAd(
            h_name=h_name,
            h_addr=h_addr,
            h_tel = h_tel,
            h_url = h_url,
            h_image = h_image,
            h_comment = h_comment
        ).save()    
        
            
        print('file', h_image)
        print(h_name, h_addr, h_tel, h_url, h_comment)        
        return redirect('/')        



    
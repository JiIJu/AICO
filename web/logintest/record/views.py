from django.shortcuts import render, redirect , get_list_or_404, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Record
# from .models import Record
from .forms import RecordForm
from .newSocketServer import Communication


# client = clients[0]["ID"]
# print(client)

import datetime
from django.http import StreamingHttpResponse
from .video3 import VideoCamera
from .userdata import Userdata
# Create your views here.
# cam = VideoCamera()

# 장고 서버실행시 소켓서버 함께 실행
communication = Communication(10000)
communication.start()
clients = communication.get_clients() # [{"ID" : "aicoaicoasdas", "IP" : "192.xxx.xxx.xx"}]
cam = 0

# 메인페이지 로그인후 진입
@login_required
def main(request):
    clients = communication.get_clients()
    if clients and clients[0]['MSG']:
        context = {

            'client' : clients,
            'client2' : clients[0]['MSG'][-1],
        }
        return render(request, 'record/main.html', context)
    else:
        return render(request,'record/main.html')


# 기기관리
@login_required
def regist(request,pk):
    clients = communication.get_clients()
    try: # globals()['user_{}'.format(pk)].check:
        if clients and clients[0]['MSG']:
            context = {
                'check' : globals()['user_{}'.format(pk)].check,
                'client2' : clients[0]['MSG'][-1],
            }
        else:
            context = {
                'check' : globals()['user_{}'.format(pk)].check,
            }
    except:
        if clients and clients[0]['MSG']:
            context = {
                'check' : 0,
                'client2' : clients[0]['MSG'][-1],
            }
        else:
            context = {
                'check' : 0,
            }
    return render(request, 'record/regist.html', context)


# 영상 서버 종료
def videoclose(request, pk):
    cam.server_socket.close()
    globals()['user_{}'.format(pk)].check = 0
    return redirect('record:regist',pk=pk)


# webcam 재생함수
def video(request, pk):
    global cam
    try:
        cam = VideoCamera()
    except:
        return redirect('record:main')
    # if globals()['user_{}'.format(pk)]:
    #     globals()['user_{}'.format(pk)].check = 0
    # else:

    globals()['user_{}'.format(pk)] = Userdata()
    cam.goods = -1
    cam.bads = -1
    cam.goodp = -1
    cam.badp = -1
    cam.anss = -1
    cam.ansp = -1
    cam.data = -1
    cam.cnt0,cam.cnt1 =0,0
    cam.cnt2_0, cam.cnt2_1 = 0,0
    cam.list_s = []
    return redirect('record:regist',pk=pk)
def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def stream2(request):
    try:
        return StreamingHttpResponse(gen(()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass


bad = 0
# 실시간 운동영상 페이지
@login_required
def live(request, pk):
    clients = communication.get_clients()
    if not cam:
        return render(request,'record/regist.html')
    global bad
    bad +=1
    # 소켓ID랑 등록한 시리얼넘버가 같으면 live페이지 보여주기
    if clients and request.user.last_name == clients[0]['ID']:
    # if 'user_{}'.format(pk) in globals():
    #     print(globals()['user_{}'.format(pk)].check)
    #     if globals()['user_{}'.format(pk)].check == 1:    
        if clients[0]['MSG']:
            context = {
                'bad':bad,
                'camgoods' : cam.goods,
                'camgoodp' : cam.goodp,
                'cambads' : cam.bads,
                'camlists' : cam.list_s,
                'cambadp' : cam.badp,
                'camanss' : cam.anss,
                'camansp' : cam.ansp,
                'data':cam.data,
                'client2' : clients[0]['MSG'][-1],
            }
        else:
            context = {
                'bad':bad,
                'camgoods' : cam.goods,
                'camgoodp' : cam.goodp,
                'cambads' : cam.bads,
                'cambadp' : cam.badp,
                'camanss' : cam.anss,
                'camansp' : cam.ansp,
                'data':cam.data,
            }
        return render(request, 'record/live.html', context)
    return render(request, 'record/live.html')
    

#기록 삭제
@login_required
def delete(request, pk):
    try:
        record = get_object_or_404(Record,pk=pk)
        if record.user==request.user:
            if record:    
                record.delete()
                return redirect('record:chart')
        else:
            return redirect('record:404')
    except:
        return redirect('record:chart')


#에러 페이지
def page404(request):
    return render(request, 'record/page404.html')


# 날짜별 테이블 기록
@login_required
def chart(request):
    
    clients = communication.get_clients()
    records = list(Record.objects.all().values().order_by('-date'))
    records2 = []
    for i in records:
        if i['user_id'] == request.user.pk:
            if i['good']==0 and i['bad']==0: # b = 수행도
                b=0 
            else:
                b = 100*i['good'] / (i['good']+i['bad'])
                b = round(b,2)
            i['performance'] = b
            records2.append(i)
    if clients and clients[0]['MSG']:
        context = {
            'records2' : records2,
            'client2' : clients[0]['MSG'][-1],
        }
    else:
        context = {
            'records2' : records2,
        }
    return render(request, 'record/chart.html',context)


# 차트 기록 확인
@login_required
def totalrecord(request):
    clients = communication.get_clients()
    if clients and clients[0]['MSG']:
        context = {

            'client' : clients,
            'client2' : clients[0]['MSG'][-1],
        }
        return render(request, 'record/totalrecord.html', context)
    else:
        return render(request,'record/totalrecord.html')
# json 확인용
def jsonrecord(request):
    records = list(Record.objects.all().values().order_by('date'))
    squat = {} # 스쿼트 기록만
    pushup = {} # 푸쉬업 기록만
    lunge = {} # 런지 기록만
    myrecord = {'스쿼트':squat,'푸쉬업':pushup,'런지':lunge} # 내 기록만
    for i in records:
        if i['user_id'] == request.user.pk:
            if i['exercise'] == '스쿼트':
                cnt = squat.get(str(i['date'])) 
                if cnt:
                    squat[str(i['date'])] = cnt + i['count']
                else:
                    squat[str(i['date'])] = i['count']

            if i['exercise'] == '푸쉬업':
                cnt = pushup.get(str(i['date'])) 
                if cnt:
                    pushup[str(i['date'])] = cnt + i['count']
                else:
                    pushup[str(i['date'])] = i['count']

            if i['exercise'] == '런지':
                cnt = lunge.get(str(i['date'])) 
                if cnt:
                    lunge[str(i['date'])] = cnt + i['count']
                else:
                    lunge[str(i['date'])] = i['count']

    context = {
        'myrecord' : myrecord,
    }
    return JsonResponse(context)



# 기록 수동저장
@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    clients = communication.get_clients()
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('record:chart')
    else:
        form = RecordForm()
    if clients and clients[0]['MSG']:
        context = {
            'form': form,
            'client' : clients,
            'client2' : clients[0]['MSG'][-1],
        }
    else:
        context = {
            'form' : form,
        }
    return render(request, 'record/create.html', context)


#스쿼트(전면) 시작
def exfront(request,pk):
    global exercise_kind, bad, cam
    exercise_kind = '스쿼트'
    bad, cam.goods, cam.bads, cam.anss = 0, 0, 0, 0
    return redirect('record:live',pk=pk)

#푸쉬업(측면) 시작
def exside(request,pk):
    global exercise_kind, bad
    exercise_kind = '푸쉬업'
    bad, cam.goodp, cam.badp, cam.ansp = 0, 0, 0, 0
    return redirect('record:live',pk=pk)



#운동종료
def finish(request,pk):
    global cam, bad
    if exercise_kind == '푸쉬업':
        a = { 
            'exercise' : exercise_kind,
            'count' : cam.goodp + cam.badp,
            'time' : bad,
            'good' : cam.goodp,
            'bad' : cam.badp,
        }
    elif exercise_kind == '스쿼트':
        a = { 
            'exercise' : exercise_kind,
            'count' : cam.goods + cam.bads,
            'time' : bad,
            'good' : cam.goods,
            'bad' : cam.bads,
        }
    Record(
        exercise = a['exercise'],
        count = a['count'],
        time = a['time'],
        date = datetime.datetime.now().date(),
        good = a['good'],
        bad = a['bad'],
        user = request.user,
    ).save()
    bad, cam.goodp, cam.badp, cam.ansp = 0, 0, 0, 0
    cam.goods, cam.bads, cam.anss = 0, 0, 0
    return redirect('record:live',pk=pk)



# 데이터 자동생성
@login_required
def deepcreate(request):
    a = { 
        'exercise' : '스쿼트',
        'count' : 1,
        'time' : 0,
        'good' : 3,
        'bad' : 3,
    }
    Record(
        exercise = a['exercise'],
        time = a['time'],
        # date = datetime.datetime.now().date(),
        date =  datetime.datetime.now().date(),
        good = a['good'],
        bad = a['bad'],
        count = a['good'] + a['bad'],
        user = request.user,
    ).save()
    return redirect('record:chart')


# STT데이터 통신
# 하드웨어로 이전

# @login_required
# def test(request):
#     from google.cloud import storage

#     bucket_name = 'tts_file'    # 서비스 계정 생성한 bucket 이름 입력
#     source_blob_name = 'file.wav'    # GCP에 저장되어 있는 파일 명
#     destination_file_name = './file.wav' # 다운받을 파일을 저장할 경로("local/path/to/file")

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(source_blob_name)

#     blob.download_to_filename(destination_file_name)

#     import speech_recognition as sr

#     r = sr.Recognizer()
#     harvard = sr.AudioFile('file.wav')
#     with harvard as source:
#         audio = r.record(source)

#     data = []
#     try:
#         data.append(r.recognize_google(audio,language='ko-KR'))
#         context = {
#             'data' : data,
#         }
#     except:
#         context = {
#             'data' : 'empty',
#         }
#     return render(request, 'record/test.html',context)

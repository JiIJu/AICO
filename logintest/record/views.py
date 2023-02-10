from django.shortcuts import render, redirect , get_list_or_404, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Record
# from .models import Record
from .forms import RecordForm

import datetime

from django.http import StreamingHttpResponse
from .video import VideoCamera
from .userdata import Userdata

# Create your views here.
# cam = VideoCamera()


# 메인페이지 로그인후 진입
@login_required
def main(request):
    return render(request, 'record/main.html')


# 기기관리
@login_required
def regist(request,pk):
    try: # globals()['user_{}'.format(pk)].check:
        context = {
            'check' : globals()['user_{}'.format(pk)].check,
        }
    except:
        context = {
            'check' : 0,
        }
    return render(request, 'record/regist.html', context)


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
    cam.good = 0
    cam.bad = 0
    cam.ans = 0
    cam.data=0
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




#삭제
@login_required
def delete(request, pk):
    record = get_object_or_404(Record,pk=pk)
    if record.user==request.user:
        if record:    
            record.delete()
            return redirect('record:chart')
    else:
        return redirect('record:404')

#에러 페이지
def page404(request):
    return render(request, 'record/page404.html')




# 날짜별 테이블 기록
@login_required
def chart(request):
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
    context = {
        'records2' : records2,
    }
    return render(request, 'record/chart.html',context)


# 차트 기록 확인
@login_required
def totalrecord(request):
    return render(request, 'record/totalrecord.html')
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
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            return redirect('record:chart')
    else:
        form = RecordForm()
    context = {
        'form': form,
    }
    return render(request, 'record/create.html', context)

bad = 0
# 실시간 운동영상
@login_required
def live(request):

    global bad
    bad +=0.5
    
    context = {
        'bad':bad,
        'camgood' : cam.good,
        'cambad' : cam.bad,
        'camans' : cam.ans,
        'data':cam.data,
    }
    return render(request, 'record/live.html', context)



#푸쉬업(측면) 시작
def exside(request):
    global exercise_kind, bad
    exercise_kind = '푸쉬업'
    bad, cam.good, cam.bad, cam.ans = 0, 0, 0, 0
    return redirect('record:live')

#팔벌려 높이 뛰기(전면) 시작
def exfront(request):
    global exercise_kind, good, bad
    exercise_kind = '스쿼트'
    bad, cam.good, cam.bad, cam.ans = 0, 0, 0, 0
    return redirect('record:live')

#운동종료
def finish(request):
    global good, bad
    a = { 
        'exercise' : exercise_kind,
        'count' : cam.good + cam.bad,
        'time' : bad,
        'perfect' : 0,
        'good' : cam.good,
        'bad' : cam.bad,
    }
    Record(
        exercise = a['exercise'],
        count = a['count'],
        time = a['time'],
        date = datetime.datetime.now().date(),
        perfect = a['perfect'],
        good = a['good'],
        bad = a['bad'],
        user = request.user,
    ).save()
    bad, cam.good, cam.bad, cam.ans = 0, 0, 0, 0
    return redirect('record:live')



# 데이터 자동생성
@login_required
def deepcreate(request):

    a = { 
        'exercise' : '스쿼트',
        'count' : 123,
        'time' : 123,
        'perfect' : 1223,
        'good' : 777,
        'bad' : 777,
    }
    Record(
        exercise = a['exercise'],
        count = a['count'],
        time = a['time'],
        # date = datetime.datetime.now().date(),
        date = '2023-03-01',
        perfect = a['perfect'],
        good = a['good'],
        bad = a['bad'],
        user = request.user,
    ).save()
    return redirect('record:live')


# STT데이터 통신
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

#     '''
#     여기에 딥러닝??
#     맞으면 로봇에 신호보내기
#     '''
#     return render(request, 'record/test.html',context)

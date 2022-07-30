# python django project

# 가상화면경 설치 명령어(conda version)
conda create --name askcompany python=3.7
<!-- conda config --append channels conda-forge -->
conda activate askcompany
conda remove --name askcompany --all(ex: conda env remove -n python3_test)
conda env list
conda clean -all

conda create --name=django-react-rev2 python=3.8

# 장고 버전 확인
django-admin --version
python -m django --version
pip install django-extensions -> settings.py내에 설정 필요
pip install ipython[notebook]
python manage.py shell_plus --notebook

# 장고 프로젝트 생성
django-admin startproject askcompany .
python -m django startproject
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
python manage.py runserver --settings=askcompany.settings.dev

# 장고 앱 생성
python manage.py startapp blog1

# 어떤 SQL이 수행되는지 확인 가능
django-debug-toolbar

# Microsoft SQL Server 사용시에는
django-pyodbc-azure라이브러리가 필요
https://www.slideshare.net/TaehwanKIm27/sql-server-django-118638328

# 직접 SQL 수행 시
from django.db import connection, connections

with connection.cursor() as cursor:
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()
    print(row)

# 장고 외부에서, 데이터베이스 형상을 관리할 경우
데이터베이스로부터 모델 클래스 소스 생성 -> inspectdb명령 모델 활용

# 모델명과 DB테이블명
blog앱
  Post모델 -> blog_post
커스텀 지정
  모델 Meta클래스의 db_table 속성
  
# 실제 생성된 쿼리 보기
python manage.py sqlmigrate instagram 0001_initial

# db shell보기
python manage.py dbshell
.tables
.schema instagram_post
.quit

# File Upload Handler
파일크기가 2.5MB이하 일 경우
 메모리에 담겨 전달
 MemoryFileUploadHandler
파일크기가 2.5MB초과 일 경우
 디스크에 담겨 전달
 TemporaryFileUploaderHandler
관련 설정
 settings.FILE_UPLOAD_MAX_MEMORY_SIZE
  => 2.5MB

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'askcompany.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"
import django
django.setup()

from instagram.models import Post
Jupyter에서 사용시에는
 => os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true" 설정 추가 필요

# Model Manager
데이터베이스 질의 인터페이스를 제공
디폴트 Manager로서 ModelCls.objects가 제공

ModelCls.objects.all().order_by('-id')[:10]
ModelCls.objects.create(title="New Title")

# 정렬 조건 추가
1) (추천) 모델 클래스의 Meta속성으로 ordering 설정: list로 지정
2) 모든 queryset에서 order_by(...)지정
class Item(models.Model):
  name = models.CharField(max_length=100)
  desc = models.TextField(blank=True)
  price = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add_True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['id']

python manage.py shell_plus --print-sql
# 슬라이싱을 통한 범위조건 추가
[start:stop:step]
OFFSET -> start
LIMIT -> stop - start
(주의) step은 쿼리에 대응되지 않습니다. 사용을 비추천
역순 슬라이싱은 지원하지 않음(데이터베이스에서 지원 x)
step은 데이터베이스에서 지원하지 않음, 리턴값이 List로 반환되며 더이상 lazy하지 않음. 실제 처리는 queryset에서 주관

# django-debug-toolbar
현재 request/response에 대한 다양한 디버깅 정보를 보여줌. 다양한 Panel지원
SQLPanel을 통해, 각 요청 처리시에 발생한 SQL내역 확인 가능.
Ajax요청에 대한 지원은 불가합니다.
settings.DEBUG = True시에만 쿼리 실행내역을 메모리에 누적
from django.db import connection, connections

for row_dict in connection.queries:
  print('{time} {sql}'.format(**row_dict))

connections['default'].queries
쿼리 초기화
메모리에 누적되기에, 프로세스가 재시작되면 초기화
django.db.reset_queries() 통해서 수동 추기화도 가능

# django-querycount
SQL실행내역을 개발서버 콘솔 표준 출력
Ajax내역도 출력 가능

# RDBMS에서의 관계 예시
1: N => models.ForeignKey로 표현
1: 1 => models.OneToOneField로 표현
M : N => models.ManyToManyField
  1개의 포스팅(Post)에는 다수의 태그(Tag)
  1개의 태그(Tag)에는 다수의 포스팅(Post)
ForeignKey(to, on_delete)
  to : 대상모델
  on_delete : Record 삭제시 Rule
    CASCADE: FK로 참조하는 다른 모델의 Record도 삭제
    PROTECT: ProtectedError(IntegrityError 상속)를 발생시키며, 삭제방지
    SET_NULL: null로 대체, 필드에 null=True옵션 필수
    SET_DEFAULT: 디폴트 값으로 대체, 필드에 디폴트값 지정 필수
    SET: 대체할 값이나 함수 지정. 함수의 경우 호출하여 리턴값을 사용.
    DO_NOTHING: 어떤 액션 x. DB에 따라 오류가 발생할 수도 있음.

FK에서의 reverse_name
reverse접근 시의 속성명: 디폴트 -> "모델명소문자_set"
post = Post.objects.first()
post.comment_set.all()
 = Comment.objects.filter(post=post)
1. reverse_name 포기, related_name = '+'
2. reverse_name 명명, related_name="blog_post_set"
ForeignKey.limit_choices_to
  Form을 통한 choice위젯에서 선택항목 제한 가능.
    dict/Q 객체를 통한 지정: 일괄지정
    dict/Q 객체를 리턴하는 함수 지정: 매번 다른 조건 지정 가능
  ManyToManyField에서도 지원
    staff_member = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      limit_choices_to={'is_staff': True}
    )
  
  # OneToOneFied 1:1관계에서 어느쪽이라도 가능
  User:Profile
  ForeignKey(unique=True)와 유사하지만, reverse 차이
    User:Profile를 FK로 지정한다면 -> profile.user_set.first() -> user
    User:Profile를 O2O로 지정한다면 -> profile.user -> user
  OneToOneFiled(to, on_delete)
  
  django/contrib/auth/models.py -> User존재
  class Profile(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

# M:N의 관계 예시
Tag.objects.create(name='장고')

post = Post.objects.first()
tag = Tag.objects.get(name='파이썬')
post.tag_set.add(tag)
post.tag_set.remove(tag)

tag_qs = Tag.objects.all()
post.tag_set.add(*tag_qs) # unpack문법

# RDBMS지만, DB따라 NoSQL기능도 지원
ex) 하나의 Post안에 다수의 댓글 저장 가능
djkoch/jsonfield
  대개의 db엔진에서 사용가능
  TextField/CharField를 래핑
  dict등의 타임에 대한 저장을 직렬화하여 문자열로 저장
    내부 필드에 대해 쿼리 불가
djnago.contrib.postgres.fields.JSONField
  내부적으로 PostgreSQL의 jsonb타입
  내부 필드에 대해 쿼리 지원
adamchainz/django-mysql
  MySQL 5.7이상에서 json필드 지원

# Migrations
마이그레이션 파일 생성
  python manage.py makemigrations 앱이름 ---- (1)
지정 데이터베이스에 마이그레이션 적용
  python manage.py migrate 앱이름   ---- (3)
마이그레이션 적용 현황 출력
  python manage.py showmigrations 앱이름
지정 마이그레이션의 SQL내역 출력
  python manage.py sqlmigrate 앱이름 마이그레이션-이름 ---- (2)
주의) 같은 Migration파일이라 할지라도, DB종류에 따라 다른 SQL이 생성됩니다.
마이그레이션 파일이 너무 많아질 경우, squashmigrations명령으로 다수의 마이그레이션 파일을 통합할 수 있습니다.
모든 적용을 롤백
  python manage.py migrate blog zero
별도 다른 키를 기본키로 생성하고 싶다면
  primary_key=True 옵션 설정
새로운 필드가 필수 필드라면?
  필수필드 여부: blank/null옵션이 모두 False일때(디폴트)
  makemigrations명령을 수행할 때, 기존 Record들에 어떤 값을 채워넣을지 묻습니다.
    1) 지금 그 값을 입력하겠다.
    2) 명령 수행을 중단
개발 시에 "서버에 아직 반영하지 않은" 마이그레이션을 다수 생성했다면?
  - 이를 그대로 서버에 반영(migrate)하시지 마시고,
  - 하나의 마이그레이션으로 합쳐서 적용하기를 권장.
    방법1) 서버로의 미적용 마이그레이션들을 모두 롤백하고 -> 롤백된 마이그레이션을 모두 제거하고 -> 새로이 마이그레이션 파일 생성
    방법2) 미적용 마이그레이션들을 하나로 합치기 -> squashmigrations명령
# View
함수 기반 뷰
클래스 기반 뷰
  클래스.as_view()
django.shortcuts.render함수는 템플릿 응답을 위한 shortcut함수 ** 활용 필수 **
장고는 디폴트로 utf8로 인코딩 해줌
response = HttpResponse()
response.write('Hello World')
return response

# HttpRequest와 HttpResponse 예시
from django.http import HttpRequest, HttpResponse

def index(request: HttpRequest) -> HttpResponse:
  request.method
  request.META
  request.GET, request.POST, request.FILES, request.body

  content = '''
    <httml>...</html>
  ''' # 문자열 혹인 이미지, 각종 파일 등

  response = HttpResponse(content)
  response.write(content) # response -> file-like object
  response['Customer-Header'] = 'Customer Header Value'
  return response

#FBV의 예
Item목록 보기
myapp/views.py

from django.shortcuts import render
from shop.models import Item

def item_list(request):
  qs = Item.objects.all()
  return render(request, 'shop/item_list.html', {'item_list': qs,})

myapp/urls/py

from django.urls import path

urlpatterns = [
  path('item/', item_list, name='item_list'),
]

# 살짝 구성해본 클래스 기반의 호출 가능한 객체
from django.shortcuts import render
from shop.models import Item

class GenericListView:
  def __init__(self, model_cls):
    self.model_cls = model_cls
  
  def get_list_name(self):
    return '{}_list'.format(self.model_cls._meta.model_name)

  def get_template_name(self):
    return self.model_cls._meta.app_label + '/' + \
      self.get_list_name() + '.html'

  def get_queryset(self):
    return self.model_cls.objects.all()
  
  def get_context(self):
    return {
        self.get_list_name(): self.get_queryset(),
    }
  
  def __call__(self, request):
    context = self.get_context()
    return render(request, self.get_template_name(), context)
  
item_list = GenericView(Item)

from django.urls import path
urlpatterns = [
  path('items/', item_list, name='item_list')
]
# Excel파일 다운로드 응답
from django.http import HttpResponse
from ullib.parse import quote

def response_excel(request):
  filepath = '/other/path/excel.xls'
  filename = os.path.basename(filepath)

  with open(filepath, 'rb') as f:
    response = HttpResponse(f, content_type='application/vnd.ms-excel)
    # 브라우저에 따라 다른 처리가 필요합ㄴ디ㅏ.
    encoded_filename = quote(filename)
    response['Content-Disposition'] = "attachement; filename*=utf-8''{}".format(encoded_filename)
    # django.http.FileReader를 통해 첨부 헤더 지워

  return response

# Pandas를 통한 CSV응답 생성
import pandas as pd
from io import StringIO
from django.http import HttpResponse

def response_csv(request):
  df = pd.DataFrame([
    [100, 110, 120]
    [200, 210, 220]
    [300, 310, 320]
  ])

  io = StringIO()
  df.to_csv(io)
  io.seek(0) # 끝에 있는 file cursor를 처음으로 이동
  response = HttpResponse(io, contet_type='text/csv')
  response['Content-Disposition'] = "attache; filename*=utf-8''{}".format(encoded_filename)
  return response

# Pandas를 통한 엑셀 응답 생성(필요한 라이브러리: pandas, xlwt)

io = BytesIO()
df.to_excel(io)
.. 기타 등등

# Pillow를 통한 이미지 응답 생성 - 기본(필요한 라이브러리: pillow, requests)
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

ttf_path = 'C:/Windowns/Fonts/malgun.ttf'
image_url = 'http://www.flowermeaning.com/flower-pics/Calla-Lily-Meaning.jpg'

res = requests.get(image_url)
io = BytesIO(res.content)
io.seek(0)

canvas = Imange.open(io).convert('RGBA')

font = ImageFont.truetype(ttf_path, 40)
drasw = ImageDraw(canvas)

text = 'Ask Company'
left, top = 10, 10
margin = 10
width, height = font.getSize(text)
right = left + width + margin
bottom = left + width + margin

draw.rectangle((left, top, right, bottom), (255, 255, 244))
draw.text((5, 15), text, font=font, fill=(20, 20, 20))
canvas.show()

# Generic display views
DetailView
  <-- SingleObject/TemplateResponseMixin
    <-- TemplateResponseMixin
  <-- BaseDetailView
    <-- SingleObjectMixin
    <-- View
ListView
  <-- MultipleObject/TemplateResponseMixin
    <-- TemplateResponseMixin
  <-- BaseLitView
    <-- MultipleObjectMixin <-- ContextMixin
    <-- View
DetailView
1개의 모델의 1개의 Object에 대한 템플릿 처리
  모델명소문자 이름의 Model Instance를 템플릿에 전달
    지정 pk혹은 slug에 대응하는 Model Instance

from django.views.generic import DetailView
from .models import Post

post_detail = DetailView.as_view(model=Post, template_name='instatram/post_detail.html')
# 가급적이면 자동 명칭을 활용하는 걸 추천, 소스 간소화
class PostDetailView(DetailView):
  model = Post
post_detail2 = PostDetailView.as_view()

# 장식자(Decorators)
어떤 함수를 감싸는(Wrapping) 함수
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def protected_view1(request):
  return render(request, 'myapp/secret.html')

def protected_view2(request):
  return render(request, 'myapp/secret.html')

protected_view2 = login_required(protected_view2)

# 몇가지 장고 기본 Decorators
django.views.decorators.http
  require_http_methos, require_GET, require_POST, require_safe(head, get 변화를 일으키지 않는 메소드 호출)
    지정 method가 아닐 경우, HttpResponseNotAllowed응답(상태코드 405) 반환
django.contrib.auth.decorators
  user_passes_test: 지정 함수가 False를 반환하면 login_url로 redirect
  login_required: 로그아웃 상황에서 login_url로 redirect
  permission_required: 지정 퍼미션이 없을 때 login_url로 redirect
django.contrib.admin.views.decorators
  staff_member_required: staff member가 아닐 경우 login_url로 이동

# CBV에 장식자 입히기 #1
  가독성이 좋지 않아요
요청을 처리하는 함수를 Wrapping하기

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

class SecretView(TemplateView):
  template_name = 'myapp/secret.html'

view_fn = SecretView.as_view()
secret_view = login_required(view_fn) # 이미 생성된 함수에 장식자 입힐 수도 있어요

# CBV에 장식자 입히기 #2
  괜히 dispatch 재정의
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class SecretView(TemplateView):
  template_name = 'myapp/secret.html'

  # 클래스 멤버함수에는 method_decorator를 활용
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super().dispatch(*args, **kwargs)

secret_view = SecretView.as_view()

# CBV에 장식자 입히기 #3
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

## 클래스에 직접 적용할 수도 있어요
@method_decorator(login_required, name='dispatch')
class SecretView(TemplateView):
  template_name = 'myapp/secret.html'

secret_view = SecretView.as_view()

# ArchiveIndexView
지정 날짜필드 역순으로 정렬된 목록 -> 최신목록을 보고자 할때
from django.views.generic import ArchiveIndexView
from .models import Post

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at')

옵션: model, date_field(정렬기준필드), date_list_period(default: "year")
디폴트 template_name_suffix : "_archive.html"
Context
  latest: QuerySet
  date_list: 등록된 Record의 년도 목록

Post.objects.all().values_list('created_at__year')
Post.objects.all().values_list('created_at__year', flat=True)
year_list = _   <== 직전 실행계획
set(year_list)

# YearArchiveView
지정 year년도의 목록
필요한 URL인자: "year"
옵션
  model, date_field
  date_list_period(default: "month")
  make_object_list(default: false)
    거짓일 경우, object_list를 비움
  template_name_suffix : "_archive_year.html"
  Context
    year, previous_year, next_year
    date_list: 전체 Record의 월 목록
    object_list
urlpatterns = [
  re_path(r'^archive/(?P<year>\d{4})/$', ...),
]

from django.views.generic.dates import YearArchiveView
from .models import Post

class PostYearArchiveView(YearArchiveView):
  model = Post
  date_field = 'created_at'
  # make_object_list = False

# HTTP 상태코드
웹서버는 적절한 상태코드로서 응답해야 합니다.
각 HttpResponse클래스마다 고유한 status_code가 할당(코드)
REST API를 만들 때, 특히 유용

# django/http/response.py
class HttpResponseRedirect(HttpResponseRedirectBase):
  status_code = 302

from django.http import HttpResponse

def test_view(request):
  # Return a "created" (201) response code.
  return HttpResponse(status=201)

# 302 응답하는 몇가지 예
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url

def view1(request):
  return HttpResponseRedirect('/shop/')

def view2(request):
  url = resolve_url('shop:item_list') # 후에 배울 URL Reverse적용
  return HttpResponseRedirect(url)

def view3(request):
  # 내부적으로 resolve_url 사용
  # 인자로 지정된 문자열이 url reverse에 실패한 경우,
  # 그 문자열을 그래도 url로 사용하여, redirect 시도
  return redirect('shop:item_list')

# 404 응답하는 몇 가지 예
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from shop.models import Item

def view1(request):
  try:
    item = Item.objects.get(pk=100)
  except Item.DoesNotExist:
    raise Http404

def view2(request):
  item = get_object_or_404(Item, pk=100) # 내부적으로 raise Http404

def view3(request):
  try:
    item = Item.objects.get(pk=100)
  except Item.DoesNotExist:
    return HttpResponseNotFound() # 잘 쓰지 않는 방법

# 500 응답하는 몇가지 예
뷰에서 요청 처리 중에, 뷰에서 미처 잡지 못한 오류가 발생했을 경우
  IndexError, KeyError, django.db.models.ObjectDoesNotExist등

from shop.models import Item

def view1(request):
  # IndexError
  name = ['Tome', 'Steve'][100]

  # 지정 조건의 Item레코드가 없을 때, Item.DoesNotExist 예외
  # 지정 조건의 Item레코드가 2개 이상 있을 때, Item.MultipleObjectsReturned 예외
  item = Item.objects.get(pk=100)
# 대표적인 상태 코드
200번대: 성공
  200: 서버가 요청을 잘 처리했다.
  201: 작성됨. 서버가 요청을 접수하고, 새 리소스를 작성했다.
300번대: 요청을 마치기 위해, 추가 조치가 필요하다.
  301: 영구이동, 요청한 페이지가 새 위치로 영구적으로 이동(검색엔진에 영향)
  302: 임시이동, 페이지가 현재 다른 위치에서 요청을 응답하고 있지만, 요청자는 향후 원래 위치를 계속 사용해야 한다.
400번대: 클라이언트측 오류
  400: 잘못된 요청
  401: 권한 없음
  403(Forbidden): 필요한 권한을 가지고 있지 않아서, 요청을 거부
  404: 서버에서 요청한 리소르를 찾을 수 없다.
  405: 허용되지 않는 방법. POST방식만을 지원하는 뷰에 GET요청을 할 경우
500번대: 서버측 오류
  500: 서버 내부 오류 발생

# 다양한 HttpResponse서브 클래스
  지정 상태코드의 응답이 필요할 때 
  HttpResponseRedirect: 상태코드 302
  HttpResponsePermanentRedirect : 상태코드 301 (영구 이동)
  HttpResponseNotModified : 상태코드 304
  HttpResponseBadRequest : 상태코드 400
  HttpResponseNotFound : 상태코드 404
  HttpResponseForbidden : 상태코드 403
  HttpResponseNotAllowed : 상태코드 405
  HttpResponseGone : 상태코드 410
  HttpResponseServerError : 상태코드 500

# URL Reverse를 수행하는 4가지 함수
url 템플릿 태그
  내부적으로 reverse 함수를 사용
reverse 함수
  매칭 URL이 없으면 NoReverseMatch예외 발생
resolve_url 함수
  매핑 URL이 없으면 "인자 문자열"을 그대로 리턴
  내부적으로 reverse함수를 사용
redirect함수
  매칭 URL이 없으면 "인자 문자열"을 그대로 URL로 사용
  내부적으로 resolve_url함수를 사용

{% url "blog:post_detail" 100 %}
{% url "blog:post_detail" pk=100 %}
reverse('blog:post_detail', args=[100])
reverse('blog:post_detail', kwargs={'pk': 100})

resolve_url('blog:post_detail', 100)
resovle_url('blog:post_detail', pk=100)
resovle_url('/blog/100')

redirect('blog:post_detail', 100) => HttpResponse응답( 301 or 302)
redirect('blog:post_detail', pk=100)
redirect('/blog/100')

resovle_url('blog:post_detail', pk=post.pk)
redirect('blog:post_detail', pk=post.pk)
{% url 'blog:post_detail' post.pk %}
==>
resolve_url(post)
redirect(post)
{{ post.get_absolute_url }}

# 모델 클래스에 get_absolute_url() 구현
resolve_url함수는 가장 먼저 get_absolute_url()함수의 존재여부를 체크하고,
존재할 경우 reverse를 수행하지 않고 그 리턴값을 즉시 리턴
#django/shortcuts.py
def resolve_url(to, *args, **kwargs):
  if hasattr(to, 'get_absolute_url'):
    return to.get_absolute_url()
  # 중략
  try:
    return reverse(to, args=args, kwargs=kwargs)
  except NoReverseMatch:
    # 나머지 코드 생략
  
# resolve_url/redirect를 위한 모델 클래스 추가 구현
from django.urls import reverse
class Post(models.Model):
  def get_absolute_url(self):
    return reverse('blog:post_detail', args=[self.pk])
  
# Static & Media파일
Static
  개발리소스로서의 정적인 파일
  앱/프로젝트 단위로 저장/서빙
Media
  FileField/ImageField를 통해 저장한 모든 파일
  DB필드에는 저장경로를 저장하며, 파일은 파일 스토리지에 저장
  프로젝트 단위로 저장/서빙

python manage.py collectstatic => STATIC_ROOT를 통해 서빙 배포시 의미 있게 사용

# nginx 웹서버에서의 static 설정 예시
server {
  # 중략
  location /static {
    autoindex off;
    alias /var/www/staticfiles; # settings.STATIC_ROOT
  }
  location /media {
    autonindex off;
    alias /var/www/media; # settings.MEDIA_ROOT
  }
}

# ngrok 
 os에 맞는 ngrok 다운로드
 ngrok http 8000


from urllib.parse import urlencode
print(urlencode({'key1': 'value1', 'key2': 10, 'name': '방탄소년단'}))
print('방탄소년단'.encode('utf8'))
print(''.join('%{:X}'.format(ch) for ch in '방탄소년단'.encode('utf8')))
x-www-from-urlencoded인코딩의 값만 실을 수 있습니다. -> QueryString
요청 Body에 모든 인코딩의 인자를 실어서 보냅니다
x-www-form-urlencoded 인코딩의 값도 OK
multipart/form-data 인코딩의 값도 OK -> 파일 업로드 가능

# MultiValueDic
동일 key의 다수 value를 지원하는 사전
from django.utils.datastructures import MultiValueDict

d = MultiValueDict({'name': ['Adrian', 'Simon'], 'position': ['Developer']})
d['name']  # dict과 동일하게 동작, 단일값 획득

d.getlist('name') # 다수값 획득을 시도. 리스트를 반환
> ['Adrian', 'Simon']
d.getlist('doesnotexist') # 없는 key에 접근하면 빈리스트를 반환
> []
d['name'] = 'changed'
d
> <MultiValueDict: {'name': ['changed'], 'position': ['Developer']}>

from django.http import QueryDict
qd = QueryDict('name=Adrian&name=Simon&position=Developer', encoding='utf8')
qd['name']
> 'Simon'
qd.getlist('name')
> ['Adrian', 'Simon']
qd['name'] = 'changed'
> AttributeError: This QueryDict instance is immutable

# django.http.HttpResponse
사전-like 인터페이스로 응답의 커스텀 헤더 추가/삭제
  response = HttpResponse()
  response['Age'] = 120
  del response['Age']
파일 첨부로 처리되기를 브라우저에게 알리기
  response = HttpResponse(excel_data, context_type='application/vnd.ms-excel')
  response['Content-Disposition'] = 'attachment; filename="foo.xls"'

# Form
장고를 더욱 장고스럽게 만들어주는 주옥같은 Feature 
주요 역할
  입력폼 HTML 생성
  입력폼 값에 대한 유효성 검증(Validation) 및 값 변환
  검증을 통과한 값들을 dict형태로 제공
#myapp/forms.py
from django import forms

class PostForm(forms.Form):
  title = forms.CharField()
  content = forms.CharField(widget=form.Textarea)

# Django Style의 Form처리(1)
하나의 URL(하나의 View)에서 2가지 역할을 모두 수행
  1. 빈 폼을 보여주는 역할과
  2. 폼을 통해 입력된 값을 검증하고 저장하는 역할
# Django Style의 Form처리(2)
GET방식으로 요청받았을 때
   New/Edit 입력폼을 보여줍니다.
POST방식으로 요청받았을 때
  데이터를 입력받아 (request.POST, request.FILES) 유효성 검증 수행
  검증 성공 시: 해당 데이터를 저장하고 SUCCESS URL로 이동
  검증 실패 시: 오류메세지와 함께 입력폼을 다시 보여줍니다.

def post_new(request):
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      post = Post(**form.cleaned_data)
      post.save()
      return redirect(post)
    else:
      form = PostForm()
    
    return render(request, 'blog/post_form.html, {
      'form': form,
    })

# 1) Form/ModelForm 클래스 정의
# myapp/forms.py
form django import forms

class PostForm(forms.Form):
  title = forms.CharField()
  content = forms.CharField(widget=form.Textarea)

# 2) 필드 별로 유효성 검사 함수 추가 적용
  Form의 경우

from django.core.validators import MinLengthValidator
min_length_3_validator = MinLengthValidator(3)

# myapp/forms.py
from django import forms

def min_length_3_validator(value):
  if len(value) < 3:
    raise forms.ValidationError('3글자 이상 입력해 주세요.')
class PostForm(forms.Form):
  title = forms.CharField(validators=[min_length_3_validator])
  content = forms.CharField(widget=form.Textarea)

  ModelForm의 경우
# myapp/models.py
from django import forms
from django import models

def min_length_3_validator(value):
  if len(value) < 3:
    raise forms.ValidationError('3글자 이상 입력해주세요.')

class Post(forms.Model):
  title = models.CharField(max_length=100, validators=[min_length_3_validator])
  content = models.TextField()

# myapp/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = '__all__'
  
# 4) POST 요청에 한해 입력값 유효성 검증
if request.method == 'POST'
  # POST인자는 request.POST와 request.FILES를 제공받음
  form = PostForm(request.POST, request.FILES)
  # 인자로 받은 값에 대해서, 유효성 검증 수행
  if form.is_valid(): # 검증을 성공하면, True리턴
    # 검증에 성공한 값들을 사전타입으로 제공받음.
    # 검증에 성공한 값을 제공받으면, Django Form의 역할은 여기까지!!
    # 필요에 따라, 이 값을 DB에 저장하기
    form.cleaned_data
    post = Post(**form.cleaned_data) # DB에 저장하기
    post.save()

    return redirect('/success_url/')
  else: # 검증에 실패하면, form.errors와 form.각필드.errors에 오류정보를 저장
    form.errors
else: # GET 요청일 때
  form = PostForm()
  return render(request, 'myapp/form.html', {'form': form})
# 5) 템플릿을 통해 HTML 폼 노출
1. GET 요청일 때
-> 유저가 Form을 채우고 Submit -> POST요청
2. POST요청이지만 유효성 검증에서 실패했을 때
  Form 인스턴스를 통해 HTML폼 출력
  오류 메세지도 있따면 같이 출력
  -> 유저가 Form을 채우고 Submit -> POST 재요청
<table>
  <form action="" method="post">
    {% csrf_token %}
    <table>{{ form.as_table }}</table>
    <input type="submit" />
  </form>
</table>

# 윈도우 환경 변수 설정
set SENDGRID_API_KEY=xxxxxxxxx
echo %SENDGRID_API_KEY%  # 확인
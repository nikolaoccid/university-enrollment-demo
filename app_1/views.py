from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .groupby import groupbykey
from .models import Predmeti, Korisnik, Upisi
from .forms import PredmetiForm, NositeljForm, NewUserForm, EditUserForm
from django.db.models import Count, Q


@login_required
def welcome(request):
  if request.user.role == 'stu':
    return redirect('enrollmentform', userid=request.user.id)
  if request.user.is_superuser:
    return redirect('subjects')
  if request.user.role == 'prof':
    return redirect('profesorsubjects')


def getSubjects(request):
  if request.user.is_superuser:
    subjects = Predmeti.objects \
      .annotate(polozili=Count('upisi', filter=Q(upisi__status_upisa='polozio'))) \
      .annotate(
      polozili_redovni=Count('upisi', filter=Q(upisi__status_upisa='polozio') & Q(upisi__student__status='red'))) \
      .annotate(
      polozili_izvanredni=Count('upisi', filter=Q(upisi__status_upisa='polozio') & Q(upisi__student__status='izv'))) \
      .all
    return render(request, 'subjects.html', {'data': subjects})
  return redirect('home')


def profesorSubjects(request):
  if request.user.is_superuser or request.user.role == 'prof':
    # profesor = Korisnik.objects.get(request.user.id)
    subjects = Predmeti.objects.filter(nositelj=request.user)
    return render(request, 'subjects.html', {'data': subjects})
  return redirect('home')


def editSubject(request, subjectid):
  subject = Predmeti.objects.get(pk=subjectid)
  if request.method == 'GET' and request.user.is_superuser:
    editForm = PredmetiForm(instance=subject)
    return render(request, 'editsubject.html', {'form': editForm})
  if request.method == 'POST' and request.user.is_superuser:
    editForm = PredmetiForm(request.POST, instance=subject)
    if editForm.is_valid():
      editForm.save()
    return redirect('subjects')


def addSubject(request):
  if request.method == 'GET' and request.user.is_superuser:
    subjectForm = PredmetiForm()
    return render(request, 'createsubject.html', {'form': subjectForm})
  elif request.method == 'POST' and request.user.is_superuser:
    subjectForm = PredmetiForm(request.POST)
    if subjectForm.is_valid():
      subjectForm.save()
      return redirect('subjects')
    else:
      return HttpResponseNotAllowed()
  return redirect('home')


def deleteSubject(request, subjectid):
  if request.user.is_superuser:
    subject = Predmeti.objects.get(pk=subjectid).delete()
    return redirect('subjects')
  return redirect('home')


def editNositelj(request, subjectid):
  subject = Predmeti.objects.get(pk=subjectid)
  if request.method == 'GET' and request.user.is_superuser:
    editForm = NositeljForm(instance=subject)
    return render(request, 'editprofesor.html', {'form': editForm})
  if request.method == 'POST' and request.user.is_superuser:
    editForm = NositeljForm(request.POST, instance=subject)
    if editForm.is_valid():
      editForm.save()
    return redirect('subjects')


def register(request):
  if request.method == 'GET' and request.user.is_superuser:
    userForm = NewUserForm()
    return render(request, 'register.html', {'form': userForm})
  if request.method == 'POST' and request.user.is_superuser:
    print("entered register post")
    userForm = NewUserForm(request.POST)
    # print('formerrors', userForm.errors)
    if userForm.is_valid():
      userForm.save()
      return redirect('home')
    else:
      return redirect('register')
  else:
    return HttpResponseNotAllowed('Unable to register')


def students(request):
  if request.user.is_superuser:
    students = Korisnik.objects.filter(role='stu')
    return render(request, 'listusers.html', {'users': students})
  else:
    return redirect('home')


def profesors(request):
  if request.user.is_superuser:
    profesors = Korisnik.objects.filter(role='prof')
    return render(request, 'listusers.html', {'users': profesors})
  else:
    return redirect('home')


def editUser(request, userid):
  user = Korisnik.objects.get(pk=userid)
  if request.method == 'GET' and request.user.is_superuser:
    editForm = EditUserForm(instance=user)
    return render(request, 'edituser.html', {'form': editForm})
  if request.method == 'POST' and request.user.is_superuser:
    editForm = EditUserForm(request.POST, instance=user)
    if editForm.is_valid():
      editForm.save()
  return redirect('students') if user.role == 'stu' else redirect('profesors')


def usersOnSubject(request, subjectid):
  predmet = Predmeti.objects.get(pk=subjectid)
  if request.user == predmet.nositelj or request.user.is_superuser:
    red_studenti = Upisi.objects.filter(Q(predmet=predmet) & Q(student__status='red'))
    izv_studenti = Upisi.objects.filter(Q(predmet=predmet) & Q(student__status='izv'))

    red_grupirani_studenti = groupbykey(
      red_studenti.values('student_id', 'student__username', 'student__status', 'status_upisa'),
      'status_upisa')

    izv_grupirani_studenti = groupbykey(
      izv_studenti.values('student_id', 'student__username', 'student__status', 'status_upisa'),
      'status_upisa')

    return render(request, 'usersonsubject.html', {'red_grupirani_studenti': red_grupirani_studenti,
                                                   'izv_grupirani_studenti': izv_grupirani_studenti,
                                                   'predmet': predmet})
  return redirect('home')


def changeStatus(request, userid, subjectid, status):
  predmet = Predmeti.objects.get(pk=subjectid)
  korisnik = Korisnik.objects.get(pk=userid)
  if request.user == predmet.nositelj or request.user.is_superuser:
    upis = Upisi.objects.get(predmet=predmet, student=korisnik)
    upis.status_upisa = status
    upis.save()
  return redirect('usersonsubject', subjectid=subjectid)


def enrollmentForm(request, userid):
  if request.user.is_superuser or request.user.id == userid:
    student = Korisnik.objects.get(pk=userid)
    upisani_predmeti = Upisi.objects.filter(student=student)
    upisi = Upisi.objects.filter(student=student).prefetch_related('predmet')
    upisi_array = [
      {'id': upis.id,
       'sem_red': upis.predmet.sem_red,
       'predmet_name': upis.predmet.name,
       'sem_izv': upis.predmet.sem_izv,
       'status_upisa': upis.status_upisa,
       'predmet_id': upis.predmet.id
       }
      for upis in upisi
    ]

    upisani_predmeti_ids = Upisi.objects.filter(student=student).values_list('predmet_id', flat=True)
    predmeti_za_upis = Predmeti.objects.exclude(id__in=upisani_predmeti_ids)

    grupirani_redovni_upisani_predmeti = groupbykey(upisi_array, 'sem_red')
    grupirani_izvanredni_upisani_predmeti = groupbykey(upisi_array, 'sem_izv')
    grupirani_upisani_predmeti = grupirani_redovni_upisani_predmeti if student.status == 'red' else grupirani_izvanredni_upisani_predmeti

    return render(request, 'enrollmentform.html',
                  {'student': student,
                   'predmeti_za_upis': predmeti_za_upis,
                   'grupirani_upisani_predmeti': grupirani_upisani_predmeti
                   })
  else:
    return redirect('home')


def enroll(request, userid, subjectid):
  if request.user.is_superuser or request.user.id == userid or request.user.role == 'prof':
    predmet = Predmeti.objects.get(pk=subjectid)
    korisnik = Korisnik.objects.get(pk=userid)
    Upisi.objects.create(student=korisnik, predmet=predmet, status_upisa='upisan')
  return redirect('enrollmentform', userid=userid)


def disenroll(request, userid, subjectid):
  if request.user.is_superuser or request.user.id == userid or request.user.role == 'prof':
    upis = Upisi.objects.get(student=Korisnik.objects.get(pk=userid), predmet=Predmeti.objects.get(pk=subjectid))
    if upis and upis.status_upisa == 'upisan':
      upis.delete()
    return redirect('enrollmentform', userid=userid)
  else:
    return redirect('home')


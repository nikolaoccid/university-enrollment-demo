# from django.test import TestCase

# Create your tests here.


# def pripremazaobranu():
#   # broj polozenih predmeta za svakog korisnika
#   korisnici = Korisnik.objects\
#     .annotate(polozenipredmeti=Count('upisi', filter=Q(upisi__status_upisa='polozio'))).all()
#   # print('korisnici', korisnici)
#   # print(korisnici[3].polozenipredmeti)
#
#   #broj studenata koji su polozili svaki pojedini predmet
#   studenti_polozili_predmet = Predmeti.objects\
#     .annotate(ukbrojst=Count('upisi', filter=Q(upisi__status_upisa='polozio') & Q(upisi__student__status='red'))).all()
#   # print('studenti_polozili_predmet', studenti_polozili_predmet)
#   # print('studenti_polozili_predmet',studenti_polozili_predmet[3].name, studenti_polozili_predmet[6].ukbrojst)
#
# #za subjectId sortiraj sve studente po statusu studenta i po statusu upisa
#   subjectId = 2
#   predmet = Predmeti.objects.get(pk=subjectId)
#
#   red_stud = Upisi.objects.filter(Q(predmet=predmet) & Q(student__status='red'))
#   grupirani_red_stud = groupbykey(red_stud.values('status_upisa', 'student_id', 'student__username', 'student__status'), 'status_upisa')
#   # print('grupirani_red_stud', grupirani_red_stud)
#
#   izv_stud = Upisi.objects.filter(Q(predmet=predmet) & Q(student__status='izv'))
#   grupirani_izv_stud = groupbykey(izv_stud.values('status_upisa', 'student_id', 'student__username', 'student__status'), 'status_upisa')
#   # print('grupirani_izv_stud', grupirani_izv_stud)
#
# # pronađi predmete koje je polozio jedan student i sortiraj ih po semestrima
#   userId = 6  # user: izv_stud
#   korisnik = Korisnik.objects.get(pk=userId)
#   polozeni_predmeti = Upisi.objects.filter(Q(student=korisnik) & Q(status_upisa='polozio'))
#   print('polozeni_predmeti', polozeni_predmeti)
#   polozeni_predmeti_po_semestru = groupbykey(polozeni_predmeti.values('predmet_id', 'predmet__sem_red', 'predmet__ects'), 'predmet__sem_red')
#   print('polozeni_predmeti_po_semestru', polozeni_predmeti_po_semestru)

rezultat = {}
subjects = {
  1: [
    {'predmet_id': 1, 'predmet__sem_red': 1, 'predmet__ects': 5},
     {'predmet_id': 3, 'predmet__sem_red': 1, 'predmet__ects': 6}
  ],
  6: [
    {'predmet_id': 48, 'predmet__sem_red': 6, 'predmet__ects': 8}
  ]
}

for semestar in subjects:
  semestarsum = 0
  print(semestar)
  for y in subjects[semestar]:
    print(y)
    print(print('predmet-ects', y['predmet__ects']))
    semestarsum += y['predmet__ects']
    # for z in y:
    #   print('predmet-ects', y['predmet__ects'])
    #   print(z, y[z])
    rezultat[semestar] = semestarsum

print(rezultat)
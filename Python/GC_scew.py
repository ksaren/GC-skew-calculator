# Ohjelma, joka lukee sekvenssin tiedostosta ja tulostaa sekvenssin
# GC-vinouman toiseen tiedostoon.

# Lopputyö kurssille Python-ohjelmointia biotieteilijöolle
# Helsingin Avoin Yliopisto, syyskuu 2015

# Kaisa Saren

# Huom! Seuraavat muuttujat ovat globaaleja, niitä käyttää osa
# ohjelman funktioista.
rengas = False
GC_vino = [] # Tähän listaan tulee emäksen sijainti ja GC-arvo
DNA_bases = ['A','T','G','C']
otsikko = ''
sekvenssi = ''

# Funktio joka lukee tiedostosta sekvenssin ja sen nimen, palauttaa toden jos
# onnistuu.
def lue_FASTA():
    global sekvenssi # käytetään ohjelman yhteisiä muuttujia
    global otsikko
    ok = True
    tiedoston_nimi = input('Syötä fasta-tiedoston nimi: ')
    tiedosto = open(tiedoston_nimi, 'r')
    sekv = ''
    tarkistettu_sekv = ''
    for rivi in tiedosto:
        if len(rivi) > 0:
            if '>' in rivi:
                otsikkorivi = rivi
            else: sekv += rivi
    sekv = sekv.replace('\n','')
    for base in sekv:
        if base in DNA_bases:
            tarkistettu_sekv += base
    if tarkistettu_sekv != sekv or tarkistettu_sekv == '':
        print('''Sekvenssi oli viallinen. Tarkista tiedosto ja
    yritä uudelleen.''')
        ok = False
    else:
        sekvenssi = tarkistettu_sekv
        otsikko = otsikkorivi
    return ok

# Funktio joka kysyy käyttäjältä onko sekvenssi rengasmainen. Oletuksena
# lineaarinen, jolloin rengas = False
def onko_rengas():
    global rengas
    ok = False
    while ok == False:
        vastaus = input('''Onko sekvenssi lineaarinen(L) vai
    rengasmainen(R)? (oletus L): ''')
        if vastaus == 'R' or vastaus == 'r':
            rengas = True
            ok = True
        elif vastaus == 'L' or vastaus == 'l' or vastaus == '':
            rengas = False
            ok = True
        else:
            print('Syötä "L" tai "R", tai paina <Enter> käyttääksesi oletusta.')
    
# Funktio jolla valitaan sopiva lukuikkuna. Palauttaa valitun ikkunan koon,
# tai oletusarvon 100 jos käyttäjä painaa Enter tai syöttää epäkelvon arvon.
def valitse_ikkuna():
    lukuikkuna = 100 # Oletusarvo sata, sopii pienehköille sekvensseille
    valinta = input('Lukuikkunan koko, 1-10000 (oletus 100): ')
    if valinta == '':
        print('Käytetään oletuskokoista lukuikkunaa ' +str(lukuikkuna) + '.')
    else:
        valinta = int(valinta)
        if valinta > 0 and valinta <= 10000:
            lukuikkuna = valinta
            print('Käytetään lukuikkunaa ' +str(lukuikkuna) + '.')
        elif valinta <= 0:
            lukuikkuna = 1
            print('Liian pieni lukuikkuna. Käytetään minimikokoista lukuikkunaa ' +str(lukuikkuna) + '.')
        elif valinta > 10000:
            lukuikkuna = 10000
            print('Liian suuri lukuikkuna. Käytetään maksimikokoista lukuikkunaa ' +str(lukuikkuna) + '.')
    return lukuikkuna

# Funktio joka liikkuu sekvenssissä emäs kerrallaan (stepsize = 1) ja palauttaa sijainnin ikkunasekvenssin.
# Emäs sijaitsee lukuikkunan keskellä, paitsi lineaaristen sekvenssien
# päissä joissa lukuikkunasta jää osa (max. puolet) pois. 
def hae_ikkunan_sekvenssi(ikkunan_koko,sijainti):
    global sekvenssi
    global rengas
    ikkuna_sekvenssi = ''
    sekv_koko = len(sekvenssi)
    if sekv_koko < ikkunan_koko:
        ikkunan_koko = int(round(ikkunan_koko/100))
        print('''Valittu ikkuna on suurempi kuin koko sekvenssi. Käytetään
oletuksena ikkunankokoa ''' + ikkunan_koko + '.')
    puolikas_ikkuna = int(round(ikkunan_koko/2))
    # 1. Käsitellään ensin rengasmaiset sekvenssit
    if rengas == True:
        ylitys = ''
        # A. Tilanne jossa lukuikkuna sijaitsee sekvenssin alkupäässä:
        if sijainti < puolikas_ikkuna:
            ylitys = sijainti - puolikas_ikkuna
            ikkuna_sekvenssi += sekvenssi[ylitys:]
            ikkuna_sekvenssi += sekvenssi[:sijainti + puolikas_ikkuna]
            #print('A: lukuikkunan koko ' + str(len(ikkuna_sekvenssi)))
            return ikkuna_sekvenssi
        # B. Tilanne jossa lukuikkuna sijaitsee keskiosassa sekvenssiä: 
        elif sijainti >= puolikas_ikkuna and (sijainti + puolikas_ikkuna) < len(sekvenssi):
            ikkuna_sekvenssi += sekvenssi[(sijainti - puolikas_ikkuna):
                                          (sijainti + puolikas_ikkuna)]
            #print('B: lukuikkunan koko ' + str(len(ikkuna_sekvenssi)))
            return ikkuna_sekvenssi
        # C. Tilanne jossa lukuikkuna sijaitsee sekvenssin loppupäässä:
        elif  (sijainti + puolikas_ikkuna) >= len(sekvenssi):
            ylitys = len(sekvenssi) - sijainti
            ikkuna_sekvenssi += sekvenssi[(sijainti - puolikas_ikkuna):]
            ikkuna_sekvenssi += sekvenssi[:ylitys]
            #print('C: lukuikkunan koko ' + str(len(ikkuna_sekvenssi)))
            return ikkuna_sekvenssi
        else:
            print('Hups, määrittelemätön tilanne...')
            return
    # 2. Lineaariset sekvenssit, lukuikkuna on päissä pienempi          
    else:            
        # A. Tilanne jossa lukuikkuna sijaitsee sekvenssin alkupäässä:
        if sijainti < puolikas_ikkuna:
            ikkuna_sekvenssi += sekvenssi[:sijainti + puolikas_ikkuna]
            #print('A: lukuikkunan koko ' + str(len(ikkuna_sekvenssi)))
            return ikkuna_sekvenssi
        # B. Tilanne jossa lukuikkuna sijaitsee keskiosassa sekvenssiä: 
        elif sijainti >= puolikas_ikkuna and (sijainti + puolikas_ikkuna) < len(sekvenssi):
            ikkuna_sekvenssi += sekvenssi[(sijainti - puolikas_ikkuna):
                                          (sijainti + puolikas_ikkuna)]
            #print('B: lukuikkunan koko ' + str(len(ikkuna_sekvenssi)))
            return ikkuna_sekvenssi
        # C. Tilanne jossa lukuikkuna sijaitsee sekvenssin loppupäässä:
        elif  (sijainti + puolikas_ikkuna) >= len(sekvenssi):
            ikkuna_sekvenssi += sekvenssi[(sijainti - puolikas_ikkuna):]
            #print('C: lukuikkunan koko ' + str(len(ikkuna_sekvenssi)))
            return ikkuna_sekvenssi
        else:
            print('Hups, määrittelemätön tilanne...')
            return


# Funktio joka hoitaa GC-vinouman laskemisen annetussa lukukehyksessä. 
def laske_GC(ikkuna_sekv):
    count_A = 0 # A ja T nyt turhia, valmiina jos halutaan myös AT-vinouma
    count_C = 0
    count_G = 0
    count_T = 0
    for base in ikkuna_sekv:
        if base == 'A':
              count_A += 1
        elif base == 'C':
              count_C += 1
        elif base == 'G':
              count_G += 1
        elif base == 'T':
              count_T += 1
        else:
              print('Outoa, löytyi merkki joka ei ole emäs. Ohitetaan se.')
    # print('C: ' + str(count_C) + '\tG: ' + str(count_G)) #TEST(tulostaa paljon!)
    GC_osoittaja = count_G - count_C
    GC_nimittaja = count_G + count_C
    if GC_nimittaja == 0:
        GC_vinouma = 0 # Estetään nollalla jako
    else:
        GC_vinouma = GC_osoittaja/GC_nimittaja
    return GC_vinouma




# Tulostaa teksti-tiedostoon sekvenssin tietoineen ja GC-vinouman emäskohtaisesti.
def tulostaTXT():
    global sekvenssi
    global GC_vino
    tiedoston_nimi = input('Anna tulostiedostolle nimi: (Oletus tulokset.txt) ')
    if tiedoston_nimi == '':
        tiedoston_nimi = 'tulokset.txt'
    elif '.' not in tiedoston_nimi:
        tiedoston_nimi += '.txt'
    tiedosto = open(tiedoston_nimi, 'w')
    tiedosto.write(otsikko + '\n')
    if rengas == True:
        tiedosto.write('Rengasmainen sekvenssi.\n')
    else:
        tiedosto.write('Lineaarinen sekvenssi.\n')
    tiedosto.write('Sekvenssin pituus ' + str(len(sekvenssi)) + ' emästä.\n\n')
    # ja sitten kirjoitetaan vuororivein emäksiä ja GC-arvoja:
    indeksi_sekv = 0
    indeksi_GC = 0
    GC_arvo = 0.0
    GC_riville = False
    valmis = False
    tiedosto.write('1\n')
    while valmis == False:
        if (GC_riville == False and indeksi_sekv < len(sekvenssi)): 
            tiedosto.write(' ' + sekvenssi[indeksi_sekv] + 4*' ')
            indeksi_sekv += 1
           ## print('Päästiin kirjoittamaan emäksiä!!!') #TEST
            if indeksi_sekv%15 == 0 or indeksi_sekv >= len(sekvenssi):
                GC_riville = True
                tiedosto.write('\n')
        # GC-vinouma-rivi,kirjataan arvot etumerkkeineen:
        elif (GC_riville == True and indeksi_GC < len(GC_vino)):
            #print(GC_vino[indeksi_GC]) #TEST
            GC_arvo = GC_vino[indeksi_GC]
            if GC_arvo >= 0:
                tiedosto.write('+' + '%.2f' % GC_arvo + ' ')
            else:
                tiedosto.write('%.2f' % GC_arvo + ' ')
            indeksi_GC += 1
            if indeksi_GC%15 == 0:
                GC_riville = False
                tiedosto.write(2*'\n' + str(indeksi_GC + 1) + '\n')
        # Tänne tullaan kun kaikki on kirjattu
        else:
            valmis = True
    tiedosto.close()
    print('Valmista. Tulokset löytyvät tiedostosta ' + tiedoston_nimi + '.')
    print('''\n\nKiitos kun kokeilit tätä ohjelmaa. Se on kehitetty
Python-ohjelmoinnin peruskurssilla ja ohjelman toimintaan liittyviä kommentteja
otetaan mieluusti vastaan osoitteessa kaisa.saren@helsinki.fi.\nKaisa Saren, 2015.''')
    
# Ja vihdoin; tästä alkaa pääohjelma:
print('GC-VINOUMALASKURI')
print('-----------------')
print('Tällä ohjelmalla voit laskea fasta-muotoisen sekvenssin GC-vinouman.\n')
ok = lue_FASTA()
while ok == False:
    ok = lue_FASTA()
#print('fasta luettu!!!') #TEST
ikkunan_koko = valitse_ikkuna() #palauttaa halutun lukuikkunan koon
onko_rengas() #selvitetään rengasmaisuus...
#print('circular: ' + str(rengas)) #TEST
# sitten lasketaan...
for indeksi in range(len(sekvenssi)):
    GC_vino.insert(indeksi, laske_GC(hae_ikkunan_sekvenssi(ikkunan_koko, indeksi)))
    indeksi += 1
# Tulostetaan tiedot, TEST:
#ind = 0
#while ind< 1000:
    # print(GC_vino[ind])
    #ind += 1
tulostaTXT()
    



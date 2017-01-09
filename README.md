**Dokumentaatio GC-vinoumalaskuriin GC_scew.py**

Ohjelma, joka lukee sekvenssin tiedostosta ja tulostaa sekvenssin
GC-vinouman toiseen tiedostoon.

Lopputyö kurssille Python-ohjelmointia biotieteilijöolle
Helsingin Avoin Yliopisto, syyskuu 2015

Python-versio 3.4.

Tekijä: Kaisa Saren


**Ohjelman kuvaus:**
Ohjelma lukee käyttäjältä saamastaan fasta-muotoisesta tiedostosta sekvenssin, jolle se laskee GC-vinouman kaavalla (G-C)/(G+C). GC-vinouma vaihtelee välillä -1 -- +1, jossa negatiivinen kuvaa runsasta C-pitoisuutta ja positiivinen arvo runsasta G-pitoisuutta.
On hyvä tietää, että tässä ohjelmassa GC-vinouma asetetaan aina arvoon 0 tilanteessa, jossa tutkitussa lukuikkunassa ei ole lainkaan G:tä eikä C:tä, tämä on mahdollista erityisesti pienillä lukuikkunoilla.
Lisää GC-vinoumasta: *https://en.wikipedia.org/wiki/GC_skew*

Ohjelma pyytää käyttäjältä tietoa genomin mahdollisesta rengasmaisuudesta ja halutusta lukuikkunan koosta. Lukuikkuna siirtyy sekvenssissä emäs kerrallaan eteenpäin (stepsize = 1), eikä ohjelma siksi nykyisellään sovi erittäin suurten genomien laskentaan. 
Lukuikkuna voi olla kooltaan 1-10000, joskin aivan pienillä tai suhteessa sekvenssiin suurilla ikkunoilla tulokset eivät ole mielekkäitä. Mikäli lukuikkuna osoittautuu suuremmaksi kuin sekvenssi, se muutetaan oletuksena sadasosaan sekvenssin pituudesta. Huom! Taas, hyvin suurilla sekvensseillä näin suuri lukuikkuna johtaa hitaaseen laskentaan.

Laskettu GC-vinouma kunkin emäksen kohdalla on saatu sijoittamalla tarkasteltava emäs lukuikkunan keskelle. Sekvenssin alku- ja loppupäässä lukuikkuna on siksi lineaarisilla sekvensseillä pienempi, minimissään puolikas normaalista ensimmäisen ja viimeisen emäksen kohdalla. Rengasmaista sekvenssiä laskettaessa lukuikkuna kuitenkin ylettyy myös alku- ja lopukohdan yli.

Saadut tulokset tallennetaan tekstitiedostoon, jonka nimen käyttäjä voi valita tai käyttää oletusnimeä tulokset.txt. Ohjelma lisää automaattisesti käyttäjän syöttämän vastaustiedoston nimen perään .txt-päätteen, mikäli se tulkitsee ettei nimessä ole päätettä. **Huom! Ohjelma kirjoittaa kyselemättä myös olemassaolevien tiedostojen päälle.**

**Tiedetyt puutteet:**
- Ohjelma ei sovellu vielä hyvin erittäin isoille sekvensseille 
- Ohjelma kaatuu jos tiedostonimi on virheellinen
- Ohjelma kaatuu jos käyttäjä syöttää esimerkiksi lukuikkunan kooksi muuta kuin numeron.

Päivitetty 30.9.2015




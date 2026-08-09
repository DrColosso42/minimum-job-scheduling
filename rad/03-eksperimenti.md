# Eksperimentalni rezultati

Kako bismo olakšali kasniju interpretaciju rezultata, za početak ćemo dostaviti kontekstualne informacije o metodologiji usporedbe dve optimizacione metode, veličini eksperimenata i okruženju na kojima su eksperimenti pokretani.

## Okruženje za eksperimentisanje

Sve eksperimentalne skripte izvršavane su na privatnom računaru, čije se najznačajnije karakteristike nalaze u sledećoj tabeli:

| komponenta                | vrednost                                            |
| ------------------------- | --------------------------------------------------- |
| procesor                  | Intel Core Ultra 7 165U                             |
| frekvencija               | 3,71 GHz                                            |
| broj jezgara              | 12 fizičkih / 14 logičkih                           |
| radna memorija            | 62,2 GB                                             |
| operativni sistem         | Ubuntu 24.04.4 LTS, 7.0.0-28-generic kernel, x86-64 |
| standardna biblioteka     | glibc 2.39                                          |
| programski jezik          | Python 3.12.3, GCC 13.3.0                           |
| egzaktni rešavač          | IBM ILOG CPLEX 22.2.0.0                             |
| biblioteka za modelovanje | PuLP 3.3.2                                          |

: Karakteristike računara na kome su izvršena sva merenja.\label{tbl:okruzenje}

Vredi napomenuti da su sve razvijene metaheuristike implementirane tako da se izvršavaju na **jednoj niti** bez mogućnosti paralelizacije.
Egzaktni rešavač (CPLEX) pokretan je sa podrazumevanim brojem niti, dakle sa svih 14 logičkih
jezgara. Zbog te razlike, metode je najpreciznije porediti na osnovu broja poziva funkcije dekodiranja,
a ne po utrošenom vremenu. Dužina izvršavanja navedena je kao dodatni, orijentacioni podatak.

## Test instance

Pri evaluaciji razvijenih metoda korišćeno je devet različitih test instanci. Od njih devet, osam je preuzeto iz zbirke OR-Library [@beasley1990]. Instance `ft06`, `ft10` i `ft20` potiču iz rada [@fisher1963], dok instance `la01`--`la05` dolaze iz [@lawrence1984]. Poslednja, deveta, instanca `mini3` kreirana je za potrebe ovog rada. Predstavlja relativno malu instancu čiji se optimum može pronaći algoritmom grube sile. Kao takva služila je najpre pri validaciji ispravnosti implementiranih metoda optimizacije.
Pregled najvažnijih informacija o svim instancama dat je u narednoj tabeli.

| instanca |  $n \times m$  | operacija | donja granica | optimum | izvor optimuma   |
| -------- | :------------: | --------: | ------------: | ------: | ---------------- |
| `mini3`  |  $3 \times 3$  |         9 |            10 |      11 | iscrpna pretraga |
| `ft06`   |  $6 \times 6$  |        36 |            47 |      55 | [@fisher1963]    |
| `la01`   | $10 \times 5$  |        50 |       **666** |     666 | donja granica    |
| `la02`   | $10 \times 5$  |        50 |           635 |     655 | [@lawrence1984]  |
| `la03`   | $10 \times 5$  |        50 |           588 |     597 | [@lawrence1984]  |
| `la04`   | $10 \times 5$  |        50 |           537 |     590 | [@lawrence1984]  |
| `la05`   | $10 \times 5$  |        50 |       **593** |     593 | donja granica    |
| `ft10`   | $10 \times 10$ |       100 |           655 |     930 | [@fisher1963]    |
| `ft20`   | $20 \times 5$  |       100 |          1119 |    1165 | [@fisher1963]    |

: Test instance sa dimenzijama, donjim granicama i objavljenim optimalnim
vrednostima.\label{tbl:instance}

Donja granica u tabeli \ref{tbl:instance} predstavlja veću od dve trivijalne
granice: (1) najdužeg posla i (2) najopterećenije mašine. Način računanja detaljno je opisan u odeljku
o donjim granicama. Kod instanci `la01` i `la05` ta granica se poklapa sa optimumom,
pa svako rešenje koje je dostigne ujedno i **dokazuje** svoju optimalnost, bez potrebe
za egzaktnim rešavačem.

Instance su izabrane tako da pokriju što širi opseg težine. Konkretno, `mini3` i `ft06` sve razvijene
metode rešavaju do optimuma, pa služe kao provera ispravnosti. Instance `la01`--`la05`
razdvajaju metode po pouzdanosti. `ft10` i `ft20` su, uprkos skromnim dimenzijama,
poznato teške. Instanca `ft10` je ostala nerešena punih dvadeset šest godina nakon
objavljivanja [@jain1999].

## Metodologija

Za početak je potrebno objasniti način izbora veličine eksperimenta. Bilo je potrebno održati balans između validnosti rezultata i razumne upotrebe (pre svega vremenskih) resursa. Sa jedne strane, ne možemo dopustiti da eksperimente izvršavamo na premalom uzorku i time dovedemo u pitanje opštost zaključaka, dok je sa druge strane potrebno da se eksperimenti izvrše u razumnom vremenskom roku.

### Budžet umesto vremena

Kao što je ranije navedeno, zbog nedostatka konkurentnosti u implementacijama algoritama, efikasnost različitih optimizacionih metoda nije pogodno upoređivati sa egzaktnim rešavačem na osnovu vremena izvršavanja. Kod međusobnog poređenja situacija je nešto bolja, ali se pokazalo veoma izazovno unapred dozvoliti funkciji određeni vremenski okvir^[Pre svega izazovnost se ogleda u činjenici da isti vremenski okvir na istoj mašini u različitim metodama podrazumeva različit broj koraka.], pa je vreme izvršavanja zauzelo ulogu _retrospektivne mere_, dok su sami algoritmi unapred ograničeni brojem poziva funkcije dekodiranja.

Svakom algoritmu je unapred data gornja granica broja poziva ove funkcije i taj broj nazivamo _budžetom_. Kao što možemo videti na slici \ref{sl:budzet}, prosečan rezultat nastavlja blago da se popravlja i nakon izabrane granice. Međutim, poredak metoda ostaje nepromenjen a preciznije apsolutne vrednost zahtevaju nesrazmerno veći budžet. S tim na umu, izabrani budžet predstavlja kompromis između kvaliteta rešenja i ukupnog trajanje eksperimenta. Primećujemo da se vreme izvršavanja optimizacionog metoda razlikuje i pri istom budžetu, a razlog tome nalazi se u specifičnostima samih algoritama, gde se vreme „rasipa“ na pozive drugih pomoćnih metoda.

![Prosečna vrednost funkcije cilja u zavisnosti od dodeljenog budžeta, za dve
najteže instance. Obe ose prikazane su za pet nezavisnih pokretanja po tački.
Uspravna isprekidana linija označava budžet usvojen u ostatku rada.
\label{sl:budzet}](slike/budget.png){width=100%}

### Broj ponavljanja

Po uzoru na literaturu o metaheuristikama, usvojen je izbor od **30 nezavisnih pokretanja** svake metode nad svakom instancom. Uz devet instanci i četiri različite metode dolazimo do ukupno **1080 pokretanja**. Ovo predstavlja dovoljno veliki uzorak za smisleni prikaz različitih osobina dobijenih rezultata, najpre: prosek, standardnu devijaciju, procenat dostizanja optimuma i slične.

### Stohastičnost i reproducibilnost

Svako pokretanje optimizacionog problema u sebi sadrži stohastičnost u vidu **nasumičnog izbora početnog rešenja**. Pored toga, sve četiri metode na stohastičnost nailaze i u drugim delovima svoje implementacije, što nas navodi da je potrebno detaljnije obraditi
pitanje **reproducibilnosti** rezultata.

Konkretno, postavljanjem iste početne vrednosti za generator pseudonasumičnih brojeva (engl. _seed_) omogućena je potpuna reproducibilnost svih dobijenih rezultata. Ponovno pokretanje priloženog koda dovodi do identičnih rezultata. Takođe _seed_ vrednost sačuvana je u priloženim datotekama pa je moguće reprodukovati, ne samo eksperiment, već i jedno zasebno pokretanje optimizacione metode.

## Rezultati testiranja

Dobijeni rezultati prikazani su kroz tri naredne tabele.
U prvoj tabeli nalazi se **najbolje pronađeno rešenje** kroz **svih 30 pokretanja**. U drugoj tabeli vidimo prosek i standardnu devijaciju, dok treća tabela nosi informaciju o broju pokretanja u kojima je optimum dostignut.

U prvoj tabeli jasno je izražena informacija o mogućnosti (potencijalu) metode da pronađe najbolje rešenje. Kroz drugu i treću tabelu se ogleda pouzdanost različitih metoda pri višestrukoj upotrebi.

| instanca | optimum | kaljenje |     VNS |      GA | lok. pretraga |
| -------- | ------: | -------: | ------: | ------: | ------------: |
| `mini3`  |      11 |   **11** |  **11** |  **11** |        **11** |
| `ft06`   |      55 |   **55** |  **55** |  **55** |        **55** |
| `la01`   |     666 |  **666** | **666** | **666** |       **666** |
| `la02`   |     655 |  **655** | **655** | **655** |           663 |
| `la03`   |     597 |  **597** | **597** |     604 |       **597** |
| `la04`   |     590 |  **590** | **590** | **590** |           594 |
| `la05`   |     593 |  **593** | **593** | **593** |       **593** |
| `ft10`   |     930 |      937 |     971 |     961 |          1002 |
| `ft20`   |    1165 |     1173 |    1192 |    1180 |          1249 |

: Najbolje pronađeno rešenje kroz 30 pokretanja. Podebljane vrednosti poklapaju se sa
objavljenim optimumom.\label{tbl:najbolje}

| instanca |      kaljenje |           VNS |            GA | lok. pretraga |
| -------- | ------------: | ------------: | ------------: | ------------: |
| `mini3`  |    11,0 ± 0,0 |    11,0 ± 0,0 |    11,0 ± 0,0 |    11,0 ± 0,0 |
| `ft06`   |    55,0 ± 0,0 |    55,0 ± 0,0 |    55,0 ± 0,0 |    55,0 ± 0,0 |
| `la01`   |   666,0 ± 0,0 |   666,0 ± 0,0 |   670,9 ± 8,9 |   666,0 ± 0,0 |
| `la02`   |   659,0 ± 5,7 |   660,7 ± 6,6 |   669,9 ± 9,4 |   674,5 ± 9,0 |
| `la03`   |   606,2 ± 7,4 |   607,6 ± 7,0 |  625,6 ± 14,2 |   623,9 ± 9,9 |
| `la04`   |   591,2 ± 2,0 |   594,1 ± 4,2 |  606,0 ± 14,2 |   607,5 ± 7,3 |
| `la05`   |   593,0 ± 0,0 |   593,0 ± 0,0 |   593,0 ± 0,0 |   593,0 ± 0,0 |
| `ft10`   |  965,2 ± 16,3 | 1023,8 ± 24,7 | 1012,1 ± 30,9 | 1059,6 ± 30,0 |
| `ft20`   | 1183,8 ± 11,1 | 1245,8 ± 29,9 | 1221,0 ± 26,6 | 1320,1 ± 40,9 |

: Prosečna vrednost funkcije cilja kroz 30 pokretanja, sa standardnom
devijacijom.\label{tbl:prosek}

| instanca | kaljenje | VNS |  GA | lok. pretraga |
| -------- | -------: | --: | --: | ------------: |
| `mini3`  |       30 |  30 |  30 |            30 |
| `ft06`   |       30 |  30 |  30 |            30 |
| `la01`   |       30 |  30 |  20 |            30 |
| `la02`   |       19 |  16 |   2 |             0 |
| `la03`   |        5 |   3 |   0 |             1 |
| `la04`   |       21 |  11 |   4 |             0 |
| `la05`   |       30 |  30 |  30 |            30 |
| `ft10`   |        0 |   0 |   0 |             0 |
| `ft20`   |        0 |   0 |   0 |             0 |

: Broj pokretanja, od ukupno 30, u kojima je dostignut poznati
optimum.\label{tbl:pogodaka}

Tabela \ref{tbl:najbolje} pokazuje da instance `mini3`, `ft06` i `la05` sve tri metode rešavaju do optimuma. Standardna devijacija na njima je nula (tabela \ref{tbl:prosek}), pa te instance ne razdvajaju metode i služe isključivo kao provera ispravnosti implementacije.

Poređenje metoda isključivo po najboljem pronađenom rešenju prikriva stvarnu informaciju o upotrebljivosti metode. Na primer, pri rešavanju instance `la03` sve metode, osim genetskog algoritma, dostižu optimum. Ipak, tabela \ref{tbl:pogodaka} pokazuje da ga lokalna pretraga pronalazi **u samo jednom od trideset pokretanja**, dok simulirano kaljenje to uspeva pet puta. Zbog toga je pri poređenju metoda potrebno uzeti u obzir i njihovo generalno ponašanje. Nepouzdano je ograničiti se samo na najbolje primere.

Na instancama `la02`, `la03` i `la04` razlike su najizraženije. Kaljenje dostiže optimum redom 19, 5 i 21 put, promenljive okoline 16, 3 i 11 puta, dok lokalna pretraga ne uspeva
gotovo nikada.

Instanca `la03` se u rezultatima izdvaja. Naime, iako je istih dimenzija kao `la02` i `la04`, sve metode je rešavaju znatno teže. Uzrok nije utvrđen u okviru ovog rada.

Na najvećim instancama, `ft10` i `ft20`, nijedna metoda ne dostiže objavljeni optimum. Ipak, simulirano kaljenje je i tu najbliže, sa prosečnim odstupanjem od 3,8% odnosno 1,6%.

![Rasipanje vrednosti funkcije cilja kroz 30 pokretanja, po instanci i metodi.
Kutija obuhvata srednjih 50% rezultata, linija u njoj je medijana, a kružići označavaju anomalije.\label{sl:rasipanje}](slike/box_chart.png){width=100%}

Posmatrano na svim instancama, prosečno odstupanje od optimuma iznosi 0,86% za kaljenje, 2,26% za promenljive okoline, 2,68% za genetski algoritam i 4,19% za lokalnu pretragu sa ponovnim pokretanjem. Poredak je isti u sve tri tabele, što ga čini pouzdanim zaključkom.

## Egzaktno rešavanje

Radi provere ispravnosti razvijenih metoda i utvrđivanja stvarnih optimuma, problem je rešen i egzaktno, celobrojnim linearnim programiranjem. Korišćena je disjunktivna
formulacija [@manne1960], opisana u odeljku o celobrojnom modelu, dok je model rešen putem
rešavača CPLEX. Pritom, svakoo pokretanje vremenski je unapred ograničeno na jedan sat i zahtevana je stroga optimalnost. Rezultati egzaktnog rešavanja dati su u sledećoj tabeli:

| instanca | promenljivih | ograničenja | rešenje | donja granica | procep | vreme [s] |
| -------- | -----------: | ----------: | ------: | ------------: | -----: | --------: |
| `mini3`  |           19 |          27 |  **11** |            11 |      0 |       0,1 |
| `ft06`   |          127 |         216 |  **55** |            55 |      0 |       0,3 |
| `la01`   |          276 |         500 | **666** |           666 |      0 |       5,2 |
| `la02`   |          276 |         500 | **655** |           655 |      0 |       3,0 |
| `la03`   |          276 |         500 | **597** |           597 |      0 |       2,7 |
| `la04`   |          276 |         500 | **590** |           590 |      0 |       1,6 |
| `la05`   |          276 |         500 | **593** |           593 |      0 |       9,8 |
| `ft10`   |          551 |        1000 | **930** |           930 |      0 |      50,8 |
| `ft20`   |         1051 |        2000 |    1182 |           657 | 44,4 % |    > 3600 |

: Rezultati egzaktnog rešavanja. Podebljane vrednosti su dokazano optimalne.\label{tbl:ilp}

Osam od devet instanci rešeno je do dokazane optimalnosti i sve dobijene vrednosti
poklapaju se sa objavljenim optimumima iz tabele \ref{tbl:instance}. Ovime je nezavisno potvrđeno da implementirani dekoder ne proizvodi neizvodljive rasporede.

Primetimo da vreme rešavanja raste izrazito brzo sa veličinom instance: 0,3 sekunde za `ft06`, oko 3 sekunde za instance `la01`--`la05`, 50,8 sekundi za `ft10`, dok `ft20` nije
rešen ni nakon sat vremena. Upravo ovde vidimo najveću vrednost metaheuristika.

![Vreme rešavanja celobrojnog modela u zavisnosti od broja promenljivih.
Vertikalna osa je logaritamska. Instanca `ft20` nije rešena u zadatom roku od sat vremena, pa njena vrednost predstavlja donju procenu potrebnog
vremena.\label{sl:ilp-rast}](slike/ilp_rast.png){width=95%}

Posvetimo na kratko pažnju instanci `ft20`. Nakon sat vremena rešavač je pronašao rešenje vrednosti 1182 i dokazao donju granicu 657. U pitanju je razilaženje od preko 44%. Poređenja radi,
simulirano kaljenje je u istom okruženju pronašlo rešenje vrednosti 1173 za oko pet
sekundi. Rezultat je da je primenom metode optimizacije putem metaheuristika pronađeno **bolje rešenje u vremenu manjem za tri reda veličine**.

Pored toga, jednostavna donja granica opisana u odeljku o donjim granicama iznosi za `ft20` **1119**, što je znatno jače ograničenje od granice 657 koju je rešavač dokazao za sat
vremena. Kombinovanjem te granice sa najboljim pronađenim rešenjem dobija se interval $[1119, 1173]$, odnosno raskol od 4,6% umesto 44,37%.

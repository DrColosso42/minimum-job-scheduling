# Eksperimentalni rezultati

Kako bismo olakšali kasniju interpretaciju rezultata, za početak ćemo dostaviti kontekstualne informacije o metodologiji usporedbe dve optimizacione metode, veličini eksperimenata i okruženju na kojima su eksperimenti pokretani.

## Okruženje za eksperimentisanje

Sve eksperimentalne skripte izvršavane su na privatnom računaru, čije se najznačajnije karakteristike nalaze u sledećoj tabeli:

| komponenta                | vrednost                                            |
| ------------------------- | --------------------------------------------------- |
| procesor                  | Intel Core Ultra 7 165U                             |
| frekvencija               | 0,4 -- 4,9 GHz                                      |
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

Primetićemo ipak, a što će biti detaljnije obrađeno kasnije, da ovaj izbor normalizacije povlači sa sobom pristrasnost prema metodama koje zahtevaju manji broj poziva funkcije cilja po koraku, što im omogućava da dosegnu nešto dalje od metoda koje nemaju tu osobinu.

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
| `la02`   |     655 |  **655** | **655** |     660 |           663 |
| `la03`   |     597 |  **597** | **597** |     603 |       **597** |
| `la04`   |     590 |  **590** | **590** | **590** |           594 |
| `la05`   |     593 |  **593** | **593** | **593** |       **593** |
| `ft10`   |     930 |      937 |     971 |     956 |          1002 |
| `ft20`   |    1165 | **1165** |    1192 |    1185 |          1249 |

: Najbolje pronađeno rešenje kroz 30 pokretanja. Podebljane vrednosti poklapaju se sa
objavljenim optimumom.\label{tbl:najbolje}

| instanca |     kaljenje |           VNS |            GA | lok. pretraga |
| -------- | -----------: | ------------: | ------------: | ------------: |
| `mini3`  |   11,0 ± 0,0 |    11,0 ± 0,0 |    11,0 ± 0,0 |    11,0 ± 0,0 |
| `ft06`   |   55,0 ± 0,0 |    55,0 ± 0,0 |    55,2 ± 0,8 |    55,0 ± 0,0 |
| `la01`   |  666,0 ± 0,0 |   666,0 ± 0,0 |   670,0 ± 8,2 |   666,0 ± 0,0 |
| `la02`   |  659,4 ± 5,7 |   660,7 ± 6,6 |  673,3 ± 11,1 |   674,5 ± 9,0 |
| `la03`   |  602,1 ± 4,0 |   607,6 ± 7,0 |  623,8 ± 10,1 |   623,9 ± 9,9 |
| `la04`   |  591,7 ± 2,9 |   594,1 ± 4,2 |   602,2 ± 7,7 |   607,5 ± 7,3 |
| `la05`   |  593,0 ± 0,0 |   593,0 ± 0,0 |   593,0 ± 0,0 |   593,0 ± 0,0 |
| `ft10`   | 959,2 ± 14,3 | 1023,8 ± 24,7 | 1021,7 ± 32,2 | 1059,6 ± 30,0 |
| `ft20`   | 1180,8 ± 7,3 | 1245,8 ± 29,9 | 1229,2 ± 23,9 | 1320,1 ± 40,9 |

: Prosečna vrednost funkcije cilja kroz 30 pokretanja, sa standardnom
devijacijom.\label{tbl:prosek}

| instanca | kaljenje | VNS |  GA | lok. pretraga |
| -------- | -------: | --: | --: | ------------: |
| `mini3`  |       30 |  30 |  30 |            30 |
| `ft06`   |       30 |  30 |  28 |            30 |
| `la01`   |       30 |  30 |  19 |            30 |
| `la02`   |       18 |  16 |   0 |             0 |
| `la03`   |        8 |   3 |   0 |             1 |
| `la04`   |       21 |  11 |   3 |             0 |
| `la05`   |       30 |  30 |  30 |            30 |
| `ft10`   |        0 |   0 |   0 |             0 |
| `ft20`   |        1 |   0 |   0 |             0 |

: Broj pokretanja, od ukupno 30, u kojima je dostignut poznati
optimum.\label{tbl:pogodaka}

Tabela \ref{tbl:najbolje} pokazuje da instance `mini3`, `ft06` i `la05` sve četiri rešavaju do optimuma. Standardna devijacija na njima je nula (tabela \ref{tbl:prosek}), uz jedini izuzetak genetskog algoritma na instanci `ft06`, koji u dva od trideset pokretanja završi sa vrednostima 57 i 59. Te instance stoga gotovo da ne razdvajaju metode i služe pre svega kao provera ispravnosti implementacije.

Poređenje metoda isključivo po najboljem pronađenom rešenju prikriva stvarnu informaciju o upotrebljivosti metode. Na primer, pri rešavanju instance `la03` sve metode, osim genetskog algoritma, dostižu optimum. Ipak, tabela \ref{tbl:pogodaka} pokazuje da ga lokalna pretraga pronalazi **u samo jednom od trideset pokretanja**, dok simulirano kaljenje to uspeva osam puta. Zbog toga je pri poređenju metoda potrebno uzeti u obzir i njihovo generalno ponašanje. Nepouzdano je ograničiti se samo na najbolje primere.

Na instancama `la02`, `la03` i `la04` razlike su najizraženije. Kaljenje dostiže optimum redom 18, 8 i 21 put, promenljive okoline 16, 3 i 11 puta, dok lokalna pretraga ne uspeva
gotovo nikada.

Instanca `la03` se u rezultatima izdvaja. Naime, iako je istih dimenzija kao `la02` i `la04`, sve metode je rešavaju znatno teže. Uzrok nije utvrđen u okviru ovog rada.

Na najvećim instancama, `ft10` i `ft20`, nijedna metoda ne dostiže objavljeni optimum pouzdano. Jedini pogodak je kaljenje na instanci `ft20`, i to u samo jednom od trideset pokretanja. Simulirano kaljenje je i tu najbliže, sa prosečnim odstupanjem od 3,1% odnosno 1,4%.

![Rasipanje vrednosti funkcije cilja kroz 30 pokretanja, po instanci i metodi.
Kutija obuhvata srednjih 50% rezultata, linija u njoj je medijana, a kružići označavaju odudarajuće vrednosti (_engl. outliers_).\label{sl:rasipanje}](slike/box_chart.png){width=100%}

Posmatrano na svim instancama, prosečno odstupanje od optimuma iznosi 0,70% za kaljenje, 2,26% za promenljive okoline, 2,85% za genetski algoritam i 4,19% za lokalnu pretragu sa ponovnim pokretanjem.
Poredak je isti u sve tri tabele, što ga čini prihvatljivim zaključkom.

## Uticaj vrednosti parametara

Svaka od implementiranih metoda, pored početne tačke, zavisi i od nekih, sebi specifičnih, parametara. Vrednosti tih parametara do sada su birane po preporukama iz arhitekture, ali je potrebno i eksperimentalno potvrditi njihovu validnost i uspešnost.

### Postavka

U eksperimentu je testiran **po jedan parametar u svakom trenutku**, dok su svi ostali parametri zadržali fiksirane vrednosti. Za svaki testirani parametar izabrano je po nekoliko vrednosti oko podrazumevane tako da opseg testiranja pokrije što raznovrsnije vrednosti uz razumno vreme izvršavanja testa.

| metoda   | parametar         | značenje                              |
| -------- | ----------------- | ------------------------------------- |
| kaljenje | `T0`              | početna temperatura                   |
| VNS      | `kmax`            | najveća okolina                       |
| GA       | `population_size` | veličina populacije                   |
| GA       | `p`               | verovatnoća mutacije                  |
| GA       | `tournament_pct`  | veličina turnira, kao udeo populacije |

: Ispitivani parametri.\label{tbl:parametri-opis}

Merenje je sprovedeno nad trima instancama: `la03`, `ft10` i `ft20`. Izabrane su konkretne instance zbog toga što glavni ekperiment pokazuje da se na njima vidi najveća varijacija pri različitim metodama.

Takođe, poput glavnog eksperimenta, metode su pokretane sa budžetom od 200 000 poziva dekodera po deset puta za svaki parametar. Pri tome se koristi isti generator tako da su svi ostali uslovi identični.

### Rezultati

| metoda   | parametar         | vrednost | `la03` | `ft10` | `ft20` | odstupanje |       $p$ |
| -------- | ----------------- | -------: | -----: | -----: | -----: | ---------: | --------: |
| kaljenje | `T0`              |        5 |  602,6 |  982,4 | 1183,1 |      2,7 % | **0,009** |
| kaljenje | `T0`              |       20 |  602,1 |  956,7 | 1180,7 |      1,7 % |       --- |
| kaljenje | `T0`              |       50 |  603,6 |  959,4 | 1182,2 |      1,9 % |     0,449 |
| kaljenje | `T0`              |      100 |  601,2 |  957,4 | 1180,2 |      1,7 % |     0,926 |
| VNS      | `kmax`            |        2 |  610,7 | 1022,3 | 1267,7 |      7,0 % |     0,923 |
| VNS      | `kmax`            |        5 |  605,9 | 1040,7 | 1263,6 |      7,3 % |     0,181 |
| VNS      | `kmax`            |       10 |  606,6 | 1031,4 | 1263,8 |      7,0 % |       --- |
| VNS      | `kmax`            |       20 |  609,7 | 1031,4 | 1263,8 |      7,2 % |     0,064 |
| GA       | `population_size` |       20 |  626,0 | 1008,0 | 1233,2 |      6,4 % |     0,880 |
| GA       | `population_size` |       50 |  625,4 | 1015,7 | 1229,2 |      6,5 % |       --- |
| GA       | `population_size` |      100 |  622,3 | 1026,9 | 1226,7 |      6,7 % |     0,712 |
| GA       | `population_size` |      200 |  619,9 | 1024,6 | 1252,3 |      7,2 % |     0,213 |
| GA       | `p`               |      0,1 |  623,1 | 1050,0 | 1245,6 |      8,1 % | **0,017** |
| GA       | `p`               |      0,3 |  625,4 | 1015,7 | 1229,2 |      6,5 % |       --- |
| GA       | `p`               |      0,5 |  620,2 | 1001,5 | 1227,7 |      5,7 % |     0,264 |
| GA       | `p`               |      0,7 |  620,7 | 1002,7 | 1230,1 |      5,8 % |     0,224 |
| GA       | `tournament_pct`  |      0,1 |  623,2 | 1006,9 | 1224,8 |      5,9 % |     0,419 |
| GA       | `tournament_pct`  |      0,3 |  625,4 | 1015,7 | 1229,2 |      6,5 % |       --- |
| GA       | `tournament_pct`  |      0,6 |  624,0 | 1007,6 | 1234,5 |      6,3 % |     0,802 |

: Prosečna vrednost funkcije cilja po instanci i prosečno odstupanje od optimuma, kroz
10 pokretanja. Red bez vrednosti $p$ je podrazumevana vrednost, prema kojoj se ostale
porede.\label{tbl:parametri}

Primetno je da su odstupanja dosta veća nego tabeli \ref{tbl:prosek}, što je uzrokovano izborom tri najteže instance. One koje
metode lako rešavaju do optimuma ovde nisu iskorišćene.

### Provera značajnosti

Upoređivanje proseka ovde nije nužno dovoljno za pouzdanu analizu. Razlike između parametara su reda nekoliko jedinica, a
standardna devijacija je kroz ponavljanja oko 30, što nam govori da neki rezultati mogu biti postignuti samo usled slučajnosti.

Srećom, pokretanja se mogu porediti i u parovima, zbog korišćenja iste vrednosti generatora. Formirano je trideset razlika
u odnosu na podrazumevanu. Dobijeni rezultat jeste tabela u kojoj parametar $p$ govori kolika je verovatnoća da bi se razlika
te veličine dobila slučajno.

Ova analiza pokazuje da samo dva para postižu prag od 0,05:

- simulirano kaljenje pri $T_0 = 5$ je lošije za 9,53 jedinice u proseku, $p = 0{,}009$
- genetski algoritam pri $p_m = 0{,}1$ je lošiji za 16,13 jedinica, $p = 0{,}017$

Sve ostale vrednosti, uključujući i one koje u tabeli izgledaju bolje od podrazumevanih, ne razlikuju se značajno. Konkretno, $T_0 = 100$ i $p_m = 0{,}5$ imaju naizgled niže odstupanje, ali su im $p$ vrednosti 0,926 i 0,264, pa se ta prednost ne može tvrditi.

### Tumačenje

Rezultat analize govori nam da na su izabrane metode gotovo **neosetljive na izbor parametara u širokom opsegu**, ali postoji
donji prag ispod koga metode postaju značajno nepouzdanije.

Oba statistički značajna slučaja su upravo slučajevi donje granice i oba imaju jasno objašnjenje. Pri $T_0 = 5$ je verovatnoća prihvatanja lošijeg rešenja izuzetno mala, pa kaljenje ne može da pobegne lokalnim optimumima. Slično, pri $p_m = 0{,}1$ mutacija ima nedovoljno visoku šansu dešavanja pa raznovrsnost populacije ostaje ograničena početnom populacijom i algoritam daje loše rezultate.

Metoda promenljivih okolina pokazala se potpuno neosetljivom na izbor parametra $k_{max}$. Ne postoji statistički značajna razlika između vrednosti 2 i 20. Ovde vredi primetiti da su veće okoline potencijalno ograničene budžetom, s obzirom da pretraga ne stigne da istraži udaljene tačke pre nego joj ponestane budžeta.

Praktična posledica jeste da fini izbor parametra iz odeljka o metodologiji ne utiče presudno na rezultate metode, sve dok je on
u prihvatljivom opsegu, pa zaključci iz prethodnog odeljka ne zavise od izbora.

## Egzaktno rešavanje

Radi provere ispravnosti razvijenih metoda i utvrđivanja stvarnih optimuma, problem je rešen i egzaktno, celobrojnim linearnim programiranjem. Korišćena je disjunktivna
formulacija [@manne1960], opisana u odeljku o celobrojnom modelu, dok je model rešen putem
rešavača CPLEX. Pritom, svakoo pokretanje vremenski je unapred ograničeno na jedan sat i zahtevana je stroga optimalnost. Rezultati egzaktnog rešavanja dati su u sledećoj tabeli:

| instanca | promenljivih | ograničenja | rešenje | donja granica | odstupanje | vreme [s] |
| -------- | -----------: | ----------: | ------: | ------------: | ---------: | --------: |
| `mini3`  |           19 |          27 |  **11** |            11 |          0 |       0,1 |
| `ft06`   |          127 |         216 |  **55** |            55 |          0 |       0,3 |
| `la01`   |          276 |         500 | **666** |           666 |          0 |       5,2 |
| `la02`   |          276 |         500 | **655** |           655 |          0 |       3,0 |
| `la03`   |          276 |         500 | **597** |           597 |          0 |       2,7 |
| `la04`   |          276 |         500 | **590** |           590 |          0 |       1,6 |
| `la05`   |          276 |         500 | **593** |           593 |          0 |       9,8 |
| `ft10`   |          551 |        1000 | **930** |           930 |          0 |      50,8 |
| `ft20`   |         1051 |        2000 |    1182 |           657 |     44,4 % |    > 3600 |

: Rezultati egzaktnog rešavanja. Podebljane vrednosti su dokazano optimalne.\label{tbl:ilp}

Osam od devet instanci rešeno je do dokazane optimalnosti i sve dobijene vrednosti
poklapaju se sa objavljenim optimumima iz tabele \ref{tbl:instance}. Ovime je nezavisno potvrđeno da implementirani dekoder ne proizvodi neizvodljive rasporede.

Primetimo da vreme rešavanja raste izrazito brzo sa veličinom instance: 0,3 sekunde za `ft06`, oko 3 sekunde za instance `la01`--`la05`, 50,8 sekundi za `ft10`, dok `ft20` nije
rešen ni nakon sat vremena. Upravo ovde vidimo najveću vrednost metaheuristika.

![Vreme rešavanja celobrojnog modela u zavisnosti od broja promenljivih.
Vertikalna osa je logaritamska. Instanca `ft20` nije rešena u zadatom roku od sat vremena, pa njena vrednost predstavlja donju procenu potrebnog
vremena.\label{sl:ilp-rast}](slike/ilp_rast.png){width=95%}

Posvetimo na kratko pažnju instanci `ft20`. Nakon sat vremena rešavač je pronašao rešenje vrednosti 1182 i dokazao donju granicu 657. U pitanju je razilaženje od preko 44%. Poređenja radi,
simulirano kaljenje je u istom okruženju pronašlo rešenje vrednosti 1165 za nepunih šest
sekundi. Rezultat je da je primenom metode optimizacije putem metaheuristika pronađeno **bolje rešenje u vremenu manjem za tri reda veličine**.

Pored toga, jednostavna donja granica opisana u odeljku o donjim granicama iznosi za `ft20` **1119**, što je znatno jače ograničenje od granice 657 koju je rešavač dokazao za sat
vremena. Kombinovanjem te granice sa najboljim pronađenim rešenjem dobija se interval $[1119, 1165]$, odnosno raskol od 4,1% umesto 44,37%.

## Poređenje sa rezultatima iz literature

U cilju procene realne upotrebljivosti razvijenih metoda, njihovi rezultati upoređeni su sa optimalnim vrednostima objavljenim u literaturi. Za instance iz zbirke OR-Library te vrednosti su odavno poznate i dosegnute su specijalizovanim metodama, između ostalih egzaktnim algoritmima granjanja i ograđivanja, i tabu pretragom
prilagođenom strukturi problema.

Na osam od devet instanci simulirano kaljenje dostiže objavljeni optimum, s tim da ga na instanci `ft20` pronalazi u samo jednom od trideset pokretanja. Jedina instanca na kojoj optimum nije dostignut je `ft10`, gde odstupanje iznosi 0,75%.

| instanca | optimum | najbolje (kaljenje) | odstupanje |     ILP | odstupanje |
| -------- | ------: | ------------------: | ---------: | ------: | ---------: |
| `mini3`  |      11 |              **11** |          0 |  **11** |          0 |
| `ft06`   |      55 |              **55** |          0 |  **55** |          0 |
| `la01`   |     666 |             **666** |          0 | **666** |          0 |
| `la02`   |     655 |             **655** |          0 | **655** |          0 |
| `la03`   |     597 |             **597** |          0 | **597** |          0 |
| `la04`   |     590 |             **590** |          0 | **590** |          0 |
| `la05`   |     593 |             **593** |          0 | **593** |          0 |
| `ft10`   |     930 |                 937 |     0,75 % | **930** |          0 |
| `ft20`   |    1165 |            **1165** |          0 |    1182 |     1,46 % |

: Poređenje najboljih pronađenih rešenja sa objavljenim optimumima. Podebljane
vrednosti poklapaju se sa optimumom.\label{tbl:literatura}

Na osnovu priloženih rezultata jasno se vidi da razvijene metode ipak **ne nadmašuju rezultate iz literature**. Objavljene vrednosti za instance `ft10` i `ft20` dostignute su metodima koji pri optimizaciji koriste strukturu samog problema [@nowicki1996], dok su naše implementirane metode opšte prirode i oslanjaju se na pronalaženje jednostavne okoline. Ovakav ishod je očekivan i u skladu sa obimom rada.

Vredi, međutim, još jednom osvrnuti se na odnos utrošenog vremena. Rešenje vrednosti 1165 za instancu `ft20` simulirano kaljenje pronalazi za nepunih šest sekundi, dok egzaktni rešavač ni nakon sat vremena ne uspeva da pronađe bolje od 1182. Za praktičnu primenu, u kojoj se
raspored često mora dobiti u kratkom roku, odstupanje ispod jednog procenta uz vreme izvršavanja od nekoliko sekundi predstavlja upotrebljiv rezultat.

## Diskusija

Prilokom razvoja i merenja uočeno je nekoliko pojava koje se ne vide iz zbirnih tabela,
a koje su bitno uticale na konačan izbor metoda i njihovih parametara.

### Uža okolina ne donosi bolji rezultat

Okolina zasnovana na kritičnom putu, u literaturi poznata kao $N_1$
[@vanlaarhoven1992], razmatra samo zamene susednih operacija na kritičnom putu koje se izvršavaju na istoj mašini. Time se broj kandidata po koraku drastično smanjuje. Na primer, sa 540
na 6,7^[Date su prosečne vrednosti broja kandidata] kod instance `ft06`, sa 4500 na 17,4 kod `ft10` i sa 4750 na 31,6 kod `ft20`, dakle između 81 i 259 puta.^[Ova merenja sprovedena su naknadno, s obzirom na neobećavajuće rezultate]

Uprkos tome, pri izjednačenom broju poziva funkcije dekodiranja ta okolina daje **lošiji** rezultat od proste zamene dva elementa. Kod višestruko pokrenute lokalne pretrage na instanci `ft10` prosek je 1063,6 naspram 1051,8, a kod simuliranog kaljenja 1000,5
naspram 956,7. Na instanci `ft20` razlika je najizraženija: 1223,7 naspram 1180,7.

Nameće se očigledan razlog za loše performanse $N_1$ okolina, koji se ogleda u tome što $N_1$ okoline zahtevaju poziv funkcije dekodiranja za sopstveno formiranje. Naš eksperiment konstruisan je tako da direktno zavisi od broja poziva ove funkcije. Ipak, ispostavlja se da ovo nije razlog, s obzirom da su u radu $N_1$ okoline dobije zasebnu funkciju dekodiranja, čiji broj pozivanja nismo uzimali u obzir pri evaluaciji rešenja.

Uzroci su druge prirode. Prvi je taj što uža okolina daje plići pojam lokalnog optimuma, što navodi pretragu na ranije zaustavljanje i to na lošijem mestu. Kod simuliranog kaljenja postoji i drugi razlog. Naime, ograničavanjem izbora na
kritični put oduzimaju se neutralni potezi, koji ne menjaju vrednost funkcije cilja odmah, ali otvaraju put kasnijim poboljšanjima.

U literaturi $N_1$ i srodne okoline daju vrlo dobre rezultate, ali u sprezi sa tabu listom i inkrementalnom procenom vrednosti [@nowicki1996], čime se oba navedena nedostatka uklanjaju. Bez tih dopuna, sama okolina ispostavlja se nedovoljnom.

### Složenija metoda nije nužno bolja

Metoda promenljivih okolina koristi lokalnu pretragu kao potprogram i nad njom gradi mehanizam izlaska iz lokalnog optimuma. Očekivano bi bilo da nadmaši simulirano kaljenje, koje je konceptualno jednostavnije. Merenja pokazuju suprotno: pri istom
budžetu prosečno odstupanje iznosi 2,26% za promenljive okoline naspram 0,70% za kaljenje.

Razlog je u ceni jednog koraka. Jedan silazak lokalne pretrage na instanci `ft10` troši oko 39 000 poziva funkcije cilja, pa pri budžetu od 200 000 poziva metoda stigne da izvede svega nekoliko silazaka. Simulirano kaljenje u istom budžetu razmotri 200 000 pojedinačnih poteza. Pri ovako postavljenom poređenju prednost ima metoda sa jeftinijim korakom.

### Odnos prema egzaktnom rešavanju

Rezultati na instanci `ft20` pokazuju granicu primenljivosti egzaktnog pristupa. Rešavač je za sat vremena pronašao rešenje vrednosti 1182 i dokazao donju granicu 657, dok je simulirano kaljenje za nepunih šest sekundi pronašlo rešenje vrednosti 1165.
Uz to je jednostavna donja granica iz odeljka o donjim granicama, izračunata u zanemarljivom vremenu, iznosila 1119, što je znatno više od granice koju je rešavač dokazao.

Kombinovanjem sopstvenih rezultata, dakle donje granice 1119 i najboljeg pronađenog rešenja 1165, dobija se procena optimuma sa odstupanjem od 4,1%, umesto 44,37% koliko je iznosilo odstupanje egzaktnog rešavača.

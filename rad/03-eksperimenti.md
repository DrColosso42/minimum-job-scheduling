# Eksperimentalni rezultati

## Okruženje za eksperimentisanje

Kako bismo olakšali kasniju interpretaciju rezultata, za početak ćemo dostaviti kontekstualne informacije o veličini eksperimenata i okruženju na kojima su eksperimenti pokretani.

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

Pri evaluaciji razvijenih metoda korišćeno je devet različitih test instanci. Od njih devet, osam je preuzeto iz zbirke OR-Library [@beasley1990]. Instance `ft06`, `ft10` i `ft20` potiču iz rada [@fisher1963], dok instance `la01` - `la05` dolaze iz [@lawrence1984]. Poslednja, deveta, instanca `mini3` kreirana je za potrebe ovog rada. Predstavlja relativno malu instancu čiji se optimum može pronaći algoritmom grube sile. Kao takva služila je najpre pri validaciji ispravnosti implementiranih metoda optimizacije.
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
granice: (1) najdužeg posla i (2) najopterećenije mašine. Način implementacije računa detaljno je opisan u odeljku
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

Kao što je ranije navedeno, zbog nedostatka konkurentnosti u implementacijama algoritama, efikasnost različitih optimizacionih metoda nije pogodno upoređivati sa egzaktnim rešavačem na osnovu vremena izvršavanja. Kod međusobnog poređenja situacija je nešto bolja, ali se pokazalo veoma izazovno unapred dozvoliti funkciji određeni vremenski okvir, pa je vreme izvršavanja zauzelo ulogu _retrospektivne mere_, dok su sami algoritmi unapred ograničeni brojem pozivanja funkcije dekodiranja.

Svakom algoritmu je unapred data gornja granica broja poziva ove funkcije i taj broj nazivamo _budžetom_ funkcije. Ispostavlja se da je budžet od oko 200,000 poziva dekodera sasvim dovoljan za verodostojno reprodukovanje rezultata, a opet dovoljno mali da poziv optimizacione metode ostane dovoljno vremenski ograničen. Primećujemo da se vreme izvršavanja optimizacionog metoda razlikuje i pri istom budžetu, a razlog tome nalazi se u specifičnostima samih algoritama, gde se vreme "rasipa" na pozive drugih pomoćnih metoda.

--- slike idu ovde

# Eksperimentalni rezultati

## Okruženje za eksperimentisanje

Kako bismo olakšali kasniju interpretaciju rezultata, za početak ćemo dostaviti kontekstualne informacije o veličini eksperimenata i okruženju na kojima su eksperimenti pokretani.

Za početak je potrebno objasniti način izbora veličine eksperimenta. Bilo je potrebno održati balans između validnosti rezultata i razumne upotrebe (pre svega vremenskih) resursa. Sa jedne strane, ne možemo dopustiti da eksperimente izvršavamo na premalom uzorku i time dovedemo u pitanje opštost zaključaka, dok je sa druge strane potrebno da se eksperimenti izvrše u razumnom vremenskom roku.

Sve eksperimentalne skripte izvršavane su na privatnom računaru, čije se najznačajnije karakteristike nalaze u sledećoj tabeli:

| komponenta                | vrednost                                             |
| ------------------------- | ---------------------------------------------------- |
| procesor                  | Intel Core Ultra 7 165U                              |
| frekvencija               | 3,71 GHz                                             |
| broj jezgara              | 12 fizičkih / 14 logičkih                            |
| radna memorija            | 62,2 GB                                              |
| operativni sistem         | Ubuntu 24.04.4 LTS, 7.0.0-28-generic kernel , x86-64 |
| standardna biblioteka     | glibc 2.39                                           |
| programski jezik          | Python 3.12.3, GCC 13.3.0                            |
| egzaktni rešavač          | IBM ILOG CPLEX 22.2.0.0                              |
| biblioteka za modelovanje | PuLP 3.3.2                                           |

: Karakteristike računara na kome su izvršena sva merenja.\label{tbl:okruzenje}

Vredi napomenuti da sve razvijene metaheuristike tako da se izvršavaju na **jednoj niti** bez mogućnosti paralelizacije.
Egzaktni rešavač (CPLEX) pokretan je sa podrazumevanim brojem niti, dakle sa svih 14 logičkih
jezgara. Zbog te razlike, metode je najpreciznije porediti na osnovu broja pozivanih funkcija dekodiranja
a ne po utrošenom vremenu. Dužina izvršavanja navedena je kao dodatni, orijetnacioni podatak.

## Test instance

Za vrednovanje razvijenih metoda korišćeno je devet instanci. Osam ih je preuzeto iz
zbirke OR-Library [@beasley1990], koja je standardni skup za poređenje rezultata u
literaturi o raspoređivanju. Instance `ft06`, `ft10` i `ft20` potiču iz rada
[@fisher1963], a instance `la01`--`la05` iz [@lawrence1984]. Deveta instanca, `mini3`,
napravljena je za potrebe ovog rada; dovoljno je mala da se njen optimum utvrdi
iscrpnom pretragom, pa služi za proveru ispravnosti implementacije.

| instanca | $n \times m$ | operacija | donja granica | optimum |
|---|:---:|---:|---:|---:|
| `mini3` | $3 \times 3$ | 9 | 10 | 11 |
| `ft06` | $6 \times 6$ | 36 | 47 | 55 |
| `la01` | $10 \times 5$ | 50 | **666** | 666 |
| `la02` | $10 \times 5$ | 50 | 635 | 655 |
| `la03` | $10 \times 5$ | 50 | 588 | 597 |
| `la04` | $10 \times 5$ | 50 | 537 | 590 |
| `la05` | $10 \times 5$ | 50 | **593** | 593 |
| `ft10` | $10 \times 10$ | 100 | 655 | 930 |
| `ft20` | $20 \times 5$ | 100 | 1119 | 1165 |

: Test instance sa dimenzijama, donjim granicama i objavljenim optimalnim
vrednostima. Optimum instance `mini3` utvrđen je iscrpnom pretragom, a ostali su
preuzeti iz literature navedene u prethodnom pasusu.\label{tbl:instance}

Donja granica u tabeli \ref{tbl:instance} izračunata je kao veća od dve trivijalne
granice --- najdužeg posla i najopterećenije mašine --- na način opisan u odeljku
o donjim granicama. Kod instanci `la01` i `la05` ta granica se poklapa sa optimumom,
pa svako rešenje koje je dostigne ujedno i **dokazuje** svoju optimalnost, bez potrebe
za egzaktnim rešavačem. Te dve instance zato imaju posebnu ulogu: neuspeh metode na
njima nedvosmisleno ukazuje na grešku u implementaciji dekodera ili okoline, a ne na
slabost same metode.

Instance su izabrane tako da pokriju raspon težine. `mini3` i `ft06` sve razvijene
metode rešavaju do optimuma, pa služe kao provera ispravnosti. Instance `la01`--`la05`
razdvajaju metode po pouzdanosti. `ft10` i `ft20` su, uprkos skromnim dimenzijama,
poznato teške --- instanca `ft10` je ostala nerešena punih dvadeset šest godina nakon
objavljivanja [@jain1999].

# Opis rešenja

## Kodiranje rešenja

Za početak potrebno je formalno definisati rešenje ka kojem stremimo i
odrediti format pogodan za primenu optimizacija koje slede. U ovom poglavlju obrađeno je upravo to pitanje, ali i sve pomoćne strukture neophodne za uspešno implementiranje optimizacija. Dati su opisi oblika okoline, načina ukrštanja, načina evaluacije i drugi.

### Prirodan zapis i njegov nedostatak

Redosled operacija unutar posla zadat je instancom i ne može se menjati. Jedina dimenzija slobode koju rešavač poseduje jeste određivanje **redosleda koji operacije zauzimaju na svakoj mašini**. Nameće se, dakle, prirodan zapis, kao $m$ permutacija, po jedan raspored za svaku mašinu.

Takav zapis ima ozbiljan nedostatak koji se vrlo brzo prikazuje. Naime, većina kombinacija ne odgovara nijednom validnom rasporedu.
Posmatrajmo instancu sa dva posla i dve mašine:

$$J_1: M_1(3) \rightarrow M_2(2), \qquad J_2: M_2(2) \rightarrow M_1(4)$$

Mašina $M_1$ obrađuje prvu operaciju posla $J_1$ i drugu operaciju posla $J_2$, dok mašina $M_2$ obrađuje prvu operaciju posla $J_2$ i drugu operaciju posla $J_1$. Za svaku
mašinu postoje dva moguća redosleda, dakle ukupno četiri kombinacije:

| redosled na $M_1$ | redosled na $M_2$ | $C_{max}$ |
| ----------------- | ----------------- | --------- |
| $J_1$ pa $J_2$    | $J_2$ pa $J_1$    | **7**     |
| $J_1$ pa $J_2$    | $J_1$ pa $J_2$    | 11        |
| $J_2$ pa $J_1$    | $J_2$ pa $J_1$    | 11        |
| $J_2$ pa $J_1$    | $J_1$ pa $J_2$    | ---       |

: Sve kombinacije redosleda po mašinama za instancu sa dva posla i dve
mašine.\label{tbl:kombinacije}

Poslednja kombinacija **ne opisuje validan raspored**. Prva operacija posla $J_1$ čeka da se na mašini $M_1$ završi druga operacija posla $J_2$. Ta operacija čeka prvu operaciju istog posla. Dalje, sad ona čeka da se na mašini $M_2$ završi druga operacija posla $J_1$, a ta
operacija čeka prvu operaciju posla $J_1$, od koje smo i pošli. Zavisnosti čine ciklus i nijedna operacija ne može da počne.

Na ovako maloj instanci neizvodljiva je jedna od četiri kombinacije. Sa porastom broja poslova i mašina taj udeo raste, pa bi svaka metoda koja slučajno bira redoslede po mašinama najveći deo rada trošila na odbacivanje neispravnih rešenja.

### Permutacija sa ponavljanjem

Zbog toga je usvojeno kodiranje koje je za ovaj problem predložio Kristijan Birvirt
[@bierwirth1995]. Rešenje je **lista oznaka poslova**, u kome se oznaka svakog posla javlja onoliko puta koliko taj posao ima operacija. Za instancu sa dva posla po dve operacije, jedan takav niz je

$$(J_2,\ J_1,\ J_1,\ J_2).$$

Niz se čita sleva nadesno, a $k$-to pojavljivanje oznake posla $J_j$ predstavlja
**$k$-tu operaciju** tog posla. Gornji niz stoga redom označava prvu operaciju posla
$J_2$, prvu i drugu operaciju posla $J_1$, pa drugu operaciju posla $J_2$.

Ključna osobina ovog zapisa jeste da je **svaki niz sa ispravnim brojem pojavljivanja izvodljiv**. $(k+1)$. operacija nekog posla ne može se pojaviti pre $k$-te, jer je njeno mesto u nizu po definiciji kasnije pojavljivanje iste oznake. Redosled unutar
posla time nije ograničenje koje se proverava, već osobina samog zapisa, pa ciklus opisan u prethodnom odeljku nije moguće ni zapisati u Birvirtovoj notaciji.

Broj različitih nizova za instancu sa poslovima $J_1, \dots, J_n$ iznosi

$$\frac{\left( \sum_{j} |J_j| \right)!}{\prod_{j} |J_j|!},$$

što za instancu `ft06` sa 36 operacija daje približno $2{,}67 \cdot 10^{24}$ različitih nizova.

### Višeznačnost zapisa

Jedan od izazova ove notacije jeste to što ne garantuje uzajamnu jednoznačnost zapisa i rasporeda. Odnosno, više različitih nizova
može dati isti raspored. Za pomenutu instancu sa dva posla postoji šest različitih nizova, koji se preslikavaju u svega tri izvodljiva rasporeda iz tabele
\ref{tbl:kombinacije}. Čak četiri od šest nizova daju optimalno rešenje.

Prostor pretrage je, dakle, veći od prostora rešenja. Ipak, u literaturi je cena koja se plaća za garantovanu izvodljivost smatrana prihvatljivom. Navodi se (a što nije ovim radom eksplicitno proveravano) da je provera izvodljivosti u alternativnom zapisu znatno skuplja od višestrukog obilaska istog rasporeda.

## Dekoder

Glavna mana Birvirtove notacije jeste što niz oznaka ne nosi eksplicitno informaciju o rasporedu poslova na mašini. Ona jeste sadržana unutar njega, ali je potrebno niz adekvatno transformisati ba bismo do nje došli. Postupak kojim od niza dolazimo do rasporeda, odnosno svakoj operaciji dodeljuje trenutak početka, nazivamo _dekoderom_.

### Postupak

Operacije se obrađuju redom kojim se javljaju u nizu. Za svaku od njih trenutak početka određen je sa dva ograničenja: operacija ne može početi pre nego što se završi prethodna
operacija istog posla, niti pre nego što se oslobodi mašina koju zahteva. Stoga, najraniji trenutak koji zadovoljava oba jeste

$$s_o = \max \left( r_{J(o)},\ f_{M(o)} \right),$$

gde je $r_{J(o)}$ trenutak završetka prethodne operacije posla kome $o$ pripada, a $f_{M(o)}$ trenutak u kome se oslobađa mašina $M(o)$. Nakon dodele, obe vrednosti ažuriraju se na $s_o + p_o$.

Dekoder time održava tri niza vrednosti: vreme spremnosti svakog posla, vreme oslobađanja svake mašine i redni broj sledeće operacije svakog posla (poput brojača instrukcija u savremenim računarima). Poslednji od njih pretvara oznaku posla u konkretnu operaciju, u skladu sa pravilom o $k$-tom pojavljivanju.

Vrednost funkcije cilja, $C_{max}$, jednaka je najvećem trenutku završetka među svim operacijama.

### Poluaktivni rasporedi

Ovako opisan postupak svaku operaciju smešta u **najraniji mogući trenutak** pri zadatom redosledu. Rasporedi sa tom osobinom nazivaju se _poluaktivnim_ i nose osobinu da se nijedna operacija ne
može pomeriti ulevo bez promene redosleda na nekoj mašini.

Poluaktivni rasporedi nisu najuži skup koji vredi razmatrati. Uži je skup _aktivnih_ rasporeda, u kome se nijedna operacija ne može pomeriti ulevo ni uz promenu redosleda. Poznato je da taj skup sadrži bar jedno optimalno rešenje [@giffler1960]. Postupak Gifler--Tompsona proizvodi upravo takve rasporede i time smanjuje prostor pretrage.

U ovom radu korišćen je poluaktivni dekoder, iz dva razloga. Najpre zato što je poluaktivni dekoder izuzetno jednostavan za implementaciju, a pritom skup poluaktivnih rasporeda i dalje sadrži optimalno rešenje. Jedina cena jednostavnosti je veći prostor pretrage.

### Složenost

Dekoder obavlja jedan prolaz kroz niz i za svaku operaciju konstantan broj radnji, pa je njegova složenost $O(L)$, gde je $L = \sum_j |J_j|$ ukupan broj operacija.

Kako je dekoder jedino mesto na kome se rešenje vrednuje, broj njegovih poziva korišćen je kao mera uloženog rada pri poređenju metoda, na način opisan u odeljku o metodologiji.

### Primer

Za instancu iz odeljka o kodiranju i niz $(J_1, J_2, J_1, J_2)$ dekoder redom dodeljuje:

| korak | operacija    | mašina | spreman posao | slobodna mašina | početak | kraj |
| ----- | ------------ | ------ | ------------: | --------------: | ------: | ---: |
| 1     | $J_1$, prva  | $M_1$  |             0 |               0 |       0 |    3 |
| 2     | $J_2$, prva  | $M_2$  |             0 |               0 |       0 |    2 |
| 3     | $J_1$, druga | $M_2$  |             3 |               2 |       3 |    5 |
| 4     | $J_2$, druga | $M_1$  |             2 |               3 |       3 |    7 |

: Rad dekodera nad nizom $(J_1, J_2, J_1, J_2)$. Vrednost $C_{max}$ jednaka je
7.\label{tbl:dekoder}

U trećem koraku jasno možemo videti prvo ograničenje na delu. Operacija čeka da se završi prva operacija istog posla iako je mašina slobodna. U četvrtom koraku ograničenje nameće mašina. Bitno je uočiti tu razliku, s obzirom da nam je potrebna prilikom konstrukcije kritičnog puta, čiji postupak je opisan u narednoj sekciji.

## Kritični put

U prethodnom odeljku opisali smo postupak koji nam iz Birvirtovog zapisa rasporeda poslova daje vrednost $C_{max}$. Ipak, vrednost $C_{max}$ govori o tome koliko raspored traje, ali ne nosi informaciju **šta ga određuje**. Za dalju analizu, a pre svega za konstrukciju okolina, potrebno je znati koje operacije zaista utiču na dužinu rasporeda, a koje imaju vremenskog prostora.

### Definicija

_Kritični put_ je niz operacija $o_1, o_2, \dots, o_k$ takav da važi

$$s_{o_1} = 0, \qquad f_{o_i} = s_{o_{i+1}}, \qquad f_{o_k} = C_{max},$$

dakle lanac koji počinje u trenutku nula, završava se u trenutku $C_{max}$ i u kome između uzastopnih operacija nema praznog hoda. Svaki par uzastopnih operacija povezan je jednim od dva ranije navedena ograničenja. Posao ne može da počne ili zbog toga što čeka na prethodnu operaciju istog posla ili na oslobađanje potrebne mašine.

Iz uslova da praznog hoda nema neposredno sledi

$$C_{max} = \sum_{i=1}^{k} p_{o_i},$$

odnosno dužina kritičnog puta jednaka je vrednosti funkcije cilja.

### Značaj

Neposredna posledica prethodne jednakosti jeste da se $C_{max}$ može smanjiti **isključivo** promenom koja utiče na neku od operacija sa kritičnog puta. Operacije van puta nemaju uticaj na ukupnu dužinu puta i mogu se proizvoljno pomerati.^[Vredi napomenuti da je operacije van kritičnog puta moguće izmestiti tako da _produže_ ukupno vreme trajanja i time pogoršaju ukupni rezultat. Ipak, u tom slučaju bi se i one same našle na kritičnom putu.]

Ovo nosi značajan uvid pri formiranju okoline neke tačke. Naime, smisleno je razmatrati samo one okoline koje menjaju kritični put. Taj postupak opisan je u odeljku o okolinama.

### Određivanje

Određivanje kritičnog puta moguće je učiniti blagom izmenom funkcije dekodera. Pri dodeli trenutka početka,

$$s_o = \max \left( r_{J(o)},\ f_{M(o)} \right),$$

jedan od dva argumenta je veći i on je razlog zašto operacija nije mogla ranije. Ako je veći bio $r_{J(o)}$, operaciju je zadržala prethodna operacija istog posla. U suprotnom, ako je bio
$f_{M(o)}$, zadržala ju je prethodna operacija na istoj mašini. Pamćenjem te odluke (npr. u matrici) dobija se, za svaku operaciju, pokazivač na njenog **neposrednog prethodnika**.

Kritični put se zatim dobija polazeći od operacije sa najvećim trenutkom završetka i praćenjem pokazivača unazad, sve do operacije koja počinje u trenutku nula. Postupak je
složenosti $O(L)$, kao i sam dekoder.

Radi efikasnosti, pamćenje prethodnika izdvojeno je u zasebnu funkciju. Osnovni dekoder, koji se poziva pri svakom vrednovanju, ne obavlja taj posao, dok se prošireni poziva samo kada je kritični put zaista potreban.

### Primer

Za instancu `mini3` i niz koji daje optimalno rešenje, kritični put čini pet od devet
operacija:

| operacija    | mašina | trajanje | početak | kraj | zadržao je |
| ------------ | :----: | -------: | ------: | ---: | ---------- |
| $J_1$, prva  | $M_1$  |        3 |       0 |    3 | ---        |
| $J_2$, prva  | $M_1$  |        2 |       3 |    5 | mašina     |
| $J_2$, druga | $M_3$  |        1 |       5 |    6 | posao      |
| $J_3$, druga | $M_3$  |        3 |       6 |    9 | mašina     |
| $J_1$, treća | $M_3$  |        2 |       9 |   11 | mašina     |

: Kritični put instance `mini3` pri optimalnom rasporedu. Zbir trajanja iznosi 11, što
je jednako vrednosti $C_{max}$.\label{tbl:kriticni}

![Raspored dobijen dekodiranjem niza $(J_1, J_2, J_2, J_3, J_1, J_2, J_3, J_1, J_3)$
nad instancom `mini3`. Šrafirane su operacije koje pripadaju kritičnom putu. \label{sl:kriticni}](slike/mini3_critical_path.png){width=95%}

Primetimo da na slici \ref{sl:kriticni} treća operacija $J_2$ može biti pomerena za jednu jedinicu vremena unapred bez uticaja na optimalnost rešenja. Slično, operacije koje se izvršavaju na mašini $M_2$ mogu biti u potpunosti ispremeštane sve dok pošutuju uslov dovršavanja prethodnih instrukcija svojih poslova.

## Donja granica

Vrednost koju metoda pronađe sama po sebi ne daje nam informaciju o kvalitetu datog rešenja. Kako bismo mogli to da utvrdimo potrebno je da imamo informaciju o dokazanom optimumu (ukoliko je instanca problema formalno rešiva^[U razumnom vremenu]) sa kojim bismo uporedili ovaj rezultat. Druga mogućnost jeste da nekako izračunamo donju granicu rešenja, odnosno vrednost za koju možemo da tvrdimo da je nužno manja od optimalnog rešenja. Što veću takvu vrednost nađemo to nam je procena verodostojnija i korisnija u analizi metoda optimizacije.

### Dva trivijalna ograničenja

Prvo ograničenje nameće posao. Operacije jednog posla izvršavaju se jedna za drugom, pa od početka prve do kraja poslednje protekne bar zbir njihovih trajanja. Kako to važi za svaki posao, važi i za najduži među njima:

$$C_{max} \ge \max_{j} \sum_{o \in J_j} p_o.$$

Drugo ograničenje nameće mašina. Mašina obrađuje jednu operaciju u datom trenutku, pa se sve operacije dodeljene jednoj mašini izvršavaju uzastopno. Čak i kada mašina nikada ne stoji, poslednja operacija završava se najranije u trenutku koji je jednak zbiru
trajanja svih operacija na toj mašini:

$$C_{max} \ge \max_{k} \sum_{o \in M_k} p_o.$$

Obe nejednakosti važe za svaki validan raspored, pa važi i veća od njih:

$$LB = \max \left( \max_{j} \sum_{o \in J_j} p_o,\ \ \max_{k} \sum_{o \in M_k} p_o \right).$$

Izračunavanje zahteva jedan prolaz kroz instancu, dakle složenosti je $O(L)$, pri čemu se dekoder ne poziva nijednom.

### Ograničenja pristupa

Ovako dobijena granica zanemaruje **čekanje** (prazan hod). Prvi argument pretpostavlja da posao nikada ne čeka slobodnu mašinu, drugi da mašina nikada ne stoji prazna. U stvarnim rasporedima dešava se i jedno i drugo, pa je granica po pravilu strogo manja od
optimuma.

Koliko je manja, zavisi od instance:

| instanca | donja granica | optimum | odstupanje |
| -------- | ------------: | ------: | ---------: |
| `la01`   |       **666** |     666 |          0 |
| `la05`   |       **593** |     593 |          0 |
| `la03`   |           588 |     597 |      1,5 % |
| `la02`   |           635 |     655 |      3,1 % |
| `ft20`   |          1119 |    1165 |      3,9 % |
| `la04`   |           537 |     590 |      9,0 % |
| `mini3`  |            10 |      11 |      9,1 % |
| `ft06`   |            47 |      55 |     14,5 % |
| `ft10`   |           655 |     930 |     29,6 % |

: Odstupanje donje granice od poznatog optimuma, poređano po veličini
odstupanja .\label{tbl:granice}

Na instanci `ft10` granica je za skoro trećinu ispod optimuma i tu je praktično beskorisna. Na `la01` i `la05`, međutim, poklapa se sa optimumom.

### Dokaz optimalnosti bez rešavača

Donja granica nam pored procene optimalnosti može dati i čvrst dokaz iste u određenim situacijama. Naime, ukoliko na instanci $I$ za koju važi donja granica $LB$, pronađemo raspored čija je vrednost $C_{max} = LB$ onda smo sigurni da je takav raspored optimalan. Po definiciji donje granice nijedan raspored ne može biti bolji od nje, pa je onaj čija je vrednost upravo ona sigurno najbolji mogući.

Upravo zbog ove osobine dostizanje vrednosti 666 na instanic `la01`, odnosno 593 na `la05` dokazuje optimalnost istog.

## Iscrpna pretraga

Pre implementiranja bilo koje heuristike korisno nam je da imamo postupak koji garantuje optimalno rešenje, makar i po cenu izrazito velikog (nekada nedostižnog) vremena izvršavanja. Takav postupak može nam služiti kao sredstvo validacije. Na primerima gde ga je moguće izvršiti on će nam dati informaciju o optimalnom rezultatu, a tom informacijom možemo da evaluiramo rešenja dobijena primenom neke od heuristika.

### Postupak

Iscrpna pretraga (metoda grube sile) prolazi kroz **sve različite nizove** iz odeljka o kodiranju, dekodira svaki i pamti najbolji. Kako je svaki niz izvodljiv, nikakva provera ispravnosti nije
potrebna, a kako se svaki raspored može zapisati bar jednim nizom, optimum se sigurno nalazi među razmotrenim rešenjima.

Nizovi se nabrajaju kao permutacije multiskupa, dakle bez ponavljanja istih rasporeda oznaka. Za instancu sa poslovima $J_1, \dots, J_n$ njihov broj iznosi

$$\frac{\left( \sum_{j} |J_j| \right)!}{\prod_{j} |J_j|!}.$$

Nizovi se obrađuju jedan po jedan, bez čuvanja u memoriji, pa je prostorna složenost zanemarljiva. Vremenska složenost jednaka je proizvodu gornjeg izraza i cene jednog
dekodiranja (u našem slučaju $O(L)$ gde je L dužina niza).

### Granica primenljivosti

Broj nizova raste brže od eksponencijalne funkcije, pa je pretraga upotrebljiva samo na vrlo malim instancama. Za instance sa tri mašine i rastućim brojem poslova dobija se:

| poslova | operacija |           broj nizova | procenjeno vreme |
| ------: | --------: | --------------------: | ---------------- |
|       3 |         9 |                 1 680 | trenutno         |
|       4 |        12 |               369 600 | oko 1 s          |
|       5 |        15 |           168 168 000 | oko 10 min       |
|       6 |        18 | $1{,}3 \cdot 10^{11}$ | oko 5 dana       |

: Rast prostora pretrage sa brojem poslova, pri tri mašine.\label{tbl:grubasila}

Već pri šest poslova pretraga prestaje da bude izvodljiva. Za instancu `ft06`, koja sadrži svega šest poslova i šest mašina, broj različitih nizova iznosi približno
$2{,}67 \cdot 10^{24}$; pri milion dekodiranja u sekundi obilazak bi trajao oko $8{,}5 \cdot 10^{10}$ godina, dakle višestruko duže od procenjene starosti svemira.

### Uloga u radu

Iscrpna pretraga primenjena je na instancu `mini3`, sa tri posla i tri mašine, kao i na dve još manje instance korišćene pri razvoju. Dobijeni optimum od 11 za `mini3` jedina je vrednost u ovom radu koja je **dokazana neposredno**, obilaskom celog prostora rešenja^[Kasnije će biti reči o rešavanju egzaktnim metodama putem rešavača CPLEX. Bez obzira na to, ovo predstavlja značajan rezultat i oslonac za ostatak rada imajući u vidu jednostavnost implementacije i sigurnost u dobijeno rešenje].

Ta vrednost korišćena je kao provera ispravnosti dekodera i svih razvijenih metoda. Zaista, metoda koja na `mini3` ne dostiže 11 sadrži grešku, jer nijedna heuristika ne može biti lošija od tačnog odgovora na instanci ove veličine.

## Okoline

Svaka od metoda razvijenih u ovom radu (izuzev genetskog algoritma), prostor rešenja pretražuju počevši od dostavljene početne tačke i istražujući njenu neposrednu okolinu, tražeći (možda lokalno) optimalno rešenje. Zbog toga neophodno je definisati _okolinu_ određenog Birvirtovog niza na koju će se osloniti sve metaheuristike.

### Zamena dva elementa

Najjednostavnija okolina rasporeda u Birvirtovom zapisu može se dobiti **zamenom mesta** dvema instrukcijama u nizu. S obzirom da rezultat ovakve transformacije daje permutaciju početnog niza znamo da je taj raspored sigurno validan.

Zamena dve iste oznake ne menja niz, pa se takvi parovi preskaču. Za niz dužine $L$ broj suseda je stoga najviše $\binom{L}{2}$, a u praksi manji za broj parova jednakih oznaka.
Orijentacije radi, na instanci `ft06` to daje 540 suseda, a na `ft10` i `ft20` po 4500, odnosno 4750.

Ovakva definicija okoline ne koristi nikakvo znanje o problemu. Ne služi se osobinom o kritičnom putu koju smo naveli ranije u radu i bira nasumičnu permutaciju dobijenu jednom zamenom. To je ujedno i glavna mana ovakve definicije okoline. Naravno, prednost se ogleda u jednostavnosti implementacije i ceni jednog generisanja koje se izvršava u konstantnom vremenu.

### Okolina po kritičnom putu

Iz osobine kritičnog puta, izvedene ranije, sledi da izmena koja ne dira nijednu operaciju sa puta ne može smanjiti $C_{max}$. Prirodno je stoga razmatrati samo izmene koje ga dodiruju.

Upravo tu osobinu koristi $N_1$ okolina koju su predložili Piter van Larhoven i saradnici [@vanlaarhoven1992], obuhvata
zamene **susednih operacija na kritičnom putu koje se izvršavaju na istoj mašini**. Oba uslova su neophodna za uspešnost definicije ove okoline. Najpre susednost obezbeđuje da izmena utiče na kritičan put, a zajednička mašina obezbeđuje da je izmena validna (jer se redosled unutar posla ne sme menjati).

Sužavanje prostora pretrage je znatno:

| instanca | zamena dva elementa | $N_1$ |       odnos |
| -------- | ------------------: | ----: | ----------: |
| `ft06`   |                 540 |   6,7 |  $81\times$ |
| `ft10`   |                4500 |  17,4 | $259\times$ |
| `ft20`   |                4750 |  31,6 | $150\times$ |

: Prosečan broj suseda po koraku, izmeren nad 200 slučajno izabranih
nizova.\label{tbl:okoline}

### Poređenje okolina

Očekivano bi bilo da uža okolina, koja razmatra samo poteze sa izgledom na uspeh, daje bolje rezultate. Merenje pokazuje suprotno. U tabeli su prikazani rezultati pri izjednačenom budžetu od 200 000 poziva dekodera, kroz 10 pokretanja:

| instanca | metoda           |     zamena |  $N_1$ |
| -------- | ---------------- | ---------: | -----: |
| `ft06`   | lokalna pretraga |       55,0 |   55,0 |
| `ft06`   | kaljenje         |       55,0 |   55,0 |
| `ft10`   | lokalna pretraga | **1050,5** | 1063,6 |
| `ft10`   | kaljenje         |  **956,7** | 1001,0 |
| `ft20`   | lokalna pretraga | **1305,1** | 1431,2 |
| `ft20`   | kaljenje         | **1182,1** | 1223,7 |

: Prosečna vrednost funkcije cilja pri izjednačenom budžetu, po
okolini.\label{tbl:poredjenje-okolina}

Uzroci su razmotreni u odeljku o diskusiji rezultata.

Zbog ovakvih rezultatima je u svim metodama razvijenim u ovom radu korišćena okolina zamene dva elementa, dok je $N_1$ implementirana i izmerena, ali nije ušla u konačan izbor.

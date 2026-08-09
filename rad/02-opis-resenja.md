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

Ključna osobina ovog zapisa jeste da je **svaki niz sa ispravnim brojem pojavljivanja izvodljiv**. $(k+1)$. operacija nekog posla ne može se pojaviti pre operacije $k$, jer je njeno mesto u nizu po definiciji kasnije pojavljivanje iste oznake. Redosled unutar
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

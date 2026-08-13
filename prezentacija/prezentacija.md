## Formulacija

Dato je $n$ poslova i $m$ mašina. Posao predstavlja **uređeni niz operacija**. Operacija je određena trajanjem i mašinom na kojoj se izvršava.

Cilj je pronaći raspored poslova tako da se minimizuje ukupno trajanje
izvršavanja svih poslova, koje označavamo sa $C_{max}$.

Rešenje mora da zadovolji dva uslova:

- operacije jednog posla izvršavaju se **zadatim redosledom**
- mašina u jednom trenutku može da izvršava **najviše jednu** operaciju

Problem je NP-težak. Primer: instanca `ft10` ostala je nerešena 26 godina.

## Isti poslovi, dva rasporeda

![Dva rasporeda iste instance sa dva posla i dve mašine.](uvod.png){width=78%}

## Kodiranje rešenja

Niz je kodiran **Birvirtovim kodiranjem**.

To je **niz oznaka poslova** od kojih se svaka ponavlja onoliko puta koliko posao ima operacija. Položaj u nizu označava redni broj operacije.

```
0 1 1 2 0 1 2 0 2
```

**Svaki takav niz opisuje izvodljiv raspored**.

## Dekoder

Birvirtovo kodiranje **ne prikazuje raspored eksplicitno**.

Dekoder pretvara Birvirtov niz u realni raspored.

Dekoder iterira kroz niz i svakoj operaciji dodeljuje najraniji mogući početak:

$$s_o = \max\big(r_{J(o)},\; f_{M(o)}\big)$$

gde je $r_J$ trenutak kad je posao spreman, a $f_M$ trenutak kad se mašina oslobađa.

Složenost je $O(L)$, gde je $L$ ukupan broj operacija.

## Algoritam grube sile

Broj različitih nizova je

$$\frac{\left(\sum_j |J_j|\right)!}{\prod_j |J_j|!}$$

| poslova (3 mašine) |                 nizova |  vreme |
| -----------------: | ---------------------: | -----: |
|                  4 |                369 600 |    1 s |
|                  5 |            168 168 000 | 10 min |
|                  6 | $1{,}3 \times 10^{11}$ | 5 dana |

Iscrpna pretraga je ipak implementirana, i na instanci `mini3` ona je prvi nezavisan dokaz da su ostale metode ispravne.

## Okoline

**Zamena dva elementa.** Menjaju se dve pozicije sa različitim oznakama.

Ne koristi
nikakvo znanje o problemu, ali je jedan potez konstantne cene.

**Okolina po kritičnom putu ($N_1$).** Razmatraju se samo
zamene susednih operacija na putu koje dele mašinu.

![Kritični put na instanci `mini3`](mini3_critical_path.png){width=62%}

## Heuristike

| metoda              | potez          | izlazak iz lokalnog optimuma |
| ------------------- | -------------- | ---------------------------- |
| lokalna pretraga    | najbolji sused | ponovno pokretanje           |
| simulirano kaljenje | slučajan sused | Metropolisov kriterijum      |
| promenljive okoline | silazak        | rastuće mešanje              |
| genetski algoritam  | PPX ukrštanje  | mutacija i elitizam          |

## Poređenje

Broj pozivanja funkcije dekodiranja **budžetom.**

**Trideset pokretanja** po instanci i metodi, dakle 1080 ukupno.

**Reproducibilnost.** Svako pokretanje ima podešen RNG seed.

![](budget.png){width=80%}

## Najbolje pronađeno rešenje {.shrink}

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

Prosečno odstupanje: simulirano kaljenje **0,70 %**, VNS 2,26 %, GA 2,85 %, lokalna pretraga 4,19 %.

## Rasipanje kroz trideset pokretanja

![](box_prezentacija.png){width=100%}

## Egzaktno rešavanje

Disjunktivna forma, rešena CPLEX-om uz rok od sat vremena.
Dokazano optimalno rešenje na **osam od devet** instanci.

![](ilp_rast.png){width=47%}

## Instanca `ft20`

|          |  rešenje | donja granica |     vreme |
| -------- | -------: | ------------: | --------: |
| CPLEX    |     1182 |           657 |    3603 s |
| kaljenje | **1165** |          1119 | **5,8 s** |

Rešavač posle sat vremena prikazuje odstupanje od 44,37 %. Kaljenje za nepunih šest sekundi nalazi **objavljeni optimum**.

Sopstvenim rezultatima optimum se ograđuje na $[1119,\, 1165]$, što je 4,1% umesto 44,4%.

## Rezultati

**Uža okolina ne donosi bolji rezultat.**

$N_1$ okolina smanjuje broj kandidata između 81 i
259 puta, ali pri izjednačenom budžetu gubi.

Traži dodatno dekodiranje po potezu, daje
plići lokalni optimum, a kaljenju oduzima neutralne poteze.

**Složenija metoda nije nužno bolja.** Promenljive okoline nadgrađuju lokalnu pretragu, ali gube od kaljenja.

## Zaključak

Implementirane su četiri metaheuristike, iscrpna pretraga i celobrojni model, i upoređene pri izjednačenom budžetu na devet instanci.

Najbolje se pokazalo **simulirano kaljenje**, sa 0,70% prosečnog odstupanja i
optimumom dostignutim na osam od devet instanci.

# Uvod

## Opis problema

Problem raspoređivanja poslova po mašinama (engl. _job shop scheduling problem_) jedan je
od najviše proučavanih problema kombinatorne optimizacije. Postavka je sledeća.

Zadato je $n$ poslova i na raspolaganju je $m$ mašina (resursa). Svaki pojedinačni posao $J_j$ sastoji se od niza operacija koje moraju biti
izvršene **tačno zadatim redosledom**. Pored toga, svaka operacija $o$ izvršava se na specifičnoj mašini $M(o)$ i traje $p_o$ jedinica vremena. Traži se raspored poslova sa **najmanjim ukupnim trajanjem**. Pri tome, moraju se poštovati sledeća ograničenja:

1.  **Redosled unutar posla mora biti očuvan.** Operacija $o_k$ može započeti izvršavanje tek kada je gotovo izvršavanje operacija $o_1 \dots o_{k-1}$.
2.  **Najviše jedna operacija može da se izvršava u jednom trenutku na jednoj mašini**. Da bi operacija $o$ započela izvršavanje, mašina $M(o)$ mora biti slobodna.

Ukupno trajanje jednog ovakvog rasporeda nazivamo _makespan_ i označavamo sa $C_{max}$.

![Dva rasporeda iste instance sa dva posla i dve mašine, prikazana u istoj razmeri.
Gornji raspored traje 7, donji 11 vremenskih jedinica. Operacije i njihova trajanja
su u oba slučaja identični --- razlikuje se samo redosled kojim zauzimaju
mašine.\label{sl:uvod}](slike/uvod.png){width=95%}

Na slici iznad jasno možemo videti razliku između lošeg i dobrog rasporeda. Za instancu koja sadrži svega dva posla i dve mašine prvi raspored traje 7, a drugi čak 11 jedinica vremena.

![Dva rasporeda instance `ft06` sa šest poslova i šest mašina. Gornji nastaje
izvršavanjem poslova jednog za drugim i traje 152 vremenske jedinice, donji je
optimalno rešenje sa trajanjem 55.\label{sl:ft06}](slike/ft06.png){width=95%}

Uticaj optimizacije još je primetniji na većoj instanci `ft06`.

## Složenost

Već pri tri mašine problem postaje NP-težak [@garey1976], a u opštem slučaju svrstava se u najteže probleme raspoređivanja zbog svojih specifičnosti. [@garey1976]

Ovu tvrdnju dodatno utvrđuje veličina prostora pretrage. Naime, za svaku mašinu biramo redosled operacija koje se na njoj izvršavaju, pa je broj kombinacija reda $(n!)^m$. Kod instance sa šest poslova i šest mašina dobijamo procenu od oko $1{,}4 \cdot 10^{17}$ kombinacija, pri čemu mnoge od tih kombinacija ne predstavljaju validan raspored.

Problem se u praksi pokazao toliko težak da je instanca `ft10`, sa svojih deset poslova i deset mašina, koja je objavljena 1963. godine [@fisher1963], uprkos _skromnim_ zahtevima rešena tek **dvadeset šest godina kasnije**^[Optimalno rešenje ove konkretne instance dokazali su tek Džek Karlijer i Erik Pinson 1989. godine [@carlier1989].].

## Pregled literature

Prve formulacije problema kao zadatka celobrojnog linearnog programiranja dali su Vagner
[@wagner1959] i Mane [@manne1960]. Maneova, disjunktivna formulacija iskorišćena je i u ovom
radu za formiranje egzaktnog rešenja. Metode granjanja i ograđivanja dovele su do dokazivanja optimuma instance `ft10`
[@carlier1989], a potom i do sistematskog rešavanja standardnih zbirki [@applegate1991].

Gifler i Tompson [@giffler1960] uveli su pojam aktivnog rasporeda i pokazali da taj skup sadrži optimalno rešenje. Na toj strukturi, a pre svega na pojmu kritičnog puta, kasnije
su građene okoline kod heurističkih metoda. Van Larhoven sa saradnicima[@vanlaarhoven1992]
spojili su takvu okolinu sa simuliranim kaljenjem, a Novicki i Smutnicki [@nowicki1996]
sa tabu pretragom. Za genetske algoritme, Birvirt [@bierwirth1995] je predložio kodiranje
permutacijom sa ponavljanjem koje je korišćeno i ovde, dok su u [@bierwirth1996]
upoređeni operatori ukrštanja prilagođeni takvom zapisu. Pregled razvoja oblasti dat je u
[@jain1999].

Test instance korišćene u radu potiču od Fišera i Tompsona [@fisher1963] i Lorensa
[@lawrence1984], a dostupne su preko zbirke OR-Library [@beasley1990].

### Domaći izvori

Na razumevanje samih metaheuristika, njihove strukture i međusobnih odnosa, najviše je
uticala domaća literatura. Materijali sa vežbi iz predmeta Računarska inteligencija [@kapunac2026] pomogli su u konceptualnom razumevanju implementiranih metaheuristika i njihovu praktičnu primenu. Udžbenik _Veštačka inteligencija_ [@janicic2025] poslužio je
kao dodatni izvor pri razumevanju genetskih algoritama i njegove primene.

Strana literatura navedena u prethodnom odeljku korišćena je pre svega za deo koji je specifičan za sam problem raspoređivanja. Prvenstveno za kodiranje rešenja, strukturu rasporeda,
konstrukciju okolina i celobrojnu formulaciju, ali i za poređenje dobijenih rezultata sa objavljenim optimalnim vrednostima.

## Sadržaj i doprinos rada

U ovom radu problem je formulisan i rešavan koristeći dva pristupa.
Najpre je formulisano zajedničko kodiranje rešenja i zajednički dekoder. Zatim je nad tom formulacijom problem rešen putem četiri metaheuristike:

1. Lokalna pretraga sa ponovnim pokretanjem
2. Simulirano kaljenje
3. Metoda promenljivih okolina
4. Genetski algoritam

Nakon toga, problem je formulisan i kao zadatak celobrojnog linearnog programiranja (engl. _ILP_) i rešen egzaktnim rešavačem, radi utvrđivanja stvarnih optimuma i nezavisne provere ispravnosti implementacije.

Sve metode upoređene su pod istim uslovima uloženog truda. Dodeljen im je jednak budžet izražen brojem poziva funkcije cilja (dekodiranja), pokretane su trideset nezavisnih puta nad devet test instanci različitih dimenzija.

Rad je organizovan na sledeći način. Poglavlje 2 opisuje kodiranje rešenja, dekoder, pomoćne strukture i sve razvijene metode. Poglavlje 3 sadrži eksperimentalne rezultate, poređenje sa vrednostima iz literature i raspravu o zapaženim pojavama. Poglavlje 4 daje
zaključak i moguće pravce daljeg rada.

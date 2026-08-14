# Zaključak

U ovom radu prikazan je problem raspoređivanja poslova po mašinama a kasnije rešavan iz dva ugla. Nad zajedničkim kodiranjem rešenja (i odgovarajućim zajedničkim dekoderom) razvijene su četiri metaheuristike, a kasnije je problem formulisan i kao zadatak celobrojnog linearnog programiranja i rešen egzaktnim rešavačem.

## Postignuti rezultati

Sve implementirane metode poređene su pri istim uslovima. Svaka je imala jednak budžet od 200 000 poziva funkcije dekodiranja, trideset nezavisnih pokretanja nad devet instanci različitih veličina. Pri ovim uslovima najbolje se pokazala metoda simuliranog kaljenja sa 0,70% prosečnog odstupanja od optimuma. Niže rangirane su metoda promenljivih okolina (2,26%), genetski algoritam (2,85%) i lokalna pretraga sa ponovnim pokretanjem (4,19%).

Simulirano kaljenje uspelo je da dostigne objavljeni optimum na osam od devet instanci, s tim da ga je na instanci `ft20` pronašlo u samo jednom od trideset pokretanja. Na preostaloj instanci, `ft10`, odstupanje najboljeg pronađenog rešenja od optimuma iznosilo je 0,75%.

Konačno, celobrojni model rešen je do dokazane optimalnosti na osam od devet instanci, pri čemu se sve dobijene vrednosti poklapaju sa rezultatima iz literature. Ispravnost je potvrđena i sa druge strane, implementacijom iscrpne pretrage i njenim pokretanjem na dovoljno malim primerima.

## Zapažanja

Tri zapažanja iz merenja odstupaju od očekivanog i vredna su posebnog pomena.

**Uža okolina nije donela bolji rezultat.** Okolina zasnovana na kritičnom putu smanjuje broj kandidata po koraku između 80 i 260 puta, ali pri izjednačenom budžetu daje lošije rezultate od proste zamene dva elementa, i to u svim ispitanim postavkama. Razlozi za ovaj rezultat jesu (1) postavka eksperimenta (činjenica da formiranje ovakve okoline troši budžet pozivajući funkciju dekodiranja) i (2) činjenica da smanjivanje okoline daje plići pojam lokalnog optimuma.^[Kao što je napomenuto u sekciji 3, pretpostavljamo da bi se rezultati značajno poboljšali u slučaju drugačijeg vrednovanja budžeta kao i uvođenja strukture samog problema u metaheuristike.]

**Složenija metoda nije bila bolja.** Metoda promenljivih okolina, koja lokalnu pretragu koristi kao potprogram, izgubila je od konceptualno jednostavnijeg simuliranog kaljenja. Ovaj rezultat takođe je, bar delimično, posledica izbora metrike budžeta, s obzirom da simulirano kaljenje pri istom budžetu može da razmotri znatno više pojedinačnih stanja, a metoda promenljivih okolina uspe da pokrene lokalnu pretragu svega nekoliko puta.
Implementirane metode **nisu osetljive na vrednosti parametara u širokom opsegu**. Od četrnaest sprovedenih poređenja u analizi parametara, tek dva pokazuju značajnu razliku u odnosu na ranije ustaljene vrednosti. U oba slučaja su u pitanju donje granice, tj. granice raspada. Pri početnoj temperaturi $T_0 = 5$ simulirano kaljenje retko prihvata pogoršanja i ne uspeva da pobegne lokalnim optimumima. Slično, nizak koeficijent mutacije $p_m = 0{,}1$ ne dozvoljava genetskom algoritmu da poveća diverzitet populacije i rešenje ostaje zaglavljeno u lokalnom optimumu. Metoda promenljivih okolina pokazala se sasvim agnostična na izbor dopuštenog intenziteta udaljenosti.

## Ograničenja

Razvijene metode **ne nadmašuju rezultate iz literature**. Objavljene vrednosti za najteže instance dostignute su postupcima koji se pomažu informacijama o samoj strukturi problema, pre svega kroz korišćenje okolina nad kritičnim putem u kombinaciji sa tabu pretragom [@nowicki1996], dok su metode razvijene ovde opšte namene.

Poređenje je vođeno brojem poziva funkcije cilja. To merilo je nezavisno od mašine i implementacije, ali daje prednost metodama sa jeftinijim korakom. Posmatrajući dobijene rezultate možemo jasno videti uticaj ove odluke (sekcija 3.7).

Izbor parametara metoda nije sistemski optimizovan. Vrednosti početne i krajnje temperature, veličine populacije i verovatnoće mutacije usvojene su na osnovu preporuka iz literature i nekoliko probnih pokretanja. Naknadna analiza pokazala je da se nijedna od njih ne nalazi u području u kome metoda otkazuje. Treba imati u vidu da naša analiza ima svoja ograničenja. Najpre, menjan je po jedan parametar u isto vreme, pa uzajamna dejstva nisu ispitana, a merenje je izvedeno na tri instance uz deset pokretanja po vrednosti. Manje razlike time ostaju izvan domašaja korišćenog testa.

## Pravci daljeg rada

Najizgledniji pravac je **tabu pretraga sa okolinom nad kritičnim putem**. Merenja iz ovog rada govore nam da sama takva okolina nije dovoljna za postizanje boljeg rezultata. Očekuje se da tabu pretraga nadoknadi nedostatak raznovrsnosti okolina, a inkrementalna procena vrednosti umanji uticaj izbora metrike budžeta.

Drugi pravac je **proširenje modela na mašine sa kapacitetom većim od jedan**. U razmatranoj postavci mašina obrađuje najviše jednu operaciju u datom trenutku. Uopštenjem na kapacitet $c_k$, gde mašina istovremeno
može obrađivati do $c_k$ operacija, dobija se _kumulativni_ resurs. U praksi to odgovara datacentru sa više identičnih mašina.

Za ovaj pravac razvijeno rešenje delom može biti primenjeno bez izmena. U pomenutom problemu i dalje može biti iskorišćeno Birvirtovo kodiranje. Dekoder je potrebno blago izmeniti tako da, umesto trenutka oslobađanja mašine, čuva listu takvih trenutaka (dužine $c_k$), a operacija se smešta u najranije slobodno mesto.

Glavna teškoća je u egzaktnom modelu. Disjunktivna formulacija počiva na tome da se za svaki par operacija na istoj mašini odredi redosled, što pri kapacitetu većem od jedan više nije dovoljno i moralo bi se razmisliti o drugačijem rešenju.

Konačno, kod celobrojnog modela vredi ispitati **strože formulacije**. Slaba donja granica dobijena na instanci `ft20` posledica je velike konstante $M$ u disjunktivnim ograničenjima. Prilagođavanje ove konstante moglo bi da pomogne pri ostvarivanju boljih rezultata.

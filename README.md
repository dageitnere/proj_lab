## Ievads


Diētas optimizācijas problēma ir viena no klasiskākajiem lineārās programmēšanas piemēriem, kas pirmo reizi formulēts 20\. Gadsimta vidū ar mērķi atrast lētako risinājumu uzturam, kas vienlaikus spētu nodrošināt cilvēkam nepieciešamo uzturvielu daudzumu. Sākotnējais uzdevums tika izstrādāts ASV armijas vajadzībām (https://pmc.ncbi.nlm.nih.gov/articles/PMC6021504/\#abstract1), taču vēlāk šis mdelis ieguva plašāku pielietojumu dažados uztura plānošanas un sabiedrības veselības kontekstos. Līdz ar tehnoloģiju attīstību un lineārās programmēšanas rīku pieejamību, diētas problēmas risināšana kļuvusi efektīvāka (https://www.nature.com/articles/ejcn201556).  
Šobrīd diētas optimizācijas problēma ir aktuāla ne tikai individuāla uztura sabalansēšanā, bet arī plašākā kontekstā, piemēram, pārtikas palīdzības atbalsta programmās, ilgstpējīgas pārtikas politikas izstrādē vai valsts uztura vadlīnijās. Pētījumi rāda, ka uztura modeļus bieži ir grūti izveidot tā, lai tie vienlaikus būtu gan uzturvērtīgi, gan izmaksu ziņā efektīvi, tāpēc lineārās programmēšanas pieejas kļūst par nozīmīgu instrumentu optimāliem risinājumiem. (https://www.slideshare.net/slideshow/the-diet-problem/32900458)

## Problēmas nostādne


Ikdienā cilvēkam nepieciešams uzturs, kas nodrošina visas organismam nepieciešamās uzturvielas, taču bieži šāda uztura nodrošināšanu ierobežo gan pārtikas pieejamība, gan pārtikas cenas, gan uztura ieradumi. Bez sistemātiskas pieejas ir sarežģīti sasniegt tādu produktu komibnāciju ēdienreizei, kas vienlaikus atbilstu visiem kritērijiem. Tādēļ nepieciešams matemātisks modelis, kas spēj efektīvi optimizēt ēdienreizes sastāvu, ievērojot gan uzturvielu ierobežojumus, gan naudas patēriņu.

## Darba un novērtēšanas mērķis


Darba mērķis ir izveidot tādu lineārās programmēšanas modeli tīmekļa vietnes veidā, kas atrisinātu iepriekš minēto diētas problēmu. Modeļa izstrāde un tā rezultāti ļaus analizēt, kā dažādi lietotāju ierobežojumi, piemēram, uzturvielu daudzumi, ietekmēs gala risinājumu.

Novērtēšanas mērķis ir novērtēt aplikācijas spēju ģenerēt atbilstošās ēdienkartes dažādiem cilvēku aktivitātes līmeņiem un mērķiem.

## Līdzīgo risinājumu pārskats

Lai salīdzinātu līdzīgos risinājumus sabalansētu ēdienkaršu plānošanā, tika noteikti vienoti vērtēšanas kritēriji: 

* Funkcionalitāte \- vērtē, vai sistēma nodrošina pamatfunkcijas ēdienkaršu plānošanā (lietotāja profila un plānu saglabāšana, automātisks kaloriju aprēķins, dienas vai nedēļas ēdienkaršu ģenerēšana).  
* Pielāgojamība \- raksturo, cik elastīgi risinājums pielāgojas individuālajām vajadzībām (diētu izvēle, alerģiju ievērošana).  
* Uzturlīdzsvars un dažādība \- novērtē, cik kvalitatīvi ir izveidotie plāni (atbilstība kaloriju un makroelementu mērķiem, ēdienkartes dažādība).  
* Izmantojamība un pieejamība \- atspoguļo praktisko lietderību ikdienā (lietotāja interfeisa saprotamība, pārskatu un atskaišu pieejamība).  
* Cena \- izvērtē risinājuma izmaksas un pieejamību (bezmaksas funkciju apjoms, iespēja aprēķināt produktu izmaksas). 

| Risinājums | Pozitīvas īpašības | Trūkumi | Atsauces |
| ----- | ----- | ----- | ----- |
| Eat This Much | **Funkcionalitāte**: piejams automātisks kaloriju aprēķins, dienas ēdienkaršu ģenerēšana, plānu saglabāšana profilā. **Pielāgojamība**: diētu izvēle (vegan, vegeterian keto,  u.c.), produktus var izslēgt no ēdienkartes, ievērojot alerģijas. **Uzturlīdzsvars un dažādība**: izveidotās ēdienkartes lielākoties atbilst noteiktajiem kaloriju un makroelementu mērķiem, un tajās tiek piedāvāta pietiekama ēdienu un recepšu dažādība, kas palīdz izvairīties no vienveidības ikdienas maltītēs. **Izmantojamība un pieejamība**: platforma ir ērti lietojama ikdienā. Risinājums pieejams gan tīmekļa versijā, gan mobilajās lietotnēs, kas nodrošina ērtu piekļuvi jebkurā vietā. **Cena:** pieejama bezmaksas versija ar ierobežojumiem, Premium nodrošina nedēļas plānus un papildu iespējas, iespējams ņemt vērā arī produktu cenas (ASV cenas) | **Funkcionalitāte:** bezmaksas versijā var izmantot tikai dienas plānošanu, nedēļas plāni pieejami tikai Premium lietotājiem. **Izmantojamība un pieejamība:** daudzas ērtas funkcijas, piemēram, PDF eksports vai iepirkumu saraksti, pieejamas tikai maksas versijā. **Cena:** Premium cena ir 14.99$ par menesi, un izmaksas rēķinātas pēc ASV produktu bāzes. | [https://www.eatthismuch.com/app/planner/today](https://www.eatthismuch.com/app/planner/today)  |
| MyNetDiary | **Funkcionalitāte:** sistēma nodrošina kaloriju automātisku aprēķinu, uzturvielu bilances uzraudzību, ēdienu datubāzi, kā arī dienas ēdienkaršu plānošanu; **Pielāgojamība:** iespējams izvēlēties dažādas diētas (keto, veģetāriešu, diabēta u.c.), pievienot produktus manuāli un ņemt vērā alerģijas;  **Uzturlīdzsvars un dažādība:** ģenerētie plāni tiek veidoti atbilstoši lietotāja mērķiem (svara samazināšana, noturēšana vai palielināšana), piedāvā dažādus ēdienu variantus; **Izmantojamība un pieejamība:** pieejama mobilā lietotne (iOS, Android), intuitīvs interfeiss, datu sinhronizācija ar viedpulksteņiem un fitnesa ierīcēm; **Cena:** ir bezmaksas versija, kurā iekļauta kaloriju uzskaite un pamata uzturvielu kontrole. | **Funkcionalitāte:** bezmaksas versijā nav automātiskas nedēļas ēdienkaršu ģenerēšanas;  **Pielāgojamība:** atsevišķas specializētas diētas pieejamas tikai Premium versijā; **Uzturlīdzsvars un dažādība:** datubāze vairāk orientēta uz ASV produktiem, trūkst vietējo produktu; **Cena:** Premium(9.00$ menesī) nepieciešams, lai piekļūtu pilnai ēdienkaršu plānošanai, cenu uzskaite nav pieejama. | [https://www.mynetdiary.com/](https://www.mynetdiary.com/) |
| Prospre | **Funkcionalitāte:** ir pieejami automātiski kaloriju un uzturvielu aprēķini, ir pieejama ikdienas/nedēļas ēdienkartes ģenerēšana, un plānus var saglabāt profilā. **Pielāgojamība**: ir iespēja izvēlēt diētas veidu (vegānisks, veģetāriešu utt.), izslēgt no ēdienkartes pārtikas produktus, pamatojoties uz alerģijām un nepanesamību. **Uzturlīdzsvars un dažādība**: plāni ir balstīti uz kaloriju un makroelementu mērķiem, ir pieejams plašs ēdienu klāsts, un ir pieejama “swap” funkcija. **Izmantojamība un pieejamība:** skaidrs interfeiss, pieejamas atskaites un iepirkumu saraksti. **Cena:** pamata funkcijas ir bez maksas, papildu funkcijas ir pieejamas pēc abonēšanas. | **Funkcionalitāte:** Bezsaistes darba iespējas ir ierobežotas. **Pielāgojamība**: produktu bāze ir orientēta uz ASV, daži vietējie produkti var trūkt. **Uzturlīdzsvars un dažādība**: ar ierobežotu tarifu dažus ēdienus var atkārtot. **Cena:** lielākajai daļai uzlaboto funkciju ir nepieciešams maksas abonements.(51$ gadā) | [Prospre \- Meal Planner App](https://www.prospre.io/?ref=toolboxable) |
| StrongrFastr | **Funkcionalitāte:** automātiska ēdienreižu plānu ģenerēšana, pamatojoties uz kaloriju un makroelementu mērķiem, profilu un plānu saglabāšana. **Pielāgojamība**: atbalsts dažādiem diētu veidiem, iespēja ņemt vērā alergēnus izraisošus pārtikas produktus, elastīgi iestatījumi (receptes sarežģītība, ēdienu biežums, ēdienkartes daudzveidība). **Uzturlīdzsvars un dažādība**: receptes ir sabalansētas atbilstoši jūsu mērķiem (svara zaudēšana, svara pieaugums, svara uzturēšana), ēdienu izvēle ir plaša. **Izmantojamība un pieejamība:** vienkārša saskarne, iespēja pielāgot atskaites, automātisks produktu saraksts. **Cena:** dažas funkcijas un pamata piekļuve ir bez maksas | **Funkcionalitāte:** ierobežots bezsaistes režīms **Uzturlīdzsvars un dažādība**: ar bezmaksas piekļuvi ēdienu klāsts ir ierobežots.  **Cena:** lielākajai daļai uzlaboto funkciju ir nepieciešams maksas abonements (middle-pro 57$, pro 89$ gadā) | [Strongr Fastr: AI Nutrition, Workouts, and Meal Planner](https://www.strongrfastr.com/) |
| MyFitnessPal | **Funkcionalitāte:** nodrošina kaloriju, makroelementu un mikroelementu uzskaiti, piedāvā detalizētu uztura analīzi pa ēdienreizēm, dienām un nedēļām. Lietotājs var viegli reģistrēt pārtiku, saņem pilnīgu pārskatu par uzturu un sekot saviem mērķiem. **Pielāgojamība:** piedāvā plānus 10 diētu tipiem un ņem vērā lietotāja pārtikas preferences, alerģijas un iecienītākās virtuves. **Uzturlīdzsvars un dažādība:** plāni veidoti, lai palīdzētu sasniegt mērķus (piem., proteīna uzņemšanu vai kaloriju kontroles), nodrošinot sabalansētu uzturu un ēdienu dažādību. **Izmantojamība un pieejamība:** viegli lietojams interfeiss, pieejams iOS, Android un web platformās. **Cena:** bezmaksas versija ar pamata funkcijām. | **Funkcionalitāte:** bezmaksas versijā nav automātiskas nedēļas ēdienkaršu ģenerēšanas; Premium+ plānotājs pieejams tikai noteiktās valstīs (ASV, AK, Kanāda, Īrija, Jaunzēlande, Austrālija). **Pielāgojamība:** dažas specializētas funkcijas un diētas pieejamas tikai Premium+ abonementā.  **Cena:** Premium+ maksā 9,99 €/mēnesī vai 49,99 €/gadā. | [https://www.myfitnesspal.com/](https://www.myfitnesspal.com/)  |
| Yazio | **Funkcionalitāte:** piedāvā kaloriju un makroelementu uzskaiti, uztura dienasgrāmatu, personalizētu ēdienkaršu plānošanu un receptes; automātiski aprēķina nepieciešamās uzturvielas un palīdz sasniegt personīgos mērķus. **Pielāgojamība:** pielāgojas lietotāju uztura izvēlei, piemēram, veģetāram, vegānam vai pescetāram uzturam. **Uzturlīdzsvars un dažādība:** plāni veidoti, lai palīdzētu sasniegt mērķus (piem., svara zudums vai muskuļu masas palielināšana), nodrošinot sabalansētu uzturu un plašu ēdienu dažādību.. **Izmantojamība un pieejamība:** viegli lietojams interfeiss, pieejams iOS un Android platformās. **Cena:** bezmaksas versija ar pamata funkcijām. | **Funkcionalitāte:** dažiem produktiem kaloriju un uzturvielu dati var neatbilst realitātei; daļa noderīgu funkciju pieejama tikai maksas versijā. **Uzturlīdzsvars un dažādība:** piedāvātie ēdienkaršu plāni dažkārt ir pārāk standartizēti un ne vienmēr atbilst individuālajām ēdienreižu izvēlēm vai gaumei.  **Cena:** Pro maksā 10,00 €/mēnesī. | [https://www.yazio.com/en](https://www.yazio.com/en)  |

**Tehniskais risinājums**

1. **Prasības:**  
   1. Must haves:  
      1. Lietotājs vēlas reģistrēties un pieteikties sistēmā, jo tādējādi viņš varēs saglabāt savas ēdienkartes un personalizēt prognozes;  
      2. Lietotājs vēlas apskatīt, rediģēt vai dzēst savas iepriekšējās ēdienkartes prognozes, jo tas ļauj kontrolēt un uzlabot savus uztura paradumus;  
      3. Lietotājs vēlas automātiski aprēķināt nepieciešamās kalorijas un uzturvielas jaunajai ēdienkartei pēc lietotāja fiziskiem datiem, jo tas ļauj nodrošināt precīzu un sabalansētu uzturu katram lietotājam;  
      4. Lietotājs vēlas ģenerēt jaunu sabalansētas ēdienkartes prognozi, jo sistēma viņam palīdzēs iegūt uzturvielām līdzsvarotu un daudzveidīgu ēdienkarti bez manuālas aprēķināšanas;  
      5. Lietotājs vēlas redzēt ēdienkartes datus apkopotā veidā, jo tas ļauj viegli saprast uzturvielu sadalījumu un kaloriju patēriņu.  
   2. Should haves:  
      1. Lietotājs vēlas filtrēt ēdienkartes pēc produktiem, jo tas ļauj viegli izveidot ēdienkarti atbilstoši savām vēlmēm vai diētām;  
      2. Lietotājs vēlas redzēt ēdienu recepšu idejas, jo tas atvieglo ēšanas plānošanu;  
      3. Lietotājs vēlas aprēķināt ikdienas kaloriju un uzturvielu sadalījumu katram ēdienam, jo tas nodrošina detalizētu informāciju par katru ēdienreizi;  
      4. Lietotājs vēlas atzīmēt apēstos ēdienus sistēmā, jo tas ļauj veikt tālāko analīzi;  
      5. Lietotājs vēlas pielāgot dažu uzturvielu daudzumu savā ēdienkartē attiecīgi mērķiem (muskuļu masas augšana/svara balansēšana/svara zaudēšana).  
   3. Could haves:  
      1. Lietotājs vēlas redzēt ēdienu bildes, jo tas palīdz vieglāk saprast lietotājam, kura recepte viņam būs garšīgāka;  
      2. Lietotājs vēlas saņemt informāciju par produktu pieejamību un cenu blakusesošos veikalos, jo tas var atvieglot produktu iepirksānas plānošanu;  
      3. Lietotājs vēlas automātiski pasūtīt produktu grozu no veikala, jo tā var ietaupīt laiku;  
      4. Lietotājs vēlas saglabāt iecienītākos ēdienus vai receptes, jo tas paātrina nākotnes ēdienkaršu veidošanu;  
      5. Lietotājs vēlas ģenerēt nedēļas vai mēneša pārskatus par lietotāja uztura paradumiem, jo tas palīdz lietotājam sekot līdzi savam progresam un veselības mērķiem.  

## Algoritms
Aplikācija izmanto lineārās programmēšanas (LP) pieeju un SIMPLEX algoritmu, lai izveidotu lietotājam optimizētu, uzturvielām sabalansētu ēdienkarti, kas atbilst gan uztura mērķiem, gan produktu ierobežojumiem. Algoritms tiek realizēts ar PuLP bibliotēku

### Algoritmam ir sekojošas iezīmes:
* Atbilst lietotāja kaloriju un uzturvielu mērķiem.
* Ievēro diētas tipu (vegāns, veģetārietis, bez piena).
* Ievēro lietotāja produktu ierobežojumus (min/max svars, izslēgšana).
* Nodrošina dažādību (≥ 15 produkti ar ≥ 50g katrs).
* Saglabā olbaltumvielu avotu proporcijas (dzīvnieku / piena / augu).

### Algoritms saņem:
* Lietotāja uztura mērķus (kcal, proteīni, tauki, ogļhidrāti, utt.),
* Diētas tipu (vegāns, veģetārietis, bez piena),
* Produktu ierobežojumus,
* Produktus no datubāzes (globālie + lietotāja).

### LP problēma:

Mērķa funkcija - minimizēt kopējās izmaksas:

*Minimize ∑(xi⋅pricei)*,

kur:
* xi - produkta i svars,
* pricei - produkta i cena uz 100 gramiem.

### Lēmumu maiņigie:
* x_i - produkta daudzums gramos.
* y_i - binārais mainīgais, kas norāda, vai produkts i tiek iekļauts ēdienkartē (1) vai nē (0).

### Iekšējie ierobežojumi:
* xi ≤ M⋅yi.
* xi ≥ m⋅yi.

kur:
* M - maksimālais produkta daudzums gramos (400).
* m - minimālais produkta daudzums gramos (50).

### Uzturvielu ierobežojumi:
Katram uzturvielu veidam definēti min/max robežu intervāli, lai izvairītos no pārpielagošanas problēmas, piemēram:
* Kalorijas: 0.9⋅kcal(target) ≤ ∑(xi⋅kcali) ≤ 1.3⋅kcal(target)

### Proteīnu avotu ierobežojumi:
Ēdienkartei tiek kontrolēta olbaltumvielu avotu proporcija (tiek ņemti vērā lietotāja diētas ierobežojumi):
* Dzīvnieku olbaltumvielas (~40% no mērķa).
* Piena olbaltumvielas (~30% no mērķa).
* Augu olbaltumvielas (~30% no mērķa).

### Daudzveidības ierobežojums:
Lai nodrošinātu ēdienkartes dažādību, tiek ieviests ierobežojums, kas prasa iekļaut vismaz 10 dažādus produktus:
* ∑yi ≥ 10

### Lietotāja produktu ierobežojumi:
Piemēri:
* max_weight xi: produkta xi svars nevar pārsniegt noteikto maksimālo vērtību.
* min_weight xi: produkta xi svars nevar būt mazāks par noteikto minimālo vērtību.
* exclude xi: produkts xi tiek pilnībā izslēgts.

### Rezultātu iegūšana:
* Tiek atlasīti produkti ar x_i > 0 un y_i =1.
* Tiek aprēķinātas kopējās uzturvielas.
* Tiek ģenerēta GenerateMenuResponse struktūra.
## Konceptu modelis

![UML Diagram](https://i.ibb.co/xq10VNw9/image.png)

```plantuml
@startuml
hide circle
skinparam linetype ortho
skinparam entity {
  BackgroundColor White
  BorderColor Black
}

entity "lietotāji" as users {
  + uuid : bigint
  --
  username : text
  email : text
  age : bigint
  gender : text
  weight : double
  height : double
  bmi : double
  bmr : double
  goal : text
  activityFactor : text
}

entity "produkti" as products {
  + id : bigint
  --
  productName : text
  protein : double
  dairyProt : double
  animalProt : double
  plantProt : double
}

entity "lietotāju pievienotie produkti" as userProducts {
  + id : bigint
  --
  productName : text
  kcal : bigint
  fat : double
  carbs : double
  protein : double
  price1kg : double
  vegan : boolean
}

entity "lietotāju apēstie produkti" as userConsumedProducts {
  + id : bigint
  --
  productName : text
  amount : double
  kcal : double
  protein : double
  cost : double
  date : timestamp
}

entity "lietotāju ēdienkartes" as userMenu {
  + id : bigint
  --
  date : timestamp
  name : text
  totalKcal : double
  totalCost : double
  vegan : boolean
  vegetarian : boolean
  dairyFree : boolean
}

entity "ēdienreize" as meal {
  mealType : breakfast / lunch / dinner / snack
}

entity "receptes" as recipes {
  + id : bigint
  --
  name : text
  calories : double
}

entity "uzturvērtība" as nutrition {
  kcal : number
  protein : number
  fat : number
  carbs : number
  sugar : number
  salt : number
}

' =====================
' Relācijas
' =====================

users ||--o{ userMenu : ģenerē
users ||--o{ userProducts : pievieno
users ||--o{ userConsumedProducts : reģistrē

userMenu ||--o{ meal : sastāv no
userMenu ||--o{ products : sastāv no
meal ||--o{ recipes : ietver ģenerētās

' Produktu saiknes
products ||--o{ userProducts : ietver
products ||--o{ userConsumedProducts : ietver

products ||--|| nutrition : satur


@enduml
```

## Tehnoloģiju steks


### Frontend


*   **React + Tailwind CSS** – nodrošina modernu, reaģējošu un interaktīvu lietotāja saskarni (piemērots sarežģītākām un dinamiskām funkcijām).


### Backend

*   **FastAPI** – ātrs Python tīmekļa ietvars, kas nodrošina REST API izveidi ar automātisku dokumentāciju.
    
*   **PuLP** – izmanto optimizācijas algoritmu realizācijai.
    

### Datu bāze


*   **PostgreSQL** – relāciju datu bāzes pārvaldības sistēma ar augstu veiktspēju un paplašināmību.
    
*   **SQLAlchemy ORM** – Python ORM rīks datu modeļu definēšanai un manipulācijai.
* **Papildu risinājums:**
    
    *   **Supabase** – mākoņbāzēta PostgreSQL platforma ar iebūvētu API un autentifikācijas iespējām.
        

### Datu apstrāde

    
*   **API integrācija** – datu saņemšana un apstrāde caur FastAPI backend.
    

### Datu vizualizācija


*   **React komponentes** – datu attēlošanai frontend vidē.


### Operētājsistēma


*   **Linux (Ubuntu)** – galvenā izvietošanas vide.
    

### Servera infrastruktūra


*   **Microsoft Azure** – galvenā hostinga platforma (nodrošināta ar RTU finansējumu).

## Programmatūras apraksts

## Novērtējums

### 1. **Novērtēšanas plāns**  
#### Eksperimenta mērķis
Novērtēšanas mērķis ir analizēt un pārbaudīt, kā izstrādātā diētas optimizācijas aplikācija spēj ģenerēt sabalansētas un lietotāja vajadzībām atbilstošas ēdienkartes dažādiem cilvēku aktivitātes līmeņiem un mērķiem. Tā kā optimālās ēdienkartes aprēķināšana balstās uz lineārās programmēšanas modeli, kura uzdevums ir nodrošināt precīzu uzturvielu, kaloriju un cenas līdzsvaru, ir būtiski izvērtēt aplikācijas veiktspēju praksē un tās spēju pielāgoties atšķirīgām lietotāju prasībām.
#### Ieejas parametri
* Lietotāja aktivitātes līmenis (mazkustīgs, mērens, ļoti aktīvs). Šie līmeņi tika izvēlēti, jo tie aptver cilvēku kustības spektru, sākot no mazkustīga dzīvesveida līdz ļoti aktīvam (programmas pilnais aktivitātes līmeņu saraksts - mazkustīgs, viegls, merēns, aktīvs, ļoti aktīvs).
* Lietotāja mērķi (svara zaudēšana, svara uzturēšana, muskuļu masas palielināšana).
* Lietotāja ierobežojumu skaits (0, 3, 6). Tika izvēlēti tieši šie skaitļi, jo programma nodrošina 3 veidu ierobežojumus, tāpēc tādā veidā var nodrošināt dažāda veida ierobežojumu skaitu līdzīgo sadalījumu.
* Diētas preference (nav, piena nepanesība). Tika izvēlētā piena nepanesība, jo tā ir viena no izplatītākajām pārtikas nepanesībām.
#### Novērtēšanas metrikas
* Ēdienkartes ģenerēšanas laiks.
* Recepšu un ēdienu bilžu ģenerēšanas laiks.
* Barības vielu un kaloriju precizitāte.

| Numurs | Aktivitātes līmenis | Mērķis           | Ierobežojumu skaits | Diētas preference | Ēdienkartes ģenerēšanas laiks | Recepšu un ēdienu bilžu ģenerēšanas laiks | Barības vielu un kaloriju precizitāte |
|--------|----------------------|-------------------|----------------------|-------------------|-------------------------------|--------------------------------------------|----------------------------------------|
| 1  | Mazkustīgs | Svara zaudēšana   | 0 | Nav | | | |
| 2  | Mazkustīgs | Svara zaudēšana   | 0 | Piena nepanesība | | | |
| 3  | Mazkustīgs | Svara zaudēšana   | 3 | Nav | | | |
| 4  | Mazkustīgs | Svara zaudēšana   | 3 | Piena nepanesība | | | |
| 5  | Mazkustīgs | Svara zaudēšana   | 6 | Nav | | | |
| 6  | Mazkustīgs | Svara zaudēšana   | 6 | Piena nepanesība | | | |
| 7  | Mazkustīgs | Svara uzturēšana  | 0 | Nav | | | |
| 8  | Mazkustīgs | Svara uzturēšana  | 0 | Piena nepanesība | | | |
| 9  | Mazkustīgs | Svara uzturēšana  | 3 | Nav | | | |
| 10 | Mazkustīgs | Svara uzturēšana  | 3 | Piena nepanesība | | | |
| 11 | Mazkustīgs | Svara uzturēšana  | 6 | Nav | | | |
| 12 | Mazkustīgs | Svara uzturēšana  | 6 | Piena nepanesība | | | |
| 13 | Mazkustīgs | Muskuļu uzņemšana | 0 | Nav | | | |
| 14 | Mazkustīgs | Muskuļu uzņemšana | 0 | Piena nepanesība | | | |
| 15 | Mazkustīgs | Muskuļu uzņemšana | 3 | Nav | | | |
| 16 | Mazkustīgs | Muskuļu uzņemšana | 3 | Piena nepanesība | | | |
| 17 | Mazkustīgs | Muskuļu uzņemšana | 6 | Nav | | | |
| 18 | Mazkustīgs | Muskuļu uzņemšana | 6 | Piena nepanesība | | | |
| 19 | Mērens | Svara zaudēšana   | 0 | Nav | | | |
| 20 | Mērens | Svara zaudēšana   | 0 | Piena nepanesība | | | |
| 21 | Mērens | Svara zaudēšana   | 3 | Nav | | | |
| 22 | Mērens | Svara zaudēšana   | 3 | Piena nepanesība | | | |
| 23 | Mērens | Svara zaudēšana   | 6 | Nav | | | |
| 24 | Mērens | Svara zaudēšana   | 6 | Piena nepanesība | | | |
| 25 | Mērens | Svara uzturēšana  | 0 | Nav | | | |
| 26 | Mērens | Svara uzturēšana  | 0 | Piena nepanesība | | | |
| 27 | Mērens | Svara uzturēšana  | 3 | Nav | | | |
| 28 | Mērens | Svara uzturēšana  | 3 | Piena nepanesība | | | |
| 29 | Mērens | Svara uzturēšana  | 6 | Nav | | | |
| 30 | Mērens | Svara uzturēšana  | 6 | Piena nepanesība | | | |
| 31 | Mērens | Muskuļu uzņemšana | 0 | Nav | | | |
| 32 | Mērens | Muskuļu uzņemšana | 0 | Piena nepanesība | | | |
| 33 | Mērens | Muskuļu uzņemšana | 3 | Nav | | | |
| 34 | Mērens | Muskuļu uzņemšana | 3 | Piena nepanesība | | | |
| 35 | Mērens | Muskuļu uzņemšana | 6 | Nav | | | |
| 36 | Mērens | Muskuļu uzņemšana | 6 | Piena nepanesība | | | |
| 37 | Ļoti aktīvs | Svara zaudēšana   | 0 | Nav | | | |
| 38 | Ļoti aktīvs | Svara zaudēšana   | 0 | Piena nepanesība | | | |
| 39 | Ļoti aktīvs | Svara zaudēšana   | 3 | Nav | | | |
| 40 | Ļoti aktīvs | Svara zaudēšana   | 3 | Piena nepanesība | | | |
| 41 | Ļoti aktīvs | Svara zaudēšana   | 6 | Nav | | | |
| 42 | Ļoti aktīvs | Svara zaudēšana   | 6 | Piena nepanesība | | | |
| 43 | Ļoti aktīvs | Svara uzturēšana  | 0 | Nav | | | |
| 44 | Ļoti aktīvs | Svara uzturēšana  | 0 | Piena nepanesība | | | |
| 45 | Ļoti aktīvs | Svara uzturēšana  | 3 | Nav | | | |
| 46 | Ļoti aktīvs | Svara uzturēšana  | 3 | Piena nepanesība | | | |
| 47 | Ļoti aktīvs | Svara uzturēšana  | 6 | Nav | | | |
| 48 | Ļoti aktīvs | Svara uzturēšana  | 6 | Piena nepanesība | | | |
| 49 | Ļoti aktīvs | Muskuļu uzņemšana | 0 | Nav | | | |
| 50 | Ļoti aktīvs | Muskuļu uzņemšana | 0 | Piena nepanesība | | | |
| 51 | Ļoti aktīvs | Muskuļu uzņemšana | 3 | Nav | | | |
| 52 | Ļoti aktīvs | Muskuļu uzņemšana | 3 | Piena nepanesība | | | |
| 53 | Ļoti aktīvs | Muskuļu uzņemšana | 6 | Nav | | | |
| 54 | Ļoti aktīvs | Muskuļu uzņemšana | 6 | Piena nepanesība | | | |
### 2. **Novērtēšanas rezultāti**

## Secinājumi

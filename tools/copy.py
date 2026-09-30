"""Hand-written Swedish copy for the generated pages.

Kept out of build.py so text edits never touch layout. Fragments are plain
HTML; `{y}` is the page's year and `{n}` the län name where used. AdSense
rejected the site for "low value content", so every generated page carries a
few hundred words that the tables alone cannot say.
"""

HUB = {}
GROUPS = {}
DAYS = {}

HUB["year"] = """
<h2>Så fungerar röda dagar</h2>
<p>En röd dag är en allmän helgdag enligt lag (1989:253) om allmänna helgdagar. Sverige har tretton sådana dagar om året: nyårsdagen, trettondedag jul, långfredagen, påskdagen, annandag påsk, första maj, Kristi himmelsfärdsdag, pingstdagen, nationaldagen, midsommardagen, alla helgons dag, juldagen och annandag jul. Lagen räknar också varje söndag som helgdag, vilket är skälet till att söndagarna är röda i almanackan.</p>
<p>Sex av dagarna har fasta datum, fem följer påsken och två ligger alltid på en lördag. Därför varierar antalet röda dagar som hamnar på en vardag från år till år. Infaller en röd dag på en helg får du ingen ersättningsdag, till skillnad från i till exempel Storbritannien, och det är det som gör att vissa år känns snåla och andra generösa.</p>
<h2>Aftnar och andra lediga dagar</h2>
<p>Midsommarafton, julafton och nyårsafton är inte röda dagar, men i praktiken lediga för de allra flesta. Semesterlagen jämställer dem med söndag, så de kostar inga semesterdagar. Många kollektivavtal ger dessutom halv dag på skärtorsdagen, valborgsmässoafton, allhelgonaafton och trettondagsafton. Vad som gäller på din arbetsplats står i kollektivavtalet eller i personalhandboken.</p>
<h2>Röda dagar och semester</h2>
<p>Semesterlagen ger dig minst 25 semesterdagar om året. Lördagar, söndagar och röda dagar räknas inte som semesterdagar, vilket är hela poängen med klämdagar: en semesterdag som placeras mellan en röd dag och en helg köper flera lediga dagar. På sidan för klämdagar finns en dag-för-dag-remsa för varje tillfälle {y} som visar exakt vilka datum du behöver ta ut.</p>
<h2>Vad kolumnerna betyder</h2>
<p>Typ-kolumnen skiljer på tre saker. Röd dag är en helgdag enligt lag. Ledig är en afton som inte är röd men som nästan alla har ledigt. Märkesdag är en dag som är utmärkt i almanackan utan att vara ledig, som mors dag, fars dag och lucia. Klämdag-kolumnen visar om det finns en vardag intill helgdagen som är värd att ta ledigt.</p>
<h2>Planera året</h2>
<p>De stora chanserna återkommer varje år: fredagen efter Kristi himmelsfärdsdag är alltid en klämdag, dagarna kring påsk och jul ger långledigt för få semesterdagar, och när nationaldagen eller första maj hamnar på en tisdag eller torsdag uppstår en klämdag mitt i veckan. Kalendrarna längst ned visar hela året i ett svep med veckonummer, och varje månad går att skriva ut.</p>
"""

HUB["klamdagar"] = """
<h2>Vad är en klämdag?</h2>
<p>En klämdag är en vanlig arbetsdag som ligger inklämd mellan en röd dag och en helg, eller mellan två röda dagar. Klämdagen är inte ledig i sig. Den kostar en semesterdag, en flexdag eller en kompledig dag, om inte arbetsgivaren väljer att stänga. Poängen är utväxlingen: en dag ut, fyra eller fler dagar ledigt.</p>
<h2>Så räknar vi</h2>
<p>Listan ovan tar varje sammanhängande rad av arbetsdagar mellan två lediga dagar och prövar att ta en, två eller tre semesterdagar. Ett tillfälle kommer med om vinsten är minst tre lediga dagar utöver de dagar du tar ut, och om spannet innehåller en röd dag eller en afton på en vardag. Två enstaka klämdagar som bara skiljs åt av en helg slås ihop, som 2 och 5 januari när trettondedag jul ligger rätt. Lördag och söndag räknas alltid som lediga, liksom midsommarafton, julafton och nyårsafton.</p>
<h2>Klämdagar som återkommer varje år</h2>
<p>Fredagen efter Kristi himmelsfärdsdag är den säkraste klämdagen i Sverige, eftersom helgdagen alltid ligger på en torsdag. Skärtorsdagen och dagarna före gör påsken till en tiodagarshelg för fyra semesterdagar. Mellandagarna mellan jul och nyår ger ofta elva lediga dagar för tre. Nyårsdagen, trettondedag jul, första maj, nationaldagen och juldagarna vandrar genom veckan, så deras klämdagar kommer och går med årtalet.</p>
<h2>Vad kollektivavtalet säger</h2>
<p>Semesterlagen ger dig rätt till minst 25 dagars semester och till fyra sammanhängande veckor under juni till augusti, men enstaka dagar under resten av året beviljas i mån av verksamhet. Vill du ha klämdagen ledig bör du be om den tidigt; på många arbetsplatser är den mer eftertraktad än en vanlig vecka i juli. En del arbetsgivare stänger helt på klämdagar och drar dagarna från semestern eller ger dem som förmån. Kontrollera vad som gäller för dig innan du bokar resan.</p>
<h2>Halvdagar</h2>
<p>Trettondagsafton, skärtorsdagen, valborgsmässoafton och allhelgonaafton är inte lediga enligt lag, men många kollektivavtal förkortar arbetsdagen. De syns inte i listan ovan eftersom de inte ändrar hur många hela dagar du får ut, men de gör klämdagarna kring påsk och allhelgona ännu mer värda.</p>
"""

HUB["skollov"] = """
<h2>Så bestäms loven</h2>
<p>Läsåret i grundskolan ska enligt skolförordningen ha minst 178 skoldagar och minst tolv lovdagar utöver helgerna. Exakt när loven ligger bestämmer varje kommun i sin läsårsplan, och friskolor får sätta egna datum. Sportlovet och höstlovet har ändå blivit så samordnade att de i praktiken följer länet: alla kommuner i Stockholms län har sportlov samma vecka, alla i Skåne en annan.</p>
<h2>Varför sportlovet ligger olika veckor</h2>
<p>Sportlovet infördes under andra världskriget som kokslov: skolorna stängde en vecka på vintern för att spara bränsle. Efter kriget behölls veckan som ett friluftslov, och för att sprida trycket på fjällanläggningar och tåg fick länen olika veckor. Mönstret är i stort sett detsamma varje år, Götaland först, Svealand i mitten och Norrland sist. Tabellen ovan har den vecka som gäller {y}; det är sällan den ändras, men kontrollera alltid mot skolans läsårsplan.</p>
<h2>Höstlovet</h2>
<p>Höstlovet är vecka 44 i praktiskt taget hela landet, alltid den vecka som slutar med alla helgons dag. Sedan 2016 kallas det läslov i många kommuner efter en satsning på läsning, men veckan är densamma.</p>
<h2>Påsklov, sommarlov och jullov</h2>
<p>De tre övriga loven varierar mer. Påsklovet ligger antingen veckan före eller veckan efter påsk beroende på kommun, och kan därför skilja sig mellan grannkommuner. Sommarlovet börjar i mitten av juni och slutar i mitten av augusti, oftast tio veckor. Jullovet börjar några dagar före jul och slutar strax efter trettondedag jul. Eftersom de datumen sätts per kommun listar vi dem inte här; din skolas läsårsplan är den enda säkra källan.</p>
<p>Lovveckorna gäller grundskolan. Gymnasieskolorna har i regel samma sportlov och höstlov, medan förskolan och fritidshemmet är öppna som vanligt under loven, oftast med förbokning. Friskolor följer ofta kommunens lov, men inte alltid.</p>
"""

GROUPS["pask"] = """
<h2>Varför påsken flyttar sig</h2>
<p>Påskdagen är den första söndagen efter den första fullmånen på eller efter vårdagjämningen, räknat efter kyrkans tabeller snarare än den faktiska månen. Därför kan påskdagen infalla så tidigt som 22 mars och så sent som 25 april. Långfredagen, påskafton och annandag påsk följer med, liksom Kristi himmelsfärdsdag 39 dagar senare och pingstdagen 49 dagar senare. Hela den rörliga delen av almanackan hänger på ett enda datum.</p>
<h2>Lediga dagar under påsken</h2>
<p>Långfredagen och annandag påsk är röda dagar, påskdagen är en söndag och påskafton en lördag. Det ger en fyradagarshelg utan att en enda semesterdag går åt. Ta skärtorsdagen och de tre dagarna före, så är du ledig tio dagar i följd för fyra semesterdagar; hur klämdagarna faller {y} ser du på klämdagssidan. Skärtorsdagen är dessutom halvdag i många kollektivavtal.</p>
<h2>Påsklovet</h2>
<p>Skolornas påsklov ligger antingen veckan före påsk, stilla veckan, eller veckan efter, och det avgörs kommun för kommun. Är du osäker, se läsårsplanen. Sidan för skollov visar bara sportlov och höstlov, eftersom de är de enda loven som är samordnade per län.</p>
"""

GROUPS["midsommar"] = """
<h2>Alltid en fredag och en lördag</h2>
<p>Sedan 1953 firas midsommar på en helg i stället för på ett fast datum. Midsommardagen är den lördag som infaller mellan 20 och 26 juni, och midsommarafton är fredagen före, mellan 19 och 25 juni. Flytten gjordes för att alla skulle få en sammanhängande ledighet; tidigare låg midsommardagen alltid den 24 juni oavsett veckodag.</p>
<h2>Ledigt utan semesterdagar</h2>
<p>Midsommardagen är en röd dag men ligger alltid på en lördag, så den ger ingen extra ledighet för den som arbetar vardagar. Midsommarafton är inte en röd dag enligt lag, men den räknas som söndag i semesterlagen och nästan alla arbetsplatser har stängt. Vill du ha en längre ledighet är torsdagen före midsommarafton en klassisk klämdag: en semesterdag ger fyra dagar ledigt. Många börjar också sin sommarsemester veckan efter midsommar, då stora delar av landet går ned i varv.</p>
"""

GROUPS["jul"] = """
<h2>Röda dagar och aftnar i jul</h2>
<p>Juldagen och annandag jul är röda dagar; julafton är det inte, men den räknas som söndag i semesterlagen och i praktiken är landet stängt. Trettondedag jul den 6 januari är också en röd dag, medan trettondagsafton ofta är halvdag. Nyårsdagen är röd och nyårsafton jämställs med söndag på samma sätt som julafton. Vilka veckodagar de här datumen hamnar på avgör hur mycket ledighet julen ger utan semester: en jul där julafton är torsdag ger fyra dagar i rad, en jul där julafton är lördag ger nästan ingenting.</p>
<h2>Mellandagarna</h2>
<p>Mellandagarna är vardagarna mellan annandag jul och nyårsafton, som mest fyra stycken. Tar du dem som semester blir du ofta ledig från julafton till efter nyår, mer än en vecka för tre eller fyra semesterdagar. På många arbetsplatser är mellandagarna lugna, och en del företag stänger helt och drar dagarna från semestern. Räkna på ditt år på klämdagssidan.</p>
<h2>Jullovet</h2>
<p>Skolornas jullov börjar vanligen några dagar före julafton och pågår till strax efter trettondedag jul, ungefär två och en halv vecka. Datumen sätts av varje kommun.</p>
"""

DAYS["nyarsdagen"] = """
<h2>Om nyårsdagen</h2>
<p>Nyårsdagen är årets första röda dag och en av de sex helgdagarna med fast datum. Dagen efter nyårsafton är nästan allt stängt, och de flesta butiker öppnar först den 2 januari. Infaller nyårsdagen på en torsdag är fredagen den 2 januari en klämdag, ofta i kombination med dagarna före trettondedag jul den 6 januari.</p>
<p>Nyårsafton är inte en röd dag men jämställs med söndag i semesterlagen, så den kostar ingen semester. Ligger nyårsafton och nyårsdagen på torsdag och fredag får du fyra dagar i rad utan att ta ut något.</p>
"""

DAYS["trettondedag-jul"] = """
<h2>Om trettondedag jul</h2>
<p>Trettondedag jul den 6 januari firas till minne av de tre vise männens besök och är en röd dag i Sverige, till skillnad från i Danmark och Norge. Trettondagsafton den 5 januari är inte ledig enligt lag, men många kollektivavtal ger halvdag.</p>
<p>Hamnar trettondedagen på en tisdag eller torsdag blir måndagen eller fredagen en klämdag, ofta i kombination med den 2 januari. Trettondedag jul avslutar julen i almanackan; tjugondag Knut den 13 januari, då granen dansas ut, är ingen helgdag.</p>
"""

DAYS["langfredagen"] = """
<h2>Om långfredagen</h2>
<p>Långfredagen är fredagen före påskdagen och en röd dag till minne av Jesu korsfästelse. Fram till 1969 rådde nöjesförbud på långfredagen, med stängda biografer och danslokaler. Eftersom påsken flyttar sig varierar långfredagen mellan 20 mars och 23 april.</p>
<p>Tillsammans med annandag påsk ger den en fyradagarshelg utan semester. Skärtorsdagen dagen före är halvdag på många arbetsplatser och en av årets bästa klämdagar.</p>
"""

DAYS["paskafton"] = """
<h2>Om påskafton</h2>
<p>Påskafton är lördagen före påskdagen och ingen röd dag, men den är alltid en lördag och därför ledig för de flesta. Det är dagen för påskmiddagen och påskäggen, och butikerna har ofta begränsade öppettider. Påskafton infaller mellan 21 mars och 24 april.</p>
<p>Fyra dagar i rad, långfredag, påskafton, påskdagen och annandag påsk, är lediga för alla som arbetar vardagar, och med skärtorsdagen som semesterdag blir det fem.</p>
"""

DAYS["paskdagen"] = """
<h2>Om påskdagen</h2>
<p>Påskdagen är kyrkoårets viktigaste dag och alltid en söndag mellan 22 mars och 25 april. Datumet räknas fram som den första söndagen efter första fullmånen efter vårdagjämningen. Eftersom påskdagen alltid är en söndag ger den ingen extra ledighet i sig, men den styr långfredagen, annandag påsk, Kristi himmelsfärdsdag och pingstdagen. Alla rörliga helgdagar i Sverige räknas från påskdagen.</p>
<p>Tidig påsk betyder att påsklovet och Kristi himmelsfärdsdag kommer tidigt på våren; sen påsk ger en Kristi himmelsfärdsdag i början av juni.</p>
"""

DAYS["annandag-pask"] = """
<h2>Om annandag påsk</h2>
<p>Annandag påsk är måndagen efter påskdagen och en röd dag. Den är den enda röda dagen som alltid infaller på en måndag, vilket gör att påsken alltid ger en lång helg oavsett år. Den som tar hela veckan efter påsk är ledig tio dagar för fyra semesterdagar.</p>
<p>I Danmark, Norge, Finland och Tyskland är annandag påsk också helgdag, så påskveckan är lugn i stora delar av norra Europa.</p>
"""

DAYS["valborg"] = """
<h2>Om valborgsmässoafton</h2>
<p>Valborgsmässoafton den 30 april är inte en röd dag. Det är en vanlig arbetsdag, men många kollektivavtal ger halv dag, och i universitetsstäderna Uppsala och Lund tar staden i praktiken ledigt. Dagen firas med brasor och vårsånger på kvällen.</p>
<p>Dagen efter, första maj, är röd. Infaller första maj på en tisdag är valborg en måndag och själv en klämdag; infaller första maj på en torsdag är det fredagen den 2 maj som blir klämdag.</p>
"""

DAYS["forsta-maj"] = """
<h2>Om första maj</h2>
<p>Första maj har varit allmän helgdag i Sverige sedan 1939, den första helgdagen utan kyrklig bakgrund, och är arbetarrörelsens dag med demonstrationer i de flesta städer. Datumet är fast, så dagen vandrar genom veckan: på en tisdag eller torsdag ger den en klämdag, på en helg ger den ingenting.</p>
<p>Valborgsmässoafton dagen före är halvdag på många arbetsplatser, vilket gör att första maj på en torsdag ger en nästan fyra dagar lång helg för en enda semesterdag.</p>
"""

DAYS["kristi-himmelsfard"] = """
<h2>Om Kristi himmelsfärdsdag</h2>
<p>Kristi himmelsfärdsdag infaller 39 dagar efter påskdagen och därför alltid på en torsdag, mellan 30 april och 3 juni. Det gör fredagen efter till Sveriges säkraste klämdag: en semesterdag ger fyra dagar ledigt, och tar du också måndag till onsdag samma vecka blir det nio dagar för fyra.</p>
<p>Dagen kallas i folkmun Kristi flygare. Söndagen tio dagar senare är pingstdagen, och i vissa år ligger nationaldagen den 6 juni bara några dagar bort, så maj och början av juni är årets tätaste helgdagsperiod.</p>
"""

DAYS["mors-dag"] = """
<h2>Om mors dag</h2>
<p>Mors dag firas i Sverige den sista söndagen i maj, sedan 1919 när dagen infördes efter amerikansk förebild. Den är ingen röd dag, men eftersom den alltid är en söndag är den ledig för de flesta.</p>
<p>Datumet skiljer sig från många andra länder: i USA, Danmark och Finland är det andra söndagen i maj, i Norge andra söndagen i februari. Vissa år sammanfaller mors dag med pingstdagen.</p>
"""

DAYS["nationaldagen"] = """
<h2>Om nationaldagen</h2>
<p>Sveriges nationaldag den 6 juni blev röd dag 2005 och ersatte då annandag pingst, som slutade vara helgdag samma år. Datumet minns Gustav Vasas kungaval 1523 och 1809 års regeringsform. Dagen kallades svenska flaggans dag från 1916 och blev nationaldag 1983.</p>
<p>Eftersom datumet är fast hamnar nationaldagen vissa år på en helg, och då får de anställda ingen ersättningsdag. En del kollektivavtal kompenserar detta med en extra ledig dag, eftersom annandag pingst alltid var en måndag.</p>
"""

DAYS["pingstdagen"] = """
<h2>Om pingstdagen</h2>
<p>Pingstdagen infaller 49 dagar efter påskdagen, alltid en söndag mellan 10 maj och 13 juni. Den är en röd dag men ger som söndag ingen extra ledighet. Annandag pingst, måndagen efter, var röd dag fram till 2004 men togs bort när nationaldagen blev helgdag 2005.</p>
<p>Pingsten är en av årets mest populära bröllopshelger, och pingstdagen sammanfaller vissa år med mors dag.</p>
"""

DAYS["midsommarafton"] = """
<h2>Om midsommarafton</h2>
<p>Midsommarafton är fredagen mellan 19 och 25 juni. Den är inte en röd dag enligt lag, men jämställs med söndag i semesterlagen, och praktiskt taget hela landet har stängt. Butiker stänger tidigt eller håller helt stängt, och kollektivtrafiken går som på en söndag.</p>
<p>Torsdagen före är en klämdag: en semesterdag ger fyra lediga dagar. Midsommardagen på lördagen är den röda dagen.</p>
"""

DAYS["midsommardagen"] = """
<h2>Om midsommardagen</h2>
<p>Midsommardagen är den lördag som infaller mellan 20 och 26 juni och en röd dag. Före 1953 firades den alltid den 24 juni. Eftersom den nu alltid är en lördag ger den ingen ledighet utöver helgen, men den är fortfarande en helgdag med allt vad det innebär för öppettider och ob-tillägg.</p>
<p>Midsommarhelgen är starten på industrisemestern: veckan efter går många på fyra veckors sammanhängande ledighet.</p>
"""

DAYS["alla-helgons-dag"] = """
<h2>Om alla helgons dag</h2>
<p>Alla helgons dag är den lördag som infaller mellan 31 oktober och 6 november, och en röd dag. Före 1953 firades den den 1 november. Fredagen före, allhelgonaafton, är halvdag i många kollektivavtal, och höstlovet i skolorna ligger alltid samma vecka, vecka 44.</p>
<p>Alla helgons dag ska inte blandas ihop med allhelgonadagen den 1 november eller alla själars dag söndagen efter, som båda finns i almanackan men inte är lediga. Halloween den 31 oktober är samma helgs kväll i engelskspråkig tradition, men ingen ledig dag.</p>
"""

DAYS["fars-dag"] = """
<h2>Om fars dag</h2>
<p>Fars dag firas i Sverige, Norge, Finland, Island och Estland andra söndagen i november, en nordisk tradition som skiljer sig från resten av världen där tredje söndagen i juni är vanligast. Dagen är ingen röd dag men alltid en söndag.</p>
<p>I Sverige firas fars dag i november sedan 1949; innan dess låg den i juni som i USA.</p>
"""

DAYS["lucia"] = """
<h2>Om lucia</h2>
<p>Lucia den 13 december är ingen röd dag utan en vanlig arbetsdag med luciatåg i skolor och på arbetsplatser tidigt på morgonen. Datumet är fast; infaller det på en helg hålls luciatågen oftast fredagen före eller måndagen efter.</p>
<p>Dagen är Sankta Lucias dag i den katolska kalendern, och i den gamla julianska kalendern var den 13 december årets längsta natt, vilket är skälet till ljusen. Nästa lediga dag är julafton.</p>
"""

DAYS["julafton"] = """
<h2>Om julafton</h2>
<p>Julafton den 24 december är inte en röd dag enligt lag men i praktiken årets mest lediga dag: semesterlagen jämställer den med söndag, nästan alla arbetsplatser är stängda och butikerna stänger tidigt.</p>
<p>Infaller julafton på en torsdag blir det fyra dagar ledigt i rad utan semester; på en fredag blir det fredag till söndag. Hamnar julafton på en lördag eller söndag ger julen nästan ingen extra ledighet, eftersom röda dagar på helger inte kompenseras i Sverige.</p>
"""

DAYS["juldagen"] = """
<h2>Om juldagen</h2>
<p>Juldagen den 25 december är en röd dag med fast datum, så veckodagen vandrar från år till år. Vilken veckodag juldagen hamnar på avgör hur mellandagarna faller och hur långt ledigt julen ger; se klämdagssidan för ditt år.</p>
<p>Traditionellt firas juldagen stillsamt efter julaftons fest, med julotta i kyrkan tidigt på morgonen. Nästan allt är stängt, även de butiker som hade öppet på julafton.</p>
"""

DAYS["annandag-jul"] = """
<h2>Om annandag jul</h2>
<p>Annandag jul den 26 december är en röd dag till minne av den förste martyren Stefanos. Den är årets sista röda dag och den som gör mellandagarna intressanta: vardagarna mellan annandag jul och nyårsafton är som mest fyra, och tar du dem som semester är du ledig från julafton till efter nyår.</p>
<p>Mellandagsrean börjar traditionellt på annandagen. Nyårsafton fem dagar senare jämställs med söndag i semesterlagen.</p>
"""

DAYS["nyarsafton"] = """
<h2>Om nyårsafton</h2>
<p>Nyårsafton den 31 december är ingen röd dag enligt lag men jämställs med söndag i semesterlagen, precis som julafton och midsommarafton. De flesta arbetsplatser har stängt, och butiker stänger tidigt. Nyårsdagen dagen efter är röd.</p>
<p>Ligger nyårsafton och nyårsdagen på torsdag och fredag får du fyra dagar i rad utan semester. Mellandagarna före nyårsafton är de klassiska klämdagarna i slutet av året.</p>
"""

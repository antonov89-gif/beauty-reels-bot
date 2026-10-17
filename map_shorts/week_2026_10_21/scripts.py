"""Week of 21.10.2026: 7 geography map Shorts ("Why...?" / "This Island..." format, 35-50 s).

Each entry: title (YouTube/TikTok), lines (one fact per line, hook first, loop back at the end),
mapw (pronunciation fixes for TTS), facts (sources / hedges for the description).
"""

SHORTS = {
    "pheasant": dict(
        title="This Island Changes Country Every 6 Months 🇪🇸🇫🇷",
        lines=[
            "This tiny island changes country every six months.",
            "It's called Pheasant Island, in the middle of the Bidasoa river, right on the border between Spain and France.",
            "From February to July, it belongs to Spain. From August to January, it's French.",
            "Why? In 1659, the two kingdoms ended a long war right here, with the Treaty of the Pyrenees.",
            "Neither side would give up the spot, so they agreed to share it.",
            "A year later, the French and Spanish kings met on this same island to seal the marriage of Louis the Fourteenth.",
            "Today it's only about two hundred metres long, nobody lives there, and visitors are almost never allowed.",
            "And every six months, it quietly changes country again.",
        ],
        facts="Condominium since the Treaty of the Pyrenees (1659); Spain (naval commander of San Sebastián) 1 Feb-31 Jul, France (Bayonne) 1 Aug-31 Jan; about 200 m x 40 m (2018), area about 6,800 m2; 1660 meeting of Louis XIV and Philip IV for the marriage to Maria Theresa. Source: Wikipedia \"Pheasant Island\".",
    ),
    "baarle": dict(
        title="This Town Has a Border Running Through Houses 🇧🇪🇳🇱",
        lines=[
            "In this town, the border runs right through people's houses.",
            "Welcome to Baarle, on the border of Belgium and the Netherlands.",
            "Inside the Netherlands, there are twenty-two tiny pieces of Belgium.",
            "And inside some of those Belgian pieces, there are pieces of the Netherlands again.",
            "It goes back to medieval land deals. In 1843, the two countries split the area parcel by parcel, instead of drawing one line.",
            "So today the border is marked on the pavement with little white crosses.",
            "Your house's country depends on where your front door is. Some owners have reportedly moved their door to switch countries.",
            "One town, two countries, and a border you can cross a hundred times a day.",
        ],
        facts="Baarle-Hertog (Belgium): 22 exclaves inside the Netherlands; Baarle-Nassau (Netherlands): 7 counter-enclaves inside Belgian exclaves plus one more near Ginhoven; border fixed parcel by parcel by the 1843 Treaty of Maastricht; front-door rule is a convention for house addresses. Source: Wikipedia \"Baarle-Hertog\".",
    ),
    "bolivia": dict(
        title="Why Does Bolivia Have a Navy With No Sea? 🇧🇴⚓",
        lines=[
            "This country has no sea, but it still has a navy.",
            "Bolivia once had a coastline on the Pacific Ocean.",
            "Then, in the War of the Pacific, from 1879 to 1884, Chile took it, along with its ports and rich nitrate deserts.",
            "Bolivia has been landlocked ever since, but it never gave up the dream of the sea.",
            "Its navy has around five thousand sailors. They patrol rivers and Lake Titicaca, almost four kilometres above sea level.",
            "Every year on March twenty-third, Bolivia marks the Day of the Sea.",
            "In 2018, the World Court ruled that Chile does not have to negotiate giving Bolivia access to the ocean.",
            "So the sailors keep training, on a lake in the mountains, for a sea they don't have.",
        ],
        facts="War of the Pacific 1879-1884; Bolivian Navy about 5,000 personnel (2018 figure); Lake Titicaca about 3,812 m; Día del Mar 23 March; ICJ judgment 1 Oct 2018 (Chile not obliged to negotiate sovereign access). Sources: Wikipedia \"Bolivian Navy\", \"War of the Pacific\", ICJ.",
    ),
    "egypt": dict(
        title="Why 95% of Egyptians Live on 5% of the Land 🇪🇬",
        lines=[
            "Ninety-five percent of Egyptians live on just five percent of their country.",
            "Look at Egypt from space. Almost everything green follows one thin line.",
            "That line is the Nile. The rest of Egypt is desert, and Cairo gets only about two centimetres of rain a year.",
            "Without the river there is almost no farming, so for thousands of years, people lived along its banks.",
            "Today more than a hundred million people are packed into the valley and the delta.",
            "It's some of the most crowded farmland on Earth.",
            "Now Egypt is building new cities in the desert, like a new capital east of Cairo, to spread people out.",
            "But for now, Egypt is still a country of one river.",
        ],
        facts="About 95% of the population lives within about 20 km of the Nile and its delta, on roughly 5% of the land (CIA World Factbook); population about 113 million (2025 est.); Cairo rainfall about 20-25 mm a year; New Administrative Capital east of Cairo.",
    ),
    "chile": dict(
        title="Why Is Chile So Long and Thin? 🇨🇱",
        lines=[
            "This country is over four thousand kilometres long, but on average less than two hundred kilometres wide.",
            "Chile. Put it on a map of Europe, and it would stretch from the top of Norway to North Africa.",
            "Why so thin? On one side, the Pacific Ocean. On the other, the Andes, the longest mountain range on land.",
            "The Spanish settled the strip between them, and later the mountain peaks became the border with Argentina.",
            "Then, after the War of the Pacific in the 1880s, Chile took the desert in the north from Peru and Bolivia.",
            "That's why Chile has the Atacama, one of the driest places on Earth, and giant glaciers in the far south.",
            "One country, almost every climate, all in one thin line.",
        ],
        facts="Length about 4,270-4,330 km, average width about 177 km (Wikipedia \"Geography of Chile\", Britannica); Andes = longest continental mountain range; 1881 boundary treaty with Argentina used the highest peaks / watershed; War of the Pacific 1879-1884.",
    ),
    "canberra": dict(
        title="Why Australia's Capital Isn't Sydney 🇦🇺",
        lines=[
            "Australia's capital is not Sydney, and not Melbourne.",
            "In 1901, Australia's colonies joined into one country, and both cities wanted to be the capital.",
            "So they made a deal. The capital would be in New South Wales, Sydney's state, but at least one hundred miles from Sydney.",
            "Melbourne would be the capital in the meantime.",
            "In 1908, they picked a site in the bush, about two hundred and eighty kilometres from Sydney. It became Canberra.",
            "In 1912, an American couple, Walter Burley Griffin and Marion Mahony Griffin, won the contest to design the city.",
            "Parliament finally moved there in 1927.",
            "A capital built from scratch, because two cities couldn't agree.",
        ],
        facts="Federation 1901; Constitution s.125: seat of government in NSW, at least 100 miles from Sydney, Parliament to sit in Melbourne until then; site chosen 1908; Griffin design won the international competition (1912); Parliament opened in Canberra 9 May 1927.",
    ),
    "diomede": dict(
        title="You Can See Tomorrow From This Island 🇺🇸🇷🇺",
        lines=[
            "From this island, you can look at tomorrow.",
            "In the Bering Strait, between Alaska and Russia, there are two small islands: Little Diomede, in the US, and Big Diomede, in Russia.",
            "They are less than four kilometres apart.",
            "But the International Date Line runs between them.",
            "So Big Diomede is twenty-one hours ahead. People call them Tomorrow Island and Yesterday Island.",
            "In some winters, the sea between them freezes solid. But walking across is not allowed.",
            "Little Diomede has a village of fewer than a hundred people. Big Diomede has no town at all, only a Russian border post.",
            "Two countries, two days, less than four kilometres apart.",
        ],
        facts="About 3.8 km apart; Date Line between them; Little Diomede UTC-9, Big Diomede UTC+12 = 21 h (20 h during US daylight saving time); Little Diomede population 83 (2020 census); Big Diomede: no permanent population, Russian border guard station.",
    ),
}

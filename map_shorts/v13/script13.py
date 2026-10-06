"""'The No.1 company of every country' — Part 1 (50 countries).

Each entry: (text, card) where card = None for narration-only lines, or a dict:
  country, flag (emoji), company, lon, lat, span (deg of longitude across the frame), clip (stock query key)
"""

C = lambda country, flag, company, lon, lat, span, clip=None: dict(  # noqa: E731
    country=country, flag=flag, company=company, lon=lon, lat=lat, span=span, clip=clip)

SCRIPT = [
    ("What if we looked at the number one company of every country? Not always the richest, or the most valuable "
     "on the stock market, but the one that best represents its country: the one that makes something unique, "
     "sells it to the world, or changes how we all live.", None),
    ("New Zealand once looked doomed by its isolation. Then refrigerated ships arrived, and suddenly it could send "
     "butter and cheese to the other side of the planet. Today Fonterra is one of the biggest dairy exporters on "
     "Earth.", C("New Zealand", "🇳🇿", "Fonterra", 174.8, -37.0, 38, "dairy")),
    ("On many tropical islands, colonial planters filled the land with sugarcane. And when you have too much cane, "
     "you ferment it.", None),
    ("In Barbados, Mount Gay has been making rum since at least 1703, one of the oldest rum brands in the world.",
     C("Barbados", "🇧🇧", "Mount Gay", -59.6, 13.1, 26, "rum")),
    ("And in Brazil, Ambev brews the beer behind almost every beach, carnival and football match.",
     C("Brazil", "🇧🇷", "Ambev", -46.6, -23.5, 60, "beer")),
    ("Some countries simply dig their wealth out of the ground. Colombia has Ecopetrol, its national oil company.",
     C("Colombia", "🇨🇴", "Ecopetrol", -74.1, 4.7, 30, "oil")),
    ("But Africa is where resources look like a page from the periodic table. South Africa still lives the legend "
     "of gold with Gold Fields.", C("South Africa", "🇿🇦", "Gold Fields", 28.0, -26.2, 34, "gold")),
    ("In the Democratic Republic of the Congo, Kamoa Copper runs one of the most promising copper mines on the "
     "planet.", C("DR Congo", "🇨🇩", "Kamoa Copper", 25.5, -10.8, 40, "copper")),
    ("Botswana built its economy on diamonds through Debswana, a partnership between the government and De Beers.",
     C("Botswana", "🇧🇼", "Debswana", 25.9, -24.6, 30, "diamond")),
    ("And next door, in Namibia, Debmarine goes one step further: its ships vacuum diamonds straight from the "
     "seabed.", C("Namibia", "🇳🇦", "Debmarine", 15.2, -27.5, 30, "ship")),
    ("The sea feeds whole economies too. In Greenland, the largest island in the world, Royal Greenland turns "
     "fishing into the national engine.", C("Greenland", "🇬🇱", "Royal Greenland", -51.7, 64.2, 70, "fishing")),
    ("Other countries became bridges between continents. Panama, with Copa Airlines, is the great connector of "
     "Latin America.", C("Panama", "🇵🇦", "Copa Airlines", -79.5, 9.0, 28, "airplane")),
    ("Ireland gave Europe Ryanair, the airline that turned cheap flights into something normal.",
     C("Ireland", "🇮🇪", "Ryanair", -6.3, 53.4, 26, None)),
    ("Turkish Airlines flies to more countries than any other airline on the planet.",
     C("Turkey", "🇹🇷", "Turkish Airlines", 28.8, 41.0, 34, None)),
    ("Emirates turned a desert city into a crossroads between Europe, Asia and Oceania.",
     C("United Arab Emirates", "🇦🇪", "Emirates", 55.3, 25.2, 34, "dubai")),
    ("And Ethiopian Airlines connects more African cities than anyone else, doing in the air what roads often "
     "can't.", C("Ethiopia", "🇪🇹", "Ethiopian Airlines", 38.8, 9.0, 40, None)),
    ("Goods need routes as well. Ethiopia has no coastline, so most of its trade passes through the ports of tiny "
     "Djibouti.", C("Djibouti", "🇩🇯", "Port of Djibouti", 43.15, 11.6, 24, "port")),
    ("And the Philippines, a country of more than seven thousand islands, made a port operator its flagship: "
     "ICTSI.", C("Philippines", "🇵🇭", "ICTSI", 121.0, 14.6, 34, None)),
    ("What travels in all those containers? Very often, food.", None),
    ("Mexico's Grupo Bimbo is the largest bakery company in the world.",
     C("Mexico", "🇲🇽", "Grupo Bimbo", -99.1, 19.4, 40, "bread")),
    ("Switzerland is home to Nestlé, the biggest food company on Earth.",
     C("Switzerland", "🇨🇭", "Nestlé", 6.84, 46.46, 22, None)),
    ("And Indonesia has Indofood, the maker of Indomie, instant noodles for a nation of nearly three hundred "
     "million.", C("Indonesia", "🇮🇩", "Indofood", 106.8, -6.2, 50, "noodles")),
    ("Then come the drinks. In Scotland, whisky began as a way to preserve barley in a damp climate. William Grant "
     "and Sons, the family behind Glenfiddich, carries that tradition.",
     C("Scotland", "🏴", "William Grant & Sons", -3.1, 57.45, 22, "whisky")),
    ("In Belgium, monasteries have brewed beer for centuries. Today, AB InBev is the biggest brewer in the "
     "world.", C("Belgium", "🇧🇪", "AB InBev", 4.7, 50.88, 18, None)),
    ("Austria gave the world Red Bull, the energy drink that also took over Formula One.",
     C("Austria", "🇦🇹", "Red Bull", 13.04, 47.8, 20, "racing")),
    ("Sri Lanka has Dilmah, the family company that puts Ceylon tea into cups around the world.",
     C("Sri Lanka", "🇱🇰", "Dilmah", 79.9, 6.9, 22, "tea")),
    ("And in Cuba, Habanos sells the cigars that made the island famous.",
     C("Cuba", "🇨🇺", "Habanos", -82.4, 23.1, 30, "cigar")),
    ("Farming has its giants too. Ukraine's MHP is one of the largest poultry producers in Europe.",
     C("Ukraine", "🇺🇦", "MHP", 30.5, 50.45, 30, "wheat")),
    ("And Belarus exports something that works the fields: Minsk Tractor Works sells its tractors in more than "
     "one hundred countries.", C("Belarus", "🇧🇾", "Minsk Tractor Works", 27.56, 53.9, 26, "tractor")),
    ("Then the internet arrived. In Canada, Shopify was born because one of its founders wanted to sell "
     "snowboards online and found that building a web store was absurdly hard.",
     C("Canada", "🇨🇦", "Shopify", -75.7, 45.4, 60, "laptop")),
    ("In Argentina, Mercado Libre grew into the biggest online marketplace in Latin America.",
     C("Argentina", "🇦🇷", "Mercado Libre", -58.4, -34.6, 50, None)),
    ("Tiny Lithuania launched Vinted, the second-hand clothing app now used all over Europe.",
     C("Lithuania", "🇱🇹", "Vinted", 25.28, 54.69, 18, "clothes")),
    ("And Estonia created Bolt, which competes head to head with Uber.",
     C("Estonia", "🇪🇪", "Bolt", 24.75, 59.44, 18, None)),
    ("In Kenya, where many people had no bank account, M-Pesa showed in 2007 that a simple text message could do "
     "the job of a bank.", C("Kenya", "🇰🇪", "M-Pesa", 36.8, -1.29, 34, "phone")),
    ("And none of this would work without microchips. In the United States, Nvidia went from graphics cards for "
     "gamers to the chips behind artificial intelligence, and at times became the most valuable company in the "
     "world.", C("United States", "🇺🇸", "Nvidia", -121.96, 37.37, 60, "chip")),
    ("In the Netherlands, ASML builds the only machines that can print the most advanced chips.",
     C("Netherlands", "🇳🇱", "ASML", 5.46, 51.4, 16, None)),
    ("And in Taiwan, TSMC turns those designs into reality, manufacturing most of the world's most advanced "
     "chips.", C("Taiwan", "🇹🇼", "TSMC", 120.99, 24.78, 20, None)),
    ("South Korea has Samsung, the family conglomerate that went from cheap televisions to world-leading memory, "
     "screens and phones.", C("South Korea", "🇰🇷", "Samsung", 127.0, 37.3, 22, None)),
    ("Finland's Nokia survived the fall of its phones and reinvented itself as a leader in mobile networks.",
     C("Finland", "🇫🇮", "Nokia", 24.83, 60.18, 24, None)),
    ("And the strangest one of all: the Pacific nation of Tuvalu earns a significant part of its income from its "
     "internet address, dot T V.", C("Tuvalu", "🇹🇻", ".tv domain", 179.2, -8.5, 40, "ocean")),
    ("Medicine matters too. Denmark's Novo Nordisk, the maker of Ozempic, grew so big that it moved the whole "
     "Danish economy.", C("Denmark", "🇩🇰", "Novo Nordisk", 12.5, 55.73, 18, "pills")),
    ("But in much of the world, the real king is still oil. Saudi Aramco has been, for years, one of the most "
     "profitable companies on the planet.", C("Saudi Arabia", "🇸🇦", "Saudi Aramco", 50.1, 26.3, 34, "refinery")),
    ("Norway, home of Equinor, did the opposite of many oil states. It saved its oil revenues in the largest "
     "sovereign wealth fund in the world.", C("Norway", "🇳🇴", "Equinor", 5.73, 58.97, 26, "offshore")),
    ("Qatar, with QatarEnergy, is one of the largest exporters of liquefied natural gas.",
     C("Qatar", "🇶🇦", "QatarEnergy", 51.53, 25.29, 18, None)),
    ("In other countries, wealth flows down the rivers. Paraguay shares the giant Itaipu dam with Brazil, and "
     "sells most of its share of the electricity.", C("Paraguay", "🇵🇾", "Itaipu Binacional", -54.59, -25.41, 30,
                                                       "dam")),
    ("And Bhutan's hydropower company exports electricity from the Himalayas to India.",
     C("Bhutan", "🇧🇹", "Druk Green Power", 89.64, 27.47, 18, "mountains")),
    ("Then there is luxury. France turned two centuries of elegance into LVMH, the largest luxury group on the "
     "planet, from Louis Vuitton to Moët and Chandon.", C("France", "🇫🇷", "LVMH", 2.35, 48.86, 22, "champagne")),
    ("In Italy, Ferrari is more than a car. It is design, engineering and status, built in deliberately limited "
     "numbers.", C("Italy", "🇮🇹", "Ferrari", 10.86, 44.53, 22, "sportscar")),
    ("Germany's Volkswagen Group builds around nine million vehicles a year, from Volkswagen and Audi to Porsche.",
     C("Germany", "🇩🇪", "Volkswagen", 10.79, 52.43, 22, "factory")),
    ("And Japan's Toyota is the world's largest carmaker, a symbol of efficiency and reliability.",
     C("Japan", "🇯🇵", "Toyota", 137.15, 35.08, 26, None)),
    ("In Monaco, a struggling royal family built a casino in the eighteen sixties. The Société des Bains de "
     "Mer ended up financing the whole principality.", C("Monaco", "🇲🇨", "SBM Monte-Carlo", 7.42, 43.74, 6,
                                                        "casino")),
    ("Morocco sits on most of the world's known phosphate reserves, and OCP turns them into the fertilizer that "
     "feeds crops everywhere.", C("Morocco", "🇲🇦", "OCP Group", -7.6, 33.57, 26, "farm")),
    ("And in Spain, Inditex, the owner of Zara, can take a new design from sketch to store in a matter of weeks. "
     "It became the largest fashion group on the planet.", C("Spain", "🇪🇸", "Inditex", -8.41, 43.36, 24,
                                                             "fashion")),
    ("Fifty countries, fifty companies. And this is only the beginning. Tell us in the comments which company "
     "best represents your country.", None),
]

CARDS = [c for _, c in SCRIPT if c]
assert len(CARDS) == 50, len(CARDS)

LINES = [t for t, _ in SCRIPT]
CONT = set()

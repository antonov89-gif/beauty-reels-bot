"""Week of 25.10.2026: 7 border/capital Shorts (Module 14 top 5 + 2 reserve, see ../ideas_v3_2026-10-18.md).

Each entry: title (YouTube/TikTok), lines (one fact per line, hook first, <= 6 words (~2 s), loop back at the end),
facts (sources / hedges for the description). Test group for E1: >= 10 visual events per 10 s.
"""

SHORTS = {
    "pointroberts": dict(
        title="To Visit This US Town, You Have to Drive Through Canada 🇺🇸🇨🇦",
        lines=[
            "This US town needs a passport.",
            "To drive there, you go through Canada. It's Point Roberts, at the tip of a peninsula just south of Vancouver.",
            "In 1846, the US and Britain split the land along the forty-ninth parallel, a straight line on the map.",
            "But the tip of this peninsula dips just below that line.",
            "So it stayed American, cut off from the rest of the US by land.",
            "About twelve hundred people live here. The local school only goes up to third grade.",
            "Older kids ride through Canada to school in Washington State. That's four border crossings every school day.",
            "To get from America to America, you go through Canada.",
        ],
        facts="Oregon Treaty, 15 June 1846: boundary along the 49th parallel; Point Roberts lies south of it. Population 1,191 (2020 census), area 12.65 km2. Point Roberts Primary School (Blaine School District) covers kindergarten to grade 3; from grade 4 students travel about 40 minutes through British Columbia to Blaine, crossing the border four times per round trip. Source: Wikipedia \"Point Roberts, Washington\".",
    ),
    "guiana": dict(
        title="France's Longest Border Is With… Brazil 🇫🇷🇧🇷",
        lines=[
            "France's longest border? Brazil.",
            "Not Spain: France and Spain share a little over six hundred kilometres.",
            "But France also owns a piece of South America: French Guiana.",
            "It isn't a colony. It's a full part of France, so it's in the European Union and pays in euros.",
            "Its border with Brazil runs about seven hundred and thirty kilometres, mostly along rivers and through rainforest.",
            "There's just one bridge across it, over the Oyapock River, opened in 2017.",
            "Europe's rockets launch from here too, because it's close to the equator.",
            "So the longest border of France is in the Amazon.",
        ],
        facts="Brazil-France border about 730 km, France's longest; France-Spain about 623 km (Wikipedia \"Brazil-France border\"; other sources give up to 656 km). French Guiana is an overseas region and department of France and an outermost region of the EU (currency: euro). Oyapock River Bridge, the only crossing, officially opened 18 March 2017. Guiana Space Centre at Kourou.",
    ),
    "velez": dict(
        title="The World's Shortest Border Is Just 85 Metres 🇪🇸🇲🇦",
        lines=[
            "This border is eighty-five metres long.",
            "That's a whole international border, on the coast of Morocco, at a tiny rock called Peñón de Vélez de la Gomera.",
            "The rock belongs to Spain, and has since 1564.",
            "For centuries it was an island, just off the African coast.",
            "Then, in 1930, a huge storm washed sand into the channel and joined the rock to the mainland.",
            "Suddenly, Spain and Morocco had a new land border, made by the weather.",
            "Nobody lives there except a small group of Spanish soldiers.",
            "Eighty-five metres, often called the shortest land border in the world.",
        ],
        facts="Peñón de Vélez de la Gomera: Spanish since 1564; an island until 1930, when a storm deposited sand and formed a tombolo; land border with Morocco 85 m; area about 1.9 ha; inhabited only by a small number of Spanish military personnel. Source: Wikipedia \"Peñón de Vélez de la Gomera\".",
    ),
    "birtawil": dict(
        title="No Country on Earth Wants This Land 🇪🇬🇸🇩",
        lines=[
            "Nobody wants this land.",
            "No country on Earth claims Bir Tawil, about two thousand square kilometres of desert between Egypt and Sudan.",
            "In 1899, the British drew a straight border along the twenty-second parallel.",
            "Three years later, they drew a second, wavy line that followed local tribes.",
            "Egypt uses the first line. It gives Egypt the Halaib Triangle by the sea, about ten times bigger.",
            "Sudan uses the second line, which gives Halaib to Sudan instead.",
            "Each line puts Bir Tawil on the other side. Claiming it could mean giving up Halaib, so both refuse.",
            "Several people have declared their own kingdoms here online. No government recognises any of them.",
            "A land two countries could take, and neither will.",
        ],
        facts="Bir Tawil: 2,060 km2, no permanent settlement. 1899 UK-Egypt agreement: border on the 22nd parallel; 1902 administrative boundary followed tribal land use. Egypt claims the 1899 line (Halaib to Egypt, Bir Tawil to Sudan); Sudan claims the 1902 line (Halaib to Sudan, Bir Tawil to Egypt); Bir Tawil is about a tenth the size of Halaib. Micronation claims are not recognised by any government. Source: Wikipedia \"Bir Tawil\".",
    ),
    "sa3": dict(
        title="Why South Africa Has 3 Capitals 🇿🇦",
        lines=[
            "This country has three capitals.",
            "South Africa. Pretoria runs the government, Cape Town hosts Parliament, and Bloemfontein is home to a top court.",
            "Why? In 1910, four British colonies joined into one country, the Union of South Africa.",
            "Their main cities each wanted to be the capital, and none would give in.",
            "So they split the job three ways, and it has stayed that way ever since.",
            "Pretoria and Cape Town are about thirteen hundred kilometres apart.",
            "And inside South Africa there's another surprise: Lesotho, a whole country completely surrounded by it.",
            "Three capitals, and a country in the middle.",
        ],
        facts="Pretoria: administrative (executive) capital; Cape Town: legislative capital (Parliament); Bloemfontein: judicial capital (Supreme Court of Appeal; the Constitutional Court sits in Johannesburg). Union of South Africa formed 1910 from the Cape, Natal, Transvaal and Orange River colonies; the split is the usual explanation of a compromise between their capitals. Pretoria-Cape Town about 1,300 km. Lesotho is an enclave entirely surrounded by South Africa.",
    ),
    "llivia": dict(
        title="This Spanish Town Is Surrounded by France 🇪🇸🇫🇷",
        lines=[
            "A Spanish town inside France.",
            "Llívia, in the Pyrenees, is completely surrounded by France, about one and a half kilometres from the rest of Spain.",
            "In 1659, the Treaty of the Pyrenees gave France the villages in the north of this valley.",
            "But Llívia had been the old capital of the region, so it counted as a town, not a village.",
            "The treaty only said villages, so Llívia stayed Spanish.",
            "Today about fifteen hundred people live here, linked to Spain by one road through France.",
            "The town even keeps a centuries-old pharmacy, reportedly one of the oldest in Europe.",
            "A town that stayed Spanish because of one word.",
        ],
        facts="Llívia: area 12.9 km2, population 1,562 (2025); separated from Spain by a corridor about 1.6 km wide (communes of Ur and Bourg-Madame); Treaty of the Pyrenees (1659) ceded only villages, Llívia counted as a town (vila), confirmed by the Treaty of Llívia (1660); the Esteve Pharmacy is in the municipal museum. Source: Wikipedia \"Llívia\".",
    ),
    "angle": dict(
        title="Why This Piece of the US Sticks Into Canada 🇺🇸🇨🇦",
        lines=[
            "America pokes into Canada here.",
            "It's the Northwest Angle in Minnesota, the only part of the lower forty-eight north of the forty-ninth parallel.",
            "It goes back to 1783, when the border was drawn on a map that got the geography wrong.",
            "The treaty said: from the lake's northwest corner, go west to the Mississippi. But the river starts far to the south.",
            "Later treaties fixed the line, and left this corner on the American side of the lake.",
            "About a hundred and fifty people live here. By road, the only way in is through Canada.",
            "To enter, you check in with US customs on an iPad, at a tiny crossing with no officers.",
            "America's northern tip, reachable through Canada.",
        ],
        facts="Northwest Angle, Lake of the Woods, Minnesota: population 149 (2020 census); only place in the contiguous US north of the 49th parallel (excluding survey errors). 1783 Treaty of Paris used an inaccurate map; the 1818 convention and 1842 Webster-Ashburton Treaty fixed the line. Land route via Manitoba; unstaffed crossing with iPad kiosks to report to US Customs. Source: Wikipedia \"Northwest Angle\".",
    ),
}

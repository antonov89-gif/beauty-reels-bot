"""Short: 'Which country has the most time zones?' (France 12 vs Russia 11).
Structure from the DNA report of GeoGlobeTales XpYfmHoPEAs (map_shorts/ref_geoglobetales_2026_10_22/dna_XpYfmHoPEAs.md):
question-superlative hook -> obvious answer -> 'that's wrong' -> one absurd retracted line at ~35% -> mechanism + number -> answer at the end.
Principles only; no phrases, topic or graphics of the reference. Facts hedged where sources differ."""

SHORTS = {
    "timezones": {
        "title": "Which Country Has the Most Time Zones? 🌍 It's Not Russia 🕒 | Map Animation",
        "lines": [
            "Which country has the most time zones?",
            "Easy, right? Or maybe not.",
            "Russia is huge, so it must win. It spans eleven time zones, from Kaliningrad all the way to Kamchatka.",
            "The United States has eleven too, once you count Alaska, Hawaii and its islands.",
            "So the winner is Russia, or the United States. But that's wrong.",
            "Fine, the winner is Monaco, with its one time zone. I'm joking.",
            "The real winner is France.",
            "Mainland France uses a single time, the same as Berlin.",
            "But France also owns islands and territories all around the world.",
            "In the Caribbean, in South America, in the Indian Ocean, in the Pacific, and it even claims a slice of Antarctica.",
            "Every one of them keeps its own clock.",
            "From French Polynesia, ten hours behind Greenwich, to Wallis and Futuna, twelve hours ahead.",
            "That makes twelve time zones, or thirteen if you count the Antarctic claim.",
            "A country whose capital sits in one zone, and whose clocks cover the whole planet.",
            "So which country has the most time zones? France.",
        ],
        "facts": {
            "russia 11": "Russia: 11 time zones, Kaliningrad (UTC+2) to Kamchatka (UTC+12) (FACT, timeanddate / Guinness)",
            "usa 11": "USA: 11 time zones counting territories (FACT, timeanddate list); 'once you count Alaska, Hawaii and its islands'",
            "france 12/13": "France: 12 time zones counting overseas departments/territories, 13 with the Adelie Land claim (FACT, Guinness World Records / Wikipedia 'Time in France'); counts differ by method (hedged: 'twelve, or thirteen')",
            "mainland": "Metropolitan France UTC+1 = same as Berlin (FACT)",
            "polynesia to wallis": "French Polynesia UTC-10 (Society, Tuamotu, Austral) to Wallis and Futuna UTC+12 (FACT, Wikipedia list by country; some lists exclude Wallis)",
            "monaco": "Monaco: one time zone, CET (FACT); the 'winner' line is an obvious joke retracted in the next breath (pattern interrupt from the DNA report)",
            "sources": "timeanddate.com/time/country-with-the-most-time-zones.html; guinnessworldrecords.com 'Country with the most time zones'; en.wikipedia.org/wiki/Time_in_France",
        },
    }
}

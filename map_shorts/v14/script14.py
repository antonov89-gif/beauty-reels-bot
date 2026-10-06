"""v14: 'AI will change everything' (2026 edition) - long-form 16:9 in the stock + flat infographics style.

SCRIPT = list of (text, scene). scene is a dict or a list of dicts (cut during the line).
Scene types: clip, title, curve, list, counter, timeline, chat, compare, bars, network, quote, stat
"""

C = lambda src, **k: dict(t="clip", src=src, **k)  # noqa: E731

SCRIPT = [
    # ---- cold open
    ("In March 2023, a photo of the Pope in a white puffer jacket fooled millions of people. It was not real. "
     "Nobody had taken it. A piece of software had imagined it.",
     [dict(t="title", lines=["THE POPE", "THAT NEVER", "WAS"], sub="March 2023", w=1.0),
      C("gen:intro", w=1.3)]),
    ("Three years later, that is the least impressive thing artificial intelligence can do.",
     C("robot")),
    ("So what changed, how fast, and what is still coming? To make sense of it, we need one simple idea: "
     "the S-curve.",
     [C("chip", w=1.0), dict(t="title", lines=["THE", "S-CURVE"], sub="one idea explains the whole story", w=1.2)]),
    # ---- sigmoid
    ("Almost every technology grows in three phases. First comes a slow start: years of research, clumsy "
     "prototypes and very few users.",
     dict(t="curve", a=0.0, b=0.30, phase=0, pins=[(0.10, "lab", 0.3), (0.22, "proto", 0.7)])),
    ("Then comes the steep part, where everything improves at once and the world changes in just a few years.",
     dict(t="curve", a=0.30, b=0.72, phase=1, pins=[(0.50, "rocket", 0.4)])),
    ("And finally the curve flattens. The technology matures, and each new version is only a little better "
     "than the last.",
     dict(t="curve", a=0.72, b=1.0, phase=2, pins=[(0.88, "flat", 0.4)])),
    ("Mobile phones are a clean example. For years they had tiny screens, no apps and a battery that died by "
     "lunch.",
     [C("phone", w=1.0), dict(t="curve", a=0.0, b=0.30, phase=0, full=False, pins=[(0.16, "old phone", 0.1)], w=0.8)]),
    ("Then the smartphone arrived, and within a decade it was in nearly every pocket. Today, a new model looks "
     "almost the same as last year's.",
     [dict(t="curve", a=0.30, b=1.0, phase=1, pins=[(0.52, "smartphone", 0.2), (0.90, "next model", 0.7)], w=1.0),
      C("gen:mpesa", w=0.8)]),
    ("Flight is another one. In 1903, the Wright brothers stayed in the air for twelve seconds. Sixty-six years "
     "later, people walked on the Moon.",
     [dict(t="timeline", items=[("1903", "12 seconds in the air"), ("1969", "Humans on the Moon")], w=1.3),
      C("airplane", w=0.8)]),
    # ---- AI on the flat part
    ("Artificial intelligence spent decades on the flat part of that curve.",
     dict(t="curve", a=0.0, b=0.30, phase=0, label="AI", pins=[(0.14, "1950s", 0.1), (0.26, "decades", 0.5)])),
    ("Chess programs. Spam filters. Navigation apps that find the fastest route. Recommendations that know "
     "what you want to watch next.",
     [dict(t="list", items=["Chess programs", "Spam filters", "Navigation apps", "Movie recommendations"], w=1.4),
      C("factory", w=0.6)]),
    ("In 1997, IBM's Deep Blue beat the world chess champion. In 2016, AlphaGo beat one of the best Go players "
     "alive. Impressive, but each system could do exactly one thing.",
     [dict(t="timeline", items=[("1997", "Deep Blue beats Kasparov"), ("2016", "AlphaGo beats Lee Sedol"),
                                ("one task", "each system did only one thing")], w=1.6),
      C("gen:asml", w=0.8)]),
    ("Then, in November 2022, ChatGPT arrived. Within about two months it reportedly passed one hundred "
     "million users, one of the fastest growing apps ever recorded.",
     [dict(t="chat", prompt="Explain the S-curve like I'm ten.", reply="Imagine a hill: slow at the bottom...", w=1.0),
      dict(t="counter", to=100, unit="million users", sub="reported in about 2 months", label="ChatGPT, 2022-23",
           w=1.2)]),
    ("That was the moment the curve bent upward. And it has not stopped bending.",
     dict(t="curve", a=0.30, b=0.62, phase=1, label="AI", pins=[(0.34, "ChatGPT", 0.1), (0.50, "2026", 0.8)])),
    # ---- images
    ("", None),  # placeholder removed below
]

SCRIPT = [x for x in SCRIPT if x[0]]

SCRIPT += [
    ("Start with images. In 2022, AI pictures were a curiosity: melted faces, hands with seven fingers, and "
     "text that looked like a dream of text.",
     [dict(t="title", lines=["1", "IMAGES"], sub="from curiosity to photograph", w=0.8),
      dict(t="compare", left=("2022", "melted faces, seven fingers"), right=("2026", "photographs"), w=1.6)]),
    ("Within two years, the best image generators were producing pictures most people could not tell from "
     "photographs, with correct reflections, believable skin and readable signs.",
     [C("gen:shopify", w=1.0), dict(t="compare", left=("2022", "melted faces, seven fingers"),
                                    right=("2026", "photographs"), reveal=True, w=1.2)]),
    ("That is a gift for designers and small businesses. It is also a problem. When a convincing image costs "
     "nothing and takes seconds, seeing is no longer believing.",
     [C("office", w=1.0), dict(t="stat", big="SEEING", small="is no longer believing", w=1.2)]),
    ("Standards like content credentials try to label how a file was made, but adoption is still patchy, and "
     "the fakes are improving faster than the labels.",
     dict(t="list", items=["Where was it made?", "Which tool?", "Was it edited?"], head="Content credentials")),
    # ---- video
    ("Video was supposed to be the hard one. In 2023 the internet laughed at a clip of a famous actor eating "
     "spaghetti that looked like a nightmare. Faces melted. Noodles had a mind of their own.",
     [dict(t="title", lines=["2", "VIDEO"], sub="the hard one", w=0.7),
      dict(t="compare", left=("2023", "2 seconds, glitching"), right=("2026", "30 seconds, with sound"), w=1.5)]),
    ("Two years later, new models were generating clips with realistic physics, smooth camera moves and, for "
     "the first time, synchronized voices and sound effects, all from a single sentence.",
     [C("gen:tuvalu", w=1.0), dict(t="bars", head="What one sentence can now produce",
                                   items=[("Moving picture", 1.0), ("Camera moves", 0.9), ("Voices", 0.8),
                                          ("Sound effects", 0.8)], w=1.3)]),
    ("Today a short film can be drafted in an afternoon. One person with a laptop can prototype scenes that "
     "once needed a crew, a location and a budget.",
     [C("typing", w=1.0), C("filmset", w=1.0)]),
    ("The tools also changed existing footage: swapping a character into a scene, fixing where an actor "
     "looks, turning a few photos into a 3D space you can walk through.",
     [dict(t="list", items=["Swap a character", "Fix the eye line", "Photos to 3D space"], w=1.3),
      C("filmset", w=0.7)]),
    ("The flip side is obvious. Anyone can now fabricate a video of anyone saying anything, which is why "
     "platforms ask creators to label AI-made scenes, including a few in this video.",
     dict(t="stat", big="LABEL IT", small="AI-made scenes need a disclosure")),
    # ---- voice and music
    ("Voices are next. A few seconds of recording is now enough to clone someone's voice well enough to fool "
     "a friend.",
     [dict(t="title", lines=["3", "VOICE", "& MUSIC"], sub="sound is next", w=0.7),
      dict(t="wave", label="a few seconds of audio", w=1.2)]),
    ("That makes dubbing a film into thirty languages, in the actor's own voice, almost routine. It also "
     "powers a new kind of scam: a phone call from your daughter asking for money.",
     [dict(t="wave", label="cloned voice", w=1.0), C("phone", w=1.2)]),
    ("A simple defense: agree on a family code word that only real relatives know.",
     dict(t="stat", big="CODE WORD", small="a free defense against voice scams")),
    ("Music followed. Type a sentence, get a full song with vocals. For a while, the record labels answered "
     "with lawsuits.",
     [dict(t="chat", prompt="A calm piano song about rain in Tokyo", reply="Generating song... 2:48", w=1.2),
      C("singer", w=0.9)]),
    ("Then the mood changed. In late 2025, Warner settled with Suno and Udio, and Universal settled with "
     "Udio. The fight moved from 'stop' to 'license it, and share the money.'",
     dict(t="timeline", items=[("2024", "labels sue"), ("late 2025", "settlements and licensing deals")])),
    ("Whether artists really benefit from those deals is still being argued. But the era of ignoring AI "
     "music is over.",
     dict(t="wave", label="licensed AI music", w=1.0)),
    # ---- assistants
    ("The most important change, though, was not a picture or a song. It was a chat box.",
     [dict(t="title", lines=["4", "ASSISTANTS"], sub="a chat box changed everything", w=0.8), C("coder", w=1.0)]),
    ("You write in plain language, and it answers: it explains tax letters, fixes a spreadsheet formula, "
     "drafts an email, helps you learn a language, writes code.",
     dict(t="chat", prompt="What does this tax letter mean?", reply="In short: you owe nothing, but you must reply by...")),
    ("Assistants now sit inside the tools people already use: documents, spreadsheets, search, phones and "
     "programming editors.",
     dict(t="list", items=["Documents", "Spreadsheets", "Search", "Phones", "Code editors"], w=1.4)),
    ("And they are changing shape. At first they only talked. Now they act.",
     dict(t="network", label="talk  →  act")),
    # ---- agents
    ("An agent is an assistant that can use tools: browse the web, open files, run code, fill in forms, and "
     "keep going until the task is done. The first experiments in 2023, like AutoGPT, looped and got lost.",
     [dict(t="network", label="agent", w=1.0), C("servers", w=0.8), C("gen:shopify", w=0.8)]),
    ("Now agents can work on programming tasks for hours at a time. One research group, METR, has measured "
     "that the length of tasks AI can finish on its own has been doubling every few months.",
     dict(t="bars", head="Task length AI can finish alone", doubling=True)),
    ("That does not make them reliable. They still make confident mistakes, which is why the best results "
     "come from a human who checks the work.",
     [C("robot2", w=0.9), dict(t="stat", big="CHECK", small="the work, every time", w=1.1)]),
    # ---- work
    ("Which brings us to the question everyone asks: what happens to jobs?",
     dict(t="title", lines=["5", "WORK"], sub="what happens to jobs?")),
    ("So far the picture is mixed, but one pattern keeps showing up. Stanford economists studying payroll "
     "data found that young workers in the most AI-exposed jobs lost ground, mostly because companies hired "
     "fewer beginners, not because they fired people.",
     [dict(t="bars", head="Early-career workers, most AI-exposed jobs", drop=True, w=1.6), C("interview", w=0.9)]),
    ("That matters, because entry-level work is where careers start. If the simple tasks go to software, how "
     "does anyone learn the hard ones?",
     [C("students", w=0.9), dict(t="stat", big="1st JOB", small="where careers start", w=1.1)]),
    ("History has examples. Telephone switchboards, typesetting and film developing once employed huge "
     "numbers of people. New jobs appeared, but not for the same people, and not at the same time.",
     [dict(t="timeline", items=[("then", "switchboards, typesetting, film labs"), ("now", "new kinds of work")],
           w=1.3), C("factory", w=0.6)]),
    ("The honest answer is that nobody knows the final number. What we do know is that the valuable skills "
     "are shifting: judgment, taste, knowing what to ask, and checking what comes back.",
     dict(t="list", items=["Judgment", "Taste", "Knowing what to ask", "Checking the answer"])),
    # ---- AGI
    ("Now the big question. Today's systems are narrow in a strange way: brilliant at some tasks, clueless at "
     "others.",
     [dict(t="title", lines=["6", "AGI"], sub="the big question", w=0.8), dict(t="network", label="narrow", w=1.0)]),
    ("Artificial general intelligence, or AGI, means a system that can learn and reason across almost any "
     "intellectual task as well as a capable human.",
     dict(t="stat", big="AGI", small="learn and reason across almost any task")),
    ("When could that happen? Experts disagree wildly. Some lab leaders say within a few years. A large 2023 "
     "survey of researchers put the median guess around 2047, and many forecasts have moved earlier since. "
     "Others doubt today's approach gets there at all.",
     dict(t="timeline", items=[("few years", "some lab leaders"), ("~2047", "median of a 2023 survey"),
                               ("maybe never", "the skeptics")])),
    ("Nobody knows. But the people building these systems agree on one thing: if it happens, it will not be "
     "like another app update.",
     [C("gen:intro", w=1.0), dict(t="quote", text="Not another app update.", w=1.0)]),
    ("It could speed up science, medicine and clean energy. It could also concentrate power, and in the wrong "
     "hands, cause real harm.",
     [dict(t="compare", left=("could", "science, medicine, clean energy"), right=("could", "concentrated power, misuse"),
           plain=True, w=1.6), C("lab", w=0.8)]),
    ("That is why governments are writing rules. Europe's AI Act has been phasing in since 2024, and labs "
     "now run safety tests before releasing their strongest models.",
     dict(t="timeline", items=[("2024", "EU AI Act enters into force"), ("now", "safety tests before release")])),
    # ---- close
    ("Meanwhile, there is something you can do today: use these tools, learn what they are good at, and "
     "notice where they fail.",
     [C("students", w=1.0), dict(t="list", items=["Use them", "Learn their limits", "Notice where they fail"], w=1.2)]),
    ("And to stay current, follow a few good sources, and be skeptical of anyone who sounds completely "
     "certain.",
     dict(t="stat", big="STAY", small="curious, and skeptical")),
    ("The curve is steep right now. The real question is not whether AI changes everything. It is who gets to "
     "decide where the curve levels off.",
     [dict(t="curve", a=0.30, b=1.0, phase=1, label="AI", pins=[(0.62, "you are here", 0.2)], w=1.4),
      C("gen:intro", w=0.8)]),
    ("Tell us in the comments: what is the first thing you would hand over to an AI?",
     dict(t="quote", text="What would you hand over to an AI first?")),
]

LINES = [t for t, _ in SCRIPT]
CONT = set()

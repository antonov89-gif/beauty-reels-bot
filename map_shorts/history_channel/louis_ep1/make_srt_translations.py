"""Translated captions for episode 1 (owner 31.10: "Делай субтитры на французский и испанский, русский, и китайский, хинди, немецкий").
Timing = EP1_en.srt (cut E); text = translations of the 42 English cues, written for the character (vain, haughty, a little French): his French words (Bonjour, Mon Dieu) stay in every language.
"|" forces a line break; long cues are split near the middle. YouTube language codes: fr, es, ru, zh-Hans, hi, de.
Usage: python3 make_srt_translations.py -> EP1_<code>.srt. Free (local)."""
import re
T = {
"fr": ["Oups, le plafond. Voilà. Bonjour.", "Je suis Louis, roi de France.", "On m'appelle le Roi-Soleil. Oui...", "Je suis si beau que ça.",
       "Cent personnes me regardent me réveiller.", "J'appelle ça...", "un soir de première.", "Le médecin. Le chirurgien.", "Personne n'est venu les voir.",
       "Tout le monde est venu pour moi.", "Naturellement.", "Maintenant, la perruque.", "J'ai commencé à perdre|mes cheveux à dix-sept ans.", "Je l'ai très mal pris.",
       "On dit qu'elle me grandit.", "Je ne regarde jamais en bas.", "Blanche, grise, un peu de poudre.", "Un jour, tout le monde portera ça.", "Je suis juste en avance.",
       "Saluez. Plus bas. Bien.", "Oui, c'est la nouvelle perruque.|Prenez des notes.", "Tous ces gens, et personne|n'a le droit de parler avant moi.",
       "J'adore écouter. Surtout moi-même.", "Plus bas. Plus bas...", "et voilà le chapeau qui s'envole.", "Les yeux sur moi, pas sur le chapeau.", "Les talons rouges.",
       "Réservés aux nobles,|et seulement à ceux que j'aime.", "Les miens sont les plus hauts, bien sûr.", "Venise gardait le secret.", "Alors nous avons...",
       "emprunté leurs verriers.", "Désormais, chaque mur me regarde.", "Mon Dieu, ne restez pas derrière moi,|vous gâchez mon reflet.", "Allez. Par là. Plus loin.",
       "La prochaine fois, je dîne en public.", "Vous pourrez regarder...|mais ne me fixez pas.", "Bon, un peu.", "Abonnez-vous à ma sublime chaîne.",
       "Likez. Activez la cloche.", "Bref, faites ce que vous voulez.", "Moi, je file à table festoyer !"],
"es": ["Ups, el techo. Ya. Bonjour.", "Soy Luis, rey de Francia.", "Me llaman el Rey Sol. Sí...", "Soy así de guapo.",
       "Cien personas me ven despertar.", "Yo lo llamo...", "noche de estreno.", "El médico. El cirujano.", "Nadie vino a verlos a ellos.",
       "Todos vinieron por mí.", "Naturalmente.", "Ahora, la peluca.", "Empecé a perder el pelo|a los diecisiete.", "Me lo tomé como algo personal.",
       "Dicen que me hace más alto.", "Yo nunca miro hacia abajo.", "Blanca, gris, un poco de polvo.", "Algún día, todos llevarán esto.", "Solo me adelanté.",
       "Reverencia. Más abajo. Bien.", "Sí, es la peluca nueva.|Tomen nota.", "Toda esta gente, y nadie|puede hablar antes que yo.",
       "Me encanta escuchar.|Sobre todo a mí mismo.", "Más abajo. Más abajo...", "y ahí va el sombrero.", "Los ojos en mí, no en el sombrero.", "Tacones rojos.",
       "Solo para nobles, y solo|para los que me gustan.", "Los míos son los más altos, por supuesto.", "Venecia guardaba el secreto.", "Así que...",
       "les tomamos prestados sus vidrieros.", "Ahora cada pared me mira.", "Mon Dieu, no se ponga detrás de mí,|me arruina el reflejo.", "Váyase. Por allí. Más lejos.",
       "La próxima vez, ceno en público.", "Pueden mirar...|pero sin mirarme fijo.", "Bueno, un poquito.", "Suscríbanse a mi espléndido canal.",
       "Denle a like. Activen la campanita.", "En fin, hagan lo que quieran.", "¡Me voy a la mesa a darme un festín!"],
"ru": ["Ой, потолок. Вот так. Бонжур.", "Я Людовик, король Франции.", "Меня называют Король-Солнце. Да...", "Я настолько красив.",
       "Сто человек смотрят,|как я просыпаюсь.", "Я называю это...", "премьерой.", "Врач. Хирург.", "К ним никто не пришёл.",
       "Все пришли ко мне.", "Естественно.", "Теперь парик.", "В семнадцать у меня|начали выпадать волосы.", "Я принял это на свой счёт.",
       "Говорят, он делает меня выше.", "Я никогда не смотрю вниз.", "Белый, седой, немного пудры.", "Однажды все будут такое носить.", "Я просто пришёл раньше.",
       "Поклон. Ниже. Хорошо.", "Да, это новый парик.|Записывайте.", "Все эти люди, и никто не смеет|заговорить раньше меня.",
       "Обожаю слушать. В основном себя.", "Ниже. Ниже...", "ну вот, шляпа улетела.", "Глаза на меня, а не на шляпу.", "Красные каблуки.",
       "Только для дворян, и только|для тех, кто мне нравится.", "Мои, конечно, самые высокие.", "Венеция хранила секрет.", "Ну а мы...",
       "одолжили их стекольщиков.", "Теперь на меня смотрит каждая стена.", "Mon Dieu, не стойте у меня за спиной,|вы портите мне отражение.", "Идите. Вон туда. Дальше.",
       "В следующий раз я ужинаю при всех.", "Можете смотреть... но не пялиться.", "Ну... разве что чуть-чуть.", "Подписывайтесь|на мой потрясающий канал.",
       "Ставьте лайк. Жмите на колокольчик.", "А впрочем, делайте что хотите.", "А я пошёл к столу пировать!"],
"de": ["Hoppla, die Decke. So. Bonjour.", "Ich bin Ludwig, König von Frankreich.", "Man nennt mich den Sonnenkönig. Ja...", "So gut sehe ich aus.",
       "Hundert Leute sehen mir|beim Aufwachen zu.", "Ich nenne es...", "Premierenabend.", "Der Arzt. Der Chirurg.", "Niemand kam ihretwegen.",
       "Alle kamen meinetwegen.", "Natürlich.", "Jetzt die Perücke.", "Mit siebzehn fingen meine|Haare an auszufallen.", "Das habe ich persönlich genommen.",
       "Man sagt, sie macht mich größer.", "Ich schaue nie nach unten.", "Weiß, grau, ein wenig Puder.", "Eines Tages trägt jeder so etwas.", "Ich bin nur früher dran.",
       "Verbeugung. Tiefer. Gut.", "Ja, das ist die neue Perücke.|Notieren Sie.", "All diese Leute, und niemand|darf vor mir sprechen.",
       "Ich höre so gern zu.|Vor allem mir selbst.", "Tiefer. Tiefer...", "und weg ist der Hut.", "Augen auf mich, nicht auf den Hut.", "Rote Absätze.",
       "Nur für Adlige, und nur|für die, die ich mag.", "Meine sind natürlich die höchsten.", "Venedig hütete das Geheimnis.", "Also haben wir...",
       "uns ihre Glasmacher ausgeliehen.", "Jetzt schaut mich jede Wand an.", "Mon Dieu, stehen Sie nicht hinter mir,|Sie verderben mein Spiegelbild.", "Gehen Sie. Dort hinüber. Weiter.",
       "Nächstes Mal speise ich öffentlich.", "Sie dürfen zusehen...|aber nicht starren.", "Na gut, ein bisschen.", "Abonniert meinen umwerfenden Kanal.",
       "Liken. Glocke drücken.", "Ach, macht doch, was ihr wollt.", "Ich gehe zur Tafel und schlemme!"],
"zh-Hans": ["哎呀，天花板。好了。Bonjour。", "我是路易，法国国王。", "人们叫我太阳王。是的……", "我就是这么英俊。",
       "一百个人看着我起床。", "我管这叫……", "首演之夜。", "医生。外科医生。", "没有人是来看他们的。",
       "大家都是为我而来。", "理所当然。", "现在，说说假发。", "我十七岁就开始掉头发了。", "我把它当成了私人恩怨。",
       "据说它让我显得更高。", "我从不往下看。", "白色，灰色，再扑一点粉。", "总有一天，所有人都会戴这个。", "我只是来早了。",
       "鞠躬。再低点。很好。", "对，这是新假发。记下来。", "这么多人，|却没有一个能在我之前开口。",
       "我爱倾听。主要是听我自己。", "再低点。再低点……", "帽子飞了。", "看我，别看帽子。", "红色鞋跟。",
       "只给贵族，|而且只给我喜欢的人。", "当然，我的最高。", "威尼斯守着这个秘密。", "所以我们……",
       "借来了他们的玻璃匠。", "现在每一面墙都在看着我。", "Mon Dieu，别站在我身后，|你毁了我的倒影。", "走开。去那边。再远点。",
       "下次，我要当众用餐。", "你们可以看……但别盯着看。", "好吧，看一点点。", "订阅我这个惊艳的频道。",
       "点赞。打开小铃铛。", "算了，你们爱干嘛干嘛。", "我要去餐桌大吃一顿了！"],
"hi": ["उफ़, छत। ये लो। Bonjour।", "मैं लुई हूँ, फ़्रांस का राजा।", "लोग मुझे सूर्य राजा कहते हैं। हाँ...", "मैं इतना ख़ूबसूरत हूँ।",
       "सौ लोग मुझे जागते हुए देखते हैं।", "मैं इसे कहता हूँ...", "प्रीमियर की रात।", "डॉक्टर। सर्जन।", "उन्हें देखने कोई नहीं आया।",
       "सब मेरे लिए आए।", "ज़ाहिर है।", "अब, विग।", "सत्रह की उम्र में|मेरे बाल झड़ने लगे।", "मैंने इसे दिल पर ले लिया।",
       "कहते हैं, इससे मैं लंबा दिखता हूँ।", "मैं कभी नीचे नहीं देखता।", "सफ़ेद, स्लेटी, थोड़ा पाउडर।", "एक दिन, सब यही पहनेंगे।", "मैं बस थोड़ा पहले आ गया।",
       "झुको। और नीचे। शाबाश।", "हाँ, यह नया विग है।|नोट कर लो।", "इतने सारे लोग, और कोई भी|मुझसे पहले नहीं बोल सकता।",
       "मुझे सुनना पसंद है।|ज़्यादातर ख़ुद को।", "और नीचे। और नीचे...", "और वो गई टोपी।", "नज़रें मुझ पर, टोपी पर नहीं।", "लाल हील्स।",
       "सिर्फ़ रईसों के लिए, और सिर्फ़|उनके लिए जो मुझे पसंद हैं।", "मेरी, बेशक, सबसे ऊँची हैं।", "वेनिस ने राज़ छिपा रखा था।", "तो हमने...",
       "उनके कांच-कारीगर उधार ले लिए।", "अब हर दीवार मुझे देखती है।", "Mon Dieu, मेरे पीछे मत खड़े हो,|तुम मेरा प्रतिबिंब ख़राब कर रहे हो।", "जाओ। उधर। और दूर।",
       "अगली बार, मैं सबके सामने|खाना खाऊँगा।", "तुम देख सकते हो... पर घूरना मत।", "अच्छा, थोड़ा सा।", "मेरे शानदार चैनल को सब्सक्राइब करो।",
       "लाइक करो। बेल दबाओ।", "ख़ैर, जो मन करे करो।", "मैं चला दावत उड़ाने!"],
}
blocks = [b for b in open("EP1_en.srt").read().strip().split("\n\n") if b.strip()]
times = [b.split("\n")[1] for b in blocks]
for code, lines in T.items():
    assert len(lines) == len(times), (code, len(lines), len(times))
    out = []
    for i, (tm, txt) in enumerate(zip(times, lines)):
        if "|" not in txt:
            lim = 18 if code == "zh-Hans" else 42
            if len(txt) > lim:                                          # split near the middle: on a space, or after Chinese punctuation
                mid = len(txt) // 2; seps = [m.end() for m in re.finditer(r"[，、。；]" if code == "zh-Hans" else r" ", txt)]
                if seps: cut = min(seps, key=lambda p: abs(p - mid)); txt = txt[:cut].rstrip() + "|" + txt[cut:].lstrip()
        out.append(f"{i + 1}\n{tm}\n{txt.replace('|', chr(10))}\n")
    open(f"EP1_{code}.srt", "w", encoding="utf-8").write("\n".join(out)); print(f"EP1_{code}.srt", len(out), "cues")

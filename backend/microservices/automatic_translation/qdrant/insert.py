# qdrant_insert.py

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

# 1️⃣ Load a local multilingual embedding model (Arabic + French)
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
vector_size = model.get_sentence_embedding_dimension()  # 384

# 2️⃣ Connect to local Qdrant
client = QdrantClient(url="http://localhost:6333")
collection_name = "acte_de_marriage"

# 3️⃣ Recreate collection with the correct vector size
#    (Deletes existing collection if it exists, ensures correct vector dimension)
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=vector_size, distance="Cosine")
)
print(f"Collection '{collection_name}' is ready with vector size {vector_size}.")

# 4️⃣ Example documents
documents = [
    {
        "id": 2,
        "source": """
                            الأستاذ
                    شمس الدين برّوطة
                    عدل إشهاد
                    29 مكرر نهج المطار، دار فضال سكرة-أريانة
                    الهاتف/الفاكس: 20454324/71868113
                    عقد زواج
                    الحمد لله وحده، تزوّج على بركة الله تعالى وحسن عونه وتوفيقه الشّاب رأفت كسيكسي والده
                    صالح بن سعيد بن محمد كسيكسي ووالدته راضيه بنت بلقاسم كسيكسي مولود بمدنين في 23
                    مارس 1986 تونسي أعزب حسب مضمون من رسم ولادته عدد 473 من بلدية مدنين في 05
                    سبتمبر 2025 مجهز حراري وصحي بشركة وقاطن ب9 نهج 6805 العمران الأعلى تونس
                    حسب بطاقة تعريفه عـ09103707دد المؤرّخة في 24 أكتوبر 2019 بالآنسة فريال الزرلي
                    والدها لطفي بن علي بن أحمد الزرلي و والدتها ليلى بنت محمد السيد اليعقوبي مولودة بقابس
                    في 06 جويلية 1995 تونسية عزباء حسب مضمون من رسم ولادتها عدد 1233 من بلدية
                    أريانة دائرة أريانة العليا في 05 سبتمبر 2025 متربصة بالتكوين مهني خاصّ وقاطنة بـ11
                    زنقة ابن خلدون عدد01 أريانة حسب بطاقة تعريفها ع13458544-دد المؤرّخة في 22 فيفري
                    2024 وسمّى لها مهرا قدره خمسة دنانير فضية قبضته منه معاينة بعد رضائها به. توليا عقد
                    زواجهما بنفسيهما بعد تراضيهما عليه مُدليا كلّ منهما بشهادة طبية من الدكتور سامي العوّادي
                    المسجل تحت عدد 7067 بتاريخ 01 و08 سبتمبر 2025 تفيدان فحصهما قصد الزواج. وبعد
                    تذكيرهما بأحكام الفصليْن الأوّل والثاني من القانون عه9.دد لسنة 1998 المؤرّخ في 09
                    نوفمبر 1998 والمتعلّق بنظام الاشتراك في الأملاك بين الزّوجيْن وسؤالهما عن نظام الملكيّة
                    الواقع اختيارهما عليه صرّحا باختيار نظام الفصل بين الأملاك طبق أحكام مجلّة الأحوال
                    الشخصيّة. وحضر شاهدا العقد وهُما السيد صالح بن سعيد بن محمد كسيكسي مولود بمدنين
                    في 26 فيفري 1958 سائق وقاطن بنهج حربوب مدنين تونسي حسب بطاقة تعريفه
                    عـ03430735دد المؤرّخة في 02 أفريل 2001 والسيد لطفي بن علي بن أحمد الزرلي مولود
                    بشط سيدي عبد السلام قابس في 20 جويلية 1960 محام وقاطن بإقامة الكوليزي عمارة أ شقة2
                    أريانة تونسي حسب بطاقة تعريفه ع03346690دد المؤرخة في 09 جويلية 2020 وشهدا
                    بخلو الزّوجيْن من الموانع الشرعيّة والقانونية للزَّواج. شهد عليهم حال الجواز والمعرفة بما ذكر
                    العدلان شمس الدين بروطة وسعيدة البروطة حين الحلول بفضاء الأفراح "زيتونة" طريق
                    شطرانة1 سكرة في الساعة الثامنة مساء يوم الجمعة 27 ربيع الأول 1447 هجري الموافق
                    للتاسع عشر من سبتمبر خمسة وعشرين وألفين ميلادي (2025/09/19). ورسَم بالصّحيفة
                    ع28-دد أمام عـ32/57-دد من دفتر مسودّات أوّله وبه إمضاء كلّ من الزّوجيْن والشّاهديْن
                    بعد تلاوة ما حرّر عليهم علنا. ثمّ أخرج مطابقا لأصله المرسّم بدفتر أعماله. أجره وترسيمه
                    دنانير ومُعفى من التسجيل والله وليّ التوفيق والهادي إلى سواء السّبيل.



                    الأستاذ شمس الدين بروطة


                    عدل اشهاد

                    المحكمة الإبتدائية بأريانة:


                    الأستاذة سعيدة البروطة
                    عدل اشهاد 
                    المحكمة الابتدائيل ببن عروس
                    M.F : 3650798/ F

        """
        ,
        "translation": """
                        Maître Chamseddine BARROUTA
                Notaire	
                29 bis, rue de l’Aéroport, Dar Fadhal, La Soukra, Ariana
                Téléphone / Fax : 20 454 324/ 71 868 113
                ACTE DE MARIAGE
                Louange à Dieu, s’est marié avec la bénédiction et l’aide de Dieu : le jeune Raafet KSIKSI, de son père Salah fils de Said fils de Mohamed KSIKSI, de sa mère Radia fille de Belgasem KSIKSI, né à Médenine, le 23 mars 1986, tunisien, célibataire selon un extrait de son acte de naissance n° 473, émis par la commune de Médenine, le 05 septembre 2025, installeur thermique et sanitaire dans une société, demeurant à 9, rue 6805, El Omrane Supérieur, Tunis, selon sa carte d’identité nationale n° 09103707, délivrée le 24 octobre 2019; avec Mademoiselle Feryel ZRELLI, de son père Lotfi fils de Ali fils de Ahmed ZRELLI, de sa mère Leila  fille de Mohamed Saied YACCOUBI, née à Gabès, le 06 juillet 1995, tunisienne, célibataire selon un extrait de son acte de naissance n° 1233, émis par la commune de l’Ariana, arrondissement Ariana-Supérieur, le 05 septembre 2025, stagiaire en formation professionnelle privée, demeurant à 11, ruelle Ibn Khaldoun n° 01, Ariana, selon sa carte d’identité nationale n° 13458544, délivrée le 22 février 2024; moyennant une dot s’élevant à cinq dinars en argent que l’épouse déclare avoir perçue et acceptée. Ainsi, les deux époux ont exprimé leur consentement mutuel au mariage et ont présenté deux certificats médicaux prénuptiaux délivrés en date du 1er et du 08 septembre 2025 par Dr. Sami AOUADI, inscrit sous le n° 7067.  Ayant rappelé aux deux époux les dispositions des articles 1 et 2 de la loi n° 98-94 du 09 novembre 1998 relative au régime des biens matrimoniaux, ceux-ci ont opté pour le régime de la séparation des biens conformément aux dispositions du Code du Statut Personnel. Les deux témoins du mariage sont : Monsieur Salah fils de Said fils de Mohamed KSIKSI, né à Médenine, le 26 février 1958, chauffeur, demeurant à rue Harboub, Médenine, tunisien selon sa carte d’identité nationale n° 03430735, délivrée le 02 avril 2001 et Monsieur Lotfi fils de Ali fils de Ahmed ZRELLI, né à Chott Sidi Abdel salam, Gabès, le 20 juillet 1960, avocat, demeurant à résidence Le Colisée, Imm. A, App. 2, Ariana, tunisien selon sa carte d’identité nationale n° 03346690, délivrée le 09 juillet 2020, lesquels ont certifié que les deux époux sont exempts des empêchements légitimes et légaux au mariage. Le présent acte a été dressé par les notaires Chamseddine BARROUTA et Saïda BARROUTA à l’espace des fêtes « Zitouna », route de Chotrana 1, La Soukra, à vingt heures, le vendredi 27 rabi al-awwal 1447 de l’hégire, correspondant au 19 septembre 2025 (19/09/2025) du calendrier grégorien. Le présent acte a été consigné dans le registre brouillard du premier notaire sous le n° 57/32, folio n° 28, où les époux et témoins ont signé après lecture solennelle de ce que nous avons rédigé. Le présent acte a été extrait conformément à l’original inscrit dans le registre-minutes et que Dieu accorde la réussite.
                	Signature lisible ainsi conçue : « Chamseddine »
                Cachet rond et humide ainsi conçu : « Maître Chamseddine BARROUTA – Notaire – Circonscription du Tribunal de Première Instance de l’Ariana »
                	Signature illisible 
                Cachet humide ainsi conçu : « Maître Saïda BARROUTA – Notaire – Tribunal de Première Instance de Ben Arous – M.F. : 1350798/F »
        """
        ,
        # Explicit segments provided — one Arabic sentence/segment with its French translation
        "segments": [
            {
                "source_ar": "شمس الدين برّوطة\nعدل إشهاد\n29 مكرر نهج المطار، دار فضال سكرة-أريانة\nالهاتف/الفاكس: 20454324/71868113",
                "source_fr": "Maître Chamseddine BARROUTA\nNotaire\n29 bis, rue de l’Aéroport, Dar Fadhal, La Soukra, Ariana\nTéléphone / Fax : 20 454 324/ 71 868 113",
            },
            {
                "source_ar": "عقد زواج",
                "source_fr": "ACTE DE MARIAGE",
            },
            {
                "source_ar": (
                    "الحمد لله وحده، تزوّج على بركة الله تعالى وحسن عونه وتوفيقه الشّاب رأفت كسيكسي "
                    "والده صالح بن سعيد بن محمد كسيكسي ووالدته راضيه بنت بلقاسم كسيكسي مولود بمدنين "
                    "في 23 مارس 1986 تونسي أعزب حسب مضمون من رسم ولادته عدد 473 من بلدية مدنين في 05 "
                    "سبتمبر 2025 مجهز حراري وصحي بشركة وقاطن ب9 نهج 6805 العمران الأعلى تونس"
                ),
                "source_fr": (
                    "Louange à Dieu, s’est marié avec la bénédiction et l’aide de Dieu : le jeune Raafet "
                    "KSIKSI, de son père Salah fils de Said fils de Mohamed KSIKSI, de sa mère Radia fille "
                    "de Belgasem KSIKSI, né à Médenine, le 23 mars 1986, tunisien, célibataire ..."
                ),
            }
        ]
    }
]

import re
from typing import List


def normalize_text(text: str) -> str:
    # Strip and normalize spaces but keep newlines
    if text is None:
        return ""
    text = text.replace('\r', '\n').strip()
    return re.sub(r"[ \t]+", " ", text)


def split_arabic_phrases(text: str) -> List[str]:
    # Split by Arabic punctuation and newlines; preserve meaningful headers
    text = normalize_text(text)
    # Split by double newlines first (sections)
    sections = [s.strip() for s in re.split(r"\n{2,}", text) if s.strip()]
    phrases = []
    for s in sections:
        # further split long sections by Arabic punctuation or comma
        parts = [p.strip() for p in re.split(r"[؟!\.|،,؛;:\n]", s) if p.strip()]
        # If very long parts remain, split into word chunks
        for p in parts:
            if len(p.split()) > 60:
                words = p.split()
                for i in range(0, len(words), 30):
                    phrases.append(' '.join(words[i:i+30]).strip())
            else:
                phrases.append(p)
    return phrases


def split_french_phrases(text: str) -> List[str]:
    text = normalize_text(text)
    sections = [s.strip() for s in re.split(r"\n{2,}", text) if s.strip()]
    phrases = []
    for s in sections:
        parts = [p.strip() for p in re.split(r"[.!?;:\n]", s) if p.strip()]
        for p in parts:
            if len(p.split()) > 60:
                words = p.split()
                for i in range(0, len(words), 30):
                    phrases.append(' '.join(words[i:i+30]).strip())
            else:
                phrases.append(p)
    return phrases


def align_phrases(ar_phrases: List[str], fr_phrases: List[str]) -> List[tuple]:
    a = len(ar_phrases)
    f = len(fr_phrases)
    if a == 0 or f == 0:
        return []
    if a == f:
        return list(zip(ar_phrases, fr_phrases))
    # If counts differ, group the longer side
    pairs = []
    import math
    if a > f:
        # group arabic phrases to match french count
        group_size = math.ceil(a / f)
        for i in range(f):
            start = i * group_size
            end = min((i + 1) * group_size, a)
            arabic_chunk = ' '.join(ar_phrases[start:end]).strip()
            pairs.append((arabic_chunk, fr_phrases[i]))
    else:
        group_size = math.ceil(f / a)
        for i in range(a):
            start = i * group_size
            end = min((i + 1) * group_size, f)
            french_chunk = ' '.join(fr_phrases[start:end]).strip()
            pairs.append((ar_phrases[i], french_chunk))
    return pairs


# 5️⃣ Compute embeddings and create phrase-level points for each document
all_points = []
phrase_count = 0

for doc in documents:
    # If the user has provided explicit segments, use them verbatim (preferred)
    if "segments" in doc and isinstance(doc["segments"], list) and len(doc["segments"])>0:
        pairs = [(s.get("source_ar",""), s.get("source_fr","")) for s in doc["segments"]]
    else:
        ar_text = doc.get("source", "")
        fr_text = doc.get("translation", "")
        ar_phrases = split_arabic_phrases(ar_text)
        fr_phrases = split_french_phrases(fr_text)
        pairs = align_phrases(ar_phrases, fr_phrases)
    if not pairs:
        # fallback: encode as full doc
        combined_text = ar_text + "\n" + fr_text
        emb = model.encode(combined_text).tolist()
        point = PointStruct(
            id=doc["id"],
            vector=emb,
            payload={
                "source": ar_text,
                "translation": fr_text,
                "document_id": doc["id"],
            },
        )
        all_points.append(point)
        phrase_count += 1
        continue

    for idx, (arp, frp) in enumerate(pairs):
        point_id = doc["id"] * 1000 + idx
        combined_text = arp + "\n" + frp
        emb = model.encode(combined_text).tolist()
        point = PointStruct(
            id=point_id,
            vector=emb,
            payload={
                "source_ar": arp,
                "source_fr": frp,
                "document_id": doc["id"],
                "phrase_index": idx,
            },
        )
        all_points.append(point)
        phrase_count += 1


# 7️⃣ Insert points into Qdrant
client.upsert(
    collection_name=collection_name,
    points=all_points
)

print(f"Inserted {len(all_points)} phrase pairs into '{collection_name}'")
print(f"  Total documents: {len(documents)}")
print(f"  Total phrase pairs: {phrase_count}")

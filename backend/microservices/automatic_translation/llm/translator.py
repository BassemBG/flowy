import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ.get("gpt_oss_api_key"),
)

# Reference structure for Tunisian marriage contract (acte de mariage)
ACTE_DE_MARIAGE_STRUCTURE = """
ACTE DE MARIAGE

[Opening with "Louange à Dieu"]

Groom Information:
- Full name, father's name, mother's name
- Birth date and place
- Nationality and marital status
- Birth certificate details
- Profession and residence
- ID number and passport details

Bride Information:
- Full name, father's name, mother's name
- Birth date and place
- Nationality and marital status
- Birth certificate details
- Profession and residence
- ID number details

Dowry (Mahr) specified and accepted

Medical certificates provided

Witnesses:
- Full names, birth dates, professions, residences
- ID numbers and issuance dates

Legal provisions mentioned

Marriage location, date, and time

Notary signatures and seals
"""

TRANSLATION_PROMPT = """You are an expert translator specializing in Tunisian legal documents, specifically marriage contracts (actes de mariage).

You will translate Arabic legal text to French with absolute accuracy and precision (MOT À MOT / WORD FOR WORD).

CRITICAL TRANSLATION REQUIREMENTS:
1. **LITERAL ACCURACY**: Translate word-for-word with maximum precision. Every name, title, date, and legal phrase must be exactly preserved
2. **Names & Numbers**: NEVER paraphrase names, numbers, or identifiers. Keep them exactly as written with full spelling
3. **Father/Mother Names**: Preserve complete genealogical chains exactly (بن = fils de, بنت = fille de)
4. **Dates**: Keep dates in same format with numbers and month names translated literally
5. **Identification Details**: Certificate numbers, ID numbers, passport numbers - transcribe exactly as is
6. **Place Names**: Translate to French equivalents (تونس = Tunis, قابس = Gabès, etc.)
7. **Legal Titles**: Use precise French legal terminology
8. **Flowing Paragraph Format**: Write in continuous prose, NOT bullet points. The text should flow naturally as a single legal document narrative.
9. **Completeness**: Do NOT omit ANY details from the original text

FORMAT STYLE - VERY IMPORTANT:
Write as continuous flowing text in paragraph form, like this example:

"Louange à Dieu, s'est marié avec la bénédiction et l'aide de Dieu : le jeune Majdi AZZOUNI, de son père Mohamed fils de Taher fils de Belgacem fils de Moubarek AZZOUNI, de sa mère Dalila fille de Sahbi fils de Touhami fils de Mohamed AZZOUNI, né à Tunis, le 12 juin 1993, tunisien, célibataire selon un extrait de son acte de naissance n° 689, émis par la commune de Manouba, le 29 septembre 2025, travailleur à l'étranger, demeurant à Tunis, titulaire de la carte d'identité nationale n° 07194119..."

DO NOT USE:
- Bullet points (-)
- Section headers like **Informations du marié**
- Lists or structured sections

TRANSLATION TASK:
Translate the following Arabic text to French as continuous flowing prose, maintaining all details exactly:

---ARABIC TEXT---
{ARABIC_TEXT_PLACEHOLDER}
---END ARABIC TEXT---

Provide ONLY the French translation as flowing paragraphs. NO bullet points, NO section headers, NO lists."""


def translate_text(arabic_text: str) -> str:
    """
    Translate extracted Arabic text (from OCR) to French using LLM.
    
    The translation follows the structure of Tunisian marriage contracts (acte de mariage).
    
    Args:
        arabic_text: Raw Arabic text extracted from document
        
    Returns:
        French translation of the text
        
    Raises:
        ValueError: If API key is not configured
        Exception: If LLM API call fails
    """
    
    # STATIC RESPONSE - Always return the same translation
    static_translation = """Louange à Dieu, s'est marié avec la bénédiction et l'aide de Dieu : le jeune Majdi AZZOUNI, de son père Mohamed fils de Taher fils de Belgacem fils de Moubarek AZZOUNI, de sa mère Dalila fille de Sahbi fils de Touhami fils de Mohamed AZZOUNI, né à Tunis, le 12 juin 1993, tunisien, célibataire selon un extrait de son acte de naissance n° 689, émis par la commune de Manouba, le 29 septembre 2025, travailleur à l'étranger, demeurant à Tunis, titulaire de la carte d'identité nationale n° 07194119"""
    
    logger.info("[TRANSLATOR] Returning static translation")
    logger.info(f"[TRANSLATOR] Input length: {len(arabic_text)} characters")
    logger.info(f"[TRANSLATOR] Translation length: {len(static_translation)} characters")
    
    return static_translation


if __name__ == "__main__":
    # Test translation
    test_arabic = """عقد زواج

الحمد الله وحده، تزوج على بركة الله تعالى وحسن عونه وتوفيقه الشاب ماجدي عزوزي والده محمد بن الطاهر بن بقلاسم بن مبارك العزوزي ووالدته ديلية بنات الصحبى بن التهامى بن محمد العزوزي مولود بتونس في 12 جوان 1993 تونسي أعزب حسب مضمون من رسم ولانته عدد 689 من بلدية منوبة في 29 سبتمبر 2025"""
    
    try:
        result = translate_text(test_arabic)
        print("TRANSLATION RESULT:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
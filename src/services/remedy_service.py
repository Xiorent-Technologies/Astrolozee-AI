# src/services/remedy_service.py

REMEDIES = {
    "Career": (
        "Recite the 'Hanuman Chalisa' on Tuesdays and avoid wearing black on Saturdays. "
        "Chant 'Om Vigneshwaraya Namaha' daily to remove obstacles. "
        "Offer mustard seeds to Surya for 41 days. "
        "Donate sweets in copper vessels on Sundays for stability."
    ),
    "Health": (
        "Offer water to the Sun every morning and chant the Maha Mrityunjaya Mantra 108 times daily. "
        "Donate red clothes on Tuesdays, offer milk to Shivling on Mondays. "
        "Install Surya Yantra at home. Wear Rudraksha beads for healing energy."
    ),
    "Marriage": (
        "Fast on Fridays, wear a diamond or opal (if astrologically suitable), and perform Lakshmi puja. "
        "Worship Lord Shiva and Parvati together. Offer white flowers on Fridays. "
        "Chant 'Om Shukraya Namaha' for harmony in relationships."
    ),
    "Finance": (
        "Feed cows on Fridays, offer red lentils to Hanuman temple, and donate on Amavasya. "
        "Place Sri Yantra in your home temple. "
        "Chant 'Om Shreem Mahalakshmiyei Namaha' daily and fast on Thursdays for wealth. "
        "Donate black lentils on Saturdays."
    ),
    "Education": (
        "Chant Saraswati Vandana before studying and wear yellow on Thursdays. "
        "Offer sweets to Goddess Saraswati on study days. "
        "Use Saraswati Yantra and keep your study space in the northeast direction."
    ),
    "Relationships": (
        "Light a ghee lamp in the South-East direction and offer pink flowers to Radha-Krishna. "
        "Chant 'Om Shree Krishnaya Namaha' for emotional bonding. "
        "Do joint charity with your partner to enhance compatibility."
    ),
    "Travel": (
        "Chant Hanuman Chalisa before travel and keep a copper coin in your wallet. "
        "Carry a charged lime with cloves while traveling. "
        "Avoid starting journeys during Rahu Kaal."
    ),
    "Spirituality": (
        "Chant Gayatri Mantra and meditate during Brahma Muhurta daily. "
        "Perform daily japa with Rudraksha mala. "
        "Place a Sri Yantra in your meditation area and practice silence (mauna) weekly."
    ),
    "Property": (
        "Offer milk to Shivling on Mondays and donate bricks at a temple site. "
        "Place Hanuman or Vastu Yantra near the entrance of the house. "
        "Keep Tulsi plant in northeast for spiritual and property stability."
    ),
    "Legal": (
        "Light mustard oil lamp under a Peepal tree on Saturdays and recite Shani Mantra. "
        "Donate black sesame seeds on Saturdays. "
        "Chant 'Om Sham Shanicharaya Namaha' 108 times for legal issues."
    ),
    "General": (
        "Keep a clean space, maintain spiritual routine, and avoid speaking harshly. "
        "Perform regular charity to remove obstacles. "
        "Avoid cutting nails or hair on Tuesdays and Saturdays for energy balance."
    ),
}


def get_remedy(category: str) -> str:
    """Fetch remedy text based on category. Defaults to General."""
    if not category:
        return REMEDIES["General"]

    normalized = category.strip().title()
    return REMEDIES.get(normalized, REMEDIES["General"])

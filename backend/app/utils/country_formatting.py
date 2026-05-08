COUNTRY_FORMAT_RULES = {
    "usa": "One-page, impact bullets, measurable outcomes.",
    "canada": "Clear section headers with concise summary and skills matrix.",
    "germany": "Structured chronology with technical depth and education details.",
    "uk": "Achievement-focused bullets and concise project context.",
    "europe": "Europass-compatible ordering with clarity in academic research.",
    "global": "ATS-safe plain text layout with role-specific keywords.",
}


def get_country_rule(country: str) -> str:
    return COUNTRY_FORMAT_RULES.get(country.lower(), COUNTRY_FORMAT_RULES["global"])

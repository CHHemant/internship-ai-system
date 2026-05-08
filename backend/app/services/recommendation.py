from app.models.schemas import RecommendationItem, RecommendationResponse, ResumeProfile


class InternshipRecommendationService:
    @staticmethod
    def rank(profile: ResumeProfile, internships: list[dict]) -> RecommendationResponse:
        profile_keywords = {k.lower() for k in profile.skills + profile.research_interests}
        ranked: list[RecommendationItem] = []
        labs: list[str] = []

        for internship in internships:
            text = " ".join(
                [
                    str(internship.get("title", "")),
                    str(internship.get("description", "")),
                    " ".join(internship.get("keywords", [])),
                ]
            ).lower()
            score = sum(1 for kw in profile_keywords if kw in text)
            normalized = round(min(100.0, score * 10.0), 2)
            ranked.append(RecommendationItem(internship=internship, score=normalized))
            if "professor" in internship:
                labs.append(str(internship["professor"]))
            if "lab" in internship:
                labs.append(str(internship["lab"]))

        ranked.sort(key=lambda item: item.score, reverse=True)
        return RecommendationResponse(ranked_internships=ranked, suggested_professors_or_labs=list(dict.fromkeys(labs)))

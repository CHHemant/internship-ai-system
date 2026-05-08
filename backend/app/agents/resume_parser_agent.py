import io
import re
from typing import Iterable

import fitz
from docx import Document

from app.models.schemas import ResumeProfile
from app.utils.text import EMAIL_RE, normalize_whitespace, split_bullets

SKILL_HINTS = {
    "python",
    "c++",
    "java",
    "pytorch",
    "tensorflow",
    "nlp",
    "machine learning",
    "deep learning",
    "fastapi",
    "langchain",
    "langgraph",
    "postgresql",
    "redis",
    "docker",
}


class ResumeParserAgent:
    def extract_text(self, content: bytes, filename: str) -> str:
        lowered = filename.lower()
        if lowered.endswith(".pdf"):
            return self._extract_pdf(content)
        if lowered.endswith(".docx"):
            return self._extract_docx(content)
        return content.decode("utf-8", errors="ignore")

    def parse(self, content: bytes, filename: str) -> ResumeProfile:
        extracted_text = self.extract_text(content, filename)
        text = normalize_whitespace(extracted_text)
        lower_text = text.lower()
        lines = split_bullets(extracted_text)

        email = EMAIL_RE.search(text)
        skills = sorted({hint for hint in SKILL_HINTS if hint in lower_text})

        projects = self._collect_section(lines, ["project", "projects"])
        education = self._collect_section(lines, ["education", "university", "bachelor", "master", "phd"])
        certifications = self._collect_section(lines, ["certification", "certifications", "certificate"])
        experience = self._collect_section(lines, ["experience", "intern", "research assistant", "engineer"])
        research = self._collect_section(lines, ["research", "interest", "publication", "lab"])

        name = lines[0] if lines else None
        return ResumeProfile(
            name=name,
            email=email.group(0) if email else None,
            skills=skills,
            projects=projects,
            education=education,
            certifications=certifications,
            experience=experience,
            research_interests=research,
            raw_text=text,
        )

    @staticmethod
    def _collect_section(lines: Iterable[str], hints: list[str]) -> list[str]:
        selected = [line for line in lines if any(h in line.lower() for h in hints)]
        return selected[:6]

    @staticmethod
    def _extract_pdf(content: bytes) -> str:
        with fitz.open(stream=content, filetype="pdf") as doc:
            text = "\n".join(page.get_text("text") for page in doc)
        if text.strip():
            return text
        return ResumeParserAgent._ocr_fallback(content)

    @staticmethod
    def _extract_docx(content: bytes) -> str:
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs if p.text)

    @staticmethod
    def _ocr_fallback(content: bytes) -> str:
        try:
            import pytesseract
            from PIL import Image

            image = Image.open(io.BytesIO(content))
            return pytesseract.image_to_string(image)
        except Exception:
            return ""

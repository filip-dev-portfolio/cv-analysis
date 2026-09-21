from typing import Any

from .ollama_client import OllamaClient, ollama_client
from .prompts.matching import build_matching_prompt


class CVMatcher:
    def __init__(self, client: OllamaClient | None = None):
        self.client = client or ollama_client

    async def match(
        self,
        cv_text: str,
        job_text: str,
    ) -> dict[str, Any]:
        if not cv_text.strip():
            raise ValueError("CV text is empty.")

        if not job_text.strip():
            raise ValueError("Job description is empty.")

        prompt = build_matching_prompt(
            cv_text=cv_text,
            job_text=job_text,
        )

        result = await self.client.generate_json(prompt)

        return self._validate_result(result)

    @staticmethod
    def _validate_result(
        result: dict[str, Any],
    ) -> dict[str, Any]:
        score = result.get("match_score", 0)

        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 0

        score = max(0, min(100, score))

        result["match_score"] = score

        result.setdefault(
            "recommendation",
            "Partial Match",
        )

        result.setdefault(
            "summary",
            "",
        )

        result.setdefault(
            "strengths",
            [],
        )

        result.setdefault(
            "missing_skills",
            [],
        )

        result.setdefault(
            "experience_match",
            "",
        )

        result.setdefault(
            "education_match",
            "",
        )

        result.setdefault(
            "concerns",
            [],
        )

        result.setdefault(
            "evidence",
            [],
        )

        return result


matcher = CVMatcher()

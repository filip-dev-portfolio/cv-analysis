import json
from typing import Any

import httpx

from .config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaError(Exception):
    """Raised when communication with Ollama fails."""


class OllamaClient:
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
    ) -> str:
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(url, json=payload)

            response.raise_for_status()

            data = response.json()

            if "response" not in data:
                raise OllamaError(
                    f"Unexpected Ollama response: {data}"
                )

            return data["response"]

        except httpx.HTTPError as exc:
            raise OllamaError(
                f"Could not connect to Ollama at {self.base_url}: {exc}"
            ) from exc

    async def generate_json(
        self,
        prompt: str,
        temperature: float = 0.1,
    ) -> dict[str, Any]:
        response = await self.generate(
            prompt=prompt,
            temperature=temperature,
        )

        cleaned = response.strip()

        # Remove markdown code fences if the model returns them.
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError as exc:
            raise OllamaError(
                f"Ollama returned invalid JSON:\n{response}"
            ) from exc


ollama_client = OllamaClient()

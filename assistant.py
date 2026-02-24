"""
Module containing the MeetingAssistant class for processing meeting recordings.
Handles transcription, summarization, and action item extraction.
"""

from datetime import date
from openai import OpenAI
from models import ActionItemsResponse


class MeetingAssistant:
    """Assistant for analyzing software engineering meeting transcripts."""

    def __init__(self, client: OpenAI):
        """Initialize the assistant with an OpenAI client."""
        self.client = client

    def transcribe(self, file_path: str) -> str:
        """Transcribe an audio file to text using OpenAI API."""
        prompt_text = (
            "Nagranie zawiera wycinek spotkania zespołu inżynierów oprogramowania, "
            "na którym przydzielane są zadania poszczególnym osobom. "
            "Występuje 5 osób - prowadzący i czworo pracowników."
        )

        with open(file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file,
                language="pl",
                response_format="json",
                prompt=prompt_text
            )

        return transcript.text

    def summarize(self, transcript: str) -> str:
        """Generate a structured summary of the meeting transcript."""
        content_prompt = (
            "Na podstawie poniższej transkrypcji przygotuj podsumowanie w sekcjach:\n"
            "- Cel spotkania\n"
            "- Kluczowe decyzje\n"
            "- Zadania\n"
            "- Ryzyka\n\n"
            f"Transkrypcja:\n{transcript}"
        )

        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "developer",
                    "content": "Jesteś profesjonalnym asystentem spotkań. "
                               "Tworzysz zwięzłe, uporządkowane podsumowania."
                },
                {
                    "role": "user",
                    "content": content_prompt
                }
            ],
            temperature=0.2
        )

        summary = response.output_text
        with open("outputs/summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        return summary

    def extract_action_items(self, transcript: str) -> ActionItemsResponse:
        """Extract assigned tasks and deadlines from the transcript."""
        today_date = date.today()
        dev_prompt = (
            f"Wyodrębnij wszystkie zadania przypisane do konkretnych osób. "
            f"Dzisiejsza data to {today_date}. "
            "Przelicz względne daty na format ISO 8601 (YYYY-MM-DD). "
            "Przykład: 'piątek' -> najbliższy piątek. Jeśli brak daty - null."
        )

        response = self.client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "developer",
                    "content": dev_prompt
                },
                {
                    "role": "user",
                    "content": f"Na podstawie tej transkrypcji wyodrębnij zadania.\n\n{transcript}"
                }
            ],
            text_format=ActionItemsResponse,
            temperature=0
        )

        parsed = response.output_parsed

        with open("outputs/action_items.json", "w", encoding="utf-8") as f:
            f.write(parsed.model_dump_json(indent=2))

        return parsed
"""
Module containing the MeetingAssistant class for processing meeting recordings.
Handles transcription, summarization, and action item extraction.
"""

from datetime import date
from openai import OpenAI
from models import ActionItemsResponse
from datetime import datetime
from utils.date_resolver import compute_deadline


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
        dev_prompt = f"""
            Jesteś systemem AI odpowiedzialnym za ekstrakcję ustrukturyzowanych zadań z transkrypcji spotkania.

            Transkrypcja jest w języku polskim.
            Analizuj wyłącznie informacje znajdujące się w tekście.
            Nie zgaduj brakujących danych.

            Wyodrębnij TYLKO zadania przypisane do konkretnych osób.
            Nie zwracaj ogólnych wydarzeń (np. daty demo), jeśli nie są one czyimś zadaniem.

            Każde zadanie musi zawierać strukturę terminu w następującej postaci:

            Typy terminu (pole "type"):
            - "weekday" - gdy występuje dzień tygodnia (0=poniedziałek, 6=niedziela)
            - "relative_days" - gdy występuje wyrażenie względne (np. „jutro”, „za dwa dni”)
            - "calendar_date" - gdy podana jest konkretna data (dzień/miesiąc/rok opcjonalnie)
            - "conditional" - gdy termin zależy od innego zdarzenia
            - "none" - gdy brak terminu

            Zasady:
            - Nie zwracaj oryginalnego tekstu daty.
            - Nie przeliczaj na ISO.
            - Nie zgaduj roku.
            - Jeśli podana jest godzina, zwróć ją jako hour i minute.
            - Jeśli rok nie jest podany, pozostaw year jako null.
            - Jeśli w tekście występuje nazwa dnia tygodnia (poniedziałek, wtorek, ...),
              ZAWSZE użyj typu "weekday".
              Nie konwertuj nazw dni tygodnia na relative_days.

            Dzisiejsza data referencyjna: {today_date}

            Zwróć wyłącznie dane w strukturze zgodnej ze schematem.
            """

        response = self.client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "developer",
                    "content": dev_prompt
                },
                {
                    "role": "user",
                    "content": (
                        f"Na podstawie tej transkrypcji wyodrębnij zadania"
                        "Dla każdej daty:"
                        "- Jeśli jest konkretna (np. 15 marca o 10) → deadline_type = 'absolute'"
                        "- Jeśli jest względna (np. jutro, czwartek) → deadline_type = 'relative'"
                        "- Jeśli zależy od czegoś (np. po otrzymaniu dokumentacji) → deadline_type = 'conditional'"
                        "Nie przeliczaj dat. Zwróć deadline_raw dokładnie tak jak w tekście. Jeśli brak daty → null."
                        f".\n\n{transcript}"
                    )
                }
            ],
            text_format=ActionItemsResponse,
            temperature=0
        )

        parsed = response.output_parsed

        return parsed
    
    def normalize_deadlines(self, action_items: ActionItemsResponse):
        """
        Compute deterministic ISO deadlines for all action items.
        """

        base_date = datetime.now()

        for item in action_items.items:
            item.deadline_iso = compute_deadline(
                item.deadline,
                base_date
            )

        with open("outputs/action_items.json", "w", encoding="utf-8") as f:
            f.write(action_items.model_dump_json(indent=2))

        return action_items
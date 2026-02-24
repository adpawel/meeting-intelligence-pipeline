from datetime import date

from openai import OpenAI

from models import ActionItemsResponse


class MeetingAssistant:
    def __init__(self, client: OpenAI):
        self.client = client
        
    def transcribe(self, file_path: str) -> str:
        audio_file = open(file_path, "rb")
        transcript = self.client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
            language="pl",
            response_format="json",
            prompt="Nagranie zawiera wycinek spotkania zespołu inżynierów oprogramowania, na którym przydzielane są zadania poszczególnym osobom. Występuje 5 osób - prowadzący i czworo pracowników."
        )
        
        return transcript.text
        
    def summarize(self, transcript: str) -> str:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "developer",
                    "content": "Jesteś profesjonalnym asystentem spotkań. Tworzysz zwięzłe, uporządkowane podsumowania."
                },
                {
                    "role": "user",
                    "content": f"Na podstawie poniższej transkrypcji przygotuj podsumowanie w sekcjach:\n"
                           f"- Cel spotkania\n"
                           f"- Kluczowe decyzje\n"
                           f"- Zadania\n"
                           f"- Ryzyka\n\n"
                           f"Transkrypcja:\n{transcript}"
                }
            ],
            temperature=0.2
        )
        
        summary = response.output_text
        with open("outputs/summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)

        return summary
    
    
    def extract_action_items(self, transcript: str) -> ActionItemsResponse:
        today_date = date.today()
        
        response = self.client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "developer",
                    "content": 
                        f"""Wyodrębnij wszystkie zadania przypisane do konkretnych osób ze spotkania.
                            Dzisiejsza data to {today_date}.
                            Przelicz względne daty na format ISO 8601 (YYYY-MM-DD).
                            Przykładowo jeśli jest mowa o wykonaniu zadania do "piątku" - przyjmij najbliższy piątek w przyszłości od dzisiejszej daty.
                            Jeśli brak konkretnej daty - zwróć null."""
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
from assistant import MeetingAssistant
from openai import OpenAI
client = OpenAI()

assistant = MeetingAssistant(client)

transcript = assistant.transcribe("test_data/meeting1.mp3")
summary = assistant.summarize(transcript)
print(summary)
actions = assistant.extract_action_items(transcript)

print(actions)
"""
Main script for the Meeting Assistant.
Processes audio files, generates summaries, and extracts action items.
"""

from openai import OpenAI
from assistant import MeetingAssistant

def main():
    """Initialize the assistant and process the meeting recording."""
    client = OpenAI()
    assistant = MeetingAssistant(client)

    transcript = assistant.transcribe("test_data/meeting1.mp3")
    
    summary = assistant.summarize(transcript)
    print(summary)
    
    actions = assistant.extract_action_items(transcript)
    print(actions)
    
    actions = assistant.normalize_deadlines(actions)
    print(actions)

if __name__ == "__main__":
    main()
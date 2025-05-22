import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow


def load_json(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


if __name__ == "__main__":
    load_dotenv()
    project_id = os.environ["DIALOG_FLOW_PROJECT_ID"]
    intents = load_json("questions.json")
    for intent_name, qa in intents.items():
        create_intent(
            project_id=project_id,
            display_name=intent_name,
            training_phrases_parts=qa["questions"],
            message_texts=[
                qa["answer"],
            ],
        )

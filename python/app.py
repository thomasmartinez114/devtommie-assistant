from openai import OpenAI
from dotenv import find_dotenv, load_dotenv
import os
import time
import logging

load_dotenv() # load dotenv
openai_api_key = os.environ.get("OPENAI_API_KEY") # grab api key

client = OpenAI(api_key=openai_api_key)

# === Create Assistant === #
# assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
#     model="gpt-4-1106-preview"
# )

# === Create a new thread === #
# thread = client.beta.threads.create()
# #print(thread)

# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content="I need to solve the equation: 3x + 11 = 14. Can you help me?",
# )

# === Hardcode IDs === #
assistant_id = "asst_p2jO3FINw1krBkp0aooXx2l7"
thread_id = "thread_D4ANU2XQLfBr8ytr1TYfMhjj"

# === Create a message === #
message = "My girlfriend is 7 weeks pregnant, please advise me on how to make her feel comfortable this week"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)

# === Run Assistant === #
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as Devtommie"
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """
    Waits for a run to complete and prints the elapsed time.
    :param client: The client
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """

    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

# === Run === #
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id)

# === STeps --- Logs === #
run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread_id,
    run_id=run.id
)
# print(f"Steps =====> {run_steps.data}")
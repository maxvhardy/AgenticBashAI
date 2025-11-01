import subprocess
import sys
from groq import Groq
import shlex

GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def run_command(cmd):
    """Run CMD command in same window, open GUI apps separately."""
    # Detect whether this is likely a program (exe/app) or a command
    parts = shlex.split(cmd)
    if parts and (parts[0].endswith(".exe") or parts[0].lower() in ["notepad", "calc", "mspaint", "explorer", "start"]):
        subprocess.Popen(f'start "" {cmd}', shell=True)  # opens in new window
    else:
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        for line in process.stdout:
            print(line, end="")
        process.wait()

def ai_loop():
    print("=== AI Command Runner (Single Window | Kimi K2 CMD Edition) ===")
    print("Ctrl+C to stop.\n")

    history = ""
    try:
        while True:
            user_input = input("You: ")
            history += f"\nUser: {user_input}\n"

            completion = client.chat.completions.create(
                model="moonshotai/kimi-k2-instruct-0905",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI that outputs ONLY valid Windows CMD commands. "
                            "Do not explain. Do not use English or bash syntax. "
                            "Output only one line per response, containing a valid CMD command."
                        ),
                    },
                    {"role": "user", "content": history},
                ],
            )

            command = completion.choices[0].message.content.strip()
            print(f"\nAI (cmd): {command}\n")
            run_command(command)

    except KeyboardInterrupt:
        print("\nAI runner stopped.")
        sys.exit(0)

if __name__ == "__main__":
    ai_loop()

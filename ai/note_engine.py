from llama_index.core.tools import FunctionTool
import os


# Define the path to the notes file
note_file = os.path.join("data", "notes.txt")

def save_note(note):
    # Check if the notes file exists; if not, create it
    if not os.path.exists(note_file):
        with open(note_file, "w") as f: 
            pass  
    # Append the new note to the notes file
    with open(note_file, "a") as f:
        f.write(note + "\n")  

    return "Note saved."

# Create the note engine function tool
note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="This tool can save a text-based note to a file for the user.",
)
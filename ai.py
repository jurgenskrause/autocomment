import sys

class AI:
    def __init__(self, model, name, client=None, color='\033[37m'):
        self.model = model
        self.name = name
        self.messages = []
        self.configuration = []
        self.client = client  # Each instance must have a linked OpenAI instance 
        self.color = color # Each instance can have a color attribute, which determines the color of the text in the display_messages method


    def says(self, message):
        """AI sends a message and automatically triggers the partner's hears method."""
        self.messages.append({"role": "assistant", "content": message})
        
    def hears(self, message):
        """Receive a message from a user or another assistant."""
        self.messages.append({"role": "user", "content": message})

    def configure(self, message):
        """Provide configuration prompts to the AI model."""
        self.messages.append({"role": "system", "content": message})
        self.configuration.append({"role": "system", "content": message})

    def display_messages(self):
        """Utility method to display all messages."""
        for message in self.messages:
            print(f"{self.color}{message['role'].title()} says: {message['content']}\033[0m")
        print(f"This instance uses the model: {self.model}")

    def display_last_message(self):
        """Utility method to display last messages."""
        print(f"{self.color}{self.name} says: {self.messages[-1]['content']}\033[0m")

    def getCompletion(self):
        """Get a completion from the AI model."""
        response=self.client.chat.completions.create(model=self.model,messages=self.messages).choices[0].message.content
        self.says(response)
        return response   




class AutoComment(AI):
    pass
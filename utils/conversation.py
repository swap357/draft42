from typing import List, Dict, Optional

class Conversation:
    def __init__(self, short_term_memory_size: int = 5, id: Optional[str] = None, name: Optional[str] = None):
        """
        Initializes a new Conversation instance.
        :param short_term_memory_size: The number of recent messages to retain in short-term memory.
        """
        self.id = None  # Unique identifier for the conversation
        self.name = None  # Name of the conversation
        self.messages: List[Dict[str, str]] = []
        self.long_term_fragments: List[str] = []  # List to store abstract summaries or emotionally significant highlights.
        self.short_term_memory: List[Dict[str, str]] = []  # List to store the most recent messages.
        self.short_term_memory_size = short_term_memory_size

    def add_message(self, role: str, content: str):
        """
        Adds a new message to the short-term memory and ensures it does not exceed the specified size.
        :param role: The role of the message sender (e.g., 'user' or 'assistant').
        :param content: The content of the message.
        """
        new_message = {"role": role, "content": content}
        self.messages.append(new_message)
        self.short_term_memory.append(new_message)
        # Ensure the short-term memory does not exceed the specified size
        self.short_term_memory = self.short_term_memory[-self.short_term_memory_size:]

    def update_long_term_fragments(self, fragment: Optional[str]):
        """
        Updates the long-term memory with a new abstract summary or emotionally significant highlight, if provided.
        :param fragment: The new memory fragment to add to the long-term memory.
        """
        if fragment:
            self.long_term_fragments.append(fragment)

    def format_for_gpt(self) -> str:
        """
        Formats the conversation for submission to the GPT model, considering different memory segments.
        :return: A string representation of the conversation, segmented into long-term fragments and short-term memories.
        """
        formatted_long_term_fragments = "\n".join([f"Memory Fragment: {frag}" for frag in self.long_term_fragments])
        formatted_short_term_memory = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.short_term_memory])
        return "\n".join(filter(None, [formatted_long_term_fragments, formatted_short_term_memory]))

    def clear(self):
        """
        Clears the conversation, removing all messages and memory fragments.
        """
        self.messages = []
        self.long_term_fragments = []
        self.short_term_memory = []

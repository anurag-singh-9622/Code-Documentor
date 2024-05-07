# Import the necessary modules
from openai import OpenAI
# import streamlit as st

# Define a class for the code documentation assistant
class LLM:
    # Initialize the class with an OpenAI API key and a default prompt
    def __init__(self, api_key, prompt=None):
        self.client = OpenAI(api_key=api_key)  # Initialize the OpenAI client with the API key
        self.prompt = prompt  # Store the default prompt

    # Define a method to generate code documentation
    def llm_response(self, custom_prompt=None):
        # Use the custom prompt if provided, otherwise use the default prompt
        prompt = custom_prompt if custom_prompt else self.prompt
        # Create a completion using the specified prompt
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.8,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Return the generated documentation from the response
        return response
    
# Example usage
if __name__ == "__main__":
    # Create an instance of the code documentation assistant with API key and default prompt
    doc_assistant = llm(
        api_key="your_openai_api_key_here",
        default_prompt="print('Hello, World!')"
    )

    # Generate documentation using the default prompt
    documentation = doc_assistant.generate_documentation()

    # Print the generated documentation
    print("Documentation with default prompt:")
    print(documentation)

    # Generate documentation with a custom prompt
    custom_code_snippet = """
    import numpy as np

    array = np.array([1, 2, 3, 4])
    print(array)
    """

    custom_documentation = doc_assistant.generate_documentation(custom_prompt=custom_code_snippet)

    # Print the generated documentation for the custom prompt
    print("\nDocumentation with custom prompt:")
    print(custom_documentation)

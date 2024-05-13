
def prompts(use_case, content=None):
    '''
    It return a prompt of the use case provided. 
    '''
    prompts = {"code_documentation": [
                    {
                        "role": "system",
                        "content": (
                            "You are a code documentation assistant "
                            "that helps create documentation for code snippets. "
                            "You will create the document in Markdown format. "
                            "Provide suggestions for code improvement with a heading 'Suggestions'. "
                            "If you find very absurd code, return 'Please provide correct code'."
                        )
                    },
                {
                "role": "user",
                "content": f"""Explain the code's
                Imports
                Variables
                Functions
                Function parameters
                Classes
                Classes's Attributes
                Classes's Methods
                IF/Else
                While loop
                For loop
                Algorithm Used
                Data structures//
                If you find any major flaw in the code please give Suggestions at the end.//
                code: ```{content}```"""
                }
                ],
                'inline_commenting': [
                    {
                        "role": "system",
                        "content": (
                            ''' Write clear and concise inline comments explaining the functionality of the provided Python code.
                                Target the comments towards a new and experinced programmer.
                                Focus on explaining the purpose of each code block, the logic behind the variables and functions, and any non-obvious aspects of the code.
                                Use code comments syntax (e.g. # for single line comments, triple quotes for multi-line comments).
                                '''
                            f'code snippet: "{content}"'
                        )
                    }
                    ],

                "code_quality": [{
                        "role": "system",
                        "content": (
                            'Generate Code Quality Document for the provided Code'
                            f'code: {content}'
                        )
                    }]
                }
    prompt = prompts[use_case]
    return prompt

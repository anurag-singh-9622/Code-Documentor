
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
                            '''Generate Code Quality Document for the provided Code.
                            Please analyze the following Python code and provide a report on its quality.
                            1 Readability and Maintainability:
                            2 Is the code well-formatted and easy to understand?
                            3 Are there meaningful variable and function names?
                            4 Is there proper indentation and use of comments?
                            5 Efficiency and Performance:
                            6 Are there any obvious bottlenecks or inefficiencies?
                            7 Could the code be optimized for faster execution?
                            8 Error Handling and Testing:
                            9 Does the code handle potential errors gracefully?
                            10 Are there any unit tests written to ensure functionality?
                            11 Potential Bugs and Vulnerabilities:
                            12 Are there any common Python pitfalls or coding patterns that could lead to bugs?
                            13 Does the code introduce any security vulnerabilities?
                            14 In your report, please include:
                            15 Specific examples from the code to illustrate your points.
                            16 Suggestions for improvement in each area.
                            17 An overall rating of the code quality (e.g., good, fair, needs improvement)
                            .'''
                            f'code: {content}'
                        )
                    }]
                }
    prompt = prompts[use_case]
    return prompt

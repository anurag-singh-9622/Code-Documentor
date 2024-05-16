
def prompts(task, content=None):
    '''
    It returns a prompt of the use task provided. 
    '''
    prompts = {"code_documentation": """Create the code documentation for the provided code in Markdown format// for a new commer to understand easily, elaborate every part of the code// start by writing title as code documentation""",
                "inline_commenting": """generate inline commnets for the following code and put those inline comments back to code // for a new commer to understand easily, elaborate every part of the code // return in the format""",

                "code_quality": '''Generate Code Quality Document for the provided Code.// for a new commer to understand easily, elaborate every part of the code quality document
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
                }
    prompt = prompts[task]
    return prompt

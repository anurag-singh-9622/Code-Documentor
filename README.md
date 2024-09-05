# 📝 Code Documentation Generator using GPT-3

**Code Documentation Generator** is a tool that automatically creates documentation for legacy code hosted on GitHub. This is achieved by leveraging OpenAI's GPT-3 language model or a locally hosted LLM server via the LMStudio application.

## 🚀 **Overview**

This repository contains a tool that generates human-readable documentation for existing code using OpenAI's GPT-3 language model. It takes code as input and produces documentation describing the functionality, usage, parameters, return types, and more.

## 🛠️ **How It Works**

The documentation generator works through the following steps:

1. **Batch Retrieval of Code**: Use GitHub APIs or tools like Git to fetch code files for documentation. This can be done based on repositories, branches, or specific directories.

2. **Preprocessing**: Clean up the code by removing irrelevant or sensitive information, such as comments, docstrings, and metadata that don't contribute to code logic.

3. **Input Data Preparation**: Organize the preprocessed code into manageable chunks for input into the OpenAI model. Split large codebases into smaller, processable pieces.

4. **Model Interaction**: Utilize the OpenAI GPT-3 model to analyze each code chunk and generate documentation. Guide the model with specific prompts for optimal results.

5. **Documentation Generation**: Generate detailed documentation, including function/class descriptions, parameter lists, return types, usage examples, and other relevant details.

6. **Integration with GitHub**: Automate the creation and updating of documentation files within GitHub repositories, including generating Markdown files or updating READMEs.

7. **Quality Assurance**: Review the generated documentation for accuracy and clarity. Human oversight is crucial, especially for complex or domain-specific code.

8. **Iterative Improvement**: Refine the documentation process based on feedback. This may include adjusting prompts, refining templates, or improving data preparation.

9. **Automation Pipeline**: Set up an automation pipeline to update the documentation as the codebase evolves, ensuring that it stays current with the latest changes.

By following these steps, you can automate the creation of comprehensive and accurate documentation for your legacy code hosted on GitHub.

## 📦 **Installation**

To set up and use the Code Documentation Generator, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/code-documentation-generator.git
   cd code-documentation-generator
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Obtain an OpenAI API Key**:

   Sign up for access to the OpenAI API on the [OpenAI website](https://openai.com) and obtain your API key.

4. **Set Your API Key as an Environment Variable**:

   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

## ⚙️ **Usage**

To generate documentation for a specific piece of code, run the `generate_documentation.py` script with the path to your code file:

```bash
python generate_documentation.py path/to/your/code.py
```

The tool will send the code to the GPT-3 API and print the generated documentation to the console.

## 📋 **Example**

For instance, if you have a Python function like this:

```python
def greet(name):
    """
    Greets the user by name.
    
    Parameters:
        name (str): The name of the user.
        
    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}! Welcome."
```

Running the documentation generator on this code may produce documentation like:

> **This function, `greet`, takes a single argument, `name`, which is a string representing the name of the user. It returns a string containing a greeting message addressed to the user.**

## 🤝 **Contributing**

Contributions are welcome! If you find any bugs, have ideas for improvements, or would like to add new features, please open an issue or submit a pull request.

## 📄 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

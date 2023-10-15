import os
import re
import glob
import html  # Import the HTML escape module

# Function to preserve newlines and indentation
def preserve_formatting(text):
    return '\n'.join([line.rstrip() for line in text.split('\n')])



# Specify the directory containing question HTML files
questions_directory = 'questions/'

# Specify the directory containing solution files
solutions_directory = 'D:\\leetcode\\'

# Create a directory to store the updated HTML files
output_directory = 'output/'

# Function to manually escape HTML characters
# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Iterate through the question HTML files
for question_filename in os.listdir(questions_directory):
    if question_filename.startswith("question_") and question_filename.endswith(".html"):
        question_number = re.search(r'(\d+)', question_filename).group(0)

        # Read the question HTML content
        with open(os.path.join(questions_directory, question_filename), 'r', encoding='utf-8') as question_file:
            question_content = question_file.read()

        # Check if there's a corresponding solution file
        solution_filename = os.path.join(solutions_directory, f"{question_number}.*.cpp")
        solution_files = glob.glob(solution_filename)

        # Create a new HTML file for the question
        output_filename = os.path.join(output_directory, question_filename)
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(question_content)  # Include the question content

            # Include the solution content if found
            if solution_files:
                for solution_file in solution_files:
                    with open(solution_file, 'r', encoding='utf-8') as solution_content:
                        output_file.write(f"\n<!-- Solution for Question {question_number} -->\n")
                        solution_content_text = solution_content.read()
                        escaped_solution_content = html.escape(solution_content_text)
                        formatted_escaped_solution = f'<pre>{escaped_solution_content}</pre>'
                        output_file.write(formatted_escaped_solution)

        print(f"HTML file for Question {question_number} with the solution has been created.")

print("HTML files with solutions for each question have been created.")


merged_directory = 'merged/'

# Create the merged directory if it doesn't exist
os.makedirs(merged_directory, exist_ok=True)

# Create the index file for merging
index_filename = os.path.join(merged_directory, 'index.html')

# Create the index file with the initial HTML structure
with open(index_filename, 'w', encoding='utf-8') as index_file:
    index_file.write('''<!DOCTYPE html>
<html>
<head>
    <title>Merged HTML</title>
</head>
<body>
''')

# Iterate through the question HTML files
for question_filename in os.listdir(output_directory):
    if question_filename.startswith("question_") and question_filename.endswith(".html"):
        with open(os.path.join(output_directory, question_filename), 'r', encoding='utf-8') as question_file:
            question_content = question_file.read()

            # Append the content of each question's HTML file to the index file
            with open(index_filename, 'a', encoding='utf-8') as index_file:
                index_file.write(question_content)

# Complete the HTML structure in the index file
with open(index_filename, 'a', encoding='utf-8') as index_file:
    index_file.write('''</body>
</html>
''')

print("All HTML files have been merged into 'index.html'.")

import requests
from bs4 import BeautifulSoup

class Question:
    def __init__(self, question_text, question_html, options_text, options_html, answer_text, answer_html):
        self.question_text = question_text
        self.question_html = question_html
        self.options_text = options_text  # This will be a list
        self.options_html = options_html  # This will be a list
        self.answer_text = answer_text
        self.answer_html = answer_html

    def __str__(self):
        # This method allows you to print the Question object in a readable format
        output = f"Question: {self.question_text}\nQuestion HTML: {self.question_html}\nOptions:\n"
        for option_text, option_html in zip(self.options_text, self.options_html):
            output += f"- {option_text}\nOption HTML: {option_html}\n"
        output += f"Answer: {self.answer_text}\nAnswer HTML: {self.answer_html}\n"
        return output

def getPageQuestions(url): # Returns an list of objects
    questions = []  # Initialize list to collect Question objects

    while url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers, verify= False)  # Assuming SSL verification is enabled
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            question_blocks = soup.find_all('div', class_='bix-div-container')

            for block in question_blocks:
                question_text = block.find('div', class_='bix-td-qtxt').text.strip() if block.find('div', class_='bix-td-qtxt') else "Question not found"
                question_html = block.find('div', class_='bix-td-qtxt').prettify() if block.find('div', class_='bix-td-qtxt') else "<div>Question not found</div>"

                options_text = []
                options_html = []
                options_container = block.find_all('div', class_='bix-tbl-options')
                for option in options_container:
                    for td in option.find_all('div', class_='flex-wrap'):
                        options_text.append(td.text.strip())
                        options_html.append(td.prettify())

                try:
                    answer_block = block.find('div', class_='bix-td-miscell').find('div', class_='bix-ans-option').find('div', class_="ps-1 pt-1")
                    answer_text = answer_block.find('span').get('class')[1].replace('mdi-alpha-', '').replace('-circle-outline', '') if answer_block else "Answer not found"
                    answer_html = answer_block.prettify() if answer_block else "<div>Answer not found</div>"
                except AttributeError:
                    answer_text = "Answer not found"
                    answer_html = "<div>Answer not found</div>"

                # Create a Question object and append it to the list
                questions.append(Question(question_text, question_html, options_text, options_html, answer_text, answer_html))

            # Find the 'Next' button and update the URL or break the loop
            next_button = soup.findAll('a', class_="page-link")[-1]
            if next_button and next_button.get('href') and next_button.get('href') != 'https://#':
                url = next_button.get('href')
            else:
                break  # End loop

        except requests.exceptions.RequestException as e:
            print(f"Error during requests to {url} : {str(e)}")
            break  # Exit the loop on error

    return questions  # Return the list of Question objects

# Example usage
# scraped_questions = getPageQuestions("https://www.indiabix.com/c-programming/strings/")
# for question in scraped_questions:
#     print(question  )  # Each Question object's __str__ method is called here

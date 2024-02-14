import requests
from bs4 import BeautifulSoup

class Question:
    def __init__(self, id=None, posted=None, jobFunctionSought=None, desiredIndustry=None, location=None,
                 objective=None, experience=None, education=None, affiliations=None, skills=None,
                 additionalInformation=None, reference=None):
        self.id = id
        self.posted = posted
        self.jobFunctionSought = jobFunctionSought
        self.desiredIndustry = desiredIndustry
        self.location = location
        self.objective = objective
        self.experience = experience
        self.education = education
        self.affiliations = affiliations
        self.skills = skills
        self.additionalInformation = additionalInformation
        self.reference = reference

    def __str__(self):
        return (f"ID: {self.id}\nPosted: {self.posted}\nJob Function Sought: {self.jobFunctionSought}\n"
                f"\nDesired Industry: {self.desiredIndustry}\nLocation: {self.location}\n"
                f"\nObjective: {self.objective}\nExperience: {self.experience}\n"
                f"\nEducation: {self.education}\nAffiliations: {self.affiliations}\n"
                f"\nSkills: {self.skills}\nAdditional Information: {self.additionalInformation}\n"
                f"\nReference: {self.reference}")

def getPageQuestions(url): # Returns an list of objects
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)  # Assuming SSL verification is enabled
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', id='Table3').parent.find_all('table')[1].find_all('table')[0]
        desired_content = table.find('table').find_next_siblings()

        category_map = {
            "Objective": "objective",
            "Experience": "experience",
            "Education": "education",
            "Skills": "skills",
            "Additional Information": "additionalInformation",
            "Reference": "reference",
            "Affiliations": "affiliations"
        }

        question = Question()

        for content in desired_content:
            if content.name == 'font':
                current_category = content.find('b').text.strip().replace(':', '')
                if current_category in category_map:
                    print(category_map[current_category])
                    text_content = str(content.find('font')).replace('<br>', '\n').replace('<br/>', '\n')
                    if hasattr(question, category_map[current_category]):
                        setattr(question, category_map[current_category], text_content)
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url} : {str(e)}")

    return question  # Return the list of Question objects

# Example usage

# scraped_questions = getPageQuestions("https://www.jobspider.com/job/view-resume-39673.html")
# print(scraped_questions)

prompt_template = """
    You are an expert at creating interview questions across multiple domains, including coding, theoretical knowledge, and behavioral insights.
    Your goal is to thoroughly prepare an individual for various aspects of their interview, including technical proficiency, problem-solving, and personal fit.
    Using the material below, create atleast {num_questions} questions or more if needed that assess coding skills, technical understanding, problem-solving abilities, and general reasoning where applicable.

    ------------
    {text}
    ------------

    Ensure each question provides significant value and covers diverse aspects of the material.
    Make sure not to lose any important information.
    Just Give the questions in English and not other things like headings.

    QUESTIONS:
    """


refine_template = ("""
    You are an expert at refining interview questions to cover a comprehensive range of topics.
    Your goal is to ensure readiness of an individual for both technical and non-technical aspects of an interview.
    We have received some practice questions to a certain extent: {existing_answer}.
    Select the best {num_questions} questions from the list, focusing on those that cover diverse competencies.
    We have the option to refine the existing questions to maximize coverage of technical, analytical, and interpersonal competencies.
    We have the option to refine the existing questions or add new ones (only if necessary) with some more context below.
                   
    ------------
    {text}
    ------------

    Given the new context, improve the questions where relevant or introduce new ones to cover any missing aspects.
    If the context is not helpful, please provide the original questions.
    Also add the question number in front of questions generated.
    
    QUESTIONS:
    """
)
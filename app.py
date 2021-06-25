"""Allows users to take a satisfaction survey and stores their responses for later use."""
from surveys import Question, Survey, satisfaction_survey
from flask import Flask, request, render_template, redirect
app=Flask(__name__)

max_question_number = len(satisfaction_survey.questions)
question_number = 0
option_number = 0
responses = []

@app.route('/')
def survey_start():
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    return render_template('survey_start.html', survey_title=survey_title, survey_instructions=survey_instructions, question_number=question_number)

@app.route('/questions/<int:question_number>')
def survey_question(question_number):
    option_number = 0
    options_and_indices = {}
    if question_number + 1 <= max_question_number:
        survey_question = satisfaction_survey.questions[question_number].question
        survey_options=satisfaction_survey.questions[question_number].choices
        for option in survey_options:
            options_and_indices[option] = option_number
            option_number += 1
    question_number+= 1
    if question_number > max_question_number:
        return redirect('/end_survey')
    else:
        return render_template('survey_question.html', question_number=question_number, max_question_number=max_question_number, survey_question=survey_question, options_and_indices=options_and_indices)

@app.route('/answer', methods = ['POST'])
def get_answers():
    answer = request.form[f'question_{question_number + 1}']
    responses.append(satisfaction_survey.questions[question_number].choices[int(answer)])
    return redirect(f'/questions/{question_number + 1}')

@app.route('/end_survey')
def survey_end():
    return render_template('end_survey.html')
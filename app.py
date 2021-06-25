"""Allows users to take a satisfaction survey and stores their responses for later use."""
from surveys import Question, Survey, satisfaction_survey
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
app=Flask(__name__)
app.config['SECRET_KEY'] = 'catdog'
debug = DebugToolbarExtension(app)

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
    if question_number + 1 <= max_question_number and question_number == len(responses):
        survey_question = satisfaction_survey.questions[question_number].question
        survey_options=satisfaction_survey.questions[question_number].choices
        for option in survey_options:
            options_and_indices[option] = option_number
            option_number += 1
        return render_template('survey_question.html', question_number=question_number, max_question_number=max_question_number, survey_question=survey_question, options_and_indices=options_and_indices)
    elif len(responses) == max_question_number:
        flash(f"You have already completed the survey!")
        return redirect('/end_survey')
    elif question_number + 1 > max_question_number and len(responses) < max_question_number:
        flash(f"The survey does not have question {question_number}!")
        return redirect(f'/questions/{len(responses)}')
    else:
        question_number = len(responses)
        flash("Please do the questions in order!")
        return redirect(f'/questions/{question_number}')

@app.route('/answer', methods = ['POST'])
def get_answers():
    global question_number
    answer = request.form[f'question_{question_number}']
    question_number += 1
    if question_number < max_question_number:
        responses.append(satisfaction_survey.questions[question_number - 1].choices[int(answer)])
        return redirect(f'/questions/{question_number}')
    elif question_number == max_question_number:
        responses.append(satisfaction_survey.questions[question_number - 1].choices[int(answer)])
        return redirect('/end_survey')

@app.route('/end_survey')
def survey_end():
    return render_template('end_survey.html', responses=responses)
"""Allows users to take a satisfaction survey and stores their responses for later use."""
from surveys import Question, Survey, satisfaction_survey
from flask import Flask, request, render_template
app=Flask(__name__)

responses = []

@app.route('/')
def survey_start():
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    return render_template('survey_start.html', survey_title=survey_title, survey_instructions=survey_instructions)
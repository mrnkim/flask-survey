from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
# responses_length = len(responses)

@app.get('/')
def show_survey_start():
    """returns the start of the survey with title and instructions"""
    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", title=title, instructions=instructions)

@app.post('/begin')
def begin_survey():
    """redirect to the first question page"""
    return redirect('/questions/0')

@app.get(f'/questions/{len(responses)}')
def first_question():
    """returns question"""

    prompt = survey.questions[len(responses)].prompt
    choices = survey.questions[len(responses)].choices

    return render_template("question.html", prompt=prompt, choices=choices)

@app.post('/answer')
def answer():
    responses.append(request.form["answer"])
    # responses_length = len(responses)
    if (len(responses) == len(survey.questions)):
        return redirect('/completion.html')
    else:
        return redirect(f'/questions/{len(responses)}')
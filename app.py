from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def show_survey_start():
    """returns the start of the survey with title and instructions"""

    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html", title=title, instructions=instructions)

@app.post('/begin')
def begin_survey():
    """redirect to the first question page"""

    session['responses'] = []

    return redirect('/questions/0')

@app.get('/questions/<number>')
def show_question(number):
    """returns question"""

    res_len = len(session['responses'])

    if not number == str(res_len):
        number = res_len
        return redirect(f'/questions/{number}')

    prompt = survey.questions[res_len].prompt
    choices = survey.questions[res_len].choices

    return render_template("question.html", prompt=prompt, choices=choices)

@app.post('/answer')
def answer():
    """updates responses and returns next question or completion page if survey is done"""

    response = session['responses']
    response.append(request.form["answer"])
    session['responses'] = response

    if (len(session['responses']) == len(survey.questions)):
        return redirect('/completion')
    else:
        # breakpoint()
        return redirect(f'/questions/{len(response)}')

@app.get('/completion')
def completed_survey():
    """brings user to thank you page when done"""

    return render_template("completion.html")
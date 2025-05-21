from flask import Flask, render_template, request, redirect, url_for, flash
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages

# Ensure static folder exists
if not os.path.exists('static'):
    os.makedirs('static')

def get_score(question, answer):
    if question == 'weight':
        if answer == 'Yes, more than 5kg': return 3
        elif answer == 'Yes, less than 5kg': return 2
        elif answer == 'No change': return 0
    elif question == 'tired':
        if answer == 'Yes, Daily': return 3
        elif answer == 'sometimes': return 2
        elif answer == 'Only after activity': return 1
        elif answer == ' No, full energy': return 0
    elif question == 'lump':
        if answer == 'Yes, its growing': return 3
        elif answer == 'Yes, its small and unchnaged': return 2
        elif answer == 'Not sure': return 1
        else: return 0
    elif question == 'bleeding':
        if answer.startswith('Yes'): return 3
        else: return 0
    elif question == 'cough':
        if answer == 'Yes, with mucus and blood': return 3
        elif answer == 'Yes, dry cough': return 2
        elif answer == 'No, just short term cough': return 1
        else: return 0
    elif question == 'pain':
        if answer == 'Yes, constant': return 3
        elif answer == 'Yes, on and off': return 1
        else: return 0
    elif question == 'spot':
        if answer == 'Yes, it changed color or shape': return 3
        elif answer == 'Yes, it bleeds or itches': return 2
        elif answer == 'Not sure': return 1
        else: return 0
    elif question == 'bowel_habits':
        if answer == 'Yes, blood in stool': return 3
        elif answer == 'Yes, frequent diarrhea': return 2
        elif answer == 'Yes, frequent constipation': return 2
        else: return 0
    elif question == 'swallow':
        if answer == 'Yes, difficulty swallowing solids' : return 3 
        elif answer == 'Constant blaoting or heartburn': return 1
        else: return 0
    elif question == 'voice':
        if answer =="Always hoarse": return 3
        elif answer =="Its improving": return 2
        elif answer =='Just started':  return 1
        else: return 0
    elif question == 'urine':
        if answer.startswith('Yes'): return 3
        elif answer == 'Frequent or painful urination' or answer == 'suddne urge to urinate': return 1
        else: return 0
    elif question == 'alcohol':
        if answer == 'Yes, daily': return 3
        else: return 0
    elif question == 'smoking':
        if answer =='Yes, daily': return 3
        elif answer =='Weekly': return 2
        elif answer =='I quit': return 1
        else: return 0
    elif question == 'stress':
        if answer.startswith('Yes, diagnosed condition'): return 3
        elif answer == "I'm unsure": return 1
        else: return 0
    elif question == 'family':
        if answer.startswith('Yes, First degree relatives'): return 3
        elif answer == 'distant relative': return 2
        else: return 0
    return 0

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        return redirect(url_for('health_profile'))
    return render_template('create_profile.html')

@app.route('/health-profile', methods=['GET', 'POST'])
def health_profile():
    if request.method == 'POST':
        data = request.form.to_dict()
        user_scores = []
        questions = ['weight', 'tired', 'lump', 'bleeding', 'cough', 'pain', 'spot',
                     'bowel_habits', 'swallow', 'voice', 'urine', 'alcohol', 'smoking', 'stress', 'family']
        for q in questions:
            answer = data.get(q)
            if answer:
                user_scores.append(get_score(q, answer))
            else:
                user_scores.append(0)

        user_scores_str = ','.join(map(str, user_scores))
        return redirect(url_for('processing', user_scores=user_scores_str))
        print(f"user_scores_str before redirect: {user_scores_str}")
    return render_template('health_profile.html')

@app.route('/processing')
def processing():
    user_scores = request.args.get('user_scores')
    # Redirect to the report page, passing the user_scores
    return render_template('processing.html', user_scores=user_scores)

@app.route('/report')
def report():
    user_scores_str = request.args.get('user_scores')
    user_scores = []
    if user_scores_str:
        try:
            user_scores = [int(x) for x in user_scores_str.split(',')]
        except ValueError:
            user_scores = [0] * 15

    global_avg = [1, 1, 0.5, 0.3, 0.5, 0.2, 0.4, 0.6, 0.5, 0.2, 0.5, 0.8, 1, 1, 0.6]
    return render_template('report.html', user_scores=user_scores, global_avg=global_avg)

if __name__ == '__main__':
    app.run(debug=True)
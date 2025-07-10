from flask import Flask, render_template, request, redirect, url_for
from quiz_brain import QuizBrain
from data import question_data
from question_model import Question

app = Flask(__name__)

# Initialize quiz and question bank
question_bank = [Question(q["question"], q["correct_answer"], q["incorrect_answers"]) for q in question_data]
quiz = QuizBrain(question_bank)

feedback_message = None  # To store feedback between requests


@app.route("/", methods=["GET", "POST"])
def index():
    global feedback_message

    if request.method == "POST":
        user_answer = request.form["answer"]
        correct_answer = quiz.current_question.answer

        if quiz.check_answer(user_answer, correct_answer):
            feedback_message = "Correct!"
        else:
            feedback_message = f"Wrong! The correct answer was: {correct_answer}"

        if quiz.still_has_questions():
            return redirect(url_for("index"))
        else:
            return redirect(url_for("result"))

    # Get next question
    current_question = quiz.next_question()
    if current_question:
        return render_template(
            "index.html",
            question=current_question.text,
            options=current_question.options,
            question_number=quiz.question_number,
            score=quiz.score,
            feedback=feedback_message
        )
    else:
        return redirect(url_for("result"))


@app.route("/result")
def result():
    return render_template("result.html", score=quiz.score, total=quiz.question_number)


@app.route("/reset")
def reset():
    global quiz, feedback_message
    # Reinitialize everything
    question_box = [Question(q["question"], q["correct_answer"], q["incorrect_answers"]) for q in question_data]
    quiz = QuizBrain(question_box)
    feedback_message = None
    return redirect(url_for("index"))

@app.route("/quit")
def quit_game():
    return render_template("thankyou.html")



if __name__ == "__main__":
    app.run(debug=True)

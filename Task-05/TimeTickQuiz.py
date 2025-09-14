import requests
import html
import random
import threading
import time

CATEGORY_URL = "https://opentdb.com/api_category.php"
QUESTION_URL = "https://opentdb.com/api.php"
TIME_LIMIT = 15  


def fetch_categories():
    try:
        response = requests.get(CATEGORY_URL)
        data = response.json()
        return data["trivia_categories"]
    except Exception as e:
        print("Error fetching categories:", e)
        return []


def fetch_questions(amount=5, category=None, difficulty=None, q_type="multiple"):
    params = {
        "amount": amount,
        "type": q_type
    }
    if category:
        params["category"] = category
    if difficulty:
        params["difficulty"] = difficulty

    try:
        response = requests.get(QUESTION_URL, params=params)
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print("Error fetching questions:", e)
        return []


def select_category(categories):
    if not categories:
        print("No categories available, skipping selection.")
        return None

    print("\nAvailable Categories:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat['name']}")

    try:
        choice = int(input("Select a category (number): "))
        if 1 <= choice <= len(categories):
            return categories[choice - 1]["id"]
    except:
        pass

    print("Invalid choice, using random category.")
    return None


def select_difficulty():
    levels = ["easy", "medium", "hard"]
    print("\nDifficulties: easy / medium / hard")
    choice = input("Choose difficulty: ").lower()
    if choice in levels:
        return choice
    print("Invalid choice, using easy.")
    return "easy"


def select_question_type():
    print("\nQuestion types: multiple / boolean")
    choice = input("Choose type: ").lower()
    if choice in ["multiple", "boolean"]:
        return choice
    print("Invalid choice, using multiple.")
    return "multiple"


def ask_question(q_data, q_num, time_limit=TIME_LIMIT):
    answer = None
    question = html.unescape(q_data["question"])
    correct = html.unescape(q_data["correct_answer"])
    options = [html.unescape(opt) for opt in q_data["incorrect_answers"]]
    options.append(correct)
    random.shuffle(options)

    print(f"\nQ{q_num}: {question}")
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")

    def user_input():
        nonlocal answer
        try:
            answer = input("Your choice: ")
        except:
            answer = None

    start = time.time()
    t = threading.Thread(target=user_input)
    t.start()
    t.join(timeout=time_limit)
    elapsed = time.time() - start

    if answer is None:
        print("⏳ Time's up! No answer chosen.")
        return 0

    try:
        chosen = options[int(answer) - 1]
        if chosen == correct:
            print("Correct!")
            if elapsed < 5:
                print("Bonus Point for fast answer!")
                return 2  # fast correct answer
            return 1  # normal correct answer
        else:
            print(f"Wrong! Correct answer: {correct}")
            return 0
    except:
        print(f"Invalid input! Correct answer: {correct}")
        return 0


def select_quiz_options(categories):
    category = select_category(categories)
    difficulty = select_difficulty()
    q_type = select_question_type()
    try:
        num_q = int(input("\nHow many questions? "))
    except:
        num_q = 5
    return fetch_questions(num_q, category, difficulty, q_type)


def main():
    print("Welcome to TimeTickQuiz!")
    print(f"You have {TIME_LIMIT} seconds per question.\n")

    categories = fetch_categories()
    questions = select_quiz_options(categories)

    score = 0
    for i, q in enumerate(questions, 1):
        score += ask_question(q, i)

    print("\n Quiz Over!")
    print(f"Your Score: {score}/{len(questions)} (Bonus included)")


if __name__ == "__main__":
    main()

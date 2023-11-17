from flask import Flask, render_template, request, jsonify
from chatbot import get_answer_for_mistake, load_knowledge_base, find_best_match, get_answer_for_question

app = Flask(__name__)

knowledge_base_path = 'app\knowledge_base.json'  # Ajusta la ruta según sea necesario
knowledge_base = load_knowledge_base(knowledge_base_path)

@app.route('/chat', methods=['GET','POST'])
def chat():
    try:
        user_input = request.json['user_input']
        # Resto del código...
            # Lógica del chatbot
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])

        if any(ban["ban"] in user_input.lower() for ban in knowledge_base["ban"]):
            response = get_answer_for_mistake(user_input, knowledge_base)
        elif best_match:
            response = get_answer_for_question(best_match, knowledge_base)
        else:
            response = "No sé la respuesta. ¿Puede enseñármela?"

        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    

if __name__ == '__main__':
    app.run(debug=True)

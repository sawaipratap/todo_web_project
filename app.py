from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient
from bson import ObjectId
from config import MongoUrl

app = Flask(__name__)

# Connect to MongoDB
# Update the URI as needed if using remote database (e.g. MongoDB Atlas)
client = client = MongoClient(MongoUrl)
db = client["todo_database"]
collection = db["todos"]

@app.route('/')
def index():
    todos = list(collection.find({}))
    for todo in todos:
        todo['_id'] = str(todo['_id'])  # Convert ObjectId to string
    return render_template("index.html", todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get("title")
    description = request.form.get("description")
    if title and description:
        collection.insert_one({
            "title": title,
            "description": description,
            "completed": False
        })
    return redirect(url_for('index'))

@app.route('/complete/<todo_id>')
def complete_todo(todo_id):
    try:
        collection.update_one({"_id": ObjectId(todo_id)}, {"$set": {"completed": True}})
    except:
        pass
    return redirect(url_for('index'))

@app.route('/delete/<todo_id>')
def delete_todo(todo_id):
    try:
        collection.delete_one({"_id": ObjectId(todo_id)})
    except:
        pass
    return redirect(url_for('index'))

@app.route('/update/<todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    if request.method == 'POST':
        new_title = request.form.get("title")
        new_description = request.form.get("description")
        if new_title and new_description:
            collection.update_one({"_id": ObjectId(todo_id)}, {
                "$set": {
                    "title": new_title,
                    "description": new_description
                }
            })
        return redirect(url_for('index'))
    else:
        # GET method: Show a form to update the todo
        todo = collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            todo['_id'] = str(todo['_id'])  # Convert ObjectId to string
        return render_template("update.html", todo=todo)

# @app.teardown_appcontext
# def close_db(exception):
#     client.close()

if __name__ == '__main__':
    app.run(debug=True)
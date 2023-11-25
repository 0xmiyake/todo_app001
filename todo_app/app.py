from datetime import datetime

from flask import Flask, render_template, request, redirect # 追加で2つimportする
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        return render_template('index.html', posts=posts)
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
    # キャスト
        due = datetime.strptime(due, '%Y-%m-%d')
    #新しい投稿として作成
        new_post = Post(title=title, detail=detail, due=due)
    # 新しい投稿を保存 dbにデータを保存
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')


@app.route('/create')
def create():
    return render_template('create.html')

if __name__ == "__main__":
    app.run(debug=True)

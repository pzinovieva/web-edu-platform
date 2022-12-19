from flask import (
    Blueprint, render_template, request, redirect
)
from app.moduls.forms import (
    AddArticleForm
)
from app.database.articles import (
    Article
)
from app.database.users import (
    User
)
from app.database.db_session import create_session
from flask_login import current_user
from mammoth import convert_to_html

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/')
def blog():
    db_session = create_session()
    articles = db_session.query(Article)
    user = db_session.query(User).filter(User.id == 1).first()
    return render_template("blog.html", articles=articles, user=user)


@bp.route('/<int:index_article>')
def showCurrentArticle(index_article):
    db_session = create_session()
    article = db_session.query(Article).filter(Article.id == index_article).first()
    return render_template("current_article.html", article=article, article_content=article.content)


@bp.route('/create-article', methods=['GET', 'POST'])
def createArticle():
    form = AddArticleForm()
    db_session = create_session()
    if form.validate_on_submit():
        if request.method == 'POST':
            f = request.files['file']
            print(f.filename)
            if ".docx" in f.filename:
                content = articleToHtml(f)
                article = Article(
                    title=form.title.data,
                    description=form.description.data,
                    content=content,
                    user_id=current_user.id
                )
                db_session.add(article)
                db_session.commit()
                return redirect("/blog")
            else:
                return render_template(
                    'add_article.html',
                    title='Добавление статьи',
                    btn_txt="Создать", form=form,
                    message="Загрузите файл в формате .docx"
                )
    return render_template("add_article.html", title='Добавление статьи', btn_txt="Создать", form=form)


def articleToHtml(document):
    new_document = convert_to_html(document)
    string = new_document.value
    return string


@bp.route('/upgrade/<int:index_article>', methods=['GET', 'POST'])
def upgradeArticle(index_article):
    form = AddArticleForm()
    if request.method == "GET":
        db_session = create_session()
        article = db_session.query(Article).filter(Article.id == index_article).first()
        if article:
            form.title.data = article.title
            form.description.data = article.description
    if form.validate_on_submit():
        db_session = create_session()
        article = db_session.query(Article).filter(Article.id == index_article).first()
        if article:
            f = request.files['file']
            if ".docx" in f.filename:
                content = articleToHtml(f)
                article.title = form.title.data
                article.description = form.description.data
                article.content = content
                db_session.commit()
                return redirect('/blog')
            else:
                render_template('add_article.html',
                                title='Редактирование статьи',
                                btn_txt="Изменить",
                                form=form,
                                message="Загрузите файл в формате .docx"
                                )
    return render_template('add_article.html',
                           title='Редактирование статьи',
                           btn_txt="Изменить",
                           form=form
                           )


@bp.route('/delete/<int:index_article>', methods=['GET', 'POST'])
def deleteArticle(index_article):
    db_session = create_session()
    article = db_session.query(Article).filter(Article.id == index_article).first()
    if article:
        db_session.delete(article)
        db_session.commit()
    return redirect('/blog')


@bp.route('/my-articles')
def showOnlyMyArticles():
    db_session = create_session()
    articles = db_session.query(Article)
    user = db_session.query(User).filter(User.id == 1).first()
    return render_template("only_my_articles.html", articles=articles, user=user)

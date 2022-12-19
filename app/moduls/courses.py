from flask import (
    Blueprint, render_template, request, redirect
)
from app.moduls.forms import (
    AddCourseForm, AddLessonForm
)
from app.database.courses import (
    Course, Lesson, Review
)
from app.database.users import (
    User
)
from app.database.db_session import create_session
from flask_login import current_user
from mammoth import convert_to_html

bp = Blueprint('courses', __name__, url_prefix='/course')


@bp.route('/')
def courses():
    db_session = create_session()
    courses = db_session.query(Course)
    user = db_session.query(User).filter(User.id == 1).first()
    return render_template("courses.html", courses=courses, user=user)


@bp.route('/<int:index_course>')
def showCurrentCourse(index_course):
    db_session = create_session()
    course = db_session.query(Course).filter(Course.id == index_course).first()
    lessons = db_session.query(Lesson).filter(Lesson.course_id == index_course)
    return render_template("current_course.html", course=course, lessons=lessons)


@bp.route('/<int:index_course>/<int:index_lesson>')
def showCurrentLesson(index_course, index_lesson):
    db_session = create_session()
    course = db_session.query(Course).filter(Course.id == index_course).first()
    lessons = db_session.query(Lesson).filter(Lesson.id == index_lesson).first()
    return render_template("current_lesson.html", course=course, lessons=lessons)


@bp.route('/create-course', methods=['GET', 'POST'])
def addCourse():
    form = AddCourseForm()
    db_session = create_session()
    if form.validate_on_submit():
        if request.method == 'POST':
            course = Course(
                title=form.title.data,
                description=form.description.data,
                user_id=current_user.id
            )
            db_session.add(course)
            db_session.commit()
            return redirect("/course")
    return render_template("add_course.html", title='Добавление статьи', btn_txt="Создать", form=form)


def docxToHtml(document):
    new_document = convert_to_html(document)
    string = new_document.value
    return string


def videoLinkToEmbedFormat(link):
    if "https://www.youtube.com/" in link:
        if "embed" not in link:
            if "watch?v=" in link:
                return link.replace("watch?v=", "/embed/")
            part_code = link.replace("https://www.youtube.com/", "/embed/")
            return "https://www.youtube.com" + part_code
        else:
            return link
    elif "https://youtu.be/" in link:
        part_code = link.replace("https://youtu.be/", "/embed/")
        return "https://www.youtube.com" + part_code
    return


@bp.route('/<int:index_course>/add_lesson', methods=['GET', 'POST'])
def addLesson(index_course):
    form = AddLessonForm()
    db_session = create_session()
    if form.validate_on_submit():
        if request.method == 'POST':
            f_lesson = request.files['file_lesson']
            f_homework = request.files['file_homework']
            if (".docx" in f_lesson.filename) and (".docx" in f_homework.filename):
                link_video = videoLinkToEmbedFormat(form.link_video.data)
                print(link_video)
                if link_video:
                    lesson = Lesson(
                        title=form.title.data,
                        content=docxToHtml(f_lesson),
                        link_video=link_video,
                        content_homework=docxToHtml(f_homework),
                        course_id=index_course
                    )
                    db_session.add(lesson)
                    db_session.commit()
                    return showCurrentCourse(index_course)
                else:
                    return render_template(
                        "add_lesson.html",
                        title='Добавление урока',
                        btn_txt="Создать",
                        form=form,
                        index_course=index_course,
                        message='''Принимаются только ссылки на видео с youtube в трех форматах:
                        https://www.youtube.com/embed/какой-то_набор символов,  
                        https://www.youtube.com/watch?v=какой-то_набор символов
                        https://youtu.be/какой-то_набор символов'''
                    )
            else:
                return render_template(
                    "add_lesson.html",
                    title='Добавление урока',
                    btn_txt="Создать",
                    form=form,
                    index_course=index_course,
                    message='''Файл должен быть с расширением .docx'''
                )
    return render_template(
        "add_lesson.html",
        title='Добавление урока',
        btn_txt="Создать",
        form=form,
        index_course=index_course
    )


@bp.route('/delete/<int:index_course>/<int:index_lesson>', methods=['GET', 'POST'])
def deleteLesson(index_course, index_lesson):
    db_session = create_session()
    print("aaaaaaaaaaaaaa", index_lesson, index_course)
    lesson = db_session.query(Lesson).filter(Lesson.id == index_lesson).first()
    if lesson:
        db_session.delete(lesson)
        db_session.commit()
        return showCurrentCourse(index_course)
    return redirect('/course')


@bp.route('/delete/<int:index_course>', methods=['GET', 'POST'])
def deleteCourse(index_course):
    db_session = create_session()
    lessons = db_session.query(Lesson).filter(Lesson.course_id == index_course)
    if lessons:
        for lesson in lessons:
            db_session.delete(lesson)
            db_session.commit()
    course = db_session.query(Course).filter(Course.id == index_course).first()
    if course:
        db_session.delete(course)
        db_session.commit()
    return redirect('/course')


@bp.route('/my-courses')
def showOnlyMyCourses():
    db_session = create_session()
    courses = db_session.query(Course)
    return render_template("only_my_courses.html", courses=courses)

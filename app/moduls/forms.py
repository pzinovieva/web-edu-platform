from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField('Фамилия Имя Отчество', validators=[DataRequired()])
    type_user = SelectField(u'Выберите тип пользователя ', choices=[('ученик', 'Я ученик'), ('логопед', 'Я логопед')])
    login = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повторить пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


class AddArticleForm(FlaskForm):
    title = StringField('Название статьи', validators=[DataRequired()])
    description = TextAreaField('Описание статьи', validators=[DataRequired()])
    file = FileField('Загрузить статью', validators=[DataRequired()], name="file")
    submit = SubmitField('Создать')


class AddCourseForm(FlaskForm):
    title = StringField('Название курса', validators=[DataRequired()])
    description = TextAreaField('Описание курса', validators=[DataRequired()])
    submit = SubmitField('Создать')


class AddLessonForm(FlaskForm):
    title = StringField('Название курса', validators=[DataRequired()])
    link_video = StringField('Ссылка на видео', validators=[DataRequired()])
    file_lesson = FileField('Загрузить текст урока', name="file_lesson", validators=[DataRequired()])
    file_homework = FileField('Загрузить домашнюю работу', name="file_homework", validators=[DataRequired()])
    submit = SubmitField('Создать')

from flask import (
    Flask
)
import app.database.db_session as db_session


def create_app():
    import app.moduls.home as home_page
    import app.moduls.blog as blog_page
    import app.moduls.courses as course_page
    import app.moduls.parents as parents_pages
    import app.moduls.auth as auth_page
    from app.moduls.auth import login_manager

    app = Flask(__name__, template_folder="app\\templates", static_folder="app\\static")
    app.config.from_object('config')

    db_session.global_init("app\\database\\db\\speech_therapist_online.db")
    login_manager.init_app(app)
    app.register_blueprint(home_page.bp)
    app.register_blueprint(blog_page.bp)
    app.register_blueprint(course_page.bp)
    app.register_blueprint(parents_pages.bp)
    app.register_blueprint(auth_page.bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

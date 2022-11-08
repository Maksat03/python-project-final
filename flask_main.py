from flask_app.app import app
from flask import request, render_template, redirect, make_response

from flask_app import services


@app.route("/", methods=["GET"])
def main_page_view():
    return render_template("about_project_page.html",
                           request_is_authenticated=services.request_is_authenticated(request))


@app.route("/login/", methods=["GET", "POST"])
def login_view():
    if request.method == "GET" and not services.request_is_authenticated(request):
        return render_template("login_page.html")
    elif request.method == "POST" and not services.request_is_authenticated(request):
        user_logged_in, session_id = services.user_login(request.form)
        if user_logged_in:
            response = make_response(redirect("/dashboard/"))
            response.set_cookie("session_id", session_id)
            return response
        return render_template("login_page.html", login_form_is_invalid=request.form)
    else:
        return redirect("/dashboard/")


@app.route("/registration/", methods=["GET", "POST"])
def registration_view():
    if request.method == "GET" and not services.request_is_authenticated(request):
        return render_template("registration_page.html")
    elif request.method == "POST" and not services.request_is_authenticated(request):
        user_registered = services.user_register(request.form)
        if user_registered:
            return render_template("success_registration_page.html")
        return render_template("registration_page.html", registration_form_is_invalid=request.form)
    else:
        return redirect("/profile/")


@app.route("/logout/")
def logout_view():
    if services.request_is_authenticated(request):
        services.user_logout(request)
    return redirect("/")


@app.route("/dashboard/", methods=["GET"])
def dashboard_page_view():
    if services.request_is_authenticated(request):
        return render_template("dashboard_page.html", user=services.get_request_user(request))
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

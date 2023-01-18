from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint
from .database import DataBase

view = Blueprint("views", __name__)


#CONSTANTS
USER_NAME = 'name'
MSG_LIMIT = 20


@view.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":  # if user input a name
        name = request.form["inputName"]
        lastName = request.form["tempinputName"]
        if len(name) > 1:
            session[USER_NAME] = name + " " + lastName
            flash(f' You were successfully logged in as {name + " " + lastName}.')
            return redirect(url_for("views.home"))
        else:
            flash(" Please type a longer Name.")

    return render_template("login.html", **{"session": session})


@view.route("/logout")
def logout():
    #Name is logged out successfully and popped from the session
    flash(f' You have logged out')
    session.pop(USER_NAME, None)
    return redirect(url_for("views.login"))


@view.route("/")
@view.route("/home")
def home():
    if USER_NAME not in session: #if user logged out, redirect to login page
        return redirect(url_for("views.login"))
    #else direct to chat 
    return render_template("chatroom.html", **{"session": session})


@view.route("/history")
def history():
    if USER_NAME not in session:
        flash(" Message history can only be accessed once logged in")
        return redirect(url_for("views.login"))

    json_messages = get_history(session[USER_NAME])
    return render_template("history.html", **{"history": json_messages})


@view.route("/get_name")
def get_name():
    data = {"name": ""}
    if USER_NAME in session:
        data = {"name": session[USER_NAME]}
    return jsonify(data)


@view.route("/get_messages")
def get_messages():
    Data1 = DataBase()
    messages = Data1.get_all_messages(MSG_LIMIT)
    new_messages = updated_messages(messages)

    return jsonify(new_messages)


@view.route("/get_history")
def get_history(name):
    Data = DataBase()
    messages = Data.get_messages_by_name(name)
    new_messages = updated_messages(messages)

    return new_messages


# UTILITIES
def updated_messages(msgs):
    messages = []
    for msg in msgs:
        message = msg
        message["time"] = message["time"].split(".")[0][:-3]
        messages.append(message)

    return messages

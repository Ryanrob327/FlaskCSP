from flask import Blueprint, render_template

app_projects = Blueprint('projects', __name__,
                url_prefix='/weeks',
                template_folder='templates/bp_projects/')

# connects /kangaroos path to render kangaroos.html
@app_projects.route('/week05/')
def week05():
    return render_template("week05.html")

# connects /kangaroos path to render kangaroos.html
@app_projects.route('/week06/')
def week06():
    return render_template("week07.html")

@app_projects.route('/week07/')
def week07():
    return render_template("week07.html")

@app_projects.route('/week08/')
def week08():
    return render_template("week08.html")
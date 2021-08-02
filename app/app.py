from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from forms import SignupForm

app = Flask(__name__,
            template_folder="templates",
            static_folder="static",
            static_url_path='')

mysql = MySQL(cursorclass=DictCursor)

app.config.from_object('config.Config')


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Data Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldheight'), request.form.get('fldweight'), city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldheight = %s, t.fldweight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Data Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('fldheight'), request.form.get('fldweight'))
    sql_insert_query = """INSERT INTO tblCitiesImport (fldheight,fldweight) VALUES (%s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/cities', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM tblCitiesImport WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/cities/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['fldheight'], content['fldweight'],city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldheight = %s, t.fldweight = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/cities', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['fldheight'], content['fldweight'])
    sql_insert_query = """INSERT INTO tblCitiesImport (fldheight,fldweight) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/cities/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM tblCitiesImport WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    return render_template(
        '/signup.html',
        title='Create an Account | Flask-Login Tutorial.',
        form=SignupForm(),
        template='signup-page',
        body="Sign up for a user account."
    )


@app.route("/signin")
def dashboard():
    # This had to serve a static page b/c of how tutorial made the route
    return redirect('/dashboard.html')


@app.route("/login")
def login():
    return redirect(url_for('dashboard'))


@app.errorhandler(404)
def not_found(arg):
    """Page not found."""
    return render_template('404.html', title='404 error.', message='Page Not Found')


@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return render_template('400.html', title='400 error.', message='Bad request.  Page Not Found')


@app.errorhandler(500)
def server_error(arg):
    """Internal server error."""
    return render_template('500.html', message='Server Error')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
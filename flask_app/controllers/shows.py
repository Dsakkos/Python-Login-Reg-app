from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import show, user


# CREATE 
@app.route('/new/show', methods=['POST', 'GET'])
def create_show():
    if 'users_id' in session:
        if request.method == 'GET':
            data = {
                'id': session['users_id']
            }
            return render_template('create_report.html', user = user.User.get_user_by_id(data) )
        if show.Show.create_report(request.form):
            return redirect('/users/dashboard')
    else:
        return redirect('/users/logout')
    return redirect('/new/show')



@app.route('/show/<int:id>')
def show_shows(id):
    return render_template('show_post.html', show_show = show.Show.get_one_show(id),  user = user.User.get_user_by_id({"id": session['users_id']}))


# UPDATE 
@app.route('/show/edit/<int:id>')
def update_show(id):
    return render_template('edit_show.html', update = show.Show.get_one_show(id),  user = user.User.get_user_by_id({"id": session['users_id']}))


@app.route('/show/edit', methods=['POST'])
def update_show_method():
    if not show.Show.validate_show(request.form):
        return redirect(f"/show/edit/{request.form['id']}")
    show.Show.update(request.form)
    return redirect('/users/dashboard')




@app.route('/show/delete/<int:id>')
def delete_show(id):
    show.Show.delete_show(id)
    return redirect('/users/dashboard')




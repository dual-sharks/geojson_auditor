# ROUTING AND VIEW LOGIC

from flask import render_template, request, redirect, url_for
from models import update_validation_status, process_previous_next, load_geojson_details, app_state


def init_views(app):
    @app.route('/')
    def index():
        return load_geojson_details(app_state=app_state)

    @app.route('/validate', methods=['POST'])
    def validate():
        update_validation_status(request.form['validation_result'])
        return redirect(url_for('index'))

    @app.route('/previous_geojson', methods=['POST'])
    def previous_geojson():
        process_previous_next(direction='previous')
        return redirect(url_for('index'))

    @app.route('/next_geojson', methods=['POST'])
    def next_geojson():
        process_previous_next(direction='next')
        return redirect(url_for('index'))
    
    @app.route('/edit_name', methods=['POST'])
    def edit_name(): 
        new_name = request.form['new_name']
        app_state.df.loc[app_state.nav_index, 'name'] = new_name
        app_state.df.to_csv('geojsons.csv', index=False)
        return redirect(url_for('index'))

    @app.route('/info_issue', methods=['POST'])
    def info_issue():
        print("Before update:", app_state.df.loc[app_state.nav_index])
        app_state.df.loc[app_state.nav_index, 'info_issue'] = 'issue'

        print("After update:", app_state.df.loc[app_state.nav_index])
        app_state.df.to_csv('geojsons.csv', index=False)
        return redirect(url_for('index'))
    
    @app.route('/mark_bad_polygon', methods=['POST'])
    def mark_bad_polygon():
        print("Before update:", app_state.df.loc[app_state.nav_index])
        app_state.df.loc[app_state.nav_index, 'bad_polygon'] = 'bad'

        print("After update:", app_state.df.loc[app_state.nav_index])
        app_state.df.to_csv('geojsons.csv', index=False)
        return redirect(url_for('index'))

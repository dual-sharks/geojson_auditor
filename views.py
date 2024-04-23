# ROUTING AND VIEW LOGIC

from flask import render_template, request, redirect, url_for
from models import find_next_unvalidated_index, update_validation_status, process_previous_next, load_geojson_details

def init_views(app):
    @app.route('/')
    def index():
        return load_geojson_details()

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
        global nav_index  
        new_name = request.form['new_name']
        df.loc[nav_index, 'name'] = new_name
        df.to_csv('geojsons.csv', index=False)
        return redirect(url_for('index'))

    @app.route('/info_issue', methods=['POST'])
    def info_issue():
        global nav_index  
        print("Before update:", df.loc[nav_index])

        df.loc[nav_index, 'info_issue'] = 'issue'

        print("After update:", df.loc[nav_index])

        df.to_csv('geojsons.csv', index=False)
        return redirect(url_for('index'))
    
    @app.route('/mark_bad_polygon', methods=['POST'])
    def mark_bad_polygon():
        global nav_index
        print("Before update:", df.loc[nav_index])
        df.loc[nav_index, 'bad_polygon'] = 'bad'
        print("After update:", df.loc[nav_index])
        df.to_csv('geojsons.csv', index=False)
        return redirect(url_for('index'))

from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import pprint
import trello as t
from view_model import ViewModel 

pp = pprint.PrettyPrinter(indent=4)

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        view = ViewModel(t.get_items(), t.get_app_board_lists())
        return render_template('index.html' , view_model=view)

    @app.route('/create', methods=['POST'])
    def create():
        t.add_item('5f3d5425b0c82d22a3d25f72', request.form.get('newItemTitle'))
        return redirect(url_for('index'), code=302)

    @app.route('/view/<id>', methods=['GET'])
    def view(id):
        item=session.get_item(id)
        return render_template('item.html', item=item)

    @app.route('/save', methods=['POST'])
    def save():
        id=request.form.get( 'itemId' )
        status=request.form.get( 'itemStatus' )
        title=request.form.get( 'itemTitle' )
        t.save_item(id, status, title)
        return redirect(url_for('index'), code=302)
        
    @app.route('/sort/<sortType>', methods=['GET'])
    def sort_items(sortType):
        unsorted_items = session.get_items()
        sorted_items = sorted(unsorted_items, key=lambda item: item[str(sortType)].upper())
        return render_template('index.html' , items=sorted_items) 

    @app.route('/delete/<id>', methods=['POST'])
    def delete(id):
        t.delete_item(id)
        return redirect(url_for('index'), code=302)

    @app.route('/complete_item/<id>', methods=['POST'])
    def complete_item(id):
        return redirect(url_for('index'), code=302)

    return app

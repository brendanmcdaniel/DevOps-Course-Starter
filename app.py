from flask import Flask, render_template, request, redirect, url_for
import session_items as session
import pprint
import trello as t
pp = pprint.PrettyPrinter(indent=4)

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index(): 
    items = t.get_items()
    statuses = t.get_app_board_lists()
    return render_template('index.html' , items=items, statuses=statuses)
if __name__ == '__main__':
    app.run()

# @app.route('/create', methods=['POST'])
# def create():
#     session.add_item(request.form.get('newItemTitle') )
#     return redirect(url_for('index'), code=302)

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
    print(id)
    print(status)
    print(title)
    t.save_item(id, status, title)
    return redirect(url_for('index'), code=302)
    
@app.route('/sort/<sortType>', methods=['GET'])
def sort_items(sortType):
    unsorted_items = session.get_items()
    pp.pprint(unsorted_items)
    sorted_items = sorted(unsorted_items, key=lambda item: item[str(sortType)].upper())
    pp.pprint(sorted_items)
    return render_template('index.html' , items=sorted_items) 

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    print(t.get_item(id))
    t.delete_item(id)
    return redirect(url_for('index'), code=302)

@app.route('/complete_item/<id>', methods=['POST'])
def complete_item(id):
    #session.delete_item(id)
    return redirect(url_for('index'), code=302)
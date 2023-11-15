
from todo_app import create_app, todo_list_to_list_of_dict
from todo_list import TodoList


def test_todo_list_to_list_of_dict():
    todo_list = TodoList()
    result = todo_list_to_list_of_dict(todo_list.get_list())
    assert result == []

    todo_list.add('d1', 'c1')
    result = todo_list_to_list_of_dict(todo_list.get_list())
    assert result == [{'description':'d1', 'category':'c1'}]

    todo_list.add('d2', 'c2')
    result = todo_list_to_list_of_dict(todo_list.get_list())
    assert result == [{'description':'d1', 'category':'c1'},
                      {'description':'d2', 'category':'c2'}]



def test_todo_list_endpoint_on_empty_todolist():
    app = create_app(TodoList())

    app.config['TESTING'] = True
    client = app.test_client()

    response = client.get('/todos')
    assert response.status_code == 200

    assert response.get_json() == {'data': []}


def test_todo_list_endpoint_on_nonempty_todolist():
    todo_list = TodoList()
    todo_list.add('d1', 'c1')
    todo_list.add('d2', 'c2')

    app = create_app(todo_list)

    app.config['TESTING'] = True
    client = app.test_client()

    response = client.get('/todos')
    assert response.status_code == 200

    assert response.get_json() == {'data': [{'description':'d1', 'category':'c1'},
                                            {'description':'d2', 'category':'c2'}]}


def test_todo_list_endpoint_with_optional_category_parameter():
    todo_list = TodoList()
    todo_list.add('d1', 'c1')
    todo_list.add('d2', 'c2')

    app = create_app(todo_list)

    app.config['TESTING'] = True
    client = app.test_client()

    query = {'category': 'c1'}

    response = client.get('/todos', query_string=query)
    assert response.status_code == 200

    assert response.get_json() == {'data': [{'description':'d1', 'category':'c1'}]}


def test_add_item_succeeds():
    todo_list = TodoList()
    app = create_app(todo_list)

    app.config['TESTING'] = True
    client = app.test_client()

    response = client.post('/add', data={'description': 'd1', 'category': 'c1'})
    assert response.status_code == 200
    assert response.data == b''


def test_add_category_required():
    todo_list = TodoList()
    app = create_app(todo_list)

    app.config['TESTING'] = True
    client = app.test_client()

    response = client.post('/add', data={'description': 'd1'})
    assert response.status_code == 400

    assert response.data == b'Missing category'


def test_add_description_required():
    todo_list = TodoList()
    app = create_app(todo_list)

    app.config['TESTING'] = True
    client = app.test_client()

    response = client.post('/add', data={'category': 'c1'})
    assert response.status_code == 400
    assert response.data == b'Missing description'
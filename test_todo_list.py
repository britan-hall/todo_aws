
from todo_list import TodoList, TodoItem, DuplicateException, NoSuchItemException
import pytest


def test_new_list_is_empty():
    todo_list = TodoList()
    assert todo_list.get_list() == []


def test_item_retained():
    todo_list = TodoList()
    todo_list.add('homework', 'school')
    assert todo_list.contains('homework', 'school')
    assert TodoItem('homework', 'school') in todo_list.get_list()


def test_get_filtered_by_category():
    todo_list = TodoList()
    todo_list.add('homework', 'school')
    todo_list.add('mow grass', 'home')
    results = todo_list.get_list(category='home')
    assert len(results) == 1
    assert TodoItem('mow grass', 'home') in results


def test_filter_removes_all():
    todo_list = TodoList()
    todo_list.add('homework', 'school')
    todo_list.add('mow grass', 'home')
    results = todo_list.get_list(category='hobby')
    assert len(results) == 0


def test_remove_present_item():
    todo_list = TodoList()
    todo_list.add('homework', 'school')
    todo_list.add('mow grass', 'home')
    todo_list.remove('homework', 'school')
    results = todo_list.get_list()
    assert len(results) == 1
    assert TodoItem('mow grass', 'home') in results
    assert todo_list.contains('homework', 'school') is False


def test_remove_missing_item():
    todo_list = TodoList()
    with pytest.raises(NoSuchItemException):
        todo_list.remove('not', 'present')


def test_duplicate_not_allowed():
    todo_list = TodoList()
    todo_list.add('homework', 'school')

    with pytest.raises(DuplicateException):
        todo_list.add('homework', 'school')
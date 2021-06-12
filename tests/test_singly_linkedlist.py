# pylint: disable=missing-function-docstring,redefined-outer-name,
# pylint: disable=protected-access,missing-module-docstring
import pytest
from singly_linkedlist.singly_linkedlist import Node, \
    SinglyLinkedList, SinglyLinkedListException, SinglyLinkedListIndexError, \
    SinglyLinkedListEmptyError


# return an empty linked list
@pytest.fixture
def test_linkedlist():
    return SinglyLinkedList()


def test_node_data():
    node = Node('A')
    assert node.data == 'A'


def test_node_next():
    node = Node('A')
    assert node.next is None


def test_insert_head_empty_list_1(test_linkedlist):
    """Insert data into an empty linked list."""
    test_linkedlist.insert_head('A')
    assert test_linkedlist.head.data == 'A'


def test_insert_head_empty_list_2(test_linkedlist):
    """
    Insert data into an empty linked list
    and check whether header node's next has None
    """
    test_linkedlist.insert_head('A')
    assert test_linkedlist.head.next is None


def test_insert_head_one_element_list_1(test_linkedlist):
    """
    Insert head element to a single element linked list
    and check whether header node has expected data.
    """
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_head('B')
    assert test_linkedlist.head.data == 'B'


def test_insert_head_one_element_list_2(test_linkedlist):
    """
    Insert head element to a single element linked list
    and check whether header node.next points to second element
    """
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_head('B')
    assert test_linkedlist.head.next.data == 'A'


def test_insert_head_for_two_element_list_1(test_linkedlist):
    """
    Insert head element to a two element linked list
    and check whether header node has expected data.
    """
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_head('B')
    test_linkedlist.insert_head('C')
    assert test_linkedlist.head.data == 'C'


# capfd - capturefd is a built-in pytest fixture to capture
# stdout, stderr using file descriptor method
def test_print_elements_empty_list(test_linkedlist, capfd):
    # print to stdout
    test_linkedlist.print_elements()
    # capture stdout
    out, _ = capfd.readouterr()
    assert out == "\nThe list is empty!\n"


def test_print_elements_one_element_list(test_linkedlist, capfd):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    test_linkedlist.print_elements()
    out, _ = capfd.readouterr()
    assert out == "\nA\nB\n"


def test_print_elements_two_element_list(test_linkedlist, capfd):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    test_linkedlist.insert_at('C', 2)
    test_linkedlist.print_elements()
    out, _ = capfd.readouterr()
    assert out == "\nA\nB\nC\n"


def test_insert_end_for_empty_list(test_linkedlist):
    """
    Insert last element to an empty element linked list
    and check whether header node has expected data
    """
    test_linkedlist.insert_end('A')
    assert test_linkedlist.head.data == 'A'


def test_insert_end_for_one_element_list(test_linkedlist):
    """
    Insert last element to a single element linked list
    and check whether the last node has expected data
    """
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    assert test_linkedlist.head.data == 'A'


def test_length_for_empty_linked_list(test_linkedlist):
    assert test_linkedlist.list_length() == 0


def test_length_for_non_empty_linked_list(test_linkedlist):
    test_linkedlist.insert_end('A')
    assert test_linkedlist.list_length() == 1


def test_insert_at_negetive_index_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListIndexError):
        test_linkedlist.insert_at('B', -1)


def test_insert_at_index_greater_than_list_length_exception(test_linkedlist):
    test_linkedlist.insert_head('A')
    # or below base class will also work
    # with pytest.raises(SinglyLinkedListException) as excinfo:
    with pytest.raises(SinglyLinkedListIndexError) as excinfo:
        test_linkedlist.insert_at('B', 2)
    assert str(excinfo.value) == ("Unable to insert at index 2"
                                  " : Invalid Position")


def test_insert_at_empty_list(test_linkedlist):
    test_linkedlist.insert_at('A', 0)
    assert test_linkedlist.head.data == 'A'


def test_insert_at_one_element_list_pos_0(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 0)
    assert test_linkedlist.head.data == 'B'


def test_insert_at_one_element_list_pos_1(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    assert test_linkedlist.head.next.data == 'B'


def test_insert_at_out_of_range_index_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListException):
        test_linkedlist.insert_at('A', 1)


def test_insert_at_negative_index_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListException):
        test_linkedlist.insert_at('A', -1)


def test_delete_end_empty_list_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListEmptyError) as excinfo:
        test_linkedlist.delete_end()
    assert str(excinfo.value) == ("Unable to delete "
                                  "from empty list")


def test_delete_end_one_element_list(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.delete_end()
    assert test_linkedlist.head is None


def test_delete_end_two_element_list_head_data(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    test_linkedlist.delete_end()
    assert test_linkedlist.head.data == 'A'


def test_delete_end_two_element_list_head_next(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    test_linkedlist.delete_end()
    assert test_linkedlist.head.next is None


def test_delete_head_empty_linked_list(test_linkedlist):
    with pytest.raises(SinglyLinkedListEmptyError) as execinfo:
        test_linkedlist.delete_head()
    assert str(execinfo.value) == ("Unable to delete head from"
                                   " empty linked list")


def test_delete_head_one_element_linked_list(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.delete_head()
    assert test_linkedlist.head is None


def test_delete_head_two_element_linked_list(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    test_linkedlist.delete_head()
    assert test_linkedlist.head.data == 'B'


def test_delete_at_empty_list(test_linkedlist):
    with pytest.raises(SinglyLinkedListEmptyError) as execinfo:
        test_linkedlist.delete_at(0)
    assert str(execinfo.value) == ("Unable to delete head from"
                                   " empty linked list")


def test_delete_at_negative_index(test_linkedlist):
    test_linkedlist.insert_head('A')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        test_linkedlist.delete_at(-1)
    assert str(execinfo.value) == "Index cannot be negative"


def test_delete_at_index_greater_than_list_length(test_linkedlist):
    test_linkedlist.insert_head('A')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        test_linkedlist.delete_at(1)
    assert str(execinfo.value) == ("Index=1 is out of range for"
                                   " list length=1")


def test_delete_at_delete_head(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.delete_at(0)
    assert test_linkedlist.head is None


def test_delete_at_delete_end(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    test_linkedlist.delete_at(1)
    assert test_linkedlist.head.next is None


def test_delete_at_four_element_list_index_two(test_linkedlist):
    test_linkedlist.insert_head('A')
    test_linkedlist.insert_at('B', 1)
    test_linkedlist.insert_at('C', 2)
    test_linkedlist.insert_at('D', 3)
    test_linkedlist.delete_at(2)
    second_element = test_linkedlist.head.next
    third_element = second_element.next
    assert third_element.data == 'D'


# __get_cycle_meet_node() private method in class becomes
# _SinglyLinkedList__get_cycle_meet_node()
def test__get_cycle_meet_node_empty_list_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListException) as execinfo:
        test_linkedlist._SinglyLinkedList__get_cycle_meet_node()
    assert str(execinfo.value) == "Empty linked list"


def test__get_cycle_meet_node_one_element_list_none(test_linkedlist):
    test_linkedlist.insert_head('A')
    assert test_linkedlist._SinglyLinkedList__get_cycle_meet_node() is None


def test__get_cycle_meet_node_two_element_list_none(test_linkedlist):
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    assert test_linkedlist._SinglyLinkedList__get_cycle_meet_node() is None


def test__get_cycle_meet_node_two_element_list_true(test_linkedlist):
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    # create a cycle/loop
    test_linkedlist.head.next.next = test_linkedlist.head
    assert test_linkedlist._SinglyLinkedList__get_cycle_meet_node() \
           is test_linkedlist.head


def test_cycle_present_false(test_linkedlist):
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    test_linkedlist.insert_end('C')
    # assert cycle_present() function returns False
    assert not test_linkedlist.cycle_present()


def test_cycle_present_true(test_linkedlist):
    """
    Create a 3 element linked list with a cycle
    and test whether cycle_present() function detects it
    """
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    test_linkedlist.insert_end('C')
    # create a cycle - connection from 3rd to 2nd element
    test_linkedlist.head.next.next.next = test_linkedlist.head.next
    # assert cycle_present() function returns True
    assert test_linkedlist.cycle_present()


def test_remove_cycle_no_cycle(test_linkedlist):
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    test_linkedlist.remove_cycle()
    assert test_linkedlist.head.next.next is None


def test_remove_cycle_circular_linkedlist(test_linkedlist):
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    test_linkedlist.insert_end('C')
    # create a cycle - connection from 3rd to 1st element
    test_linkedlist.head.next.next.next = test_linkedlist.head
    test_linkedlist.remove_cycle()
    assert test_linkedlist.head.next.next.next is None


def test_remove_cycle(test_linkedlist):
    char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    for i in char_list:
        test_linkedlist.insert_end(i)
    last_node = test_linkedlist.head
    while last_node.next is not None:
        if last_node.data == 'E':
            fifth_element = last_node
        last_node = last_node.next
    # create a cycle - connection from last to fifth element
    last_node.next = fifth_element
    test_linkedlist.remove_cycle()
    last_node = test_linkedlist.head
    while last_node.next is not None:
        last_node = last_node.next
    assert last_node.next is None


def test_get_node_at_index_empty_list_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListEmptyError) as execinfo:
        _ = test_linkedlist.get_node_at_index(0)
    assert str(execinfo.value) == "Empty linked list"


def test_get_node_at_index_negative_index_exception(test_linkedlist):
    test_linkedlist.insert_end('A')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        _ = test_linkedlist.get_node_at_index(-1)
    assert str(execinfo.value) == "Index out of range: -1"


def test_get_node_at_index_out_of_range_index_exception(test_linkedlist):
    test_linkedlist.insert_end('A')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        _ = test_linkedlist.get_node_at_index(1)
    assert str(execinfo.value) == ("Index=1 out of range for "
                                   "list length=1")


def test__check_indices_for_swap_empty_list(test_linkedlist):
    with pytest.raises(SinglyLinkedListException) as execinfo:
        test_linkedlist._SinglyLinkedList__check_indices_for_swap(0, 0)
    assert str(execinfo.value) == "Empty linked list"


def test__check_indices_for_swap_negative_index1(test_linkedlist):
    test_linkedlist.insert_end('A')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        test_linkedlist._SinglyLinkedList__check_indices_for_swap(-1, 0)
    assert str(execinfo.value) == "Invalid index: -1"


def test__check_indices_for_swap_negative_index2(test_linkedlist):
    test_linkedlist.insert_end('B')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        test_linkedlist._SinglyLinkedList__check_indices_for_swap(0, -2)
    assert str(execinfo.value) == "Invalid index: -2"


def test__check_indices_for_swap_out_of_range_index1(test_linkedlist):
    test_linkedlist.insert_end('A')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        test_linkedlist._SinglyLinkedList__check_indices_for_swap(1, 0)
    assert str(execinfo.value) == ("Index=1 out of range for"
                                   " list length=1")


def test__check_indices_for_swap_out_of_range_index2(test_linkedlist):
    test_linkedlist.insert_end('B')
    with pytest.raises(SinglyLinkedListIndexError) as execinfo:
        test_linkedlist._SinglyLinkedList__check_indices_for_swap(0, 2)
    assert str(execinfo.value) == ("Index=2 out of range for"
                                   " list length=1")


def test_swap_nodes_empty_linkedlist(test_linkedlist):
    with pytest.raises(SinglyLinkedListException):
        test_linkedlist.swap_nodes_at_indices(1, 2)


def test_swap_nodes_negetive_index1_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListException):
        test_linkedlist.swap_nodes_at_indices(-1, 2)


def test_swap_nodes_negetive_index2_exception(test_linkedlist):
    with pytest.raises(SinglyLinkedListException):
        test_linkedlist.swap_nodes_at_indices(1, -2)


def test_swap_nodes_out_of_range_index1_exception(test_linkedlist):
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    with pytest.raises(SinglyLinkedListException):
        test_linkedlist.swap_nodes_at_indices(2, 0)


def test_swap_nodes_out_of_range_index2_exception(test_linkedlist):
    test_linkedlist.insert_end('A')
    test_linkedlist.insert_end('B')
    with pytest.raises(SinglyLinkedListException):
        test_linkedlist.swap_nodes_at_indices(0, 2)

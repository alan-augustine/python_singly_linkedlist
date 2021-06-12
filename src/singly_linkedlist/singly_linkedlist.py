"""Singly linked list. """


class SinglyLinkedListException(Exception):
    """ Base class for linked list module.
        This will make it easier for future modifications
    """


class SinglyLinkedListIndexError(SinglyLinkedListException):
    """ Invalid/Out of range index"""
    def __init__(self, message="linked list index out of range"):
        super().__init__(message)
        self.message = message


class SinglyLinkedListEmptyError(SinglyLinkedListException):
    """ Empty Linked List"""
    def __init__(self, message="linked list has no nodes"):
        super().__init__(message)
        self.message = message


class Node:                # pylint: disable=too-few-public-methods
    """Class representing a node in a linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """Linked list class representing a collection of linked nodes"""
    def __init__(self):
        self.head = None

    def insert_head(self, data):
        """ Insert an node at the begenning of the linked list"""
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head = new_node
        else:
            self.head = new_node

    def insert_end(self, data):
        """Insert an element at the end of the linked list"""
        # create a new node
        new_node = Node(data)
        # if SinglyLinkedList is not empty or if head exists, iterate and
        # link the newly created node with current last node
        if self.head:
            # start with first node and then iterate
            last_node = self.head
            # 'next' will be empty for current last node
            while last_node.next:
                last_node = last_node.next
            # link current last node with newly created node
            last_node.next = new_node
        else:
            # if list is empty
            self.head = new_node

    def insert_at(self, data, index):
        """ Insert a node at the specified index starting from 0"""
        if index < 0 or index > self.list_length():
            raise SinglyLinkedListIndexError("Unable to insert at index " +
                                             str(index) +
                                             " : Invalid Position")
        if index == 0:
            self.insert_head(data)
        else:
            current_node = self.head
            new_node = Node(data)
            i = 1
            while i < index:
                current_node = current_node.next
                i += 1
            temp = current_node.next
            current_node.next = new_node
            new_node.next = temp
            del temp

    def delete_end(self):
        """ Delete a node from the end of linked list"""
        if not self.head:
            raise SinglyLinkedListEmptyError("Unable to delete "
                                             "from empty list")
        if self.head.next is None:
            self.head = None
        else:
            # get last node and delete it
            # (remove all references to that object)
            current_node = self.head
            previous_node = None
            while current_node.next is not None:
                previous_node = current_node
                current_node = current_node.next
            del current_node
            previous_node.next = None

    def delete_head(self):
        """Remove the first node of the linked list"""
        if self.head is None:
            raise SinglyLinkedListEmptyError("Unable to delete head from"
                                             " empty linked list")
        # if only one element
        if self.head.next is None:
            self.head = None
        else:
            self.head = self.head.next

    # index starts at 0
    def delete_at(self, index):
        """Remove the node at the specified index(starting from 0)
           from the linked list
        """
        if self.head is None:
            raise SinglyLinkedListEmptyError("Unable to delete head from"
                                             " empty linked list")
        if index < 0:
            raise SinglyLinkedListIndexError("Index cannot be negative")
        if index >= self.list_length():
            raise SinglyLinkedListIndexError("Index={0} is out of range"
                                             " for list length={1}"
                                             .format(index,
                                                     self.list_length()
                                                     )
                                             )
        if index == 0:
            self.delete_head()
        # index starts at 0
        elif index == self.list_length() - 1:
            self.delete_end()
        else:
            i = 1
            current_node = self.head
            previous_node = None
            while i <= index:
                previous_node = current_node
                current_node = current_node.next
                i += 1
            previous_node.next = current_node.next
            del current_node

    def print_elements(self):
        """Print data in all nodes in the linked list"""
        print('')
        if self.head:
            current_node = self.head
            while current_node:
                print(current_node.data)
                if current_node.next:
                    current_node = current_node.next
                else:
                    break
        else:
            print("The list is empty!")

    def list_length(self):
        """Returns the number of nodes in the linked list"""
        length = 0
        current_node = self.head
        while current_node is not None:
            length += 1
            current_node = current_node.next
        return length

    def __get_cycle_meet_node(self):
        """
        Return Node where slow(Tortoise or t) and fast(Hare or h) pointers meet
        (Floyd's cycle detection algorithm)
        If no cycle, return None
        """
        if self.head is None:
            raise SinglyLinkedListEmptyError("Empty linked list")
        # single element linkedlist with 'next' None cannot have a cycle
        if self.head.next is None:
            return None

        hare = tortoise = self.head
        while (tortoise is not None) and (tortoise.next is not None):
            hare = hare.next
            tortoise = tortoise.next.next
            if hare is tortoise:
                return hare
        # if no meeting node in the linkedlist, return None
        return None

    def cycle_present(self):
        """Return True is a cycle is detected in the linked list,
        else retruns False
        """
        return bool(self.__get_cycle_meet_node())

    # TODO: get cycle start node
    def remove_cycle(self):
        """Removes cycle(if present in the linked list"""
        if self.cycle_present():
            # Floyd's cycle detection algorithm - to find starting
            # index of cycle. Point Hare to element at cycle_meet_index
            # and Tortoise to head element and move them at same speed
            tortoise = self.head
            hare = self.__get_cycle_meet_node()

            # For circular linked list(special case of linkedlist),
            #  hare = meeting_node = head = tortoise
            # For this edge case, the second while loop will not get executed
            # So, get last element of linkedlist and set it as initial
            #  value of previous_hare
            if hare is self.head:
                previous_hare = self.head
                while previous_hare.next is not self.head:
                    previous_hare = previous_hare.next

            while hare is not tortoise:
                previous_hare = hare
                tortoise = tortoise.next
                hare = hare.next
            # at this point, hare = tortoise = cycle start node
            # remove the cycle by setting next pointer of last element to None
            previous_hare.next = None

        else:
            pass

    def get_node_at_index(self, index):
        """Return node at specified index, starting from 0"""
        if self.head is None:
            raise SinglyLinkedListEmptyError("Empty linked list")
        if index < 0:
            raise SinglyLinkedListIndexError("Index out of range: "
                                             "{0}".format(index))
        if index >= self.list_length():
            raise SinglyLinkedListIndexError("Index={0} out of range for "
                                             "list length={1}"
                                             .format(index,
                                                     self.list_length())
                                             )
        current_node = self.head
        i = 0
        while i < index:
            current_node = current_node.next
            i += i
        return current_node

    def __check_indices_for_swap(self, index1, index2):
        """ Sanity checks for function swap_nodes_at_indices.
            This to avoid pylint error R0912 for
            function swap_nodes_at_indices().
            R0912: Too many branches (17/12) (too-many-branches).
        """
        if self.head is None:
            raise SinglyLinkedListEmptyError("Empty linked list")
        if index1 < 0:
            raise SinglyLinkedListIndexError("Invalid index: {0}"
                                             .format(index1))
        if index2 < 0:
            raise SinglyLinkedListIndexError("Invalid index: {0}"
                                             .format(index2))
        if index1 >= self.list_length():
            raise SinglyLinkedListIndexError("Index={0} out of range for"
                                             " list length={1}"
                                             .format(index1,
                                                     self.list_length())
                                             )
        if index2 >= self.list_length():
            raise SinglyLinkedListIndexError("Index={0} out of range for"
                                             " list length={1}"
                                             .format(index2,
                                                     self.list_length())
                                             )

    # TODO: write a function to check if list is empty and throw exception
    # TODO: different exception classses for different edge cases
    def swap_nodes_at_indices(self, index1, index2):
        """Swaps two nodes (specified using indices) of the linked list.
           Retrun True, if swap success or if swap not required
        """
        # if both indices are same, no need to swap
        if index1 == index2:
            return True

        # if only one element
        if self.head and self.head.next is None:
            return True

        self.__check_indices_for_swap(index1, index2)

        # ensure index2 > index1 , as an internal standard in this function
        if index1 > index2:
            index1, index2 = index2, index1

        # Get elements to be swapped in one pass/loop.
        # Since we need to update the links, also get nodes
        # just before the nodes to be swapped
        node1 = self.head
        prev_node1 = None  # node just before node1
        node2 = self.head
        prev_node2 = None  # node just before node2
        current_node = self.head
        i = j = 0
        while j <= index2:  # index2 >= index1, so iterate till index2
            if i == index1 - 1:
                prev_node1 = current_node
            if j == index2 - 1:
                prev_node2 = current_node
                break
            current_node = current_node.next
            i += 1
            j += 1

        if prev_node1:  # to handle edge case node1=self.head
            node1 = prev_node1.next
        if prev_node2:  # to handle edge case node2=self.head
            node2 = prev_node2.next

        if prev_node1:
            prev_node1.next = node2
        else:
            self.head = node2  # to handle edge case node1=self.head
        if prev_node2:
            prev_node2.next = node1
        else:
            self.head = node1  # to handle edge case node2=self.head

        node1.next, node2.next = node2.next, node1.next


if __name__ == '__main__':
    pass

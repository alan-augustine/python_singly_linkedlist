from time import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from singly_linkedlist.singly_linkedlist import SinglyLinkedList

start = time()
linked_list = SinglyLinkedList()
for i in range(100000):
    linked_list.insert_head(111111111111)
end = time()
print("Took {0} seconds".format(start-end))
# linked_list.print_elements()


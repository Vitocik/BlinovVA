# main.py
from binary_search_tree import BinarySearchTree
import tree_traversal as trav


def main():
    values = [50, 30, 70, 20, 40, 60, 80]
    bst = BinarySearchTree()
    for v in values:
        bst.insert(v)

    print("Tree visualization (indented):")
    print(bst.visualize())

    print("Bracket repr:")
    print(bst.bracket_repr())

    print("In-order (should be sorted):", trav.inorder_recursive(bst.root))
    print("Pre-order:", trav.preorder_recursive(bst.root))
    print("Post-order:", trav.postorder_recursive(bst.root))
    print("In-order (iterative):", trav.inorder_iterative(bst.root))

    print("Search 40 ->", bst.search(40))
    print("Search 99 ->", bst.search(99))

    print("Is valid BST?", bst.is_valid_bst())

    print("Find min:", bst.find_min().value)
    print("Find max:", bst.find_max().value)

    print("Height:", bst.height())

    print("\nDeleting 30 (node with two children), then show in-order:")
    bst.delete(30)
    print("In-order after delete:", trav.inorder_recursive(bst.root))


if __name__ == "__main__":
    main()

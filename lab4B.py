# method that prints all anagrams from a given word.
def print_anagrams(word, english_words, prefix=""):
   if len(word) <= 1:
       str = prefix + word
       # searches for word in english_words data structure, if the word if found then it exists.
       if english_words.find(str) is True:
           print(prefix + word)
   else:
       # creates different combinations of the word and search if its an actual word.
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur

           if cur not in before: # Check if permutations of cur have not been generated.
               print_anagrams(before + after, english_words, prefix + cur)

# method that gives the total number of anagrams a word has.
# same as printing_anagrams method but instead of printing it return value.
def count_anagrams(word, english_words, prefix=""):
   count = 0
   if len(word) <= 1:
       str = prefix + word

       if english_words.find(str) is True:
           return 1
   else:
       for i in range(len(word)):
           cur = word[i: i + 1]
           before = word[0: i] # letters before cur
           after = word[i + 1:] # letters after cur

           if cur not in before: # Check if permutations of cur have not been generated.
               count += count_anagrams(before + after, english_words, prefix + cur)
   return count

# given a file, max_anagrams find the word that has the most anagrams.              
def max_anagrams(english_words):
    print("input the text file name")
    file = open(input())
    max_word = None
    for word in file:
        if max_word is None:
            max_word = word.rstrip()
        # compares the number of anagrams from each word and returns the word that has the most anagrams.
        elif count_anagrams(word.rstrip(), english_words) > count_anagrams(max_word, english_words):
            max_word = word.rstrip()
    return max_word

class BTreeNode:
    
    def __init__(self, keys=[], children=[], is_leaf=True, max_num_keys=5):
        self.keys = keys
        self.children = children
        self.is_leaf = is_leaf
        if max_num_keys < 3:
            max_num_keys = 3
        if max_num_keys % 2 == 0:
            max_num_keys += 1
        self.max_num_keys = max_num_keys

class BTree:

    def __init__(self, max_num_keys=5):
        self.max_num_keys = max_num_keys
        self.root = BTreeNode(max_num_keys=max_num_keys)
        
    def insert(self, item, node=None):
        if node is None:
            node = self.root
        # list is full then divide list into three the middle (middle key) and left (list of items less than key) and 
        # right children (list of items greater than key).
        if len(node.keys) >= node.max_num_keys:
            m, l, r = self.split(node)
            node.keys = [m]
            node.children = [l, r]
            node.is_leaf = False
            k = self.find_child(item, node)
            self.insert_internal(item, node.children[k])
        # if list is not full, insert item in the list.
        else:
            self.insert_internal(item, node)
            
    def insert_internal(self, item, node=None):
        if node is None:
            node = self.root
        # leafs are not full therefore we may always insert the item.
        if node.is_leaf:
            self.insert_leaf(item, node)
        # Determine the location where key must be inserted.
        else:
            k = self.find_child(item, node)
            # if list is full split.
            if len(node.children[k].keys) >= node.children[k].max_num_keys:
                m, l, r = self.split(node.children[k])
                node.keys.insert(k, m)
                node.children[k] = l
                node.children.insert(k + 1, r)
                k = self.find_child(item, node)
            self.insert_internal(item, node.children[k])
            
    def insert_leaf(self, item, node=None):
        if node is None:
            node = self.root
        # insert the item in the list located in the leaf of the tree then sort content.
        node.keys.append(item)
        node.keys.sort()
        
    # divide the node into three, the middle key and the left and right child of that key.
    def split(self, node=None):
        if node is None:
            node = self.root
        mid = node.max_num_keys // 2
        if node.is_leaf:
            left_child = BTreeNode(node.keys[:mid], max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], max_num_keys=node.max_num_keys)
        else:
            left_child = BTreeNode(node.keys[:mid], node.children[:mid + 1], node.is_leaf, max_num_keys=node.max_num_keys)
            right_child = BTreeNode(node.keys[mid + 1:], node.children[mid + 1:], node.is_leaf, max_num_keys=node.max_num_keys)
        return node.keys[mid], left_child, right_child

    # finds the index of a child where the key belongs.
    def find_child(self, key, node=None):
        if node is None:
            node = self.root
        # gets the index where keys of a node are greater than the key.
        for i in range(len(node.keys)):
            if key < node.keys[i]:
                return i
        return len(node.keys)
            
    # finds key in the B-Tree.
    def find(self, key, node=None):
        if node is None:
            node = self.root
        # if key is in list return true
        if key in node.keys:
            return True
        # node is a leaf then theres nothing in the node and we reach the end of the tree.
        if node.is_leaf:
            return False
        return self.find(key, node.children[self.find_child(key, node)])
        
def main():
    word_file = open("words.txt", "r")
    english_words = BTree(5)
    # insert each word from the file in the B-Tree.
    for word in word_file:
        english_words.insert(word.lower().rstrip())
    print("Input 1 : print and count number of anagrams")
    print("Input 2 : find word with max anagrams from a file")
    option = int(input())
    if option == 1:
        print("input any word for anagram")
        word = input()
        print_anagrams(word, english_words)
        print(count_anagrams(word, english_words))
    elif option == 2:
        print(max_anagrams(english_words))
    
main()
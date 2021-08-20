import functools
from typing import Iterable, Any

from types_extensions import void, const, _assert_py_version, PythonVersion

_assert_py_version(PythonVersion(3, 10))


class _TrieNode:
    """
    Do not use this class directly.
    self.complete = Does this Node correspond to a word?
    self.size = Number of all completed words downstream. Size should never be 0.
    TODO: Weighed nodes/weighed trie
    """

    default_charset = r'abcdefghijklmnopqrstuvwxyz!@#$%^&*()-_1234567890=+[{]}\|;:\'"<,>./?`~'

    def __init__(self, character: str, charset: str | Iterable[str]) -> void:

        self.charset: set[str] = iterable_to_set(charset or self.default_charset)
        self.character: const(str) = character
        self.children: dict[str, _TrieNode] = {}
        self.size: int = 0
        self.complete: bool = False

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def insert(self, partial: str) -> void:
        first_letter = partial[0]
        if first_letter not in self.charset:
            raise InvalidCharacterException(first_letter, self.charset)
        if first_letter not in self.children:
            node = _TrieNode(character=first_letter, charset=self.charset)
            self.children[first_letter] = node
            setattr(self, first_letter, node)
        else:
            node = self.children[first_letter]
        match len(partial):
            case x if x > 1:
                new_partial = partial[1:]
                node.insert(partial=new_partial)
            case x if x == 1:
                node._set_complete()
        self.size += 1

    def _set_complete(self) -> void:
        if not self.complete:
            self.size += 1
            self.complete = True

    def _invalidate(self) -> void:
        if self.complete:
            self.size -= 1
            self.complete = False

    def search(self, word: str, index: int) -> list[str]:
        rv = []
        if len(word) <= index + 1:
            if self.complete:
                rv.append(word)
            for node in self.children.values():
                rv.extend(node.search(word + node.character, index + 1))
        else:
            if (next_letter := word[index + 1]) in self.children:
                rv.extend(self.children[next_letter].search(word, index + 1))

        return rv

    def delete(self, partial: str, delete_downstream: bool) -> bool:
        if len(partial) == 0:
            if self.complete:
                if not self.is_leaf:
                    self._invalidate()
                return True
            return False
        first_letter = partial[0]
        if first_letter in self.children:
            node = self.children[first_letter]
            downstream_result = node.delete(partial=partial[1:], delete_downstream=delete_downstream)
            if downstream_result:
                if node.is_leaf or delete_downstream:
                    del self.children[first_letter]
                self.size -= 1
            return downstream_result
        return False

    def __str__(self) -> str:
        return f"TrieNode(<{self.character}>, complete={self.complete}, is_leaf={self.is_leaf})"

    def __repr__(self) -> str:
        return str(self)


class Trie:
    """
    Trie structure which is an unbalanced multi-branch tree of characters which make up words.
    Searching a trie for a word is O(k) where k is the length of the word being searched.

    Individual nodes can be reached by either going over each dict one by one or by using properties_and_methods
    Eg: To get the node at the "i" in "hi" in Trie trie_ (assuming you know the h and i nodes exist):
    >>> i_node = trie_.heads.get('h').get('i')
    >>> i_node = trie_.h.i

    """

    default_charset = 'abcdefghijklmnopqrstuvwxyz1234567890'

    def __init__(self, trie_charset: str | Iterable[str] = None, node_charset: str | Iterable[str] = None) -> void:
        self.charset: set[str] = iterable_to_set(trie_charset or self.default_charset)
        self.heads: dict[str, _TrieNode] = {}
        self._node_charset: str | Iterable[str] = node_charset
        self.size: int = 0

    def __setattr__(self, key: str, value: Any) -> void:
        if len(key) == 1 and key in self.charset and not isinstance(value, _TrieNode):
            # Setting single char properties_and_methods is forbidden unless you're setting it to a node
            raise ReservedAttributeException(key)
        super().__setattr__(key, value)

    def insert(self, word: str) -> void:
        """
        Add a new word to the trie. See _TrieNode.insert() for more details on how each letter floats down.
        The Trie itself will only have a reference to the first character of the word in self.heads

        :param word: The word to insert
        """
        if len(word) == 0:
            raise EmptyInputException

        word = word.casefold()
        first_letter = word[0]
        if first_letter not in self.charset:
            raise InvalidCharacterException(first_letter, self.charset)
        if first_letter not in self.heads:
            node = _TrieNode(character=first_letter, charset=self._node_charset)
            self.heads[first_letter] = node
            setattr(self, first_letter, node)
        else:
            node = self.heads[first_letter]
        if len(word) > 1:
            new_partial = word[1:]
            node.insert(partial=new_partial)
        self.search.cache_clear()
        self.size += 1

    @functools.cache
    def search(self, word: str, insert_if_missing: bool = False, max_results: int = None) -> list[str]:
        """
        Looks for a word (complete or partly complete). It will return a list of the word (if it exists and is
        complete), as well as ALL downstream results if max_results isn't set. For now, results are ordered in the
        way thay are found.

        Searches are cached in until the insert() or delete() methods are called.

        :param word: The word or word partial to search for
        :param insert_if_missing: If the word is missing, insert it for next time. (Maybe don't do this for partials)
        :param max_results: The trie has no weights so the first found results are given. Leave blank for all results
        :return: A list of results
        """
        if len(word) == 0:
            raise EmptyInputException

        word = word.casefold()
        first_letter = word[0]
        if first_letter not in self.heads:
            if insert_if_missing:
                self.insert(word)
            return []
        results = self.heads[first_letter].search(word, 0)
        if len(results) == 0 and insert_if_missing:
            self.insert(word)
        if not max_results or len(results) <= max_results:
            return results
        return results[:max_results]

    def delete(self, word: str, delete_downstream: bool = False) -> bool:
        """
        Delete a word from the trie. Can be used to trim entire branches with cascading deletes.
        Invalidates search cache only upon successful delete.

        :param word: The word to delete
        :param delete_downstream: Dangerous! Will delete the node, even if it has children!
        :return: True if the word existed and was deleted, else False
        """
        if len(word) == 0:
            raise EmptyInputException

        word = word.casefold()
        first_letter = word[0]
        if first_letter not in self.heads:
            return False
        new_partial = word[1:]
        rv = self.heads[first_letter].delete(partial=new_partial, delete_downstream=delete_downstream)
        if rv:
            self.size -= 1
            self.search.cache_clear()
        return rv

    def exists(self, word: str) -> bool:
        """
        Does a word exist? (Partials not matched)
        """
        if len(word) == 0:
            raise EmptyInputException
        word = word.casefold()
        first_letter = word[0]
        if first_letter not in self.heads:
            return False
        node = self.heads[first_letter]
        for letter in word[1:]:
            node = getattr(node, letter, void)
            if not node:
                return False
        return node.complete


def iterable_to_set(charset: Iterable[str]) -> set[str]:
    rv = set()
    for value in charset:
        if len(value) == 1:
            rv.add(value.casefold())
        else:
            for char_ in value:
                rv.add(char_.casefold())
    return rv


class InvalidCharacterException(Exception):

    def __init__(self, character: str, allowed_charset: str | Iterable[str]) -> void:
        self.character: const(str) = character
        self.allowed_charset: const(str) = allowed_charset

    def __str__(self) -> str:
        message = f"Invalid character detected in input string {self.character}." \
                  f"The allowed characters are:\n{self.allowed_charset}"
        return message


class EmptyInputException(Exception):

    def __str__(self) -> str:
        message = f"The given string should be at least one character long"
        return message


class ReservedAttributeException(Exception):

    def __init__(self, character: str) -> void:
        self.char: const(str) = character

    def __str__(self) -> str:
        message = f"The attribute {self.char} is reserved for this class."
        return message

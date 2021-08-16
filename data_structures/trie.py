import functools
from typing import Iterable, Any

from types_extensions import void, const


class _TrieNode:

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

    default_charset = 'abcdefghijklmnopqrstuvwxyz1234567890'

    def __init__(self, trie_charset: str | Iterable[str] = void, node_charset: str | Iterable[str] = void) -> void:
        self.charset: set[str] = iterable_to_set(trie_charset or self.default_charset)
        self.heads: dict[str, _TrieNode] = {}
        self._node_charset: str | Iterable[str] = node_charset
        self.size: int = 0

    def __setattr__(self, key: str, value: Any) -> void:
        if len(key) == 1 and key in self.charset and not isinstance(value, _TrieNode):
            raise ReservedAttributeException(key)
        super().__setattr__(key, value)

    def insert(self, word: str) -> void:
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
    def search(self, word: str, insert_if_missing: bool = False) -> list[str]:
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
        return results

    def delete(self, word: str, delete_downstream: bool = False) -> void:
        if len(word) == 0:
            raise EmptyInputException

        word = word.casefold()
        first_letter = word[0]
        if first_letter not in self.heads:
            return void
        new_partial = word[1:]
        rv = self.heads[first_letter].delete(partial=new_partial, delete_downstream=delete_downstream)
        if rv:
            self.size -= 1
            self.search.cache_clear()
        return rv

    def exists(self, word: str) -> bool:
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

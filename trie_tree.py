import pygtrie


class Entity:

    def __init__(self, key, value, begin):
        self.key = key
        self.value = value
        self.begin = begin

    def __repr__(self):
        return f'<Entity {self.key} {self.value} {self.begin}>'


class TrieTree:

    def __init__(self, word2type_dict):
        self.char_trie = pygtrie.CharTrie()
        for key, value in word2type_dict.items():
            self.char_trie[key] = value

    def get_match_entity(self, query):
        results = []
        position = 0
        while position < len(query):
            sub_query = query[position:]
            longest_entity = self.char_trie.longest_prefix(sub_query)
            if longest_entity:
                results.append(Entity(longest_entity.value, longest_entity.key, position))
                position += len(longest_entity.key)
            else:
                position += 1
        return results

    def replace_entity(self, query):
        entity_list = self.get_match_entity(query)
        result = ""
        last_end = 0
        for entity in entity_list:
            result += query[last_end:entity.begin] + f"#{entity.key}#"
            last_end = entity.begin + len(entity.value)
        result += query[last_end:]
        return result


if __name__ == '__main__':
    dictset = {"平安": "平安银行", "你们银行": "平安银行", "农村商业银行": "农商银行"}
    query = "我想了解一下你们银行，你觉得农村商业银行怎么样"
    trie_tree = TrieTree(dictset)
    print(trie_tree.get_match_entity(query))
    print(query)
    print(trie_tree.replace_entity(query))

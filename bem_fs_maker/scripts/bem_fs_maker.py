import re
import os


class Bem_fs_maker:
    def __init__(self, blocks_path, html_name, exts, fs_scheme):
        if not blocks_path:
            raise Exception("Blocks folder error")
        self.blocks_path = blocks_path
        if ".html" not in html_name:
            raise Exception("html_file error")
        self.html_name = html_name
        if not exts:
            raise Exception("Extensions error")
        self.exts = exts
        if fs_scheme not in ["nest", "flat", "fluent"]:
            raise Exception("Scheme error")
        self.fs_scheme = fs_scheme
        self.blocks = self.get_blocks()

    """ returns html string """

    def get_file_data(self):
        with open(self.html_name, "r", encoding="utf-8") as file:
            return file.read()

    """ returns strings in tags class attributes """

    def get_raw_tokens_from_html(self):
        result = re.findall(r"class=\"([^\"]+)\"[\s|>]", self.get_file_data())
        result = set(map(lambda word: word.strip(), result))
        raw_tokens = set()
        for word in result:
            if " " in word:
                raw_tokens.update(word.split(" "))
            else:
                raw_tokens.add(word)
        return raw_tokens

    """ returns blocks tree """

    def get_blocks(self):
        blocks = {}
        raw_tokens = self.get_raw_tokens_from_html()
        for word in raw_tokens:
            if "__" not in word and "_" not in word:
                blocks[word] = {"modifiers": [], "elements": {}}
            elif "__" not in word:
                block, modifier = word.split("_", 1)
                blocks[block] = {"modifiers": [], "elements": {}}
                blocks[block]["modifiers"].append(modifier)
            else:
                if "__" in word:
                    block, tail = word.split("__")
                    if block not in blocks:
                        blocks[block] = {"modifiers": [], "elements": {}}
                    if "_" in tail:
                        element, modifier = tail.split("_", 1)
                    else:
                        element = tail
                        modifier = None
                    if element not in blocks[block]:
                        blocks[block]["elements"][element] = {"modifiers": []}
                    if modifier:
                        blocks[block]["elements"][element]["modifiers"].append(
                            modifier
                        )
                elif "_" in word:
                    block, modifier = word.split("_", 1)
                    blocks[block]["modifiers"].append(modifier)
        return blocks

    """ makes nest fs """

    def make_nest_fs(self):
        for block in self.blocks.keys():
            block_dir = os.path.join(self.blocks_path, block)
            if not os.path.exists(block_dir):
                os.mkdir(block_dir)
            for ext in self.exts:
                filename = os.path.join(block_dir, f"{block}.{ext}")
                if not os.path.exists(filename):
                    file = open(filename, "w")
                    file.close()
            for mod in self.blocks[block]["modifiers"]:
                mod_dir = os.path.join(block_dir, f"_{mod}")
                if not os.path.exists(mod_dir):
                    os.mkdir(mod_dir)
                for ext in self.exts:
                    filename = os.path.join(mod_dir, f"{block}_{mod}.{ext}")
                    if not os.path.exists(filename):
                        file = open(filename, "w")
                        file.close()
            for elem in self.blocks[block]["elements"].keys():
                elem_dir = os.path.join(block_dir, f"__{elem}")
                if not os.path.exists(elem_dir):
                    os.mkdir(elem_dir)
                for ext in self.exts:
                    filename = os.path.join(elem_dir, f"{block}__{elem}.{ext}")
                    if not os.path.exists(filename):
                        file = open(filename, "w")
                        file.close()
                for el_mod in self.blocks[block]["elements"][elem][
                    "modifiers"
                ]:
                    el_mod_dir = os.path.join(elem_dir, f"_{el_mod}")
                    if not os.path.exists(el_mod_dir):
                        os.mkdir(el_mod_dir)
                    for ext in self.exts:
                        filename = os.path.join(
                            el_mod_dir, f"{block}__{elem}_{el_mod}.{ext}"
                        )
                        if not os.path.exists(filename):
                            file = open(filename, "w")
                            file.close()

    def make_flat_fs(self):
        pass

    def make_fluent_fs(self):
        pass

    def make_fs(self):
        if self.fs_scheme == "nest":
            self.make_nest_fs()
        elif self.fs_scheme == "flat":
            self.make_flat_fs()
        else:
            self.make_fluent_fs()
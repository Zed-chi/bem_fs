import re
import os


class Bem_fs_maker:
    def __init__(self, blocks_path, html_name, ext, fs_scheme):
        if not blocks_path:
            raise Exception("Blocks folder error")
        self.blocks_path = blocks_path
        if ".html" not in html_name:
            raise Exception("html_file error")
        self.html_name = html_name
        if not ext:
            raise Exception("Extensions error")
        self.ext = ext
        if fs_scheme not in ["nest", "flat", "fluent"]:
            raise Exception("Scheme error")
        self.fs_scheme = fs_scheme
        self.blocks = {}
        self.fill_blocks_dict()

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

    def fill_blocks_dict(self):
        raw_tokens = self.get_raw_tokens_from_html()
        for word in raw_tokens:
            self.add_to_blocks(*self.process_token(word))

    def process_token(self, word):
        if re.search(r"[a-z0-9]__[a-z0-9]", word) and re.search(
            r"[a-z0-9]_[a-z0-9]", word
        ):
            block, tail = word.split("__", 1)
            element, modifier = tail.split("_", 1)
            return (block, None, element, modifier)
        elif re.search(r"[a-z0-9]__[a-z0-9]", word):
            block, element = word.split("__", 1)
            return (block, None, element, None)
        elif re.search(r"[a-z0-9]_[a-z0-9]", word):
            block, modifier = word.split("_", 1)
            return (block, modifier, None, None)
        else:
            return (word, None, None, None)

    def add_to_blocks(self, block, mod=None, elem=None, el_mod=None):
        if block not in self.blocks:
            self.blocks[block] = {"modifiers": set(), "elements": {}}
        if mod:
            self.blocks[block]["modifiers"].add(mod)
        if elem and elem not in self.blocks[block]["elements"]:
            self.blocks[block]["elements"][elem] = {"modifiers": set()}
        if elem and el_mod:
            self.blocks[block]["elements"][elem]["modifiers"].add(el_mod)

    """ makes nest fs """

    def mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def mkfile(self, file_path, data=None):
        if not os.path.exists(file_path):
            file = open(file_path, "w")
            if data:
                file.write(data)
            file.close()

    def mk_css(
        self, block=None, mods=[], elements=[], element=None, el_mods=[]
    ):
        data = ""
        for mod in mods:
            if "_" in mod:
                name, _ = mod.split("_", 1)
                url = f"@import url('./_{name}/{block}_{mod}.css');"
            else:
                url = f"@import url('./_{mod}/{block}_{mod}.css');"
            data = data + f"\n{url}"
        if elements:
            data = (
                data
                + "\n"
                + "\n".join(
                    map(
                        lambda e: f"@import url('./__{e}/{block}__{e}.css');",
                        elements,
                    )
                )
            )
        for emod in el_mods:
            if "_" in emod:
                name, _ = emod.split("_", 1)
                url = f"@import url('./_{name}/{element}_{emod}.css');"
            else:
                url = f"@import url('./_{emod}/{element}_{emod}.css');"
            data = data + f"\n{url}"
        return data

    def make_nest_fs(self):
        for block in self.blocks.keys():
            block_dir = os.path.join(self.blocks_path, block)
            self.mkdir(block_dir)
            file_path = os.path.join(block_dir, f"{block}.{self.ext}")
            data = self.mk_css(
                block=block,
                mods=self.blocks[block]["modifiers"],
                elements=self.blocks[block]["elements"].keys(),
            )
            self.mkfile(file_path, data=data)
            for mod in self.blocks[block]["modifiers"]:
                if re.search(r"[a-z0-9]_[a-z0-9]", mod):
                    mod_name, mod_value = mod.split("_", 1)
                    mod_dir = os.path.join(block_dir, f"_{mod_name}")
                    self.mkdir(mod_dir)
                else:
                    mod_dir = os.path.join(block_dir, f"_{mod}")
                    self.mkdir(mod_dir)
                file_path = os.path.join(mod_dir, f"{block}_{mod}.{self.ext}")
                self.mkfile(file_path)
            for elem in self.blocks[block]["elements"].keys():
                elem_dir = os.path.join(block_dir, f"__{elem}")
                self.mkdir(elem_dir)
                file_path = os.path.join(
                    elem_dir, f"{block}__{elem}.{self.ext}"
                )
                data = self.mk_css(
                    element=elem,
                    el_mods=self.blocks[block]["elements"][elem]["modifiers"],
                )
                self.mkfile(file_path, data)
                for el_mod in self.blocks[block]["elements"][elem][
                    "modifiers"
                ]:
                    if re.search(r"[a-z0-9]_[a-z0-9]", el_mod):
                        mod_name, _ = el_mod.split("_", 1)
                        el_mod_dir = os.path.join(elem_dir, f"_{mod_name}")
                        self.mkdir(el_mod_dir)
                    else:
                        el_mod_dir = os.path.join(elem_dir, f"_{el_mod}")
                        self.mkdir(el_mod_dir)
                    file_path = os.path.join(
                        el_mod_dir, f"{block}__{elem}_{el_mod}.{self.ext}"
                    )
                    self.mkfile(file_path)

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

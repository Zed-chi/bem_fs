from .scripts.bem_fs_maker import Bem_fs_maker
import os


def run():
    print("Создание файлов и папок проекта")
    root = input("\nпапка с блоками [blocks по-умолчанию]: ")
    if not root:
        root = "blocks"

    filename = input("\nфайл хтмл [index.html по-умолчанию]: ")
    if not filename:
        filename = "index.html"

    root = os.path.join(os.getcwd(), root)
    if not os.path.exists(root):
        os.mkdir(root)

    ext = input("\nрасширение [css по-умолчанию]: ")
    if not ext:
        ext = "css"
    fs_maker = Bem_fs_maker(root, filename, ext, "nest")
    fs_maker.make_fs()
    print("\nЗавершено")

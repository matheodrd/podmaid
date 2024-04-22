from pprint import pprint as print
import podman
import pytermgui as ptg

CONFIG = """
config:
    Window:
        styles:
            border: '140'
            corner: '140'

    Container:
        styles:
            border: '96'
            corner: '96'
"""

with ptg.YamlLoader() as loader:
    loader.load(CONFIG)

def safe_get(ls: list, idx: int, default: any) -> str:
    try:
        return ls[idx]
    except IndexError:
        return default

def get_images() -> dict:
    with podman.PodmanClient() as pdm:
        if pdm.ping():
            images = pdm.images.list()
            dict_images = {}
            for image in images:
                dict_images[image.id] = {"short_id": image.short_id,
                                         "tag": safe_get(image.tags, 0, "<none>")}
            return dict_images
        else:
            print("Impossible de se connecter à l'API de Podman\n\
                  Essayez : podman system service -t 0 &")

def handle_select(img_id):
    print(f"Vous avez sélectionné l'image avec ID: {img_id}")

def build_labels_list() -> list[list]:
    list_labels = []
    for img_id, img_data in get_images().items():
        list_labels.append([f"[@black #auto]{img_data['short_id']} {img_data['tag']}",
                            lambda img_id=img_id: handle_select(img_id)])
    return list_labels

def display_window() -> None:
    with ptg.WindowManager() as manager:

        window = (ptg.Window(*build_labels_list(),
                             width=100,
                             box="DOUBLE")
                  .set_title("[210 bold]Images")
                  .center())

        manager.add(window)

def main():
    display_window()


if __name__ == "__main__":
    main()
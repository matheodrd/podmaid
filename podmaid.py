﻿import podman
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header

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

class Podmaid(App):
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit"),
        Binding(key="j", action="down", description="Scroll down", show=False),
        Binding(key="k", action="up", description="Scroll up", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.title = "Podmaid"
        self.sub_title = "A podman cleaner in the terminal"

def main():
    app = Podmaid()
    app.run()

if __name__ == "__main__":
    main()
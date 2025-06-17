from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent
from src.events import KeywordQueryEventListener


class DenoScriptsExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener(self.render))
        # self.subscribe(ItemEnterEvent, ItemEnterEventListener(self))
        # self.refresh_state()

    def render_error(self, error: str):
        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/deno-scripts.png",
                    name="An unexpected error occurred",
                    description="Press enter to copy to clipboard, good luck o7",
                    on_enter=CopyToClipboardAction(error),
                )
            ]
        )

    def render(self, query: str | None):
        return self.render_error("test")

from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction


def render_error(error: str):
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


def render_message(title: str, description: str):
    return RenderResultListAction(
        [
            ExtensionResultItem(
                icon="images/deno-scripts.png",
                name=title,
                description=description,
                on_enter=HideWindowAction(),
            )
        ]
    )

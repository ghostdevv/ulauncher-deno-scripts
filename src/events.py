from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from typing import Callable


class KeywordQueryEventListener(EventListener):
    render: Callable[[str | None], RenderResultListAction]

    def __init__(self, render: Callable[[str | None], RenderResultListAction]):
        super().__init__()
        self.render = render

    def on_event(self, event: KeywordQueryEvent, _):  # type: ignore
        return self.render(event.get_argument())

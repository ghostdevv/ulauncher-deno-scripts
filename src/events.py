from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from typing import Callable


class KeywordQueryEventListener(EventListener):
    render: Callable[[str | None], RenderResultListAction]

    def __init__(self, render: Callable[[str | None], RenderResultListAction]):
        super().__init__()
        self.render = render

    def on_event(self, event: KeywordQueryEvent, _):  # type: ignore
        return self.render(event.get_argument())


class ItemEnterEventListener(EventListener):
    run_script: Callable[[str], RenderResultListAction]

    def __init__(self, run_script: Callable[[str], RenderResultListAction]):
        super().__init__()
        self.run_script = run_script

    def on_event(self, event: ItemEnterEvent, _):  # type: ignore
        data = event.get_data()
        if not data:
            return DoNothingAction()

        action = data.get("action")
        if not action:
            return DoNothingAction()

        match action:
            case "run-script":
                return self.run_script(data.get("script"))

        return DoNothingAction()

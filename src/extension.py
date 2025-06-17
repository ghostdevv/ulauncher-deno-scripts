from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from src.events import KeywordQueryEventListener, ItemEnterEventListener
from src.scripts import Scripts
from src.render import render_message
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from src.fuzzyfinder import fuzzyfinder


class DenoScriptsExtension(Extension):
    scripts: Scripts

    def __init__(self):
        super().__init__()
        self.scripts = Scripts()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener(self.render))
        self.subscribe(ItemEnterEvent, ItemEnterEventListener(self.scripts.run))

    def render(self, query: str | None):
        self.scripts.load()

        if self.scripts.scripts is None:
            return render_message("Error", "No configuration found")

        if len(self.scripts.scripts) == 0:
            return render_message("No Scripts", "No scripts found")

        # todo implement pagination
        limit = int(self.preferences.get("limit", "9"))

        options = [
            ExtensionResultItem(
                icon="images/deno-scripts.png",
                name=script["name"],
                description=script["description"],
                on_enter=ExtensionCustomAction(
                    {
                        "action": "run-script",
                        "script": script["id"],
                    },
                    True,
                ),
            )
            for script in self.scripts.scripts
        ]

        if not query:
            return RenderResultListAction(options[:limit])

        items: list[ExtensionResultItem] = list(
            fuzzyfinder(
                query,
                options,
                accessor=lambda item: item.get_name(),
            )
        )[:limit]

        return RenderResultListAction(items)

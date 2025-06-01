# :#

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich import box
import shutil


class PrettyLogger:
    def __init__(self):
        self.console = Console()
        self.logs = []

    def log(self, message, level="info"):
        level_color = {
            "info": "bright_black",
            "success": "green",
            "warn": "yellow",
            "error": "bold red"
        }
        styled = Text(message, style=level_color.get(level, "white"))
        self.logs.append(styled)

    def run(self, crawl_function):
        with Live(self.render_panel(), refresh_per_second=10, screen=True) as live:
            self._live = live
            crawl_function(self)

    from rich.layout import Layout


    def render_panel(self):
        # Get terminal height
        _, terminal_height = shutil.get_terminal_size((80, 24))

        # Calculate usable height (subtract for title, borders, padding)
        usable_height = terminal_height - 4

        # Take the last N lines that fit
        visible_logs = self.logs[-usable_height:] if usable_height > 0 else self.logs[-20:]

        content = Text("\n").join(visible_logs)
        panel = Panel(content, title=" OCR Crawler ", border_style="pink3", box=box.ROUNDED)

        layout = Layout()
        layout.split_column(
            Layout(panel, name="main", ratio=1),
        )
        return layout

    def update(self):
        self._live.update(self.render_panel())

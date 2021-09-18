import network_manager as nm
from rich import print
from datetime import datetime
# from rich.align import Align
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
# from rich.text import Text

layout = Layout()
layout.split_column(
    Layout(name="upper",size=3),
    Layout(name="lower")
)

class Header:
    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "Network Management Tool",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")



layout["upper"].update(Header())
layout["lower"].update(nm.main())


print(layout)
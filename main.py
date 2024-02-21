from nicegui import ui, Client, events
from head import head


async def return_focus():
    lookup = ui.query('input')
    script = f"""
        const e = getElement({lookup})
        e.addEventListener('focusout', e.focus());
        }});
        """
    js = ui.run_javascript(script)
    return js


async def select(x, e):
    ui.notify(x, level='info')
    print(f'@selection_change: {e}')
    await return_focus()


async def search(e: events.ValueChangeEventArguments, menu: ui.menu):
    print(f'@input_change: {e.value}')
    # not an async function
    if e.value is None or e.value == '':
        # to avoid a dropdown of numbers only or None and numbers
        return
    # list_item = ui.menu_item(text=f'{i}', on_click=lambda x: select(x, e.value))

lectures = []


@ui.refreshable
def lecture_ui() -> None:
    ui.label(', '.join(str(n) for n in sorted(lectures)))


async def add_lecture() -> None:
    lecture_ui.refresh()


@ui.page(path='/')
async def main(client: Client):
    ui.add_head_html(head)
    with ui.header():
        ui.label('Discuss Maps of Meaning').classes('text-4xl m-4')
    with ui.row():
        ui.label('Choose Course Year').classes('text-xl ml-10').style('margin-top: 20px;')
    with ui.row():
        # await client.connected()
        courses = [
            'Maps of Meaning 2015',
            'Maps of Meaning 2016',
            'Maps of Meaning 2017',
        ]
        dropdown = ui.menu().classes('w-96 self-center mt-24 transition-all')
        text_search = ui.select(options=courses, with_input=True, on_change=lambda x: search(x, dropdown))\
            .props('autofocus clearable outlined rounded item-aligned input-class="ml-3"') \
            .classes('w-96 self-center mt-0 transition-all animate__animated animate__fadeInUp').bind_value_to(dropdown
                                                                                                               ).style(
            'margin-left: 0px;')
        ui.button('Analyze Lectures', on_click=add_lecture).classes('w-96 self-center mt-0 transition-all '
                                                                         'animate__animated animate__rotateIn')


ui.run()


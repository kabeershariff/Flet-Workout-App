import flet as ft
import db_operations

current_page = None

def initialize():
    db_operations.schedule()
    db_operations.log()

def refresh_page():
    if current_page:
        current_page.update()
def home_view():
    def fetch_workout_today():
        pass
    if db_operations.is_empty_table():
        placeholder = ft.Text("Add workouts from settings to get started", theme_style=ft.TextThemeStyle.DISPLAY_SMALL)
        layout = ft.Container(content=ft.Column(
            controls=[placeholder],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        ), 
        padding= ft.padding.symmetric(horizontal=25, vertical=50),
        expand=True,
        )   
        return [layout]
    jobs = db_operations.get_today_workout()
    if jobs:
        placeholder = ft.Text("You have stuff to do!", theme_style=ft.TextThemeStyle.DISPLAY_SMALL)
        layout = ft.Container(content=ft.Column(
            controls=[placeholder],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        ), padding= ft.padding.symmetric(horizontal=25, vertical=50),
        )

        return [layout]
    else:
        placeholder = ft.Text("REST you need REST :)", theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM)

        layout = ft.Container(content=ft.Column(
            controls=[placeholder],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        ), 
        padding= ft.padding.symmetric(horizontal=25, vertical=50),
        expand=True,
        )
        return [layout]

def settings_view():
    def validate_required(e):
        if e.control.value =="":
            e.control.error_text = 'The field is required'
            e.control.update()
    
    def add_to_schedule(e):
        if (
            not workout_name.value or
            not sets.value or
            not reps.value or
            not select_day.value
        ):
            print('Error: Fill in Empty fields')
        else: 
            db_operations.add_workout(select_day.value, workout_name.value, sets.value, reps.value)
            print("Workout added successfully to Database")
            fetch_tasks()

    def delete_workout(id):
        db_operations.remove_workout(id)
        fetch_tasks()

    def fetch_tasks():
        tasks = db_operations.fetch_schedule_values()
        tasks_view.controls.clear()  # Clear previous entries
        for id, day, workout_name, sets, reps in tasks:
            tasks_view.controls.append(
                ft.Row([
                    ft.Text(f"{day} {sets}X{reps} -> {workout_name}"),
                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, workout_id=id: delete_workout(workout_id))
        ])
            )
        refresh_page()  # Update the page to reflect new changes

    tasks_view = ft.Column(scroll="auto")
    scroll_view = ft.Container(
        content=tasks_view,
        height=400,
    )
    select_day = ft.Dropdown(
        label="Select the Day",
        options=[
            ft.dropdown.Option("Monday"),
            ft.dropdown.Option("Tuesday"),
            ft.dropdown.Option("Wednesday"),
            ft.dropdown.Option("Thursday"),
            ft.dropdown.Option("Friday"),
            ft.dropdown.Option("Saturday"),
            ft.dropdown.Option("Sunday"),
        ],
    )
    workout_name = ft.TextField(hint_text="Workout name", max_length=45, on_blur=validate_required)
    sets = ft.TextField(
        hint_text="Enter number of Sets",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        max_length=5,
        on_blur=validate_required, )
    reps = ft.TextField(
        hint_text="Enter number of Reps", 
        keyboard_type=ft.KeyboardType.NUMBER, 
        input_filter=ft.NumbersOnlyInputFilter(), 
        max_length=5,
        on_blur=validate_required,)

    add_button = ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_to_schedule)

    layout = ft.Container(content=ft.Column(
        controls=[select_day, workout_name, sets, reps, add_button, scroll_view],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
    ), padding= ft.padding.symmetric(horizontal=25, vertical=50),
    )

    fetch_tasks()

    return [layout]

def progress_view():
    return [ft.Text("View your progress here")]

def main(page: ft.Page):
    global current_page
    current_page = page
    
    def handle_nav_change(e):
        page.clean()
        if e.control.selected_index == 0:
            page.add(*home_view())
        
        elif e.control.selected_index == 1:
            page.add(*settings_view())

        elif e.control.selected_index == 2:
            page.add(*progress_view())
        page.update()
    
    initialize()
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    page.title = "Beast Mode"
    page.navigation_bar = ft.NavigationBar(
        on_change = handle_nav_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Settings"),
            ft.NavigationBarDestination(icon=ft.Icons.EVENT_NOTE_OUTLINED, selected_icon=ft.Icons.EVENT_NOTE, label="Progress")
        ]
    ) 
    
    page.add(*home_view())
    

ft.app(main)

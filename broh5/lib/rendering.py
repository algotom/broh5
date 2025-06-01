"""
Module for constructing GUI components:
    -   Main window.
    -   Dialog for selecting a file.
    -   Dialog for saving a file.
"""

import os
import string
import platform
from pathlib import Path
from typing import Optional, List
from nicegui import ui
from nicegui.events import GenericEventArguments
import broh5.lib.utilities as util


# ============================================================================
#                   Global parameters for the GUI
# ============================================================================

MARKER_LIST = [",", ".", "o", "x"]
CMAP_LIST = ["gray", "inferno", "afmhot", "viridis", "magma"]
AXIS_LIST = [0, 1, 2]
FONT_STYLE = "font-size: 105%; font-weight: bold"
DISPLAY_TYPE = ["plot", "table"]
UPDATE_RATE = 0.2  # second
RATIO = 0.65  # Ratio for adjusting size between image/plot and screen
MAX_FIG_SIZE = [12.0, 9.0]
MAX_PLOT_SIZE = [9.0, 7.0]
INPUT_EXT = ["hdf", "nxs", "h5", "hdf5"]
PLOT_COLOR = "blue"
HEADER_COLOR = "#3874c8"
HEADER_TITLE = "BROWSER-BASED HDF VIEWER"
LEFT_DRAWER_COLOR = "#d7e3f4"
TREE_BGR_COLOR = "#f8f8ff"
BOX_LINE_COLOR = "lime"
BOX_LINE_WIDTH = 3


class GuiRendering:
    """
    A class to build the graphical user interface for an HDF viewer.

    This class creates various UI elements like headers, buttons,
    sliders, tables, and plots to facilitate user interaction with HDF data.

    Attributes
    ----------
    fig_size : tuple
        Dimensions for the figure in the UI.
    plot_size : tuple
        Dimensions for the histogram plot in the UI.
    tree_container : UI column
        Container for the HDF tree structure.
    select_file_button : UI button
        Button to trigger file selection.
    file_path_display : UI label
        Label to display selected file path.
    hdf_key_display : UI label
        Label to display HDF key.
    hdf_value_display : UI label
        Label to display HDF value.
    axis_list : UI select
        Dropdown to select axis for slicing.
    cmap_list : UI select
        Dropdown to select color map for plots.
    enable_zoom : UI checkbox
        Check-box to enable/disable image zoom.
    zoom_list : UI select
        Dropdown to select zooming ratio.
    enable_profile :  UI checkbox
        Check-box to enable/disable the intensity-profile plot
    profile_list : UI select
        Dropdown to select the direction of the intensity profile.
    save_image_button : UI button
        Button to save current image.
    display_type : UI select
        Dropdown to choose the display type (plot or table).
    marker_list : UI select
        Dropdown to select marker type for plots.
    save_data_button : UI button
        Button to save current data.
    main_slider : UI slider
        Slider to navigate through slices of 3D data.
    main_table : UI table
        Table to display data in tabular form.
    main_plot : UI matplotlib
        Matplotlib element to display plots.
    zoom_profile_plot : UI pyplot
        Pyplot element to display zooming of an image or intensity-profile.
    min_slider : UI slider
        Slider to adjust the minimum value for image contrast.
    max_slider : UI slider
        Slider to adjust the maximum value for image contrast.
    reset_button : UI button
        Button to reset adjustments.
    histogram_plot : UI pyplot
        Pyplot element to display histogram of an image.
    image_info_table : UI table
        Table to display statistical information of an image.

    Methods
    -------
    init_gui()
        Initializes and constructs the GUI elements.
    """
    def __init__(self):
        super().__init__()
        # Initial parameters
        (sc_height, sc_width, dpi) = util.get_height_width_screen()
        hei_size = RATIO * sc_width / dpi
        wid_size = RATIO * sc_height / dpi
        self.dpi = dpi
        self.fig_size = (min(hei_size, MAX_FIG_SIZE[0]),
                         min(wid_size, MAX_FIG_SIZE[1]))
        self.plot_size = (min(hei_size, MAX_PLOT_SIZE[0]),
                          min(wid_size, MAX_PLOT_SIZE[1]))
        self.tree_container = None
        self.select_file_button = None
        self.file_path_display = None
        self.hdf_key_display = None
        self.hdf_value_display = None
        self.axis_list = None
        self.cmap_list = None
        self.enable_zoom = None
        self.zoom_list = None
        self.enable_profile = None
        self.profile_list = None
        self.save_image_button = None
        self.display_type = None
        self.marker_list = None
        self.save_data_button = None
        self.main_slider = None
        self.main_table = None
        self.main_plot = None
        self.zoom_profile_plot = None
        self.min_slider = None
        self.max_slider = None
        self.reset_button = None
        self.histogram_plot = None
        self.image_info_table = None
        self.tab_one = None
        self.tab_two = None
        self.panel_tabs = None
        self.init_gui()

    def init_gui(self):
        """
        Initializes and constructs the various elements of the GUI.

        This method sets up headers, drawers, rows, labels, buttons, sliders,
        tables, and plots to create an interactive user interface.
        """
        # For the header
        with ui.header().style("background-color: " + HEADER_COLOR).classes(
                "items-center justify-between"):
            ui.label(HEADER_TITLE).style(FONT_STYLE)

        # For the left drawer, used to display a hdf tree.
        with ui.left_drawer(fixed=True, bottom_corner=True).style(
                "background-color: " + LEFT_DRAWER_COLOR):
            with ui.row():
                self.tree_container = ui.column()
                with self.tree_container:
                    self.select_file_button = ui.button(
                        "Select file").props("icon=folder")

        # Layout for the main page.
        with ui.column().classes("w-full no-wrap gap-1"):
            # For displaying file-path, key, and value of a hdf/nxs/h5 file
            with ui.row().classes("w-full no-wrap"):
                with ui.row().classes("w-1/3 items-center"):
                    ui.label("File path: ").style(FONT_STYLE)
                    self.file_path_display = ui.label("")
                with ui.row().classes("w-1/3 items-center"):
                    ui.label("Key: ").style(FONT_STYLE)
                    self.hdf_key_display = ui.label("")
                with ui.row().classes("w-1/3 items-center"):
                    ui.label("Value: ").style(FONT_STYLE)
                    self.hdf_value_display = ui.label("")
            ui.separator()

            # For ui-components used to interact with data.
            with ui.row().classes("w-full justify-between items-center"):
                # For ui-components used to interact with 3d data.
                with ui.row().classes("items-center"):
                    ui.label("Axis: ").style(FONT_STYLE)
                    self.axis_list = ui.select(AXIS_LIST, value=AXIS_LIST[0])
                with ui.row().classes("items-center"):
                    ui.label("Color map: ").style(FONT_STYLE)
                    self.cmap_list = ui.select(CMAP_LIST, value=CMAP_LIST[0])
                with ui.row().classes("items-center"):
                    self.enable_zoom = ui.checkbox('Zoom')
                    self.zoom_list = ui.select(['2x', '4x', '8x'], value="2x")
                with ui.row().classes("items-center"):
                    self.enable_profile = ui.checkbox('Profile')
                    self.profile_list = ui.select(['vertical', 'horizontal'],
                                                  value='horizontal')
                self.save_image_button = ui.button("Save image")

                # For ui-components used to interact with 1d/2d data.
                with ui.row().classes("items-center"):
                    ui.label("Display: ").style(FONT_STYLE)
                    self.display_type = ui.select(DISPLAY_TYPE,
                                                  value=DISPLAY_TYPE[0])
                with ui.row().classes("items-center"):
                    ui.label("Marker: ").style(FONT_STYLE)
                    self.marker_list = ui.select(MARKER_LIST,
                                                 value=MARKER_LIST[0])
                self.save_data_button = ui.button("Save data")

            # Slider for slicing 3d dataset
            with ui.row().classes("w-full items-center no-wrap"):
                ui.label("Slice: ").style(FONT_STYLE)
                self.main_slider = ui.slider(min=0, max=100, value=0).props(
                    "label-always").on("update:model-value",
                                       throttle=UPDATE_RATE,
                                       leading_events=False)

            # Tabs for data visualization and displaying image information
            tabs = ui.tabs().classes('w-full')
            with tabs:
                self.tab_one = ui.tab('Data visualization').style(
                    "background-color: " + TREE_BGR_COLOR)
                self.tab_two = ui.tab('Image information').style(
                    "background-color: " + TREE_BGR_COLOR)
            self.panel_tabs = ui.tab_panels(tabs, value=self.tab_one).classes(
                'w-full')
            with self.panel_tabs:
                # Tab 1 for data visualization
                with ui.tab_panel(self.tab_one):
                    # For display data as an image, table, or plot
                    self.main_table = ui.table(columns=[], rows=[],
                                               row_key="Index")
                    with ui.row().classes("w-full justify-left items-center"):
                        self.main_plot = ui.matplotlib(figsize=self.fig_size,
                                                       dpi=self.dpi)
                        self.zoom_profile_plot = ui.matplotlib(
                            figsize=self.fig_size, dpi=self.dpi)

                    # Sliders for adjust the contrast of an image.
                    with ui.row().classes(
                            "w-full justify-between no-wrap items-center"):
                        ui.label("Min: ").style(FONT_STYLE)
                        self.min_slider = ui.slider(min=0, max=254,
                                                    value=0).props(
                            "label-always").on("update:model-value",
                                               throttle=UPDATE_RATE,
                                               leading_events=False)

                        ui.label("Max: ").style(FONT_STYLE)
                        self.max_slider = ui.slider(min=1, max=255,
                                                    value=255).props(
                            "label-always").on("update:model-value",
                                               throttle=UPDATE_RATE,
                                               leading_events=False)
                        self.reset_button = ui.button("Reset")
                # Tab 2 for showing image information
                with ui.tab_panel(self.tab_two):
                    with ui.row().classes(
                            "w-full justify-between no-wrap items-center"):
                        self.histogram_plot = ui.pyplot(figsize=self.plot_size,
                                                        close=False,
                                                        ).classes("w-full")
                        self.image_info_table = ui.table(columns=[],
                                                         rows=[],
                                                         row_key="name")


class FilePicker(ui.dialog):
    """
    A dialog class for file picking in the GUI. Codes are adapted from an
    example of NiceGUI:
    https://github.com/zauberzeug/nicegui/tree/main/examples/local_file_picker

    Allows users to browse and select files from the local filesystem where
    the application is running.

    Parameters
    ----------
    directory : str
        The starting directory for the file picker.
    upper_limit : str, optional
        The upper directory limit for browsing. None by default.
    show_hidden_files : bool, optional
        Flag to show hidden files. False by default.
    allowed_extensions : List of str, optional
        List of allowed file extensions for filtering. None by default.

    Methods
    -------
    check_extension(filename: str)
        Check if the given filename has an allowed extension.
    add_drives_toggle()
        Add a toggle for drive selection on Windows systems.
    update_grid()
        Update the file grid based on the current directory and filters.
    handle_double_click(GenericEventArguments)
        Handle double click events on the file grid.
    handle_ok()
        Handle the OK button, click to submit the selected file path.
    """
    def __init__(self, directory: str, *,
                 upper_limit: Optional[str] = None,
                 show_hidden_files: bool = False,
                 allowed_extensions: Optional[List[str]] = None) -> None:
        super().__init__()
        self.show_hidden_files = show_hidden_files
        self.allowed_extensions = allowed_extensions
        self.drives_toggle = None
        self.path = Path(directory).expanduser()
        if upper_limit is None:
            self.upper_limit = None
        else:
            self.upper_limit = Path(
                directory if upper_limit is ... else upper_limit).expanduser()
        with self, ui.card():
            self.add_drives_toggle()
            self.grid = ui.aggrid(
                {'columnDefs': [{'field': 'name', 'headerName': 'File'}],
                 'rowSelection': 'single'}, html_columns=[0]).classes(
                'w-96').on('cellDoubleClicked', self.handle_double_click)
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self.handle_ok)
        self.update_grid()

    def check_extension(self, filename: str) -> bool:
        """Check if the filename has an allowed extension."""
        if self.allowed_extensions is None:
            return True
        else:
            return filename.split('.')[-1].lower() in self.allowed_extensions

    def add_drives_toggle(self):
        """Give a list of available drivers in a WinOS computer"""
        if platform.system() == 'Windows':
            drives = ['%s:\\' % d for d in string.ascii_uppercase if
                      os.path.exists('%s:' % d)]
            if self.path != "" or self.path != ".":
                select_drive = os.path.splitdrive(self.path)[0] + "\\"
            else:
                self.path = Path(drives[0]).expanduser()
                select_drive = drives[0]
            self.drives_toggle = ui.toggle(drives, value=select_drive,
                                           on_change=self.__update_drive)

    def __update_drive(self):
        if self.drives_toggle:
            self.path = Path(self.drives_toggle.value).expanduser()
            self.update_grid()

    def update_grid(self) -> None:
        paths = list(self.path.glob('*'))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith('.')]
        if self.allowed_extensions:
            paths = [p for p in paths if
                     p.is_dir() or self.check_extension(p.name)]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.grid.options['rowData'] = [
            {'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
             'path': str(p), } for p in paths]
        if (self.upper_limit is None
                and self.path != self.path.parent
                or self.upper_limit is not None
                and self.path != self.upper_limit):
            self.grid.options['rowData'].insert(0, {
                'name': '📁 <strong>..</strong>',
                'path': str(self.path.parent), })
        self.grid.update()

    def handle_double_click(self, e: GenericEventArguments) -> None:
        self.path = Path(e.args['data']['path'])
        if self.path.is_dir():
            self.update_grid()
        else:
            if self.path:
                self.submit(str(self.path))
            else:
                return

    async def handle_ok(self):
        try:
            self.update_grid()
            rows = await self.grid.get_selected_rows()
            if rows:
                fpath = [r['path'] for r in rows]
                if fpath:
                    selected_path = Path(fpath[0])
                    if selected_path.suffix in {'.h5', '.hdf', '.nxs'}:
                        self.submit(str(selected_path))
                    else:
                        ui.notify("Please select a file with the extension "
                                  ".h5, .hdf, or .nxs!")
                        return
                else:
                    ui.notify("No file path found in the selected rows")
                    return
            else:
                ui.notify("No rows selected. Try double-clicking instead!")
                return
        except Exception as e:
            ui.notify(f"An error occurred: {e}")
            return


class FileSaver(ui.dialog):
    """
    A dialog class for saving files in the GUI.

    Allows users to specify a file name and directory for saving files.

    Parameters
    ----------
    directory : str
        Starting directory for the file saver.
    upper_limit : str, optional
        Upper directory limit for browsing. None by default.
    show_hidden_files : bool, optional
        Flag to show hidden files. False by default.
    title : str, optional
        Title for the file-name input-field. 'File name' by default.

    Methods
    -------
    add_drives_toggle()
        Add a toggle for drive selection on Windows systems.
    update_grid() -> None
        Update the file grid based on the current directory.
    handle_double_click(e: GenericEventArguments) -> None
        Handle double-click events on the file grid.
    handle_save()
        Handle the Save button, click to submit the specified file path.
    create_folder_dialog()
        Open a dialog for creating a new folder.
    create_folder(folder_name: str, dialog: ui.dialog)
        Create a new folder with the specified name.
    """
    def __init__(self, directory: str, *, upper_limit: Optional[str] = None,
                 show_hidden_files: bool = False,
                 title: Optional[str] = 'File name') -> None:
        super().__init__()
        self.show_hidden_files = show_hidden_files
        self.drives_toggle = None
        self.path = Path(directory).expanduser()
        self.title = title
        if upper_limit is None:
            self.upper_limit = None
        else:
            self.upper_limit = Path(
                directory if upper_limit is ... else upper_limit).expanduser()

        with self, ui.card():
            self.add_drives_toggle()
            self.grid = ui.aggrid(
                {'columnDefs': [{'field': 'name', 'headerName': 'File'}],
                 'rowSelection': 'single'}, html_columns=[0]).classes(
                'w-96').on('cellDoubleClicked', self.handle_double_click)
            # Input field for filename
            self.filename_input = ui.input(self.title).classes(
                'w-full justify-between').on('keydown.enter',
                                             self.handle_save)
            with ui.row().classes('w-full justify-between'):
                ui.button('Create Folder',
                          on_click=self.create_folder_dialog).props('outline')
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Save', on_click=self.handle_save)
        self.update_grid()

    def add_drives_toggle(self):
        """Give a list of available drivers in a WinOS computer"""
        if platform.system() == 'Windows':
            drives = ['%s:\\' % d for d in string.ascii_uppercase if
                      os.path.exists('%s:' % d)]
            if self.path != "" or self.path != ".":
                select_drive = os.path.splitdrive(self.path)[0] + "\\"
            else:
                self.path = Path(drives[0]).expanduser()
                select_drive = drives[0]
            self.drives_toggle = ui.toggle(drives, value=select_drive,
                                           on_change=self.__update_drive)

    def __update_drive(self):
        if self.drives_toggle:
            self.path = Path(self.drives_toggle.value).expanduser()
            self.update_grid()

    def update_grid(self) -> None:
        paths = list(self.path.glob('*'))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith('.')]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.grid.options['rowData'] = [
            {'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
             'path': str(p)} for p in paths]
        if (self.upper_limit is None
                and self.path != self.path.parent
                or self.upper_limit is not None
                and self.path != self.upper_limit):
            self.grid.options['rowData'].insert(0, {
                'name': '📁 <strong>..</strong>',
                'path': str(self.path.parent)})
        self.grid.update()

    def handle_double_click(self, e: GenericEventArguments) -> None:
        self.path = Path(e.args['data']['path'])
        if self.path.is_dir():
            self.update_grid()
        else:
            self.filename_input.value = self.path.name
            self.path = self.path.parent

    def handle_save(self):
        filename = self.filename_input.value
        if not filename:
            ui.notify('File name cannot be empty!')
            return
        save_path = self.path / filename
        save_path_str = str(save_path).replace('\\', '/')
        self.submit(save_path_str)

    async def create_folder_dialog(self):
        """Open a dialog to get the name of the new folder and create it."""
        with ui.dialog().classes('w-100 h-100') as dialog, ui.card():
            with ui.column():
                folder_name_input = ui.input('Folder Name').classes(
                    'w-full justify-between')
                with ui.row():
                    ui.button('Cancel', on_click=dialog.close).props('outline')
                    ui.button('Create', on_click=lambda: self.create_folder(
                        folder_name_input.value, dialog))
        await dialog

    def create_folder(self, folder_name: str, dialog: ui.dialog):
        if not folder_name:
            ui.notify('Folder name cannot be empty!')
            return
        new_folder_path = self.path / folder_name
        if new_folder_path.exists():
            ui.notify(f"A folder named '{folder_name}' already exists!")
            return
        new_folder_path.mkdir(parents=True, exist_ok=True)
        self.update_grid()
        dialog.close()

import os
import h5py
import hdf5plugin
import numpy as np
import matplotlib.pyplot as plt
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import broh5.lib.rendering as re
import broh5.lib.utilities as util
from broh5.lib.rendering import GuiRendering, FilePicker, FileSaver


class GuiInteraction(GuiRendering):
    """
    Methods to link actions <-> response of the GUI.
    """

    def __init__(self):
        super().__init__()
        self.select_file_button.on("click", self.pick_file)
        self.save_image_button.on("click", self.save_image)
        self.save_data_button.on("click", self.save_data)
        self.reset_button.on("click", self.reset_min_max)
        self.current_state = None
        self.columns = None
        self.rows = None
        self.image = None
        self.current_slice = None
        self.data_1d_2d = None
        ui.timer(re.UPDATE_RATE, lambda: self.show_data())

    def show_key(self, event: ValueChangeEventArguments, file_path):
        """
        Show key to a dataset/group of a hdf file when users click
        to a branch of the hdf tree.
        """
        hdf_key = event.value
        if hdf_key is not None:
            self.hdf_key_display.set_text(hdf_key)
        else:
            self.hdf_value_display.set_text("")
        if file_path is not None:
            self.file_path_display.set_text(file_path)

    async def pick_file(self) -> None:
        """To pick a file when click the button 'Select file' """
        file_path = await FilePicker("~",
                                     allowed_extensions=re.INPUT_EXT)
        if file_path:
            self.display_hdf_tree(file_path)

    def display_hdf_tree(self, file_path):
        """Display interactive tree structure of a hdf file"""
        with self.tree_container:
            file_path = file_path.replace("\\", "/")
            self.file_path_display.set_text(file_path)
            self.hdf_key_display.set_text("")
            hdf_dic = util.hdf_tree_to_dict(file_path)
            if isinstance(hdf_dic, list):
                tree_display = ui.card()

                def close_file():
                    if isinstance(self.current_state, tuple):
                        if file_path == self.current_state[0]:
                            self.reset()
                    else:
                        self.reset()
                    self.tree_container.remove(tree_display)

                with tree_display.style("background-color: "
                                        + re.TREE_BGR_COLOR):
                    ui.tree(hdf_dic, label_key="id", node_key="label",
                            on_select=lambda e: self.show_key(e, file_path))
                    ui.button("Close file", on_click=lambda: close_file())
            else:
                if isinstance(hdf_dic, str):
                    ui.notify(hdf_dic)
                else:
                    ui.notify("Input must be hdf, hdf5, nxs, or h5 format!")

    def disable_sliders(self):
        """Disable and reset values of sliders"""
        self.main_slider.set_value(0)
        self.main_slider.disable()
        self.min_slider.set_value(0)
        self.min_slider.disable()
        self.max_slider.set_value(255)
        self.max_slider.disable()

    def enable_ui_elements_3d_data(self):
        """
        Enable UI-elements for displaying a slice from 3d data as an image and
        disable non-related UI-elements.
        """
        # Enable ui-components related to image show
        self.main_slider.enable()
        self.max_slider.enable()
        self.min_slider.enable()
        self.main_plot.set_visibility(True)
        self.axis_list.enable()
        self.cmap_list.enable()
        self.save_image_button.enable()

        # Disable other ui-components
        self.main_table.set_visibility(False)
        self.display_type.disable()
        self.marker_list.disable()
        self.save_data_button.disable()
        self.data_1d_2d = None

    def enable_ui_elements_1d_2d_data(self):
        """
        Enable UI-elements for displaying 1d/2d data as a table or plot, and
        disable non-related UI-elements.
        """
        self.image = None
        # Disable ui-components related to image show
        self.disable_sliders()
        self.axis_list.value = re.AXIS_LIST[0]
        self.cmap_list.value = re.CMAP_LIST[0]
        self.axis_list.disable()
        self.cmap_list.disable()
        self.save_image_button.disable()

        # Enable other ui-components
        self.display_type.enable()
        self.marker_list.enable()
        self.save_data_button.enable()

    def reset(self, keep_display=False):
        """Reset status of UI-elements"""
        if not keep_display:
            self.hdf_key_display.set_text("")
            self.file_path_display.set_text("")
            self.hdf_value_display.set_text("")
        self.axis_list.value = re.AXIS_LIST[0]
        self.cmap_list.value = re.CMAP_LIST[0]
        self.display_type.value = re.DISPLAY_TYPE[0]
        self.marker_list.value = re.MARKER_LIST[0]
        self.axis_list.disable()
        self.cmap_list.disable()
        self.display_type.disable()
        self.marker_list.disable()
        self.disable_sliders()
        self.rows, self.columns = None, None
        self.image, self.data_1d_2d = None, None
        self.main_table.set_visibility(False)
        self.main_plot.set_visibility(True)
        self.save_image_button.disable()
        self.save_data_button.disable()

    def reset_min_max(self):
        """Reset minimum and maximum values of sliders"""
        self.min_slider.set_value(0)
        self.max_slider.set_value(255)

    def display_3d_data(self, data_obj):
        """Display a slice of 3d array as an image"""
        self.enable_ui_elements_3d_data()
        (depth, height, width) = data_obj.shape
        current_max = self.main_slider._props["max"]
        if int(self.axis_list.value) == 2:
            max_val = width - 1
        elif int(self.axis_list.value) == 1:
            max_val = height - 1
        else:
            max_val = depth - 1
        if current_max != max_val:
            self.main_slider._props["max"] = max_val
            self.main_slider.update()
        d_pos = int(self.main_slider.value)
        if d_pos > max_val:
            self.main_slider.set_value(max_val)
            d_pos = max_val
        new_slice = (self.main_slider.value, self.axis_list.value,
                     self.file_path_display.text)
        if new_slice != self.current_slice or self.image is None:
            self.current_slice = new_slice
            if int(self.axis_list.value) == 2:
                if depth > 1000 and height > 1000:
                    ui.notify("Slicing along axis 2 is very time consuming!")
                    self.axis_list.value = 0
                    self.main_slider.set_value(0)
                    self.image = data_obj[0]
                else:
                    self.image = data_obj[:, :, d_pos]
            elif int(self.axis_list.value) == 1:
                if depth > 1000 and width > 1000:
                    ui.notify("Slicing along axis 1 can take time !")
                self.image = data_obj[:, d_pos, :]
            else:
                self.image = data_obj[d_pos]
        min_val = int(self.min_slider.value)
        max_val = int(self.max_slider.value)
        if min_val > 0 or max_val < 255:
            if min_val >= max_val:
                min_val = np.clip(max_val - 1, 0, 254)
                self.min_slider.set_value(min_val)
            nmin, nmax = np.min(self.image), np.max(self.image)
            if nmax != nmin:
                image1 = np.uint8(255.0 * (self.image - nmin) / (nmax - nmin))
                image1 = np.clip(image1, min_val, max_val)
            else:
                image1 = np.zeros(self.image.shape)
        else:
            image1 = np.copy(self.image)
        with self.main_plot:
            plt.clf()
            plt.imshow(image1, cmap=self.cmap_list.value)
            plt.tight_layout()
            self.main_plot.update()

    def display_1d_2d_data(self, data_obj, disp_type="plot"):
        """Display 1d/2d array as a table or plot"""
        self.enable_ui_elements_1d_2d_data()
        self.data_1d_2d = data_obj[:]
        if disp_type == "table":
            self.main_plot.set_visibility(False)
            self.main_table.set_visibility(True)
            rows, columns = util.format_table_from_array(data_obj[:])
            if self.main_table.rows is None:
                self.main_table._props["rows"] = rows
            else:
                self.main_table.rows[:] = rows
            self.main_table.update()
        else:
            self.main_plot.set_visibility(True)
            self.main_table.set_visibility(False)
            x, y = None, None
            img = False
            if len(data_obj.shape) == 2:
                (height, width) = data_obj.shape
                if height == 2:
                    x, y = np.asarray(data_obj[0]), np.asarray(data_obj[1])
                elif width == 2:
                    x = np.asarray(data_obj[:, 0])
                    y = np.asarray(data_obj[:, 1])
                else:
                    img = True
            else:
                size = len(data_obj)
                x, y = np.arange(size), np.asarray(data_obj[:])
            if x is not None:
                with self.main_plot:
                    plt.clf()
                    title = self.hdf_key_display.text.split("/")[-1]
                    plt.title(title.capitalize())
                    plt.plot(x, y, marker=self.marker_list.value,
                             color=re.PLOT_COLOR)
                    plt.tight_layout()
                    self.main_plot.update()
            if img:
                with self.main_plot:
                    plt.clf()
                    plt.imshow(data_obj[:], cmap=self.cmap_list.value,
                               aspect="auto")
                    plt.tight_layout()
                    self.main_plot.update()

    def show_data(self):
        """Display data getting from a hdf file"""
        file_path1 = self.file_path_display.text
        hdf_key1 = self.hdf_key_display.text
        if (file_path1 != "") and (hdf_key1 != "") and (hdf_key1 is not None):
            new_state = (file_path1, hdf_key1, self.main_slider.value,
                         self.hdf_value_display.text, self.axis_list.value,
                         self.cmap_list.value, self.display_type.value,
                         self.marker_list.value, self.min_slider.value,
                         self.max_slider.value)
            if new_state != self.current_state:
                self.current_state = new_state
                try:
                    (data_type, value) = util.get_hdf_data(file_path1,
                                                           hdf_key1)
                    if (data_type == "string" or data_type == "number"
                            or data_type == "boolean"):
                        self.hdf_value_display.set_text(str(value))
                        with self.main_plot:
                            plt.clf()
                            self.main_plot.update()
                        self.reset(keep_display=True)
                    elif data_type == "array":
                        self.hdf_value_display.set_text("Array shape: "
                                                        "" + str(value))
                        hdf_obj = h5py.File(file_path1, "r")
                        dim = len(value)
                        if dim == 3:
                            self.display_3d_data(hdf_obj[hdf_key1])
                        elif dim < 3:
                            self.display_1d_2d_data(
                                hdf_obj[hdf_key1],
                                disp_type=self.display_type.value)
                        else:
                            ui.notify("Can't display {}-d array!".format(dim))
                            with self.main_plot:
                                plt.clf()
                                self.main_plot.update()
                            self.reset(keep_display=True)
                        hdf_obj.close()
                    else:
                        self.hdf_value_display.set_text(data_type)
                        with self.main_plot:
                            plt.clf()
                            self.main_plot.update()
                        self.reset(keep_display=True)
                except Exception as error:
                    self.reset(keep_display=True)
                    _, broken_link, msg = util.check_external_link(file_path1,
                                                                   hdf_key1)
                    if broken_link:
                        ui.notify(msg)
                    else:
                        _, ext_compressed, msg = util.check_compressed_dataset(
                            file_path1, hdf_key1)
                        if ext_compressed:
                            ui.notify(msg)
                        else:
                            ui.notify("Error: {}".format(error))
                            ui.notify("Dataset may be an external link and the"
                                      " target file is not accessible (moved, "
                                      "deleted, or corrupted) !!!")
        else:
            self.hdf_value_display.set_text("")
            with self.main_plot:
                plt.clf()
                self.main_plot.update()
            self.reset(keep_display=True)

    async def save_image(self) -> None:
        """To save a slice to file when click 'Save image' """
        file_path = await FileSaver("~", title="File name (ext: .tif, "
                                               ".jpg, .png, or .csv)")
        if file_path and self.image is not None:
            file_ext = os.path.splitext(file_path)[-1]
            if (file_ext != ".tif" and file_ext != ".jpg"
                    and file_ext != ".png" and file_ext != ".csv"):
                ui.notify("Please use .tif, .jpg, .png, or .csv as "
                          "file extension!")
            else:
                check = os.path.isfile(file_path)
                if file_ext == ".csv":
                    error = util.save_table(file_path, self.image)
                else:
                    error = util.save_image(file_path, self.image)
                if error is not None:
                    ui.notify(error)
                else:
                    if check:
                        ui.notify(
                            "File {} is overwritten".format(file_path))
                    else:
                        ui.notify("File is saved at: {}".format(file_path))

    async def save_data(self) -> None:
        """To save data to file when click the button 'Save data' """
        file_path = await FileSaver("~", title="File name (ext: .csv)")
        if file_path and self.data_1d_2d is not None:
            file_ext = os.path.splitext(file_path)[-1]
            if file_ext == "":
                file_ext = ".csv"
                file_path = file_path + file_ext
            if file_ext != ".csv":
                ui.notify("Please use .csv as file extension!")
            else:
                check = os.path.isfile(file_path)
                error = util.save_table(file_path, self.data_1d_2d)
                if error is not None:
                    ui.notify(error)
                else:
                    if check:
                        ui.notify(
                            "File {} is overwritten".format(file_path))
                    else:
                        ui.notify(
                            "File is saved at: {}".format(file_path))

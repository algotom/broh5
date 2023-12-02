"""
Module for utility methods:

    -   Get height and with of a screen.
    -   Convert hdf tree to a nested dictionary.
    -   Get data-type and value from a dataset in a hdf file.
    -   Convert 1d/2d array to a table format.
    -   Save 2d array to an image.
    -   Save 1d/2d array to a csv file.
"""

import os
import csv
import tkinter as tk
import h5py
import hdf5plugin
import numpy as np
from PIL import Image


def get_height_width_screen():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_height, screen_width


def __recurse(parent_path, name, obj):
    current_path = f"{parent_path}/{name}" if parent_path else name
    if isinstance(obj, h5py._hl.dataset.Dataset):
        return [{"id": name, "label": current_path}]
    elif isinstance(obj, h5py._hl.group.Group):
        children = []
        for key in obj.keys():
            try:
                child_obj = obj[key]
                child_items = __recurse(current_path, key, child_obj)
                children.extend(child_items)
            except Exception:
                children.append({"id": key, "label": f"{current_path}/{key}"})
        return [{"id": name, "label": current_path, "children": children}]


def hdf_tree_to_dict(hdf_file):
    """Convert an HDF5 tree to a nested dictionary"""
    try:
        hdf_obj1 = h5py.File(hdf_file, 'r')
        result = __recurse("", "", hdf_obj1)
        file_name = os.path.basename(hdf_file)
        result[0]['id'] = file_name
        result[0]['label'] = "/"
        hdf_obj1.close()
        return result
    except Exception as error:
        return str(error)


def get_hdf_data(file_path, dataset_path):
    """ Get data type and value from a hdf dataset """
    with h5py.File(file_path, 'r') as file:
        if dataset_path not in file:
            return "not path", None
        try:
            item = file[dataset_path]
            if isinstance(item, h5py.Group):
                return "group", None
            data_type, value = "unknown", None
            # Check the type and shape of a dataset
            if item.dtype.kind == 'S':  # Fixed-length bytes
                data = item[()]
                if item.size == 1:  # Single string or byte
                    if isinstance(data, bytes):
                        data_type, value = "string", data.decode('utf-8')
                    elif isinstance(data.flat[0], bytes):
                        data_type, value = "string", data.flat[0].decode(
                            'utf-8')
                else:
                    data_type, value = "array", [d.decode('utf-8') for d in
                                                 data]
            elif item.dtype.kind == 'U':  # Fixed-length Unicode
                data = item[()]
                if item.size == 1:  # Single string
                    data_type, value = "string", data
                else:
                    data_type, value = "array", list(data)
            elif h5py.check_dtype(vlen=item.dtype) in [str, bytes]:
                data = item[()]
                if isinstance(data, (str, bytes)):
                    data_type, value = "string", data if isinstance(data, str)\
                        else data.decode('utf-8')
                else:
                    joined_data = ''.join(
                        [d if isinstance(d, str) else d.decode('utf-8')
                         for d in data])
                    data_type, value = "string", joined_data
            elif item.dtype.kind in ['i', 'f', 'u']:
                if item.shape == () or item.size == 1:
                    data_type, value = "number", item[()]
                else:
                    data_type, value = "array", item.shape
            elif item.dtype.kind == 'b':  # Boolean type
                data_type, value = "boolean", int(item[()])
            return data_type, value
        except Exception as error:
            return str(error), None


def check_external_link(file_path, dataset_path):
    """
    Checks if the dataset at the specified path is an external link
    and if it's broken.
    """
    ext_link = False
    broken = False
    msg = ""
    with h5py.File(file_path, 'r') as file:
        if dataset_path in file:
            # Check for external link
            link = file.get(dataset_path, getlink=True)
            if isinstance(link, h5py.ExternalLink):
                ext_link = True
                try:
                    file[dataset_path]
                    msg = "Dataset is an external link"
                except Exception as error:
                    msg = "Dataset is an external link but failed " \
                          "to link. Error: " + str(error)
                    broken = True
        else:
            msg = "Dataset path not found in the file."
    return ext_link, broken, msg


def check_compressed_dataset(file_path, dataset_path):
    """
    Checks if the specified dataset is compressed including checking for
    external compression filters.
    """
    compressed = False
    ext_compressed = False
    msg = ""
    with h5py.File(file_path, 'r') as file:
        if dataset_path in file:
            dataset = file[dataset_path]
            compression = dataset.compression
            # Check for standard compression
            if compression:
                compressed = True
                msg = "Dataset is compressed using standard method: " \
                      "{}".format(compression)
            # Check for external filters
            plist = dataset.id.get_create_plist()
            n_filters = plist.get_nfilters()
            for i in range(n_filters):
                filter_info = plist.get_filter(i)
                if filter_info:
                    msg = "Dataset is compressed using external plugin:" \
                          " {}".format(filter_info[-1])
                    ext_compressed = True
        else:
            msg = "Dataset path not found in the file."
    return compressed, ext_compressed, msg


def format_table_from_array(data):
    if len(data.shape) == 1:
        data = np.expand_dims(np.asarray(data), 1)
    (height, width) = data.shape[:2]
    if height > 1000 and width > 1000:
        rows, columns = None, None
    else:
        fm_data = np.insert(data, 0, np.arange(height), axis=1)
        columns = [{"name": "Column " + str(j), "label": "Column " + str(j),
                    "field": "Column " + str(j)} for j in range(width)]
        columns.insert(0,
                       {"name": "Index", "label": "Index", "field": "Index"})
        rows = []
        for i in range(height):
            dict_tmp = {}
            for j in range(width + 1):
                dict_tmp[columns[j]["name"]] = fm_data[i][j]
            rows.append(dict_tmp)
    return rows, columns


def save_image(file_path, mat):
    """
    Save 2D array to an image.
    """
    file_ext = os.path.splitext(file_path)[-1]
    if not ((file_ext == ".tif") or (file_ext == ".tiff")):
        mat = np.uint8(
            255.0 * (mat - np.min(mat)) / (np.max(mat) - np.min(mat)))
    else:
        if mat.dtype != np.float32:
            mat = mat.astype(np.float32)
    image = Image.fromarray(mat)
    try:
        image.save(file_path)
    except Exception as error:
        return error


def save_table(file_path, data):
    """
    Save 1D/2D numpy array to a CSV file.
    """
    try:
        data = np.asarray(data)
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            if data.ndim == 1:
                for item in data:
                    writer.writerow([item])
            elif data.ndim == 2:
                if data.shape[0] * data.shape[1] < 4000000:
                    writer.writerows(data)
                else:
                    return "Array has more than 4,000,000 elements. " \
                           "Operation not performed."
            else:
                return "Data must be a 1D or 2D array"
    except Exception as error:
        return error

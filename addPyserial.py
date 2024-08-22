#Author-
#Description- Install pyserial and list available serial ports

import adsk.core, adsk.fusion, adsk.cam, traceback
import sys
import os
import urllib.request
import tempfile
import tarfile
import shutil

def install_pyserial():
    url = "https://files.pythonhosted.org/packages/source/p/pyserial/pyserial-3.5.tar.gz"
    scripts_dir = os.path.dirname(os.path.realpath(__file__))
    install_dir = os.path.join(scripts_dir, "pyserial-3.5")
    
    if not os.path.exists(install_dir):
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "pyserial.tar.gz")
            urllib.request.urlretrieve(url, filename)
            with tarfile.open(filename, "r:gz") as tar:
                tar.extractall(path=tmpdir)
            tmp_install_dir = os.path.join(tmpdir, "pyserial-3.5")
            shutil.copytree(tmp_install_dir, install_dir)
    
    if install_dir not in sys.path:
        sys.path.insert(0, install_dir)

    return install_dir

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Install pyserial
        pyserial_path = install_pyserial()
        ui.messageBox(f'PySerial installed at: {pyserial_path}')

        # Print sys.path and directory contents for debugging
        ui.messageBox(f'sys.path: {sys.path}')
        dir_contents = os.listdir(pyserial_path)
        ui.messageBox(f'Directory contents: {dir_contents}')

        # Try to import serial
        import serial
        ui.messageBox(f'PySerial version: {serial.__version__}')

        # Import serial and list ports
        import serial.tools.list_ports
        ports = list(serial.tools.list_ports.comports())

        if ports:
            port_list = "\n".join([f"{p.device}: {p.description}" for p in ports])
            ui.messageBox(f'Available serial ports:\n{port_list}')
        else:
            ui.messageBox('No serial ports found')

    except Exception as e:
        if ui:
            ui.messageBox(f'Failed:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}')

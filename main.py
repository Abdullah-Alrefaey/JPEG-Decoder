import applicationUI as ui
from PyQt5 import QtWidgets, QtGui
import logging
import progress as pr

class JpegDecoder(ui.Ui_MainWindow):
    """
    Main Application (JPEG DECODER) Class.

    This application provides a simple Progressive Decoding
    process.

    =======================================================

    **NOTE**: This app is only for Educational Usages.

    =======================================================

    **Basic Usage**

    - Load a Progressive JPEG image.
    - Follow with the applications visualizations of the
      processes done on a progressive jpeg image.
    """

    def __init__(self, starter_window):
        super(JpegDecoder, self).setupUi(starter_window)
        self.loaded_image = None  # Holds path to loaded Images
        self.jpeg_extracted = None
        self.loaded_image_format = None
        self.progressive = True
        self.results_file = 'results'
        self.test_file = 'tests'
        self.logger = logging.getLogger()  # Logger maintainer
        self.logger.setLevel(logging.DEBUG)
        self.photos = [widget for widget in self.scrollAreaWidgetContents_2.children() if isinstance(widget,
                                                                                                     QtWidgets.QLabel)]

        self.scrollArea.hide()
        self.load.clicked.connect(self.loadFile)

    def loadFile(self):
        """
        Responsible for the following :

        - Loading desired image
        - Passing the image path to main extraction function
        - show the images in their position
        """
        self.statusbar.showMessage("Loading Image File")
        self.loaded_image, self.loaded_image_format = QtWidgets.QFileDialog.getOpenFileName(None,
                                                                                            "Load Image File",
                                                                                            filter="*.jpg;; *.jpeg")
        self.logger.debug("Image File Loaded")

        # CHECK CONDITIONS
        if self.loaded_image == "":
            self.logger.debug("loading cancelled")
            self.statusbar.showMessage("Loading cancelled")
            pass
        else:
            self.logger.debug("starting extraction of data")

            try:
                self.logger.debug("Progressive Image ..")
                self.jpeg_extracted = pr.progress(self.loaded_image)
                self.progressive = True
            except TypeError:
                self.logger.debug("Loaded image %s is not progressive " % self.loaded_image)
                self.showMessage("Warning !", "You need to load a progressive Image",
                                 QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Warning)
                self.progressive = False
                pass
            if self.progressive:
                self.imageLoaded.setPixmap(QtGui.QPixmap(self.loaded_image).scaled(250, 250))
                self.logger.debug("Loaded Image %s" % self.loaded_image)
                self.statusbar.showMessage("Extracting Image ... ")

                self.logger.debug("saving ")
                pr.save_images(self.jpeg_extracted, "results")
                self.logger.debug("Done")

                self.scrollArea.show()

                for indx, widget in enumerate(sorted(self.photos, key=lambda x: x.objectName())):
                    self.logger.debug("Showing results/out%s.jpg" % indx)
                    widget.setPixmap(QtGui.QPixmap("results/out%s.jpg" % indx).scaled(250, 250))
                self.statusbar.clearMessage()
                self.statusbar.showMessage("Images are saved in results/ ")
                
    def showMessage(self, header, message, button, icon):
        """
        Responsible for showing message boxes

        ============= ===================================================================================
        **Arguments**
        header:       Box header title.
        message       the informative message to be shown.
        button:       button type.
        icon:         icon type.
        ============= ===================================================================================
        """
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(header)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStandardButtons(button)
        self.logger.debug("messege shown with %s %s "%(header, message))
        msg.exec_()


if __name__ == '__main__':
    import sys
    logging.basicConfig(filename="logs/logfile.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = JpegDecoder(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


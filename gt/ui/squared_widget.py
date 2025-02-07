"""
Square Widget
"""

import gt.ui.qt_import as ui_qt


class SquaredWidget(ui_qt.QtWidgets.QWidget):
    def __init__(self, parent=None, center_x=True, center_y=True):
        """
        A custom QWidget that displays a square image.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent=parent)
        self.pixmap = ui_qt.QtGui.QPixmap()
        self.center_x = center_x
        self.center_y = center_y

    def center(self, center_x=True, center_y=False):
        """
        Centers the widget horizontally and/or vertically within its parent widget.

        Args:
            center_x (bool, optional): Whether to center the widget horizontally. Default is True.
            center_y (bool, optional): Whether to center the widget vertically. Default is False.
        """
        parent_geometry = self.parent().geometry()

        y = self.geometry().y()
        x = self.geometry().x()

        if center_y:
            y = (parent_geometry.height() - self.height()) / 2

        if center_x:
            x = (parent_geometry.width() - self.width()) / 2
        self.move(x, y)

    def set_pixmap(self, pixmap):
        """
        Set the QPixmap to be displayed in the widget.

        Args:
            pixmap (QPixmap): The QPixmap to be displayed.
        """
        self.pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        """
        Override the paintEvent to draw the QPixmap on the widget.

        Args:
            event (QPaintEvent): The paint event.
        """
        if not self.pixmap.isNull():
            painter = ui_qt.QtGui.QPainter(self)
            painter.setRenderHint(ui_qt.QtLib.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(self.get_image_rect(), self.pixmap)
            self.center(center_x=self.center_x, center_y=self.center_y)

    def get_image_rect(self):
        """
        Calculate the QRect within the widget.

        Returns:
            QRect: The QRect representing the square area.
        """
        widget_rect = self.rect()
        _width = min(widget_rect.width(), widget_rect.height())
        _height = _width

        if not self.pixmap.isNull():  # Re-size but keep aspect ratio
            original_size = self.pixmap.size()
            aspect_ratio = original_size.width() / original_size.height()
            new_height = int(_width / aspect_ratio)
            new_width = int(_height * aspect_ratio)
            if new_height <= _height:
                _height = new_height
            if new_width <= _width:
                _width = new_width

        square_rect = ui_qt.QtCore.QRect(0, 0, _width, _height)
        square_rect.moveCenter(widget_rect.center())
        return square_rect

    def resizeEvent(self, event):
        """
        Override the resizeEvent to maintain a square aspect ratio.

        Args:
            event (QResizeEvent): The resize event.
        """
        new_size = ui_qt.QtCore.QSize(event.size().width(), event.size().height())
        square_size = min(new_size.width(), new_size.height())
        self.resize(square_size, square_size)
        super().resizeEvent(event)


if __name__ == "__main__":
    import gt.ui.resource_library as ui_res_lib
    import gt.ui.qt_utils as ui_t_utils

    with ui_t_utils.QtApplicationContext():
        main_window = ui_qt.QtWidgets.QMainWindow()
        central_widget = SquaredWidget(center_y=False)
        a_pixmap = ui_qt.QtGui.QPixmap(ui_res_lib.Icon.library_missing_file)
        central_widget.set_pixmap(a_pixmap)
        main_window.setCentralWidget(central_widget)
        layout = ui_qt.QtWidgets.QVBoxLayout(central_widget)
        center_widget = ui_qt.QtWidgets.QWidget()
        layout.addWidget(center_widget)
        main_window.show()

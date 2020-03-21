from TouchStyle import *


# a toolbutton with drop shadow
class ShadowButton(QToolButton):
    def __init__(self, icon):
        QToolButton.__init__(self)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(QPointF(3,3))
        self.setGraphicsEffect(shadow)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        pix = QPixmap(icon)
        icon = QIcon(pix)
        self.setIcon(icon)
        self.setIconSize(pix.size())

        # hide shadow while icon is pressed
    def mousePressEvent(self, event):
        self.graphicsEffect().setEnabled(False)
        QToolButton.mousePressEvent(self,event)

    def mouseReleaseEvent(self, event):
        self.graphicsEffect().setEnabled(True)
        QToolButton.mouseReleaseEvent(self,event)
import os
import sys
import random

# Third-party imports.
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt, QRect

def path(src: str) -> str:
    """A function to get the real path of a string for packaging reasons.

    Args:
        src (str): Source directory of the file.

    Returns:
        str: Real path of the file.
    """
    
    # Remove the first / from the src string if present.
    if src[0] == "/":
        src = src[1:]
        
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    
    return os.path.join(base_path, src)

def circular_pixmap(pixmap: QPixmap) -> QPixmap:
    """A function to take a pixmap and crop an eclipse, returning the cropped image.

    Args:
        pixmap (QPixmap): QPixmap object to crop.

    Returns:
        QPixmap: Cropped image as a QPixmap.
    """
    # Get the minimum size of the pixmap - for a 1:1 crop.
    size = min(pixmap.width(), pixmap.height())
    
    # Create a new pixmap, filled with transparency.
    target = QPixmap(size, size)
    target.fill(Qt.GlobalColor.transparent)
    
    # Create a painter with an eclipse path.
    painter = QPainter(target)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)
    
    # Get the QRect centre.
    source_rect = QRect(0, 0, size, size)
    source_rect.moveCenter(pixmap.rect().center())
    
    # Apply the circular crop.
    painter.drawPixmap(target.rect(), pixmap, source_rect)
    painter.end()
    
    # Return the generated pixmap.
    return target

def get_random_profile_pixmap() -> QPixmap:
    """A function to search through the /assets/profiles directory, returning a random image from there as a QPixmap.

    Returns:
        QPixmap: Random image found in the directory.
    """
    profile_assets_dir = path("/assets/profiles")
    
    # List of directories from the profiles directory - contains paths to images.
    profile_images = [f"{profile_assets_dir}/{x}" for x in os.listdir(profile_assets_dir)]
    random_image = random.choice(profile_images) # Random image path from the profile images list.
    
    return QPixmap(random_image)

def get_property(name: str):
    """A function to get a property from the QApplication."""
    return QApplication.instance().property(name)
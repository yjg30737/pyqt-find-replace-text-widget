from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='pyqt-find-replace-text-widget',
    version='0.0.12',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyqt_find_replace_text_widget.ico': ['swap_v.svg', 'close.svg']},
    description='PyQt widget which can find and replace text in the QTextEdit/QTextBrowser',
    url='https://github.com/yjg30737/pyqt-find-replace-text-widget.git',
    long_description_content_type='text/markdown',
    long_description=long_description,
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-find-text-widget>=0.0.1'
    ]
)
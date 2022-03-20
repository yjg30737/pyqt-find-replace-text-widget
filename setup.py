from setuptools import setup, find_packages

setup(
    name='pyqt-find-replace-text-widget',
    version='0.2.0',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyqt_find_replace_text_widget.style': ['button.css'],
                  'pyqt_find_replace_text_widget.ico': ['swap_v.svg', 'close.svg']},
    description='PyQt widget which can find and replace text in the QTextEdit/QTextBrowser',
    url='https://github.com/yjg30737/pyqt-find-replace-text-widget.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-find-text-widget @ git+https://git@github.com/yjg30737/pyqt-find-text-widget.git@main'
    ]
)
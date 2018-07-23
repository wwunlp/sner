import os
import sys
sys.path.append(os.path.abspath('../sner'))

project = 'SNER'
author = 'WWUNLP SNER Team'
copyright = '2017, ' + author

release = '0.1.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]
source_suffix = '.rst'
master_doc = 'index'

pygments_style = 'sphinx'
html_theme = 'alabaster'
html_theme_options = {
    'description': 'Sumerian Named Entity Recognition'
}

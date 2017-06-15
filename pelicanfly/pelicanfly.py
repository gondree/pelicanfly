import os
import sys
from pelican import signals
from fontawesome_markdown import FontAwesomeExtension


def add_md_ext_and_static(peli):
    md_ext = peli.settings.get('MD_EXTENSIONS')
    cls = FontAwesomeExtension
    inst = FontAwesomeExtension()
    try:
        if isinstance(peli.settings.get('MD_EXTENSIONS'), list): # pelican 3.6.3 and earlier
            if not md_ext:
                peli.settings['MD_EXTENSIONS'] = [inst]
            elif not any([isinstance(ext, cls) for ext in md_ext]):
                peli.settings['MD_EXTENSIONS'].append(inst)
        else:
            peli.settings['MARKDOWN'].setdefault('extensions', []).append(inst)
    except:
        sys.excepthook(*sys.exc_info())
        sys.stderr.write("\nError - the fontawesome_markdown extension failed to configure.\n")
        sys.stderr.flush()
    pelifly_static = os.path.join(os.path.split(__file__)[0], 'static')
    peli.settings['THEME_STATIC_PATHS'].append(pelifly_static)


def publish_fontawesome_assets(peli):
    css_file = os.path.join(peli.output_path,
                            'theme',
                            'css',
                            peli.settings['CSS_FILE'])
    with open(css_file, "r+") as f:
        s = f.read()
        f.seek(0)
        f.write("@import url('font-awesome.css');\n" + s)


def register():
    signals.initialized.connect(add_md_ext_and_static)
    signals.finalized.connect(publish_fontawesome_assets)

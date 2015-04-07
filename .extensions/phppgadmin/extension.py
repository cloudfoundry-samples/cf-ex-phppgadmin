"""PHPPgAdmin Extension

Downloads, installs and configures PHPPgAdmin
"""
import os
import os.path
import logging
from build_pack_utils import utils


_log = logging.getLogger('phppgadmin')


DEFAULTS = utils.FormattedDict({
    'PHPPGADMIN_VERSION': '5.1',
    'PHPPGADMIN_PACKAGE': 'phpPgAdmin-{PHPPGADMIN_VERSION}.tar.gz',
    'PHPPGADMIN_HASH': 'ef90fc9942c67ab95f063cacc43911a40d34fbc1',
    'PHPPGADMIN_URL': 'http://downloads.sourceforge.net/project/phppgadmin/'
                      'phpPgAdmin%20%5Bstable%5D/phpPgAdmin-'
                      '{PHPPGADMIN_VERSION}/{PHPPGADMIN_PACKAGE}'
})


# Extension Methods
def preprocess_commands(ctx):
    return ()


def service_commands(ctx):
    return {}


def service_environment(ctx):
    return {}


def compile(install):
    print 'Installing PHPPgAdmin %s' % DEFAULTS['PHPPGADMIN_VERSION']
    ctx = install.builder._ctx
    inst = install._installer
    workDir = os.path.join(ctx['TMPDIR'], 'phppgadmin')
    inst.install_binary_direct(
        DEFAULTS['PHPPGADMIN_URL'],
        DEFAULTS['PHPPGADMIN_HASH'],
        workDir,
        fileName=DEFAULTS['PHPPGADMIN_PACKAGE'],
        strip=True)
    (install.builder
        .move()
        .everything()
        .under('{BUILD_DIR}/htdocs')
        .into(workDir)
        .done())
    (install.builder
        .move()
        .everything()
        .under(workDir)
        .into('{BUILD_DIR}/htdocs')
        .done())
    return 0

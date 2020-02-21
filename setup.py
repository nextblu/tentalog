import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

conf = {
    'name':                             'tentalog',
    'version':                          '0.1.0',
    'description':                      'Utility package for logging in Python',
    'author':                           'NextBlu',
    'author_email':                     'hello@nextblu.com',
    'long_description':                 long_description,
    'long_description_content_type':    'text/markdown',
    'license':                          'MIT',
    'packages':                         setuptools.find_namespace_packages(),
    'url':                              'https://github.com/nextblu/tentalog',
}

setuptools.setup(**conf)

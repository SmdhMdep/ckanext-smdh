[![Tests](https://github.com/SmdhMdep/ckanext-smdh/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/SmdhMdep/ckanext-smdh/actions/workflows/test.yml)

# ckanext-smdh

This extension applies a SMDH specific branding theme. 


## Requirements

This extension does not have any particular requirements as it only changes visual components using dependencies already installed by CKAN 2.9

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| 2.9             | yes   |


## Installation

To install ckanext-smdh:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    ```bash 
    git clone https://github.com/SmdhMdep/ckanext-smdh.git
    cd ckanext-smdh
    pip install -e .
    pip install -r requirements.txt
    ```

3. Add `smdh` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

    ```bash
    sudo service apache2 reload
    ```


## Config settings

None at present


## Developer installation

To install ckanext-smdh for development, activate your CKAN virtualenv and
do:
    
    git clone https://github.com//ckanext-smdh.git
    cd ckanext-smdh
    python setup.py develop
    pip install -r dev-requirements.txt
    
## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## Releasing a new version of ckanext-smdh

If ckanext-smdh should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:
    
    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)

import requests
import tempfile
import zipfile

from picli.linter import base


class CppLint(base.Base):

    def __init__(self, base_config, config):
        super(CppLint, self).__init__(base_config, config)

    @property
    def name(self):
        return 'cpplint'

    @property
    def default_options(self):
        options = self._config.cpplint_options

        return options

    @property
    def url(self):
        return self._base_config._config[f'{self.name}']['url']

    def zip_files(self, destination):
        zip_file = zipfile.ZipFile(f'{destination}/{self.name}.zip', 'w', zipfile.ZIP_DEFLATED)
        for file in self._config.files:
            if file['linter'] == f'{self.name}':
                zip_file.write(file['file'])
        zip_file.close()

        return zip_file

    def execute(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_file = self.zip_files(temp_dir)
            files = [('files', open(zip_file.filename, 'rb'))]
            try:
                r = requests.post(self.url, files=files)
                print(r.text)
            except requests.exceptions.RequestException as e:
                print(e)

import os

from django.conf import settings
from django.test import SimpleTestCase


class LogDirectorySetupTests(SimpleTestCase):
    """Trava a invariante da T-017: o diretório de log tem que existir depois de
    carregar as settings.

    `logs/` está no `.gitignore` e `logging.FileHandler` não cria o diretório
    pai, então sem o `os.makedirs` em `settings.py` toda checkout limpa (CI,
    clone novo, container sem volume) quebra em `django.setup()` antes de rodar
    qualquer teste. Estes testes não reproduzem esse crash — quando ele acontece
    o processo morre antes do test runner subir —, mas documentam por que o
    `makedirs` existe e falham se o `filename` do handler for apontado para fora
    do diretório garantido.
    """

    def test_log_directory_exists_after_settings_load(self):
        self.assertTrue(os.path.isdir(settings.LOG_DIR))

    def test_file_handler_points_into_log_directory(self):
        filename = settings.LOGGING['handlers']['file']['filename']
        self.assertEqual(os.path.dirname(filename), settings.LOG_DIR)

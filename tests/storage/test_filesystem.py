# -*- coding: utf-8 -*-

import pytest

from vdirsyncer.storage.filesystem import FilesystemStorage

from . import StorageTests
from tests import format_item


class TestFilesystemStorage(StorageTests):
    storage_class = FilesystemStorage

    @pytest.fixture
    def get_storage_args(self, tmpdir):
        def inner(collection='test'):
            rv = {'path': str(tmpdir), 'fileext': '.txt', 'collection':
                  collection}
            if collection is not None:
                rv = self.storage_class.create_collection(**rv)
            return rv
        return inner

    def test_is_not_directory(self, tmpdir):
        with pytest.raises(IOError):
            f = tmpdir.join('hue')
            f.write('stub')
            self.storage_class(str(tmpdir) + '/hue', '.txt')

    def test_ident_with_slash(self, tmpdir):
        s = self.storage_class(str(tmpdir), '.txt')
        s.upload(format_item('a/b/c'))
        item_file, = tmpdir.listdir()
        assert '/' not in item_file.basename and item_file.isfile()

    def test_too_long_uid(self, tmpdir):
        s = self.storage_class(str(tmpdir), '.txt')
        item = format_item('hue' * 600)
        href, etag = s.upload(item)
        assert item.uid not in href

    def test_post_hook_active(self, tmpdir):
        s = self.storage_class(str(tmpdir), '.txt', post_hook='rm')
        s.upload(format_item('a/b/c'))
        assert not list(s.list())

    def test_ignore_git_dirs(self, tmpdir):
        tmpdir.mkdir('.git').mkdir('foo')
        tmpdir.mkdir('a')
        tmpdir.mkdir('b')
        assert set(c['collection'] for c
                   in self.storage_class.discover(str(tmpdir))) == {'a', 'b'}

from __future__ import absolute_import

import mock

from ciarlare import testcase
from ciarlare import testing
from ciarlare import FixturesManager
from ciarlare.builder import Builder

fixtures_manager = FixturesManager()
fixtures_manager.load(
    './ciarlare/tests/data/relationships_without_models.yaml')


class TestTestCase(testing.TestCase, testcase.FixturesManagerMixin):

    def _pre_setup(self):
        self.fixtures_manager = fixtures_manager
        self.init_fixtures()
        self.install_fixtures(('simple_dict', 'dict_with_nest'))

    def _post_teardown(self):
        self.uninstall_all_fixtures()

    def test_install_fixture(self):
        """Verify install_fixture should return the installed fixture."""
        self.uninstall_all_fixtures()

        simple_dict = self.install_fixture('simple_dict')
        self.assertEqual(simple_dict['field1'], 'lolin')
        self.assertEqual(simple_dict['field2'], 2)

    def test_install_fixtures(self):
        """Verify install_fixtures should return installed fixtures."""
        self.uninstall_all_fixtures()

        fixtures = self.install_fixtures(('simple_dict', 'dict_with_nest'))
        self.assertEqual(len(fixtures), 2)

    def test_install_all_fixtures(self):
        """Verify it installs all fixtures of the yaml file."""
        self.uninstall_all_fixtures()

        fixtures = self.install_all_fixtures()
        self.assertEqual(len(fixtures), 6)

    def test_uninstall_fixture(self):
        self.uninstall_fixture('simple_dict')
        self.uninstall_fixture('dict_with_nest')
        self.uninstall_all_fixtures()

    def test_uninstall_fixtures(self):
        self.uninstall_fixtures(('simple_dict', 'dict_with_nest'))
        self.uninstall_fixtures(('simple_dict', 'dict_with_nest'))

    def test_uninstall_all_fixtures(self):
        """Verify should uninstall all the installed fixtures.

        The _pre_setup method install the 2 fixtures defined in self.fixtures:
        'simple_dict' and 'dict_with_nest'.
        """
        self.uninstall_all_fixtures()

    def test_get_fixture(self):
        """Verify get_fixture should return the fixture."""
        simple_dict = self.get_fixture('simple_dict')
        self.assertEqual(simple_dict['field1'], 'lolin')
        self.assertEqual(simple_dict['field2'], 2)

        dict_with_nest = self.get_fixture('dict_with_nest')
        self.assertEqual(dict_with_nest['field1'], 'asdlkf')
        self.assertEqual(dict_with_nest['field2'], 4)

    def test_get_fixtures(self):
        """Verify get_fixtures should return the list of fixtures."""
        fixtures = self.get_fixtures(('simple_dict', 'dict_with_nest'))
        self.assertEqual(len(fixtures), 2)

        simple_dict = fixtures[0]
        self.assertEqual(simple_dict['field1'], 'lolin')
        self.assertEqual(simple_dict['field2'], 2)

        dict_with_nest = fixtures[1]
        self.assertEqual(dict_with_nest['field1'], 'asdlkf')
        self.assertEqual(dict_with_nest['field2'], 4)

    @mock.patch('ciarlare.FixturesManager.get_fixture')
    def test_get_fixtures_builder(self, mocked_get_fixture):
        """Verify builder instance passed to inner get_fixture call."""
        builder = Builder()
        self.get_fixtures(('simple_dict', 'dict_with_nest'), builder=builder)

        self.assertEqual(mocked_get_fixture.call_count, 2)
        mocked_get_fixture.assert_any_call('simple_dict', builder=builder)
        mocked_get_fixture.assert_any_call('dict_with_nest', builder=builder)

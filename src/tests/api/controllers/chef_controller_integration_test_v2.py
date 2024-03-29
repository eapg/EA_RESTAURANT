from unittest import mock

from src.api.controllers.chef_controller import ChefController
from src.lib.repositories.impl_v2.chef_repository_impl import ChefRepositoryImpl
from src.tests.lib.repositories.sqlalchemy_base_repository_impl_test import (
    SqlAlchemyBaseRepositoryTestCase,
)

from src.tests.utils.fixtures.mapping_orm_fixtures import build_chef, build_chefs


class ChefRepositoryControllerIntegrationTestCase(SqlAlchemyBaseRepositoryTestCase):
    def after_base_setup(self):

        self.mocked_creation_session_path = mock.patch(
            "src.lib.repositories.impl_v2.chef_repository_impl.create_session",
            return_value=self.mocked_sqlalchemy_session,
        )
        self.chef_repository = mock.Mock(
            wraps=ChefRepositoryImpl(self.mocked_sqlalchemy_engine)
        )
        self.mocked_creation_session_path.start()

        self.chef_controller = ChefController(self.chef_repository)

    def test_add_chef_to_repository_using_controller(self):

        chef = build_chef()

        self.chef_controller.add(chef)
        self.chef_repository.add.assert_called_with(chef)

    def test_get_chef_from_repository_using_controller(self):

        chefs = build_chefs(count=3)

        self.chef_repository.get_by_id.return_value = chefs[2]
        self.chef_controller.add(chefs[0])
        self.chef_controller.add(chefs[1])
        self.chef_controller.add(chefs[2])

        found_chef5 = self.chef_controller.get_by_id(2)

        self.chef_repository.get_by_id.assert_called_with(2)
        self.assertEqual(found_chef5.id, 2)

    def test_get_all_chefs_from_repository_using_controller(self):

        chefs_to_insert = build_chefs(count=4)
        self.chef_repository.get_all.return_value = chefs_to_insert
        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])
        self.chef_controller.add(chefs_to_insert[2])
        self.chef_controller.add(chefs_to_insert[3])

        chefs = self.chef_controller.get_all()

        self.chef_repository.get_all.assert_called_with()

        self.assertEqual(
            chefs,
            [
                chefs_to_insert[0],
                chefs_to_insert[1],
                chefs_to_insert[2],
                chefs_to_insert[3],
            ],
        )

    def test_get_all_chefs_empty_from_repository_through_controller(self):
        self.chef_repository.get_all.return_value = []

        chefs = self.chef_controller.get_all()

        self.chef_repository.get_all.assert_called_with()
        self.assertEqual(chefs, [])

    def test_delete_an_chef_from_repository_using_controller(self):

        chef_to_delete = build_chef()
        chefs_to_insert = build_chefs(count=4)
        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])
        self.chef_controller.add(chefs_to_insert[2])
        self.chef_controller.add(chefs_to_insert[3])

        self.chef_controller.delete_by_id(3, chef_to_delete)
        self.chef_repository.get_all.return_value = [
            chefs_to_insert[0],
            chefs_to_insert[1],
            chefs_to_insert[3],
        ]

        chefs = self.chef_controller.get_all()

        self.chef_repository.delete_by_id.assert_called_once_with(3, chef_to_delete)

        self.assertEqual(
            chefs,
            [
                chefs_to_insert[0],
                chefs_to_insert[1],
                chefs_to_insert[3],
            ],
        )

    def test_update_chef_from_repository_using_controller(self):

        chefs_to_insert = build_chefs(count=2)

        self.chef_controller.add(chefs_to_insert[0])
        self.chef_controller.add(chefs_to_insert[1])

        chef_to_update = build_chef(skill=1)

        self.chef_controller.update_by_id(2, chef_to_update)
        self.chef_repository.get_by_id.return_value = chef_to_update
        updated_chef = self.chef_controller.get_by_id(2)
        self.chef_repository.get_all.return_value = chefs_to_insert
        chefs = self.chef_controller.get_all()

        self.chef_repository.update_by_id.assert_called_once_with(2, chef_to_update)

        self.assertEqual(len(chefs), 2)
        self.assertEqual(updated_chef.skill, chef_to_update.skill)

    def test_get_available_chefs_from_repository_using_controller(self):

        chef_principal = build_chef(
            chef_id=1, name="Elido p", skill=5
        )
        chef_intermediate = build_chef(
            chef_id=2, name="Andres p", skill=3
        )
        chef_basic = build_chef(chef_id=3, name="Juan p", skill=1)

        self.chef_controller.add(chef_principal)
        self.chef_controller.add(chef_intermediate)
        self.chef_controller.add(chef_basic)
        self.chef_repository.get_available_chefs.return_value = [
            chef_principal.id,
            chef_basic.id,
        ]
        available_chefs = self.chef_controller.get_available_chefs()
        self.chef_repository.get_available_chefs.assert_called()
        self.assertEqual(available_chefs, [chef_principal.id, chef_basic.id])

from associations.models import Role
from associations.tests.role.base_test_role import BaseRoleTestCase, ALL_USERS, ALL_USERS_EXCEPT_ADMIN_BIERO


class RoleTestCase(BaseRoleTestCase):
    #########
    # MODEL #
    #########

    def test_permissions(self):
        """Test if the constant Role.PERMISSION_NAMES is exhaustive and if, for each field xxx_permission, Role has the
        corresponding property Role.xxx."""

        for field in Role._meta.get_fields():
            if '_permission' in field.name:
                permission_name = field.name[:-len('_permission')]
                self.assertTrue(hasattr(Role, permission_name), msg=f'{permission_name} property not found in Role.')
                self.assertIn(permission_name, Role.PERMISSION_NAMES,
                              msg=f'{permission_name} not found in Role.PERMISSION_NAMES.')

        for permission_name in Role.PERMISSION_NAMES:
            self.assertTrue(hasattr(Role, permission_name),
                            msg=f'{permission_name} property not found in Role but found in Role.PERMISSION_NAMES.')

    ########
    # LIST #
    ########

    def test_if_not_logged_in_then_cannot_list(self):
        res = self.list()
        self.assertStatusCode(res, 401)

    def if_logged_in_then_can_list(self):
        self.login('17simple')
        res = self.list()
        self.assertStatusCode(res, 200)
        for association in res.data:
            self.assertSetEqual(set(association.keys()), set(self.SERIALIZED_FIELDS))

    ############
    # RETRIEVE #
    ############

    def test_if_not_logged_in_then_cannot_retrieve(self):
        res = self.retrieve(0)
        self.assertStatusCode(res, 401)

    def test_if_logged_in_then_can_retrieve(self):
        self.login('17simple')
        res = self.retrieve(0)
        self.assertStatusCode(res, 200)
        self.assertSetEqual(set(res.data), set(self.SERIALIZED_FIELDS))

    ##########
    # CREATE #
    ##########

    def test_if_global_admin_then_can_create_role_with_valid_data(self):
        self.login('17admin')
        res = self.create(self.global_admin_create_role_data)
        self.assertStatusCode(res, 201)

        last_role = Role.objects.order_by('-id')[0]
        for field, value in self.global_admin_create_role_data.items():
            compare_to = getattr(last_role, field).id if hasattr(getattr(last_role, field), 'id') \
                else getattr(last_role, field)
            self.assertEqual(value, compare_to, msg=f'Field {field} not equal.')

    def test_if_global_admin_then_cannot_create_role_with_invalid_data(self):
        self.login('17admin')
        res = self.create(self.global_admin_create_role_invalid_data)
        self.assertStatusCode(res, 201)

        last_role = Role.objects.order_by('-id')[0]
        for field, value in self.global_admin_create_role_data.items():
            if field in self.GLOBAL_ADMIN_ALLOWED_FIELDS:
                compare_to = getattr(last_role, field).id if hasattr(getattr(last_role, field), 'id') \
                    else getattr(last_role, field)
                self.assertEqual(value, compare_to, msg=f'Field {field} not equal.')
            else:
                compare_to = getattr(last_role, field).id if hasattr(getattr(last_role, field), 'id') \
                    else getattr(last_role, field)
                self.assertNotEqual(value, compare_to, msg=f'Field {field} equal.')

    def test_if_association_admin_then_can_create_role_with_valid_data(self):
        self.login('17admin_biero')
        res = self.create(self.association_admin_create_role_data)
        self.assertStatusCode(res, 201)

        last_role = Role.objects.order_by('-id')[0]
        for field, value in self.association_admin_create_role_data.items():
            compare_to = getattr(last_role, field).id if hasattr(getattr(last_role, field), 'id') \
                else getattr(last_role, field)
            self.assertEqual(value, compare_to, msg=f'Field {field} not equal.')

    def test_if_association_admin_then_cannot_create_role_with_invalid_data(self):
        self.login('17admin_biero')
        res = self.create(self.association_admin_create_role_invalid_data)
        self.assertStatusCode(res, 201)

        last_role = Role.objects.order_by('-id')[0]
        for field, value in self.association_admin_create_role_invalid_data.items():
            if field in self.ASSOCIATION_ADMIN_ALLOWED_FIELDS:
                compare_to = getattr(last_role, field).id if hasattr(getattr(last_role, field), 'id') \
                    else getattr(last_role, field)
                self.assertEqual(value, compare_to, msg=f'Field {field} not equal.')
            else:
                compare_to = getattr(last_role, field).id if hasattr(getattr(last_role, field), 'id') \
                    else getattr(last_role, field)
                self.assertNotEqual(value, compare_to, msg=f'Field {field} equal.')

    def test_if_not_admin_then_cannot_create_role_with_full_data(self):
        for user in ALL_USERS:
            if user != '17admin_biero' and user != '17admin':
                length_before = len(Role.objects.all())

                self.login(user)
                res = self.create(self.association_admin_create_role_data)
                self.assertStatusCode(res, 403)

                self.assertEqual(length_before, len(Role.objects.all()), msg=f'User {user} managed to create a role.')

    def test_if_association_admin_then_cannot_create_other_association_role(self):
        for user in ALL_USERS:
            if user != '17admin_pdm' and user != '17admin':
                length_before = len(Role.objects.all())

                self.login(user)
                res = self.create(self.association_admin_create_role_for_pdm)
                self.assertStatusCode(res, 403)

                self.assertEqual(length_before, len(Role.objects.all()), msg=f'User {user} managed to create a role.')

    ##########
    # UPDATE #
    ##########

    full_update_role_data = {
        'id': 0,
        'role': 'Piche',
        'rank': 42,
        'is_archived': True,
        'administration_permission': False,
        'election_permission': True,
        'events_permission': True,
        'filesystem_permission': True,
        'library_permission': True,
        'marketplace_permission': True,
        'page_permission': True,
    }

    def test_if_not_association_admin_then_cannot_full_update(self):
        for user in ALL_USERS:
            if user != '17admin_biero' and user != '17admin':
                self.login(user)
                res = self.update(0, data=self.full_update_role_data)
                self.assertStatusCode(res, 403)

    def test_if_association_admin_then_can_full_update(self):
        self.login('17admin_biero')

        res = self.update(0, data=self.full_update_role_data)
        self.assertStatusCode(res, 200)

        role = Role.objects.get(pk=0)
        for field, value in self.full_update_role_data.items():
            if field != 'id':  # Skip id 'coz equal ofc.
                compare_to = getattr(role, field).id if hasattr(getattr(role, field), 'id') \
                    else getattr(role, field)
                self.assertEqual(value, compare_to, msg=f'Field {field} not equal.')

    def test_if_global_admin_then_can_limited_update(self):
        self.login('17admin')

        res = self.update(0, data=self.full_update_role_data)
        self.assertStatusCode(res, 200)

        role = Role.objects.get(pk=0)
        for field, value in self.full_update_role_data.items():
            if field != 'id':  # Skip id 'coz equal ofc.
                if field in self.GLOBAL_ADMIN_ALLOWED_FIELDS:
                    compare_to = getattr(role, field).id if hasattr(getattr(role, field), 'id') \
                        else getattr(role, field)
                    self.assertEqual(value, compare_to, msg=f'Field {field} not equal.')
                else:
                    compare_to = getattr(role, field).id if hasattr(getattr(role, field), 'id') \
                        else getattr(role, field)
                    self.assertNotEqual(value, compare_to, msg=f'Field {field} equal.')

    def test_cannot_update_user(self):
        self.login('17admin_biero')

        role_before = Role.objects.get(pk=0)
        res = self.update(0, data={'id':0, 'user': '17admin_pdm'})
        self.assertStatusCode(res, 200)
        self.assertEqual(Role.objects.get(pk=0), role_before)

    def test_cannot_update_association(self):
        self.login('17admin_biero')

        role_before = Role.objects.get(pk=0)
        res = self.update(0, data={'id': 0, 'association': 'pdm'})
        self.assertStatusCode(res, 200)
        self.assertEqual(Role.objects.get(pk=0), role_before)

    ###########
    # DESTROY #
    ###########

    def test_if_not_association_admin_then_cannot_destroy(self):
        for user in ALL_USERS_EXCEPT_ADMIN_BIERO:
            self.login(user)
            res = self.destroy(0)
            self.assertStatusCode(res, 403)
            self.assertTrue(Role.objects.filter(pk=0).exists())

    def test_if_association_admin_then_can_destroy_own_association_role(self):
        self.login('17admin_biero')
        res = self.destroy(0)
        self.assertStatusCode(res, 204)
        self.assertFalse(Role.objects.filter(pk=0).exists())

# Copyright 2017-2019 MuK IT GmbH.
# Copyright 2020 Creu Blanca
# Copyright 2021-2022 Tecnativa - Víctor Martínez
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64

from odoo.exceptions import UserError
from odoo.tests import new_test_user
from odoo.tests.common import users

from .common import StorageFileBaseCase

try:
    import magic
except ImportError:
    magic = None


class FileFilestoreTestCase(StorageFileBaseCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_a = new_test_user(cls.env, login="user-a", groups="dms.group_dms_user")
        cls.group_a = cls.access_group_model.create(
            {
                "name": "Group A",
                "perm_create": True,
                "explicit_user_ids": [(6, 0, [cls.user_a.id])],
            }
        )
        cls.directory_group_a = cls.create_directory(storage=cls.storage)
        cls.directory_group_a.group_ids = [(4, cls.group_a.id)]
        cls.sub_directory_x = cls.create_directory(directory=cls.directory_group_a)
        cls.file2 = cls.create_file(directory=cls.sub_directory_x)

    @users("user-a")
    def test_file_access(self):
        dms_files = self.file_model.with_user(self.env.user).search(
            [("storage_id", "=", self.storage.id)]
        )
        self.assertNotIn(self.file.id, dms_files.ids)
        self.assertIn(self.file2.id, dms_files.ids)
        dms_directories = self.directory_model.with_user(self.env.user).search(
            [("storage_id", "=", self.storage.id)]
        )
        self.assertNotIn(self.directory.id, dms_directories.ids)
        self.assertIn(self.sub_directory_x.id, dms_directories.ids)

    @users("dms-manager", "dms-user")
    def test_content_file(self):
        lobject_file = self.create_file(directory=self.directory)
        self.assertTrue(lobject_file.content)
        self.assertTrue(lobject_file.content_file)
        self.assertTrue(lobject_file.with_context(bin_size=True).content)
        self.assertTrue(lobject_file.with_context(bin_size=True).content_file)
        self.assertTrue(lobject_file.with_context(human_size=True).content_file)
        self.assertTrue(lobject_file.with_context(base64=True).content_file)
        self.assertTrue(lobject_file.with_context(stream=True).content_file)
        oid = lobject_file.with_context(oid=True).content_file
        self.assertTrue(oid)
        lobject_file.with_context(**{"show_content": True}).write(
            {"content": base64.b64encode(b"\xff new content")}
        )
        self.assertNotEqual(
            oid, lobject_file.with_context(**{"oid": True}).content_file
        )
        self.assertTrue(lobject_file.export_data(["content"]))
        lobject_file.unlink()

    def test_content_file_mimetype(self):
        file_svg = self.env.ref("dms.file_05_demo")
        self.assertEqual(file_svg.mimetype, "image/svg+xml")
        file_logo = self.env.ref("dms.file_02_demo")
        self.assertEqual(file_logo.mimetype, "image/jpeg")

    def test_content_file_mimetype_magic_library(self):
        if not magic:
            self.skipTest("Without python-magic library installed")
        file_video = self.env.ref("dms.file_10_demo")
        self.assertEqual(file_video.mimetype, "video/mp4")

    def test_content_file_extension(self):
        file_pdf = self.env.ref("dms.file_27_demo")
        self.assertEqual(file_pdf.extension, "pdf")
        file_pdf.name = "Document_05"
        self.assertEqual(file_pdf.extension, "pdf")
        file_pdf.name = "Document_05.pdf"
        self.assertEqual(file_pdf.extension, "pdf")

    def test_wizard_dms_file_move(self):
        file3 = self.create_file(directory=self.sub_directory_x)
        all_files = self.file + self.file2 + file3
        # Error: All files must have the same root directory
        with self.assertRaises(UserError):
            self.file_model.with_context(
                active_ids=all_files.ids
            ).action_wizard_dms_file_move()
        # Change the files that have the same root directory
        files = self.file2 + file3
        res = self.file_model.with_context(
            active_ids=files.ids
        ).action_wizard_dms_file_move()
        wizard_model = self.env[res["res_model"]].with_context(**res["context"])
        wizard = wizard_model.create({"directory_id": self.directory.id})
        self.assertEqual(wizard.count_files, 2)
        wizard.process()
        self.assertEqual(self.file2.directory_id, self.directory)
        self.assertEqual(file3.directory_id, self.directory)

from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Note

class NotesAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.note = Note.objects.create(
            body="Initial note body"
        )

    def test_get_all_notes(self):
        response = self.client.get("/api/notes/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_get_single_note(self):
        response = self.client.get(f"/api/notes/{self.note.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["body"], "Initial note body")

    def test_create_note(self):
        response = self.client.post("/api/notes/create/", {
            "body": "New test note"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 2)

    def test_update_note(self):
        response = self.client.put(
            f"/api/notes/{self.note.id}/update/",
            {"body": "Updated note"},
            format="json"
        )
        self.assertEqual(response.status_code, 200)

        self.note.refresh_from_db()
        self.assertEqual(self.note.body, "Updated note")

    def test_delete_note(self):
        response = self.client.delete(
            f"/api/notes/{self.note.id}/delete/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 0)

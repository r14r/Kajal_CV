from django.test import Client, TestCase
from django.urls import reverse
from .models import Task


class TaskBoardTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get(reverse("home"))
        self.csrf = self.client.cookies["csrftoken"].value

    def post(self, path, data):
        return self.client.post(path, data, HTTP_X_CSRFTOKEN=self.csrf)

    def test_create_filter_toggle_delete(self):
        add = reverse("add_task")
        self.assertEqual(self.client.post(add, {"title": "Unauthorised"}).status_code, 403)
        invalid = self.post(add, {"title": "", "note": "x"})
        self.assertEqual(invalid.status_code, 200)
        self.assertEqual(invalid["HX-Retarget"], "#task-form")
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(self.post(add, {"title": "Study Django", "note": "Models"}).status_code, 200)
        task = Task.objects.get()
        self.assertContains(self.client.get(reverse("tasks")+"?filter=open"), "Study Django")
        self.assertNotContains(self.client.get(reverse("tasks")+"?filter=done"), "Study Django")
        self.assertEqual(self.post(reverse("toggle_task", args=[task.pk]), {"filter": "done"}).status_code, 200)
        self.assertTrue(Task.objects.get(pk=task.pk).done)
        self.assertContains(self.client.get(reverse("tasks")+"?filter=done"), "Study Django")
        self.assertEqual(self.post(reverse("delete_task", args=[task.pk]), {}).status_code, 200)
        self.assertEqual(Task.objects.count(), 0)

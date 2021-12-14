import unittest
import requests


class ApiTest(unittest.TestCase):
    API_URL = "http://192.168.1.2:5000/tasks"
    task_obj = {
        "task_id": 1,
        "task_title": "first task",
        "task_state": "draft"
    }

    # get all existing tasks
    def test_1_get_all_tasks(self):
        r = requests.get(ApiTest.API_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 0)

    # add new task
    def test_2_add_new_task(self):
        id = 1
        r = requests.post(f"{ApiTest.API_URL}/{id}", json=ApiTest.task_obj)
        self.assertEqual(r.status_code, 201)

    # get the new task
    def test_3_get_new_task(self):
        id = 1
        r = requests.get(f"{ApiTest.API_URL}/{id}")
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), ApiTest.task_obj)

    # update the new task (move forward to active state)
    def test_4_update_existing_task_1(self):
        id = 1
        new_task_obj = {
            "task_id": 1,
            "task_title": "first task updated",
            "task_state": "active"
        }
        r = requests.put(f"{ApiTest.API_URL}/{id}", json=new_task_obj)
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), new_task_obj)

    # update the new task (move backward to the draft state)
    def test_4_update_existing_task_2(self):
        id = 1
        new_task_obj = {
            "task_id": 1,
            "task_title": "first task updated",
            "task_state": "draft"
        }
        r = requests.put(f"{ApiTest.API_URL}/{id}", json=new_task_obj)
        self.assertEqual(r.status_code, 409)

    # continue to the done state
    def test_4_update_existing_task_3(self):
        id = 1
        new_task_obj = {
            "task_id": 1,
            "task_title": "first task updated",
            "task_state": "done"
        }
        r = requests.put(f"{ApiTest.API_URL}/{id}", json=new_task_obj)
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), new_task_obj)

    # reach the archived state
    def test_4_update_existing_task_4(self):
        id = 1
        new_task_obj = {
            "task_id": 1,
            "task_title": "first task updated",
            "task_state": "archived"
        }
        r = requests.put(f"{ApiTest.API_URL}/{id}", json=new_task_obj)
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), new_task_obj)

    # trying to move backward after the archived state
    def test_4_update_existing_task_5(self):
        id = 1
        new_task_obj = {
            "task_id": 1,
            "task_title": "first task updated",
            "task_state": "active"
        }
        r = requests.put(f"{ApiTest.API_URL}/{id}", json=new_task_obj)
        self.assertEqual(r.status_code, 409)

    # delete the existing task
    def test_5_delete_existing_task(self):
        id = 1
        r = requests.delete(f"{ApiTest.API_URL}/{id}")
        self.assertEqual(r.status_code, 204)

    # trying to get the task after deleted
    def test_6_get_task_after_deleted(self):
        id = 1
        r = requests.get(f"{ApiTest.API_URL}/{id}")
        self.assertEqual(r.status_code, 404)

    # add new task again
    def test_7_add_new_task_again(self):
        id = 1
        r = requests.post(f"{ApiTest.API_URL}/{id}", json=ApiTest.task_obj)
        self.assertEqual(r.status_code, 201)

    # jump directly to the archived state
    def test_8_update_existing_task(self):
        id = 1
        new_task_obj = {
            "task_id": 1,
            "task_title": "first task updated",
            "task_state": "archived"
        }
        r = requests.put(f"{ApiTest.API_URL}/{id}", json=new_task_obj)
        self.assertEqual(r.status_code, 200)
        self.assertDictEqual(r.json(), new_task_obj)

    # delete the existing task
    def test_9_delete_existing_task(self):
        id = 1
        r = requests.delete(f"{ApiTest.API_URL}/{id}")
        self.assertEqual(r.status_code, 204)


if __name__ == '__main__':
    unittest.main()

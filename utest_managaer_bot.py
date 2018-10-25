import unittest
import manager_bot as m


class MyTestCase(unittest.TestCase):
    def test_generate_names_workers(self):
        self.assertEqual(len(set(m.generate_names_workers(10))), 10)

    def test_create_worker(self):

        result = {'name': 'Anna', 'productivity': 10, 'tasks': []}
        self.assertEqual(result, m.create_worker('Anna', 10))

    @staticmethod
    def test_generate_workers():
        for worker in m.generate_workers(10, 1, 10):
            print(worker)

    def test_generate_names_tasks(self):
        self.assertEqual(len(set(m.generate_names_tasks(10))), 10)

    def test_create_task(self):

        result = {'name': 'серверный цифровой комплекс', 'complexity': 54}
        self.assertEqual(result, m.create_task('серверный цифровой комплекс', 54))

    @staticmethod
    def test_generate_tasks():
        for task in m.generate_tasks(10, 30, 90):
            print(task)

    @staticmethod
    def test_round_robin():
        workers = m.generate_workers(10, 1, 10)
        tasks = m.generate_tasks(43, 50, 90)

        for worker in m.round_robin(workers, tasks):
            print(worker['tasks'])

    def test_redistributes_tasks(self):
        workers = m.generate_workers((5, 5), 1, 10)
        tasks = m.generate_tasks((10, 10), 50, 90)
        workers = m.round_robin(workers, tasks)
        r1 = workers[0]['tasks'][0]
        r2 = workers[1]['tasks'][0]
        r3 = workers[-2]['tasks'][0]
        r4 = workers[-1]['tasks'][0]
        m.redistributes_tasks(workers)
        self.assertEqual(r1, workers[1]['tasks'][0])
        self.assertEqual(r2, workers[2]['tasks'][0])
        self.assertEqual(r3, workers[-1]['tasks'][0])
        self.assertEqual(r4, workers[0]['tasks'][0])


if __name__ == '__main__':
    unittest.main()

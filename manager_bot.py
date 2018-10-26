from mimesis import Person
from random import randint, choice
from threading import Timer


def generate_names_workers(count):
    """
    Возвращает случайные имена исполнителей
    """
    person = Person('ru')
    return [person.full_name() for _ in range(count)]


def generate_names_tasks(count):
    """
    Возвращает случайные имена задач
    """
    adjective = [
        'цифровой',
        'онлайновый',
        'автоматический',
        'компьютерный',
        'облачный',
        'конфиденциальный',
        'совместимый',
        'аппаратный',
        'серверный'
    ]
    noun = [
        'продукт',
        'проект',
        'комплекс'
    ]
    tasks = []
    while len(tasks) != count:

        new_task = []
        while len(new_task) < 2:
            word = choice(adjective)
            if word not in new_task:
                new_task.append(word)

        new_task = ' '.join(new_task) + ' ' + choice(noun)
        if new_task not in tasks:
            tasks.append(new_task)

    return tasks


def generate_complexity_tasks(count, mn, mx):
    """
    Возвращает случайные единицы сложности
    """
    return [randint(mn, mx) for _ in range(count)]


def generate_productivity_workers(count, mn, mx):
    """
    Возвращает случайные единицы продуктивности
    """
    return [randint(mn, mx) for _ in range(count)]


def create_task(name, complexity):
    """
    Возвращает задачу
    """
    task = dict()
    task['name'] = name
    task['complexity'] = complexity
    return task


def create_worker(name, productivity):
    """
    Возвращает исполнителя
    """
    worker = dict()
    worker['name'] = name
    worker['productivity'] = productivity
    worker['tasks'] = []
    return worker


def generate_tasks(count, mn, mx):
    """
    Возвращает список задач
    """
    count = randint(count[0], count[1])
    names = generate_names_tasks(count)
    complexity = generate_complexity_tasks(count, mn, mx)

    tasks = []
    for i in range(len(names)):
        task = create_task(names[i], complexity[i])
        tasks.append(task)
    return tasks


def generate_workers(count, mn, mx):
    """
    Возвращает список исполнителей
    """
    count = randint(count[0], count[1])
    names = generate_names_workers(count)
    productivity = generate_productivity_workers(count, mn, mx)

    workers = []
    for i in range(len(names)):
        worker = create_worker(names[i], productivity[i])
        workers.append(worker)
    return workers


def round_robin(workers, tasks):
    """
    Распределяет задачи по исполнителям
    :return: workers с задачами
    """
    i = 0
    for task in tasks:
        if i > len(workers) - 1:
            i = 0
        workers[i]['tasks'].append(task)
        i += 1
    return workers


def redistributes_tasks(workers):
    count = 1
    for worker in workers:
        if worker['tasks']:
            if count > len(workers) - 1:
                workers[0]['tasks'].insert(0, worker['tasks'].pop(0))
                break
            workers[count]['tasks'].insert(1, worker['tasks'].pop(0))
            count += 1

    return workers


class InfiniteTimer:
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        stop_timer = self.target()
        if stop_timer:
            self.thread.cancel()
            self._should_continue = False
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue:  # Code could have been running when cancel was called.
            self.thread = Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")

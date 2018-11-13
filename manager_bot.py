from mimesis import Person
from random import randint, choice
from threading import Timer


def generate_random_names_workers(count):
    person = Person('ru')
    return [person.full_name() for _ in range(count)]


def choice_random_adjective():
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
    return choice(adjective)


def choice_random_noun():
    noun = [
        'продукт',
        'проект',
        'комплекс'
    ]
    return choice(noun)


def generate_unique_adjectives(count):
    adjectives = []
    while len(adjectives) < count:
        adjective = choice_random_adjective()
        if adjective not in adjectives:
            adjectives.append(adjective)

    return adjectives


def generate_random_names_tasks(count):
    tasks = []
    while len(tasks) != count:
        adjectives = generate_unique_adjectives(2)
        new_name_task = ' '.join(adjectives) + ' ' + choice_random_noun()
        if new_name_task not in tasks:
            tasks.append(new_name_task)
    return tasks


def generate_complexity_tasks(count, mn, mx):
    return [randint(mn, mx) for _ in range(count)]


def generate_productivity_workers(count, mn, mx):
    return [randint(mn, mx) for _ in range(count)]


def create_task(name, complexity):
    task = dict()
    task['name'] = name
    task['complexity'] = complexity
    return task


def create_tasks(names, complexities):
    tasks = []
    for i in range(len(names)):
        task = create_task(names[i], complexities[i])
        tasks.append(task)
    return tasks


def create_worker(name, productivity):
    worker = dict()
    worker['name'] = name
    worker['productivity'] = productivity
    worker['tasks'] = []
    return worker


def create_workers(names, performances):
    workers = []
    for i in range(len(names)):
        worker = create_worker(names[i], performances[i])
        workers.append(worker)
    return workers


def generate_tasks(min_max_count_tasks, min_max_complexity):
    min_count_tasks = min_max_count_tasks[0]
    max_count_tasks = min_max_count_tasks[1]
    min_complexity = min_max_complexity[0]
    max_complexity = min_max_complexity[1]
    count_tasks = randint(min_count_tasks, max_count_tasks)
    names = generate_random_names_tasks(count_tasks)
    complexities = generate_complexity_tasks(count_tasks, min_complexity,
                                             max_complexity)

    return create_tasks(names, complexities)


def generate_workers(min_max_count_workers, min_max_performance):
    min_count_workers = min_max_count_workers[0]
    max_count_workers = min_max_count_workers[1]
    min_performance = min_max_performance[0]
    max_performance = min_max_performance[1]
    count_workers = randint(min_count_workers, max_count_workers)
    names = generate_random_names_workers(count_workers)
    performances = generate_productivity_workers(count_workers, min_performance,
                                                 max_performance)

    return create_workers(names, performances)


def round_robin(workers, tasks):
    i = 0
    for task in tasks:
        if i > len(workers) - 1:
            i = 0
        workers[i]['tasks'].append(task)
        i += 1
    return workers


def redistributes_tasks(workers):
    for count, worker in enumerate(workers):
        if worker['tasks']:
            if count + 1 > len(workers) - 1:
                workers[0]['tasks'].insert(0, worker['tasks'].pop(0))
                break
            if len(workers[count]['tasks']) > 1:
                workers[count + 1]['tasks'].insert(1, worker['tasks'].pop(0))

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
        if self._should_continue:
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
            self._should_continue = False
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")

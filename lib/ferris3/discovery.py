import os
import importlib
import inspect
from protorpc import remote


base_directory = os.path.abspath(os.getcwd())
app_directory = os.path.join(base_directory, 'app')


def discover_api_services():
    api_module_files = discover_files(lambda x: x.endswith('_api.py'))
    modules = load_modules_from_files(api_module_files)
    apis = find_api_classes(modules)
    return [x[1] for x in apis]


def discover_files(predicate):
    results = []
    for root_path, _, files in os.walk(app_directory):
        for filename in files:
            if predicate(filename):
                results.append(os.path.join(root_path, filename))
    return results


def load_modules_from_files(files):
    modules = []
    for filename in files:
        # /home/.../app/thing/thing_api.py -> app/thing/thing_api.py
        relative_path = os.path.relpath(filename, base_directory)
        # app/thing/thing_api.py -> app/thing/thing_api
        module_path, ext = os.path.splitext(relative_path)
        # app/thing/thing_api -> app.thing.thing_api
        import_path = '.'.join(module_path.split(os.sep))
        
        module = importlib.import_module(import_path)
        modules.append(module)
    return modules


def find_api_classes(modules):
    classes = []
    for module in modules:
        apis = inspect.getmembers(module, lambda x: inspect.isclass(x) and is_remote_service(x))
        classes.extend(apis)
    return classes

def is_remote_service(cls):
    # This is kind of an ugly hack, for some reason issubclass doesn't always work.
    for mro in inspect.getmro(cls):
        if mro.__module__ == remote.Service.__module__ and mro.__name__ == remote.Service.__name__:
            return True
    return False

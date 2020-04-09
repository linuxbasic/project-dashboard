from django import template

register = template.Library()


def to_gantt_row(task_id, task_name, start=None, end=None, duration=None, percent_complete=None, dependencies=[],
                 resource_id=None):
    row = ["'{}'".format(task_id)]

    row.append("'{}'".format(task_name))
    row.append("'{}'".format(resource_id) if resource_id else 'null')
    row.append("new Date('{}')".format(start) if start else 'null')
    row.append("new Date('{}')".format(end) if end else 'null')
    row.append('daysToMilliseconds({})'.format(duration) if duration else 'null')
    row.append(str(percent_complete) if percent_complete else 'null')
    row.append("'{}'".format(','.join(map(str, dependencies))) if dependencies else 'null')

    return '[{}],'.format(', '.join(row))


phase_id_tpl = 'phase-{}'
task_id_tpl = 'task-{}'


def get_dependencies(model, id_tpl):
    if model.predecessor:
        return [id_tpl.format(model.predecessor.id)]
    return []


@register.simple_tag
def print_phase_row(phase):
    phase_id = phase_id_tpl.format(phase.id)
    duration = phase.get_planned_duration()
    dependencies = get_dependencies(phase, phase_id_tpl)
    start_date = None
    if not dependencies:
        start_date = phase.get_start_date()
    return to_gantt_row(task_id=phase_id, resource_id=phase_id, task_name=phase.name, duration=duration,
                        dependencies=dependencies, start=start_date)


@register.simple_tag
def print_task_row(task):
    dependencies = get_dependencies(task, task_id_tpl)
    task_id = task_id_tpl.format(task.id)
    phase_id = phase_id_tpl.format(task.phase.id)
    start_date = None
    if not dependencies:
        start_date = task.phase.get_start_date()
    return to_gantt_row(task_id=task_id, resource_id=phase_id, task_name=task.name, duration=task.planned_duration,
                        dependencies=dependencies, start=start_date)

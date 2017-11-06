from django import template

register = template.Library()


@register.filter
def planned_resource_duration(resource, project):
    return sum([phase.get_planned_duration() for phase in resource.tasks.filter(phase__project=project) if
                phase.get_end_date() <= project.today()])


@register.filter
def resource_duration(resource, project):
    return sum([phase.get_duration() for phase in resource.tasks.filter(phase__project=project) if
                phase.get_end_date() <= project.today()])


@register.filter
def planned_resource_cost(resource, project):
    return sum([phase.get_planned_duration() * resource.cost for phase in resource.tasks.filter(phase__project=project) if
                phase.get_end_date() <= project.today()])


@register.filter
def resource_cost(resource, project):
    return sum([phase.get_duration() * resource.cost for phase in resource.tasks.filter(phase__project=project) if
                phase.get_end_date() <= project.today()])


@register.filter
def resource_cost_delta(resource, project):
    planned_cost = planned_resource_cost(resource, project)
    actual_cost = resource_cost(resource, project)
    return actual_cost / planned_cost

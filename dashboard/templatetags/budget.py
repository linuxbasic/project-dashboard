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
    return sum(
        [phase.get_planned_duration() * resource.cost for phase in resource.tasks.filter(phase__project=project) if
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


@register.filter
def phase_cost_delta(phase):
    return phase.get_cost() / phase.get_planned_cost()


@register.filter
def cost(earning, project):
    cost_total = project.get_cost(earning.date)
    cost_last_earning = 0
    last_earning = project.earnings.filter(date__lt=earning.date).first()
    if last_earning:
        cost_last_earning = project.get_cost(last_earning.date)
    return cost_total - cost_last_earning


@register.filter
def contract_delta(earning, project):
    spent = cost(earning, project)
    earned = earning.value
    return earned / spent

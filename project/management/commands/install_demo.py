from django.core.management.base import BaseCommand
from project.models import (Project, Resource)
from datetime import datetime
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        project_manager_resource = Resource.objects.create(name='Project Manager', cost=200)
        architect_resource = Resource.objects.create(name='Software Architect', cost=250)
        business_analyst_resource = Resource.objects.create(name='Business Analyst', cost=180)
        developer_resource = Resource.objects.create(name='Development Team', cost=1500)
        ux_resource = Resource.objects.create(name='UX Designer', cost=120)
        dba_resource = Resource.objects.create(name='Database Administrator', cost=210)
        qa_resource = Resource.objects.create(name='Quality Assurance Manager', cost=100)
        ops_resource = Resource.objects.create(name='Operations Manager', cost=180)

        project = Project.objects.create(name='Demo Project', start_date='2017-08-25')

        phase_1 = project.phases.create(name='Kickoff')

        task_1_1 = phase_1.tasks.create(name='Kickoff planen', planned_duration=1)
        task_1_1.resources.add(project_manager_resource)

        task_1_2 = phase_1.tasks.create(name='Kickoff durchführen', planned_duration=1, predecessor=task_1_1)
        task_1_2.resources.add(project_manager_resource)
        task_1_2.resources.add(architect_resource)
        task_1_2.resources.add(business_analyst_resource)

        task_1_3 = phase_1.tasks.create(name='Stakeholder onboarden', planned_duration=3, predecessor=task_1_2)
        task_1_3.resources.add(project_manager_resource)
        task_1_3.resources.add(business_analyst_resource)
        task_1_3.duration_predictions.create(date='2017-08-28', duration=2)

        phase_2 = project.phases.create(name='Anforderungen', predecessor=phase_1)

        task_2_1 = phase_2.tasks.create(name='Anforderungen Abt. A ermitteln', planned_duration=3)
        task_2_1.resources.add(project_manager_resource)
        task_2_1.resources.add(business_analyst_resource)
        task_2_1.duration_predictions.create(date='2017-08-29', duration=2)

        task_2_2 = phase_2.tasks.create(name='Anforderungen Abt. B ermitteln', planned_duration=1, predecessor=task_2_1)
        task_2_2.resources.add(project_manager_resource)
        task_2_2.resources.add(business_analyst_resource)
        task_2_2.duration_predictions.create(date='2017-08-30', duration=2)

        task_2_3 = phase_2.tasks.create(name='Anforderungen Abt. C ermitteln', planned_duration=1, predecessor=task_2_2)
        task_2_3.resources.add(project_manager_resource)
        task_2_3.resources.add(business_analyst_resource)

        phase_3 = project.phases.create(name='Planung', predecessor=phase_2)

        task_3_1 = phase_3.tasks.create(name='Use Cases dokumentieren', planned_duration=1)
        task_3_1.resources.add(project_manager_resource)
        task_3_1.resources.add(business_analyst_resource)
        task_3_1.resources.add(architect_resource)
        task_3_1.duration_predictions.create(date='2017-09-04', duration=2)

        task_3_2 = phase_3.tasks.create(name='Domain Analyse machen', planned_duration=1, predecessor=task_3_1)
        task_3_2.resources.add(business_analyst_resource)
        task_3_2.resources.add(architect_resource)

        task_3_3 = phase_3.tasks.create(name='Prototype erstellen', planned_duration=5, predecessor=task_3_2)
        task_3_3.resources.add(developer_resource)
        task_3_3.resources.add(architect_resource)
        task_3_3.duration_predictions.create(date='2017-09-07', duration=3)

        task_3_4 = phase_3.tasks.create(name='Datenmodell erstellen', planned_duration=1, predecessor=task_3_3)
        task_3_4.resources.add(dba_resource)
        task_3_4.resources.add(architect_resource)
        task_3_4.duration_predictions.create(date='2017-09-07', duration=0)

        task_3_5 = phase_3.tasks.create(name='Architektur dokumentieren', planned_duration=2, predecessor=task_3_4)
        task_3_5.resources.add(architect_resource)

        project.earnings.create(date='2017-09-11', name='Payout No. 1', value=14640)
        phase_4 = project.phases.create(name='Implementierung', predecessor=phase_3)

        task_4_1 = phase_4.tasks.create(name='UX Konzept erstellen', planned_duration=3)
        task_4_1.resources.add(ux_resource)
        task_4_1.duration_predictions.create(date='2017-09-12', duration=4)
        task_4_1.duration_predictions.create(date='2017-09-13', duration=5)

        task_4_2 = phase_4.tasks.create(name='Frontend implementieren', planned_duration=15, predecessor=task_4_1)
        task_4_2.resources.add(developer_resource)
        task_4_2.duration_predictions.create(date='2017-09-25', duration=13)

        task_4_3 = phase_4.tasks.create(name='Backend implementieren', planned_duration=20, predecessor=task_4_2)
        task_4_3.resources.add(developer_resource)
        task_4_3.duration_predictions.create(date='2017-10-05', duration=25)  # new issue
        task_4_3.duration_predictions.create(date='2017-10-15', duration=18)

        task_4_4 = phase_4.tasks.create(name='Database review', planned_duration=1, predecessor=task_4_3)
        task_4_4.resources.add(architect_resource)
        task_4_4.resources.add(dba_resource)

        task_4_5 = phase_4.tasks.create(name='Deployment vorbereiten', planned_duration=1, predecessor=task_4_4)
        task_4_5.resources.add(project_manager_resource)
        task_4_5.resources.add(architect_resource)
        task_4_5.resources.add(ops_resource)

        task_4_6 = phase_4.tasks.create(name='Deployment nach Staging', planned_duration=1, predecessor=task_4_5)
        task_4_6.resources.add(ops_resource)
        task_4_6.duration_predictions.create(date='2017-10-16', duration=3)

        phase_5 = project.phases.create(name='Qualitäts Sicherung', predecessor=phase_4)
        task_5_1 = phase_5.tasks.create(name='QA Kickoff', planned_duration=1)
        task_5_1.resources.add(project_manager_resource)
        task_5_1.resources.add(business_analyst_resource)
        task_5_1.resources.add(architect_resource)
        task_5_1.resources.add(qa_resource)

        project.earnings.create(date='2017-10-22', name='Payout No. 2', value=68770 - 14640)

        task_5_2 = phase_5.tasks.create(name='QA testing', planned_duration=5, predecessor=task_5_1)
        task_5_2.resources.add(qa_resource)

        task_5_3 = phase_5.tasks.create(name='Verbesserungen implementieren', planned_duration=2, predecessor=task_5_2)
        task_5_3.resources.add(project_manager_resource)
        task_5_3.resources.add(developer_resource)
        task_5_3.resources.add(qa_resource)
        task_5_3.duration_predictions.create(date='2017-10-25', duration=0)

        task_5_4 = phase_5.tasks.create(name='Final QA', planned_duration=1, predecessor=task_5_2)
        task_5_4.resources.add(project_manager_resource)
        task_5_4.resources.add(qa_resource)

        phase_6 = project.phases.create(name='Release', predecessor=phase_5)

        task_6_1 = phase_6.tasks.create(name='Deploy to production', planned_duration=2)
        task_6_1.resources.add(architect_resource)
        task_6_1.resources.add(ops_resource)
        task_6_1.duration_predictions.create(date='2017-11-26', duration=4)

        task_6_2 = phase_6.tasks.create(name='User trainieren + Dokumentation finalisieren', planned_duration=5,
                                        predecessor=task_6_1)
        task_6_2.resources.add(project_manager_resource)
        task_6_2.resources.add(business_analyst_resource)
        task_6_2.resources.add(developer_resource)
        task_6_2.duration_predictions.create(date='2017-11-01', duration=8)

        task_6_3 = phase_6.tasks.create(name='Bugfixes', planned_duration=3, predecessor=task_6_2)
        task_6_3.resources.add(project_manager_resource)
        task_6_3.resources.add(developer_resource)
        task_6_3.duration_predictions.create(date='2017-11-01', duration=4)

        task_6_4 = phase_6.tasks.create(name='Handover to Operations', planned_duration=1, predecessor=task_6_3)
        task_6_4.resources.add(project_manager_resource)
        task_6_4.resources.add(developer_resource)
        task_6_4.resources.add(ops_resource)

        phase_7 = project.phases.create(name='Debriefing', predecessor=phase_6)
        task_7_1 = phase_7.tasks.create(name='Retrospektive abhalten', planned_duration=1)
        task_7_1.resources.add(project_manager_resource)
        task_7_1.resources.add(architect_resource)
        task_7_1.resources.add(developer_resource)
        task_7_1.resources.add(qa_resource)

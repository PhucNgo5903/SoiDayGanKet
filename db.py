import os
import django
import random
from faker import Faker
from datetime import timedelta, datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'donenv.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import (
    NguoiDung, Volunteer, Beneficiary, CharityOrg,
    Skill, VolunteerSkill, SupportArea, SkillsSupportArea,
    CharityOrgSupportArea, AssistanceRequestType, AssistanceRequest,
    AssistanceRequestTypeMap, AssistanceRequestImage,
    Event, EventRegistration
)

fake = Faker()

def create_users():
    roles = ['admin', 'volunteer', 'charity', 'beneficiary']
    nguoi_dung_list = []

    for _ in range(5):
        username = fake.user_name()
        email = fake.email()
        password = 'Password123'
        user = User.objects.create(
            username=username,
            email=email,
            last_login=timezone.now()
        )
        user.set_password(password)
        user.save()

        role = random.choice(roles)
        nd = NguoiDung.objects.create(
            user=user,
            role=role,
            dob=fake.date_of_birth(minimum_age=18, maximum_age=60),
            phone=fake.phone_number(),
            address=fake.address(),
            description=fake.text(max_nb_chars=200),
            status='active'
        )
        nguoi_dung_list.append(nd)

    return nguoi_dung_list


def create_sub_roles(nguoi_dungs):
    volunteers = []
    beneficiaries = []
    charities = []

    for nd in nguoi_dungs:
        if nd.role == 'volunteer':
            volunteers.append(Volunteer.objects.create(user=nd, gender=random.choice(['male', 'female'])))
        elif nd.role == 'beneficiary':
            beneficiaries.append(Beneficiary.objects.create(user=nd, gender=random.choice(['male', 'female'])))
        elif nd.role == 'charity':
            charities.append(CharityOrg.objects.create(user=nd, type=random.choice(['local', 'national', 'international']), website=fake.url()))

    return volunteers, beneficiaries, charities


def create_skills_support():
    skills = [Skill.objects.create(name=fake.job()) for _ in range(5)]
    areas = [SupportArea.objects.create(name=fake.city()) for _ in range(5)]

    for skill in skills:
        area = random.choice(areas)
        SkillsSupportArea.objects.create(skill=skill, support_area=area)

    return skills, areas


def create_volunteer_skills(volunteers, skills):
    for vol in volunteers:
        selected_skills = random.sample(skills, k=min(2, len(skills)))
        for skill in selected_skills:
            VolunteerSkill.objects.create(volunteer=vol, skill=skill)


def create_charity_org_support_areas(charities, areas):
    for co in charities:
        selected_areas = random.sample(areas, k=min(2, len(areas)))
        for area in selected_areas:
            CharityOrgSupportArea.objects.create(charity_org=co, support_area=area)


def create_assistance_types():
    return [AssistanceRequestType.objects.create(name=fake.word()) for _ in range(5)]


def create_assistance_requests(beneficiaries, charities, admins, types):
    requests = []

    for _ in range(5):
        ben = random.choice(beneficiaries)
        org = random.choice(charities) if charities else None
        admin = random.choice(admins) if admins else None
        title = fake.sentence()
        request = AssistanceRequest.objects.create(
            beneficiary=ben,
            charity_org=org,
            title=title,
            description=fake.text(),
            priority=random.choice(['low', 'medium', 'high']),
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=10),
            status='approved',
            receiving_status='waiting',
            update_by=admin,
            update_status_at=timezone.now(),
            place=fake.address(),
            proof_url=fake.image_url(),
            admin_remark=fake.sentence()
        )
        AssistanceRequestTypeMap.objects.create(assistance_request=request, type=random.choice(types))
        AssistanceRequestImage.objects.create(assistance_request=request, image_url=fake.image_url())
        requests.append(request)

    return requests


def create_events(charities, requests, admins):
    events = []
    for _ in range(5):
        charity = random.choice(charities)
        request = random.choice(requests)
        admin = random.choice(admins)
        event = Event.objects.create(
            charity_org=charity,
            assistance_request=request,
            title=fake.catch_phrase(),
            description=fake.text(),
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=3),
            status='approved',
            approved_by=admin,
            approved_at=timezone.now(),
            volunteers_number=random.randint(5, 20),
            report_url=fake.url(),
            confirmed_by=True
        )
        events.append(event)
    return events


def create_event_registrations(events, volunteers):
    for event in events:
        selected_volunteers = random.sample(volunteers, k=min(2, len(volunteers)))
        for vol in selected_volunteers:
            EventRegistration.objects.create(
                event=event,
                volunteer=vol,
                status='approved',
                checked_in_at=timezone.now(),
                checked_out_at=timezone.now() + timedelta(hours=3),
                rating=random.randint(1, 5),
                review=fake.text()
            )


def run():
    nguoi_dungs = create_users()
    volunteers, beneficiaries, charities = create_sub_roles(nguoi_dungs)
    admins = [nd for nd in nguoi_dungs if nd.role == 'admin']
    skills, areas = create_skills_support()
    create_volunteer_skills(volunteers, skills)
    create_charity_org_support_areas(charities, areas)
    types = create_assistance_types()
    requests = create_assistance_requests(beneficiaries, charities, admins, types)
    events = create_events(charities, requests, admins)
    create_event_registrations(events, volunteers)
    print("✅ Fake data inserted successfully!")

if __name__ == '__main__':
    run()

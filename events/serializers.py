from django.urls import reverse

"""
Responsible for serializing Event modules into JSON objects
"""


def event(event, request):
    signup_location = reverse('events:event_signup', args=[event.fair.year, event.pk])
    signup_url = request.build_absolute_uri(signup_location)

    data = {
        'id': event.pk,
        'name': event.name,
        'description': event.description,
        'location': event.location,
        'event_start': int(event.date_start.strftime('%s')),
        'event_end': int(event.date_end.strftime('%s')),
        'registration_end': int(event.date_start.strftime('%s')),
        'image_url': '//archive.kottnet.net/pictures/armada%20run.png',
        'fee': event.fee_s,
        'registration_required': True,
        'external_event_link': event.external_event_link,
        'signup_questions': [signup_question(question) for question in event.signupquestion_set.all()],
        'signup_link': signup_url,
    }

    return data


def signup_question(signup_question):
    data = {
        'id': signup_question.pk,
        'type': signup_question.type,
        'question': signup_question.question,
        'required': signup_question.required,
        'options': signup_question.options,
    }

    return data


def team(team):
    data = {
        'id': team.pk,
        'name': team.name,
        'capacity': team.max_capacity,
        'members': [team_member(member) for member in team.teammember_set.all()],
        'number_of_members': team.number_of_members()
    }

    return data


def team_member(team_member):
    data = {
        'name': team_member.participant.__str__(),
        'leader': team_member.leader
    }

    return data


def participant(participant):
    data = {
        'id': participant.id,
        'name': participant.assigned_name(),
        'fee_payed': participant.fee_payed_s,
        'signup_complete': participant.signup_complete,
        'team_id': participant.team().id if participant.team() else None,
        'check_in_token': participant.check_in_token,
        'has_checked_in': participant.has_checked_in()

    }

    return data

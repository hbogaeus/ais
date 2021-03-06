from django.shortcuts import get_object_or_404
from matching.models import StudentQuestionBase, StudentQuestionType, StudentAnswerSlider, StudentAnswerGrading, WorkField, StudentAnswerWorkField, Continent, SwedenRegion, \
StudentAnswerRegion, StudentAnswerContinent, JobType, StudentAnswerJobType


def answer_slider(answer, student, question, survey):
    '''
    Validate and deserialize an answer to a question of type SLIDER
    Returns true if the question was validated sucessfuly and saved
    '''
    question = question.studentquestionslider
    if type(answer) is dict:
        if 'min' in answer and 'max' in answer \
        and (type(answer['min']) is float or type(answer['min']) is int) \
        and (type(answer['max']) is float or type(answer['max']) is int) \
        and answer['min'] <= answer['max'] \
        and answer['min'] >= question.min_value \
        and answer['max'] <= question.max_value:
            (answer_model, was_created) = StudentAnswerSlider.objects.get_or_create(question=question, student=student)
            if was_created:
                answer_model.survey.add(survey)
            answer_model.answer_min = answer['min']
            answer_model.answer_max = answer['max']
            answer_model.save()
            return True
    elif (type(answer) is float or type(answer) is int):
        if question.min_value <= answer <= question.max_value:
            (answer_model, was_created) = StudentAnswerSlider.objects.get_or_create(question=question, student=student)
            if was_created:
                answer_model.survey.add(survey)
            answer_model.answer_min = answer
            answer_model.answer_max = answer
            answer_model.save()
            return True
    return False


def answer_grading(answer, student, question, survey):
    '''
    Validate and deseralize an answer to a question of type GRADING
    Returns true if the question was validated sucessfuly and saved
    '''
    if type(answer) is int:
        sizes = [-(question.studentquestiongrading.grading_size - 1) / 2,
                question.studentquestiongrading.grading_size / 2]
        if (sizes[0] < answer < sizes[1]):
            question = question.studentquestiongrading
            (answer_model, was_created) = StudentAnswerGrading.objects.get_or_create(question=question, student=student)
            if was_created:
                answer_model.survey.add(survey)
            answer_model.answer = answer
            answer_model.save()
            return True
    return False


ANSWER_DESERIALIZERS = {
    StudentQuestionType.SLIDER.value : answer_slider,
    StudentQuestionType.GRADING.value : answer_grading
}


def answers(answers, student, survey):
    '''
    Create or modify question answers from payload data
    used by questions_PUT in api/views
    Returns (int, int):
        where the first int tells the number of saved answers (all of which passed validation)
        and the second one is total number of processed anwers (some of which may have failed validation)
    '''
    modified_count = 0
    total_count = 0
    for answer in answers:
        total_count += 1
        if type(answer) is dict and 'id' in answer and 'answer' in answer:
            question = StudentQuestionBase.objects.filter(pk=answer['id']).first()
            if question and question.question_type in ANSWER_DESERIALIZERS:
                if ANSWER_DESERIALIZERS[question.question_type](answer['answer'], student, question, survey):
                    modified_count += 1
    return (modified_count, total_count)


def fields(fields, student, survey):
    '''
    Create or modify field answers from payload data
    used by questions_PUT in api/views
    '''
    work_fields = WorkField.objects.filter(survey=survey).all()
    for work_field in work_fields:
        (field_model, was_created) = StudentAnswerWorkField.objects.get_or_create(student=student, work_field=work_field)
        if was_created:
            field_model.survey.add(survey)
        field_model.answer = work_field.pk in fields
        field_model.save()

def student_profile(data, profile):
    '''
    Deserialize the data into the student_profile, validating the data on the way
    '''
    if type(data) is dict:
        if 'nickname' in data and type(data['nickname']) is str:
            profile.nickname = data['nickname']
        else:
            return False

        # optional fields
        if 'facebook_profile' in data and type(data['facebook_profile']) is str:
            profile.facebook_profile = data['facebook_profile']
        if 'linkedin_profile' in data and type(data['linkedin_profile']) is str:
            profile.linkedin_profile = data['linkedin_profile']
        if 'phone_number' in data and type(data['phone_number']) is str:
            profile.phone_number = data['phone_number']
        profile.save()
        return True
    else:
        return False

def regions(regions, student, survey):
    '''
    Create or modify field answers from payload data.
    used by questions_PUT in api/views.
    '''
    for region_id in regions:
        region = get_object_or_404(SwedenRegion, region_id=region_id)
        StudentAnswerRegion.objects.get_or_create(student=student, region=region)


def continents(continents, student, survey):
    '''
    Create or modify field answers from payload data.
    used by questions_PUT in api/views.
    '''
    for continent_id in continents:
        continent = get_object_or_404(Continent, continent_id=continent_id)
        StudentAnswerContinent.objects.get_or_create(student=student, continent=continent)

def jobtype(jobtypes, student, survey):
    '''
    Create or modify field answers from payload data.
    used by questions_PUT in api/views. Uses the JobType defined in the Matching app.
    LATER: Change it to use the JobType model in the exhibitors app.
    '''
    for job_type_id in jobtypes:
        job_type = get_object_or_404(JobType, job_type_id=job_type_id)
        StudentAnswerJobType.objects.get_or_create(student=student, job_type=job_type)

# -*- coding: utf-8 -*-

import os
try:
    import requests
except:
    print("Trying to Install required module: reqests\n")
    os.system('python3 -m pip install requests')
    import requests
try:
    import canvasapi
except:
    print("Trying to Install required module: canvasapi\n")
    os.system('python3 -m pip install canvasapi')    
    import canvasapi
try:
    import click
except:
    print("Trying to Install required module: click\n")
    os.system('python3 -m pip install click')   
    import click
try:
    import click
except:
    print("Trying to Install required module: pandas\n")
    os.system('python3 -m pip install pandas')   
    import click

from gamification import config
from gamification.prompts import course_prompt
from gamification.data_helpers import process_canvas_course, process_canvas_sections, \
    process_canvas_students

@click.command()
@click.option('--store_data',
    default=False,
    is_flag=True,
    help='Store data fetched into `.csv` files. [default: False]',
    envvar='CANVAS_STORE_DATA_LOCALLY')
@click.option('--course_id',
    help='Canvas Course ID.',
    type=int,
    envvar='CANVAS_COURSE_ID')
@click.option('--token',
    prompt=True,
    hide_input=True,
    help='Canvas API token.',
    required=True,
    envvar='CANVAS_API_TOKEN')
@click.option('--url',
    default='https://canvas.ubc.ca',
    help='Canvas Url. [default: https://canvas.ubc.ca]',
    required=True,
    envvar='CANVAS_BASE_URL')
def fetch_data(url, token, course_id, store_data):
    config.STORE_DATA_LOCALLY = store_data
    _fetch_data(url, token, course_id)

def _fetch_data(url, token, course_id):
    canvas = canvasapi.Canvas(url, token)
    data = {}
    
    if not course_id:
        # prompt user to select a course they have access to (paginated)
        course_id = course_prompt(canvas)
    
    # get course by id
    course = canvas.get_course(course_id, include=['total_students'])
    data['course_df'] = process_canvas_course(course)
    sections = course.get_sections(include=['students'], per_page=config.PER_PAGE)
    data['sections_df'] = process_canvas_sections(sections)
    students = course.get_users(enrollment_type=['student'], enrollment_stat=['active'], per_page=config.PER_PAGE)
    data['students_df'] = process_canvas_students(students)
    return (course, data)

if __name__ == '__main__':
    fetch_data()

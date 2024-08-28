#!/usr/bin/env python3
"""contains the function top_students"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    students = mongo_collection.find({})
    result = []
    for student in students:
        total_score = 0
        no_of_score = 0
        for topic in student.get("topics"):
            no_of_score += 1
            total_score += topic.get('score', 0)
        student['averageScore'] = total_score / no_of_score
        result.append(student)
    return sorted(result, key=lambda x: x['averageScore'], reverse=True)

import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from api.models import Teacher, Question, Student, Lesson, LessonStudent
from .factories import TeacherFactory, StudentFactory
from .. import watson_service

class TeacherViewSet(TestCase):
  def setUp(self):
    self.teacher1 = TeacherFactory(first_name='teacher1First')
    self.teacher2 = TeacherFactory(first_name='teacher2First')
    self.teacher3 = TeacherFactory(first_name='teacher3First')
    

  def test_get_list(self):
    response = self.client.get('/api/v1/teachers/')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 3)
    self.assertEqual(response.data[0]['id'], self.teacher1.id)
    self.assertEqual(response.data[0]['first_name'], self.teacher1.first_name)
  
  def test_get_detail(self):
    response = self.client.get('/api/v1/teachers/%s/' % self.teacher1.id)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['id'], self.teacher1.id)
    self.assertEqual(response.data['first_name'], self.teacher1.first_name)

  def test_post(self):
    data = {
      'first_name': 'newTeacher1First',
      'last_name': 'newTeacher1Last'
    }
    response = self.client.post('/api/v1/teachers/', data=data)

    self.assertEqual(response.status_code, 201)
    self.assertEqual(Teacher.objects.count(), 4)
    self.assertEqual(response.data['first_name'], data['first_name'])

  def test_teacher_student_get(self):
    Student.objects.create(first_name='max', last_name='ericson', teacher_id=self.teacher1.id)
    Student.objects.create(first_name='max2', last_name='ericson', teacher_id=self.teacher1.id)
    Student.objects.create(first_name='max3', last_name='ericson', teacher_id=self.teacher1.id)
    response = self.client.get('/api/v1/teachers/%s/students/' % self.teacher1.id)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 3)

  def test_teacher_student_post(self): 
    data = {
      'id': 1,
      'students': [
        {
        'first_name': 'newStudent1First',
        'last_name': 'newStudent1Last'
        },
        {
        'first_name': 'newStudent2First',
        'last_name': 'newStudent2Last'
        }
      ]
    }
    response = self.client.post('/api/v1/teachers/%s/students/' % self.teacher1.id, content_type='application/json', data=data)
   

    self.assertEqual(response.status_code, 200)
    self.assertEqual(Student.objects.count(), 2)
    self.assertEqual(response.data[0]['first_name'], data['students'][0]['first_name'])
    
class TeacherLessonSet(TestCase):
  def setUp(self):
    self.teacher1 = TeacherFactory(first_name='teacher1First', last_name='teacher1Last')

    self.lesson1 = self.teacher1.lesson_set.create(name='name1', description='description1')

    self.question1 = self.lesson1.question_set.create(question='question1', reading='reading1')
    self.answer1 = self.question1.answer_set.create(answer='answer1', correct=False)
    self.answer2 = self.question1.answer_set.create(answer='answer2', correct=True)

    self.question2 = self.lesson1.question_set.create(question='question2', reading='reading2')
    self.answer3 = self.question2.answer_set.create(answer='answer3', correct=True)
    self.answer4 = self.question2.answer_set.create(answer='answer4', correct=False)

    self.lesson2 = self.teacher1.lesson_set.create(name='name2', description='description2')

    self.question3 = self.lesson2.question_set.create(question='question1', reading='reading1')
    self.answer5 = self.question3.answer_set.create(answer='answer1', correct=False)
    self.answer6 = self.question3.answer_set.create(answer='answer2', correct=True)

    self.question4 = self.lesson2.question_set.create(question='question2', reading='reading2')
    self.answer7 = self.question4.answer_set.create(answer='answer3', correct=True)
    self.answer8 = self.question4.answer_set.create(answer='answer4', correct=False)


  def test_can_post_lesson(self):
    data = {
      'lesson': {
        'name': 'lessonName1',
        'questions': [
            {
              'question': 'question1 description',
              'reading': 'question1 reading',
              'answers': [
                  {
                    'answer': 'answer1 description',
                    'correct': 'false'
                  },
                  {
                    'answer': 'answer2 description',
                    'correct': 'true'
                  },
                  {
                    'answer': 'answer3 description',
                    'correct': 'false'
                  },
                  {
                    'answer': 'answer4 description',
                    'correct': 'false'
                  }
                ]
            },
            {
              'question': 'question2 description',
              'reading': 'question2 reading',
              'answers': [
                  {
                    'answer': 'answer1 description',
                    'correct': 'false'
                  },
                  {
                    'answer': 'answer2 description',
                    'correct': 'true'
                  },
                  {
                    'answer': 'answer3 description',
                    'correct': 'false'
                  },
                  {
                    'answer': 'answer4 description',
                    'correct': 'false'
                  }
                ]
              }   
          ]
     }
 }

    response = self.client.post('/api/v1/teachers/%s/lessons/' % self.teacher1.id, data=data, content_type='application/json')

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['name'], data['lesson']['name'])
    self.assertIsInstance(response.data['questions'][0], dict)
    self.assertIsInstance(response.data['questions'][1], dict)
    self.assertIsInstance(response.data['questions'][0]['answers'][0], dict)
    self.assertIsInstance(response.data['questions'][1]['answers'][0], dict)

  def test_can_get_lesson(self):
    response = self.client.get('/api/v1/lessons/%s/' % self.lesson1.id)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['name'], self.lesson1.name)
    self.assertIsInstance(response.data['questions'][0], dict)
    self.assertIsInstance(response.data['questions'][1], dict)
    self.assertIsInstance(response.data['questions'][0]['answers'][0], dict)
    self.assertIsInstance(response.data['questions'][1]['answers'][0], dict)

  def test_can_get_all_lessons_for_teacher(self):
    response = self.client.get('/api/v1/teachers/%s/lessons/' % self.teacher1.id)

    self.assertEqual(response.status_code, 200)
    self.assertIsNotNone(response.data[0]['name'])
    self.assertIsNotNone(response.data[1]['name'])
    self.assertIsInstance(response.data[0]['questions'], list)
    self.assertIsInstance(response.data[1]['questions'], list)
    self.assertIsInstance(response.data[0]['questions'][0]['answers'], list)
    self.assertIsInstance(response.data[1]['questions'][0]['answers'], list)

class StatisticsSet(TestCase):
  def setUp(self):
    self.teacher1 = TeacherFactory(first_name='teacher1First', last_name='teacher1Last')

    self.lesson1 = self.teacher1.lesson_set.create(name='name1', description='description1')

    self.question1 = self.lesson1.question_set.create(question='question1', reading='reading1')
    self.answer1 = self.question1.answer_set.create(answer='answer1', correct=False)
    self.answer2 = self.question1.answer_set.create(answer='answer2', correct=True)

    self.question2 = self.lesson1.question_set.create(question='question2', reading='reading2')
    self.answer3 = self.question2.answer_set.create(answer='answer3', correct=True)
    self.answer4 = self.question2.answer_set.create(answer='answer4', correct=False)

    self.lesson2 = self.teacher1.lesson_set.create(name='name2', description='description2')

    self.question3 = self.lesson2.question_set.create(question='question1', reading='reading1')
    self.answer5 = self.question3.answer_set.create(answer='answer1', correct=False)
    self.answer6 = self.question3.answer_set.create(answer='answer2', correct=True)

    self.question4 = self.lesson2.question_set.create(question='question2', reading='reading2')
    self.answer7 = self.question4.answer_set.create(answer='answer3', correct=True)
    self.answer8 = self.question4.answer_set.create(answer='answer4', correct=False)

    self.student1 = StudentFactory(teacher=self.teacher1)
    self.student2 = StudentFactory(teacher=self.teacher1)
    self.student3 = StudentFactory(teacher=self.teacher1)
    self.student4 = StudentFactory(teacher=self.teacher1)

    self.lessonStudent1 = self.student1.lessonstudent_set.create(lesson_id=self.lesson1.id, mood='cranky', score=90)
    self.lessonStudent2 = self.student1.lessonstudent_set.create(lesson_id=self.lesson2.id, mood='cranky', score=96)

    self.lessonStudent4 = self.student2.lessonstudent_set.create(lesson_id=self.lesson1.id, mood='cranky', score=62)
    self.lessonStudent5 = self.student2.lessonstudent_set.create(lesson_id=self.lesson2.id, mood='cranky', score=22)

    self.lessonStudent6 = self.student3.lessonstudent_set.create(lesson_id=self.lesson1.id, mood='I felt great', score=87)
    self.lessonStudent7 = self.student3.lessonstudent_set.create(lesson_id=self.lesson2.id, mood='ok', score=67)

  
  def test_get_average_score_per_student(self):
    response = self.client.get('/api/v1/students/%s/average_score/' % self.student1.id)

    response_data = {
        "student_id": self.student1.id,
        "average_score": 93
    }

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, response_data)

  def test_get_average_score_per_lesson(self):
    response = self.client.get('/api/v1/lessons/%s/average_score/' % self.lesson1.id)

    response_data = {
        "lesson_id": self.lesson1.id,
        "average_score": 79
    }

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, response_data)

  def test_get_zscore_for_all_students_on_lesson(self):
    response = self.client.get('/api/v1/lessons/%s/zscores/' % self.lesson1.id)

    self.assertEqual(response.status_code, 200)

    self.assertIsNotNone(response.data[0]["student_id"])
    self.assertIsInstance(response.data[0]["zscore"], float)
    self.assertIsNotNone(response.data[1]["student_id"])
    self.assertIsInstance(response.data[1]["zscore"], float)
    self.assertIsNotNone(response.data[2]["student_id"])
    self.assertIsInstance(response.data[2]["zscore"], float)

  def test_get_student_rank_for_all_students(self):
    response = self.client.get('/api/v1/teachers/%s/students/' % self.teacher1.id)

    self.assertIsInstance(response.data[0]['class_rank'], int)
    self.assertIsInstance(response.data[1]['class_rank'], int)
    self.assertIsInstance(response.data[2]['class_rank'], int)


class StudentLessonViewSet(TestCase):
  def setUp(self):
    self.teacher = Teacher.objects.create(first_name='Severus', last_name='Snape')
    self.student = Student.objects.create(first_name='Draco', last_name='Malfoy', teacher_id=self.teacher.id)
    self.lesson = self.teacher.lesson_set.create(name='Potions', description='Brew potions properly')

  def test_post_student_lesson(self):
    data = {
      "lesson": self.lesson.id,
      "score": 3,
      "mood": "I had a brilliant time"
    }
    response = self.client.post('/api/v1/students/%s/' % self.student.id, data=data, content_type='application/json')
   
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['score'], 3)
    self.assertEqual(response.data['mood'], 'I had a brilliant time')
    self.assertEqual(response.data['lesson'], self.lesson.id)
    self.assertEqual(response.data['student'], self.student.id)
    self.assertEqual(response.data['mood_analyzer'], 'Joy')

  def test_get_student_lesson(self):
    
    self.student2 = Student.objects.create(first_name='praco', last_name='palfoy', teacher_id=self.teacher.id)   
    self.student3 = Student.objects.create(first_name='qraco', last_name='qalfoy', teacher_id=self.teacher.id)   
    self.lessonstudent1 = LessonStudent.objects.create(lesson_id=self.lesson.id, student_id=self.student2.id, score=5, mood='great!')
    self.lessonstudent2 = LessonStudent.objects.create(lesson_id=self.lesson.id, student_id=self.student3.id, score=7, mood='Bad!' )

    # data = {
    #   "lesson": self.lesson.id,
    #   "student": self.student2.id
    # }
    response = self.client.get('/api/v1/lessons/%s/students/%s/' %(self.lesson.id, self.student2.id), content_type='application/json')

 
    self.assertEqual(response.data['score'], 5)
    self.assertEqual(response.data['mood'], 'great!')
    self.assertEqual(response.data['student'], self.student2.id)

  def test_get_all_lesson_students_for_lesson(self):
    self.student2 = Student.objects.create(first_name='praco', last_name='palfoy', teacher_id=self.teacher.id)   
    self.student3 = Student.objects.create(first_name='qraco', last_name='qalfoy', teacher_id=self.teacher.id)   
    self.lessonstudent1 = LessonStudent.objects.create(lesson_id=self.lesson.id, student_id=self.student2.id, score=5, mood='great!')
    self.lessonstudent2 = LessonStudent.objects.create(lesson_id=self.lesson.id, student_id=self.student3.id, score=7, mood='Bad!' )

    response = self.client.get('/api/v1/lessonstudents/%s/' % self.lesson.id, content_type='application/json')
    self.assertEqual(response.status_code, 200)
    # self.assertEqual(response.data[0]['score'], 5)
    self.assertIsInstance(response.data[0]['score'], int)
    # self.assertEqual(response.data[0]['mood'], 'great!')
    # self.assertEqual(response.data[0]['student'], self.student2.id)
    self.assertIsInstance(response.data[0]['score'], int)
    # self.assertEqual(response.data[1]['mood'], 'Bad!')
    # self.assertEqual(response.data[1]['student'], self.student3.id)

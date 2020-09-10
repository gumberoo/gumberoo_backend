from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from api.models import Teacher, Student, Lesson, LessonStudent

from .factories import TeacherFactory, StudentFactory

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

class StudentLessonViewSet(TestCase):
  def setUp(self):
    self.teacher = Teacher.objects.create(first_name='Severus',
    last_name='Snape')
    self.student = Student.objects.create(first_name='Draco', last_name='Malfoy', age= 13, teacher_id=self.teacher.id)
    self.lesson1 = Lesson.objects.create(name='Potions', description='Brew potions properly')

  def test_post_student_lesson(self):
    data = {
      "lesson": self.lesson1.id,
      "score": 3,
      "mood": "I had a brilliant time"
    }
    response = self.client.post(
        '/api/v1/students/%s' % (self.student.id), data=data, content_type='application/json')
   
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data['score'], 3)
    self.assertEqual(response.data['mood'], 'I had a brilliant time')
    self.assertEqual(response.data['lesson'], 4)
    self.assertEqual(response.data['student'], 3)

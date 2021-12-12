from django.shortcuts import render, get_object_or_404
from department.models import Department

# Delibrately didn't used Class Based Views just for experiment

def dept_list(request):
    departments = Department.objects.all()
    return render(request, 'department/department_list.html',
                            {'departments': departments,})

def dept_details(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'department/department_detail.html',
                            {'department': department,})

def dept_subjects(request, pk):
    department = get_object_or_404(Department, pk=pk)
    subjects = department.subjects.all()

    return render(request, 'department/department_subjects.html',
                            {'department': department,
                            'subjects': subjects,})

def dept_students(request, pk):
    department = get_object_or_404(Department, pk=pk)
    students = department.students.all()
    
    return render(request, 'department/department_students.html',
                            {'department': department,
                            'students': students,})
from rest_framework.views import APIView
from rest_framework.response import Response    
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.models import Users,Skill,CV
from users.serializer import  SkillSerializer, CVSerializer

import pdfplumber

class ExtractSkillsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            cv_file = user.cv 
        except CV.DoesNotExist:
            return Response({"error": "CV not found for the user."}, status=status.HTTP_404_NOT_FOUND) 

        if not cv_file:
            return Response({"error": "No CV file provided."}, status=status.HTTP_400_BAD_REQUEST)
        # Extract text from the CV PDF file
        cv_path=cv_file.cv_file.path
        extracted_skills = self.extract_skills_from_cv(cv_path)

        for skill_name in extracted_skills:
            skill, created = Skill.objects.get_or_create(user=user, skill_name=skill_name)
        
        return Response({
                        "message": "Skills extracted and saved successfully.",
                        "extracted_skills": extracted_skills
                        }, status=status.HTTP_201_CREATED)




    def extract_text_from_pdf(self, cv_path):
        text = ""
        with pdfplumber.open(cv_path) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
        return text
    
    
    def extract_skills_from_cv(self, cv_file):
        cv_text = self.extract_text_from_pdf(cv_file)

        skills_db = [
        'Python', 'Django', 'Flask', 'JavaScript', 'React',
        'SQL', 'MongoDB', 'HTML', 'CSS', 'Machine Learning',
        'Data Science', 'NLP', 'Git', 'Docker', 'Kubernetes',
        'AWS', 'REST APIs', 'Linux','Microsoft Word', 'Microsoft Excel',]
        extracted_skills = set()

        for skill in skills_db:
            if skill.lower() in cv_text.lower():
                extracted_skills.add(skill)

        return list(extracted_skills)




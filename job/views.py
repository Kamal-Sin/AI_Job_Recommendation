from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .data import df    
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



class JobRecommendationAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user=request.user
        user_skills = [skill.skill_name.lower() for skill in user.skills.all()]

        if not user_skills:
            return Response({"error": "No skills found for the user."}, status=status.HTTP_404_NOT_FOUND)

        job_text = df['job_title'].fillna('') + '' + df['description_text'].fillna('')+''+ df['description'].fillna('')
        job_text = job_text.str.lower().tolist()

        vectorizer = TfidfVectorizer()
        job_matrix = vectorizer.fit_transform(job_text)

        skills=''.join(user_skills)
        skills_vector = vectorizer.transform([skills])

        similarity_scores = cosine_similarity(skills_vector, job_matrix).flatten()

        top_indices = similarity_scores.argsort()[-10:][::-1]

       
        results = []
        for i in top_indices:
            results.append({
                "company": df.iloc[i]['company_name'],
                "job_title": df.iloc[i]['job_title'],
                "location": df.iloc[i]['location'],
                "score": float(similarity_scores[i])
            })

        return Response({"recommendations": results})

          
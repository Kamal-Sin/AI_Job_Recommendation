from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import pandas as pd
from .data import df    
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



class JobRecommendationAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user_skills = [skill.skill_name.lower() for skill in user.skills.all()]

        if not user_skills:
            return Response({
                "error": "No skills found. Please add skills to your profile first.",
                "recommendations": []
            }, status=status.HTTP_200_OK)

        if df.empty or len(df) == 0:
            return Response({
                "error": "No job data available.",
                "recommendations": []
            }, status=status.HTTP_200_OK)

        # Combine job information with proper spacing
        job_text = (
            df['job_title'].fillna('') + ' ' + 
            df['description_text'].fillna('') + ' ' + 
            df.get('description', pd.Series([''] * len(df))).fillna('')
        )
        job_text = job_text.str.lower().tolist()

        # Combine user skills with spaces for better matching
        skills_text = ' '.join(user_skills)

        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        job_matrix = vectorizer.fit_transform(job_text)
        skills_vector = vectorizer.transform([skills_text])

        # Calculate similarity scores
        similarity_scores = cosine_similarity(skills_vector, job_matrix).flatten()

        # Get top 10 jobs (filter out scores that are too low)
        min_score = 0.01  # Minimum similarity score to show
        valid_indices = [i for i, score in enumerate(similarity_scores) if score >= min_score]
        
        if not valid_indices:
            return Response({
                "error": "No matching jobs found based on your skills.",
                "recommendations": [],
                "user_skills": user_skills
            }, status=status.HTTP_200_OK)

        # Get top indices sorted by score
        top_indices = sorted(valid_indices, key=lambda i: similarity_scores[i], reverse=True)[:10]

        # Build results
        results = []
        for i in top_indices:
            score = float(similarity_scores[i])
            results.append({
                "company": str(df.iloc[i].get('company_name', 'N/A')),
                "job_title": str(df.iloc[i].get('job_title', 'N/A')),
                "location": str(df.iloc[i].get('location', 'N/A')),
                "score": round(score, 4),  # Round to 4 decimal places
                "score_percentage": round(score * 100, 2)  # Percentage for display
            })

        return Response({
            "recommendations": results,
            "user_skills": user_skills,
            "total_jobs_analyzed": len(df),
            "matching_jobs": len(results)
        })

          
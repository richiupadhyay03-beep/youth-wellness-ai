import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

import plotly.graph_objects as go
import json
import random

# Configure Streamlit page
st.set_page_config(
    page_title="YouthWell - Mental Health Assessment",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 3em;
    color: #FF6B35;
    text-align: center;
    margin-bottom: 30px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.section-header {
    font-size: 1.5em;
    color: #2E8B57;
    margin-top: 30px;
    margin-bottom: 15px;
}
.question-box {
    background-color: #F0F8FF;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 5px solid #4169E1;
}
.suggestion-box {
    background-color: #F5F5DC;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    border-left: 4px solid #32CD32;
}
.sloka-box {
    background-color: #FFF8DC;
    padding: 20px;
    border-radius: 10px;
    margin: 15px 0;
    border: 2px solid #DAA520;
    font-style: italic;
}
.stress-high { color: #DC143C; font-weight: bold; }
.stress-medium { color: #FF8C00; font-weight: bold; }
.stress-low { color: #32CD32; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

class YouthWellBeingAssessment:
    def __init__(self):
        # Mental health assessment questions
        self.questions = [
            {
                "id": "sleep_quality",
                "question": "How would you rate your sleep quality over the past week?",
                "options": ["Excellent", "Good", "Fair", "Poor", "Very Poor"],
                "weights": [1, 2, 3, 4, 5]
            },
            {
                "id": "stress_level",
                "question": "How often do you feel overwhelmed or stressed?",
                "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
                "weights": [1, 2, 3, 4, 5]
            },
            {
                "id": "social_connection",
                "question": "How satisfied are you with your social relationships?",
                "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"],
                "weights": [1, 2, 3, 4, 5]
            },
            {
                "id": "physical_activity",
                "question": "How often do you engage in physical exercise?",
                "options": ["Daily", "4-6 times/week", "2-3 times/week", "Once a week", "Never"],
                "weights": [1, 2, 3, 4, 5]
            },
            {
                "id": "mood_stability",
                "question": "How stable has your mood been lately?",
                "options": ["Very Stable", "Mostly Stable", "Somewhat Variable", "Often Variable", "Very Variable"],
                "weights": [1, 2, 3, 4, 5]
            },
            {
                "id": "concentration",
                "question": "How is your ability to focus and concentrate?",
                "options": ["Excellent", "Good", "Average", "Poor", "Very Poor"],
                "weights": [1, 2, 3, 4, 5]
            },
            {
                "id": "life_satisfaction",
                "question": "How satisfied are you with your life currently?",
                "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"],
                "weights": [1, 2, 3, 4, 5]
            },
            {
                "id": "anxiety_level",
                "question": "How often do you experience anxiety or worry?",
                "options": ["Never", "Rarely", "Sometimes", "Often", "Always"],
                "weights": [1, 2, 3, 4, 5]
            }
        ]
        
        # Exercise suggestions based on stress levels
        self.exercises = {
            "low_stress": [
                "🚶‍♀️ **Morning Walk (15-20 mins)**: Start your day with a gentle walk in nature",
                "🧘‍♀️ **Mindful Breathing (5 mins)**: Practice deep breathing exercises",
                "🤸‍♀️ **Light Stretching (10 mins)**: Simple yoga poses to maintain flexibility",
                "🏓 **Fun Activities**: Play games like table tennis or badminton with friends",
                "🎵 **Dance Therapy (15 mins)**: Put on your favorite music and dance freely"
            ],
            "medium_stress": [
                "🏃‍♀️ **Moderate Cardio (20-30 mins)**: Jogging, cycling, or swimming",
                "🧘‍♀️ **Yoga Session (20-30 mins)**: Practice stress-relieving yoga poses",
                "💪 **Strength Training (20 mins)**: Light weights or bodyweight exercises",
                "🎨 **Creative Expression**: Drawing, painting, or writing in a journal",
                "🌊 **Progressive Muscle Relaxation (15 mins)**: Tense and relax muscle groups",
                "🎶 **Music Meditation (10-15 mins)**: Listen to calming instrumental music"
            ],
            "high_stress": [
                "🏃‍♀️ **High-Intensity Cardio (30-45 mins)**: Running, HIIT workouts, or sports",
                "🧘‍♀️ **Extended Meditation (20-30 mins)**: Deep mindfulness or guided meditation",
                "💪 **Strength Training (30-45 mins)**: Weight lifting to release tension",
                "🥊 **Kickboxing/Martial Arts (30 mins)**: Channel energy into structured combat sports",
                "🌿 **Nature Therapy**: Spend 1-2 hours in natural settings (hiking, gardening)",
                "📝 **Journaling (15-20 mins)**: Write about your thoughts and feelings",
                "🛀 **Relaxation Routine**: Hot bath, aromatherapy, and gentle stretching"
            ]
        }
        
        # Bhagavad Gita slokas with translations
        self.gita_slokas = {
            "low_stress": [
                {
                    "sanskrit": "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय। सिद्ध्यसिद्ध्योः समो भूत्वा समत्वं योग उच्यते॥",
                    "translation": "Perform your duties while maintaining equanimity in success and failure. This balanced state of mind is called Yoga.",
                    "chapter": "Chapter 2, Verse 48",
                    "relevance": "Maintain balance and peace in daily activities"
                },
                {
                    "sanskrit": "सुखदुःखे समे कृत्वा लाभालाभौ जयाजयौ। ततो युद्धाय युज्यस्व नैवं पापमवाप्स्यसि॥",
                    "translation": "Fight for the sake of duty, treating pleasure and pain, gain and loss, victory and defeat alike.",
                    "chapter": "Chapter 2, Verse 38",
                    "relevance": "Face life's challenges with equanimity"
                }
            ],
            "medium_stress": [
                {
                    "sanskrit": "मन्मना भव मद्भक्तो मद्याजी मां नमस्कुरु। मामेवैष्यसि सत्यं ते प्रतिजाने प्रियोऽसि मे॥",
                    "translation": "Focus your mind on the divine, be devoted, worship, and surrender. You will surely reach the supreme destination.",
                    "chapter": "Chapter 18, Verse 65",
                    "relevance": "Find peace through spiritual connection and devotion"
                },
                {
                    "sanskrit": "तस्माद्योगाय युज्यस्व योग करमसु कौशलम्। कर्मजं बुद्धियुक्ता हि फलं त्यक्त्वा मनीषिणः॥",
                    "translation": "Therefore, engage in yoga and perform actions with skill. Wise people abandon attachment to results.",
                    "chapter": "Chapter 2, Verse 50",
                    "relevance": "Perform duties without attachment to outcomes"
                }
            ],
            "high_stress": [
                {
                    "sanskrit": "सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज। अहं त्वां सर्वपापेभ्यो मोक्षयिष्यामि मा शुचः॥",
                    "translation": "Abandon all varieties of dharma and surrender unto me alone. I will deliver you from all sins, do not despair.",
                    "chapter": "Chapter 18, Verse 66",
                    "relevance": "Find ultimate peace through complete surrender and faith"
                },
                {
                    "sanskrit": "क्लैब्यं मा स्म गमः पार्थ नैतत्त्वय्युपपद्यते। क्षुद्रं हृदयदौर्बल्यं त्यक्त्वोत्तिष्ठ परन्तप॥",
                    "translation": "Do not yield to cowardice, O Arjuna. It does not befit you. Cast off this weakness of heart and arise!",
                    "chapter": "Chapter 2, Verse 3",
                    "relevance": "Overcome fear and weakness with courage and determination"
                },
                {
                    "sanskrit": "योगी युञ्जीत सततमात्मानं रहसि स्थितः। एकाकी यतचित्तात्मा निराशीरपरिग्रहः॥",
                    "translation": "The yogi should constantly discipline the mind by remaining in solitude, alone, with controlled thoughts.",
                    "chapter": "Chapter 6, Verse 10",
                    "relevance": "Practice regular meditation and self-discipline for inner peace"
                }
            ]
        }

    def calculate_stress_level(self, responses):
        total_score = sum(responses.values())
        max_score = len(self.questions) * 5
        stress_percentage = (total_score / max_score) * 100
        
        if stress_percentage <= 40:
            return "low_stress", stress_percentage, "Low Stress - You're managing well! 😊"
        elif stress_percentage <= 70:
            return "medium_stress", stress_percentage, "Moderate Stress - Some areas need attention 🤔"
        else:
            return "high_stress", stress_percentage, "High Stress - Priority support needed 🚨"
    
    def generate_insights(self, responses):
        insights = []
        
        # Analyze specific aspects
        if responses.get('sleep_quality', 0) >= 4:
            insights.append("💤 **Sleep Quality**: Consider establishing a better sleep routine")
        
        if responses.get('physical_activity', 0) >= 4:
            insights.append("🏃‍♀️ **Physical Activity**: Increasing exercise could significantly improve your mood")
        
        if responses.get('social_connection', 0) >= 4:
            insights.append("👥 **Social Connection**: Building stronger relationships may help reduce stress")
        
        if responses.get('anxiety_level', 0) >= 4:
            insights.append("😰 **Anxiety Management**: Consider learning anxiety-reduction techniques")
        
        return insights

def main():
    st.markdown('<h1 class="main-header">🧘 YouthWell - Mental Health Assessment</h1>', unsafe_allow_html=True)
    
    assessment = YouthWellBeingAssessment()
    
    # Initialize session state
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("🎯 Assessment Progress")
        progress = len(st.session_state.responses) / len(assessment.questions)
        st.progress(progress)
        st.write(f"{len(st.session_state.responses)}/{len(assessment.questions)} questions completed")
        
        if st.button("🔄 Reset Assessment"):
            st.session_state.responses = {}
            st.session_state.assessment_complete = False
            st.rerun()
    
    # Main assessment area
    if not st.session_state.assessment_complete:
        st.markdown('<h2 class="section-header">📝 Mental Health Assessment</h2>', unsafe_allow_html=True)
        st.write("Please answer the following questions honestly. Your responses will help us provide personalized suggestions.")
        
        # Display questions
        with st.form("assessment_form"):
            for question in assessment.questions:
                st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
                response = st.radio(
                    question["question"],
                    options=question["options"],
                    key=question["id"],
                    index=None if question["id"] not in st.session_state.responses else question["options"].index(st.session_state.responses[question["id"]])
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                if response:
                    weight_index = question["options"].index(response)
                    st.session_state.responses[question["id"]] = question["weights"][weight_index]
            
            submitted = st.form_submit_button("🚀 Complete Assessment", use_container_width=True)
            
            if submitted and len(st.session_state.responses) == len(assessment.questions):
                st.session_state.assessment_complete = True
                st.rerun()
            elif submitted:
                st.warning("Please answer all questions before submitting.")
    
    # Results display
    if st.session_state.assessment_complete and st.session_state.responses:
        stress_level, stress_percentage, stress_description = assessment.calculate_stress_level(st.session_state.responses)
        
        # Results header
        st.markdown('<h2 class="section-header">📊 Your Assessment Results</h2>', unsafe_allow_html=True)
        
        # Stress level visualization
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            # Gauge chart for stress level
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = stress_percentage,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Stress Level (%)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgreen"},
                        {'range': [40, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.metric("Stress Level", f"{stress_percentage:.1f}%", 
                     delta=None, delta_color="inverse")
        
        with col3:
            # Category breakdown
            categories = ['Sleep', 'Stress', 'Social', 'Physical', 'Mood', 'Focus', 'Life Sat.', 'Anxiety']
            scores = list(st.session_state.responses.values())
            
            fig_bar = px.bar(
                x=categories, 
                y=scores,
                title="Category Breakdown",
                color=scores,
                color_continuous_scale="RdYlGn_r"
            )
            fig_bar.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Stress level description
        if stress_level == "low_stress":
            st.success(stress_description)
        elif stress_level == "medium_stress":
            st.warning(stress_description)
        else:
            st.error(stress_description)
        
        # Insights
        insights = assessment.generate_insights(st.session_state.responses)
        if insights:
            st.markdown('<h3 class="section-header">💡 Personal Insights</h3>', unsafe_allow_html=True)
            for insight in insights:
                st.markdown(f'<div class="suggestion-box">{insight}</div>', unsafe_allow_html=True)
        
        # Exercise recommendations
        st.markdown('<h3 class="section-header">🏃‍♀️ Recommended Exercises</h3>', unsafe_allow_html=True)
        exercises = assessment.exercises[stress_level]
        
        cols = st.columns(2)
        for i, exercise in enumerate(exercises):
            with cols[i % 2]:
                st.markdown(f'<div class="suggestion-box">{exercise}</div>', unsafe_allow_html=True)
        
        # Bhagavad Gita Slokas
        st.markdown('<h3 class="section-header">🕉️ Wisdom from Bhagavad Gita</h3>', unsafe_allow_html=True)
        slokas = assessment.gita_slokas[stress_level]
        
        for sloka in slokas:
            st.markdown(f'''
            <div class="sloka-box">
                <h4 style="color: #8B4513; margin-bottom: 10px;">{sloka["chapter"]}</h4>
                <p style="font-size: 1.1em; color: #2F4F4F; margin-bottom: 15px;"><strong>Sanskrit:</strong><br>{sloka["sanskrit"]}</p>
                <p style="color: #556B2F; margin-bottom: 10px;"><strong>Translation:</strong><br>{sloka["translation"]}</p>
                <p style="color: #8B0000; font-size: 0.9em;"><strong>Relevance:</strong> {sloka["relevance"]}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Additional recommendations
        st.markdown('<h3 class="section-header">🌟 Additional Recommendations</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📱 **Digital Wellness**
            - Limit social media usage
            - Practice digital detox regularly
            - Use apps for meditation and mindfulness
            - Set boundaries for screen time
            """)
            
            st.markdown("""
            ### 🍎 **Nutrition Tips**
            - Eat regular, balanced meals
            - Stay hydrated (8-10 glasses water/day)
            - Include omega-3 rich foods
            - Limit caffeine and sugar intake
            """)
        
        with col2:
            st.markdown("""
            ### 😴 **Sleep Hygiene**
            - Maintain consistent sleep schedule
            - Create a relaxing bedtime routine
            - Keep bedroom cool and dark
            - Avoid screens 1 hour before bed
            """)
            
            st.markdown("""
            ### 🤝 **Social Support**
            - Connect with friends and family regularly
            - Join clubs or groups with similar interests
            - Practice active listening
            - Seek professional help when needed
            """)
        
        # Emergency resources
        st.markdown('<h3 class="section-header">🆘 Emergency Resources</h3>', unsafe_allow_html=True)
        if stress_level == "high_stress":
            st.error("""
            **If you're experiencing severe distress, please reach out for immediate help:**
            - **National Suicide Prevention Lifeline**: 988 (US)
            - **Crisis Text Line**: Text HOME to 741741
            - **Emergency Services**: 911 (US) / 112 (EU) / Local emergency number
            - **Mental Health Professional**: Consider scheduling an appointment
            """)
        
        # Save results option
        st.markdown('<h3 class="section-header">💾 Save Your Results</h3>', unsafe_allow_html=True)
        
        results_summary = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "stress_level": stress_level,
            "stress_percentage": stress_percentage,
            "responses": st.session_state.responses,
            "insights": insights
        }
        
        if st.download_button(
            label="📁 Download Results (JSON)",
            data=json.dumps(results_summary, indent=2),
            file_name=f"youthwell_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        ):
            st.success("Results downloaded successfully!")

if __name__ == "__main__":
    main()
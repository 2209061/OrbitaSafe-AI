import streamlit as st
#AI Avoidance Recommendation
def show_recommendation(risk_score):
  st.subheader("AI AVOIDANCE RECOMMENDATION")
  if risk_score>=70:
   st.write("Recommendation:Move Satellite upward by +1 in Y direction")
   st.write("Reason:Devris is too close to orbital path")
  elif risk_score >=40:
   st.write("Recommendation:Monitor closely and prepare small orbitadjustment")
  else:
   st.write("Recommendation: No immediate action needed.")
   st.write("Reason:Orbit is safe.")
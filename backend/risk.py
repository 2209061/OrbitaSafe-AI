#Risk Score+ Mission Status
def calculate_risk_score(distance):
 risk_score=max(0,100-(distance*30))
 return risk_score
def get_risk_level(risk_score):
  if risk_score>=70:
   return "High Collision Risk"
  elif risk_score >=40:
   return"Midium Risk"
  else:
   return"SAFE ORBIT"
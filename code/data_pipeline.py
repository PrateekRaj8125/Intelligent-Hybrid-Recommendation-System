import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
random.seed(42)
np.random.seed(42)
names = [
"Aarav Shah","Priya Mehta","Rohan Verma","Sneha Iyer","Karan Kapoor",
"Nisha Bose","Arjun Nair","Divya Singh","Vikram Rao","Pooja Sharma",
"Rahul Gupta","Ananya Das","Siddharth Joshi","Meera Pillai","Aditya Kumar",
"Lakshmi Reddy","Nikhil Pandey","Sunita Yadav","Deepak Mishra","Kavya Nambiar",
"Harish Tiwari","Shreya Chatterjee","Manish Malhotra","Ritu Aggarwal","Gaurav Saxena",
"Ishaan Bhatia","Tanvi Kulkarni","Sameer Wagh","Neha Jain","Vinay Patil",
"Amrita Ghosh","Rajesh Sinha","Pallavi Goswami","Kunal Acharya","Swati Dey",
"Rohit Tripathi","Madhuri Sen","Suresh Nayak","Ritika Dubey","Ajay Biswas",
"Monika Choudhury","Prakash Menon","Varsha Patel","Sanjay Pillai","Usha Rajan",
"Nitesh Thakur","Ankita Srivastava","Pankaj Agrawal","Geeta Murthy","Vivek Shukla",
"Rashmi Hegde","Devraj Khanna","Chitra Sundaram","Arun Lal","Falguni Shah",
"Bhavesh Garg","Asha Krishnan","Mihir Desai","Nandini Basu","Tejas Sawant",
"Lata Venkatesh","Abhishek Roy","Poonam Dubey","Varun Batra","Smitha Nair",
"Chirag Modi","Anjali Tomar","Sunil Barve","Kavitha Suresh","Nitin Joshi",
"Reema Das","Shubham Chawla","Kriti Bhatt","Yash Oberoi","Sarika Pandey"
]
locations = [
"Mumbai","Bangalore","Delhi","Hyderabad","Chennai",
"Pune","Kolkata","Ahmedabad","Jaipur","Surat"
]
professions = [
"Data Analyst","Software Engineer","Product Manager",
"UX Designer","Data Scientist","DevOps Engineer",
"Business Analyst","ML Engineer","Full Stack Developer",
"Cloud Architect"
]
mbti_types = [
"INTJ","INTP","ENTJ","ENTP",
"INFJ","INFP","ENFJ","ENFP",
"ISTJ","ISFJ","ESTJ","ESFJ",
"ISTP","ISFP","ESTP","ESFP"
]
summary_templates = [
"Data analyst with {} years of experience in healthcare analytics, skilled in SQL, Python, Power BI, and business reporting.",
"Software engineer with {} years of experience building scalable web applications, REST APIs, and cloud-native solutions.",
"Machine learning engineer with {} years of experience developing recommendation systems, NLP pipelines, and predictive models.",
"Product manager with {} years of experience leading agile teams and delivering customer-centric digital products.",
"DevOps engineer with {} years of experience automating deployments, CI/CD workflows, and cloud infrastructure management.",
"Business analyst with {} years of experience translating business requirements into data-driven strategic decisions.",
"Cloud architect with {} years of experience designing secure, scalable, and cost-efficient cloud platforms.",
"Full-stack developer with {} years of experience building responsive applications using modern frontend and backend technologies.",
"UX designer with {} years of experience creating user-centered digital experiences backed by research and usability testing.",
"Data scientist with {} years of experience applying statistical modeling, machine learning, and visualization techniques.",
"AI researcher with {} years of experience exploring deep learning, computer vision, and intelligent automation systems.",
"Cybersecurity specialist with {} years of experience securing enterprise systems and conducting risk assessments.",
"FinTech professional with {} years of experience building innovative financial products and digital payment solutions.",
"Healthcare technology specialist with {} years of experience improving patient outcomes through analytics and digital transformation.",
"EdTech professional with {} years of experience designing learning platforms and technology-enabled education solutions.",
"Supply chain analyst with {} years of experience optimizing logistics operations through forecasting and analytics.",
"Marketing analytics professional with {} years of experience leveraging customer data to drive business growth.",
"Startup enthusiast with {} years of experience building products in fast-paced entrepreneurial environments.",
"Research engineer with {} years of experience combining software engineering and advanced data analysis techniques.",
"Technology consultant with {} years of experience helping organizations adopt scalable digital solutions."
]
about_templates = [
"I enjoy solving real-world problems, mentoring junior professionals, and contributing to collaborative team environments.",
"Passionate about continuous learning and innovation, I thrive when working on challenging projects that create measurable impact.",
"I value teamwork, curiosity, and open communication while striving to build meaningful professional relationships.",
"Outside work, I enjoy reading, fitness, and exploring emerging technologies that shape the future.",
"I thrive in collaborative environments and enjoy sharing knowledge with colleagues from diverse backgrounds.",
"I believe in lifelong learning and enjoy taking on new challenges that help me grow professionally and personally.",
"My work style combines analytical thinking with creativity, allowing me to approach problems from multiple perspectives.",
"I enjoy mentoring others, exchanging ideas, and contributing to communities that promote knowledge sharing.",
"I value integrity, accountability, and a strong sense of ownership in every project I undertake.",
"I am naturally curious and enjoy exploring innovative solutions to complex business and technical challenges.",
"I appreciate diverse viewpoints and enjoy collaborating with people who bring unique perspectives to the table.",
"I strive to maintain a balance between professional growth, personal well-being, and meaningful relationships.",
"I enjoy participating in professional communities, attending conferences, and staying updated with industry trends.",
"I am motivated by opportunities to create positive impact through technology and data-driven decision making.",
"I enjoy working in environments that encourage experimentation, creativity, and continuous improvement.",
"I value empathy and effective communication as essential qualities for successful teamwork and leadership.",
"I enjoy helping others succeed and believe that collaboration often produces the best outcomes.",
"My interests include learning new skills, networking with professionals, and contributing to impactful initiatives.",
"I am driven by curiosity and enjoy discovering innovative approaches to long-standing problems.",
"I believe meaningful work comes from combining technical expertise with a genuine desire to help people."
]
interest_pool = [
"Artificial Intelligence",
"Machine Learning",
"Data Science",
"Analytics",
"Cloud Computing",
"Cybersecurity",
"Software Development",
"Startups",
"Entrepreneurship",
"Product Management",
"Public Speaking",
"Teaching",
"Reading",
"Writing",
"Fitness",
"Running",
"Yoga",
"Travel",
"Photography",
"Music",
"Gaming",
"Cooking",
"Finance",
"Investing",
"Blockchain",
"Open Source",
"Research",
"Robotics",
"Design",
"Mentoring"
]
users = []
for i in range(75):
    users.append({
        "user_id": f"U{i+1:03d}",
        "name": names[i],
        "age": random.randint(22,42),
        "location": random.choice(locations),
        "profession": random.choice(professions),
        "experience_years": random.randint(1,10),
        "professional_summary": random.choice(summary_templates).format(random.randint(1,10)),
        "about_me": random.choice(about_templates),
        "mbti": random.choice(mbti_types),
        "interests": ", ".join(random.sample(interest_pool,random.randint(3, 5)))
    })
users_df = pd.DataFrame(users)
users_df.to_csv("data/users.csv",index=False)
feedback_rows = []
for uid in users_df["user_id"]:
    for _ in range(random.randint(5,10)):
        match = random.choice(users_df["user_id"].tolist())
        if match == uid:
            continue
        text_score = round(random.uniform(30,100),2)
        mbti_score = random.choice([50,60,70,80,90,95])
        location_score = random.choice([20,60,100])
        action = 1 if (text_score*0.5 +mbti_score*0.3 +location_score*0.2) > 70 else 0
        feedback_rows.append({
            "user_id": uid,
            "matched_user_id": match,
            "text_score": text_score,
            "mbti_score": mbti_score,
            "location_score": location_score,
            "action": action,
            "timestamp": (datetime.now()-timedelta(days=random.randint(1,180))).strftime("%Y-%m-%d")
        })
feedback_df = pd.DataFrame(feedback_rows)
feedback_df.to_csv("data/feedback.csv",index=False)
print("users.csv generated")
print("feedback.csv generated")
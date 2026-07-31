/**
 * CALCULATOR HUB DATABASE (100 CALCULATORS)
 * Contains metadata, inputs schema, formula descriptions, SEO content, and FAQs.
 */

const CALCULATOR_CATEGORIES = {
  education: {
    id: "education",
    name: "Education Calculators",
    icon: "🎓",
    desc: "Calculate CGPA, GPA, percentage, study schedules, rank predictions, and marks.",
    url: "/calculators/education.html"
  },
  health: {
    id: "health",
    name: "Health & Fitness Calculators",
    icon: "❤️",
    desc: "Monitor BMI, BMR, daily calorie intake, water requirements, macros, and sleep cycles.",
    url: "/calculators/health.html"
  },
  finance: {
    id: "finance",
    name: "Finance Calculators",
    icon: "💰",
    desc: "Calculate EMI, SIP returns, loan interest, FD/RD growth, GST, and income taxes.",
    url: "/calculators/finance.html"
  },
  developer: {
    id: "developer",
    name: "Developer Tools",
    icon: "💻",
    desc: "Generate secure passwords, QR codes, format JSON, encode HTML/URLs, and convert bases.",
    url: "/calculators/developer.html"
  },
  math: {
    id: "math",
    name: "Math Calculators",
    icon: "📐",
    desc: "Scientific calculator, fractions, LCM/HCF, area, volume, and percentage difference.",
    url: "/calculators/math.html"
  },
  "daily-tools": {
    id: "daily-tools",
    name: "Daily Utility Tools",
    icon: "⚡",
    desc: "Time calculations, age gap, universal unit converters, electricity bills, and fuel costs.",
    url: "/calculators/daily-tools.html"
  },
  "fitness-advanced": {
    id: "fitness-advanced",
    name: "Fitness Advanced",
    icon: "🏋️",
    desc: "Calculate 1RM, calories burned per activity, pushups, step distance, and water weight.",
    url: "/calculators/fitness-advanced.html"
  },
  "seo-tools": {
    id: "seo-tools",
    name: "Extra SEO & Text Tools",
    icon: "🔤",
    desc: "CGPA to percentage, word counter, password strength tester, text case converter.",
    url: "/calculators/seo-tools.html"
  }
};

const CALCULATORS_DB = [
  // ==================== 1. EDUCATION (1-15) ====================
  {
    id: "cgpa-calculator",
    category: "education",
    title: "CGPA Calculator",
    subtitle: "Calculate Cumulative Grade Point Average easily.",
    metaTitle: "CGPA Calculator - Calculate Cumulative Grade Point Average Online",
    metaDesc: "Free CGPA Calculator to calculate Cumulative Grade Point Average for school and university students with step-by-step grade breakdown.",
    inputs: [
      { id: "gpas", label: "Semester GPAs (comma separated)", type: "text", default: "8.5, 9.0, 8.2, 8.8" }
    ],
    formula: "CGPA = (Sum of all Semester GPAs) / (Total Number of Semesters)",
    intro: "The CGPA Calculator helps school, college, and university students compute their Cumulative Grade Point Average across multiple semesters accurately.",
    howTo: ["Enter your semester GPAs separated by commas.", "Click Calculate.", "View your overall CGPA and percentage equivalent."],
    faqs: [
      { q: "What is CGPA?", a: "CGPA stands for Cumulative Grade Point Average, representing your overall academic performance across all completed semesters." },
      { q: "How to convert CGPA to Percentage?", a: "Multiply your CGPA by 9.5 (or your university specific factor) to get your percentage." }
    ]
  },
  {
    id: "gpa-calculator",
    category: "education",
    title: "GPA Calculator",
    subtitle: "Calculate semester grade point average based on credits and grades.",
    metaTitle: "GPA Calculator - Calculate Semester GPA Online",
    metaDesc: "Easy GPA Calculator for students. Input course grades and credits to compute your term Grade Point Average instantly.",
    inputs: [
      { id: "grades", label: "Grades (comma separated points, e.g. 4,3,3.5,4)", type: "text", default: "4, 3.5, 3, 4" },
      { id: "credits", label: "Credits per course (comma separated, e.g. 3,4,3,2)", type: "text", default: "3, 4, 3, 2" }
    ],
    formula: "GPA = Sum(Grade Points × Credits) / Sum(Total Credits)",
    intro: "Calculate your Semester Grade Point Average accurately using weighted course credits and earned grade points.",
    howTo: ["Input your grade points earned per subject.", "Input corresponding course credits.", "Click Calculate."],
    faqs: [{ q: "What scale does this GPA calculator use?", a: "It accepts standard 4.0, 5.0, or 10.0 grade point scales." }]
  },
  {
    id: "percentage-calculator",
    category: "education",
    title: "Percentage Calculator",
    subtitle: "Calculate percentages, percentage change, and fractions.",
    metaTitle: "Percentage Calculator - Calculate Percentages Online",
    metaDesc: "Free online percentage calculator. Find percentage of a number, percentage increase/decrease, and what percent one number is of another.",
    inputs: [
      { id: "value", label: "What is X %", type: "number", default: 15 },
      { id: "total", label: "of Y", type: "number", default: 250 }
    ],
    formula: "Result = (X / 100) × Y",
    intro: "Calculate any percentage quickly for exams, shopping discounts, taxes, or general math problems.",
    howTo: ["Enter the percentage value X.", "Enter the base total number Y.", "Click Calculate."],
    faqs: [{ q: "How do you calculate percentage?", a: "Divide the part by the total and multiply by 100." }]
  },
  {
    id: "marks-calculator",
    category: "education",
    title: "Marks Calculator",
    subtitle: "Compute total marks obtained and overall percentage.",
    metaTitle: "Marks Calculator - Calculate Total Marks & Percentage",
    metaDesc: "Calculate total exam marks obtained, missing marks needed, and final score percentage instantly.",
    inputs: [
      { id: "obtained", label: "Marks Obtained", type: "number", default: 425 },
      { id: "total", label: "Maximum Marks", type: "number", default: 500 }
    ],
    formula: "Percentage = (Marks Obtained / Total Marks) × 100",
    intro: "Calculate overall exam score percentages and grade standings in seconds.",
    howTo: ["Enter your obtained marks.", "Enter total maximum marks.", "Click Calculate."],
    faqs: [{ q: "What is a good pass percentage?", a: "Most academic institutions consider 40% to 50% as the minimum passing threshold." }]
  },
  {
    id: "attendance-calculator",
    category: "education",
    title: "Attendance Calculator",
    subtitle: "Calculate your current attendance percentage and classes needed.",
    metaTitle: "Attendance Calculator - Check Minimum Class Attendance Needed",
    metaDesc: "Find your current attendance percentage and calculate how many future classes you must attend to reach your target percentage (75% or 80%).",
    inputs: [
      { id: "attended", label: "Classes Attended", type: "number", default: 45 },
      { id: "total", label: "Total Classes Conducted", type: "number", default: 60 },
      { id: "target", label: "Target Attendance %", type: "number", default: 75 }
    ],
    formula: "Current % = (Attended / Total) × 100. Target Classes Needed = Math.ceil((Target/100 * Total - Attended) / (1 - Target/100))",
    intro: "Never miss exam eligibility! Calculate your current attendance percentage and know exactly how many upcoming lectures you must attend to meet the required threshold.",
    howTo: ["Enter classes attended.", "Enter total classes held so far.", "Set your target attendance %.", "Click Calculate."],
    faqs: [{ q: "Why is 75% attendance mandatory?", a: "Many colleges enforce a 75% minimum attendance requirement to ensure academic discipline." }]
  },
  {
    id: "sgpa-calculator",
    category: "education",
    title: "SGPA Calculator",
    subtitle: "Calculate Semester Grade Point Average from credits and subject grades.",
    metaTitle: "SGPA Calculator - Calculate Semester Grade Point Average",
    metaDesc: "Calculate your SGPA online for college exams. Input subject grades and credits to compute semester results.",
    inputs: [
      { id: "sgpa_points", label: "Grade Points (e.g. 9, 8, 10, 7)", type: "text", default: "9, 8, 10, 7, 9" },
      { id: "sgpa_credits", label: "Subject Credits (e.g. 4, 4, 3, 3, 2)", type: "text", default: "4, 4, 3, 3, 2" }
    ],
    formula: "SGPA = ∑(Grade Point × Credit) / ∑(Credits)",
    intro: "Calculate your Semester Grade Point Average (SGPA) with weighted credit points.",
    howTo: ["Enter subject grade points.", "Enter credit allocations.", "Click Calculate."],
    faqs: [{ q: "What is SGPA?", a: "SGPA stands for Semester Grade Point Average earned in a single academic term." }]
  },
  {
    id: "grade-calculator",
    category: "education",
    title: "Grade Calculator",
    subtitle: "Determine the score required on your final exam to achieve your desired class grade.",
    metaTitle: "Final Grade Calculator - Find Required Exam Score",
    metaDesc: "Calculate what grade you need on your final exam to get an A, B, or overall target course grade.",
    inputs: [
      { id: "current_grade", label: "Current Grade (%)", type: "number", default: 82 },
      { id: "target_grade", label: "Desired Overall Grade (%)", type: "number", default: 85 },
      { id: "final_weight", label: "Final Exam Weight (%)", type: "number", default: 25 }
    ],
    formula: "Required Score = (Target - Current × (1 - Weight)) / Weight",
    intro: "Find out exactly what score you need on your final exam or project to reach your target overall course grade.",
    howTo: ["Enter your current overall class percentage.", "Enter your desired target grade.", "Enter the percentage weight of the final exam."],
    faqs: [{ q: "What if required score is above 100%?", a: "If the required score exceeds 100%, extra credit or a higher current score is needed to achieve the target grade." }]
  },
  {
    id: "study-time-calculator",
    category: "education",
    title: "Study Time Calculator",
    subtitle: "Plan daily study hours based on subjects, credit loads, and exam dates.",
    metaTitle: "Study Time Calculator - Daily Study Hours Planner",
    metaDesc: "Calculate ideal weekly and daily study hours per subject according to credit difficulty.",
    inputs: [
      { id: "credits_total", label: "Total Credit Hours", type: "number", default: 15 },
      { id: "difficulty", label: "Course Difficulty Level (1-3)", type: "number", default: 2 }
    ],
    formula: "Weekly Hours = Total Credits × Difficulty Factor (2 to 3 hrs/credit)",
    intro: "Optimize your study schedule with recommended study hours per subject and day.",
    howTo: ["Enter total course credits.", "Select difficulty level.", "Click Calculate."],
    faqs: [{ q: "How many hours should I study per credit hour?", a: "Universities recommend 2 to 3 study hours outside of class for every 1 credit hour." }]
  },
  {
    id: "exam-score-calculator",
    category: "education",
    title: "Exam Score Calculator",
    subtitle: "Calculate weighted exam scores and final semester standing.",
    metaTitle: "Exam Score Calculator - Weighted Grade Calculation",
    metaDesc: "Free weighted exam score calculator for students to evaluate assignments, quizzes, and midterm weights.",
    inputs: [
      { id: "scores", label: "Assignment Scores (%)", type: "text", default: "90, 85, 78, 92" },
      { id: "weights", label: "Weights (%)", type: "text", default: "20, 20, 30, 30" }
    ],
    formula: "Weighted Final Score = ∑(Score × Weight / 100)",
    intro: "Calculate total weighted academic score across quizzes, midterms, projects, and final exams.",
    howTo: ["Enter exam scores.", "Enter relative category weights.", "Click Calculate."],
    faqs: [{ q: "Do weights need to sum to 100%?", a: "Yes, all assignment and exam category weights must sum to 100%." }]
  },
  {
    id: "rank-predictor",
    category: "education",
    title: "Rank Predictor",
    subtitle: "Predict competitive exam percentile and rank based on raw score.",
    metaTitle: "Rank Predictor - Estimate Percentile & Rank Online",
    metaDesc: "Predict your estimated rank and percentile from test marks for competitive entrance exams.",
    inputs: [
      { id: "raw_score", label: "Your Raw Score", type: "number", default: 180 },
      { id: "max_score", label: "Maximum Test Marks", type: "number", default: 300 },
      { id: "total_candidates", label: "Total Test Takers", type: "number", default: 100000 }
    ],
    formula: "Estimated Rank = Total Candidates × (1 - (Raw Score / Max Score)^1.2)",
    intro: "Get a statistical estimate of your candidate rank and percentile based on competitive exam scores.",
    howTo: ["Enter your score.", "Enter exam total marks.", "Enter total test takers count."],
    faqs: [{ q: "How accurate is the rank prediction?", a: "The rank prediction is a statistical estimate based on normalized bell curve distributions." }]
  },
  {
    id: "age-calculator",
    category: "education",
    title: "Age Calculator",
    subtitle: "Calculate exact age in years, months, days, hours, and minutes.",
    metaTitle: "Age Calculator - Calculate Exact Age from Birth Date",
    metaDesc: "Free age calculator. Calculate your exact age in years, months, days, weeks, hours, and seconds from date of birth.",
    inputs: [
      { id: "dob", label: "Date of Birth", type: "date", default: "2000-01-01" }
    ],
    formula: "Age = Current Date - Date of Birth",
    intro: "Calculate your precise age down to years, months, days, and total days lived.",
    howTo: ["Select your birth date.", "Click Calculate.", "View complete lifespan details."],
    faqs: [{ q: "Does this account for leap years?", a: "Yes, leap year days are calculated automatically." }]
  },
  {
    id: "date-difference-calculator",
    category: "education",
    title: "Date Difference Calculator",
    subtitle: "Calculate days, weeks, and months between two dates.",
    metaTitle: "Date Difference Calculator - Days Between Dates",
    metaDesc: "Find total days, business days, weeks, and months between any two calendar dates online.",
    inputs: [
      { id: "date1", label: "Start Date", type: "date", default: "2026-01-01" },
      { id: "date2", label: "End Date", type: "date", default: "2026-12-31" }
    ],
    formula: "Difference = End Date - Start Date",
    intro: "Find exact duration between any two dates in days, weeks, or months.",
    howTo: ["Select start date.", "Select end date.", "Click Calculate."],
    faqs: [{ q: "Can I measure countdowns to future events?", a: "Yes! Set today as start date and future date as end date." }]
  },
  {
    id: "semester-calculator",
    category: "education",
    title: "Semester Calculator",
    subtitle: "Track multi-semester GPA performance and cumulative score progression.",
    metaTitle: "Semester Calculator - Cumulative Academic Progression Tracker",
    metaDesc: "Calculate cumulative academic progress over multiple college semesters.",
    inputs: [
      { id: "sem_scores", label: "Semester GPAs (e.g. 7.8, 8.2, 8.5)", type: "text", default: "7.8, 8.2, 8.5" }
    ],
    formula: "Progression Average = ∑(SGPA) / Number of Semesters",
    intro: "Monitor grade trend progression across consecutive academic semesters.",
    howTo: ["Enter all finished semester GPAs.", "Click Calculate."],
    faqs: [{ q: "Can I predict final graduation CGPA?", a: "Yes, add projected future semester GPAs to estimate your final graduation score." }]
  },
  {
    id: "credit-calculator",
    category: "education",
    title: "Credit Calculator",
    subtitle: "Calculate total completed course credits and graduation requirements.",
    metaTitle: "Academic Credit Calculator - Graduation Credit Tracker",
    metaDesc: "Track completed university course credits and remaining credit requirements for degree completion.",
    inputs: [
      { id: "completed_credits", label: "Completed Credits", type: "number", default: 78 },
      { id: "total_required", label: "Total Degree Credits Required", type: "number", default: 120 }
    ],
    formula: "Remaining Credits = Required Credits - Completed Credits. Progress = (Completed / Required) × 100",
    intro: "Track degree progress and calculate credit hours remaining for graduation.",
    howTo: ["Enter earned credits.", "Enter degree requirement total.", "Click Calculate."],
    faqs: [{ q: "How many credits is a typical degree?", a: "Bachelor's degrees generally require 120 to 130 credit hours." }]
  },
  {
    id: "average-calculator",
    category: "education",
    title: "Average Calculator",
    subtitle: "Calculate mean average, total sum, and count of a dataset.",
    metaTitle: "Average Calculator - Calculate Mean & Sum Online",
    metaDesc: "Calculate arithmetic mean, sum, count, minimum, and maximum of a set of numbers.",
    inputs: [
      { id: "num_list", label: "Numbers (comma separated)", type: "text", default: "12, 45, 67, 89, 23, 56" }
    ],
    formula: "Average (Mean) = Sum of all values / Total count of values",
    intro: "Quickly compute arithmetic average (mean) for grades, sales, or test scores.",
    howTo: ["Type numbers separated by commas.", "Click Calculate."],
    faqs: [{ q: "What is the difference between mean and median?", a: "Mean is the sum divided by count; median is the middle number in a sorted list." }]
  },

  // ==================== 2. HEALTH AND FITNESS (16-30) ====================
  {
    id: "bmi-calculator",
    category: "health",
    title: "BMI Calculator",
    subtitle: "Calculate Body Mass Index and health category status.",
    metaTitle: "BMI Calculator - Calculate Body Mass Index Online",
    metaDesc: "Free BMI calculator to check Body Mass Index for adults. Calculates BMI, weight category, and healthy weight range.",
    inputs: [
      { id: "weight", label: "Weight (kg)", type: "number", default: 70 },
      { id: "height", label: "Height (cm)", type: "number", default: 175 }
    ],
    formula: "BMI = Weight (kg) / [Height (m)]²",
    intro: "Calculate your Body Mass Index (BMI) to understand your weight status (underweight, normal, overweight, or obese).",
    howTo: ["Enter weight in kg.", "Enter height in cm.", "Click Calculate."],
    faqs: [
      { q: "What is a healthy BMI range?", a: "A healthy adult BMI is between 18.5 and 24.9." },
      { q: "Does BMI apply to bodybuilders?", a: "BMI does not distinguish muscle mass from fat, so muscular athletes may have high BMI without high body fat." }
    ]
  },
  {
    id: "bmr-calculator",
    category: "health",
    title: "BMR Calculator",
    subtitle: "Calculate Basal Metabolic Rate using Mifflin-St Jeor equation.",
    metaTitle: "BMR Calculator - Calculate Basal Metabolic Rate Online",
    metaDesc: "Calculate your Basal Metabolic Rate (BMR) - the calories your body burns at rest every day.",
    inputs: [
      { id: "bmr_gender", label: "Gender", type: "select", options: ["Male", "Female"], default: "Male" },
      { id: "bmr_weight", label: "Weight (kg)", type: "number", default: 70 },
      { id: "bmr_height", label: "Height (cm)", type: "number", default: 175 },
      { id: "bmr_age", label: "Age (years)", type: "number", default: 25 }
    ],
    formula: "BMR (Male) = 10W + 6.25H - 5A + 5. BMR (Female) = 10W + 6.25H - 5A - 161",
    intro: "Calculate how many calories your body burns at complete rest just to keep vital organs functioning.",
    howTo: ["Select gender.", "Enter weight, height, and age.", "Click Calculate."],
    faqs: [{ q: "Why is BMR important?", a: "Knowing your BMR sets the baseline for calculating total daily calorie needs for weight loss or muscle gain." }]
  },
  {
    id: "calorie-calculator",
    category: "health",
    title: "Calorie Calculator",
    subtitle: "Calculate Total Daily Energy Expenditure (TDEE) and maintenance calories.",
    metaTitle: "Calorie Calculator - Calculate Daily TDEE & Calorie Needs",
    metaDesc: "Free daily calorie intake calculator for weight loss, maintenance, or muscle building based on activity levels.",
    inputs: [
      { id: "cal_bmr", label: "BMR (or enter weight in kg)", type: "number", default: 1650 },
      { id: "activity", label: "Activity Level", type: "select", options: ["Sedentary (office job)", "Light exercise (1-3 days/wk)", "Moderate exercise (3-5 days/wk)", "Heavy exercise (6-7 days/wk)"], default: "Moderate exercise (3-5 days/wk)" }
    ],
    formula: "TDEE = BMR × Activity Multiplier (1.2 to 1.725)",
    intro: "Determine exact daily calorie consumption required to maintain, lose, or gain weight.",
    howTo: ["Enter BMR value.", "Select your weekly physical activity level.", "Click Calculate."],
    faqs: [{ q: "How many calories deficit for weight loss?", a: "A daily calorie deficit of 500 kcal typically leads to ~0.5 kg (1 lb) weight loss per week." }]
  },
  {
    id: "protein-calculator",
    category: "health",
    title: "Protein Calculator",
    subtitle: "Calculate optimal daily protein intake for fitness goals.",
    metaTitle: "Protein Intake Calculator - Calculate Daily Protein Requirement",
    metaDesc: "Calculate daily protein intake in grams for muscle growth, fat loss, or general maintenance.",
    inputs: [
      { id: "prot_weight", label: "Body Weight (kg)", type: "number", default: 70 },
      { id: "prot_goal", label: "Fitness Goal", type: "select", options: ["Maintenance", "Muscle Building", "Fat Loss / Cutting"], default: "Muscle Building" }
    ],
    formula: "Protein = Body Weight (kg) × Factor (1.6g to 2.2g per kg)",
    intro: "Calculate how many grams of protein you need daily to build muscle or retain lean mass while cutting.",
    howTo: ["Enter body weight.", "Select fitness goal.", "Click Calculate."],
    faqs: [{ q: "How much protein is safe per day?", a: "Up to 2.2g per kg of body weight is safe and effective for active individuals." }]
  },
  {
    id: "water-intake-calculator",
    category: "health",
    title: "Water Intake Calculator",
    subtitle: "Calculate daily recommended water consumption.",
    metaTitle: "Daily Water Intake Calculator - Recommended Hydration Level",
    metaDesc: "Calculate your recommended daily water consumption in liters and glasses based on weight and activity.",
    inputs: [
      { id: "water_weight", label: "Body Weight (kg)", type: "number", default: 70 },
      { id: "exercise_min", label: "Daily Exercise (minutes)", type: "number", default: 45 }
    ],
    formula: "Water (L) = (Weight × 0.033) + (Exercise Minutes / 30 × 0.35)",
    intro: "Calculate your daily hydration requirements based on your body mass and physical exercise duration.",
    howTo: ["Enter body weight in kg.", "Enter daily workout time in minutes.", "Click Calculate."],
    faqs: [{ q: "Does coffee or tea count towards hydration?", a: "Yes, but plain water is best for optimal cellular hydration." }]
  },
  {
    id: "ideal-weight-calculator",
    category: "health",
    title: "Ideal Weight Calculator",
    subtitle: "Calculate ideal body weight using Devine, Hamwi, and Robinson formulas.",
    metaTitle: "Ideal Body Weight Calculator - Calculate IBW Online",
    metaDesc: "Find your healthy ideal body weight range based on height and gender using medical formulas.",
    inputs: [
      { id: "ibw_gender", label: "Gender", type: "select", options: ["Male", "Female"], default: "Male" },
      { id: "ibw_height", label: "Height (cm)", type: "number", default: 175 }
    ],
    formula: "Devine (Male) = 50 + 2.3 × (Height in inches - 60). Devine (Female) = 45.5 + 2.3 × (Height in inches - 60)",
    intro: "Determine your medical ideal body weight range according to validated clinical formulas.",
    howTo: ["Select gender.", "Enter height in cm.", "Click Calculate."],
    faqs: [{ q: "What is IBW?", a: "Ideal Body Weight (IBW) is a medical guideline estimating healthy body mass for height." }]
  },
  {
    id: "body-fat-calculator",
    category: "health",
    title: "Body Fat Calculator",
    subtitle: "Calculate body fat percentage using US Navy Method.",
    metaTitle: "Body Fat Calculator - US Navy Method Online",
    metaDesc: "Calculate body fat percentage, fat mass, and lean mass using waist, neck, hip, and height measurements.",
    inputs: [
      { id: "bf_gender", label: "Gender", type: "select", options: ["Male", "Female"], default: "Male" },
      { id: "bf_waist", label: "Waist Circumference (cm)", type: "number", default: 82 },
      { id: "bf_neck", label: "Neck Circumference (cm)", type: "number", default: 38 },
      { id: "bf_height", label: "Height (cm)", type: "number", default: 175 }
    ],
    formula: "US Navy Formula based on log10 of waist, neck, and height dimensions",
    intro: "Estimate your body fat percentage and lean muscle mass using the US Navy tape measurement method.",
    howTo: ["Select gender.", "Measure and enter waist and neck circumferences.", "Enter height.", "Click Calculate."],
    faqs: [{ q: "What is a healthy body fat percentage?", a: "For men: 10-20%; for women: 18-28% is generally considered healthy." }]
  },
  {
    id: "macro-calculator",
    category: "health",
    title: "Macro Calculator",
    subtitle: "Calculate daily Macronutrient breakdown (Carbs, Protein, Fats).",
    metaTitle: "Macro Calculator - Calculate Macronutrient Grams",
    metaDesc: "Calculate macronutrient target grams for keto, balanced, high protein, or low carb diets.",
    inputs: [
      { id: "macro_tdee", label: "Daily Target Calories (kcal)", type: "number", default: 2200 },
      { id: "macro_split", label: "Diet Type", type: "select", options: ["Balanced (50C/30P/20F)", "High Protein (40C/40P/20F)", "Keto (5C/30P/65F)"], default: "Balanced (50C/30P/20F)" }
    ],
    formula: "Carbs (g) = Cal × % / 4. Protein (g) = Cal × % / 4. Fat (g) = Cal × % / 9",
    intro: "Calculate exact daily grams of carbohydrates, protein, and dietary fats to match your total calorie targets.",
    howTo: ["Enter daily calorie target.", "Select diet split preference.", "Click Calculate."],
    faqs: [{ q: "Why do fats have 9 calories per gram?", a: "Dietary fat is more energy dense than carbohydrates and protein, which both provide 4 kcal/g." }]
  },
  {
    id: "running-calories-calculator",
    category: "health",
    title: "Running Calories Calculator",
    subtitle: "Calculate calories burned while running or jogging.",
    metaTitle: "Running Calories Burned Calculator Online",
    metaDesc: "Calculate total calories burned running based on speed, distance, running duration, and body weight.",
    inputs: [
      { id: "run_weight", label: "Weight (kg)", type: "number", default: 70 },
      { id: "run_dist", label: "Distance (km)", type: "number", default: 5 },
      { id: "run_time", label: "Time (minutes)", type: "number", default: 30 }
    ],
    formula: "Calories Burned = MET × Weight (kg) × Duration (hours)",
    intro: "Estimate exact energy expenditure burned during a running or jogging session.",
    howTo: ["Enter body weight.", "Enter distance run.", "Enter time taken.", "Click Calculate."],
    faqs: [{ q: "Does running speed affect calorie burn?", a: "Yes, running faster increases MET intensity and total calorie expenditure per minute." }]
  },
  {
    id: "sleep-calculator",
    category: "health",
    title: "Sleep Calculator",
    subtitle: "Calculate optimal bedtime and wake-up times based on 90-minute sleep cycles.",
    metaTitle: "Sleep Calculator - Calculate Best Bedtime & Wake Up Time",
    metaDesc: "Find the best time to go to sleep or wake up feeling refreshed based on natural 90-minute REM sleep cycles.",
    inputs: [
      { id: "wake_time", label: "Desired Wake Up Time (e.g. 07:00)", type: "text", default: "07:00" }
    ],
    formula: "Cycle Count = 5 or 6 cycles × 90 minutes + 15 min to fall asleep",
    intro: "Wake up feeling energized by planning sleep around natural 90-minute REM sleep cycles.",
    howTo: ["Enter when you need to wake up.", "Click Calculate to see recommended bedtimes."],
    faqs: [{ q: "How long is a sleep cycle?", a: "An average adult sleep cycle lasts approximately 90 minutes." }]
  },
  {
    id: "waist-height-ratio-calculator",
    category: "health",
    title: "Waist to Height Ratio Calculator",
    subtitle: "Calculate Waist-to-Height Ratio (WHtR) health risk index.",
    metaTitle: "Waist to Height Ratio Calculator - WHtR Health Risk",
    metaDesc: "Check your Waist-to-Height Ratio to assess abdominal fat distribution and cardiovascular risk.",
    inputs: [
      { id: "whtr_waist", label: "Waist Circumference (cm)", type: "number", default: 80 },
      { id: "whtr_height", label: "Height (cm)", type: "number", default: 175 }
    ],
    formula: "WHtR = Waist Circumference / Height",
    intro: "Evaluate cardiometabolic risk by comparing waist size relative to body height.",
    howTo: ["Enter waist circumference in cm.", "Enter height in cm.", "Click Calculate."],
    faqs: [{ q: "What is a healthy WHtR ratio?", a: "Keeping your waist circumference to less than half your height (ratio < 0.50) is healthy." }]
  },
  {
    id: "lean-body-mass-calculator",
    category: "health",
    title: "Lean Body Mass Calculator",
    subtitle: "Calculate Lean Body Mass (LBM) using Boer and James equations.",
    metaTitle: "Lean Body Mass Calculator - Calculate LBM Online",
    metaDesc: "Calculate total muscle and non-fat mass in kilograms using Boer and James equations.",
    inputs: [
      { id: "lbm_gender", label: "Gender", type: "select", options: ["Male", "Female"], default: "Male" },
      { id: "lbm_weight", label: "Weight (kg)", type: "number", default: 75 },
      { id: "lbm_height", label: "Height (cm)", type: "number", default: 178 }
    ],
    formula: "Boer (Male) = 0.407W + 0.267H - 19.2. Boer (Female) = 0.252W + 0.473H - 48.3",
    intro: "Calculate total body weight excluding fat mass (muscles, bones, organs, and body water).",
    howTo: ["Select gender.", "Enter body weight and height.", "Click Calculate."],
    faqs: [{ q: "Why is Lean Body Mass important?", a: "LBM helps determine baseline metabolic rates and accurate drug dosing in healthcare." }]
  },
  {
    id: "weight-loss-calculator",
    category: "health",
    title: "Weight Loss Calculator",
    subtitle: "Calculate target date and daily calorie deficit to reach weight loss goals.",
    metaTitle: "Weight Loss Calculator - Time to Reach Target Weight",
    metaDesc: "Calculate how long it will take to lose weight based on daily calorie deficit.",
    inputs: [
      { id: "current_w", label: "Current Weight (kg)", type: "number", default: 85 },
      { id: "target_w", label: "Target Weight (kg)", type: "number", default: 75 },
      { id: "deficit", label: "Daily Calorie Deficit (kcal)", type: "number", default: 500 }
    ],
    formula: "Days Needed = ((Current Weight - Target Weight) × 7700) / Daily Deficit",
    intro: "Calculate the exact number of weeks required to achieve your desired target body weight safely.",
    howTo: ["Enter current weight.", "Enter target weight.", "Enter planned daily calorie deficit."],
    faqs: [{ q: "How many calories equal 1 kg of fat?", a: "Approximately 7,700 kcal deficit equals 1 kg of body fat loss." }]
  },
  {
    id: "heart-rate-calculator",
    category: "health",
    title: "Heart Rate Calculator",
    subtitle: "Calculate Max Heart Rate and Target Heart Rate (THR) training zones.",
    metaTitle: "Target Heart Rate Calculator - Exercise Heart Zones",
    metaDesc: "Calculate Maximum Heart Rate and target cardio training zones for endurance and fat burn.",
    inputs: [
      { id: "hr_age", label: "Age (years)", type: "number", default: 30 },
      { id: "hr_rest", label: "Resting Heart Rate (bpm)", type: "number", default: 65 }
    ],
    formula: "Max HR = 220 - Age. Karvonen THR = ((Max HR - Rest HR) × Intensity%) + Rest HR",
    intro: "Calculate your heart rate zones for fat burning, aerobic endurance, and peak cardiovascular performance.",
    howTo: ["Enter your age.", "Enter resting pulse rate.", "Click Calculate."],
    faqs: [{ q: "What is a normal resting heart rate?", a: "Normal resting heart rate for adults ranges between 60 and 100 beats per minute." }]
  },
  {
    id: "pregnancy-due-date-calculator",
    category: "health",
    title: "Pregnancy Due Date Calculator",
    subtitle: "Calculate estimated due date (EDD) using Naegele's rule.",
    metaTitle: "Pregnancy Due Date Calculator - Calculate EDD Online",
    metaDesc: "Calculate estimated pregnancy due date based on last menstrual period (LMP).",
    inputs: [
      { id: "lmp_date", label: "First day of Last Menstrual Period (LMP)", type: "date", default: "2026-01-15" }
    ],
    formula: "Due Date = LMP + 280 days (40 weeks)",
    intro: "Estimate your baby's delivery due date and pregnancy milestones based on LMP.",
    howTo: ["Select date of last period.", "Click Calculate."],
    faqs: [{ q: "How long is full term pregnancy?", a: "Full term pregnancy ranges from 39 to 40 weeks." }]
  },

  // ==================== 3. FINANCE (31-50) ====================
  {
    id: "emi-calculator",
    category: "finance",
    title: "EMI Calculator",
    subtitle: "Calculate Equated Monthly Installment for home, car, or personal loans.",
    metaTitle: "EMI Calculator - Calculate Loan EMI Online",
    metaDesc: "Free EMI calculator for home loans, car loans, and personal loans. Displays monthly EMI, total interest, and repayment schedule.",
    inputs: [
      { id: "emi_principal", label: "Loan Amount ($ / ₹)", type: "number", default: 100000 },
      { id: "emi_rate", label: "Interest Rate (% per annum)", type: "number", default: 8.5 },
      { id: "emi_tenure", label: "Loan Tenure (Years)", type: "number", default: 15 }
    ],
    formula: "EMI = [P × R × (1+R)^N] / [(1+R)^N - 1]",
    intro: "Calculate monthly loan repayment installments, total interest payable, and overall loan cost.",
    howTo: ["Enter total loan principal.", "Enter annual interest rate.", "Enter tenure in years."],
    faqs: [
      { q: "What is EMI?", a: "EMI stands for Equated Monthly Installment paid to repay loan principal and interest every month." },
      { q: "How can I reduce EMI?", a: "Extend tenure, make prepayments, or negotiate a lower interest rate." }
    ]
  },
  {
    id: "loan-calculator",
    category: "finance",
    title: "Loan Calculator",
    subtitle: "Calculate loan repayment terms and total interest charges.",
    metaTitle: "Loan Repayment Calculator - Calculate Principal & Interest",
    metaDesc: "Calculate monthly payments and total interest payable across personal, student, or auto loans.",
    inputs: [
      { id: "loan_p", label: "Loan Amount", type: "number", default: 25000 },
      { id: "loan_r", label: "Annual Interest Rate (%)", type: "number", default: 7 },
      { id: "loan_months", label: "Tenure (Months)", type: "number", default: 36 }
    ],
    formula: "Monthly Payment = P × r / (1 - (1+r)^-n)",
    intro: "Determine exact monthly loan payments and interest costs over any specified duration.",
    howTo: ["Enter loan amount.", "Enter rate of interest.", "Enter tenure in months."],
    faqs: [{ q: "Does interest compound monthly?", a: "Most consumer bank loans compound monthly on reducing principal balance." }]
  },
  {
    id: "sip-calculator",
    category: "finance",
    title: "SIP Calculator",
    subtitle: "Calculate Mutual Fund Systematic Investment Plan returns.",
    metaTitle: "SIP Calculator - Mutual Fund Investment Returns",
    metaDesc: "Calculate future wealth growth and total returns from monthly SIP investments in mutual funds.",
    inputs: [
      { id: "sip_monthly", label: "Monthly Investment Amount", type: "number", default: 5000 },
      { id: "sip_rate", label: "Expected Annual Return (%)", type: "number", default: 12 },
      { id: "sip_years", label: "Investment Duration (Years)", type: "number", default: 10 }
    ],
    formula: "M = P × ({[1 + i]^n - 1} / i) × (1 + i)",
    intro: "Calculate your future wealth accumulation from monthly Systematic Investment Plans (SIP) in mutual funds.",
    howTo: ["Enter monthly investment.", "Enter expected annual rate of return.", "Enter investment period in years."],
    faqs: [{ q: "What is power of compounding in SIP?", a: "Reinvesting returns over long horizons generates compound exponential wealth growth." }]
  },
  {
    id: "fd-calculator",
    category: "finance",
    title: "FD Calculator",
    subtitle: "Calculate Fixed Deposit maturity value and interest earnings.",
    metaTitle: "FD Calculator - Fixed Deposit Interest & Maturity Value",
    metaDesc: "Calculate fixed deposit maturity amount and total interest earned for quarterly or annual compounding.",
    inputs: [
      { id: "fd_principal", label: "Deposit Amount", type: "number", default: 50000 },
      { id: "fd_rate", label: "Interest Rate (% p.a.)", type: "number", default: 7 },
      { id: "fd_years", label: "Tenure (Years)", type: "number", default: 5 }
    ],
    formula: "A = P × (1 + r/n)^(n×t)",
    intro: "Calculate total interest payout and maturity return for bank Fixed Deposits.",
    howTo: ["Enter deposit principal.", "Enter bank interest rate.", "Enter deposit term in years."],
    faqs: [{ q: "Is FD interest taxable?", a: "Yes, interest earned on Fixed Deposits is subject to income tax according to tax slabs." }]
  },
  {
    id: "rd-calculator",
    category: "finance",
    title: "RD Calculator",
    subtitle: "Calculate Recurring Deposit maturity value and interest.",
    metaTitle: "RD Calculator - Recurring Deposit Maturity Calculator",
    metaDesc: "Calculate total returns from monthly Recurring Deposit savings scheme.",
    inputs: [
      { id: "rd_monthly", label: "Monthly Deposit Amount", type: "number", default: 2000 },
      { id: "rd_rate", label: "Interest Rate (% p.a.)", type: "number", default: 6.8 },
      { id: "rd_months", label: "Tenure (Months)", type: "number", default: 24 }
    ],
    formula: "Maturity = P × N + P × N(N+1)/2 × (R/1200)",
    intro: "Calculate maturity returns for monthly recurring deposits with guaranteed interest growth.",
    howTo: ["Enter monthly deposit amount.", "Enter rate of interest.", "Enter tenure in months."],
    faqs: [{ q: "What is the difference between FD and RD?", a: "FD requires a lump sum deposit up front, while RD allows small monthly contributions." }]
  },
  {
    id: "compound-interest-calculator",
    category: "finance",
    title: "Compound Interest Calculator",
    subtitle: "Calculate interest on principal and accumulated interest.",
    metaTitle: "Compound Interest Calculator - Calculate Compound Growth",
    metaDesc: "Free compound interest calculator to compute future value with daily, monthly, or annual compounding frequency.",
    inputs: [
      { id: "ci_principal", label: "Initial Investment", type: "number", default: 10000 },
      { id: "ci_rate", label: "Annual Rate (%)", type: "number", default: 8 },
      { id: "ci_years", label: "Time (Years)", type: "number", default: 5 },
      { id: "ci_freq", label: "Compounding Frequency", type: "select", options: ["Annually (1)", "Quarterly (4)", "Monthly (12)"], default: "Monthly (12)" }
    ],
    formula: "A = P × (1 + r/n)^(n×t)",
    intro: "Calculate exponential compound interest growth over time with customizable compounding frequencies.",
    howTo: ["Enter initial capital.", "Enter interest rate.", "Enter years and select compounding frequency."],
    faqs: [{ q: "Why is compound interest called the 8th wonder?", a: "Because interest earns interest, accelerating wealth accumulation dramatically over time." }]
  },
  {
    id: "simple-interest-calculator",
    category: "finance",
    title: "Simple Interest Calculator",
    subtitle: "Calculate simple interest on principal sum.",
    metaTitle: "Simple Interest Calculator - Formula & Calculation",
    metaDesc: "Calculate simple interest and final total amount for loans or investments.",
    inputs: [
      { id: "si_p", label: "Principal ($ / ₹)", type: "number", default: 5000 },
      { id: "si_r", label: "Annual Rate (%)", type: "number", default: 5 },
      { id: "si_t", label: "Time (Years)", type: "number", default: 3 }
    ],
    formula: "SI = (P × R × T) / 100",
    intro: "Calculate basic linear interest accumulated over time without compounding.",
    howTo: ["Enter principal.", "Enter rate of interest.", "Enter time in years."],
    faqs: [{ q: "Where is simple interest used?", a: "Simple interest is often used for short-term personal loans, car financing, and simple bonds." }]
  },
  {
    id: "gst-calculator",
    category: "finance",
    title: "GST Calculator",
    subtitle: "Calculate GST Inclusive and Exclusive tax amounts.",
    metaTitle: "GST Calculator - Goods and Services Tax Calculator Online",
    metaDesc: "Calculate GST amount, net price, and gross price for inclusive and exclusive Goods and Services Tax rates.",
    inputs: [
      { id: "gst_amount", label: "Amount ($ / ₹)", type: "number", default: 1000 },
      { id: "gst_rate", label: "GST Rate (%)", type: "number", default: 18 },
      { id: "gst_type", label: "Calculation Type", type: "select", options: ["Add GST (Exclusive)", "Remove GST (Inclusive)"], default: "Add GST (Exclusive)" }
    ],
    formula: "Exclusive GST = Amount × Rate / 100. Inclusive GST = Amount - (Amount / (1 + Rate/100))",
    intro: "Calculate Goods and Services Tax (GST) easily for billing, invoice creation, and business accounting.",
    howTo: ["Enter total base amount.", "Select GST percentage rate.", "Choose Add or Remove GST."],
    faqs: [{ q: "What is inclusive vs exclusive GST?", a: "Exclusive GST is added on top of net price; inclusive GST is already part of total retail price." }]
  },
  {
    id: "discount-calculator",
    category: "finance",
    title: "Discount Calculator",
    subtitle: "Calculate sale discount, final price, and savings amount.",
    metaTitle: "Discount Calculator - Calculate Sale Price & Savings",
    metaDesc: "Calculate final discounted price, total money saved, and sales tax for shopping discounts.",
    inputs: [
      { id: "disc_orig", label: "Original Price ($)", type: "number", default: 150 },
      { id: "disc_pct", label: "Discount Percentage (%)", type: "number", default: 20 }
    ],
    formula: "Savings = Original Price × (Discount % / 100). Final Price = Original Price - Savings",
    intro: "Find out exact final prices and total savings during shopping clearance sales.",
    howTo: ["Enter original item price.", "Enter discount percentage.", "Click Calculate."],
    faqs: [{ q: "How to calculate double discounts?", a: "Apply the first discount percentage to the original price, then apply second discount to the remaining balance." }]
  },
  {
    id: "salary-calculator",
    category: "finance",
    title: "Salary Calculator",
    subtitle: "Convert annual salary to monthly, bi-weekly, weekly, and hourly pay.",
    metaTitle: "Salary Calculator - Convert Annual Salary to Hourly & Monthly",
    metaDesc: "Calculate net take-home pay, hourly wage, monthly salary, and paycheck breakdown.",
    inputs: [
      { id: "sal_annual", label: "Annual Gross Salary ($ / ₹)", type: "number", default: 60000 },
      { id: "sal_hours", label: "Hours Worked Per Week", type: "number", default: 40 }
    ],
    formula: "Monthly = Annual / 12. Hourly = Annual / (Hours per Week × 52)",
    intro: "Convert annual salary into equivalent monthly pay, bi-weekly checks, and hourly wage rates.",
    howTo: ["Enter gross annual income.", "Enter weekly work hours.", "Click Calculate."],
    faqs: [{ q: "How many working hours are in a standard year?", a: "A standard 40-hour work week equals 2,080 working hours per year." }]
  },
  {
    id: "income-tax-calculator",
    category: "finance",
    title: "Income Tax Calculator",
    subtitle: "Estimate income tax payable based on income tax slabs.",
    metaTitle: "Income Tax Calculator - Calculate Tax Liabilities",
    metaDesc: "Calculate annual income tax liabilities, effective tax rate, and net income after taxes.",
    inputs: [
      { id: "tax_income", label: "Annual Taxable Income ($ / ₹)", type: "number", default: 75000 },
      { id: "tax_deduct", label: "Deductions / Exemptions", type: "number", default: 10000 }
    ],
    formula: "Taxable Income = Gross Income - Deductions. Tax calculated per slab rates.",
    intro: "Estimate your federal or national income tax liability and net take-home income.",
    howTo: ["Enter gross annual income.", "Enter eligible tax deductions.", "Click Calculate."],
    faqs: [{ q: "What is marginal vs effective tax rate?", a: "Marginal rate is the tax rate on your top tier of income; effective rate is total tax paid divided by total income." }]
  },
  {
    id: "inflation-calculator",
    category: "finance",
    title: "Inflation Calculator",
    subtitle: "Calculate future purchasing power adjusted for inflation.",
    metaTitle: "Inflation Calculator - Calculate Future Value of Money",
    metaDesc: "Calculate how inflation decreases purchasing power over time and find future equivalent costs.",
    inputs: [
      { id: "inf_amount", label: "Current Amount ($ / ₹)", type: "number", default: 1000 },
      { id: "inf_rate", label: "Average Annual Inflation (%)", type: "number", default: 4 },
      { id: "inf_years", label: "Years into Future", type: "number", default: 10 }
    ],
    formula: "Future Equivalent = Amount × (1 + Rate/100)^Years",
    intro: "Understand how annual inflation erodes purchasing power over time and what future expenses will cost.",
    howTo: ["Enter present amount.", "Enter projected inflation rate.", "Enter number of years."],
    faqs: [{ q: "What is average historical inflation rate?", a: "Global historical inflation averages around 3% to 4% annually." }]
  },
  {
    id: "investment-calculator",
    category: "finance",
    title: "Investment Calculator",
    subtitle: "Calculate return on investment (ROI) and capital growth.",
    metaTitle: "Investment Return Calculator - Calculate ROI",
    metaDesc: "Calculate total investment returns, net profit percentage, and wealth accumulation over time.",
    inputs: [
      { id: "inv_initial", label: "Initial Investment", type: "number", default: 5000 },
      { id: "inv_final", label: "Final Value", type: "number", default: 8500 }
    ],
    formula: "ROI (%) = [(Final Value - Initial Investment) / Initial Investment] × 100",
    intro: "Calculate net return on investment (ROI) percentage and total net profit.",
    howTo: ["Enter initial capital invested.", "Enter final value.", "Click Calculate."],
    faqs: [{ q: "What is ROI?", a: "Return on Investment (ROI) measures efficiency and profitability of an investment ratio." }]
  },
  {
    id: "profit-loss-calculator",
    category: "finance",
    title: "Profit & Loss Calculator",
    subtitle: "Calculate profit amount, loss amount, and profit percentage.",
    metaTitle: "Profit and Loss Calculator - Business P&L Margin",
    metaDesc: "Calculate net profit or loss, profit margin percentage, and markup for business sales.",
    inputs: [
      { id: "cost_price", label: "Cost Price (CP)", type: "number", default: 400 },
      { id: "sell_price", label: "Selling Price (SP)", type: "number", default: 520 }
    ],
    formula: "Profit = SP - CP. Profit % = (Profit / CP) × 100",
    intro: "Calculate financial gain or loss percentage for merchandise sales and business transactions.",
    howTo: ["Enter cost price.", "Enter selling price.", "Click Calculate."],
    faqs: [{ q: "What is profit margin?", a: "Profit margin is profit expressed as a percentage of total selling price or revenue." }]
  },
  {
    id: "percentage-increase-calculator",
    category: "finance",
    title: "Percentage Increase Calculator",
    subtitle: "Calculate percentage increase or decrease between two values.",
    metaTitle: "Percentage Increase Calculator - Calculate % Change",
    metaDesc: "Calculate percentage increase or decrease between initial and final values easily.",
    inputs: [
      { id: "pct_initial", label: "Initial Value", type: "number", default: 50 },
      { id: "pct_final", label: "Final Value", type: "number", default: 75 }
    ],
    formula: "% Change = [(Final - Initial) / Initial] × 100",
    intro: "Calculate the exact percentage rise or drop between two numerical values.",
    howTo: ["Enter starting value.", "Enter ending value.", "Click Calculate."],
    faqs: [{ q: "What does negative percentage change mean?", a: "A negative result indicates a percentage decrease or reduction." }]
  },
  {
    id: "currency-converter",
    category: "finance",
    title: "Currency Converter",
    subtitle: "Convert amounts between major world currencies (USD, EUR, INR, GBP).",
    metaTitle: "Currency Converter - Convert World Currencies Online",
    metaDesc: "Convert currency exchange values between USD, EUR, INR, GBP, CAD, AUD, and JPY.",
    inputs: [
      { id: "curr_amount", label: "Amount", type: "number", default: 100 },
      { id: "curr_from", label: "From Currency", type: "select", options: ["USD", "EUR", "INR", "GBP", "CAD", "AUD"], default: "USD" },
      { id: "curr_to", label: "To Currency", type: "select", options: ["USD", "EUR", "INR", "GBP", "CAD", "AUD"], default: "INR" }
    ],
    formula: "Converted Amount = Amount × Exchange Rate",
    intro: "Convert money amounts between global currencies quickly using standard forex benchmark ratios.",
    howTo: ["Enter amount.", "Select source currency.", "Select target currency."],
    faqs: [{ q: "Are foreign exchange rates live?", a: "Rates are based on standard benchmark market rates." }]
  },
  {
    id: "tip-calculator",
    category: "finance",
    title: "Tip Calculator",
    subtitle: "Calculate tip amount, total bill, and split per person.",
    metaTitle: "Tip Calculator - Calculate Tip & Bill Split Per Person",
    metaDesc: "Calculate gratuity tips, total restaurant bill, and equal split amount per person.",
    inputs: [
      { id: "bill_total", label: "Bill Total ($)", type: "number", default: 85 },
      { id: "tip_pct", label: "Tip Percentage (%)", type: "number", default: 18 },
      { id: "split_people", label: "Number of People", type: "number", default: 4 }
    ],
    formula: "Tip = Bill × Tip%. Total = Bill + Tip. Per Person = Total / People",
    intro: "Calculate restaurant server tips and split dining bills evenly among friends.",
    howTo: ["Enter total bill.", "Select tip percentage.", "Enter number of people splitting."],
    faqs: [{ q: "What is standard tipping percentage in restaurants?", a: "15% to 20% is standard gratuity in North America and Western countries." }]
  },
  {
    id: "mortgage-calculator",
    category: "finance",
    title: "Mortgage Calculator",
    subtitle: "Calculate monthly mortgage payments, interest, and loan amortization.",
    metaTitle: "Mortgage Calculator - Calculate Monthly Home Payments",
    metaDesc: "Calculate estimated monthly mortgage payments including principal and interest for home buyers.",
    inputs: [
      { id: "home_price", label: "Home Purchase Price ($)", type: "number", default: 350000 },
      { id: "down_pay", label: "Down Payment ($)", type: "number", default: 70000 },
      { id: "mort_rate", label: "Interest Rate (%)", type: "number", default: 6.5 },
      { id: "mort_years", label: "Loan Term (Years)", type: "number", default: 30 }
    ],
    formula: "Loan = Home Price - Down Payment. Payment = Loan × r(1+r)^n / [(1+r)^n - 1]",
    intro: "Estimate your monthly mortgage payments and total interest cost when buying real estate.",
    howTo: ["Enter home purchase price.", "Enter down payment.", "Enter interest rate and loan term."],
    faqs: [{ q: "What is down payment percentage recommended?", a: "20% down payment is standard to avoid private mortgage insurance (PMI)." }]
  },
  {
    id: "savings-calculator",
    category: "finance",
    title: "Savings Calculator",
    subtitle: "Calculate how much your monthly savings will grow over time.",
    metaTitle: "Savings Goal Calculator - Future Value of Savings",
    metaDesc: "Calculate future accumulated savings value with regular monthly deposits and interest.",
    inputs: [
      { id: "sav_initial", label: "Initial Deposit", type: "number", default: 2000 },
      { id: "sav_monthly", label: "Monthly Addition", type: "number", default: 300 },
      { id: "sav_rate", label: "Annual Interest Rate (%)", type: "number", default: 5 },
      { id: "sav_years", label: "Time Horizon (Years)", type: "number", default: 10 }
    ],
    formula: "Future Savings = P(1+r)^t + PMT × [((1+r)^t - 1) / r]",
    intro: "Plan financial goals and see how regular monthly savings grow into substantial wealth.",
    howTo: ["Enter initial deposit.", "Enter monthly contributions.", "Enter interest rate and years."],
    faqs: [{ q: "How can I automate savings?", a: "Set up automatic recurring monthly bank transfers to a high-yield savings account on payday." }]
  },
  {
    id: "retirement-calculator",
    category: "finance",
    title: "Retirement Calculator",
    subtitle: "Calculate nest egg needed and monthly savings required for retirement.",
    metaTitle: "Retirement Calculator - Estimate Required Nest Egg",
    metaDesc: "Calculate total retirement corpus required and monthly savings needed for comfortable retirement.",
    inputs: [
      { id: "ret_age", label: "Current Age", type: "number", default: 30 },
      { id: "ret_retire_age", label: "Target Retirement Age", type: "number", default: 60 },
      { id: "ret_exp", label: "Desired Monthly Income at Retirement ($ / ₹)", type: "number", default: 4000 }
    ],
    formula: "Target Corpus = Annual Expenses × 25 (based on 4% safe withdrawal rule)",
    intro: "Calculate total retirement corpus target and required monthly savings to achieve financial independence.",
    howTo: ["Enter current age.", "Enter target retirement age.", "Enter desired monthly retirement income."],
    faqs: [{ q: "What is the 4% rule in retirement planning?", a: "The 4% rule suggests withdrawing 4% of your total retirement nest egg in year 1 to maintain sustainable cash flow." }]
  },

  // ==================== 4. DEVELOPER TOOLS (51-60) ====================
  {
    id: "password-generator",
    category: "developer",
    title: "Password Generator",
    subtitle: "Generate strong, secure, random passwords instantly.",
    metaTitle: "Random Password Generator - Create Secure Passwords",
    metaDesc: "Free online password generator. Create strong, secure, random passwords with customizable length and characters.",
    inputs: [
      { id: "pass_length", label: "Password Length", type: "number", default: 16 }
    ],
    formula: "Random character selection from uppercase, lowercase, numbers, and special symbols",
    intro: "Generate cryptographically strong passwords to protect your digital accounts from cyber threats.",
    howTo: ["Choose password length.", "Click Generate.", "Click Copy Result."],
    faqs: [{ q: "What makes a password strong?", a: "A strong password has 14+ characters, combining uppercase, lowercase, numbers, and symbols without dictionary words." }]
  },
  {
    id: "qr-generator",
    category: "developer",
    title: "QR Code Generator",
    subtitle: "Generate instant QR codes for URLs, text, and Wi-Fi networks.",
    metaTitle: "QR Code Generator - Create Free Custom QR Codes",
    metaDesc: "Generate free QR codes instantly for websites, text strings, emails, or links.",
    inputs: [
      { id: "qr_text", label: "Enter URL or Text", type: "text", default: "https://calculator-hub.com" }
    ],
    formula: "Generates high quality matrix barcode QR image canvas",
    intro: "Create scannable QR codes for web links, text notes, contact cards, or social media pages.",
    howTo: ["Type or paste your web link.", "Click Generate QR.", "Save or scan the image."],
    faqs: [{ q: "Do generated QR codes expire?", a: "No, static QR codes containing direct URLs never expire." }]
  },
  {
    id: "json-formatter",
    category: "developer",
    title: "JSON Formatter & Beautifier",
    subtitle: "Format, beautify, and validate JSON code data strings.",
    metaTitle: "JSON Formatter & Beautifier Online",
    metaDesc: "Beautify, format, clean, and validate JSON code with syntax highlighting and error checking.",
    inputs: [
      { id: "json_input", label: "Raw JSON Input", type: "textarea", default: '{"name":"Calculator Hub","tools":100,"active":true}' }
    ],
    formula: "JSON.stringify(JSON.parse(input), null, 2)",
    intro: "Format raw or minified JSON strings into clean, human-readable structured JSON trees.",
    howTo: ["Paste unformatted JSON.", "Click Format.", "Copy formatted JSON code."],
    faqs: [{ q: "What causes JSON parse errors?", a: "Unquoted keys, single quotes, trailing commas, or missing brackets break standard JSON format." }]
  },
  {
    id: "json-validator",
    category: "developer",
    title: "JSON Validator",
    subtitle: "Validate JSON syntax correctness and find line errors.",
    metaTitle: "JSON Validator - Check Valid JSON Syntax Online",
    metaDesc: "Check whether your JSON payload is valid syntax and pinpoint exact parsing error lines.",
    inputs: [
      { id: "json_val_input", label: "JSON to Validate", type: "textarea", default: '{\n  "status": "success",\n  "code": 200\n}' }
    ],
    formula: "Syntax validation via structural JSON parser",
    intro: "Check JSON code for syntax compliance, missing quotes, comma errors, or mismatched brackets.",
    howTo: ["Paste JSON string.", "Click Validate JSON."],
    faqs: [{ q: "Is single-quoted JSON valid?", a: "No, standard RFC 8259 JSON requires double quotes around keys and string values." }]
  },
  {
    id: "html-encoder",
    category: "developer",
    title: "HTML Encoder / Decoder",
    subtitle: "Escape or unescape special HTML entity characters.",
    metaTitle: "HTML Encoder Decoder - Escape Special HTML Characters",
    metaDesc: "Encode HTML special characters into HTML entities or decode entities back into plain text.",
    inputs: [
      { id: "html_text", label: "HTML Text", type: "textarea", default: '<div class="example">Hello & Welcome</div>' }
    ],
    formula: "Replaces <, >, &, \", ' with &lt;, &gt;, &amp;, &quot;, &#39;",
    intro: "Safely encode HTML code snippets for display on web pages without rendering raw tags.",
    howTo: ["Paste HTML code.", "Click Encode or Decode."],
    faqs: [{ q: "Why encode HTML characters?", a: "Encoding prevents Cross-Site Scripting (XSS) vulnerabilities and renders code tags safely." }]
  },
  {
    id: "url-encoder",
    category: "developer",
    title: "URL Encoder / Decoder",
    subtitle: "Encode characters into percent-encoded URL strings.",
    metaTitle: "URL Encoder Decoder - Percent Encode URLs Online",
    metaDesc: "Encode URL parameters into percent-encoded format or decode encoded URLs.",
    inputs: [
      { id: "url_text", label: "URL / String", type: "text", default: "https://calculator-hub.com/search?q=gpa calculator&ref=home" }
    ],
    formula: "encodeURIComponent(string) / decodeURIComponent(string)",
    intro: "Encode query string parameters and special characters into safe web URL formats.",
    howTo: ["Paste URL or parameter string.", "Click Encode or Decode."],
    faqs: [{ q: "Why are spaces converted to %20?", a: "URLs cannot contain literal whitespace; %20 is the URI percent encoding for spaces." }]
  },
  {
    id: "binary-converter",
    category: "developer",
    title: "Binary Converter",
    subtitle: "Convert text or decimal numbers to binary code and back.",
    metaTitle: "Binary Converter - Text/Decimal to Binary Code",
    metaDesc: "Convert ASCII text or decimal numbers into 8-bit binary code strings and vice versa.",
    inputs: [
      { id: "bin_input", label: "Text or Number Input", type: "text", default: "Hello" }
    ],
    formula: "Char to ASCII Byte -> Base-2 Binary String",
    intro: "Convert English text, characters, or numbers into binary (0s and 1s) representation.",
    howTo: ["Type text or number.", "Click Convert to Binary."],
    faqs: [{ q: "What is binary code?", a: "Binary is a base-2 numeral system representing data using only two digits: 0 and 1." }]
  },
  {
    id: "hex-converter",
    category: "developer",
    title: "Hex Converter",
    subtitle: "Convert text or numbers to Hexadecimal format.",
    metaTitle: "Hex Converter - Convert Text & Numbers to Hexadecimal",
    metaDesc: "Convert text, decimal numbers, or ASCII strings to hexadecimal values and back.",
    inputs: [
      { id: "hex_input", label: "Input Text or Decimal Number", type: "text", default: "Calculator" }
    ],
    formula: "Char / Number -> Base-16 Hexadecimal representation",
    intro: "Convert string characters or decimal integers into base-16 Hexadecimal format.",
    howTo: ["Type input text or number.", "Click Convert to Hex."],
    faqs: [{ q: "What characters are used in Hex?", a: "Hexadecimal uses digits 0-9 and letters A-F." }]
  },
  {
    id: "timestamp-converter",
    category: "developer",
    title: "Unix Timestamp Converter",
    subtitle: "Convert Unix Epoch timestamps to human readable dates.",
    metaTitle: "Unix Timestamp Converter - Epoch to Human Date",
    metaDesc: "Convert Unix Epoch timestamps (in seconds or milliseconds) to readable dates and vice versa.",
    inputs: [
      { id: "ts_val", label: "Unix Timestamp (seconds)", type: "number", default: 1770000000 }
    ],
    formula: "Date = new Date(timestamp × 1000)",
    intro: "Convert Unix timestamps to readable UTC/Local calendar dates and times.",
    howTo: ["Enter timestamp number.", "Click Convert to Date."],
    faqs: [{ q: "What is Unix Epoch timestamp?", a: "Unix timestamp measures the total number of seconds elapsed since January 1, 1970 (UTC)." }]
  },
  {
    id: "base-converter",
    category: "developer",
    title: "Number Base Converter",
    subtitle: "Convert numbers between Binary, Octal, Decimal, and Hexadecimal.",
    metaTitle: "Number Base Converter - Bin, Oct, Dec, Hex",
    metaDesc: "Convert numbers between Binary (Base-2), Octal (Base-8), Decimal (Base-10), and Hexadecimal (Base-16).",
    inputs: [
      { id: "base_num", label: "Number Value", type: "text", default: "255" },
      { id: "base_from", label: "From Base", type: "select", options: ["Decimal (10)", "Binary (2)", "Hexadecimal (16)", "Octal (8)"], default: "Decimal (10)" }
    ],
    formula: "parseInt(val, fromBase).toString(toBase)",
    intro: "Convert integer numbers between standard computer numeral base systems.",
    howTo: ["Enter number.", "Select source base system.", "Click Convert."],
    faqs: [{ q: "What is octal base system?", a: "Octal is a base-8 numbering system using digits 0 through 7." }]
  },

  // ==================== 5. MATH CALCULATORS (61-70) ====================
  {
    id: "scientific-calculator",
    category: "math",
    title: "Scientific Calculator",
    subtitle: "Perform advanced trigonometric, logarithmic, and power functions.",
    metaTitle: "Scientific Calculator - Advanced Online Math Calculator",
    metaDesc: "Free online scientific calculator. Supports sin, cos, tan, log, ln, square root, powers, and parentheses.",
    inputs: [
      { id: "sci_expr", label: "Math Expression", type: "text", default: "sin(45) + sqrt(144)" }
    ],
    formula: "Evaluates standard mathematical expression with JS Math functions",
    intro: "Perform complex scientific math calculations including trigonometry, logarithms, powers, and roots.",
    howTo: ["Enter math expression.", "Click Calculate."],
    faqs: [{ q: "Does trigonometric function use Radians or Degrees?", a: "Standard calculations use radians unless specified." }]
  },
  {
    id: "fraction-calculator",
    category: "math",
    title: "Fraction Calculator",
    subtitle: "Add, subtract, multiply, and divide fractions.",
    metaTitle: "Fraction Calculator - Add, Subtract, Multiply Fractions",
    metaDesc: "Perform arithmetic operations on fractions and simplify results to lowest terms.",
    inputs: [
      { id: "frac1_num", label: "Fraction 1 Numerator", type: "number", default: 3 },
      { id: "frac1_den", label: "Fraction 1 Denominator", type: "number", default: 4 },
      { id: "frac_op", label: "Operator", type: "select", options: ["+ (Add)", "- (Subtract)", "× (Multiply)", "÷ (Divide)"], default: "+ (Add)" },
      { id: "frac2_num", label: "Fraction 2 Numerator", type: "number", default: 1 },
      { id: "frac2_den", label: "Fraction 2 Denominator", type: "number", default: 2 }
    ],
    formula: "a/b + c/d = (ad + bc) / bd",
    intro: "Add, subtract, multiply, or divide two fractions and automatically simplify the resulting fraction.",
    howTo: ["Enter numerators and denominators.", "Select arithmetic operator.", "Click Calculate."],
    faqs: [{ q: "What is an improper fraction?", a: "An improper fraction has a numerator greater than or equal to its denominator." }]
  },
  {
    id: "lcm-calculator",
    category: "math",
    title: "LCM Calculator",
    subtitle: "Find the Least Common Multiple of two or more numbers.",
    metaTitle: "LCM Calculator - Find Least Common Multiple Online",
    metaDesc: "Calculate Least Common Multiple (LCM) of two or three numbers instantly.",
    inputs: [
      { id: "lcm_n1", label: "Number 1", type: "number", default: 12 },
      { id: "lcm_n2", label: "Number 2", type: "number", default: 18 }
    ],
    formula: "LCM(a,b) = (|a × b|) / HCF(a,b)",
    intro: "Calculate the smallest positive integer that is divisible by both given numbers.",
    howTo: ["Enter first number.", "Enter second number.", "Click Calculate."],
    faqs: [{ q: "What is LCM?", a: "LCM is the smallest number that is a multiple of two or more numbers." }]
  },
  {
    id: "hcf-calculator",
    category: "math",
    title: "HCF / GCD Calculator",
    subtitle: "Find the Highest Common Factor (GCD) of numbers.",
    metaTitle: "HCF Calculator - Highest Common Factor / GCD Online",
    metaDesc: "Calculate Highest Common Factor (HCF) and Greatest Common Divisor (GCD) using Euclidean algorithm.",
    inputs: [
      { id: "hcf_n1", label: "Number 1", type: "number", default: 24 },
      { id: "hcf_n2", label: "Number 2", type: "number", default: 36 }
    ],
    formula: "Euclidean algorithm: HCF(a,b) = HCF(b, a mod b)",
    intro: "Calculate the largest integer factor that divides two or more numbers without a remainder.",
    howTo: ["Enter first integer.", "Enter second integer.", "Click Calculate."],
    faqs: [{ q: "What is the difference between HCF and GCD?", a: "HCF (Highest Common Factor) and GCD (Greatest Common Divisor) are identical math concepts." }]
  },
  {
    id: "prime-number-checker",
    category: "math",
    title: "Prime Number Checker",
    subtitle: "Check if a number is prime and list all its factors.",
    metaTitle: "Prime Number Checker & Factor Finder",
    metaDesc: "Check if any integer is a prime number and view its complete list of factors.",
    inputs: [
      { id: "prime_num", label: "Enter Integer", type: "number", default: 97 }
    ],
    formula: "Checks divisibility up to square root of number",
    intro: "Determine if a number is a prime number (divisible only by 1 and itself) and view all factors.",
    howTo: ["Enter any positive integer.", "Click Check."],
    faqs: [{ q: "Is 1 a prime number?", a: "No, 1 is neither prime nor composite by mathematical definition." }]
  },
  {
    id: "percentage-difference-calculator",
    category: "math",
    title: "Percentage Difference Calculator",
    subtitle: "Calculate percentage difference between two positive numbers.",
    metaTitle: "Percentage Difference Calculator - Compare Two Numbers",
    metaDesc: "Calculate absolute percentage difference between two numerical values.",
    inputs: [
      { id: "pd_v1", label: "Value 1", type: "number", default: 100 },
      { id: "pd_v2", label: "Value 2", type: "number", default: 120 }
    ],
    formula: "% Difference = [ |V1 - V2| / ((V1 + V2) / 2) ] × 100",
    intro: "Calculate the relative percentage difference between two independent measurements.",
    howTo: ["Enter Value 1.", "Enter Value 2.", "Click Calculate."],
    faqs: [{ q: "How does percentage difference differ from percentage change?", a: "Percentage difference compares two numbers without specifying a direction or baseline." }]
  },
  {
    id: "area-calculator",
    category: "math",
    title: "Area Calculator",
    subtitle: "Calculate surface area of Circle, Rectangle, Triangle, and Square.",
    metaTitle: "Geometric Area Calculator - Shape Area Formulas",
    metaDesc: "Calculate surface area for geometric shapes: Circle, Rectangle, Triangle, and Trapezoid.",
    inputs: [
      { id: "shape_type", label: "Select Shape", type: "select", options: ["Circle", "Rectangle", "Triangle"], default: "Circle" },
      { id: "dim1", label: "Radius / Length / Base", type: "number", default: 10 },
      { id: "dim2", label: "Width / Height (if applicable)", type: "number", default: 5 }
    ],
    formula: "Circle: πr². Rectangle: L × W. Triangle: 0.5 × Base × Height",
    intro: "Calculate 2D geometric surface area for common shapes.",
    howTo: ["Select shape type.", "Enter dimensions.", "Click Calculate."],
    faqs: [{ q: "What are units for area?", a: "Area is measured in square units (e.g. m², cm², sq ft)." }]
  },
  {
    id: "volume-calculator",
    category: "math",
    title: "Volume Calculator",
    subtitle: "Calculate 3D volume for Sphere, Cylinder, Cube, and Rectangular Prism.",
    metaTitle: "Volume Calculator - 3D Shape Volume Formulas",
    metaDesc: "Calculate 3D volume for Sphere, Cylinder, Cube, Cone, and Rectangular Prism.",
    inputs: [
      { id: "vol_shape", label: "Select 3D Shape", type: "select", options: ["Sphere", "Cylinder", "Cube", "Rectangular Prism"], default: "Cylinder" },
      { id: "vol_dim1", label: "Radius / Side / Length", type: "number", default: 5 },
      { id: "vol_dim2", label: "Height / Width (if applicable)", type: "number", default: 10 },
      { id: "vol_dim3", label: "Depth / Height 2 (if applicable)", type: "number", default: 4 }
    ],
    formula: "Sphere: 4/3 π r³. Cylinder: π r² h. Cube: s³. Prism: L × W × H",
    intro: "Calculate total 3D cubic capacity and volume for geometric solids.",
    howTo: ["Select 3D solid shape.", "Enter dimensions.", "Click Calculate."],
    faqs: [{ q: "What is 1 liter in cubic centimeters?", a: "1 Liter equals exactly 1,000 cubic centimeters (cm³)." }]
  },
  {
    id: "triangle-calculator",
    category: "math",
    title: "Triangle Calculator",
    subtitle: "Calculate triangle perimeter, area, and angles.",
    metaTitle: "Triangle Calculator - Solve Sides, Angles & Area",
    metaDesc: "Calculate sides, angles, area, and perimeter of right-angled and scalene triangles.",
    inputs: [
      { id: "tri_side_a", label: "Side a", type: "number", default: 3 },
      { id: "tri_side_b", label: "Side b", type: "number", default: 4 },
      { id: "tri_side_c", label: "Side c", type: "number", default: 5 }
    ],
    formula: "Heron's Formula: Area = √(s(s-a)(s-b)(s-c)) where s = (a+b+c)/2",
    intro: "Solve triangle dimensions, perimeter, semi-perimeter, and interior area using side lengths.",
    howTo: ["Enter lengths for sides a, b, and c.", "Click Calculate."],
    faqs: [{ q: "What is Heron's formula?", a: "Heron's formula calculates triangle area directly from all three side lengths." }]
  },
  {
    id: "math-average-calculator",
    category: "math",
    title: "Math Average & Mean Calculator",
    subtitle: "Calculate mean, median, mode, and range of numbers.",
    metaTitle: "Math Average Calculator - Mean, Median, Mode, Range",
    metaDesc: "Calculate arithmetic mean, median, mode, range, and standard deviation for datasets.",
    inputs: [
      { id: "stat_nums", label: "Numbers (comma separated)", type: "text", default: "10, 20, 20, 30, 40, 50" }
    ],
    formula: "Mean = ∑X / N. Median = Middle value. Mode = Most frequent value",
    intro: "Compute fundamental statistical metrics (mean, median, mode, and range) for numerical datasets.",
    howTo: ["Enter numbers separated by commas.", "Click Calculate."],
    faqs: [{ q: "What is mode?", a: "Mode is the value that appears most frequently in a data set." }]
  },

  // ==================== 6. DAILY UTILITY TOOLS (71-80) ====================
  {
    id: "time-calculator",
    category: "daily-tools",
    title: "Time Calculator",
    subtitle: "Add or subtract hours, minutes, and seconds.",
    metaTitle: "Time Calculator - Add & Subtract Hours and Minutes",
    metaDesc: "Calculate total time duration by adding or subtracting hours, minutes, and seconds.",
    inputs: [
      { id: "time1", label: "Time 1 (HH:MM:SS)", type: "text", default: "02:45:30" },
      { id: "time_op", label: "Operation", type: "select", options: ["+ Add", "- Subtract"], default: "+ Add" },
      { id: "time2", label: "Time 2 (HH:MM:SS)", type: "text", default: "01:30:15" }
    ],
    formula: "Total Seconds = Time1 Seconds ± Time2 Seconds",
    intro: "Add or subtract multiple time durations easily for flight times, audio tracks, or work shifts.",
    howTo: ["Enter initial time duration.", "Select Add or Subtract.", "Enter second time duration."],
    faqs: [{ q: "How many seconds in an hour?", a: "There are 3,600 seconds in one hour." }]
  },
  {
    id: "age-difference-calculator",
    category: "daily-tools",
    title: "Age Difference Calculator",
    subtitle: "Calculate the exact age gap between two people.",
    metaTitle: "Age Difference Calculator - Find Age Gap",
    metaDesc: "Calculate the exact age difference in years, months, and days between two birth dates.",
    inputs: [
      { id: "person1_dob", label: "Person 1 Birth Date", type: "date", default: "1995-05-15" },
      { id: "person2_dob", label: "Person 2 Birth Date", type: "date", default: "1998-08-20" }
    ],
    formula: "Age Gap = Date 2 - Date 1",
    intro: "Calculate exact age difference between partners, siblings, or friends.",
    howTo: ["Select Person 1 birth date.", "Select Person 2 birth date.", "Click Calculate."],
    faqs: [{ q: "Does birth time matter for age gap?", a: "This calculator measures full calendar days between dates." }]
  },
  {
    id: "date-calculator",
    category: "daily-tools",
    title: "Date Addition / Subtraction Calculator",
    subtitle: "Add or subtract days, weeks, or months to a calendar date.",
    metaTitle: "Date Calculator - Add or Subtract Days from Date",
    metaDesc: "Calculate future or past calendar dates by adding or subtracting days, weeks, or months.",
    inputs: [
      { id: "base_date", label: "Starting Date", type: "date", default: "2026-07-30" },
      { id: "date_op", label: "Operation", type: "select", options: ["Add (+)", "Subtract (-)"], default: "Add (+)" },
      { id: "num_days", label: "Number of Days", type: "number", default: 45 }
    ],
    formula: "Result Date = Starting Date ± Number of Days",
    intro: "Find future deadline dates or past historical dates by adding or subtracting calendar days.",
    howTo: ["Select starting date.", "Select Add or Subtract.", "Enter number of days."],
    faqs: [{ q: "Does this handle month end boundaries?", a: "Yes, JS Date automatically handles leap years and variable month lengths." }]
  },
  {
    id: "unit-converter",
    category: "daily-tools",
    title: "Universal Unit Converter",
    subtitle: "Quickly convert values across measurement units.",
    metaTitle: "Universal Unit Converter Online",
    metaDesc: "Convert length, weight, speed, volume, and temperature units quickly.",
    inputs: [
      { id: "unit_val", label: "Value", type: "number", default: 100 },
      { id: "unit_from", label: "From Unit", type: "select", options: ["Meters", "Kilometers", "Miles", "Feet", "Inches"], default: "Kilometers" },
      { id: "unit_to", label: "To Unit", type: "select", options: ["Meters", "Kilometers", "Miles", "Feet", "Inches"], default: "Miles" }
    ],
    formula: "Converts value using metric / imperial unit scale factors",
    intro: "Convert units of length, distance, and measurement instantly.",
    howTo: ["Enter numeric value.", "Select source unit.", "Select target unit."],
    faqs: [{ q: "How many feet in a meter?", a: "1 meter equals approximately 3.28084 feet." }]
  },
  {
    id: "length-converter",
    category: "daily-tools",
    title: "Length Converter",
    subtitle: "Convert between meters, feet, inches, kilometers, and miles.",
    metaTitle: "Length Converter - Convert Distance & Length Units",
    metaDesc: "Convert length units: meters, km, cm, mm, feet, inches, yards, and miles.",
    inputs: [
      { id: "len_val", label: "Length", type: "number", default: 10 },
      { id: "len_from", label: "From", type: "select", options: ["Feet", "Meters", "Inches", "Centimeters", "Miles"], default: "Feet" },
      { id: "len_to", label: "To", type: "select", options: ["Feet", "Meters", "Inches", "Centimeters", "Miles"], default: "Meters" }
    ],
    formula: "1 Foot = 0.3048 Meters. 1 Inch = 2.54 Centimeters",
    intro: "Convert measurements between metric and imperial length units.",
    howTo: ["Enter length.", "Select input unit.", "Select output unit."],
    faqs: [{ q: "How many centimeters in an inch?", a: "1 inch is defined as exactly 2.54 centimeters." }]
  },
  {
    id: "weight-converter",
    category: "daily-tools",
    title: "Weight & Mass Converter",
    subtitle: "Convert kilograms, pounds, grams, ounces, and stones.",
    metaTitle: "Weight Converter - Convert Kg, Lbs, Oz, Grams",
    metaDesc: "Convert mass and weight units: Kilograms (kg), Pounds (lbs), Ounces (oz), and Grams (g).",
    inputs: [
      { id: "wt_val", label: "Weight", type: "number", default: 150 },
      { id: "wt_from", label: "From", type: "select", options: ["Pounds (lbs)", "Kilograms (kg)", "Grams (g)", "Ounces (oz)"], default: "Pounds (lbs)" },
      { id: "wt_to", label: "To", type: "select", options: ["Pounds (lbs)", "Kilograms (kg)", "Grams (g)", "Ounces (oz)"], default: "Kilograms (kg)" }
    ],
    formula: "1 kg = 2.20462 lbs. 1 lb = 16 oz",
    intro: "Convert body weight or recipe mass measurements between metric and imperial systems.",
    howTo: ["Enter weight.", "Select starting unit.", "Select target unit."],
    faqs: [{ q: "How many grams in a pound?", a: "1 pound equals approximately 453.592 grams." }]
  },
  {
    id: "temperature-converter",
    category: "daily-tools",
    title: "Temperature Converter",
    subtitle: "Convert Celsius, Fahrenheit, and Kelvin temperature scales.",
    metaTitle: "Temperature Converter - Celsius, Fahrenheit, Kelvin",
    metaDesc: "Convert temperatures between Celsius (°C), Fahrenheit (°F), and Kelvin (K).",
    inputs: [
      { id: "temp_val", label: "Temperature", type: "number", default: 37 },
      { id: "temp_from", label: "From", type: "select", options: ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"], default: "Celsius (°C)" },
      { id: "temp_to", label: "To", type: "select", options: ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"], default: "Fahrenheit (°F)" }
    ],
    formula: "°F = (°C × 9/5) + 32. °C = (°F - 32) × 5/9. K = °C + 273.15",
    intro: "Convert weather or scientific temperature readings between Celsius, Fahrenheit, and Kelvin.",
    howTo: ["Enter temperature value.", "Select starting scale.", "Select target scale."],
    faqs: [{ q: "At what temperature do °C and °F equal each other?", a: "-40° Celsius equals -40° Fahrenheit." }]
  },
  {
    id: "speed-converter",
    category: "daily-tools",
    title: "Speed Converter",
    subtitle: "Convert between km/h, mph, m/s, and knots.",
    metaTitle: "Speed Converter - Convert km/h, mph, knots",
    metaDesc: "Convert speed units: Kilometers per hour (km/h), Miles per hour (mph), Meters per second (m/s), and Knots.",
    inputs: [
      { id: "spd_val", label: "Speed", type: "number", default: 60 },
      { id: "spd_from", label: "From", type: "select", options: ["Miles per hour (mph)", "Kilometers per hour (km/h)", "Meters per second (m/s)", "Knots"], default: "Miles per hour (mph)" },
      { id: "spd_to", label: "To", type: "select", options: ["Miles per hour (mph)", "Kilometers per hour (km/h)", "Meters per second (m/s)", "Knots"], default: "Kilometers per hour (km/h)" }
    ],
    formula: "1 mph = 1.60934 km/h. 1 m/s = 3.6 km/h",
    intro: "Convert vehicle velocity or wind speeds between mph, km/h, m/s, and nautical knots.",
    howTo: ["Enter speed value.", "Select starting unit.", "Select ending unit."],
    faqs: [{ q: "What is a knot?", a: "A knot is a unit of speed equal to one nautical mile (1.852 km) per hour." }]
  },
  {
    id: "fuel-cost-calculator",
    category: "daily-tools",
    title: "Fuel Cost Calculator",
    subtitle: "Calculate trip fuel expense based on distance and fuel price.",
    metaTitle: "Fuel Cost Calculator - Calculate Trip Petrol / Diesel Cost",
    metaDesc: "Calculate total fuel required and trip cost based on mileage, distance, and fuel price per gallon/liter.",
    inputs: [
      { id: "fuel_dist", label: "Trip Distance (km / miles)", type: "number", default: 350 },
      { id: "fuel_eff", label: "Fuel Efficiency (km/L or MPG)", type: "number", default: 15 },
      { id: "fuel_price", label: "Fuel Price per Unit ($ / ₹)", type: "number", default: 1.5 }
    ],
    formula: "Fuel Needed = Distance / Efficiency. Total Cost = Fuel Needed × Price",
    intro: "Calculate exact fuel cost and liters/gallons required for road trips or daily commute.",
    howTo: ["Enter total trip distance.", "Enter vehicle mileage efficiency.", "Enter current fuel price."],
    faqs: [{ q: "How to improve vehicle fuel efficiency?", a: "Maintain proper tire inflation, avoid aggressive acceleration, and reduce extra cargo weight." }]
  },
  {
    id: "electricity-bill-calculator",
    category: "daily-tools",
    title: "Electricity Bill Calculator",
    subtitle: "Calculate appliance energy consumption and monthly electricity cost.",
    metaTitle: "Electricity Bill Calculator - Appliance kWh Power Cost",
    metaDesc: "Calculate power consumption in kWh and monthly electric utility bill for home appliances.",
    inputs: [
      { id: "elec_watt", label: "Appliance Power (Watts)", type: "number", default: 1500 },
      { id: "elec_hours", label: "Usage Hours Per Day", type: "number", default: 6 },
      { id: "elec_rate", label: "Cost Per kWh ($ / ₹)", type: "number", default: 0.15 }
    ],
    formula: "kWh per Month = (Watts × Hours × 30) / 1000. Total Cost = kWh × Rate",
    intro: "Calculate electricity power consumption and monthly utility bill costs for any home appliance.",
    howTo: ["Enter appliance wattage.", "Enter daily usage hours.", "Enter electricity cost per kWh."],
    faqs: [{ q: "What is a kWh?", a: "A kilowatt-hour (kWh) is a unit of energy equal to 1,000 watts used continuously for 1 hour." }]
  },

  // ==================== 7. FITNESS ADVANCED (81-90) ====================
  {
    id: "bmi-male-calculator",
    category: "fitness-advanced",
    title: "BMI Male Calculator",
    subtitle: "Male-tailored BMI calculator with muscle adjustment context.",
    metaTitle: "BMI Male Calculator - Calculate Body Mass Index for Men",
    metaDesc: "Male specific BMI calculator with weight categories and healthy weight range for men.",
    inputs: [
      { id: "bmim_w", label: "Weight (kg)", type: "number", default: 78 },
      { id: "bmim_h", label: "Height (cm)", type: "number", default: 178 }
    ],
    formula: "BMI = Weight (kg) / [Height (m)]²",
    intro: "Calculate Body Mass Index tailored with health advice specifically for men.",
    howTo: ["Enter weight in kg.", "Enter height in cm.", "Click Calculate."],
    faqs: [{ q: "What is normal BMI for men?", a: "A healthy adult male BMI ranges from 18.5 to 24.9." }]
  },
  {
    id: "bmi-female-calculator",
    category: "fitness-advanced",
    title: "BMI Female Calculator",
    subtitle: "Female-tailored BMI calculator with healthy weight guidance.",
    metaTitle: "BMI Female Calculator - Calculate Body Mass Index for Women",
    metaDesc: "Female specific BMI calculator with weight categories and healthy weight guidance for women.",
    inputs: [
      { id: "bmif_w", label: "Weight (kg)", type: "number", default: 62 },
      { id: "bmif_h", label: "Height (cm)", type: "number", default: 165 }
    ],
    formula: "BMI = Weight (kg) / [Height (m)]²",
    intro: "Calculate Body Mass Index with customized healthy range guidance for women.",
    howTo: ["Enter weight in kg.", "Enter height in cm.", "Click Calculate."],
    faqs: [{ q: "How does female body fat percentage affect health?", a: "Women naturally carry higher essential fat percentage (10-13%) than men (2-5%)." }]
  },
  {
    id: "calories-burned-calculator",
    category: "fitness-advanced",
    title: "Calories Burned Calculator",
    subtitle: "Calculate energy burned across different workout activities.",
    metaTitle: "Calories Burned Calculator - Workout & Activity Calories",
    metaDesc: "Calculate total calories burned during cycling, swimming, weightlifting, or sports.",
    inputs: [
      { id: "cb_weight", label: "Weight (kg)", type: "number", default: 70 },
      { id: "cb_activity", label: "Activity Type", type: "select", options: ["Weightlifting (MET 5.0)", "Cycling (MET 8.0)", "Swimming (MET 7.0)", "Basketball (MET 6.5)"], default: "Weightlifting (MET 5.0)" },
      { id: "cb_duration", label: "Duration (minutes)", type: "number", default: 45 }
    ],
    formula: "Calories Burned = (MET × 3.5 × Weight / 200) × Duration",
    intro: "Calculate total exercise calories burned based on exercise MET intensity values.",
    howTo: ["Enter body weight.", "Select exercise activity.", "Enter workout duration."],
    faqs: [{ q: "What is a MET score?", a: "MET (Metabolic Equivalent of Task) measures the energy expenditure rate of physical activities." }]
  },
  {
    id: "pushup-calories-calculator",
    category: "fitness-advanced",
    title: "Pushup Calories Calculator",
    subtitle: "Calculate calories burned doing pushups based on weight and reps.",
    metaTitle: "Pushup Calories Calculator - Calories Burned Doing Pushups",
    metaDesc: "Calculate calories burned doing pushup repetitions based on body weight and duration.",
    inputs: [
      { id: "push_weight", label: "Body Weight (kg)", type: "number", default: 72 },
      { id: "push_reps", label: "Total Pushup Reps", type: "number", default: 100 }
    ],
    formula: "Calories Burned ≈ Reps × 0.32 × (Body Weight / 70)",
    intro: "Calculate exact calories burned during calisthenics pushup sets.",
    howTo: ["Enter body weight.", "Enter pushup count.", "Click Calculate."],
    faqs: [{ q: "How many calories does 100 pushups burn?", a: "100 pushups burn roughly 30 to 45 calories depending on body weight and speed." }]
  },
  {
    id: "workout-calculator",
    category: "fitness-advanced",
    title: "Workout Calorie & Volume Calculator",
    subtitle: "Calculate total volume load lifted and total workout calories.",
    metaTitle: "Gym Workout Volume & Calorie Calculator",
    metaDesc: "Calculate total weight volume lifted (Sets × Reps × Weight) and total gym session calories.",
    inputs: [
      { id: "work_weight", label: "Weight Lifted (kg)", type: "number", default: 80 },
      { id: "work_reps", label: "Reps per Set", type: "number", default: 10 },
      { id: "work_sets", label: "Total Sets", type: "number", default: 4 }
    ],
    formula: "Total Volume = Weight × Reps × Sets",
    intro: "Calculate overall workout tonnage lifted and exercise intensity metrics.",
    howTo: ["Enter working weight.", "Enter reps per set.", "Enter sets performed."],
    faqs: [{ q: "Why track workout volume?", a: "Progressive overload in total workout volume drives long term muscle hypertrophy." }]
  },
  {
    id: "one-rep-max-calculator",
    category: "fitness-advanced",
    title: "One Rep Max (1RM) Calculator",
    subtitle: "Calculate maximum weight liftable for 1 repetition using Epley formula.",
    metaTitle: "One Rep Max Calculator (1RM) - Epley & Brzycki Formula",
    metaDesc: "Calculate your 1RM (One Rep Max) for bench press, squat, or deadlift safely.",
    inputs: [
      { id: "orm_weight", label: "Weight Lifted (kg)", type: "number", default: 100 },
      { id: "orm_reps", label: "Repetitions Performed (1-10)", type: "number", default: 5 }
    ],
    formula: "Epley 1RM = Weight × (1 + Reps / 30)",
    intro: "Calculate your max single repetition maximum lift safely without risk of injury.",
    howTo: ["Enter weight lifted.", "Enter completed reps.", "Click Calculate."],
    faqs: [{ q: "Is 1RM calculation accurate above 10 reps?", a: "1RM formulas are most accurate between 1 and 8 reps." }]
  },
  {
    id: "body-shape-calculator",
    category: "fitness-advanced",
    title: "Body Shape Calculator",
    subtitle: "Determine body shape (Hourglass, Pear, Apple, Rectangle).",
    metaTitle: "Body Shape Calculator - Find Female & Male Body Type",
    metaDesc: "Determine body shape classification (Hourglass, Pear, Apple, Rectangle) using body measurements.",
    inputs: [
      { id: "bs_bust", label: "Bust / Chest (cm)", type: "number", default: 90 },
      { id: "bs_waist", label: "Waist (cm)", type: "number", default: 70 },
      { id: "bs_hip", label: "Hips (cm)", type: "number", default: 95 }
    ],
    formula: "Evaluates ratios between bust, waist, and hip circumferences",
    intro: "Classify your body shape profile (Hourglass, Pear, Apple, or Rectangle) from tape measurements.",
    howTo: ["Measure and enter bust/chest size.", "Enter waist size.", "Enter hip size."],
    faqs: [{ q: "What defines an hourglass shape?", a: "Hourglass shape features bust and hip measurements of similar size with a significantly smaller waist." }]
  },
  {
    id: "water-weight-calculator",
    category: "fitness-advanced",
    title: "Water Weight Calculator",
    subtitle: "Estimate temporary water weight retention versus body fat.",
    metaTitle: "Water Weight Calculator - Estimate Fluid Retention",
    metaDesc: "Calculate estimated temporary water weight fluctuations due to sodium or carbohydrates.",
    inputs: [
      { id: "ww_weight", label: "Body Weight (kg)", type: "number", default: 75 },
      { id: "ww_sodium", label: "High Sodium / Carbs Intake?", type: "select", options: ["Normal", "High Sodium / Carb Feast"], default: "High Sodium / Carb Feast" }
    ],
    formula: "Water Retention Estimate ≈ Weight × 0.02 to 0.03",
    intro: "Estimate rapid scale weight fluctuations caused by water retention rather than fat gain.",
    howTo: ["Enter current weight.", "Select dietary sodium/carb intake level."],
    faqs: [{ q: "How to shed excess water weight quickly?", a: "Drink plenty of plain water, reduce sodium intake, and sweat through light cardio." }]
  },
  {
    id: "step-counter-calculator",
    category: "fitness-advanced",
    title: "Step Counter to Distance & Calories Calculator",
    subtitle: "Convert daily step count into kilometers, miles, and calories burned.",
    metaTitle: "Step Counter Calculator - Steps to Distance & Calories",
    metaDesc: "Convert daily step counts (e.g. 10,000 steps) into distance in km/miles and calories burned.",
    inputs: [
      { id: "steps_count", label: "Total Daily Steps", type: "number", default: 10000 },
      { id: "steps_weight", label: "Body Weight (kg)", type: "number", default: 70 }
    ],
    formula: "Distance (km) = Steps × 0.00078. Calories = Steps × 0.04 × (Weight / 70)",
    intro: "Convert your pedometer daily step count into walking distance and calories burned.",
    howTo: ["Enter your step count.", "Enter your body weight.", "Click Calculate."],
    faqs: [{ q: "How many km is 10,000 steps?", a: "10,000 steps equals roughly 7.5 to 8 kilometers for an average stride length." }]
  },
  {
    id: "walking-calories-calculator",
    category: "fitness-advanced",
    title: "Walking Calories Calculator",
    subtitle: "Calculate calories burned walking based on pace and body weight.",
    metaTitle: "Walking Calories Burned Calculator Online",
    metaDesc: "Calculate total calories burned walking based on distance, duration, speed, and body weight.",
    inputs: [
      { id: "walk_weight", label: "Weight (kg)", type: "number", default: 70 },
      { id: "walk_time", label: "Walking Duration (minutes)", type: "number", default: 60 },
      { id: "walk_pace", label: "Pace", type: "select", options: ["Slow (3 km/h)", "Moderate (5 km/h)", "Brisk (6.5 km/h)"], default: "Moderate (5 km/h)" }
    ],
    formula: "Calories = MET × Weight (kg) × Duration (hrs)",
    intro: "Calculate calories burned during daily walking exercise sessions.",
    howTo: ["Enter body weight.", "Enter walking time.", "Select walking pace."],
    faqs: [{ q: "Does brisk walking burn fat?", a: "Yes, brisk walking elevates heart rate into the optimal aerobic fat-burning zone." }]
  },

  // ==================== 8. EXTRA SEO TOOLS (91-100) ====================
  {
    id: "cgpa-to-percentage-converter",
    category: "seo-tools",
    title: "CGPA to Percentage (and Reverse) Converter",
    subtitle: "Convert CGPA to percentage score (8.4 to 10.0) and convert percentage back to CGPA.",
    metaTitle: "CGPA to Percentage & Reverse Converter Online (8.4 to 10.0 Scale)",
    metaDesc: "Accurately convert CGPA between 8.4 and 10.0 to percentage or percentage back to CGPA for CBSE, AICTE, VTU, Mumbai University, and GTU.",
    inputs: [
      { id: "c2p_mode", label: "Conversion Direction", type: "select", options: ["CGPA to Percentage", "Percentage to CGPA (Reverse)"], default: "CGPA to Percentage" },
      { id: "c2p_scale", label: "University / Board Formula Scale", type: "select", options: ["CBSE / Standard (CGPA × 9.5)", "AICTE / VTU / Mumbai Univ ((CGPA - 0.75) × 10)", "Direct Scale (CGPA × 10)", "Custom Factor"], default: "CBSE / Standard (CGPA × 9.5)" },
      { id: "c2p_val", label: "Enter CGPA or Percentage (e.g. 8.4, 8.6, 9.0, 9.5, 10.0)", type: "number", default: 8.5 },
      { id: "c2p_factor", label: "Custom Factor (if Custom selected)", type: "number", default: 9.5 }
    ],
    formula: "CBSE: % = CGPA × 9.5 | AICTE: % = (CGPA - 0.75) × 10 | Direct: % = CGPA × 10 | Reverse: CGPA = % ÷ 9.5 or (% ÷ 10) + 0.75",
    intro: "Accurately convert CGPA scores between 8.4 and 10.0 to percentage and vice-versa using CBSE, AICTE, VTU, or custom university formulas.",
    howTo: ["Select conversion direction (CGPA to % or Percentage to CGPA).", "Select your University/Board grading scale.", "Enter CGPA score (e.g. 8.4 to 10.0).", "Click Calculate to view exact percentage and grade breakdown."],
    faqs: [
      { q: "What is 8.4 CGPA in percentage?", a: "On CBSE scale (× 9.5): 8.4 × 9.5 = 79.80%. On AICTE scale ((CGPA - 0.75) × 10): (8.4 - 0.75) × 10 = 76.50%." },
      { q: "What is 9.0 CGPA in percentage?", a: "On CBSE scale: 9.0 × 9.5 = 85.50%. On AICTE scale: (9.0 - 0.75) × 10 = 82.50%." },
      { q: "What is 9.5 CGPA in percentage?", a: "On CBSE scale: 9.5 × 9.5 = 90.25%. On AICTE scale: (9.5 - 0.75) × 10 = 87.50%." },
      { q: "What is 10.0 CGPA in percentage?", a: "On CBSE scale: 10.0 × 9.5 = 95.00%. On Direct scale (× 10): 10.0 × 10 = 100.00%." }
    ]
  },
  {
    id: "percentage-to-cgpa-converter",
    category: "seo-tools",
    title: "Percentage to CGPA Converter",
    subtitle: "Convert marks percentage score back into CGPA on a 10.0 scale.",
    metaTitle: "Percentage to CGPA Converter Online",
    metaDesc: "Calculate CGPA from marks percentage score online using standard 9.5, AICTE, or 10.0 university factors.",
    inputs: [
      { id: "p2c_pct", label: "Percentage Score (%)", type: "number", default: 79.8 },
      { id: "p2c_scale", label: "University / Board Scale", type: "select", options: ["CBSE / Standard (CGPA = % ÷ 9.5)", "AICTE / VTU (CGPA = (% ÷ 10) + 0.75)", "Direct Scale (CGPA = % ÷ 10)"], default: "CBSE / Standard (CGPA = % ÷ 9.5)" }
    ],
    formula: "CBSE: CGPA = % ÷ 9.5 | AICTE: CGPA = (% ÷ 10) + 0.75 | Direct: CGPA = % ÷ 10",
    intro: "Convert overall marks percentage back to CGPA for university admissions and official applications.",
    howTo: ["Enter overall percentage score.", "Select university scale formula.", "Click Convert."],
    faqs: [{ q: "What CGPA is 80 percentage?", a: "CBSE scale: 80% ÷ 9.5 = 8.42 CGPA. AICTE scale: (80 ÷ 10) + 0.75 = 8.75 CGPA." }]
  },
  {
    id: "gpa-converter",
    category: "seo-tools",
    title: "GPA Converter (4.0 to 10.0 Scale)",
    subtitle: "Convert GPA between 4.0 US scale and 10.0 International scale.",
    metaTitle: "GPA Converter - Convert 4.0 to 10.0 GPA Scale",
    metaDesc: "Convert 4.0 US GPA scale to 10.0 scale, percentage, or European ECTS grade.",
    inputs: [
      { id: "gpa_val", label: "GPA Score", type: "number", default: 3.6 },
      { id: "gpa_scale_from", label: "From Scale", type: "select", options: ["4.0 Scale", "10.0 Scale"], default: "4.0 Scale" }
    ],
    formula: "10-Scale = (4-Scale / 4.0) × 10. Percentage = (4-Scale / 4.0) × 100",
    intro: "Convert academic GPA scores between 4.0 and 10.0 grading systems.",
    howTo: ["Enter GPA score.", "Select starting scale.", "Click Convert."],
    faqs: [{ q: "What is 3.5 GPA on a 10 point scale?", a: "A 3.5 GPA on a 4.0 scale is equivalent to approximately 8.75 on a 10.0 scale." }]
  },
  {
    id: "days-calculator",
    category: "seo-tools",
    title: "Days Left / Days Until Calculator",
    subtitle: "Calculate total days remaining until any target date.",
    metaTitle: "Days Until Calculator - Count Days Remaining",
    metaDesc: "Calculate total days, hours, and weekends remaining until any target event or holiday.",
    inputs: [
      { id: "days_target", label: "Target Date", type: "date", default: "2026-12-31" }
    ],
    formula: "Days Left = Target Date - Today",
    intro: "Calculate total days remaining until exams, holidays, new year, or project deadlines.",
    howTo: ["Select target date.", "Click Calculate."],
    faqs: [{ q: "Does this count weekend days?", a: "Yes, it counts total calendar days including weekends." }]
  },
  {
    id: "hours-calculator",
    category: "seo-tools",
    title: "Work Hours & Pay Calculator",
    subtitle: "Calculate total work hours and total pay with break deductions.",
    metaTitle: "Work Hours Calculator - Calculate Total Pay",
    metaDesc: "Calculate total shift work hours, unpaid break deductions, and total paycheck pay.",
    inputs: [
      { id: "hrs_start", label: "Start Time (HH:MM)", type: "text", default: "09:00" },
      { id: "hrs_end", label: "End Time (HH:MM)", type: "text", default: "17:30" },
      { id: "hrs_break", label: "Unpaid Break (minutes)", type: "number", default: 30 },
      { id: "hrs_wage", label: "Hourly Wage ($ / ₹)", type: "number", default: 20 }
    ],
    formula: "Net Hours = (End Time - Start Time) - Break. Total Pay = Net Hours × Hourly Wage",
    intro: "Calculate daily work shift hours, deduct lunch breaks, and compute gross earnings.",
    howTo: ["Enter start time.", "Enter end time.", "Enter break minutes and hourly rate."],
    faqs: [{ q: "How to handle overnight shifts?", a: "Add 24 hours to end time if the shift crosses past midnight." }]
  },
  {
    id: "minutes-calculator",
    category: "seo-tools",
    title: "Minutes to Hours & Minutes Converter",
    subtitle: "Convert total minutes into formatted hours and minutes.",
    metaTitle: "Minutes to Hours Converter - Total Minutes Format",
    metaDesc: "Convert total minutes into formatted hours, minutes, and days easily.",
    inputs: [
      { id: "min_input", label: "Total Minutes", type: "number", default: 485 }
    ],
    formula: "Hours = Math.floor(Minutes / 60). Remaining Minutes = Minutes % 60",
    intro: "Convert large minute totals into readable hours and remaining minutes.",
    howTo: ["Enter number of minutes.", "Click Convert."],
    faqs: [{ q: "How many minutes in 1 day?", a: "There are 1,440 minutes in a full 24-hour day." }]
  },
  {
    id: "random-number-generator",
    category: "seo-tools",
    title: "Random Number Generator",
    subtitle: "Generate random numbers within specified minimum and maximum bounds.",
    metaTitle: "Random Number Generator - Generate Random Numbers Online",
    metaDesc: "Generate random numbers within custom min and max range bounds.",
    inputs: [
      { id: "rng_min", label: "Minimum Value", type: "number", default: 1 },
      { id: "rng_max", label: "Maximum Value", type: "number", default: 100 },
      { id: "rng_count", label: "Quantity of Numbers", type: "number", default: 5 }
    ],
    formula: "Math.floor(Math.random() × (max - min + 1)) + min",
    intro: "Generate unbiased random integers for raffles, games, statistics, or sampling.",
    howTo: ["Enter minimum bound.", "Enter maximum bound.", "Enter quantity.", "Click Generate."],
    faqs: [{ q: "Are these numbers truly random?", a: "They are generated using high quality pseudo-random number algorithms (PRNG)." }]
  },
  {
    id: "password-strength-checker",
    category: "seo-tools",
    title: "Password Strength Checker",
    subtitle: "Test password entropy strength and estimated crack time.",
    metaTitle: "Password Strength Checker - Test Security & Crack Time",
    metaDesc: "Check password strength, security score, entropy bits, and estimated brute-force crack time.",
    inputs: [
      { id: "chk_pass", label: "Enter Password to Test", type: "text", default: "P@ssw0rd2026!" }
    ],
    formula: "Entropy Bits = Length × log2(Character Pool Size)",
    intro: "Test the cryptographic strength of your passwords and calculate estimated cracking resistance.",
    howTo: ["Type a password into the test box.", "View security score instantly."],
    faqs: [{ q: "Is it safe to type my password here?", a: "Yes! All calculations run 100% locally inside your browser; nothing is sent over the internet." }]
  },
  {
    id: "character-counter",
    category: "seo-tools",
    title: "Character Counter",
    subtitle: "Count characters, letters, numbers, and symbols in real-time.",
    metaTitle: "Character Counter - Count Characters with & without Spaces",
    metaDesc: "Free character counter tool. Count total characters, spaces, letters, and numbers in text.",
    inputs: [
      { id: "cc_text", label: "Type or Paste Text", type: "textarea", default: "Calculator Hub provides 100+ free online calculators." }
    ],
    formula: "Counts string length, non-space characters, and letter/number breakdown",
    intro: "Count total characters with and without spaces for social media posts (X/Twitter, LinkedIn, Meta).",
    howTo: ["Paste your text snippet.", "View instant character metrics."],
    faqs: [{ q: "What is Twitter character limit?", a: "X (Twitter) allows 280 characters per standard post." }]
  },
  {
    id: "word-counter",
    category: "seo-tools",
    title: "Word Counter",
    subtitle: "Count words, sentences, paragraphs, and estimated reading time.",
    metaTitle: "Word Counter - Count Words, Sentences & Reading Time",
    metaDesc: "Count words, characters, sentences, paragraphs, reading time, and speaking time online.",
    inputs: [
      { id: "wc_text", label: "Type or Paste Article Text", type: "textarea", default: "Online calculators make complex mathematical, financial, and fitness calculations fast and simple for students and professionals worldwide." }
    ],
    formula: "Words = Text.trim().split(/\\s+/). Reading Time = Words / 200 min",
    intro: "Count words, sentences, paragraphs, and reading duration for essays and articles.",
    howTo: ["Paste text into the box.", "View word count and reading time metrics."],
    faqs: [{ q: "What is average reading speed?", a: "An average adult reads approximately 200 to 250 words per minute." }]
  },
  {
    id: "text-case-converter",
    category: "seo-tools",
    title: "Text Case Converter",
    subtitle: "Convert text to UPPERCASE, lowercase, Title Case, camelCase, snake_case.",
    metaTitle: "Text Case Converter - UPPERCASE, lowercase, Title Case",
    metaDesc: "Convert text to UPPERCASE, lowercase, Title Case, Sentence case, camelCase, and snake_case.",
    inputs: [
      { id: "tcc_text", label: "Input Text", type: "textarea", default: "calculator hub online tools" }
    ],
    formula: "Applies string formatting transformations across text cases",
    intro: "Transform text casing between uppercase, lowercase, title case, camelCase, and snake_case.",
    howTo: ["Paste text string.", "Select desired text case format."],
    faqs: [{ q: "What is camelCase used for?", a: "camelCase is a programming naming convention where word boundaries are capitalized without spaces." }]
  }
];

// Helper functions for database lookups
function getCalculatorById(id) {
  return CALCULATORS_DB.find(calc => calc.id === id);
}

function getCalculatorsByCategory(catId) {
  return CALCULATORS_DB.filter(calc => calc.category === catId);
}

function searchCalculators(query) {
  if (!query || query.trim() === "") return [];
  const q = query.toLowerCase().trim();
  return CALCULATORS_DB.filter(calc => 
    calc.title.toLowerCase().includes(q) || 
    calc.subtitle.toLowerCase().includes(q) || 
    calc.category.toLowerCase().includes(q) ||
    (calc.metaDesc && calc.metaDesc.toLowerCase().includes(q))
  );
}

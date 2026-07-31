/**
 * CALCULATOR ENGINE MODULE
 * Implements math calculation logic for all 100 tools.
 */

const CalculatorEngine = {
  calculate: function(id, inputs) {
    try {
      switch (id) {
        // ==================== 1. EDUCATION ====================
        case "cgpa-calculator": {
          const arr = inputs.gpas.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          if (!arr.length) return { error: "Please enter valid semester GPAs separated by commas." };
          const sum = arr.reduce((a, b) => a + b, 0);
          const cgpa = sum / arr.length;
          const pct = cgpa * 9.5;
          return {
            value: cgpa.toFixed(2),
            explanation: `Based on ${arr.length} semester(s), your overall CGPA is ${cgpa.toFixed(2)}. Equivalent Percentage: ~${pct.toFixed(2)}%.`
          };
        }
        case "gpa-calculator": {
          const gArr = inputs.grades.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          const cArr = inputs.credits.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          if (!gArr.length || gArr.length !== cArr.length) return { error: "Grades and credits count must match." };
          let totalPoints = 0, totalCredits = 0;
          for (let i = 0; i < gArr.length; i++) {
            totalPoints += gArr[i] * cArr[i];
            totalCredits += cArr[i];
          }
          const gpa = totalPoints / totalCredits;
          return {
            value: gpa.toFixed(2),
            explanation: `Total Points: ${totalPoints.toFixed(1)}, Total Credits: ${totalCredits}. Semester GPA: ${gpa.toFixed(2)}.`
          };
        }
        case "percentage-calculator": {
          const x = parseFloat(inputs.value), y = parseFloat(inputs.total);
          if (isNaN(x) || isNaN(y)) return { error: "Invalid numbers entered." };
          const res = (x / 100) * y;
          return {
            value: res.toLocaleString('en-US', { maximumFractionDigits: 4 }),
            explanation: `${x}% of ${y} is equal to ${res}.`
          };
        }
        case "marks-calculator": {
          const ob = parseFloat(inputs.obtained), tot = parseFloat(inputs.total);
          if (isNaN(ob) || isNaN(tot) || tot <= 0) return { error: "Invalid marks entered." };
          const pct = (ob / tot) * 100;
          return {
            value: `${pct.toFixed(2)}%`,
            explanation: `You obtained ${ob} out of ${tot} marks (${pct.toFixed(2)}%).`
          };
        }
        case "attendance-calculator": {
          const att = parseInt(inputs.attended), tot = parseInt(inputs.total), tgt = parseFloat(inputs.target);
          if (isNaN(att) || isNaN(tot) || tot <= 0 || att > tot) return { error: "Invalid attendance numbers." };
          const curPct = (att / tot) * 100;
          let msg = `Current Attendance: ${curPct.toFixed(2)}%. `;
          if (curPct >= tgt) {
            const margin = Math.floor((att - (tgt / 100 * tot)) / (tgt / 100));
            msg += `Great! You are above your target of ${tgt}%. You can safely miss up to ${Math.max(0, margin)} upcoming classes.`;
          } else {
            const needed = Math.ceil((tgt / 100 * tot - att) / (1 - tgt / 100));
            msg += `Warning! You need to attend the next ${Math.max(1, needed)} consecutive classes to reach ${tgt}%.`;
          }
          return { value: `${curPct.toFixed(2)}%`, explanation: msg };
        }
        case "sgpa-calculator": {
          const g = inputs.sgpa_points.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          const c = inputs.sgpa_credits.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          if (!g.length || g.length !== c.length) return { error: "Grades and credits count must match." };
          let pts = 0, crs = 0;
          for (let i = 0; i < g.length; i++) { pts += g[i] * c[i]; crs += c[i]; }
          const sgpa = pts / crs;
          return { value: sgpa.toFixed(2), explanation: `SGPA for the semester is ${sgpa.toFixed(2)} (Total Credits: ${crs}).` };
        }
        case "grade-calculator": {
          const cur = parseFloat(inputs.current_grade), tgt = parseFloat(inputs.target_grade), w = parseFloat(inputs.final_weight);
          if (isNaN(cur) || isNaN(tgt) || isNaN(w) || w <= 0 || w > 100) return { error: "Invalid inputs." };
          const req = (tgt - (cur * (1 - w / 100))) / (w / 100);
          return {
            value: `${req.toFixed(2)}%`,
            explanation: `To achieve an overall course grade of ${tgt}%, you must score at least ${req.toFixed(2)}% on your final exam.`
          };
        }
        case "study-time-calculator": {
          const crd = parseFloat(inputs.credits_total), diff = parseFloat(inputs.difficulty);
          if (isNaN(crd) || isNaN(diff)) return { error: "Invalid credit inputs." };
          const hrsPerWk = crd * (diff + 1);
          const hrsPerDay = hrsPerWk / 7;
          return {
            value: `${hrsPerWk.toFixed(1)} hrs/week`,
            explanation: `We recommend studying ~${hrsPerWk.toFixed(1)} hours per week (~${hrsPerDay.toFixed(1)} hours per day) for optimal subject mastery.`
          };
        }
        case "exam-score-calculator": {
          const s = inputs.scores.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          const w = inputs.weights.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          if (!s.length || s.length !== w.length) return { error: "Scores and weights count must match." };
          let totalW = 0, scoreSum = 0;
          for (let i = 0; i < s.length; i++) { scoreSum += s[i] * (w[i] / 100); totalW += w[i]; }
          return { value: `${scoreSum.toFixed(2)}%`, explanation: `Overall weighted grade: ${scoreSum.toFixed(2)}% (Total weight: ${totalW}%).` };
        }
        case "rank-predictor": {
          const raw = parseFloat(inputs.raw_score), max = parseFloat(inputs.max_score), cand = parseInt(inputs.total_candidates);
          if (isNaN(raw) || isNaN(max) || max <= 0 || isNaN(cand)) return { error: "Invalid numbers." };
          const ratio = Math.min(1, Math.max(0, raw / max));
          const percentile = Math.pow(ratio, 0.85) * 100;
          const estRank = Math.max(1, Math.round(cand * (1 - percentile / 100)));
          return {
            value: `~Rank ${estRank.toLocaleString()}`,
            explanation: `Estimated Percentile: ${percentile.toFixed(2)}th percentile among ${cand.toLocaleString()} candidates.`
          };
        }
        case "age-calculator": {
          if (!inputs.dob) return { error: "Please select your date of birth." };
          const birth = new Date(inputs.dob);
          const now = new Date();
          if (birth > now) return { error: "Birth date cannot be in the future." };
          let years = now.getFullYear() - birth.getFullYear();
          let months = now.getMonth() - birth.getMonth();
          let days = now.getDate() - birth.getDate();
          if (days < 0) { months--; days += new Date(now.getFullYear(), now.getMonth(), 0).getDate(); }
          if (months < 0) { years--; months += 12; }
          const diffMs = now - birth;
          const totalDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
          return {
            value: `${years} Years, ${months} Months, ${days} Days`,
            explanation: `Total Lifespan: ${totalDays.toLocaleString()} days (${(totalDays * 24).toLocaleString()} hours).`
          };
        }
        case "date-difference-calculator": {
          if (!inputs.date1 || !inputs.date2) return { error: "Please select start and end dates." };
          const d1 = new Date(inputs.date1), d2 = new Date(inputs.date2);
          const diffTime = Math.abs(d2 - d1);
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
          const weeks = (diffDays / 7).toFixed(1);
          return { value: `${diffDays} Days`, explanation: `Difference between dates: ${diffDays} days (${weeks} weeks).` };
        }
        case "semester-calculator": {
          const arr = inputs.sem_scores.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          if (!arr.length) return { error: "Enter valid semester scores." };
          const avg = arr.reduce((a,b) => a+b, 0) / arr.length;
          return { value: avg.toFixed(2), explanation: `Average across ${arr.length} semesters is ${avg.toFixed(2)}.` };
        }
        case "credit-calculator": {
          const comp = parseFloat(inputs.completed_credits), req = parseFloat(inputs.total_required);
          if (isNaN(comp) || isNaN(req) || req <= 0) return { error: "Invalid credit inputs." };
          const rem = Math.max(0, req - comp);
          const pct = (comp / req) * 100;
          return { value: `${rem} Credits Left`, explanation: `Degree Completion Progress: ${pct.toFixed(1)}%. Completed ${comp} of ${req} credits.` };
        }
        case "average-calculator": {
          const arr = inputs.num_list.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          if (!arr.length) return { error: "Enter valid numbers." };
          const sum = arr.reduce((a,b) => a+b, 0);
          const avg = sum / arr.length;
          return { value: avg.toFixed(2), explanation: `Count: ${arr.length}, Sum: ${sum}, Mean Average: ${avg.toFixed(2)}.` };
        }

        // ==================== 2. HEALTH & FITNESS ====================
        case "bmi-calculator":
        case "bmi-male-calculator":
        case "bmi-female-calculator": {
          const w = parseFloat(inputs.weight || inputs.bmim_w || inputs.bmif_w);
          const h = parseFloat(inputs.height || inputs.bmim_h || inputs.bmif_h);
          if (isNaN(w) || isNaN(h) || h <= 0) return { error: "Please enter valid weight and height." };
          const hm = h / 100;
          const bmi = w / (hm * hm);
          let status = "";
          if (bmi < 18.5) status = "Underweight";
          else if (bmi < 25) status = "Normal weight (Healthy)";
          else if (bmi < 30) status = "Overweight";
          else status = "Obese";
          return { value: bmi.toFixed(1), explanation: `Your BMI is ${bmi.toFixed(1)} kg/m², which falls into the '${status}' range.` };
        }
        case "bmr-calculator": {
          const w = parseFloat(inputs.bmr_weight), h = parseFloat(inputs.bmr_height), a = parseFloat(inputs.bmr_age);
          const g = inputs.bmr_gender;
          if (isNaN(w) || isNaN(h) || isNaN(a)) return { error: "Invalid inputs." };
          let bmr = 10 * w + 6.25 * h - 5 * a;
          bmr += (g === "Male") ? 5 : -161;
          return { value: `${Math.round(bmr)} kcal/day`, explanation: `Your Basal Metabolic Rate (BMR) is ${Math.round(bmr)} kcal/day.` };
        }
        case "calorie-calculator": {
          const bmr = parseFloat(inputs.cal_bmr);
          if (isNaN(bmr)) return { error: "Invalid BMR." };
          let mult = 1.2;
          if (inputs.activity.includes("Light")) mult = 1.375;
          else if (inputs.activity.includes("Moderate")) mult = 1.55;
          else if (inputs.activity.includes("Heavy")) mult = 1.725;
          const tdee = Math.round(bmr * mult);
          return {
            value: `${tdee} kcal/day`,
            explanation: `Maintenance TDEE: ${tdee} kcal/day. For weight loss: ~${tdee - 500} kcal/day. For muscle gain: ~${tdee + 300} kcal/day.`
          };
        }
        case "protein-calculator": {
          const w = parseFloat(inputs.prot_weight);
          if (isNaN(w)) return { error: "Invalid weight." };
          let mult = 1.6;
          if (inputs.prot_goal.includes("Muscle")) mult = 2.0;
          else if (inputs.prot_goal.includes("Cutting")) mult = 2.2;
          const grams = Math.round(w * mult);
          return { value: `${grams} grams/day`, explanation: `Recommended daily protein intake: ${grams}g (~${(grams*4)} kcal).` };
        }
        case "water-intake-calculator": {
          const w = parseFloat(inputs.water_weight), ex = parseFloat(inputs.exercise_min) || 0;
          if (isNaN(w)) return { error: "Invalid weight." };
          const liters = (w * 0.033) + ((ex / 30) * 0.35);
          const glasses = Math.round(liters / 0.25);
          return { value: `${liters.toFixed(1)} Liters/day`, explanation: `Recommended water intake: ~${liters.toFixed(1)} Liters (${glasses} glasses per day).` };
        }
        case "ideal-weight-calculator": {
          const h = parseFloat(inputs.ibw_height), g = inputs.ibw_gender;
          if (isNaN(h)) return { error: "Invalid height." };
          const inchesOver5ft = Math.max(0, (h / 2.54) - 60);
          const devine = (g === "Male") ? 50 + (2.3 * inchesOver5ft) : 45.5 + (2.3 * inchesOver5ft);
          return { value: `${devine.toFixed(1)} kg`, explanation: `Ideal Body Weight (Devine Formula): ~${devine.toFixed(1)} kg (${(devine * 2.20462).toFixed(1)} lbs).` };
        }
        case "body-fat-calculator": {
          const w = parseFloat(inputs.bf_waist), n = parseFloat(inputs.bf_neck), h = parseFloat(inputs.bf_height), g = inputs.bf_gender;
          if (isNaN(w) || isNaN(n) || isNaN(h)) return { error: "Invalid body measurements." };
          let bf = 0;
          if (g === "Male") {
            bf = 86.010 * Math.log10(w - n) - 70.041 * Math.log10(h) + 36.76;
          } else {
            bf = 163.205 * Math.log10(w + n) - 97.684 * Math.log10(h) - 78.387;
          }
          bf = Math.max(3, Math.min(60, bf));
          return { value: `${bf.toFixed(1)}% Body Fat`, explanation: `Estimated body fat percentage using US Navy Method: ${bf.toFixed(1)}%.` };
        }
        case "macro-calculator": {
          const tdee = parseFloat(inputs.macro_tdee);
          if (isNaN(tdee)) return { error: "Invalid calorie target." };
          let cPct = 0.5, pPct = 0.3, fPct = 0.2;
          if (inputs.macro_split.includes("High Protein")) { cPct = 0.4; pPct = 0.4; fPct = 0.2; }
          else if (inputs.macro_split.includes("Keto")) { cPct = 0.05; pPct = 0.3; fPct = 0.65; }
          const cG = Math.round((tdee * cPct) / 4);
          const pG = Math.round((tdee * pPct) / 4);
          const fG = Math.round((tdee * fPct) / 9);
          return { value: `${cG}g Carbs / ${pG}g Protein / ${fG}g Fat`, explanation: `Daily macro breakdown: Carbs: ${cG}g, Protein: ${pG}g, Fat: ${fG}g.` };
        }
        case "running-calories-calculator": {
          const w = parseFloat(inputs.run_weight), d = parseFloat(inputs.run_dist), t = parseFloat(inputs.run_time);
          if (isNaN(w) || isNaN(d) || isNaN(t)) return { error: "Invalid running inputs." };
          const spd = d / (t / 60);
          let met = 8.0;
          if (spd > 12) met = 11.5;
          else if (spd > 10) met = 10.0;
          const cal = (met * 3.5 * w / 200) * t;
          return { value: `${Math.round(cal)} kcal`, explanation: `Running ${d} km in ${t} mins (${spd.toFixed(1)} km/h) burned ~${Math.round(cal)} kcal.` };
        }
        case "sleep-calculator": {
          const timeStr = inputs.wake_time || "07:00";
          const [h, m] = timeStr.split(":").map(Number);
          const wakeDate = new Date();
          wakeDate.setHours(h, m, 0, 0);
          const bedTimes = [];
          for (let cycles = 6; cycles >= 4; cycles--) {
            const bed = new Date(wakeDate.getTime() - (cycles * 90 * 60 * 1000 + 15 * 60 * 1000));
            const str = bed.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            bedTimes.push(`${str} (${cycles} cycles)`);
          }
          return { value: bedTimes.join(" OR "), explanation: `To wake up refreshed at ${timeStr}, go to sleep at one of these recommended times.` };
        }
        case "waist-height-ratio-calculator": {
          const w = parseFloat(inputs.whtr_waist), h = parseFloat(inputs.whtr_height);
          if (isNaN(w) || isNaN(h)) return { error: "Invalid inputs." };
          const ratio = w / h;
          let status = ratio < 0.5 ? "Healthy (Low Risk)" : "Increased Risk (High abdominal fat)";
          return { value: ratio.toFixed(2), explanation: `Waist-to-Height Ratio: ${ratio.toFixed(2)} (${status}).` };
        }
        case "lean-body-mass-calculator": {
          const w = parseFloat(inputs.lbm_weight), h = parseFloat(inputs.lbm_height), g = inputs.lbm_gender;
          if (isNaN(w) || isNaN(h)) return { error: "Invalid inputs." };
          const lbm = (g === "Male") ? (0.407 * w) + (0.267 * h) - 19.2 : (0.252 * w) + (0.473 * h) - 48.3;
          return { value: `${lbm.toFixed(1)} kg`, explanation: `Estimated Lean Body Mass (Boer Formula): ${lbm.toFixed(1)} kg.` };
        }
        case "weight-loss-calculator": {
          const cur = parseFloat(inputs.current_w), tgt = parseFloat(inputs.target_w), def = parseFloat(inputs.deficit);
          if (isNaN(cur) || isNaN(tgt) || isNaN(def) || def <= 0) return { error: "Invalid inputs." };
          const diffKg = cur - tgt;
          if (diffKg <= 0) return { error: "Current weight must be greater than target weight." };
          const days = Math.ceil((diffKg * 7700) / def);
          const weeks = (days / 7).toFixed(1);
          return { value: `${weeks} Weeks`, explanation: `To lose ${diffKg.toFixed(1)} kg at a ${def} kcal/day deficit will take ~${days} days (${weeks} weeks).` };
        }
        case "heart-rate-calculator": {
          const age = parseFloat(inputs.hr_age), rest = parseFloat(inputs.hr_rest) || 60;
          if (isNaN(age)) return { error: "Invalid age." };
          const maxHr = 220 - age;
          const fatBurnMin = Math.round(((maxHr - rest) * 0.6) + rest);
          const fatBurnMax = Math.round(((maxHr - rest) * 0.7) + rest);
          return { value: `${maxHr} bpm (Max HR)`, explanation: `Fat Burn Zone: ${fatBurnMin} - ${fatBurnMax} bpm. Aerobic Zone: ${Math.round(((maxHr-rest)*0.7)+rest)} - ${Math.round(((maxHr-rest)*0.85)+rest)} bpm.` };
        }
        case "pregnancy-due-date-calculator": {
          if (!inputs.lmp_date) return { error: "Select last menstrual period date." };
          const lmp = new Date(inputs.lmp_date);
          const edd = new Date(lmp.getTime() + 280 * 24 * 60 * 60 * 1000);
          return { value: edd.toDateString(), explanation: `Estimated Due Date (EDD): ${edd.toDateString()} (40 weeks from LMP).` };
        }

        // ==================== 3. FINANCE ====================
        case "emi-calculator": {
          const p = parseFloat(inputs.emi_principal), rYr = parseFloat(inputs.emi_rate), tYr = parseFloat(inputs.emi_tenure);
          if (isNaN(p) || isNaN(rYr) || isNaN(tYr) || p <= 0) return { error: "Invalid EMI parameters." };
          const r = (rYr / 12) / 100;
          const n = tYr * 12;
          const emi = (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
          const totalPay = emi * n;
          const totalInt = totalPay - p;
          return {
            value: `$${emi.toFixed(2)} / month`,
            explanation: `Monthly EMI: $${emi.toFixed(2)}. Total Payable: $${totalPay.toFixed(2)} (Principal: $${p}, Interest: $${totalInt.toFixed(2)}).`
          };
        }
        case "loan-calculator": {
          const p = parseFloat(inputs.loan_p), rYr = parseFloat(inputs.loan_r), m = parseFloat(inputs.loan_months);
          if (isNaN(p) || isNaN(rYr) || isNaN(m)) return { error: "Invalid loan inputs." };
          const r = (rYr / 12) / 100;
          const pay = (p * r) / (1 - Math.pow(1 + r, -m));
          const tot = pay * m;
          return { value: `$${pay.toFixed(2)} / month`, explanation: `Monthly payment: $${pay.toFixed(2)}. Total repayment over ${m} months: $${tot.toFixed(2)}.` };
        }
        case "sip-calculator": {
          const p = parseFloat(inputs.sip_monthly), rYr = parseFloat(inputs.sip_rate), y = parseFloat(inputs.sip_years);
          if (isNaN(p) || isNaN(rYr) || isNaN(y)) return { error: "Invalid SIP inputs." };
          const i = (rYr / 12) / 100;
          const n = y * 12;
          const futureVal = p * ((Math.pow(1 + i, n) - 1) / i) * (1 + i);
          const invested = p * n;
          const wealthGain = futureVal - invested;
          return {
            value: `$${Math.round(futureVal).toLocaleString()}`,
            explanation: `Total Value: $${Math.round(futureVal).toLocaleString()} (Invested: $${invested.toLocaleString()}, Wealth Gain: $${Math.round(wealthGain).toLocaleString()}).`
          };
        }
        case "fd-calculator": {
          const p = parseFloat(inputs.fd_principal), r = parseFloat(inputs.fd_rate), y = parseFloat(inputs.fd_years);
          if (isNaN(p) || isNaN(r) || isNaN(y)) return { error: "Invalid FD inputs." };
          const mat = p * Math.pow(1 + (r / 400), 4 * y);
          const int = mat - p;
          return { value: `$${mat.toFixed(2)}`, explanation: `Maturity Value: $${mat.toFixed(2)} (Interest Earned: $${int.toFixed(2)}).` };
        }
        case "rd-calculator": {
          const p = parseFloat(inputs.rd_monthly), r = parseFloat(inputs.rd_rate), n = parseFloat(inputs.rd_months);
          if (isNaN(p) || isNaN(r) || isNaN(n)) return { error: "Invalid RD inputs." };
          const totalDep = p * n;
          const int = p * (n * (n + 1) / 2) * (r / 1200);
          const mat = totalDep + int;
          return { value: `$${mat.toFixed(2)}`, explanation: `Maturity Value: $${mat.toFixed(2)} (Total Deposited: $${totalDep}, Interest: $${int.toFixed(2)}).` };
        }
        case "compound-interest-calculator": {
          const p = parseFloat(inputs.ci_principal), r = parseFloat(inputs.ci_rate), t = parseFloat(inputs.ci_years);
          let n = 12;
          if (inputs.ci_freq.includes("Annually")) n = 1;
          else if (inputs.ci_freq.includes("Quarterly")) n = 4;
          if (isNaN(p) || isNaN(r) || isNaN(t)) return { error: "Invalid compound interest inputs." };
          const amount = p * Math.pow(1 + (r / 100) / n, n * t);
          const ci = amount - p;
          return { value: `$${amount.toFixed(2)}`, explanation: `Future Value: $${amount.toFixed(2)} (Interest Earned: $${ci.toFixed(2)}).` };
        }
        case "simple-interest-calculator": {
          const p = parseFloat(inputs.si_p), r = parseFloat(inputs.si_r), t = parseFloat(inputs.si_t);
          if (isNaN(p) || isNaN(r) || isNaN(t)) return { error: "Invalid SI inputs." };
          const si = (p * r * t) / 100;
          const tot = p + si;
          return { value: `$${tot.toFixed(2)}`, explanation: `Simple Interest Earned: $${si.toFixed(2)}. Total Maturity Amount: $${tot.toFixed(2)}.` };
        }
        case "gst-calculator": {
          const amt = parseFloat(inputs.gst_amount), r = parseFloat(inputs.gst_rate);
          if (isNaN(amt) || isNaN(r)) return { error: "Invalid GST numbers." };
          let gst = 0, net = 0, gross = 0;
          if (inputs.gst_type.includes("Add")) {
            gst = (amt * r) / 100;
            gross = amt + gst;
            net = amt;
          } else {
            gross = amt;
            net = amt / (1 + r / 100);
            gst = gross - net;
          }
          return { value: `$${gross.toFixed(2)} Total`, explanation: `Net Price: $${net.toFixed(2)}, GST Tax (${r}%): $${gst.toFixed(2)}, Gross Total: $${gross.toFixed(2)}.` };
        }
        case "discount-calculator": {
          const orig = parseFloat(inputs.disc_orig), pct = parseFloat(inputs.disc_pct);
          if (isNaN(orig) || isNaN(pct)) return { error: "Invalid discount numbers." };
          const save = orig * (pct / 100);
          const finalP = orig - save;
          return { value: `$${finalP.toFixed(2)}`, explanation: `Discounted Price: $${finalP.toFixed(2)} (You save $${save.toFixed(2)}).` };
        }
        case "salary-calculator": {
          const ann = parseFloat(inputs.sal_annual), hrsWk = parseFloat(inputs.sal_hours) || 40;
          if (isNaN(ann)) return { error: "Invalid salary input." };
          const monthly = ann / 12;
          const hourly = ann / (hrsWk * 52);
          return { value: `$${monthly.toFixed(2)} / month`, explanation: `Monthly Pay: $${monthly.toFixed(2)}, Hourly Wage: $${hourly.toFixed(2)}/hr (${hrsWk} hrs/wk).` };
        }
        case "income-tax-calculator": {
          const inc = parseFloat(inputs.tax_income), ded = parseFloat(inputs.tax_deduct) || 0;
          if (isNaN(inc)) return { error: "Invalid income input." };
          const taxable = Math.max(0, inc - ded);
          let tax = 0;
          if (taxable > 100000) tax = 15000 + (taxable - 100000) * 0.25;
          else if (taxable > 50000) tax = 2500 + (taxable - 50000) * 0.15;
          else if (taxable > 10000) tax = (taxable - 10000) * 0.10;
          const netInc = inc - tax;
          return { value: `$${tax.toFixed(2)} Tax`, explanation: `Tax Liability: $${tax.toFixed(2)}. Net Take-Home Income: $${netInc.toFixed(2)}.` };
        }
        case "inflation-calculator": {
          const amt = parseFloat(inputs.inf_amount), r = parseFloat(inputs.inf_rate), y = parseFloat(inputs.inf_years);
          if (isNaN(amt) || isNaN(r) || isNaN(y)) return { error: "Invalid inflation numbers." };
          const fut = amt * Math.pow(1 + (r / 100), y);
          return { value: `$${fut.toFixed(2)}`, explanation: `In ${y} years, $${amt} will require $${fut.toFixed(2)} to match equivalent purchasing power.` };
        }
        case "investment-calculator": {
          const init = parseFloat(inputs.inv_initial), fin = parseFloat(inputs.inv_final);
          if (isNaN(init) || isNaN(fin) || init <= 0) return { error: "Invalid investment numbers." };
          const roi = ((fin - init) / init) * 100;
          const profit = fin - init;
          return { value: `${roi.toFixed(2)}% ROI`, explanation: `Net Profit: $${profit.toFixed(2)}. Return on Investment (ROI): ${roi.toFixed(2)}%.` };
        }
        case "profit-loss-calculator": {
          const cp = parseFloat(inputs.cost_price), sp = parseFloat(inputs.sell_price);
          if (isNaN(cp) || isNaN(sp)) return { error: "Invalid prices." };
          const diff = sp - cp;
          const pct = (diff / cp) * 100;
          const label = diff >= 0 ? "Profit" : "Loss";
          return { value: `${label}: $${Math.abs(diff).toFixed(2)} (${pct.toFixed(2)}%)`, explanation: `Selling Price vs Cost Price results in a ${label.toLowerCase()} of ${Math.abs(pct).toFixed(2)}%.` };
        }
        case "percentage-increase-calculator": {
          const init = parseFloat(inputs.pct_initial), fin = parseFloat(inputs.pct_final);
          if (isNaN(init) || isNaN(fin) || init === 0) return { error: "Invalid inputs." };
          const change = ((fin - init) / init) * 100;
          const label = change >= 0 ? "Increase" : "Decrease";
          return { value: `${Math.abs(change).toFixed(2)}% ${label}`, explanation: `Value changed from ${init} to ${fin} (${Math.abs(change).toFixed(2)}% ${label.toLowerCase()}).` };
        }
        case "currency-converter": {
          const amt = parseFloat(inputs.curr_amount), f = inputs.curr_from, t = inputs.curr_to;
          if (isNaN(amt)) return { error: "Invalid amount." };
          const ratesToUSD = { USD: 1.0, EUR: 1.08, GBP: 1.28, INR: 0.012, CAD: 0.74, AUD: 0.66 };
          const inUSD = amt * (ratesToUSD[f] || 1.0);
          const result = inUSD / (ratesToUSD[t] || 1.0);
          return { value: `${result.toFixed(2)} ${t}`, explanation: `${amt} ${f} = ${result.toFixed(2)} ${t} (Benchmark Forex Rate).` };
        }
        case "tip-calculator": {
          const bill = parseFloat(inputs.bill_total), tipP = parseFloat(inputs.tip_pct), ppl = parseInt(inputs.split_people) || 1;
          if (isNaN(bill) || isNaN(tipP)) return { error: "Invalid bill inputs." };
          const tipAmt = bill * (tipP / 100);
          const total = bill + tipAmt;
          const perP = total / ppl;
          return { value: `$${perP.toFixed(2)} per person`, explanation: `Total Tip: $${tipAmt.toFixed(2)}. Grand Total: $${total.toFixed(2)} ($${perP.toFixed(2)} split × ${ppl} people).` };
        }
        case "mortgage-calculator": {
          const price = parseFloat(inputs.home_price), down = parseFloat(inputs.down_pay), rYr = parseFloat(inputs.mort_rate), y = parseFloat(inputs.mort_years);
          if (isNaN(price) || isNaN(down) || isNaN(rYr) || isNaN(y)) return { error: "Invalid mortgage inputs." };
          const p = Math.max(0, price - down);
          const r = (rYr / 12) / 100;
          const n = y * 12;
          const pay = (p * r * Math.pow(1+r, n)) / (Math.pow(1+r, n) - 1);
          return { value: `$${pay.toFixed(2)} / month`, explanation: `Loan Amount: $${p.toFixed(2)}. Monthly P&I Mortgage Payment: $${pay.toFixed(2)}.` };
        }
        case "savings-calculator": {
          const init = parseFloat(inputs.sav_initial), mAdd = parseFloat(inputs.sav_monthly), rYr = parseFloat(inputs.sav_rate), y = parseFloat(inputs.sav_years);
          if (isNaN(init) || isNaN(mAdd) || isNaN(rYr) || isNaN(y)) return { error: "Invalid savings inputs." };
          const r = (rYr / 12) / 100;
          const n = y * 12;
          let future = init * Math.pow(1 + r, n);
          future += mAdd * ((Math.pow(1 + r, n) - 1) / r);
          return { value: `$${future.toFixed(2)}`, explanation: `Accumulated savings after ${y} years: $${future.toFixed(2)}.` };
        }
        case "retirement-calculator": {
          const cAge = parseFloat(inputs.ret_age), rAge = parseFloat(inputs.ret_retire_age), exp = parseFloat(inputs.ret_exp);
          if (isNaN(cAge) || isNaN(rAge) || isNaN(exp) || rAge <= cAge) return { error: "Invalid retirement inputs." };
          const corpus = exp * 12 * 25; // 4% rule
          const yearsLeft = rAge - cAge;
          return { value: `$${corpus.toLocaleString()} Target Corpus`, explanation: `Required Nest Egg for $${exp}/mo retirement: $${corpus.toLocaleString()} (Time left: ${yearsLeft} years).` };
        }

        // ==================== 4. DEVELOPER TOOLS ====================
        case "password-generator": {
          const len = parseInt(inputs.pass_length) || 16;
          const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=";
          let pass = "";
          for (let i = 0; i < len; i++) { pass += chars.charAt(Math.floor(Math.random() * chars.length)); }
          return { value: pass, explanation: `Generated a ${len}-character secure password with high entropy.` };
        }
        case "qr-generator": {
          const text = inputs.qr_text || "https://calculator-hub.com";
          const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(text)}`;
          return { value: `[QR Code Generated]`, explanation: `<img src="${qrUrl}" alt="QR Code" style="margin:10px auto; border-radius:8px;"> Scan QR code or copy text.` };
        }
        case "json-formatter": {
          const raw = inputs.json_input;
          if (!raw) return { error: "Please enter JSON." };
          const obj = JSON.parse(raw);
          const pretty = JSON.stringify(obj, null, 2);
          return { value: pretty, explanation: "JSON formatted and validated successfully." };
        }
        case "json-validator": {
          const raw = inputs.json_val_input;
          if (!raw) return { error: "Please enter JSON to validate." };
          JSON.parse(raw);
          return { value: "VALID JSON", explanation: "Syntax check passed! Your JSON string is 100% valid." };
        }
        case "html-encoder": {
          const txt = inputs.html_text || "";
          const encoded = txt.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
          return { value: encoded, explanation: "Special HTML entity characters encoded safely." };
        }
        case "url-encoder": {
          const txt = inputs.url_text || "";
          const enc = encodeURIComponent(txt);
          return { value: enc, explanation: "URL string encoded using percent-encoding." };
        }
        case "binary-converter": {
          const txt = inputs.bin_input || "";
          let bin = "";
          for (let i = 0; i < txt.length; i++) {
            bin += txt.charCodeAt(i).toString(2).padStart(8, '0') + " ";
          }
          return { value: bin.trim(), explanation: `Converted text "${txt}" into 8-bit binary representation.` };
        }
        case "hex-converter": {
          const txt = inputs.hex_input || "";
          let hex = "";
          for (let i = 0; i < txt.length; i++) {
            hex += txt.charCodeAt(i).toString(16).toUpperCase() + " ";
          }
          return { value: hex.trim(), explanation: `Converted text into Base-16 Hexadecimal bytes.` };
        }
        case "timestamp-converter": {
          const ts = parseInt(inputs.ts_val);
          if (isNaN(ts)) return { error: "Invalid timestamp." };
          const d = new Date(ts * 1000);
          return { value: d.toUTCString(), explanation: `Unix Timestamp ${ts} equals ${d.toUTCString()} (Local: ${d.toLocaleString()}).` };
        }
        case "base-converter": {
          const num = inputs.base_num;
          if (!num) return { error: "Enter number." };
          let fromB = 10;
          if (inputs.base_from.includes("Binary")) fromB = 2;
          else if (inputs.base_from.includes("Hexadecimal")) fromB = 16;
          else if (inputs.base_from.includes("Octal")) fromB = 8;
          const dec = parseInt(num, fromB);
          if (isNaN(dec)) return { error: "Invalid input for selected base." };
          return {
            value: `Dec: ${dec}`,
            explanation: `Bin: ${dec.toString(2)} | Oct: ${dec.toString(8)} | Hex: ${dec.toString(16).toUpperCase()}`
          };
        }

        // ==================== 5. MATH ====================
        case "scientific-calculator": {
          const expr = inputs.sci_expr;
          if (!expr) return { error: "Enter math expression." };
          const safeExpr = expr.replace(/sin/g, 'Math.sin')
                               .replace(/cos/g, 'Math.cos')
                               .replace(/tan/g, 'Math.tan')
                               .replace(/sqrt/g, 'Math.sqrt')
                               .replace(/log/g, 'Math.log10')
                               .replace(/pi/gi, 'Math.PI');
          const res = Function(`"use strict"; return (${safeExpr})`)();
          return { value: res.toString(), explanation: `Evaluated expression: ${expr} = ${res}` };
        }
        case "fraction-calculator": {
          const n1 = parseInt(inputs.frac1_num), d1 = parseInt(inputs.frac1_den);
          const n2 = parseInt(inputs.frac2_num), d2 = parseInt(inputs.frac2_den);
          if (d1 === 0 || d2 === 0) return { error: "Denominator cannot be zero." };
          let resN = 0, resD = d1 * d2;
          if (inputs.frac_op.includes("+")) resN = n1 * d2 + n2 * d1;
          else if (inputs.frac_op.includes("-")) resN = n1 * d2 - n2 * d1;
          else if (inputs.frac_op.includes("×")) { resN = n1 * n2; resD = d1 * d2; }
          else if (inputs.frac_op.includes("÷")) { resN = n1 * d2; resD = d1 * n2; }
          const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
          const g = gcd(resN, resD);
          return { value: `${resN/g} / ${resD/g}`, explanation: `Result simplified: ${resN/g}/${resD/g} (Decimal: ${(resN/resD).toFixed(4)}).` };
        }
        case "lcm-calculator": {
          const n1 = parseInt(inputs.lcm_n1), n2 = parseInt(inputs.lcm_n2);
          if (isNaN(n1) || isNaN(n2)) return { error: "Invalid numbers." };
          const gcd = (a, b) => b ? gcd(b, a % b) : a;
          const lcm = (n1 * n2) / gcd(n1, n2);
          return { value: lcm.toString(), explanation: `Least Common Multiple of ${n1} and ${n2} is ${lcm}.` };
        }
        case "hcf-calculator": {
          const n1 = parseInt(inputs.hcf_n1), n2 = parseInt(inputs.hcf_n2);
          if (isNaN(n1) || isNaN(n2)) return { error: "Invalid numbers." };
          const gcd = (a, b) => b ? gcd(b, a % b) : a;
          const hcf = gcd(n1, n2);
          return { value: hcf.toString(), explanation: `Highest Common Factor (GCD) of ${n1} and ${n2} is ${hcf}.` };
        }
        case "prime-number-checker": {
          const num = parseInt(inputs.prime_num);
          if (isNaN(num)) return { error: "Invalid integer." };
          if (num <= 1) return { value: "NOT PRIME", explanation: `${num} is not a prime number.` };
          let isPrime = true;
          const factors = [];
          for (let i = 1; i <= Math.sqrt(num); i++) {
            if (num % i === 0) {
              factors.push(i);
              if (i !== num / i) factors.push(num / i);
              if (i > 1) isPrime = false;
            }
          }
          factors.sort((a,b) => a-b);
          return {
            value: isPrime ? "PRIME NUMBER" : "COMPOSITE NUMBER",
            explanation: isPrime ? `${num} is a prime number!` : `${num} is not prime. Factors: ${factors.join(", ")}.`
          };
        }
        case "percentage-difference-calculator": {
          const v1 = parseFloat(inputs.pd_v1), v2 = parseFloat(inputs.pd_v2);
          if (isNaN(v1) || isNaN(v2)) return { error: "Invalid numbers." };
          const diff = Math.abs(v1 - v2);
          const avg = (v1 + v2) / 2;
          const pct = (diff / avg) * 100;
          return { value: `${pct.toFixed(2)}%`, explanation: `Percentage difference between ${v1} and ${v2} is ${pct.toFixed(2)}%.` };
        }
        case "area-calculator": {
          const shape = inputs.shape_type, d1 = parseFloat(inputs.dim1), d2 = parseFloat(inputs.dim2) || 0;
          if (isNaN(d1)) return { error: "Invalid dimensions." };
          let area = 0;
          if (shape === "Circle") area = Math.PI * d1 * d1;
          else if (shape === "Rectangle") area = d1 * d2;
          else if (shape === "Triangle") area = 0.5 * d1 * d2;
          return { value: `${area.toFixed(2)} sq units`, explanation: `Surface Area of ${shape}: ${area.toFixed(2)}.` };
        }
        case "volume-calculator": {
          const shape = inputs.vol_shape, d1 = parseFloat(inputs.vol_dim1), d2 = parseFloat(inputs.vol_dim2) || 0, d3 = parseFloat(inputs.vol_dim3) || 0;
          if (isNaN(d1)) return { error: "Invalid dimensions." };
          let vol = 0;
          if (shape === "Sphere") vol = (4/3) * Math.PI * Math.pow(d1, 3);
          else if (shape === "Cylinder") vol = Math.PI * Math.pow(d1, 2) * d2;
          else if (shape === "Cube") vol = Math.pow(d1, 3);
          else if (shape === "Rectangular Prism") vol = d1 * d2 * d3;
          return { value: `${vol.toFixed(2)} cubic units`, explanation: `Volume of ${shape}: ${vol.toFixed(2)}.` };
        }
        case "triangle-calculator": {
          const a = parseFloat(inputs.tri_side_a), b = parseFloat(inputs.tri_side_b), c = parseFloat(inputs.tri_side_c);
          if (isNaN(a) || isNaN(b) || isNaN(c)) return { error: "Invalid side lengths." };
          if (a+b <= c || a+c <= b || b+c <= a) return { error: "Triangle inequality violated." };
          const s = (a + b + c) / 2;
          const area = Math.sqrt(s * (s-a) * (s-b) * (s-c));
          return { value: `${area.toFixed(2)} sq units`, explanation: `Triangle Area (Heron's Formula): ${area.toFixed(2)}, Perimeter: ${a+b+c}.` };
        }
        case "math-average-calculator": {
          const arr = inputs.stat_nums.split(",").map(n => parseFloat(n.trim())).filter(n => !isNaN(n));
          if (!arr.length) return { error: "Enter valid numbers." };
          arr.sort((a,b) => a-b);
          const sum = arr.reduce((a,b) => a+b, 0);
          const mean = sum / arr.length;
          const mid = Math.floor(arr.length / 2);
          const median = arr.length % 2 !== 0 ? arr[mid] : (arr[mid - 1] + arr[mid]) / 2;
          return { value: `Mean: ${mean.toFixed(2)}`, explanation: `Median: ${median}, Min: ${arr[0]}, Max: ${arr[arr.length-1]}, Range: ${arr[arr.length-1]-arr[0]}.` };
        }

        // ==================== 6. DAILY UTILITY TOOLS ====================
        case "time-calculator": {
          const t1 = inputs.time1.split(":").map(Number);
          const t2 = inputs.time2.split(":").map(Number);
          const s1 = (t1[0]||0)*3600 + (t1[1]||0)*60 + (t1[2]||0);
          const s2 = (t2[0]||0)*3600 + (t2[1]||0)*60 + (t2[2]||0);
          const totS = inputs.time_op.includes("+") ? s1 + s2 : Math.max(0, s1 - s2);
          const h = Math.floor(totS / 3600), m = Math.floor((totS % 3600) / 60), s = totS % 60;
          return { value: `${h}h ${m}m ${s}s`, explanation: `Formatted Result: ${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}.` };
        }
        case "age-difference-calculator": {
          if (!inputs.person1_dob || !inputs.person2_dob) return { error: "Select both dates." };
          const d1 = new Date(inputs.person1_dob), d2 = new Date(inputs.person2_dob);
          const diffDays = Math.abs(Math.floor((d2 - d1) / (1000 * 60 * 60 * 24)));
          const yrs = (diffDays / 365.25).toFixed(1);
          return { value: `${diffDays} Days Gap`, explanation: `Age gap between Person 1 and Person 2 is ~${yrs} years (${diffDays} days).` };
        }
        case "date-calculator": {
          if (!inputs.base_date) return { error: "Select starting date." };
          const base = new Date(inputs.base_date);
          const days = parseInt(inputs.num_days) || 0;
          const mult = inputs.date_op.includes("-") ? -1 : 1;
          const target = new Date(base.getTime() + (days * mult * 24 * 60 * 60 * 1000));
          return { value: target.toDateString(), explanation: `Target Date: ${target.toDateString()}.` };
        }
        case "unit-converter":
        case "length-converter": {
          const val = parseFloat(inputs.unit_val || inputs.len_val);
          const from = inputs.unit_from || inputs.len_from;
          const to = inputs.unit_to || inputs.len_to;
          if (isNaN(val)) return { error: "Invalid value." };
          const toMeters = { Meters: 1, Kilometers: 1000, Miles: 1609.34, Feet: 0.3048, Inches: 0.0254, Centimeters: 0.01 };
          const meters = val * (toMeters[from] || 1);
          const res = meters / (toMeters[to] || 1);
          return { value: `${res.toFixed(4)} ${to}`, explanation: `${val} ${from} = ${res.toFixed(4)} ${to}.` };
        }
        case "weight-converter": {
          const val = parseFloat(inputs.wt_val), f = inputs.wt_from, t = inputs.wt_to;
          if (isNaN(val)) return { error: "Invalid value." };
          const toGrams = { "Kilograms (kg)": 1000, "Pounds (lbs)": 453.592, "Grams (g)": 1, "Ounces (oz)": 28.3495 };
          const g = val * (toGrams[f] || 1);
          const res = g / (toGrams[t] || 1);
          return { value: `${res.toFixed(4)}`, explanation: `${val} ${f} = ${res.toFixed(4)} ${t}.` };
        }
        case "temperature-converter": {
          const v = parseFloat(inputs.temp_val), f = inputs.temp_from, t = inputs.temp_to;
          if (isNaN(v)) return { error: "Invalid value." };
          let c = v;
          if (f.includes("Fahrenheit")) c = (v - 32) * (5/9);
          else if (f.includes("Kelvin")) c = v - 273.15;
          let res = c;
          if (t.includes("Fahrenheit")) res = (c * 9/5) + 32;
          else if (t.includes("Kelvin")) res = c + 273.15;
          return { value: `${res.toFixed(2)}`, explanation: `${v} ${f} converts to ${res.toFixed(2)} ${t}.` };
        }
        case "speed-converter": {
          const v = parseFloat(inputs.spd_val), f = inputs.spd_from, t = inputs.spd_to;
          if (isNaN(v)) return { error: "Invalid value." };
          const toKmh = { "Miles per hour (mph)": 1.60934, "Kilometers per hour (km/h)": 1.0, "Meters per second (m/s)": 3.6, "Knots": 1.852 };
          const kmh = v * (toKmh[f] || 1);
          const res = kmh / (toKmh[t] || 1);
          return { value: `${res.toFixed(2)}`, explanation: `${v} ${f} = ${res.toFixed(2)} ${t}.` };
        }
        case "fuel-cost-calculator": {
          const dist = parseFloat(inputs.fuel_dist), eff = parseFloat(inputs.fuel_eff), price = parseFloat(inputs.fuel_price);
          if (isNaN(dist) || isNaN(eff) || isNaN(price) || eff <= 0) return { error: "Invalid inputs." };
          const fuelNeeded = dist / eff;
          const cost = fuelNeeded * price;
          return { value: `$${cost.toFixed(2)} Total Cost`, explanation: `Trip requires ~${fuelNeeded.toFixed(1)} units of fuel, costing $${cost.toFixed(2)}.` };
        }
        case "electricity-bill-calculator": {
          const watts = parseFloat(inputs.elec_watt), hrs = parseFloat(inputs.elec_hours), rate = parseFloat(inputs.elec_rate);
          if (isNaN(watts) || isNaN(hrs) || isNaN(rate)) return { error: "Invalid inputs." };
          const kWhMonth = (watts * hrs * 30) / 1000;
          const costMonth = kWhMonth * rate;
          return { value: `$${costMonth.toFixed(2)} / month`, explanation: `Monthly consumption: ${kWhMonth.toFixed(1)} kWh. Estimated cost: $${costMonth.toFixed(2)}.` };
        }

        // ==================== 7. FITNESS ADVANCED ====================
        case "calories-burned-calculator": {
          const w = parseFloat(inputs.cb_weight), dur = parseFloat(inputs.cb_duration);
          if (isNaN(w) || isNaN(dur)) return { error: "Invalid inputs." };
          let met = 5.0;
          if (inputs.cb_activity.includes("Cycling")) met = 8.0;
          else if (inputs.cb_activity.includes("Swimming")) met = 7.0;
          else if (inputs.cb_activity.includes("Basketball")) met = 6.5;
          const cal = (met * 3.5 * w / 200) * dur;
          return { value: `${Math.round(cal)} kcal`, explanation: `${dur} minutes of ${inputs.cb_activity} burned ~${Math.round(cal)} kcal.` };
        }
        case "pushup-calories-calculator": {
          const w = parseFloat(inputs.push_weight), reps = parseInt(inputs.push_reps);
          if (isNaN(w) || isNaN(reps)) return { error: "Invalid inputs." };
          const cal = reps * 0.32 * (w / 70);
          return { value: `${Math.round(cal)} kcal`, explanation: `${reps} pushups by a ${w}kg person burns ~${Math.round(cal)} kcal.` };
        }
        case "workout-calculator": {
          const w = parseFloat(inputs.work_weight), r = parseInt(inputs.work_reps), s = parseInt(inputs.work_sets);
          if (isNaN(w) || isNaN(r) || isNaN(s)) return { error: "Invalid workout parameters." };
          const vol = w * r * s;
          return { value: `${vol.toLocaleString()} kg Total Volume`, explanation: `Total Workout Tonnage: ${vol.toLocaleString()} kg (${s} sets × ${r} reps @ ${w} kg).` };
        }
        case "one-rep-max-calculator": {
          const w = parseFloat(inputs.orm_weight), r = parseInt(inputs.orm_reps);
          if (isNaN(w) || isNaN(r) || r < 1) return { error: "Invalid inputs." };
          const epley1rm = w * (1 + r / 30);
          return { value: `${epley1rm.toFixed(1)} kg (1RM)`, explanation: `Estimated 1 Rep Max (Epley Formula): ~${epley1rm.toFixed(1)} kg.` };
        }
        case "body-shape-calculator": {
          const b = parseFloat(inputs.bs_bust), w = parseFloat(inputs.bs_waist), h = parseFloat(inputs.bs_hip);
          if (isNaN(b) || isNaN(w) || isNaN(h)) return { error: "Invalid body measurements." };
          let shape = "Rectangle";
          if ((b - h) <= 5 && (h - b) <= 5 && (b - w) >= 20) shape = "Hourglass";
          else if ((h - b) >= 9) shape = "Pear (Bottom Triangle)";
          else if ((b - h) >= 9) shape = "Apple (Inverted Triangle)";
          return { value: shape, explanation: `Your body proportions indicate an '${shape}' shape profile.` };
        }
        case "water-weight-calculator": {
          const w = parseFloat(inputs.ww_weight);
          if (isNaN(w)) return { error: "Invalid weight." };
          const ret = w * (inputs.ww_sodium.includes("High") ? 0.03 : 0.01);
          return { value: `~${ret.toFixed(1)} kg Water Retention`, explanation: `Temporary scale weight fluctuation attributable to sodium/carb fluid binding.` };
        }
        case "step-counter-calculator": {
          const steps = parseInt(inputs.steps_count), w = parseFloat(inputs.steps_weight) || 70;
          if (isNaN(steps)) return { error: "Invalid steps." };
          const km = steps * 0.00078;
          const cal = steps * 0.04 * (w / 70);
          return { value: `${km.toFixed(2)} km (${Math.round(cal)} kcal)`, explanation: `${steps.toLocaleString()} steps equals ~${km.toFixed(2)} km and burns ~${Math.round(cal)} kcal.` };
        }
        case "walking-calories-calculator": {
          const w = parseFloat(inputs.walk_weight), t = parseFloat(inputs.walk_time);
          if (isNaN(w) || isNaN(t)) return { error: "Invalid inputs." };
          let met = 3.5;
          if (inputs.walk_pace.includes("Slow")) met = 2.8;
          else if (inputs.walk_pace.includes("Brisk")) met = 4.3;
          const cal = (met * 3.5 * w / 200) * t;
          return { value: `${Math.round(cal)} kcal`, explanation: `Walking for ${t} minutes at ${inputs.walk_pace} burned ~${Math.round(cal)} kcal.` };
        }

        // ==================== 8. EXTRA SEO TOOLS ====================
        case "cgpa-to-percentage-converter": {
          const val = parseFloat(inputs.c2p_val || inputs.c2p_cgpa), customFactor = parseFloat(inputs.c2p_factor) || 9.5;
          const isReverse = inputs.c2p_mode && inputs.c2p_mode.includes("Reverse");
          const scale = inputs.c2p_scale || "CBSE";

          if (isNaN(val)) return { error: "Invalid numerical value." };

          if (!isReverse) {
            // CGPA to Percentage
            let pct = 0;
            let formulaText = "";
            if (scale.includes("AICTE")) {
              pct = (val - 0.75) * 10;
              formulaText = `(${val} CGPA - 0.75) × 10 = ${pct.toFixed(2)}%`;
            } else if (scale.includes("Direct")) {
              pct = val * 10;
              formulaText = `${val} CGPA × 10 = ${pct.toFixed(2)}%`;
            } else if (scale.includes("Custom")) {
              pct = val * customFactor;
              formulaText = `${val} CGPA × ${customFactor} = ${pct.toFixed(2)}%`;
            } else {
              // CBSE default
              pct = val * 9.5;
              formulaText = `${val} CGPA × 9.5 = ${pct.toFixed(2)}%`;
            }
            return {
              value: `${pct.toFixed(2)}%`,
              explanation: `Calculation (${scale}): ${formulaText}. (CBSE Equivalent: ${(val * 9.5).toFixed(2)}%, Direct Scale: ${(val * 10).toFixed(2)}%).`
            };
          } else {
            // Percentage to CGPA (Reverse)
            let cgpa = 0;
            let formulaText = "";
            if (scale.includes("AICTE")) {
              cgpa = (val / 10) + 0.75;
              formulaText = `(${val}% ÷ 10) + 0.75 = ${cgpa.toFixed(2)} CGPA`;
            } else if (scale.includes("Direct")) {
              cgpa = val / 10;
              formulaText = `${val}% ÷ 10 = ${cgpa.toFixed(2)} CGPA`;
            } else if (scale.includes("Custom")) {
              cgpa = val / customFactor;
              formulaText = `${val}% ÷ ${customFactor} = ${cgpa.toFixed(2)} CGPA`;
            } else {
              // CBSE default
              cgpa = val / 9.5;
              formulaText = `${val}% ÷ 9.5 = ${cgpa.toFixed(2)} CGPA`;
            }
            return {
              value: `${cgpa.toFixed(2)} CGPA`,
              explanation: `Reverse Calculation (${scale}): ${formulaText}. (On 10.0 scale).`
            };
          }
        }
        case "percentage-to-cgpa-converter": {
          const pct = parseFloat(inputs.p2c_pct);
          const scale = inputs.p2c_scale || "CBSE";
          if (isNaN(pct)) return { error: "Invalid percentage score." };
          
          let cgpa = 0;
          if (scale.includes("AICTE")) {
            cgpa = (pct / 10) + 0.75;
          } else if (scale.includes("Direct")) {
            cgpa = pct / 10;
          } else {
            cgpa = pct / 9.5;
          }
          return {
            value: `${cgpa.toFixed(2)} CGPA`,
            explanation: `Percentage ${pct}% converted using ${scale} formula = ${cgpa.toFixed(2)} CGPA (10.0 scale).`
          };
        }
        case "gpa-converter": {
          const score = parseFloat(inputs.gpa_val);
          if (isNaN(score)) return { error: "Invalid GPA." };
          let is4 = inputs.gpa_scale_from.includes("4.0");
          let gpa10 = is4 ? (score / 4.0) * 10 : score;
          let gpa4 = is4 ? score : (score / 10.0) * 4;
          let pct = is4 ? (score / 4.0) * 100 : score * 9.5;
          return { value: `10-Scale: ${gpa10.toFixed(2)} | 4-Scale: ${gpa4.toFixed(2)}`, explanation: `Equivalent Percentage: ~${pct.toFixed(1)}%.` };
        }
        case "days-calculator": {
          if (!inputs.days_target) return { error: "Select target date." };
          const target = new Date(inputs.days_target);
          const now = new Date();
          const diffMs = target - now;
          const days = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
          return { value: `${days} Days Left`, explanation: `There are ${days} days remaining until ${target.toDateString()}.` };
        }
        case "hours-calculator": {
          const sStr = inputs.hrs_start || "09:00", eStr = inputs.hrs_end || "17:00";
          const brk = parseInt(inputs.hrs_break) || 0, wage = parseFloat(inputs.hrs_wage) || 0;
          const [sh, sm] = sStr.split(":").map(Number);
          const [eh, em] = eStr.split(":").map(Number);
          let sMin = sh * 60 + sm, eMin = eh * 60 + em;
          if (eMin < sMin) eMin += 24 * 60;
          const netMin = Math.max(0, (eMin - sMin) - brk);
          const hrs = netMin / 60;
          const pay = hrs * wage;
          return { value: `${hrs.toFixed(2)} Net Hours`, explanation: `Net Work Hours: ${hrs.toFixed(2)} hrs. Total Earnings: $${pay.toFixed(2)}.` };
        }
        case "minutes-calculator": {
          const min = parseInt(inputs.min_input);
          if (isNaN(min)) return { error: "Invalid minutes input." };
          const h = Math.floor(min / 60);
          const m = min % 60;
          return { value: `${h} Hours, ${m} Minutes`, explanation: `${min} total minutes converts to ${h}h ${m}m.` };
        }
        case "random-number-generator": {
          const min = parseInt(inputs.rng_min), max = parseInt(inputs.rng_max), count = parseInt(inputs.rng_count) || 1;
          if (isNaN(min) || isNaN(max) || min >= max) return { error: "Invalid min/max range." };
          const nums = [];
          for (let i = 0; i < count; i++) {
            nums.push(Math.floor(Math.random() * (max - min + 1)) + min);
          }
          return { value: nums.join(", "), explanation: `Generated ${count} random number(s) between ${min} and ${max}.` };
        }
        case "password-strength-checker": {
          const p = inputs.chk_pass || "";
          let score = 0;
          if (p.length >= 8) score += 20;
          if (p.length >= 12) score += 30;
          if (/[A-Z]/.test(p)) score += 15;
          if (/[0-9]/.test(p)) score += 15;
          if (/[^A-Za-z0-9]/.test(p)) score += 20;
          let label = "WEAK";
          if (score >= 80) label = "VERY STRONG";
          else if (score >= 60) label = "STRONG";
          else if (score >= 40) label = "FAIR";
          return { value: `${score}/100 (${label})`, explanation: `Password contains ${p.length} characters. Crack estimate: ${score > 70 ? 'Centuries' : 'Hours/Days'}.` };
        }
        case "character-counter": {
          const text = inputs.cc_text || "";
          const chars = text.length;
          const noSpaces = text.replace(/\s/g, "").length;
          const words = text.trim() ? text.trim().split(/\s+/).length : 0;
          return { value: `${chars} Characters`, explanation: `Without spaces: ${noSpaces} chars. Total words: ${words}.` };
        }
        case "word-counter": {
          const text = inputs.wc_text || "";
          const words = text.trim() ? text.trim().split(/\s+/).length : 0;
          const readMin = (words / 200).toFixed(1);
          return { value: `${words} Words`, explanation: `Estimated Reading Time: ~${readMin} mins (${text.length} total characters).` };
        }
        case "text-case-converter": {
          const text = inputs.tcc_text || "";
          const upper = text.toUpperCase();
          const lower = text.toLowerCase();
          const title = text.replace(/\w\S*/g, (txt) => txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase());
          return {
            value: upper,
            explanation: `UPPERCASE: ${upper} | lowercase: ${lower} | Title Case: ${title}`
          };
        }

        default:
          return { error: "Calculator logic for this tool is not defined." };
      }
    } catch (err) {
      return { error: "Calculation error: " + err.message };
    }
  }
};

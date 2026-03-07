# 💡 Lumina Intelligence: Light Overview Dashboard (Simple Terms)

Is document me hum samjhenge ki Dashboard ke "Overview" page par dikhne wale metrics (Verdict, Avg Coherence, Avg Drift Score, Conflicts, aur Transitions) kya darshate hain aur wo kaise calculate hote hain.

### 1. ⚠️ VERDICT: WARN (Lekin saare scenes pass kyu hain?)
* **Matlab:** Pura system result ("PASS", "WARN", ya "FAIL")
* **Ye kyu aara hai:** Screenshot me likha hai *"System evaluation passed 4 out of 4 scenes successfully."* - iska matlab hai logic, format, aur lights me koi major error (Fail) nahi hai. Lekin fir bhi "WARN" results isliye aata hai, kyuki ho sakta hai kisi ek chote calculation (jaise confidence score border line pe ho) ya koi minor emotional shift hua ho, jise AI chahta hai ki ek insaan (director/operator) final execution se pehle ek baar dekh le. "Proceed" ka tag batata hai ki shows nahi rukega, aap aage badh sakte hain, bas ek nazar maar lijiye.

### 2. 💯 AVG COHERENCE (100%)
* **Matlab:** AI ki samajh aur Logic ka Score (Sense-making score).
* **Ye kya batata hai:** Ye dikhata hai ki overall pura lighting design, story aur emotion ke hisaab se kitna "Make-Sense" (logical) hai. 100% ka matlab hai ki AI ne emotion (Anxiety) ko padh kar bilkul perfect aur rule-bound lights (jaise focus, intensity, colors) banaye hain, kuch bhi be-tuka (random) nahi hai.
* **Calculation ka Basis:** Ye score baaki sabhi checks (Schema, Conflicts, Stability, Hardware bounds) ko mila kar mathematically average nikalta hai. Agar saare checks bilkul perfect aur harmonious hain, toh score 100% hota hai.

### 3. 🏎️ AVG DRIFT SCORE (0.12)
* **Matlab:** Script ki demand se Bhatkav (Bhatakne ki matra).
* **Ye kya batata hai:** Drift ka matlab hai AI original story ki feeling se kitna door nikal gaya. "0.12" ek bohot chota number (low drift) hai, iska matlab hai AI kahani par focus tha, apni marzi se hallucinate nahi kar raha tha ya unnecessary lights nahi daal raha tha (0.00 = No drift at all, perfectly aligned).
* **Calculation ka Basis:** Phase 2 (Emotion analyzer) se aayi hui emotional probabilities ki value aur Phase 4 ke actual lighting output parameters ki intensity values ke bich ki mathematical duri (variance aur standard deviations) nikal kar ye number banta hai.

### 4. ⚔️ CONFLICTS (0)
* **Matlab:** Takrav ya Clash.
* **Ye kya batata hai:** `0` Conflicts ka matlab hai ki pure script ki lighting me koi bhi rules break nahi hue hain. Koi do aisi light ek-saath cross nahi kar rahi jo nahi karni chahiye (jaise stage par ek hi jagah soft warm amber aur hard cold blue ka achanak se flash ho jana bina kisi transition ke).
* **Calculation ka Basis:** Evaluator system jab generated cues ko parta hai, toh wo Phase 3 Knowledge Base me feed kiye gaye "Lighting Design Rules" aur "Hardware limitations" se in cues ko compare karta hai. Agar dono match hote hain bina clash ke, to conflict 0 rehta hai.

### 5. 🔄 TRANSITIONS (1)
* **Matlab:** Scene ya light mood ka badalna (Shift hona).
* **Ye kya batata hai:** Transitions ka matlab hai ek major lighting state se dusri lighting state me smooth badlaav. `1` transition ka matlab hai in 4 scenes ke dauran ek baar lights ka mood ya setup clearly aur beautifully change hua hai.
* **Calculation ka Basis:** Lighting state objects ke alag-alag paramters, jaise intensity aur colors, pichle time-window se kitne time me shift ho rahe hain (Fade durations wagera read karke calculate hota hai).

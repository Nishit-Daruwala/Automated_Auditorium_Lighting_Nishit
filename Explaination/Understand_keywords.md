# 🎭 Lumina Intelligence: 8-Check System (Simple Terms)

Yeh sabhi keywords (SCH, HRD, CFT, etc.) Lumina pipeline ke **Phase 7 (Evaluation/Checking Phase)** ke metrics hain. 

Jab AI kisi scene ke liye lighting generate karta hai, to ye system 8 alag-alag ahem "Checks" (tests) karta hai taaki light ekdam perfect ho aur real auditorium me bina kisi error ke chale. 

Har check ka ek specific kaam hai. Chaliye inhe ekdam aasan bhasha me samajhte hain:

### 1. [SCH] - Schema Check 📝
* **Matlab:** Formatting / Structure Check
* **Kis kaam ka hai:** Ye check karta hai ki AI ne jo lighting ka code ya format diya hai, wo sahi JSON structure me hai ya nahi.
* **Kyu liya gaya:** Agar format galat hua to system aage crash ho sakta hai. Isse ensure hota hai ki result ek machine-readable format me hai.
* **Basis of calculate:** Code/JSON ka structure match kiya jata hai pre-defined rules (Scene Schema) ke sath.

### 2. [HRD] - Hierarchy / Hardware Limits 🏢
* **Matlab:** System Hierarchy and Hardware Capabilities Check
* **Kis kaam ka hai:** Ye check karta hai ki kya generated lighting values auditorium ke actual lights (hardware/DMX limits) ko support karti hain, aur kya emotional restrictions (hierarchy) follow ho rahi hai.
* **Kyu liya gaya:** Taaki AI aisi value na de de jo real lights me possible hi na ho (jaise kisi light ki intensity uski physically set limit se zyada kar dena).
* **Basis of calculate:** Apne knowledge base me jo actual fixture aur system limits save hain, unse AI ki output values ko compare kiya jata hai.

### 3. [CFT] - Conflict Check ⚔️
* **Matlab:** Clash ya Takrav Check
* **Kis kaam ka hai:** Dekhta hai ki kahin do alag-alag lights ya settings ek dusre se takra to nahi rahi. (Jaise ek sath stage par 'Warm Yellow' aur 'Cold Blue' mix ho jana bina kisi transition ke).
* **Kyu liya gaya:** Stage par colors, intensities ya movement mix up na ho aur artistic lighting clear aur logical bane.
* **Basis of calculate:** Lighting rules and design semantics ko base maan kar logical conflicts detect kiye jate hain.

### 4. [STB] - Stability Check 🏗️
* **Matlab:** Sthirta (Consistency) Check
* **Kis kaam ka hai:** Ensure karta hai ki background me achanak se koi faaltu ke lighting state changes ya flickers na ho. (Stable rehne wali lights ekdam se band/chalu na ho).
* **Kyu liya gaya:** Audience ko comfortable experience dene ke liye; taaki visual transitions smooth aur thande hon.
* **Basis of calculate:** Pichle scene/step ke lighting state (output) ko is naye output se compare kiya jata hai (Transition score & variance).

### 5. [DRF] - Drift Status 🏎️
* **Matlab:** Phatkav (Raste se bhatakne) ka Check
* **Kis kaam ka hai:** Ye test karta hai ki AI original script aur emotion se kitna door chala gaya hai (kahin drift to nahi ho raha). 
* **Kyu liya gaya:** Taaki AI hallucinate karke (apni marzi se) random heavy lights assign na karne lage, balki strictly story vibe ke hisab se hi chale.
* **Basis of calculate:** AI ke final output ko original script ki tone aur emotional probability se mathematically calculate (variance & drift score) kiya jata hai.

### 6. [CNF] - Confidence Check 🎯
* **Matlab:** AI ki Surety Check
* **Kis kaam ka hai:** AI khud kitna confident (sure) hai apne laye gaye lighting faislon ko lekar.
* **Kyu liya gaya:** Agar AI ki certainty low hai (kisi confusing line ke chalte), to hume pehle hi warn (Warning) mil jaye taki hum use manual review kar saken.
* **Basis of calculate:** Phase 2 ke Model outputs (Language Model probabilities aur emotion prediction scores).

### 7. [NAR] - Narrative Validation 📖
* **Matlab:** Story-line Alignment
* **Kis kaam ka hai:** Ye clear karta hai ki light cues story ke pace, tension, aur scene-to-scene flow ke hisab se chal rahe hain ya nahi.
* **Kyu liya gaya:** Ek quiet, sad scene ke baad directly aggressive bright lights na aa jaye jab tak waisa likha na ho. Kahani ki continuity barkaraar rakhne ke liye.
* **Basis of calculate:** Puraane scene aur immediate next scene ki energy levels & timestamps analyze karke.

### 8. [COH] - Coherence Score 🧠
* **Matlab:** Overall Logic & Quality Score
* **Kis kaam ka hai:** Ye ek ultimate combined mark (score) hai jo batata hai ki upper ke saare checks ko mila kar actual outcome kitna solid hai.
* **Kyu liya gaya:** Taki human user ko har baar details na dekhni pade aur single number/percentage se pata chal sake ki scene 'PASS' hai, 'WARN' hai, ya 'FAIL' hai.
* **Basis of calculate:** Upar wale sabhi metrics (SCH, HRD, CFT, DRF aadi) ki value mila ke ek average math fraction calculate hota hai, jise percentage (0% to 100%) scale me dikhaya jata hai.

---
### Hume inn sab se kya milta hai?
In saare checks ka real-time dashboard me hone ka fayda ye hai ki hame **bina actual show kiye ya script padhe** ek guarantee mil jati hai ki AI ka generate kiya hua lighting design bilkul **safe**, **beautiful**, aur **hardware pe chalne layak** hai. 

Inme se agar koi check "FAIL" ya "WARN" red flag dikhata hai, to pipeline human-director ko turant bata degi ke is particular line pe review chahiye, saving tons of time and money in real rehearsals!

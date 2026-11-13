"""Veterinary Medical Sources Registry.

Contains authentic, verified citations from Merck Veterinary Manual,
Cornell University College of Veterinary Medicine, VCA Animal Hospitals,
Veterinary Partner (VIN), AAHA, AVMA, and PubMed peer-reviewed veterinary literature.
"""
from typing import Dict, List
from backend.models.condition import SourceReference

SOURCES: Dict[str, List[SourceReference]] = {
    # ========================== CAT SOURCES ==========================
    "CAT_001": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Inflammatory Bowel Disease",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-inflammatory-bowel-disease",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Chronic vomiting, diarrhea, and weight loss are hallmark signs.",
                "Etiology involves mucosal immunity dysregulation and intestinal microbiome alterations.",
                "Definitive diagnosis requires intestinal mucosal biopsy and histopathology to rule out intestinal lymphoma."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Inflammatory Bowel Disease in Small Animals",
            url="https://www.merckvetmanual.com/digestive-system/diseases-of-the-stomach-and-intestines-in-small-animals/inflammatory-bowel-disease-in-small-animals",
            author="Jergens, A. E., DVM, PhD, DACVIM",
            publication_date="2022",
            claims_supported=[
                "Clinical disease is chronic (>3 weeks) with variable appetite and weight loss.",
                "Exclusionary workup requires fecal flotation, dietary trials, and abdominal ultrasonography."
            ]
        )
    ],
    "CAT_002": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Pancreatitis",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-pancreatitis",
            author="Cornell Feline Health Center Staff",
            publication_date="2022",
            claims_supported=[
                "Signs are often subtle: lethargy, anorexia, and dehydration rather than overt vomiting or abdominal pain.",
                "Serum fPLI (feline pancreatic lipase immunoreactivity) is the sensitive specific biomarker."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Pancreatitis in Cats",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951817",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Frequently associated with feline triaditis (concurrent IBD and cholangiohepatitis).",
                "Severe acute pancreatitis requires intensive fluid resuscitation and analgesia."
            ]
        )
    ],
    "CAT_003": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Constipation and Obstipation in Small Animals",
            url="https://www.merckvetmanual.com/digestive-system/diseases-of-the-large-intestine-in-small-animals/constipation-and-obstipation-in-small-animals",
            author="Washabau, R. J., VMD, PhD, DACVIM",
            publication_date="2022",
            claims_supported=[
                "Characterized by absent, infrequent, or painful defecation with hard, dry feces.",
                "Recurrent untreated constipation risks progression to irreversible megacolon."
            ]
        ),
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Constipation in Cats",
            url="https://vcahospitals.com/know-your-pet/constipation-in-cats",
            author="Weir, M., DVM; Downing, R., DVM, DAAPM, DACVSMR",
            publication_date="2023",
            claims_supported=[
                "Straining in the litter box may mimic feline urethral obstruction, requiring immediate palpation.",
                "Dehydration is a leading trigger in elderly cats with kidney disease."
            ]
        )
    ],
    "CAT_004": [
        SourceReference(
            organization="Companion Animal Parasite Council (CAPC)",
            title="Feline Gastrointestinal Parasites Guideline",
            url="https://capcvet.org/guidelines/feline-gastrointestinal-parasites/",
            author="CAPC Expert Scientific Panel",
            publication_date="2023",
            claims_supported=[
                "Common parasites include Toxocara cati, Ancylostoma tubaeforme, and Giardia duodenalis.",
                "Kittens present with pot-bellied appearance, dull haircoat, mucoid diarrhea, and poor growth."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Gastrointestinal Parasites of Cats",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/gastrointestinal-parasites-cats",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Diagnosis via centrifugal fecal flotation; some helminths (roundworms/tapeworm segments) visible grossly in vomit/stool."
            ]
        )
    ],
    "CAT_005": [
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Flea Allergy Dermatitis in Cats",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951398",
            author="Brooks, W., DVM, DABVP",
            publication_date="2022",
            claims_supported=[
                "Severe hypersensitivity to flea salivary antigens causing intense caudal, neck, and lumbosacral pruritus.",
                "Characteristic presentation is miliary dermatitis (scabby crusts) and symmetrical alopecia from overgrooming."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Flea Allergy Dermatitis",
            url="https://www.merckvetmanual.com/integumentary-system/fleas-and-flea-allergy-dermatitis/flea-allergy-dermatitis",
            author="Dryden, M. W., DVM, PhD, DACVM",
            publication_date="2022",
            claims_supported=[
                "Flea dirt or live fleas may not be visible due to vigorous feline grooming; trial flea control is diagnostic."
            ]
        )
    ],
    "CAT_006": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Ringworm (Dermatophytosis) in Cats",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/ringworm-serious-readily-transmissible-affliction",
            author="Cornell Feline Health Center Staff",
            publication_date="2022",
            claims_supported=[
                "Fungal infection predominantly caused by Microsporum canis; highly contagious and zoonotic.",
                "Circular patches of alopecia with scaling, crusting, and broken hair shafts, commonly on face, ears, and paws."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Dermatophytosis in Dogs and Cats",
            url="https://www.merckvetmanual.com/integumentary-system/dermatophytosis/dermatophytosis-in-dogs-and-cats",
            author="Moriello, K. A., DVM, DACVD",
            publication_date="2023",
            claims_supported=[
                "Wood's lamp examination detects green fluorescence in ~50% of M. canis strains; fungal culture or PCR confirms."
            ]
        )
    ],
    "CAT_007": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Feline Eosinophilic Granuloma Complex",
            url="https://www.merckvetmanual.com/integumentary-system/eosinophilic-granuloma-complex/feline-eosinophilic-granuloma-complex",
            author="Noli, C., DVM, PhD, ECVD",
            publication_date="2022",
            claims_supported=[
                "Reaction pattern encompassing indolent (rodent) ulcers, eosinophilic plaques, and linear collagenolytic granulomas.",
                "Commonly secondary to underlying flea, food, or environmental hypersensitivity."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Eosinophilic Granuloma Complex in Cats",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951528",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Indolent ulcers typically affect the upper lip without overt pain; eosinophilic plaques present as glistening pruritic abdominal/thigh lesions."
            ]
        )
    ],
    "CAT_008": [
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Food Allergies in Cats",
            url="https://vcahospitals.com/know-your-pet/food-allergies-in-cats",
            author="Weir, M., DVM; Downing, R., DVM",
            publication_date="2023",
            claims_supported=[
                "Non-seasonal pruritus focused on face, head, and neck; often refractory to glucocorticoids.",
                "Diagnosis confirmed strictly via an 8-12 week strict elimination diet trial using hydrolyzed or novel protein."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Cutaneous Adverse Food Reactions in Animals",
            url="https://www.merckvetmanual.com/integumentary-system/food-allergy/cutaneous-adverse-food-reactions-in-animals",
            author="Marsella, R., DVM, DACVD",
            publication_date="2023",
            claims_supported=[
                "Concurrent gastrointestinal signs (vomiting, soft stool) occur in 10-30% of affected feline cases."
            ]
        )
    ],
    "CAT_009": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Asthma: What You Need to Know",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-asthma-what-you-need-know",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Chronic inflammatory lower airway disease leading to bronchoconstriction, coughing, and wheezing.",
                "Posture during attacks involves crouching low to ground with neck extended and open-mouth panting (acute emergency)."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Chronic Bronchial Disease in Cats (Feline Asthma)",
            url="https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-small-animals/chronic-bronchial-disease-in-cats",
            author="Reinero, C. R., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Thoracic radiographs demonstrate bronchial wall thickening ('doughnuts' and 'tramlines') and lung hyperinflation."
            ]
        )
    ],
    "CAT_010": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Upper Respiratory Infections (FHV-1)",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-respiratory-infections",
            author="Cornell Feline Health Center Staff",
            publication_date="2022",
            claims_supported=[
                "FHV-1 causes severe rhinitis, sneezing, conjunctivitis, blepharospasm, and characteristic dendritic corneal ulcers.",
                "Lifelong latency established in trigeminal ganglia with recrudescence during periods of physiological or environmental stress."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Feline Respiratory Disease Complex",
            url="https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-small-animals/feline-respiratory-disease-complex",
            author="Sykes, J. E., BVSc, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "High morbidity in shelters and catteries; fever, profuse purulent oculonasal discharge, and inappetence are common."
            ]
        )
    ],
    "CAT_011": [
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Feline Calicivirus Infection",
            url="https://vcahospitals.com/know-your-pet/feline-calicivirus-infection",
            author="Ward, E., DVM; Panning, A., DVM",
            publication_date="2022",
            claims_supported=[
                "Prominent painful oral ulcerations on tongue, hard palate, and lips leading to severe hypersalivation and anorexia.",
                "Some strains induce acute self-limiting limping syndrome (viral synovitis) in young kittens."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Feline Calicivirus",
            url="https://www.merckvetmanual.com/generalized-conditions/feline-calicivirus/feline-calicivirus",
            author="Hurley, K. E., DVM, MPVM",
            publication_date="2023",
            claims_supported=[
                "Virulent systemic FCV (VS-FCV) can cause high mortality with facial edema, icterus, and hemorrhagic diathesis."
            ]
        )
    ],
    "CAT_012": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Pneumonia in Small Animals",
            url="https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-small-animals/pneumonia-in-small-animals",
            author="Dear, J. D., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Causes include aspiration, secondary bacterial infection, fungal, and protozoal pathogens.",
                "Presents with tachypnea, dyspnea, moist crackles on thoracic auscultation, pyrexia, and deep productive cough."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Bacterial Pneumonia in Cats and Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4952814",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Chest radiographs reveal alveolar lung infiltrates; pulse oximetry or arterial blood gas is vital in dyspneic patients."
            ]
        )
    ],
    "CAT_013": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Idiopathic Cystitis",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-idiopathic-cystitis",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Complex neuroendocrine-bladder disorder characterized by periuria, pollakiuria, hematuria, and stranguria.",
                "Sterile inflammatory process triggered by environmental stressors in cats with exaggerated central sympathetic drive."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Feline Idiopathic Cystitis (FIC)",
            url="https://www.merckvetmanual.com/urinary-system/noninfectious-diseases-of-the-urinary-tract-in-small-animals/feline-idiopathic-cystitis",
            author="Bartges, J. W., DVM, PhD, DACVIM, DACVN",
            publication_date="2023",
            claims_supported=[
                "Diagnosis of exclusion in non-obstructed cats after ruling out urolithiasis, bacterial UTI, and anatomical neoplasia."
            ]
        )
    ],
    "CAT_014": [
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Urinary Obstruction in Cats",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951487",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "True life-threatening emergency predominantly affecting male cats due to narrow penile urethra.",
                "Inability to pass urine leads to fatal post-renal azotemia, hyperkalemia, and cardiac arrest within 24-48 hours.",
                "Patient vocalizes in litter box with painful, firm, distended, non-expressible urinary bladder."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Urethral Obstruction in Small Animals",
            url="https://www.merckvetmanual.com/urinary-system/noninfectious-diseases-of-the-urinary-tract-in-small-animals/urethral-obstruction-in-small-animals",
            author="Grauer, G. F., DVM, MS, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Requires immediate emergency urethral catheterization, stabilization, and IV fluid correction of hyperkalemia."
            ]
        )
    ],
    "CAT_015": [
        SourceReference(
            organization="International Renal Interest Society (IRIS)",
            title="IRIS Staging of Feline Chronic Kidney Disease",
            url="http://www.iris-kidney.com/guidelines/staging.html",
            author="IRIS Board of Directors",
            publication_date="2023",
            claims_supported=[
                "Staging based on persistent fasting blood creatinine, symmetric dimethylarginine (SDMA), and proteinuria/blood pressure.",
                "Early clinical signs include polydipsia, polyuria, weight loss, and inappetence."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Chronic Kidney Disease in Cats",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/chronic-kidney-disease",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Affects over 30% of geriatric cats; management focuses on phosphate restriction, renal diet, hydration, and blood pressure control."
            ]
        )
    ],
    "CAT_016": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Urolithiasis in Small Animals",
            url="https://www.merckvetmanual.com/urinary-system/noninfectious-diseases-of-the-urinary-tract-in-small-animals/urolithiasis-in-small-animals",
            author="Lulich, J. P., DVM, PhD, DACVIM",
            publication_date="2022",
            claims_supported=[
                "Calcium oxalate and struvite represent >90% of feline bladder stones.",
                "Clinical signs include hematuria, pollakiuria, and dysuria; can cause life-threatening urethral obstruction in males."
            ]
        ),
        SourceReference(
            organization="Minnesota Urolith Center",
            title="Feline Urolithiasis Recommendations",
            url="https://www.vetmed.umn.edu/centers-programs/minnesota-urolith-center",
            author="Osborne, C. A., DVM, PhD",
            publication_date="2023",
            claims_supported=[
                "Diagnosis confirmed via abdominal radiography and ultrasonography; struvite may dissolve medically while calcium oxalate requires removal."
            ]
        )
    ],
    "CAT_017": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Conjunctivitis in Cats",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/conjunctivitis",
            author="Cornell Feline Health Center Staff",
            publication_date="2022",
            claims_supported=[
                "Primary causes in cats are infectious: FHV-1, Chlamydia felis, Mycoplasma felis, and Calicivirus.",
                "Presents with chemosis, hyperemia, blepharospasm, and serous to mucopurulent ocular discharge."
            ]
        ),
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Conjunctivitis in Cats",
            url="https://vcahospitals.com/know-your-pet/conjunctivitis-in-cats",
            author="Williams, K., DVM; Yuill, C., DVM, MS",
            publication_date="2023",
            claims_supported=[
                "Fluorescein stain is mandatory before topical steroid administration to rule out corneal ulceration."
            ]
        )
    ],
    "CAT_018": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Corneal Ulcers in Animals",
            url="https://www.merckvetmanual.com/eye-diseases-and-disorders/corneal-diseases-in-small-animals/corneal-ulcers-in-small-animals",
            author="Ledbetter, E. C., DVM, DACVO",
            publication_date="2023",
            claims_supported=[
                "Loss of corneal epithelial and stroma layers, frequently initiated by trauma, foreign bodies, or FHV-1 infection.",
                "Manifests with intense ocular pain, blepharospasm, epiphora, photophobia, and corneal cloudiness/edema."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Corneal Ulcers in Dogs and Cats",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951478",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Fluorescein dye retention confirms diagnosis; deep or descemetocele ulcers require emergency surgical stabilization."
            ]
        )
    ],
    "CAT_019": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Otitis Externa in Cats",
            url="https://www.merckvetmanual.com/ear-disorders/otitis-externa/otitis-externa-in-cats",
            author="Rosychuk, R. A., DVM, DACVD",
            publication_date="2022",
            claims_supported=[
                "Ear mite infestation (Otodectes cynotis) accounts for >50% of feline cases, presenting with dry 'coffee ground' cerumen.",
                "Head shaking, pinnal scratching, odor, erythema, and aural hematoma formation are classic clinical signs."
            ]
        ),
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Otitis Externa in Cats",
            url="https://vcahospitals.com/know-your-pet/ear-infections-in-cats-otitis-externa",
            author="Weir, M., DVM; Ward, E., DVM",
            publication_date="2023",
            claims_supported=[
                "Ear cytology is mandatory to identify mites, Malassezia yeast, or secondary bacterial overgrowth."
            ]
        )
    ],
    "CAT_020": [
        SourceReference(
            organization="American Association of Feline Practitioners (AAFP)",
            title="AAFP Guidelines for the Management of Feline Diabetes Mellitus",
            url="https://catvets.com/guidelines/practice-guidelines/diabetes-management-guidelines",
            author="AAFP Advisory Panel",
            publication_date="2023",
            claims_supported=[
                "Predominantly type 2-like pathophysiology with peripheral insulin resistance and beta-cell amyloid deposition.",
                "Classic tetrad: polyuria, polydipsia, polyphagia, and rapid weight loss; plantigrade stance occurs with diabetic neuropathy."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Diabetes",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-diabetes",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Diagnosis confirmed by persistent hyperglycemia and glucosuria, differentiated from stress hyperglycemia via serum fructosamine."
            ]
        )
    ],
    "CAT_021": [
        SourceReference(
            organization="American Association of Feline Practitioners (AAFP)",
            title="AAFP Guidelines for the Management of Feline Hyperthyroidism",
            url="https://catvets.com/guidelines/practice-guidelines/hyperthyroidism-guidelines",
            author="Carney, H. C., DVM, DABVP; et al.",
            publication_date="2022",
            claims_supported=[
                "Most common feline endocrine disorder, caused by functional adenoma or multinodular hyperplasia of thyroid gland.",
                "Hallmark triad in older cats: marked weight loss despite ravenous appetite (polyphagia), hyperactivity, and tachycardia."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Hyperthyroidism in Cats",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/hyperthyroidism-cats",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Elevated total thyroxine (total T4) confirms diagnosis; can unmask occult chronic kidney disease upon treatment."
            ]
        )
    ],
    "CAT_022": [
        SourceReference(
            organization="AAFP / EveryCat Health Foundation",
            title="AAFP Feline Retrovirus Testing and Management Guidelines",
            url="https://catvets.com/guidelines/practice-guidelines/retrovirus-management-guidelines",
            author="Little, S., DVM, DABVP; et al.",
            publication_date="2023",
            claims_supported=[
                "Retrovirus transmitted via saliva through mutual grooming, bite wounds, and vertical transmission.",
                "Progressive infection induces profound immunosuppression, persistent cytopenias, and lymphoid malignancies."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Leukemia Virus",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-leukemia-virus",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Point-of-care ELISA detects p27 viral capsular antigen in peripheral blood."
            ]
        )
    ],
    "CAT_023": [
        SourceReference(
            organization="American Association of Feline Practitioners (AAFP)",
            title="Feline Immunodeficiency Virus Educational Compendium",
            url="https://catvets.com/guidelines/practice-guidelines/retrovirus-management-guidelines",
            author="AAFP Feline Retrovirus Committee",
            publication_date="2022",
            claims_supported=[
                "Lentivirus primarily transmitted via deep bite wounds in outdoor intact male cats.",
                "Chronic progressive loss of CD4+ T-lymphocytes predisposing to recurrent infections, chronic stomatitis, and wasting."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Immunodeficiency Virus (FIV)",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-immunodeficiency-virus-fiv",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Diagnosis via point-of-care antibody detection; antibodies indicate lifelong persistent infection in adult cats."
            ]
        )
    ],
    "CAT_024": [
        SourceReference(
            organization="EveryCat Health Foundation",
            title="Feline Infectious Peritonitis Diagnosis and Management",
            url="https://everycat.org/research/fip-resources/",
            author="Pedersen, N. C., DVM, PhD",
            publication_date="2023",
            claims_supported=[
                "Immune-mediated vasculitis triggered by systemic mutation of ubiquitous feline enteric coronavirus (FCoV).",
                "Effusive (wet) form causes high-protein straw-colored peritoneal/pleural effusion; dry form causes pyogranulomatous lesions.",
                "Persistent antibiotic-refractory pyrexia, progressive weight loss, jaundice, and lethargy are typical."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Infectious Peritonitis",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-infectious-peritonitis",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Rivalta test, high serum globulins with low A:G ratio (<0.6), and FCoV RT-PCR on effusion support diagnosis."
            ]
        )
    ],
    "CAT_025": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Feline Panleukopenia",
            url="https://www.merckvetmanual.com/generalized-conditions/feline-panleukopenia/feline-panleukopenia",
            author="Truyen, U., DVM, PhD",
            publication_date="2023",
            claims_supported=[
                "Parvoviral infection targeting rapidly dividing cells in intestinal crypts, bone marrow, and lymphoid tissue.",
                "Peracute to acute onset of high fever, profound dehydration, intractable vomiting, hemorrhagic diarrhea, and severe leukopenia.",
                "High mortality rate in unvaccinated kittens; requires immediate aggressive barrier nursing and isolation."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Feline Panleukopenia (Feline Distemper)",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951475",
            author="Brooks, W., DVM, DABVP",
            publication_date="2022",
            claims_supported=[
                "Can be detected in fresh feces using canine parvovirus antigen test kits; profound panleukopenia on complete blood count."
            ]
        )
    ],
    "CAT_026": [
        SourceReference(
            organization="Association for Pet Obesity Prevention (APOP)",
            title="Pet Obesity Prevalence and Health Risks Survey",
            url="https://www.petobesityprevention.org/",
            author="Ward, E., DVM; APOP Board",
            publication_date="2023",
            claims_supported=[
                "Defined as body weight >20% above ideal, corresponding to Body Condition Score (BCS) 8/9 or 9/9.",
                "Major predisposing risk factor for feline diabetes mellitus, hepatic lipidosis, osteoarthritis, and lower urinary tract disease."
            ]
        ),
        SourceReference(
            organization="AAHA",
            title="AAHA Weight Management Guidelines for Dogs and Cats",
            url="https://www.aaha.org/aaha-guidelines/weight-management-configuration/weight-management-guidelines/",
            author="AAHA Weight Management Task Force",
            publication_date="2022",
            claims_supported=[
                "Excessive adipose tissue acts as an endocrine organ secreting pro-inflammatory cytokines; requires gradual safe caloric restriction."
            ]
        )
    ],
    "CAT_027": [
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Hepatic Lipidosis (Fatty Liver Disease)",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/hepatic-lipidosis",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Occurs when an overweight cat undergoes sudden prolonged anorexia (>2-7 days), mobilizing peripheral triglycerides to hepatocytes.",
                "Signs include severe icterus (jaundice), lethargy, persistent vomiting, dramatic weight loss, and hepatic encephalopathy.",
                "Primary treatment is aggressive enteral nutritional support via esophageal or gastrostomy feeding tube."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Hepatic Lipidosis in Cats",
            url="https://www.merckvetmanual.com/digestive-system/hepatic-disease-in-small-animals/hepatic-lipidosis-in-cats",
            author="Center, S. A., DVM, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Marked serum ALP elevation with normal or only mildly elevated GGT is highly characteristic."
            ]
        )
    ],
    "CAT_028": [
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Feline Chronic Gingivostomatitis",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951804",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Severe, debilitating, chronic immune-mediated inflammation of gingiva, caudal oral mucosa, and glossopalatine arches.",
                "Clinical signs: intense oral pain, ptysalism, pawing at mouth, head shyness, vocalizing when attempting to eat, and weight loss."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Feline Gingivostomatitis",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/feline-gingivostomatitis",
            author="Cornell Feline Health Center Staff",
            publication_date="2022",
            claims_supported=[
                "Full-mouth or partial-mouth caudal dental extractions achieve clinical cure or substantial remission in ~70-80% of cases."
            ]
        )
    ],
    "CAT_029": [
        SourceReference(
            organization="American Veterinary Dental College (AVDC)",
            title="Feline Tooth Resorption Classification and Staging",
            url="https://avdc.org/feline-tooth-resorption/",
            author="AVDC Clinical Standards Committee",
            publication_date="2022",
            claims_supported=[
                "Odontoclastic destruction of dental hard tissue, commonly originating at the cementoenamel junction.",
                "Affected cats demonstrate chattering jaw movements when lesions are touched, drooling, dysphagia, and food dropping."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Tooth Resorption in Small Animals",
            url="https://www.merckvetmanual.com/digestive-system/dentistry/tooth-resorption-in-small-animals",
            author="Bellows, J., DVM, DAVDC, DABVP",
            publication_date="2023",
            claims_supported=[
                "Definitive staging and surgical extraction planning require full-mouth intraoral dental radiographs under general anesthesia."
            ]
        )
    ],
    "CAT_030": [
        SourceReference(
            organization="American College of Veterinary Internal Medicine (ACVIM)",
            title="ACVIM Consensus Statement: Feline Cardiomyopathies",
            url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7214300/",
            author="Luis Fuentes, V., et al.",
            publication_date="2020",
            claims_supported=[
                "Most prevalent cardiac disease in cats; concentric left ventricular hypertrophy leading to diastolic dysfunction.",
                "Can remain clinically silent until sudden onset of congestive heart failure (pulmonary edema) or aortic thromboembolism (FATE).",
                "FATE presentation: sudden screaming, excruciating pain, and acute paraparesis with cold, pulseless hindlimbs (critical emergency)."
            ]
        ),
        SourceReference(
            organization="Cornell University College of Veterinary Medicine",
            title="Hypertrophic Cardiomyopathy",
            url="https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/hypertrophic-cardiomyopathy",
            author="Cornell Feline Health Center Staff",
            publication_date="2023",
            claims_supported=[
                "Echocardiography is the gold standard diagnostic tool showing left ventricular wall thickness >=6 mm."
            ]
        )
    ],

    # ========================== DOG SOURCES ==========================
    "DOG_001": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Gastritis in Small Animals",
            url="https://www.merckvetmanual.com/digestive-system/diseases-of-the-stomach-and-intestines-in-small-animals/gastritis-in-small-animals",
            author="Simpson, K. W., BVM&S, PhD, DACVIM",
            publication_date="2022",
            claims_supported=[
                "Acute gastritis is commonly initiated by dietary indiscretion ('garbage gut'), foreign materials, or systemic toxins.",
                "Presents with acute vomiting, abdominal discomfort, dehydration, and variable inappetence."
            ]
        ),
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Gastritis in Dogs",
            url="https://vcahospitals.com/know-your-pet/gastritis-in-dogs",
            author="Williams, K., DVM; Ward, E., DVM",
            publication_date="2023",
            claims_supported=[
                "Self-limiting cases respond to short fast followed by bland diet; persistent or hematemetic cases require veterinary intervention."
            ]
        )
    ],
    "DOG_002": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Inflammatory Bowel Disease in Dogs",
            url="https://www.merckvetmanual.com/digestive-system/diseases-of-the-stomach-and-intestines-in-small-animals/inflammatory-bowel-disease-in-small-animals",
            author="Jergens, A. E., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Chronic mucosal inflammation (lymphocytic-plasmacytic enteritis) causing recurrent vomiting, diarrhea, and weight loss.",
                "Requires exclusion of endoparasitism, dietary hypersensitivity, and hypocobalaminemia before biopsy."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Inflammatory Bowel Disease in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951397",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Hypoalbuminemia can develop in severe protein-losing enteropathy (PLE) forms, requiring intensive oncotic management."
            ]
        )
    ],
    "DOG_003": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Pancreatitis in Dogs",
            url="https://www.merckvetmanual.com/digestive-system/the-exocrine-pancreas/pancreatitis-in-dogs",
            author="Steiner, J. M., med. vet., PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Autodigestion of pancreatic tissue triggered frequently by high-fat dietary indiscretion.",
                "Hallmark signs: sudden vomiting, severe cranial abdominal pain ('prayer position' stretching), pyrexia, and lethargy.",
                "Canine specific pancreatic lipase (cPL / Spec cPL) is the test of choice."
            ]
        ),
        SourceReference(
            organization="American Animal Hospital Association (AAHA)",
            title="Pancreatitis Overview in Canine Patients",
            url="https://www.aaha.org/publications/newstat/articles/2021-08/pancreatitis-in-dogs/",
            author="AAHA Clinical Editors",
            publication_date="2022",
            claims_supported=[
                "Requires intravenous balanced isotonic crystalloids, multimodal analgesia (opioids), and early enteral nutrition."
            ]
        )
    ],
    "DOG_004": [
        SourceReference(
            organization="American College of Veterinary Surgeons (ACVS)",
            title="Gastric Dilatation-Volvulus (GDV)",
            url="https://www.acvs.org/small-animal/gastric-dilatation-volvulus",
            author="ACVS Board of Regents",
            publication_date="2023",
            claims_supported=[
                "Life-threatening peracute surgical emergency primarily in deep-chested large/giant breeds.",
                "Stomach distends with gas and rotates on its mesenteric axis, obstructing venous return and causing obstructive shock.",
                "Triad of hallmark signs: non-productive retching/retching without vomitus, tympanic abdominal distension, and restlessness/collapse."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Gastric Dilation and Volvulus in Small Animals",
            url="https://www.merckvetmanual.com/digestive-system/diseases-of-the-stomach-and-intestines-in-small-animals/gastric-dilation-and-volvulus-in-small-animals",
            author="Monnet, E., DVM, PhD, DACVS",
            publication_date="2023",
            claims_supported=[
                "Immediate decompression (trocharization/orogastric tube), shock fluid resuscitation, and emergency gastropexy are required."
            ]
        )
    ],
    "DOG_005": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Exocrine Pancreatic Insufficiency in Dogs and Cats",
            url="https://www.merckvetmanual.com/digestive-system/the-exocrine-pancreas/exocrine-pancreatic-insufficiency-in-dogs-and-cats",
            author="Steiner, J. M., med. vet., PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Caused by pancreatic acinar atrophy (predominantly in German Shepherd Dogs) leading to lack of digestive enzymes.",
                "Hallmark triad: massive voluminous yellow/clay-colored steatorrheic diarrhea, severe polyphagia, and marked progressive weight loss.",
                "Serum trypsin-like immunoreactivity (cTLI) <= 2.5 ug/L is diagnostic."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Exocrine Pancreatic Insufficiency (EPI)",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951468",
            author="Brooks, W., DVM, DABVP",
            publication_date="2022",
            claims_supported=[
                "Treated with lifelong dietary pancreatic enzyme replacement powder and parenteral cobalamin supplementation."
            ]
        )
    ],
    "DOG_006": [
        SourceReference(
            organization="International Committee on Allergic Diseases of Animals (ICADA)",
            title="Canine Atopic Dermatitis Guidelines",
            url="https://icada.org/guidelines/",
            author="Olivry, T., DrVet, PhD, DECVD; et al.",
            publication_date="2022",
            claims_supported=[
                "Genetically predisposed inflammatory and pruritic allergic skin disease associated with IgE to environmental allergens.",
                "Characteristic distribution: face, pinnae, ventral abdomen, axillae, perineum, and interdigital pedal spaces (paw licking).",
                "Favrot's diagnostic criteria emphasize onset under 3 years of age, indoor lifestyle, corticosteroid responsiveness, and chronic recurrence."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Atopic Dermatitis in Dogs",
            url="https://www.merckvetmanual.com/integumentary-system/atopic-dermatitis/atopic-dermatitis-in-dogs",
            author="Hensel, P., Dr.med.vet., DACVD",
            publication_date="2023",
            claims_supported=[
                "Secondary bacterial (Staphylococcus) and Malassezia yeast overgrowths are exceedingly common complications."
            ]
        )
    ],
    "DOG_007": [
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Flea Allergy Dermatitis in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951398",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Hypersensitivity to Ctenocephalides felis saliva; single flea bite can trigger unrelenting pruritus in sensitized dogs.",
                "Classic 'flea triangle' distribution: lumbosacral region, tail base, caudal thighs, and ventral groin."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Flea Allergy Dermatitis in Dogs and Cats",
            url="https://www.merckvetmanual.com/integumentary-system/fleas-and-flea-allergy-dermatitis/flea-allergy-dermatitis",
            author="Dryden, M. W., DVM, PhD, DACVM",
            publication_date="2022",
            claims_supported=[
                "Presence of flea dirt or live fleas supports diagnosis; strict continuous isoxazoline or topical preventative required."
            ]
        )
    ],
    "DOG_008": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Superficial Bacterial Pyoderma in Dogs",
            url="https://www.merckvetmanual.com/integumentary-system/pyoderma/superficial-pyoderma-in-dogs",
            author="White, S. D., DVM, DACVD",
            publication_date="2023",
            claims_supported=[
                "Bacterial infection of hair follicles (folliculitis) and epidermis, predominantly Staphylococcus pseudintermedius.",
                "Presents with erythematous papules, pustules, 'bulls-eye' epidermal collarettes, and focal alopecia with scaling.",
                "Nearly always secondary to underlying allergic, parasitic, or endocrine disease."
            ]
        ),
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Superficial Pyoderma in Dogs",
            url="https://vcahospitals.com/know-your-pet/pyoderma-in-dogs",
            author="Barnette, C., DVM; Ward, E., DVM",
            publication_date="2023",
            claims_supported=[
                "Tape-strip or impression smear cytology reveals degenerate neutrophils with intracellular cocci."
            ]
        )
    ],
    "DOG_009": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Demodicosis in Dogs",
            url="https://www.merckvetmanual.com/integumentary-system/demodicosis/demodicosis-in-dogs",
            author="Mueller, R. S., Dr.med.vet., DACVD, DECVD",
            publication_date="2023",
            claims_supported=[
                "Overproliferation of Demodex canis commensal follicular mites.",
                "Localized form (periocular/muzzle alopecia in young dogs) is typically non-pruritic and self-limiting.",
                "Generalized adult-onset form indicates severe underlying immunosuppression or endocrinopathy."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Demodectic Mange in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951505",
            author="Brooks, W., DVM, DABVP",
            publication_date="2022",
            claims_supported=[
                "Confirmed via deep skin scrapings squeezing hair follicles or trichograms showing cigar-shaped mites."
            ]
        )
    ],
    "DOG_010": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Sarcoptic Mange in Dogs",
            url="https://www.merckvetmanual.com/integumentary-system/mange/sarcoptic-mange-in-dogs",
            author="Mueller, R. S., Dr.med.vet., DACVD, DECVD",
            publication_date="2023",
            claims_supported=[
                "Intensely pruritic, contagious, and zoonotic infestation caused by Sarcoptes scabiei var canis burrowing mites.",
                "Distribution focuses on ear margins (pinnae), elbows (hocks), and ventral abdomen with scaling and crusting.",
                "Positive pinnal-pedal scratch reflex elicited in over 85% of clinical cases."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Sarcoptic Mange (Scabies) in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951399",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Mites are notoriously elusive on skin scrapes; therapeutic trial with isoxazolines is standard diagnostic strategy."
            ]
        )
    ],
    "DOG_011": [
        SourceReference(
            organization="American Animal Hospital Association (AAHA)",
            title="Canine Infectious Respiratory Disease Complex (CIRDC)",
            url="https://www.aaha.org/aaha-guidelines/canine-vaccination-guidelines/cirdc/",
            author="AAHA Canine Vaccination Task Force",
            publication_date="2022",
            claims_supported=[
                "Multifactorial syndrome (Bordetella bronchiseptica, canine parainfluenza, canine adenovirus-2).",
                "Hallmark sign is acute onset of loud, dry, harsh, honking paroxysmal cough, often followed by gagging or retching.",
                "Easily elicited tracheal palpation cough reflex in an otherwise bright, alert, afebrile dog."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Infectious Tracheobronchitis (Kennel Cough) in Dogs",
            url="https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-small-animals/tracheobronchitis-in-small-animals",
            author="Dear, J. D., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "History typically reveals recent exposure to boarding, dog parks, grooming facilities, or shelters 3-10 days prior."
            ]
        )
    ],
    "DOG_012": [
        SourceReference(
            organization="American College of Veterinary Surgeons (ACVS)",
            title="Tracheal Collapse in Dogs",
            url="https://www.acvs.org/small-animal/tracheal-collapse",
            author="ACVS Board of Regents",
            publication_date="2023",
            claims_supported=[
                "Progressive hypocellularity and loss of glycosaminoglycans in tracheal cartilaginous rings in toy/small breeds (Yorkie, Pomeranian).",
                "Classic 'goose-honk' cough exacerbated by excitement, collar pressure, exercise, heat, or humidity.",
                "Severe dynamic obstruction causes respiratory distress, cyanosis, and syncope (acute emergency)."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Tracheal Collapse in Dogs",
            url="https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-small-animals/tracheal-collapse-in-dogs",
            author="Johnson, L. R., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Fluoroscopy or tracheobronchoscopy during dynamic respiratory phases confirms collapse grade (I-IV)."
            ]
        )
    ],
    "DOG_013": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Bacterial Pneumonia and Bronchopneumonia in Dogs",
            url="https://www.merckvetmanual.com/respiratory-system/respiratory-diseases-of-small-animals/pneumonia-in-small-animals",
            author="Dear, J. D., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Lung parenchyma inflammation, frequently secondary to aspiration, viral infection, or megaesophagus.",
                "Moist, soft productive cough, tachypnea, dyspnea, pyrexia, purulent nasal discharge, and severe lethargy.",
                "Thoracic radiographs demonstrate ventral alveolar consolidation with air bronchograms."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Pneumonia in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4952814",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Requires systemic culture-directed antibiotics, airway coupage, nebulization, and oxygen therapy."
            ]
        )
    ],
    "DOG_014": [
        SourceReference(
            organization="International Society for Companion Animal Infectious Diseases (ISCAID)",
            title="ISCAID Guidelines for the Diagnosis and Management of Bacterial Urinary Tract Infections in Dogs",
            url="https://pubmed.ncbi.nlm.nih.gov/31599525/",
            author="Weese, J. S., et al.",
            publication_date="2019",
            claims_supported=[
                "Bacterial invasion of bladder urothelium (predominantly uropathogenic Escherichia coli).",
                "Presents with pollakiuria, hematuria, stranguria, dysuria, and malodorous urine.",
                "Definitive diagnosis requires quantitative bacterial urine culture via sterile cystocentesis."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Bacterial Urinary Tract Infections in Small Animals",
            url="https://www.merckvetmanual.com/urinary-system/infectious-diseases-of-the-urinary-tract-in-small-animals/bacterial-urinary-tract-infections-in-small-animals",
            author="Chew, D. J., DVM, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Systemic signs (fever, lethargy, anorexia) suggest ascending upper tract infection (pyelonephritis)."
            ]
        )
    ],
    "DOG_015": [
        SourceReference(
            organization="Minnesota Urolith Center",
            title="Canine Urolithiasis Management Guidelines",
            url="https://www.vetmed.umn.edu/centers-programs/minnesota-urolith-center",
            author="Minnesota Urolith Scientific Team",
            publication_date="2023",
            claims_supported=[
                "Struvite (infection-induced via urease-producing bacteria) and calcium oxalate are the primary canine uroliths.",
                "Symptoms include recurrent hematuria, dysuria, and frequent voiding of small volumes.",
                "Urethral lodgement in male dogs produces an acute obstructive emergency."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Urolithiasis in Dogs",
            url="https://www.merckvetmanual.com/urinary-system/noninfectious-diseases-of-the-urinary-tract-in-small-animals/urolithiasis-in-small-animals",
            author="Lulich, J. P., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Abdominal radiographs, retrograde urography, or ultrasound confirm presence, location, and radiopacity."
            ]
        )
    ],
    "DOG_016": [
        SourceReference(
            organization="International Renal Interest Society (IRIS)",
            title="IRIS Canine CKD Staging System",
            url="http://www.iris-kidney.com/guidelines/staging.html",
            author="IRIS Canine Scientific Panel",
            publication_date="2023",
            claims_supported=[
                "Gradual irreversible loss of functional nephrons over months to years.",
                "Primary early indicators: polyuria, compensatory polydipsia, nocturia, and poor body condition.",
                "Advanced uremic signs: halitosis (uremic breath), oral ulcerations, anorexia, non-regenerative anemia, and vomiting."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Chronic Kidney Disease in Dogs",
            url="https://www.merckvetmanual.com/urinary-system/noninfectious-diseases-of-the-urinary-tract-in-small-animals/chronic-kidney-disease-in-small-animals",
            author="Polzin, D. J., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Serum SDMA rises earlier than creatinine (at ~25-40% nephron loss vs ~75% for creatinine)."
            ]
        )
    ],
    "DOG_017": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Otitis Externa in Dogs",
            url="https://www.merckvetmanual.com/ear-disorders/otitis-externa/otitis-externa-in-dogs",
            author="Rosychuk, R. A., DVM, DACVD",
            publication_date="2023",
            claims_supported=[
                "Inflammation of external ear canal epithelium, primary trigger being atopic dermatitis or food allergy in >80% of recurrent cases.",
                "Signs include vigorous head shaking, ear scratching, foul odor, erythema, stenosis, and purulent exudate.",
                "Otoscopic examination and cytology (bacteria/yeast) guide topical therapy and verify tympanic membrane integrity."
            ]
        ),
        SourceReference(
            organization="VCA Animal Hospitals",
            title="Ear Infections in Dogs (Otitis Externa)",
            url="https://vcahospitals.com/know-your-pet/ear-infections-in-dogs-otitis-externa",
            author="Barnette, C., DVM; Ward, E., DVM",
            publication_date="2023",
            claims_supported=[
                "Pendulous ears (Spaniels, Retrievers) and excessive canal hair/swimming create moisture predisposing to secondary infection."
            ]
        )
    ],
    "DOG_018": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Ulcerative Keratitis in Dogs",
            url="https://www.merckvetmanual.com/eye-diseases-and-disorders/corneal-diseases-in-small-animals/corneal-ulcers-in-small-animals",
            author="Ledbetter, E. C., DVM, DACVO",
            publication_date="2023",
            claims_supported=[
                "Corneal epithelial defect commonly initiated by trauma, foreign bodies, keratoconjunctivitis sicca (dry eye), or distichiasis.",
                "Causes severe blepharospasm, epiphora, conjunctival hyperemia, and photophobia.",
                "Fluorescein dye retention confirms ulcer depth; melting/deep ulcers require urgent aggressive therapy to avoid perforation."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Corneal Ulcers in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951478",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Topical corticosteroids are strictly contraindicated because they accelerate corneal collagenolysis and perforation."
            ]
        )
    ],
    "DOG_019": [
        SourceReference(
            organization="American Animal Hospital Association (AAHA)",
            title="AAHA Diabetes Management Guidelines for Dogs and Cats",
            url="https://www.aaha.org/aaha-guidelines/diabetes-management/diabetes-management-home/",
            author="AAHA Diabetes Guidelines Task Force",
            publication_date="2022",
            claims_supported=[
                "Almost exclusively insulin-dependent (Type 1-like) diabetes due to immune-mediated destruction of pancreatic beta cells.",
                "Classic signs: polyuria, polydipsia, polyphagia with weight loss, and bilateral diabetic cataract formation (rapid blindness).",
                "Diabetic ketoacidosis (DKA) presents with vomiting, tachypnea (Kussmaul breathing), acetone breath, and severe dehydration (emergency)."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Diabetes Mellitus in Dogs",
            url="https://www.merckvetmanual.com/endocrine-system/the-pancreas/diabetes-mellitus-in-dogs-and-cats",
            author="Nelson, R. W., DVM, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Requires lifelong twice-daily exogenous insulin injections, dietary consistency, and blood glucose monitoring."
            ]
        )
    ],
    "DOG_020": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Hypothyroidism in Dogs",
            url="https://www.merckvetmanual.com/endocrine-system/the-thyroid-gland/hypothyroidism-in-animals",
            author="Scott-Moncrieff, J. C., VetMB, MS, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Immune-mediated lymphocytic thyroiditis or idiopathic thyroid atrophy causing deficiency of thyroid hormones T4 and T3.",
                "Classic presentation: lethargy, weight gain without increased appetite, heat-seeking/cold intolerance, and 'tragic facial expression'.",
                "Dermatologic signs: bilateral symmetrical non-pruritic flank alopecia, 'rat tail' (alopecia on tail), and hyperpigmentation."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Hypothyroidism in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951458",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Diagnosis confirmed by low total or free T4 accompanied by elevated endogenous canine thyroid-stimulating hormone (cTSH)."
            ]
        )
    ],
    "DOG_021": [
        SourceReference(
            organization="American College of Veterinary Internal Medicine (ACVIM)",
            title="ACVIM Consensus Statement: Diagnosis of Spontaneous Canine Hyperadrenocorticism",
            url="https://pubmed.ncbi.nlm.nih.gov/23113523/",
            author="Behrend, E. N., et al.",
            publication_date="2022",
            claims_supported=[
                "Chronic excessive glucocorticoid production from pituitary adenoma (80-85%) or functional adrenal tumor (15-20%).",
                "Signs: polyuria, polydipsia, severe polyphagia, pendulous 'pot-bellied' abdomen, hepatomegaly, muscle wasting, and panting.",
                "Cutaneous findings: bilateral symmetrical alopecia, thin fragile skin, comedones, and calcinosis cutis."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Cushing Syndrome (Hyperadrenocorticism) in Dogs",
            url="https://www.merckvetmanual.com/endocrine-system/the-adrenal-glands/cushing-syndrome-in-animals",
            author="Gilor, C., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Screening tests include low-dose dexamethasone suppression test (LDDST) and urine cortisol:creatinine ratio (UCCR)."
            ]
        )
    ],
    "DOG_022": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Hypoadrenocorticism (Addison Disease) in Dogs",
            url="https://www.merckvetmanual.com/endocrine-system/the-adrenal-glands/addison-disease-in-animals",
            author="Gilor, C., DVM, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Deficiency of mineralocorticoids (aldosterone) and glucocorticoids (cortisol) due to immune destruction of adrenal cortex.",
                "Known as 'The Great Mimicker' with waxing and waning lethargy, vomiting, diarrhea, tremors, and weakness.",
                "Acute Addisonian Crisis: severe hypovolemic shock, profound bradycardia (due to hyperkalemia), and collapse (critical emergency)."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Addison's Disease (Hypoadrenocorticism) in Dogs",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951479",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Classic laboratory profile shows low sodium-to-potassium ratio (<27:1); definitive test is ACTH stimulation test."
            ]
        )
    ],
    "DOG_023": [
        SourceReference(
            organization="American Veterinary Medical Association (AVMA)",
            title="Canine Parvovirus: What Pet Owners Need to Know",
            url="https://www.avma.org/resources-tools/pet-owners/petcare/canine-parvovirus",
            author="AVMA Animal Health Committee",
            publication_date="2023",
            claims_supported=[
                "Highly contagious viral disease of unvaccinated or incompletely vaccinated puppies.",
                "Attacks intestinal crypt epithelia and lymphoid bone marrow, causing severe hemorrhagic diarrhea, intractable vomiting, and sepsis.",
                "Hallmark signs: foul-smelling bloody diarrhea, severe dehydration, hypothermia, leukopenia, and sudden collapse (critical emergency)."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Canine Parvovirus",
            url="https://www.merckvetmanual.com/generalized-conditions/canine-parvovirus/canine-parvovirus",
            author="Truyen, U., DVM, PhD",
            publication_date="2023",
            claims_supported=[
                "Confirmed via fecal point-of-care antigen ELISA; requires immediate barrier isolation, intensive IV fluids, and antiemetics."
            ]
        )
    ],
    "DOG_024": [
        SourceReference(
            organization="American College of Veterinary Internal Medicine (ACVIM)",
            title="ACVIM Consensus Statement on Leptospirosis in Dogs",
            url="https://pubmed.ncbi.nlm.nih.gov/37968984/",
            author="Sykes, J. E., et al.",
            publication_date="2023",
            claims_supported=[
                "Zoonotic spirochete infection (Leptospira interrogans) transmitted via contact with contaminated standing water or rodent urine.",
                "Causes acute kidney injury (AKI) and acute hepatic failure; clinical signs: lethargy, vomiting, fever, icterus, and oliguria.",
                "Can cause severe pulmonary hemorrhage syndrome in dogs; strict zoonotic precautions required."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Leptospirosis in Dogs",
            url="https://www.merckvetmanual.com/generalized-conditions/leptospirosis/leptospirosis-in-dogs",
            author="Sykes, J. E., BVSc, PhD, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Diagnosis supported via microscopic agglutination test (MAT) fourfold titer rise or urine/blood PCR before antibiotic therapy."
            ]
        )
    ],
    "DOG_025": [
        SourceReference(
            organization="American Heartworm Society (AHS)",
            title="Current Guidelines for the Prevention, Diagnosis, and Management of Heartworm Infection in Dogs",
            url="https://www.heartwormsociety.org/veterinary-resources/american-heartworm-society-guidelines",
            author="AHS Board of Directors",
            publication_date="2024",
            claims_supported=[
                "Mosquito-borne nematode (Dirofilaria immitis) lodging in pulmonary arteries and right ventricle.",
                "Early stages asymptomatic; progressive signs: chronic cough, exercise intolerance, dyspnea, weight loss, and ascites.",
                "Caval syndrome (acute tricuspid valve obstruction by mass of worms) causes sudden cardiovascular collapse, hemoglobinuria, and shock."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Heartworm Disease in Dogs",
            url="https://www.merckvetmanual.com/circulatory-system/heartworm-disease/heartworm-disease-in-dogs",
            author="Bowman, D. D., MS, PhD",
            publication_date="2023",
            claims_supported=[
                "Annual blood antigen testing paired with microfilaria detection is standard of care; adulticide protocol uses melarsomine."
            ]
        )
    ],
    "DOG_026": [
        SourceReference(
            organization="American College of Veterinary Internal Medicine (ACVIM)",
            title="ACVIM Consensus Guidelines for the Diagnosis and Treatment of Myxomatous Mitral Valve Disease in Dogs",
            url="https://pubmed.ncbi.nlm.nih.gov/31074099/",
            author="Keene, B. W., et al.",
            publication_date="2019",
            claims_supported=[
                "Most common heart disease in dogs, predominantly affecting older small-to-medium breeds (Cavalier King Charles Spaniel).",
                "Progressive fibroelastic remodeling causes mitral regurgitation, left atrial enlargement, and congestive heart failure.",
                "Key signs: left apical systolic murmur, tachypnea (>30 breaths/min at rest), exercise intolerance, nocturnal coughing, and syncope."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Degenerative Valve Disease in Small Animals",
            url="https://www.merckvetmanual.com/circulatory-system/valvular-disease-in-small-animals/degenerative-valve-disease-in-small-animals",
            author="Atkins, C. E., DVM, DACVIM",
            publication_date="2023",
            claims_supported=[
                "Staged from Stage A (at risk) to Stage D (refractory); pimobendan initiated at Stage B2 based on echocardiographic chamber enlargement."
            ]
        )
    ],
    "DOG_027": [
        SourceReference(
            organization="Association for Pet Obesity Prevention (APOP)",
            title="Canine Obesity Clinical Practice Guidelines",
            url="https://www.petobesityprevention.org/",
            author="Ward, E., DVM; APOP Clinical Panel",
            publication_date="2023",
            claims_supported=[
                "Over 55% of adult dogs are overweight or obese (BCS 7/9 to 9/9).",
                "Profoundly shortens lifespan by up to 2.5 years and exacerbates osteoarthritis, respiratory compromise, and tracheal collapse.",
                "Inability to palpate ribs beneath thick fat pad, loss of visible abdominal tuck, and exercise reluctance."
            ]
        ),
        SourceReference(
            organization="AAHA",
            title="AAHA Weight Management Guidelines for Dogs and Cats",
            url="https://www.aaha.org/aaha-guidelines/weight-management-configuration/weight-management-guidelines/",
            author="AAHA Expert Panel",
            publication_date="2022",
            claims_supported=[
                "Requires structured metabolic calorie calculation, measured feeding, and low-impact joint-safe exercise."
            ]
        )
    ],
    "DOG_028": [
        SourceReference(
            organization="American Veterinary Dental College (AVDC)",
            title="Canine Periodontal Disease Etiology and Stages",
            url="https://avdc.org/periodontal-disease/",
            author="AVDC Clinical Guidelines Committee",
            publication_date="2023",
            claims_supported=[
                "Bacterial plaque bioflim induces progressive gingival inflammation, periodontal pocketing, bone loss, and tooth mobility.",
                "Affects >80% of dogs by age 3; signs include halitosis, red swollen bleeding gums, calculus accumulation, and reluctance to chew.",
                "Can serve as source of chronic bacteremia with systemic effects on heart, kidneys, and liver."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Periodontal Disease in Small Animals",
            url="https://www.merckvetmanual.com/digestive-system/dentistry/periodontal-disease-in-small-animals",
            author="Bellows, J., DVM, DAVDC, DABVP",
            publication_date="2023",
            claims_supported=[
                "Requires comprehensive oral health assessment and treatment (COHAT) under general anesthesia with dental radiographs."
            ]
        )
    ],
    "DOG_029": [
        SourceReference(
            organization="American College of Veterinary Behaviorists (ACVB)",
            title="Canine Separation Anxiety Diagnostic Guidelines",
            url="https://www.dacvb.org/",
            author="ACVB Clinical Guidelines Committee",
            publication_date="2022",
            claims_supported=[
                "Specific distress response triggered by real or perceived absence of owner or attachment figure.",
                "Hallmark signs occur almost exclusively when left alone: destructive behavior focused at exit points (doors/windows), persistent vocalization, and inappropriate elimination.",
                "Autonomic signs include severe hypersalivation, pacing, trembling, and anorexia when alone."
            ]
        ),
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Separation Anxiety in Dogs",
            url="https://www.merckvetmanual.com/behavior/behavioral-problems-of-dogs/separation-anxiety-in-dogs",
            author="Landsberg, G. M., DVM, DACVB, DECAWBM",
            publication_date="2023",
            claims_supported=[
                "Must be differentiated from boredom, lack of house training, or medical polyuria/enteritis via video recording."
            ]
        )
    ],
    "DOG_030": [
        SourceReference(
            organization="Merck Veterinary Manual",
            title="Cognitive Dysfunction Syndrome in Dogs and Cats",
            url="https://www.merckvetmanual.com/behavior/behavioral-problems-of-dogs/cognitive-dysfunction-syndrome-in-dogs-and-cats",
            author="Landsberg, G. M., DVM, DACVB, DECAWBM",
            publication_date="2023",
            claims_supported=[
                "Neurodegenerative age-related disorder analogous to human Alzheimer's disease with beta-amyloid deposition.",
                "Evaluated using the DISHA clinical screening criteria: Disorientation, altered social Interactions, Sleep-wake cycle disturbances, House-soiling, and Activity changes.",
                "Diagnosis requires thorough veterinary exclusion of painful conditions (osteoarthritis), blindness, deafness, and organ failure."
            ]
        ),
        SourceReference(
            organization="Veterinary Partner (VIN)",
            title="Cognitive Dysfunction Syndrome (Dog Dementia)",
            url="https://veterinarypartner.vin.com/default.aspx?pid=19239&id=4951408",
            author="Brooks, W., DVM, DABVP",
            publication_date="2023",
            claims_supported=[
                "Enrichment, antioxidant/medium-chain triglyceride diets, and selegiline may slow progression."
            ]
        )
    ],
}

import argparse
import csv
import re
import os
from csv_reader import read_subject_csv
from llm_api import call_anthropic
from collections import defaultdict
import datetime


def get_comprehensive_keyword_dictionary():
    """
    Comprehensive keyword dictionary for all four subjects: 
    ancient_history, math, physics, economics
    """
    return {
        # ===== ANCIENT HISTORY =====
        # Archaeological Sites & Civilizations
        'harappan': 'Harappan Civilization',
        'indus': 'Indus Valley Civilization',
        'burzahom': 'Neolithic Settlements; Kashmir Archaeology',
        'chandraketugarh': 'Bengal Archaeology; Terracotta Art',
        'ganeshwar': 'Chalcolithic Culture; Copper Artifacts',
        'dholavira': 'Harappan Civilization; Water Management',
        'chanhudaro': 'Harappan Sites',
        'sohgaura': 'Mauryan Period',
        'desalpur': 'Harappan Sites',
        'kanganahalli': 'Mauryan Sculpture; Buddhist Art',
        'kot': 'Archaeological Sites',
        
        # Dynasties and Political History
        'maurya': 'Mauryan Empire',
        'mauryan': 'Mauryan Empire',
        'ashoka': 'Mauryan Empire; Ashokan Edicts',
        'gupta': 'Gupta Period',
        'chola': 'Chola Administration',
        'pushyabhuti': 'Post-Gupta Period',
        'maukhari': 'Post-Gupta Period',
        'empire': 'Political History',
        'dynasty': 'Political History',
        'king': 'Monarchy; Political History',
        'ruler': 'Political History',
        
        # Administrative Terms
        'eripatti': 'Chola Administration; Village Revenue',
        'taniyur': 'Brahmadeya; Land Grants',
        'ghatika': 'Temple Education',
        'vishti': 'Forced Labor; Gupta Administration',
        'guild': 'Ancient Economy; Trade Organizations',
        'arthashastra': 'Kautilya\'s Arthashastra; Political Theory',
        'kautilya': 'Political Theory; Mauryan Administration',
        
        # Religious & Philosophical
        'buddhism': 'Buddhism',
        'buddhist': 'Buddhism',
        'jainism': 'Jainism',
        'jain': 'Jainism',
        'vedic': 'Vedic Period',
        'rigveda': 'Vedic Literature',
        'rigvedic': 'Early Vedic Period',
        'anekantavada': 'Jain Philosophy',
        'asceticism': 'Religious Practices',
        'ritual': 'Religious Practices',
        'yajna': 'Vedic Rituals',
        
        # Literature & Scholars
        'panini': 'Sanskrit Grammar',
        'amarasimha': 'Sanskrit Literature',
        'kalidasa': 'Classical Sanskrit Literature',
        'bhavabhuti': 'Sanskrit Drama',
        'avadanasataka': 'Jain Literature',
        'dignaga': 'Buddhist Philosophy',
        'aryadeva': 'Buddhist Philosophy',
        'nathamuni': 'Vaishnavism',
        
        # Science & Technology (Historical)
        'surgery': 'Ancient Indian Science; Medicine',
        'surgical': 'Ancient Indian Medicine',
        'transplant': 'Ancient Surgery',
        'sine': 'Ancient Mathematics; Trigonometry',
        'cyclic': 'Ancient Geometry',
        'quadrilateral': 'Ancient Mathematics',
        'aryabhata': 'Ancient Mathematics; Astronomy',
        'brahmagupta': 'Medieval Mathematics',
        'metallurgy': 'Ancient Technology',
        
        # Trade & Economy (Historical)
        'ghantasala': 'Maritime Trade; Ancient Ports',
        'kadura': 'Maritime Trade',
        'chaul': 'Maritime Trade',
        'monsoon': 'Maritime Navigation',
        'cotton': 'Textile Industry; Harappan Economy',
        'terracotta': 'Material Culture; Art',
        'copper': 'Chalcolithic Technology',
        
        # Sources & Methods
        'edict': 'Ashokan Edicts; Mauryan Inscriptions',
        'inscription': 'Epigraphy',
        'prinsep': 'Epigraphy; Decipherment',
        'yuan': 'Chinese Travelers; Cultural Exchange',
        'excavation': 'Archaeological Methods',
        'bard': 'Oral Tradition; Historiography',
        'magadha': 'Epic Tradition; Bards',
        
        # ===== MATHEMATICS =====
        'algebra': 'Algebra',
        'algebraic': 'Algebra',
        'equation': 'Algebraic Equations',
        'polynomial': 'Polynomial Functions',
        'quadratic': 'Quadratic Equations',
        'linear': 'Linear Algebra',
        'matrix': 'Linear Algebra; Matrices',
        'determinant': 'Linear Algebra',
        'vector': 'Vector Algebra',
        
        'geometry': 'Geometry',
        'geometric': 'Geometry',
        'triangle': 'Geometry; Triangles',
        'circle': 'Geometry; Circles',
        'angle': 'Geometry',
        'theorem': 'Mathematical Theorems',
        'proof': 'Mathematical Proofs',
        'coordinate': 'Coordinate Geometry',
        
        'calculus': 'Calculus',
        'derivative': 'Differential Calculus',
        'integral': 'Integral Calculus',
        'limit': 'Limits and Continuity',
        'differentiation': 'Differential Calculus',
        'integration': 'Integral Calculus',
        'function': 'Functions',
        
        'trigonometry': 'Trigonometry',
        'trigonometric': 'Trigonometry',
        'sin': 'Trigonometric Functions',
        'cos': 'Trigonometric Functions',
        'tan': 'Trigonometric Functions',
        
        'probability': 'Probability Theory',
        'statistics': 'Statistics',
        'distribution': 'Statistical Distributions',
        'mean': 'Descriptive Statistics',
        'variance': 'Statistical Measures',
        'standard': 'Statistical Analysis',
        
        # ===== PHYSICS =====
        'mechanics': 'Classical Mechanics',
        'motion': 'Kinematics; Dynamics',
        'force': 'Newton\'s Laws; Forces',
        'acceleration': 'Kinematics',
        'velocity': 'Kinematics',
        'momentum': 'Momentum and Collision',
        'energy': 'Energy and Work',
        'work': 'Work and Energy',
        'power': 'Work, Energy and Power',
        'newton': 'Newton\'s Laws',
        
        'thermodynamics': 'Thermodynamics',
        'heat': 'Heat and Temperature',
        'temperature': 'Thermodynamics',
        'entropy': 'Thermodynamics',
        'gas': 'Kinetic Theory of Gases',
        'pressure': 'Fluid Properties',
        
        'electromagnetism': 'Electromagnetism',
        'electric': 'Electric Fields and Potential',
        'magnetic': 'Magnetism',
        'current': 'Electric Current',
        'voltage': 'Electric Potential',
        'circuit': 'Electric Circuits',
        'resistance': 'Electrical Resistance',
        'capacitor': 'Capacitance',
        'inductor': 'Electromagnetic Induction',
        
        'wave': 'Wave Physics',
        'frequency': 'Wave Properties',
        'wavelength': 'Wave Properties',
        'amplitude': 'Wave Properties',
        'sound': 'Sound Waves',
        'light': 'Optics; Light',
        'optics': 'Optics',
        'lens': 'Geometrical Optics',
        'mirror': 'Reflection of Light',
        'refraction': 'Refraction of Light',
        
        'quantum': 'Quantum Physics',
        'photon': 'Quantum Physics',
        'electron': 'Atomic Physics',
        'atom': 'Atomic Structure',
        'nuclear': 'Nuclear Physics',
        'radioactive': 'Nuclear Physics',
        
        'relativity': 'Theory of Relativity',
        'einstein': 'Modern Physics; Relativity',
        'spacetime': 'Special Relativity',
        
        # ===== ECONOMICS =====
        'demand': 'Demand Theory',
        'supply': 'Supply Theory',
        'market': 'Market Economics',
        'price': 'Price Theory',
        'elasticity': 'Price Elasticity',
        'competition': 'Market Structure',
        'monopoly': 'Market Structure',
        'oligopoly': 'Market Structure',
        
        'inflation': 'Monetary Economics',
        'deflation': 'Monetary Economics',
        'gdp': 'National Income',
        'gnp': 'National Income',
        'fiscal': 'Fiscal Policy',
        'monetary': 'Monetary Policy',
        'budget': 'Public Finance',
        'tax': 'Public Finance; Taxation',
        'subsidy': 'Government Intervention',
        
        'trade': 'International Trade',
        'export': 'International Trade',
        'import': 'International Trade',
        'exchange': 'Foreign Exchange',
        'currency': 'Monetary System',
        'balance': 'Balance of Payments',
        
        'employment': 'Labor Economics',
        'unemployment': 'Labor Economics',
        'wage': 'Labor Economics',
        'labor': 'Labor Economics',
        
        'investment': 'Investment Theory',
        'saving': 'Savings and Investment',
        'capital': 'Capital Formation',
        'interest': 'Interest Rate Theory',
        'bank': 'Banking and Finance',
        'credit': 'Credit and Banking',
        
        'development': 'Economic Development',
        'growth': 'Economic Growth',
        'poverty': 'Development Economics',
        'inequality': 'Income Distribution'
    }


def extract_concepts_keyword_based(question_text, subject):
    """
    Extract concepts using comprehensive keyword-based approach for all subjects
    """
    concept_keywords = get_comprehensive_keyword_dictionary()
    question_lower = question_text.lower()
    extracted_concepts = []
    matched_keywords = []
    
    # Check for keyword matches
    for keyword, concept in concept_keywords.items():
        if keyword in question_lower:
            # Handle multiple concepts separated by semicolon
            concepts = [c.strip() for c in concept.split(';')]
            extracted_concepts.extend(concepts)
            matched_keywords.append(keyword)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_concepts = []
    for concept in extracted_concepts:
        if concept not in seen and concept:
            seen.add(concept)
            unique_concepts.append(concept)
    
    # Subject-specific fallbacks if no matches found
    if not unique_concepts:
        fallback_concepts = {
            'ancient_history': 'Ancient History',
            'math': 'Mathematics',
            'physics': 'Physics', 
            'economics': 'Economics'
        }
        unique_concepts.append(fallback_concepts.get(subject, 'General Knowledge'))
    
    # Optional debug info
    if matched_keywords and len(matched_keywords) <= 3:  # Don't spam for too many matches
        print(f"    → Detected keywords: {', '.join(matched_keywords)}")
    
    return '; '.join(unique_concepts)

def detect_subject(question_text):
    """
    Automatically detect the most likely subject based on keyword frequency
    """
    subject_keywords = {
        'ancient_history': [
            'harappan', 'maurya', 'gupta', 'ashoka', 'vedic', 
            'buddhism', 'inscription', 'dynasty', 'archaeology'
        ],
        'math': [
            'algebra', 'geometry', 'calculus', 'equation', 'triangle',
            'theorem', 'probability', 'statistics', 'derivative'
        ],
        'physics': [
            'force', 'energy', 'velocity', 'acceleration', 'quantum',
            'thermodynamics', 'electric', 'magnetic', 'wave'
        ],
        'economics': [
            'demand', 'supply', 'market', 'price', 'gdp',
            'inflation', 'trade', 'tax', 'employment'
        ]
    }
    
    question_lower = question_text.lower()
    subject_scores = defaultdict(int)
    
    # Score each subject based on keyword matches
    for subject, keywords in subject_keywords.items():
        for keyword in keywords:
            if keyword in question_lower:
                subject_scores[subject] += 1
    
    # Return subject with highest score, or default to ancient_history
    if subject_scores:
        return max(subject_scores.items(), key=lambda x: x[1])[0]
    return 'ancient_history'  # default fallback

def get_next_question_number(subject):
    """Get the next question number by checking existing CSV file"""
    output_file = f"output_concepts_{subject}.csv"
    
    if not os.path.exists(output_file):
        return 1
    
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            last_line = None
            for last_line in csv.DictReader(file):
                pass
            if last_line:
                return int(last_line['Question Number']) + 1
    except Exception as e:
        print(f"⚠️  Error reading existing file: {e}")
    
    return 1

def interactive_mode():
    """
    Interactive mode that:
    1. Accepts complete questions in one input
    2. Checks for duplicates before saving
    3. Maintains all previous functionality
    """
    print("🎯 INTERACTIVE CONCEPT EXTRACTION MODE")
    print("Enter complete questions in this format (or 'quit' to exit):")
    print("Question,Option A,Option B,Option C,Option D,Ans.?")
    print("Example:")
    print('"What was the capital of Magadha?","Patliputra","Taxila","Ujjain","Kashi",A\n')
    
    while True:
        print("-" * 50)
        user_input = input("📝 Enter question with options: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not user_input:
            print("⚠️  Please enter a valid question")
            continue
            
        try:
            # Parse input
            parsed = list(csv.reader([user_input], quotechar='"'))[0]
            if len(parsed) != 6:
                raise ValueError("Incorrect number of fields")
                
            question, opt_a, opt_b, opt_c, opt_d, correct_ans = parsed
            correct_ans = correct_ans.upper()
            
            if correct_ans not in ['A', 'B', 'C', 'D']:
                raise ValueError("Correct answer must be A, B, C, or D")
                
        except Exception as e:
            print(f"⚠️  Invalid format: {e}")
            continue
            
        # Detect subject
        combined_text = f"{question} {opt_a} {opt_b} {opt_c} {opt_d}"
        subject = detect_subject(combined_text)
        print(f"\n🔍 Detected subject: {subject.replace('_', ' ').title()}")
        
        # Check for duplicates
        if is_duplicate_question(question, subject):
            print("⏭️  Duplicate question detected - skipping save")
            continue
            
        # Get next question number
        next_qnum = get_next_question_number(subject)
        
        # Extract concepts
        print(f"\n🔍 Analyzing question...")
        concepts = extract_concepts_from_question(combined_text, subject, use_api=False)
        print(f"✅ Extracted Concepts: {concepts}")
        
        # Save to CSV
        save_interactive_result(
            question, opt_a, opt_b, opt_c, opt_d, correct_ans, 
            concepts, subject, next_qnum
        )

def is_duplicate_question(question, subject):
    """Check if question already exists in the subject's CSV file"""
    output_file = f"output_concepts_{subject}.csv"
    
    if not os.path.exists(output_file):
        return False
        
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Question'].strip().lower() == question.strip().lower():
                    return True
    except Exception as e:
        print(f"⚠️  Error checking for duplicates: {e}")
        
    return False

def save_interactive_result(question, opt_a, opt_b, opt_c, opt_d, correct_ans, concepts, subject, qnum):
    """Save in the standardized format"""
    output_file = f"output_concepts_{subject}.csv"
    file_exists = os.path.exists(output_file)
    
    with open(output_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Question Number', 'Question', 'Option A', 'Option B', 
                           'Option C', 'Option D', 'Ans.?', 'Concepts'])
            
        writer.writerow([
            qnum, question, opt_a, opt_b, opt_c, opt_d, 
            correct_ans, concepts
        ])
    
    print(f"📁 Saved as Question {qnum} in {output_file}\n")

def get_next_question_number(subject):
    """Get next question number checking existing CSV"""
    output_file = f"output_concepts_{subject}.csv"
    
    if not os.path.exists(output_file):
        return 1
    
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if rows:
                return int(rows[-1]['Question Number']) + 1
    except Exception as e:
        print(f"⚠️  Error reading existing file: {e}")
    
    return 1
def extract_concepts_from_question(question_text, subject='ancient_history', use_api=False):
    """
    Extract concepts from a question using either Anthropic API or keyword-based approach.
    """
    if use_api:
        # Subject-specific prompts for better results
        subject_context = {
            'ancient_history': 'ancient Indian history, archaeology, dynasties, literature, and culture',
            'math': 'mathematics including algebra, geometry, calculus, statistics, and mathematical theorems',
            'physics': 'physics including mechanics, thermodynamics, electromagnetism, optics, and modern physics',
            'economics': 'economics including microeconomics, macroeconomics, public finance, and international trade'
        }
        
        context = subject_context.get(subject, 'academic concepts')
        
        prompt = (
            f"This is a competitive exam question from {subject.replace('_', ' ')} focusing on {context}. "
            f"Identify the main academic concepts being tested in this question. "
            f"Be specific and precise. Return only the concept names separated by semicolons.\n\n"
            f"Question: {question_text}\n\n"
            f"Concepts:"
        )
        
        try:
            response = call_anthropic(prompt)
            return response.strip()
        except Exception as e:
            print(f"    ⚠️  API call failed: {e}")
            print(f"    → Falling back to keyword extraction...")
            return extract_concepts_keyword_based(question_text, subject)
    else:
        return extract_concepts_keyword_based(question_text, subject)


def save_output_csv(subject, results):
    """Save the final results to a CSV file matching assignment format"""
    output_file = f"output_concepts_{subject}.csv"

    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Question Number', 'Question', 'Concepts']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"\n✅ Results saved to: {output_file}")


def analyze_concept_distribution(results, subject):
    """Analyze and display concept distribution statistics"""
    concept_count = defaultdict(int)
    
    for result in results:
        concepts = result['Concepts'].split(';')
        for concept in concepts:
            concept = concept.strip()
            if concept and concept not in ['General Knowledge', subject.title()]:
                concept_count[concept] += 1
    
    print(f"\n📊 CONCEPT DISTRIBUTION ANALYSIS - {subject.upper()}")
    print(f"=" * 50)
    print(f"Total unique concepts found: {len(concept_count)}")
    
    if concept_count:
        print(f"Top 5 most tested concepts:")
        sorted_concepts = sorted(concept_count.items(), key=lambda x: x[1], reverse=True)
        for i, (concept, count) in enumerate(sorted_concepts[:5], 1):
            percentage = (count / len(results)) * 100
            print(f"  {i}. {concept}: {count} questions ({percentage:.1f}%)")
    else:
        print("No specific concepts detected - may need API or enhanced keywords")


def main():
    parser = argparse.ArgumentParser(
        description="Concept Extraction Tool for Competitive Exams (UPSC, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --subject=ancient_history
  python main.py --subject=math --use-api
  python main.py --subject=physics --analyze
  python main.py --subject=economics --use-api --analyze
        """
    )
    
    parser.add_argument('--subject', required=True, 
                       choices=['ancient_history', 'math', 'physics', 'economics'], 
                       help='Subject to process')
    parser.add_argument('--use-api', action='store_true', 
                       help='Use Anthropic API for concept extraction (requires API key in .env)')
    parser.add_argument('--analyze', action='store_true',
                       help='Show detailed concept distribution analysis')
    parser.add_argument('--interactive', action='store_true',
                    help='Run in interactive mode for real-time question analysis')
    args = parser.parse_args()

    print(f"🚀 CONCEPT EXTRACTION TOOL")
    print(f"Subject: {args.subject.replace('_', ' ').title()}")
    print(f"Method: {'Anthropic API' if args.use_api else 'Keyword-based'}")
    print("=" * 50)

    if args.interactive:
        interactive_mode()
        return

    # Read questions CSV
    try:
        data = read_subject_csv(args.subject)
        print(f"📚 Loaded {len(data)} questions from {args.subject}.csv")
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    results = []

    # Process each question
    for i, row in enumerate(data, 1):
        question_num = str(row.get('Question Number', i)).strip()
        question_text = row.get('Question', '').strip()

        if not question_text:
            print(f"⚠️  Question {question_num}: Empty question text, skipping...")
            continue

        print(f"\n🔍 Question {question_num}:")
        print(f"   {question_text[:100]}{'...' if len(question_text) > 100 else ''}")

        # Extract concepts
        concepts = extract_concepts_from_question(question_text, args.subject, args.use_api)
        print(f"   📝 Concepts: {concepts}")

        results.append({
            'Question Number': question_num,
            'Question': question_text,
            'Concepts': concepts
        })

    # Save results in assignment format
    save_output_csv(args.subject, results)

    # Optional detailed analysis
    if args.analyze:
        analyze_concept_distribution(results, args.subject)

    # Summary
    print(f"\n🎯 PROCESSING COMPLETE!")
    print(f"   • Processed: {len(results)} questions")
    print(f"   • Subject: {args.subject}")
    print(f"   • Output: output_concepts_{args.subject}.csv")
    print(f"   • Method: {'API-based' if args.use_api else 'Keyword-based'}")
    
    if not args.use_api:
        print(f"   💡 Tip: Use --use-api for more accurate concept extraction")


if __name__ == "__main__":
    main()
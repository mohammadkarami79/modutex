#!/usr/bin/env python3
"""
ModuTex v1.0 - AI-Powered LaTeX Assistant
Professional application for LaTeX content generation and management
"""

import argparse
import os
import sys
import requests
import json
from pathlib import Path
import re

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, try to read .env manually
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Fix Unicode encoding for Windows CMD
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Available OpenAI models
MODELS = {
    "gpt-4": "GPT-4 (Best Quality - Expensive)",
    "gpt-4-turbo": "GPT-4 Turbo (Recommended)",
    "gpt-3.5-turbo": "GPT-3.5 Turbo (Fast & Cheap)"
}

def get_openai_key():
    """Get OpenAI API key from environment"""
    api_key = os.environ.get('OPENAI_API_KEY', 'your_api_key')
    if api_key == 'your_api_key' or not api_key:
        print("[ERROR] OpenAI API key not configured!")
        print("Please get your API key from: https://platform.openai.com/api-keys")
        print("Then edit .env file and add:")
        print("   OPENAI_API_KEY=sk-proj-your_actual_key_here")
        print("")
        return None
    return api_key

def select_model():
    """Select OpenAI model"""
    model = os.environ.get('OPENAI_MODEL', 'gpt-4-turbo')
    if model in MODELS:
        return model
    return 'gpt-4-turbo'

def call_openai_api(system_prompt, user_prompt, temperature=0.7):
    """Common function to call OpenAI API"""
    api_key = get_openai_key()
    if not api_key:
        return None
    
    model = select_model()
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 2500,
        "temperature": temperature
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"[ERROR] API request failed: {response.status_code}")
            if response.status_code == 401:
                print("[SOLUTION] Check your OPENAI_API_KEY in .env file")
            elif response.status_code == 429:
                print("[SOLUTION] Rate limit exceeded. Wait a moment and try again")
            else:
                print(f"[DETAILS] {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return None

def edit_section(section_name, edit_prompt):
    """Edit an existing section with AI improvements"""
    section_file = Path("sections") / f"{section_name}.tex"
    
    if not section_file.exists():
        print(f"[ERROR] Section file not found: {section_file}")
        return False
    
    # Read current content
    try:
        with open(section_file, 'r', encoding='utf-8') as f:
            current_content = f.read()
    except Exception as e:
        print(f"[ERROR] Could not read section file: {e}")
        return False
    
    print(f"[AI] Improving section '{section_name}' using {MODELS[select_model()]}...")
    print(f"[PROMPT] {edit_prompt}")
    print("[STATUS] Processing improvements...")
    
    system_prompt = """You are a professional LaTeX expert and academic editor. You will receive existing LaTeX content and instructions for improvement.

IMPROVEMENT GUIDELINES:
1. Maintain the existing structure and style
2. Enhance content based on the specific instructions
3. Keep all existing citations and references
4. Add new citations where appropriate (format: \\cite{author2023topic})
5. Improve academic writing quality
6. Add relevant equations, figures, or tables if requested
7. Ensure proper LaTeX formatting
8. Don't change the overall structure unless specifically requested
9. Keep all existing cross-references (\\ref{}, \\cite{})
10. Support both English and Persian text naturally

OUTPUT: Return only the improved LaTeX code, nothing else."""
    
    user_prompt = f"""Current LaTeX content:
{current_content}

Improvement instructions: {edit_prompt}

Please improve this content according to the instructions while maintaining the existing structure and academic quality."""
    
    improved_content = call_openai_api(system_prompt, user_prompt, temperature=0.3)
    
    if improved_content:
        # Write improved content back to file
        try:
            with open(section_file, 'w', encoding='utf-8') as f:
                f.write(improved_content)
            
            print(f"[SUCCESS] Section improved: sections/{section_name}.tex")
            print(f"[INFO] Content length: {len(improved_content)} characters")
            
            # Show preview of changes
            print(f"\n[PREVIEW] Improved content (first 300 characters):")
            print("=" * 60)
            print(improved_content[:300] + "..." if len(improved_content) > 300 else improved_content)
            print("=" * 60)
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not write improved content: {e}")
            return False
    else:
        return False

def generate_section(name, prompt):
    """Generate LaTeX section content using ChatGPT"""
    print(f"[AI] Generating content for '{name}' section using {MODELS[select_model()]}...")
    print(f"[PROMPT] {prompt}")
    print("[STATUS] Processing request...")
    
    # Enhanced system prompt for better LaTeX output
    system_prompt = """You are a professional LaTeX expert and academic writer. Generate high-quality, well-structured LaTeX content for academic documents.

REQUIREMENTS:
1. Write clean, publication-ready LaTeX code
2. Use proper academic writing style
3. Include relevant citations with realistic keys (format: \\cite{author2023topic})
4. Add cross-references where appropriate (\\ref{fig:name}, \\ref{tab:name})
5. Use proper LaTeX environments for equations, figures, tables
6. Support both English and Persian text naturally
7. Don't include \\section{} header - only content
8. Use professional academic vocabulary
9. Include at least 2-3 citations per substantial paragraph
10. Add TODO comments for figures/tables if needed

LATEX FORMATTING:
- Equations: \\begin{equation}...\\end{equation}
- Tables: \\begin{table}[htbp]...\\end{table}
- Figures: \\begin{figure}[htbp]...\\end{figure}
- Lists: \\begin{itemize} or \\begin{enumerate}
- Emphasis: \\textbf{bold}, \\textit{italic}
- References: \\cite{realistic_key_2023}"""
    
    user_prompt = f"""Generate LaTeX content for a section about: {prompt}

Make this content:
- Academically rigorous and well-researched
- Properly formatted with LaTeX commands
- Include relevant equations if applicable
- Add realistic citations
- Use clear section structure with subsections if needed
- Length: 300-500 words minimum"""
    
    content = call_openai_api(system_prompt, user_prompt)
    
    if content:
        # Write to sections directory
        sections_dir = Path("sections")
        sections_dir.mkdir(exist_ok=True)
        
        output_file = sections_dir / f"{name}.tex"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[SUCCESS] Section generated: sections/{name}.tex")
            print(f"[INFO] Content length: {len(content)} characters")
            
            # Show preview
            print(f"\n[PREVIEW] First 200 characters:")
            print("=" * 60)
            print(content[:200] + "..." if len(content) > 200 else content)
            print("=" * 60)
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not write section file: {e}")
            return False
    else:
        return False

def text_to_latex(text_file, output_name=None):
    """Convert plain text to LaTeX format"""
    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            plain_text = f.read()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {text_file}")
        return False
    
    print(f"[AI] Converting text to LaTeX using {MODELS[select_model()]}...")
    print("[STATUS] Processing text conversion...")
    
    system_prompt = """You are a LaTeX formatting expert. Convert the given plain text to properly formatted LaTeX code.

CONVERSION RULES:
1. Preserve the original meaning and content
2. Add proper LaTeX formatting and structure
3. Convert lists to \\begin{itemize} or \\begin{enumerate}
4. Format equations properly with \\begin{equation}
5. Add \\textbf{} for emphasis where appropriate
6. Create tables for tabular data using \\begin{tabular}
7. Add realistic citations with \\cite{} where research references are mentioned
8. Use proper paragraph breaks
9. Don't add \\section{} headers
10. Support Persian and English text seamlessly

OUTPUT: Only the formatted LaTeX code, nothing else."""
    
    user_prompt = f"Convert this text to LaTeX format:\n\n{plain_text}"
    
    latex_content = call_openai_api(system_prompt, user_prompt, temperature=0.3)
    
    if latex_content:
        # Determine output filename
        if not output_name:
            base_name = Path(text_file).stem
            output_name = f"{base_name}_latex"
        
        # Write to sections directory
        sections_dir = Path("sections")
        sections_dir.mkdir(exist_ok=True)
        
        output_file = sections_dir / f"{output_name}.tex"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(latex_content)
            
            print(f"[SUCCESS] LaTeX file created: sections/{output_name}.tex")
            print(f"[INFO] Conversion: {len(plain_text)} chars -> {len(latex_content)} chars")
            
            # Show preview
            print(f"\n[PREVIEW] LaTeX output (first 300 characters):")
            print("=" * 60)
            print(latex_content[:300] + "..." if len(latex_content) > 300 else latex_content)
            print("=" * 60)
            
            return True
        except Exception as e:
            print(f"[ERROR] Could not write LaTeX file: {e}")
            return False
    else:
        return False

def update_main_tex():
    """Update main.tex to include all sections automatically"""
    sections_dir = Path("sections")
    if not sections_dir.exists():
        print("[ERROR] Sections directory not found!")
        return False
    
    # Get all .tex files in sections directory
    section_files = list(sections_dir.glob("*.tex"))
    if not section_files:
        print("[INFO] No sections found to include in main.tex")
        return True
    
    # Sort section files (common academic order)
    section_order = [
        'abstract', 'introduction', 'literature_review', 'related_work',
        'methodology', 'method', 'approach', 'implementation',
        'results', 'evaluation', 'experiments', 'analysis',
        'discussion', 'conclusion', 'future_work', 'acknowledgments'
    ]
    
    def get_order_priority(filename):
        name = filename.stem.lower()
        try:
            return section_order.index(name)
        except ValueError:
            return 1000  # Put unknown sections at the end
    
    section_files.sort(key=get_order_priority)
    
    print(f"[INFO] Found {len(section_files)} sections to include")
    
    # Read current main.tex
    main_tex_path = Path("main.tex")
    if main_tex_path.exists():
        try:
            with open(main_tex_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[ERROR] Could not read main.tex: {e}")
            return False
    else:
        # Create basic main.tex if it doesn't exist
        content = """\\documentclass[12pt]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{fontspec}
\\usepackage{graphicx}
\\usepackage{hyperref}
\\usepackage{xcolor}
\\usepackage{cite}

% Persian support
\\newif\\ifpersian
\\persianfalse  % Change to \\persiantrue for Persian documents

\\ifpersian
    \\usepackage{polyglossia}
    \\setdefaultlanguage{persian}
    \\setotherlanguage{english}
    \\newfontfamily\\persianfont{XB Zar}
    \\newfontfamily\\englishfont{Latin Modern Roman}
\\fi

\\title{Research Document}
\\author{Author Name}
\\date{\\today}

\\begin{document}

\\maketitle

% Sections will be automatically inserted here

\\bibliographystyle{ieeetr}
\\bibliography{bib/references,bib/local_manual}

\\end{document}"""
    
    # Find where to insert sections (after \maketitle, before bibliography)
    if "\\maketitle" in content and "\\bibliographystyle" in content:
        # Split content at bibliography
        before_bib = content.split("\\bibliographystyle")[0]
        after_maketitle = before_bib.split("\\maketitle")
        
        if len(after_maketitle) >= 2:
            # Remove any existing section inputs
            section_part = after_maketitle[1]
            # Remove lines that contain \input{sections/
            lines = section_part.split('\n')
            cleaned_lines = []
            for line in lines:
                if not (line.strip().startswith('\\input{sections/') or 
                       'Sections will be automatically inserted here' in line):
                    cleaned_lines.append(line)
            
            # Build new content
            new_content = after_maketitle[0] + "\\maketitle\n"
            new_content += '\n'.join(cleaned_lines)
            
            # Add section inputs
            new_content += "\n% === Auto-generated section includes ===\n"
            for section_file in section_files:
                section_name = section_file.stem
                new_content += f"\\input{{sections/{section_name}}}\n"
            
            new_content += "\n\\bibliographystyle{ieeetr}\n"
            new_content += content.split("\\bibliographystyle")[1]
            
            # Write updated main.tex
            try:
                with open(main_tex_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"[SUCCESS] main.tex updated with {len(section_files)} sections:")
                for section_file in section_files:
                    print(f"  • {section_file.stem}.tex")
                
                return True
            except Exception as e:
                print(f"[ERROR] Could not write main.tex: {e}")
                return False
        else:
            print("[ERROR] Could not find \\maketitle in main.tex")
            return False
    else:
        print("[ERROR] main.tex format not recognized")
        return False

def fetch_doi_citation(doi):
    """Fetch BibTeX citation from DOI using CrossRef API"""
    print(f"[API] Fetching citation for DOI: {doi}")
    
    # CrossRef API endpoint
    url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
    
    headers = {
        "User-Agent": "ModuTex/1.0 (mailto:user@example.com)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            bibtex = response.text
            
            # Append to references.bib
            bib_dir = Path("bib")
            bib_dir.mkdir(exist_ok=True)
            
            bib_file = bib_dir / "references.bib"
            with open(bib_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{bibtex}\n")
            
            print(f"[SUCCESS] Citation added to bib/references.bib")
            
            # Show preview
            print(f"\n[PREVIEW] Citation:")
            print("=" * 60)
            print(bibtex[:200] + "..." if len(bibtex) > 200 else bibtex)
            print("=" * 60)
            
            return True
            
        else:
            print(f"[ERROR] DOI not found or invalid (HTTP {response.status_code})")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False

def show_config():
    """Show current configuration"""
    print("ModuTex AI Configuration:")
    print("=" * 50)
    
    api_key = os.environ.get('OPENAI_API_KEY', 'not_set')
    if api_key == 'not_set' or api_key == 'your_api_key' or not api_key:
        print("API Key: NOT SET")
        print("Get key from: https://platform.openai.com/api-keys")
    else:
        masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 15 else "SET"
        print(f"API Key: CONFIGURED ({masked_key})")
    
    model = select_model()
    print(f"Model: {model} ({MODELS.get(model, 'Unknown')})")
    
    print(f"Working Directory: {Path.cwd()}")
    print(f"Sections Directory: {'EXISTS' if Path('sections').exists() else 'MISSING'}")
    print(f"Bibliography Directory: {'EXISTS' if Path('bib').exists() else 'MISSING'}")

def main():
    parser = argparse.ArgumentParser(
        description="ModuTex v1.0 - Professional AI-Powered LaTeX Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python texchat.py add_section methodology "Machine learning methodology"
  python texchat.py edit_section introduction "Add more mathematical background"
  python texchat.py text_to_latex my_text.txt result_section
  python texchat.py cite_doi 10.1038/nature12373
  python texchat.py update_main
  python texchat.py config
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add section command
    section_parser = subparsers.add_parser('add_section', help='Generate LaTeX section using AI')
    section_parser.add_argument('name', help='Section filename (without .tex)')
    section_parser.add_argument('prompt', help='Content description prompt')
    
    # Edit section command
    edit_parser = subparsers.add_parser('edit_section', help='Edit existing section with AI')
    edit_parser.add_argument('name', help='Section filename (without .tex)')
    edit_parser.add_argument('prompt', help='Edit instructions')
    
    # Text to LaTeX command
    text_parser = subparsers.add_parser('text_to_latex', help='Convert plain text to LaTeX')
    text_parser.add_argument('text_file', help='Input text file path')
    text_parser.add_argument('output_name', nargs='?', help='Output filename (optional)')
    
    # Update main.tex command
    update_parser = subparsers.add_parser('update_main', help='Update main.tex with all sections')
    
    # Cite DOI command
    cite_parser = subparsers.add_parser('cite_doi', help='Fetch BibTeX citation from DOI')
    cite_parser.add_argument('doi', help='DOI to fetch citation for')
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Show current configuration')
    
    args = parser.parse_args()
    
    if args.command == 'add_section':
        success = generate_section(args.name, args.prompt)
        sys.exit(0 if success else 1)
        
    elif args.command == 'edit_section':
        success = edit_section(args.name, args.prompt)
        sys.exit(0 if success else 1)
        
    elif args.command == 'text_to_latex':
        success = text_to_latex(args.text_file, args.output_name)
        sys.exit(0 if success else 1)
        
    elif args.command == 'update_main':
        success = update_main_tex()
        sys.exit(0 if success else 1)
        
    elif args.command == 'cite_doi':
        success = fetch_doi_citation(args.doi)
        sys.exit(0 if success else 1)
        
    elif args.command == 'config':
        show_config()
        sys.exit(0)
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 
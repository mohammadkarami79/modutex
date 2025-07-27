#!/usr/bin/env python3
"""
ModuTex GUI Application v1.0
Beautiful Professional Desktop Interface for AI-Powered LaTeX Content Generation
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, font
import threading
import subprocess
import sys
import os
from pathlib import Path
import time
import json

# Try to import customtkinter for modern look
try:
    import customtkinter as ctk
    ctk.set_appearance_mode("light")  # Professional light theme
    ctk.set_default_color_theme("blue")  # Professional blue theme
    USE_CUSTOM_TK = True
except ImportError:
    USE_CUSTOM_TK = False

# Import our AI functions
try:
    from texchat import (
        edit_section, generate_section, text_to_latex, 
        fetch_doi_citation, update_main_tex, show_config,
        get_openai_key
    )
    AI_AVAILABLE = True
except ImportError:
    print("Warning: AI functions not available. Running in demo mode.")
    AI_AVAILABLE = False
    # Fallback functions
    def edit_section(*args): return True
    def generate_section(*args): return True
    def text_to_latex(*args): return True
    def fetch_doi_citation(*args): return True
    def update_main_tex(*args): return True
    def show_config(*args): pass
    def get_openai_key(): return "demo_key"

class ModuTexGUI:
    def __init__(self):
        # Color scheme - Professional and beautiful
        self.colors = {
            'primary': '#2E86AB',      # Professional blue
            'secondary': '#A23B72',    # Elegant purple
            'success': '#F18F01',      # Warm orange
            'background': '#F8F9FA',   # Light gray
            'surface': '#FFFFFF',      # Pure white
            'text': '#2D3748',         # Dark gray
            'text_light': '#718096',   # Light gray
            'accent': '#E2E8F0',       # Very light gray
            'warning': '#ED8936',      # Orange
            'error': '#E53E3E'         # Red
        }
        
        # Create main window
        if USE_CUSTOM_TK:
            self.root = ctk.CTk()
            self.root.configure(fg_color=self.colors['background'])
        else:
            self.root = tk.Tk()
            self.root.configure(bg=self.colors['background'])
            
        self.setup_main_window()
        self.create_styles()
        self.create_widgets()
        self.update_status()
        
    def setup_main_window(self):
        """Configure the main application window with beautiful styling"""
        self.root.title("ModuTex Application v1.0 - Professional LaTeX Generator")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Configure grid weights for responsive design
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
    def create_styles(self):
        """Create beautiful styles for the application"""
        if not USE_CUSTOM_TK:
            self.style = ttk.Style()
            self.style.theme_use('clam')
            
            # Configure beautiful styles
            self.style.configure('Title.TLabel', 
                               font=('Segoe UI', 24, 'bold'),
                               foreground=self.colors['primary'],
                               background=self.colors['background'])
            
            self.style.configure('Subtitle.TLabel',
                               font=('Segoe UI', 12),
                               foreground=self.colors['text_light'],
                               background=self.colors['background'])
            
            self.style.configure('Header.TLabel',
                               font=('Segoe UI', 14, 'bold'),
                               foreground=self.colors['text'],
                               background=self.colors['surface'])
            
            self.style.configure('Custom.TButton',
                               font=('Segoe UI', 11),
                               padding=(20, 10))
            
            self.style.configure('Action.TButton',
                               font=('Segoe UI', 10, 'bold'),
                               padding=(15, 8))
        
    def create_widgets(self):
        """Create all GUI widgets with beautiful styling"""
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
    def create_header(self):
        """Create a beautiful application header"""
        if USE_CUSTOM_TK:
            header_frame = ctk.CTkFrame(self.root, fg_color=self.colors['surface'], corner_radius=15)
        else:
            header_frame = tk.Frame(self.root, bg=self.colors['surface'], relief='raised', bd=1)
            
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo and title section
        title_frame = tk.Frame(header_frame, bg=self.colors['surface'])
        title_frame.grid(row=0, column=0, sticky="w", padx=30, pady=20)
        
        # Main title with beautiful font
        if USE_CUSTOM_TK:
            title_label = ctk.CTkLabel(
                title_frame,
                text="🚀 ModuTex Application",
                font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
                text_color=self.colors['primary']
            )
        else:
            title_label = tk.Label(
                title_frame,
                text="🚀 ModuTex Application",
                font=('Segoe UI', 24, 'bold'),
                fg=self.colors['primary'],
                bg=self.colors['surface']
            )
        title_label.pack(anchor="w")
        
        # Version and subtitle
        if USE_CUSTOM_TK:
            subtitle_label = ctk.CTkLabel(
                title_frame,
                text="v1.0 Professional AI-Powered LaTeX Generator",
                font=ctk.CTkFont(family="Segoe UI", size=14),
                text_color=self.colors['text_light']
            )
        else:
            subtitle_label = tk.Label(
                title_frame,
                text="v1.0 Professional AI-Powered LaTeX Generator",
                font=('Segoe UI', 12),
                fg=self.colors['text_light'],
                bg=self.colors['surface']
            )
        subtitle_label.pack(anchor="w")
        
        # Status panel
        status_frame = tk.Frame(header_frame, bg=self.colors['surface'])
        status_frame.grid(row=0, column=2, sticky="e", padx=30, pady=20)
        
        # API Status with beautiful styling
        self.api_status_frame = tk.Frame(status_frame, bg=self.colors['accent'], relief='solid', bd=1)
        self.api_status_frame.pack(pady=5)
        
        self.api_status_label = tk.Label(
            self.api_status_frame,
            text="🔑 API Status: Checking...",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['accent'],
            padx=15,
            pady=8
        )
        self.api_status_label.pack()
        
    def create_main_content(self):
        """Create the beautiful main content area"""
        # Main container with elegant styling
        if USE_CUSTOM_TK:
            main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        else:
            main_frame = tk.Frame(self.root, bg=self.colors['background'])
            
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Left panel - Controls with beautiful styling
        self.create_left_panel(main_frame)
        
        # Right panel - Content/Output with beautiful styling
        self.create_right_panel(main_frame)
        
    def create_left_panel(self, parent):
        """Create the beautiful left control panel"""
        if USE_CUSTOM_TK:
            left_frame = ctk.CTkFrame(parent, fg_color=self.colors['surface'], corner_radius=15)
        else:
            left_frame = tk.Frame(parent, bg=self.colors['surface'], relief='raised', bd=2)
            
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_frame.grid_columnconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)  # Make sections area expandable
        left_frame.grid_rowconfigure(2, weight=2)  # Make buttons area expandable
        
        # Sections display with beautiful header
        self.create_sections_display(left_frame)
        
        # Action buttons with beautiful styling and scrolling
        self.create_action_buttons(left_frame)
        
    def create_sections_display(self, parent):
        """Create beautiful current sections display"""
        # Header with icon and styling
        header_frame = tk.Frame(parent, bg=self.colors['surface'])
        header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=20)
        
        if USE_CUSTOM_TK:
            sections_label = ctk.CTkLabel(
                header_frame,
                text="📋 Current Sections",
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color=self.colors['text']
            )
        else:
            sections_label = tk.Label(
                header_frame,
                text="📋 Current Sections",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['surface']
            )
        sections_label.pack(anchor="w")
        
        # Beautiful sections container
        sections_container = tk.Frame(parent, bg=self.colors['surface'])
        sections_container.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 20))
        sections_container.grid_columnconfigure(0, weight=1)
        sections_container.grid_rowconfigure(0, weight=1)
        
        # Listbox with beautiful styling
        self.sections_listbox = tk.Listbox(
            sections_container,
            height=8,
            font=('Segoe UI', 10),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white',
            relief='flat',
            bd=0,
            highlightthickness=1,
            highlightcolor=self.colors['primary'],
            activestyle='none'  # Better visual feedback
        )
        
        # Scrollbar with styling
        scrollbar = ttk.Scrollbar(sections_container, orient="vertical")
        self.sections_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sections_listbox.yview)
        
        self.sections_listbox.grid(row=0, column=0, sticky="nsew", pady=10)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        
        # Enable mousewheel scrolling for sections list
        self._bind_listbox_mousewheel(self.sections_listbox)
    
    def _bind_listbox_mousewheel(self, widget):
        """Bind mouse wheel events for listbox scrolling"""
        def _on_listbox_mousewheel(event):
            widget.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        
        widget.bind("<MouseWheel>", _on_listbox_mousewheel)
        widget.bind("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))
        widget.bind("<Button-5>", lambda e: widget.yview_scroll(1, "units"))
        
    def create_action_buttons(self, parent):
        """Create beautiful action buttons with scrolling"""
        # Header
        button_header_frame = tk.Frame(parent, bg=self.colors['surface'])
        button_header_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=(20, 10))
        
        if USE_CUSTOM_TK:
            buttons_label = ctk.CTkLabel(
                button_header_frame,
                text="🎯 Actions",
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color=self.colors['text']
            )
        else:
            buttons_label = tk.Label(
                button_header_frame,
                text="🎯 Actions",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['surface']
            )
        buttons_label.pack(anchor="w")
        
        # Create scrollable button area
        button_main_frame = tk.Frame(parent, bg=self.colors['surface'])
        button_main_frame.grid(row=3, column=0, sticky="nsew", padx=25, pady=(0, 25))
        button_main_frame.grid_columnconfigure(0, weight=1)
        button_main_frame.grid_rowconfigure(0, weight=1)
        
        # Create canvas and scrollbar for scrolling
        self.button_canvas = tk.Canvas(
            button_main_frame, 
            bg=self.colors['surface'],
            highlightthickness=0,
            bd=0
        )
        self.button_scrollbar = ttk.Scrollbar(
            button_main_frame, 
            orient="vertical", 
            command=self.button_canvas.yview
        )
        self.button_canvas.configure(yscrollcommand=self.button_scrollbar.set)
        
        # Pack canvas and scrollbar
        self.button_canvas.grid(row=0, column=0, sticky="nsew")
        self.button_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Create frame inside canvas for buttons
        self.button_container = tk.Frame(self.button_canvas, bg=self.colors['surface'])
        self.canvas_window = self.button_canvas.create_window(
            0, 0, anchor="nw", window=self.button_container
        )
        
        # Configure scrolling
        self.button_container.bind("<Configure>", self._on_button_frame_configure)
        self.button_canvas.bind("<Configure>", self._on_button_canvas_configure)
        
        # Enable mouse wheel scrolling
        self._bind_mousewheel(self.button_canvas)
        
        # Beautiful buttons with icons and styling
        buttons = [
            ("📝 Edit Section with AI", self.edit_section_dialog, self.colors['primary']),
            ("🔄 Convert Text to LaTeX", self.convert_text_dialog, self.colors['secondary']),
            ("✨ Generate New Section", self.generate_section_dialog, self.colors['success']),
            ("📚 Add Citation from DOI", self.add_citation_dialog, self.colors['primary']),
            ("📋 Manage Sections", self.manage_sections_dialog, self.colors['text']),
            ("🚀 Compile PDF", self.compile_pdf, self.colors['success']),
            ("⚙️ Configuration", self.show_configuration, self.colors['text_light'])
        ]
        
        # Configure button container grid
        self.button_container.grid_columnconfigure(0, weight=1)
        
        for i, (text, command, color) in enumerate(buttons):
            if USE_CUSTOM_TK:
                btn = ctk.CTkButton(
                    self.button_container,
                    text=text,
                    command=command,
                    height=45,
                    font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
                    fg_color=color,
                    hover_color=self._darken_color(color),
                    corner_radius=10
                )
            else:
                btn = tk.Button(
                    self.button_container,
                    text=text,
                    command=command,
                    font=('Segoe UI', 10, 'bold'),
                    bg=color,
                    fg='white',
                    activebackground=self._darken_color(color),
                    activeforeground='white',
                    relief='flat',
                    bd=0,
                    pady=12,
                    cursor='hand2'
                )
            btn.grid(row=i, column=0, pady=8, sticky="ew", padx=10)
    
    def _on_button_frame_configure(self, event):
        """Update scroll region when button frame size changes"""
        self.button_canvas.configure(scrollregion=self.button_canvas.bbox("all"))
        
    def _on_button_canvas_configure(self, event):
        """Update button container width when canvas width changes"""
        canvas_width = event.width
        self.button_canvas.itemconfig(self.canvas_window, width=canvas_width-30)  # Account for scrollbar
        
    def _bind_mousewheel(self, widget):
        """Bind mouse wheel events for scrolling"""
        def _on_mousewheel(event):
            if self.button_canvas.winfo_exists():
                self.button_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind to canvas and all child widgets
        widget.bind("<MouseWheel>", _on_mousewheel)
        widget.bind("<Button-4>", lambda e: self.button_canvas.yview_scroll(-1, "units"))
        widget.bind("<Button-5>", lambda e: self.button_canvas.yview_scroll(1, "units"))
        
        # Also bind to button container for better UX
        self.button_container.bind("<MouseWheel>", _on_mousewheel)
        self.button_container.bind("<Button-4>", lambda e: self.button_canvas.yview_scroll(-1, "units"))
        self.button_container.bind("<Button-5>", lambda e: self.button_canvas.yview_scroll(1, "units"))
    
    def _bind_text_mousewheel(self, widget):
        """Bind mouse wheel events for text widget scrolling"""
        def _on_text_mousewheel(event):
            if hasattr(widget, 'yview_scroll'):
                widget.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        
        widget.bind("<MouseWheel>", _on_text_mousewheel)
        widget.bind("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))
        widget.bind("<Button-5>", lambda e: widget.yview_scroll(1, "units"))
            
    def _darken_color(self, color):
        """Darken a color for hover effects"""
        color_map = {
            self.colors['primary']: '#1E5F7A',
            self.colors['secondary']: '#7A2356',
            self.colors['success']: '#C17001',
            self.colors['text']: '#1A202C',
            self.colors['text_light']: '#4A5568'
        }
        return color_map.get(color, color)
        
    def create_right_panel(self, parent):
        """Create the beautiful right content panel"""
        if USE_CUSTOM_TK:
            right_frame = ctk.CTkFrame(parent, fg_color=self.colors['surface'], corner_radius=15)
        else:
            right_frame = tk.Frame(parent, bg=self.colors['surface'], relief='raised', bd=2)
            
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        # Header with beautiful styling
        output_header_frame = tk.Frame(right_frame, bg=self.colors['surface'])
        output_header_frame.grid(row=0, column=0, sticky="ew", padx=25, pady=20)
        
        if USE_CUSTOM_TK:
            output_label = ctk.CTkLabel(
                output_header_frame,
                text="📄 Output & Status",
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color=self.colors['text']
            )
        else:
            output_label = tk.Label(
                output_header_frame,
                text="📄 Output & Status",
                font=('Segoe UI', 14, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['surface']
            )
        output_label.pack(anchor="w")
        
        # Beautiful text output area
        text_container = tk.Frame(right_frame, bg=self.colors['surface'])
        text_container.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 25))
        text_container.grid_columnconfigure(0, weight=1)
        text_container.grid_rowconfigure(0, weight=1)
        
        if USE_CUSTOM_TK:
            self.output_text = ctk.CTkTextbox(
                text_container,
                font=ctk.CTkFont(family="Consolas", size=11),
                fg_color=self.colors['accent'],
                corner_radius=10,
                wrap="word"
            )
        else:
            self.output_text = scrolledtext.ScrolledText(
                text_container,
                wrap=tk.WORD,
                font=('Consolas', 10),
                bg=self.colors['accent'],
                fg=self.colors['text'],
                relief='flat',
                bd=0,
                padx=15,
                pady=15,
                state=tk.NORMAL
            )
        self.output_text.grid(row=0, column=0, sticky="nsew")
        
        # Enable mousewheel scrolling for output text
        self._bind_text_mousewheel(self.output_text)
        
        # Welcome message with beautiful formatting
        welcome_msg = """🎉 Welcome to ModuTex Professional Desktop Application!

✨ Your Beautiful AI-Powered LaTeX Generator is Ready!

🎯 Quick Start Guide:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 📝 Configure your OpenAI API key (⚙️ Configuration)
2. 🤖 Use AI tools to create and edit sections
3. 📚 Add citations automatically from DOI
4. 🚀 Compile your beautiful PDF document

🎨 Beautiful Features Ready:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 📝 Edit existing sections with AI guidance
• 🔄 Convert plain text to professional LaTeX
• ✨ Generate new sections from prompts
• 📚 Automatic citation management from DOI
• 📋 Smart section organization
• 🚀 One-click PDF compilation

Ready to create amazing LaTeX documents! 🚀✨
"""
        self.log_message(welcome_msg)
        
    def create_footer(self):
        """Create a beautiful application footer"""
        if USE_CUSTOM_TK:
            footer_frame = ctk.CTkFrame(self.root, fg_color=self.colors['surface'], corner_radius=15, height=60)
        else:
            footer_frame = tk.Frame(self.root, bg=self.colors['surface'], relief='raised', bd=1, height=60)
            
        footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        footer_frame.grid_columnconfigure(1, weight=1)
        footer_frame.grid_propagate(False)
        
        # Progress bar with beautiful styling
        progress_frame = tk.Frame(footer_frame, bg=self.colors['surface'])
        progress_frame.grid(row=0, column=0, padx=25, pady=15, sticky="w")
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=200,
            style='Custom.Horizontal.TProgressbar'
        )
        self.progress.pack()
        
        # Status text with beautiful font
        self.status_label = tk.Label(
            footer_frame,
            text="🎯 Ready to create amazing content",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        )
        self.status_label.grid(row=0, column=1, padx=25, pady=15, sticky="w")
        
        # Version info with elegant styling
        version_label = tk.Label(
            footer_frame,
            text="ModuTex v1.0 | Built with ❤️ for Researchers",
            font=('Segoe UI', 9, 'italic'),
            fg=self.colors['text_light'],
            bg=self.colors['surface']
        )
        version_label.grid(row=0, column=2, padx=25, pady=15, sticky="e")
        
    def update_status(self):
        """Update API status and sections list with beautiful styling"""
        # Check API key
        if AI_AVAILABLE:
            api_key = get_openai_key()
            if api_key and api_key != "your_api_key":
                self.api_status_label.config(
                    text="🔑 API Status: ✅ Ready",
                    fg='white',
                    bg=self.colors['success']
                )
                self.api_status_frame.config(bg=self.colors['success'])
            else:
                self.api_status_label.config(
                    text="🔑 API Status: ⚙️ Setup Required",
                    fg='white',
                    bg=self.colors['warning']
                )
                self.api_status_frame.config(bg=self.colors['warning'])
        else:
            self.api_status_label.config(
                text="🔑 API Status: 🎭 Demo Mode",
                fg='white',
                bg=self.colors['secondary']
            )
            self.api_status_frame.config(bg=self.colors['secondary'])
            
        # Update sections list
        self.update_sections_list()
        
        # Schedule next update
        self.root.after(5000, self.update_status)
        
    def update_sections_list(self):
        """Update the sections list display with beautiful formatting"""
        self.sections_listbox.delete(0, tk.END)
        
        sections_dir = Path("sections")
        if sections_dir.exists():
            section_files = sorted(sections_dir.glob("*.tex"))
            if section_files:
                for file in section_files:
                    self.sections_listbox.insert(tk.END, f"📄 {file.stem}.tex")
            else:
                self.sections_listbox.insert(tk.END, "📝 No sections yet - Create your first!")
        else:
            self.sections_listbox.insert(tk.END, "📁 Sections folder will be created automatically")
                    
    def log_message(self, message):
        """Add a beautifully formatted message to the output area"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        if USE_CUSTOM_TK:
            # For CTkTextbox, append at the end and scroll to bottom
            self.output_text.insert("end", formatted_message)
            # Scroll to bottom
            self.output_text.see("end")
        else:
            # Ensure text widget is in normal state for editing
            current_state = self.output_text.cget("state")
            self.output_text.config(state=tk.NORMAL)
            
            # Insert message at the end
            self.output_text.insert(tk.END, formatted_message)
            
            # Auto-scroll to bottom to show latest message
            self.output_text.see(tk.END)
            
            # Restore original state if it was different
            if current_state != tk.NORMAL:
                self.output_text.config(state=current_state)
            
        self.root.update_idletasks()
        
    def set_status(self, text):
        """Update status label with beautiful formatting"""
        self.status_label.config(text=f"🔄 {text}")
        
    def start_progress(self):
        """Start beautiful progress indicator"""
        self.progress.start()
        
    def stop_progress(self):
        """Stop progress indicator"""
        self.progress.stop()
        
    def run_ai_task(self, task_func, *args, **kwargs):
        """Run an AI task in a separate thread with beautiful feedback"""
        def worker():
            try:
                self.start_progress()
                self.set_status("Processing AI request...")
                self.log_message("🤖 Starting AI processing...")
                
                result = task_func(*args, **kwargs)
                
                if result:
                    self.log_message("✅ Task completed successfully!")
                    self.set_status("Task completed successfully!")
                else:
                    self.log_message("❌ Task failed. Please check your configuration.")
                    self.set_status("Task failed - check configuration")
                    
            except Exception as e:
                self.log_message(f"❌ Error: {str(e)}")
                self.set_status(f"Error: {str(e)}")
            finally:
                self.stop_progress()
                self.set_status("Ready to create amazing content")
                self.update_sections_list()
                
        thread = threading.Thread(target=worker)
        thread.daemon = True
        thread.start()
        
    # Dialog methods with beautiful interfaces
    def edit_section_dialog(self):
        """Show beautiful edit section dialog"""
        dialog = EditSectionDialog(self.root, self)
        
    def convert_text_dialog(self):
        """Show beautiful convert text dialog"""
        dialog = ConvertTextDialog(self.root, self)
        
    def generate_section_dialog(self):
        """Show beautiful generate section dialog"""
        dialog = GenerateSectionDialog(self.root, self)
        
    def add_citation_dialog(self):
        """Show beautiful add citation dialog"""
        dialog = AddCitationDialog(self.root, self)
        
    def manage_sections_dialog(self):
        """Show beautiful section management dialog"""
        dialog = ManageSectionsDialog(self.root, self)
        
    def compile_pdf(self):
        """Compile PDF with beautiful progress feedback"""
        def compile_worker():
            try:
                self.start_progress()
                self.set_status("Compiling beautiful PDF...")
                self.log_message("🚀 Starting PDF compilation...")
                self.log_message("📄 Processing LaTeX document...")
                
                # Run compile.bat
                result = subprocess.run(
                    ["compile.bat"],
                    capture_output=True,
                    text=True,
                    cwd=Path.cwd()
                )
                
                if result.returncode == 0:
                    self.log_message("✅ PDF compiled successfully!")
                    self.log_message("📄 Beautiful PDF document created!")
                    
                    if Path("main.pdf").exists():
                        self.log_message("🎉 Opening your beautiful PDF...")
                        try:
                            os.startfile("main.pdf")
                        except:
                            self.log_message("📂 PDF saved as main.pdf")
                    
                    self.set_status("PDF compilation successful!")
                else:
                    error_msg = result.stderr.strip() if result.stderr else "Unknown compilation error"
                    self.log_message(f"❌ Compilation failed: {error_msg}")
                    self.set_status("Compilation failed - check output")
                    
            except Exception as e:
                self.log_message(f"❌ Compilation error: {str(e)}")
                self.set_status(f"Compilation error: {str(e)}")
            finally:
                self.stop_progress()
                
        thread = threading.Thread(target=compile_worker)
        thread.daemon = True
        thread.start()
        
    def show_configuration(self):
        """Show beautiful configuration dialog"""
        dialog = ConfigurationDialog(self.root, self)


class BaseDialog:
    """Beautiful base class for all dialogs"""
    def __init__(self, parent, main_app):
        self.parent = parent
        self.main_app = main_app
        
        # Color scheme
        self.colors = main_app.colors
        
        if USE_CUSTOM_TK:
            self.dialog = ctk.CTkToplevel(parent)
            self.dialog.configure(fg_color=self.colors['background'])
        else:
            self.dialog = tk.Toplevel(parent)
            self.dialog.configure(bg=self.colors['background'])
            
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(True, True)
        
        # Center the dialog
        self.center_dialog()
        
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_title(self, title, subtitle=""):
        """Create beautiful dialog title"""
        title_frame = tk.Frame(self.dialog, bg=self.colors['surface'], relief='raised', bd=2)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title_label = tk.Label(
            title_frame,
            text=title,
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['surface']
        )
        title_label.pack(pady=(15, 5))
        
        if subtitle:
            subtitle_label = tk.Label(
                title_frame,
                text=subtitle,
                font=('Segoe UI', 10),
                fg=self.colors['text_light'],
                bg=self.colors['surface']
            )
            subtitle_label.pack(pady=(0, 15))


class EditSectionDialog(BaseDialog):
    """Beautiful dialog for editing sections with AI"""
    def __init__(self, parent, main_app):
        super().__init__(parent, main_app)
        self.dialog.title("Edit Section with AI")
        self.dialog.geometry("600x500")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_title("📝 Edit Section with AI", "Improve your content with AI assistance")
        
        # Main content frame
        content_frame = tk.Frame(self.dialog, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Section selection with beautiful styling
        section_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        section_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            section_frame,
            text="📄 Select Section:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Get available sections
        sections_dir = Path("sections")
        section_files = []
        if sections_dir.exists():
            section_files = [f.stem for f in sections_dir.glob("*.tex")]
            
        self.section_var = tk.StringVar()
        self.section_combo = ttk.Combobox(
            section_frame,
            values=section_files,
            textvariable=self.section_var,
            state="readonly",
            font=('Segoe UI', 11)
        )
        self.section_combo.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Instructions with beautiful styling
        instructions_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        instructions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            instructions_frame,
            text="✨ Improvement Instructions:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        # Example text
        example_text = "Examples: 'Add mathematical equations', 'Include recent research', 'Improve academic tone'"
        tk.Label(
            instructions_frame,
            text=example_text,
            font=('Segoe UI', 9, 'italic'),
            fg=self.colors['text_light'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        self.instructions_text = scrolledtext.ScrolledText(
            instructions_frame,
            height=8,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors['accent'],
            fg=self.colors['text']
        )
        self.instructions_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Buttons with beautiful styling
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        improve_btn = tk.Button(
            button_frame,
            text="✨ Improve Section",
            command=self.edit_section,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['primary']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        improve_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            font=('Segoe UI', 11),
            bg=self.colors['text_light'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['text_light']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.RIGHT)
        
    def edit_section(self):
        section_name = self.section_var.get()
        instructions = self.instructions_text.get("1.0", tk.END).strip()
            
        if not section_name or not instructions:
            messagebox.showwarning(
                "Missing Information", 
                "Please select a section and provide improvement instructions."
            )
            return
            
        self.main_app.log_message(f"🤖 Improving section '{section_name}' with AI...")
        self.dialog.destroy()
        
        self.main_app.run_ai_task(edit_section, section_name, instructions)


class GenerateSectionDialog(BaseDialog):
    """Beautiful dialog for generating new sections"""
    def __init__(self, parent, main_app):
        super().__init__(parent, main_app)
        self.dialog.title("Generate New Section")
        self.dialog.geometry("600x550")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_title("✨ Generate New Section", "Create professional content with AI")
        
        # Main content frame
        content_frame = tk.Frame(self.dialog, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Section name with beautiful styling
        name_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        name_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            name_frame,
            text="📝 Section Name:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.name_entry = tk.Entry(
            name_frame,
            font=('Segoe UI', 11),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            relief='flat',
            bd=5
        )
        self.name_entry.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.name_entry.insert(0, "e.g., introduction, methodology, results")
        self.name_entry.bind('<FocusIn>', self.clear_placeholder)
        
        # Content description with beautiful styling
        content_frame_inner = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        content_frame_inner.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            content_frame_inner,
            text="💡 Content Description:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        example_text = "Describe what you want in this section. Be specific for better results!"
        tk.Label(
            content_frame_inner,
            text=example_text,
            font=('Segoe UI', 9, 'italic'),
            fg=self.colors['text_light'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(0, 10))
        
        self.content_text = scrolledtext.ScrolledText(
            content_frame_inner,
            height=10,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors['accent'],
            fg=self.colors['text']
        )
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        generate_btn = tk.Button(
            button_frame,
            text="✨ Generate Section",
            command=self.generate_section,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['success']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            font=('Segoe UI', 11),
            bg=self.colors['text_light'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['text_light']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.RIGHT)
        
    def clear_placeholder(self, event):
        if self.name_entry.get().startswith("e.g.,"):
            self.name_entry.delete(0, tk.END)
        
    def generate_section(self):
        section_name = self.name_entry.get().strip()
        content_desc = self.content_text.get("1.0", tk.END).strip()
            
        if not section_name or not content_desc or section_name.startswith("e.g.,"):
            messagebox.showwarning(
                "Missing Information", 
                "Please provide section name and description."
            )
            return
            
        self.main_app.log_message(f"🤖 Generating new section '{section_name}'...")
        self.dialog.destroy()
        
        def generate_and_update():
            success = generate_section(section_name, content_desc)
            if success:
                update_main_tex()
                
        self.main_app.run_ai_task(generate_and_update)


# Similar beautiful dialogs for other functions...
class ConvertTextDialog(BaseDialog):
    """Beautiful dialog for converting text to LaTeX"""
    def __init__(self, parent, main_app):
        super().__init__(parent, main_app)
        self.dialog.title("Convert Text to LaTeX")
        self.dialog.geometry("700x600")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_title("🔄 Convert Text to LaTeX", "Transform plain text to professional LaTeX")
        
        # Main content
        content_frame = tk.Frame(self.dialog, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Text input
        text_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            text_frame,
            text="📝 Plain Text Content:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        self.text_input = scrolledtext.ScrolledText(
            text_frame,
            height=15,
            wrap=tk.WORD,
            font=('Segoe UI', 11),
            bg=self.colors['accent'],
            fg=self.colors['text']
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Target section
        target_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        target_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            target_frame,
            text="🎯 Target Section Name:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.target_entry = tk.Entry(
            target_frame,
            font=('Segoe UI', 11),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            relief='flat',
            bd=5
        )
        self.target_entry.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        convert_btn = tk.Button(
            button_frame,
            text="🔄 Convert to LaTeX",
            command=self.convert_text,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['secondary']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        convert_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            font=('Segoe UI', 11),
            bg=self.colors['text_light'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['text_light']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.RIGHT)
        
    def convert_text(self):
        text_content = self.text_input.get("1.0", tk.END).strip()
        target_name = self.target_entry.get().strip()
        
        if not text_content or not target_name:
            messagebox.showwarning(
                "Missing Information", 
                "Please provide text content and target section name."
            )
            return
            
        # Save text to temporary file
        temp_file = "temp_convert.txt"
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(text_content)
                
            self.main_app.log_message(f"🔄 Converting text to LaTeX format...")
            self.dialog.destroy()
            
            def convert_and_cleanup():
                success = text_to_latex(temp_file, target_name)
                try:
                    os.remove(temp_file)
                except:
                    pass
                return success
                
            self.main_app.run_ai_task(convert_and_cleanup)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process text: {str(e)}")


class AddCitationDialog(BaseDialog):
    """Beautiful dialog for adding citations"""
    def __init__(self, parent, main_app):
        super().__init__(parent, main_app)
        self.dialog.title("Add Citation from DOI")
        self.dialog.geometry("500x350")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_title("📚 Add Citation from DOI", "Automatically fetch academic references")
        
        # Main content
        content_frame = tk.Frame(self.dialog, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # DOI input
        doi_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        doi_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            doi_frame,
            text="🔗 DOI:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        self.doi_entry = tk.Entry(
            doi_frame,
            font=('Segoe UI', 11),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            relief='flat',
            bd=5
        )
        self.doi_entry.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Examples
        examples_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        examples_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            examples_frame,
            text="💡 Examples:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        examples_text = """• 10.1038/nature12373 (Nature journal)
• 10.1145/3372297.3417501 (ACM conference)
• 10.1109/TPAMI.2021.3065203 (IEEE journal)

Just paste the DOI and we'll fetch the complete citation automatically!"""
        
        tk.Label(
            examples_frame,
            text=examples_text,
            font=('Segoe UI', 10),
            fg=self.colors['text'],
            bg=self.colors['surface'],
            justify=tk.LEFT
        ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        fetch_btn = tk.Button(
            button_frame,
            text="📚 Fetch Citation",
            command=self.fetch_citation,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['primary']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        fetch_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            font=('Segoe UI', 11),
            bg=self.colors['text_light'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['text_light']),
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.RIGHT)
        
    def fetch_citation(self):
        doi = self.doi_entry.get().strip()
        
        if not doi:
            messagebox.showwarning("Missing DOI", "Please enter a DOI.")
            return
            
        self.main_app.log_message(f"📚 Fetching citation for DOI: {doi}")
        self.dialog.destroy()
        
        self.main_app.run_ai_task(fetch_doi_citation, doi)


class ManageSectionsDialog(BaseDialog):
    """Beautiful dialog for section management"""
    def __init__(self, parent, main_app):
        super().__init__(parent, main_app)
        self.dialog.title("Section Management")
        self.dialog.geometry("600x500")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_title("📋 Section Management", "Organize your document structure")
        
        # Main content
        content_frame = tk.Frame(self.dialog, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Sections list
        list_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            list_frame,
            text="📄 Current Sections:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        list_container = tk.Frame(list_frame, bg=self.colors['surface'])
        list_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.sections_list = tk.Listbox(
            list_container,
            font=('Segoe UI', 10),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            selectbackground=self.colors['primary'],
            selectforeground='white'
        )
        scrollbar = ttk.Scrollbar(list_container, orient="vertical")
        self.sections_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.sections_list.yview)
        
        self.sections_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Update sections list
        self.update_sections()
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        create_btn = tk.Button(
            button_frame,
            text="➕ Create Empty",
            command=self.create_section,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['success'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['success']),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        create_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_btn = tk.Button(
            button_frame,
            text="🗑️ Delete",
            command=self.delete_section,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['error'],
            fg='white',
            activebackground='#C53030',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        sync_btn = tk.Button(
            button_frame,
            text="🔄 Sync main.tex",
            command=self.sync_main,
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['primary']),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        sync_btn.pack(side=tk.LEFT)
        
    def update_sections(self):
        self.sections_list.delete(0, tk.END)
        sections_dir = Path("sections")
        if sections_dir.exists():
            for file in sorted(sections_dir.glob("*.tex")):
                self.sections_list.insert(tk.END, f"📄 {file.stem}")
                
    def create_section(self):
        from tkinter import simpledialog
        name = simpledialog.askstring("Create Section", "Section name:")
        if name:
            section_path = Path("sections") / f"{name}.tex"
            section_path.parent.mkdir(exist_ok=True)
            section_path.write_text(f"% TODO: Add content for {name} section\n")
            self.update_sections()
            self.main_app.log_message(f"✅ Created empty section: {name}.tex")
            
    def delete_section(self):
        selection = self.sections_list.curselection()
        if selection:
            section_name = self.sections_list.get(selection[0]).replace("📄 ", "")
            if messagebox.askyesno("Delete Section", f"Delete {section_name}.tex?"):
                section_path = Path("sections") / f"{section_name}.tex"
                section_path.unlink(missing_ok=True)
                self.update_sections()
                self.main_app.log_message(f"🗑️ Deleted section: {section_name}.tex")
        else:
            messagebox.showwarning("No Selection", "Please select a section to delete.")
            
    def sync_main(self):
        self.main_app.log_message("🔄 Syncing main.tex with current sections...")
        self.main_app.run_ai_task(update_main_tex)


class ConfigurationDialog(BaseDialog):
    """Beautiful dialog for configuration"""
    def __init__(self, parent, main_app):
        super().__init__(parent, main_app)
        self.dialog.title("Configuration")
        self.dialog.geometry("600x450")
        self.create_widgets()
        
    def create_widgets(self):
        self.create_title("⚙️ Configuration", "Setup your AI and system preferences")
        
        # Main content
        content_frame = tk.Frame(self.dialog, bg=self.colors['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # API Key section
        api_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        api_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            api_frame,
            text="🔑 OpenAI API Configuration",
            font=('Segoe UI', 14, 'bold'),
            fg=self.colors['primary'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Current status
        if AI_AVAILABLE:
            api_key = get_openai_key()
            status_text = "✅ Configured and Ready" if api_key and api_key != "your_api_key" else "❌ Not Configured"
        else:
            status_text = "🎭 Demo Mode Active"
        
        tk.Label(
            api_frame,
            text=f"Status: {status_text}",
            font=('Segoe UI', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(0, 15))
        
        # Instructions
        instructions_frame = tk.Frame(content_frame, bg=self.colors['surface'], relief='raised', bd=1)
        instructions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(
            instructions_frame,
            text="📝 Setup Instructions:",
            font=('Segoe UI', 12, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['surface']
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        instructions = """🔹 Visit: https://platform.openai.com/api-keys
🔹 Create a new API key
🔹 Click "Edit .env File" below
🔹 Add: OPENAI_API_KEY=sk-proj-your_key_here
🔹 Save the file and restart the application

💡 Your API key will be kept secure and only used for AI features."""
        
        instruction_text = tk.Text(
            instructions_frame,
            height=8,
            wrap=tk.WORD,
            font=('Segoe UI', 10),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            relief='flat',
            bd=0,
            padx=10,
            pady=10
        )
        instruction_text.insert("1.0", instructions)
        instruction_text.config(state=tk.DISABLED)
        instruction_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        edit_btn = tk.Button(
            button_frame,
            text="📝 Edit .env File",
            command=self.edit_env_file,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['primary']),
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=self.dialog.destroy,
            font=('Segoe UI', 11),
            bg=self.colors['text_light'],
            fg='white',
            activebackground=self.main_app._darken_color(self.colors['text_light']),
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2'
        )
        close_btn.pack(side=tk.RIGHT)
        
    def edit_env_file(self):
        try:
            os.startfile(".env")
        except:
            messagebox.showinfo(
                "Manual Edit", 
                "Please edit the .env file manually with a text editor.\n\nAdd this line:\nOPENAI_API_KEY=sk-proj-your_actual_key_here"
            )


def main():
    """Main application entry point"""
    print("🎨 Starting ModuTex Beautiful Desktop Application...")
    
    # Create the beautiful GUI application
    try:
        app = ModuTexGUI()
        
        # Set window icon if available
        try:
            if hasattr(app.root, 'iconbitmap'):
                app.root.iconbitmap('icon.ico')
        except:
            pass
            
        print("✅ Beautiful GUI loaded successfully!")
        print("🚀 Launching application...")
        
        # Start the main loop
        app.root.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main() 
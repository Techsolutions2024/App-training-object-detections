"""
YOLO Training GUI Application
Giao diện đào tạo mô hình YOLO với đầy đủ tính năng
Author: Computer Vision Expert
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import re

class YOLOTrainerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO Training Studio - by Techsolutions")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e2e")
        
        # Variables
        self.training_thread = None
        self.is_training = False
        self.current_epoch = 0
        self.total_epochs = 0
        self.training_process = None
        
        # Style configuration
        self.setup_styles()
        
        # Create main layout
        self.create_layout()
        
        # Load saved config if exists
        self.load_config()
        
    def setup_styles(self):
        """Thiết lập styles cho giao diện hiện đại"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        self.colors = {
            'bg_dark': '#1e1e2e',
            'bg_medium': '#2a2a3e',
            'bg_light': '#363654',
            'accent': '#00d4ff',
            'accent_hover': '#00a8cc',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'text': '#e0e0e0',
            'text_dim': '#a0a0a0'
        }
        
        # Configure styles
        style.configure('TFrame', background=self.colors['bg_dark'])
        style.configure('Card.TFrame', background=self.colors['bg_medium'], relief='raised')
        
        style.configure('TLabel', 
                       background=self.colors['bg_dark'], 
                       foreground=self.colors['text'],
                       font=('Segoe UI', 10))
        
        style.configure('Title.TLabel', 
                       background=self.colors['bg_dark'], 
                       foreground=self.colors['accent'],
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       background=self.colors['bg_medium'], 
                       foreground=self.colors['text'],
                       font=('Segoe UI', 11, 'bold'))
        
        style.configure('TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('TButton',
                 background=[('active', self.colors['accent_hover'])])
        
        style.configure('Success.TButton',
                       background=self.colors['success'])
        
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_light'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='flat')
        
        style.configure('TCombobox',
                       fieldbackground=self.colors['bg_light'],
                       background=self.colors['bg_light'],
                       foreground=self.colors['text'],
                       arrowcolor=self.colors['accent'])
        
        style.configure('Horizontal.TProgressbar',
                       background=self.colors['accent'],
                       troughcolor=self.colors['bg_light'],
                       borderwidth=0,
                       thickness=25)
        
    def create_layout(self):
        """Tạo layout chính của ứng dụng"""
        # Header
        header = ttk.Frame(self.root)
        header.pack(fill='x', padx=20, pady=(20, 10))
        
        title = ttk.Label(header, text="🚀 YOLO Training Studio by Techsolutions", style='Title.TLabel')
        title.pack(side='left')
        
        version = ttk.Label(header, text="v1.0 0395458706 ", 
                           foreground=self.colors['text_dim'])
        version.pack(side='right', pady=5)
        
        # Main container with notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Tab 1: Setup & Configuration
        self.setup_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.setup_tab, text="⚙️ Setup & Configuration")
        self.create_setup_tab()
        
        # Tab 2: Training
        self.training_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.training_tab, text="🎯 Training")
        self.create_training_tab()
        
        # Tab 3: Results
        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="📊 Results & Analysis")
        self.create_results_tab()
        
        # Status bar
        self.create_status_bar()
        
    def create_setup_tab(self):
        """Tab cài đặt môi trường và cấu hình"""
        # Left panel - Environment Setup
        left_panel = ttk.Frame(self.setup_tab, style='Card.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(10, 5), pady=10)
        
        # Environment section
        env_label = ttk.Label(left_panel, text="🔧 Environment Setup", style='Subtitle.TLabel')
        env_label.pack(anchor='w', padx=15, pady=(15, 10))
        
        # Python info
        python_frame = ttk.Frame(left_panel)
        python_frame.pack(fill='x', padx=15, pady=5)
        
        ttk.Label(python_frame, text="Python Version:").pack(side='left')
        python_ver = ttk.Label(python_frame, text=f"{sys.version.split()[0]}", 
                              foreground=self.colors['success'])
        python_ver.pack(side='left', padx=10)
        
        # Install dependencies button
        install_btn = ttk.Button(left_panel, text="📦 Install Dependencies",
                                command=self.install_dependencies)
        install_btn.pack(fill='x', padx=15, pady=10)
        
        # Check environment button
        check_btn = ttk.Button(left_panel, text="✓ Check Environment",
                              command=self.check_environment)
        check_btn.pack(fill='x', padx=15, pady=5)
        
        # Environment status
        self.env_status = scrolledtext.ScrolledText(left_panel, height=10,
                                                    bg=self.colors['bg_light'],
                                                    fg=self.colors['text'],
                                                    font=('Consolas', 9))
        self.env_status.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Right panel - Model Configuration
        right_panel = ttk.Frame(self.setup_tab, style='Card.TFrame')
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 10), pady=10)
        
        # Model selection
        model_label = ttk.Label(right_panel, text="🤖 Model Configuration", style='Subtitle.TLabel')
        model_label.pack(anchor='w', padx=15, pady=(15, 10))
        
        # Pretrained model selection
        model_frame = ttk.Frame(right_panel)
        model_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Label(model_frame, text="Select Pretrained Model:").pack(anchor='w', pady=(0, 5))
        
        self.model_var = tk.StringVar(value="yolov8n.pt")
        models = [
            "yolov8n.pt", "yolov8s.pt", "yolov8m.pt", "yolov8l.pt", "yolov8x.pt",
            "yolov10n.pt", "yolov10s.pt", "yolov10m.pt", "yolov10l.pt", "yolov10x.pt",
            "yolo11n.pt", "yolo11s.pt", "yolo11m.pt", "yolo11l.pt", "yolo11x.pt",
            "yolo12n.pt", "yolo12s.pt", "yolo12m.pt", "yolo12l.pt", "yolo12x.pt",
        ]
        
        model_combo = ttk.Combobox(model_frame, textvariable=self.model_var, 
                                   values=models, state='readonly', width=30)
        model_combo.pack(fill='x')
        
        # Custom model upload
        custom_frame = ttk.Frame(right_panel)
        custom_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Label(custom_frame, text="Or Upload Custom Model:").pack(anchor='w', pady=(0, 5))
        
        upload_btn_frame = ttk.Frame(custom_frame)
        upload_btn_frame.pack(fill='x')
        
        self.custom_model_path = tk.StringVar(value="")
        custom_entry = ttk.Entry(upload_btn_frame, textvariable=self.custom_model_path, 
                                state='readonly')
        custom_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(upload_btn_frame, text="Browse", 
                               command=self.browse_model, width=10)
        browse_btn.pack(side='right')
        
        # Dataset configuration
        dataset_frame = ttk.Frame(right_panel)
        dataset_frame.pack(fill='x', padx=15, pady=10)
        
        ttk.Label(dataset_frame, text="Dataset YAML File:").pack(anchor='w', pady=(0, 5))
        
        dataset_btn_frame = ttk.Frame(dataset_frame)
        dataset_btn_frame.pack(fill='x')
        
        self.dataset_path = tk.StringVar(value="helmat.v1i.yolov11/data.yaml")
        dataset_entry = ttk.Entry(dataset_btn_frame, textvariable=self.dataset_path)
        dataset_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        dataset_browse = ttk.Button(dataset_btn_frame, text="Browse", 
                                   command=self.browse_dataset, width=10)
        dataset_browse.pack(side='right')
        
        # Training parameters
        params_label = ttk.Label(right_panel, text="⚡ Training Parameters", 
                                style='Subtitle.TLabel')
        params_label.pack(anchor='w', padx=15, pady=(20, 10))
        
        # Create scrollable frame for parameters
        params_canvas = tk.Canvas(right_panel, bg=self.colors['bg_medium'], 
                                 highlightthickness=0, height=300)
        params_scrollbar = ttk.Scrollbar(right_panel, orient="vertical", 
                                        command=params_canvas.yview)
        params_frame = ttk.Frame(params_canvas)
        
        params_frame.bind(
            "<Configure>",
            lambda e: params_canvas.configure(scrollregion=params_canvas.bbox("all"))
        )
        
        params_canvas.create_window((0, 0), window=params_frame, anchor="nw")
        params_canvas.configure(yscrollcommand=params_scrollbar.set)
        
        params_canvas.pack(side="left", fill="both", expand=True, padx=15)
        params_scrollbar.pack(side="right", fill="y")
        
        # Parameters dictionary
        self.params = {}
        
        param_configs = [
            ("epochs", "Epochs", "100"),
            ("imgsz", "Image Size", "768"),
            ("batch", "Batch Size", "8"),
            ("device", "Device (0=GPU, cpu=CPU)", "0"),
            ("workers", "Workers", "4"),
            ("optimizer", "Optimizer", "AdamW"),
            ("lr0", "Initial Learning Rate", "0.004"),
            ("lrf", "Final Learning Rate", "0.01"),
            ("weight_decay", "Weight Decay", "0.0005"),
            ("warmup_epochs", "Warmup Epochs", "5"),
            ("hsv_h", "HSV Hue", "0.02"),
            ("hsv_s", "HSV Saturation", "0.7"),
            ("hsv_v", "HSV Value", "0.5"),
            ("mosaic", "Mosaic", "1.0"),
            ("close_mosaic", "Close Mosaic", "20"),
            ("mixup", "Mixup", "0.15"),
            ("copy_paste", "Copy Paste", "0.3"),
            ("conf", "Confidence Threshold", "0.001"),
            ("iou", "IOU Threshold", "0.7"),
            ("patience", "Patience", "50"),
        ]
        
        for i, (key, label, default) in enumerate(param_configs):
            row = ttk.Frame(params_frame)
            row.pack(fill='x', pady=3, padx=5)
            
            ttk.Label(row, text=label, width=25).pack(side='left')
            
            var = tk.StringVar(value=default)
            self.params[key] = var
            
            entry = ttk.Entry(row, textvariable=var, width=15)
            entry.pack(side='right')
        
        # Boolean parameters
        bool_frame = ttk.Frame(params_frame)
        bool_frame.pack(fill='x', pady=10, padx=5)
        
        self.cos_lr_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bool_frame, text="Cosine LR", variable=self.cos_lr_var).pack(side='left', padx=5)
        
        self.amp_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bool_frame, text="AMP", variable=self.amp_var).pack(side='left', padx=5)
        
        self.pretrained_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bool_frame, text="Pretrained", variable=self.pretrained_var).pack(side='left', padx=5)
        
        self.plots_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(bool_frame, text="Plots", variable=self.plots_var).pack(side='left', padx=5)
        
        # Save/Load config buttons
        config_frame = ttk.Frame(right_panel)
        config_frame.pack(fill='x', padx=15, pady=15)
        
        save_config_btn = ttk.Button(config_frame, text="💾 Save Config", 
                                     command=self.save_config)
        save_config_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        load_config_btn = ttk.Button(config_frame, text="📂 Load Config", 
                                     command=self.load_config_file)
        load_config_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
    def create_training_tab(self):
        """Tab training với log và progress"""
        # Top section - Controls
        control_frame = ttk.Frame(self.training_tab, style='Card.TFrame')
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # Start/Stop buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(pady=15)
        
        self.start_btn = ttk.Button(btn_frame, text="▶️ Start Training", 
                                    command=self.start_training,
                                    style='Success.TButton', width=20)
        self.start_btn.pack(side='left', padx=10)
        
        self.stop_btn = ttk.Button(btn_frame, text="⏹️ Stop Training", 
                                   command=self.stop_training,
                                   state='disabled', width=20)
        self.stop_btn.pack(side='left', padx=10)
        
        # Progress section
        progress_frame = ttk.Frame(self.training_tab, style='Card.TFrame')
        progress_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Label(progress_frame, text="📈 Training Progress", 
                 style='Subtitle.TLabel').pack(anchor='w', padx=15, pady=(15, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                           maximum=100, mode='determinate',
                                           style='Horizontal.TProgressbar')
        self.progress_bar.pack(fill='x', padx=15, pady=10)
        
        # Progress text
        self.progress_text = ttk.Label(progress_frame, 
                                      text="Ready to start training...",
                                      foreground=self.colors['text_dim'])
        self.progress_text.pack(padx=15, pady=(0, 15))
        
        # Training metrics
        metrics_frame = ttk.Frame(progress_frame)
        metrics_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        # Create metric displays
        self.metric_labels = {}
        metrics = [
            ("epoch", "Epoch", "0/0"),
            ("loss", "Loss", "N/A"),
            ("precision", "Precision", "N/A"),
            ("recall", "Recall", "N/A"),
            ("mAP50", "mAP@50", "N/A"),
            ("mAP50-95", "mAP@50-95", "N/A"),
        ]
        
        for i, (key, label, default) in enumerate(metrics):
            col = i % 3
            row = i // 3
            
            metric_box = ttk.Frame(metrics_frame, style='Card.TFrame')
            metric_box.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            ttk.Label(metric_box, text=label, 
                     foreground=self.colors['text_dim']).pack(pady=(5, 0))
            
            value_label = ttk.Label(metric_box, text=default, 
                                   font=('Segoe UI', 14, 'bold'),
                                   foreground=self.colors['accent'])
            value_label.pack(pady=(0, 5))
            
            self.metric_labels[key] = value_label
            
            metrics_frame.columnconfigure(col, weight=1)
        
        # Log section
        log_frame = ttk.Frame(self.training_tab, style='Card.TFrame')
        log_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        ttk.Label(log_frame, text="📝 Training Log", 
                 style='Subtitle.TLabel').pack(anchor='w', padx=15, pady=(15, 10))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20,
                                                  bg=self.colors['bg_dark'],
                                                  fg=self.colors['text'],
                                                  font=('Consolas', 9),
                                                  wrap=tk.WORD)
        self.log_text.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Configure log tags for colored output
        self.log_text.tag_config('info', foreground=self.colors['text'])
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('error', foreground=self.colors['error'])
        
    def create_results_tab(self):
        """Tab hiển thị kết quả training"""
        # Results directory
        results_control = ttk.Frame(self.results_tab, style='Card.TFrame')
        results_control.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(results_control, text="📊 Training Results", 
                 style='Subtitle.TLabel').pack(anchor='w', padx=15, pady=(15, 10))
        
        # Results path
        path_frame = ttk.Frame(results_control)
        path_frame.pack(fill='x', padx=15, pady=(0, 15))
        
        ttk.Label(path_frame, text="Results Directory:").pack(side='left', padx=(0, 10))
        
        self.results_path = tk.StringVar(value="runs/detect/train")
        results_entry = ttk.Entry(path_frame, textvariable=self.results_path, width=40)
        results_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_folder_btn = ttk.Button(path_frame, text="📂 Browse", 
                                       command=self.browse_results_folder, width=12)
        browse_folder_btn.pack(side='left', padx=(0, 5))
        
        refresh_btn = ttk.Button(path_frame, text="🔄 Refresh", 
                                command=self.load_results, width=12)
        refresh_btn.pack(side='left', padx=(0, 5))
        
        open_folder_btn = ttk.Button(path_frame, text="📁 Open Folder", 
                                    command=self.open_results_folder, width=12)
        open_folder_btn.pack(side='left')
        
        # Results display area
        results_display = ttk.Frame(self.results_tab, style='Card.TFrame')
        results_display.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Create notebook for different result views
        results_notebook = ttk.Notebook(results_display)
        results_notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Summary tab
        summary_frame = ttk.Frame(results_notebook)
        results_notebook.add(summary_frame, text="Summary")
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame,
                                                      bg=self.colors['bg_dark'],
                                                      fg=self.colors['text'],
                                                      font=('Consolas', 10))
        self.summary_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Plots tab
        plots_frame = ttk.Frame(results_notebook)
        results_notebook.add(plots_frame, text="Plots")
        
        self.plots_list = tk.Listbox(plots_frame, 
                                     bg=self.colors['bg_dark'],
                                     fg=self.colors['text'],
                                     font=('Segoe UI', 10))
        self.plots_list.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        plots_scrollbar = ttk.Scrollbar(plots_frame, command=self.plots_list.yview)
        plots_scrollbar.pack(side='right', fill='y')
        self.plots_list.config(yscrollcommand=plots_scrollbar.set)
        
        self.plots_list.bind('<Double-Button-1>', self.open_plot)
        
        # Weights tab
        weights_frame = ttk.Frame(results_notebook)
        results_notebook.add(weights_frame, text="Model Weights")
        
        self.weights_text = scrolledtext.ScrolledText(weights_frame,
                                                      bg=self.colors['bg_dark'],
                                                      fg=self.colors['text'],
                                                      font=('Consolas', 10))
        self.weights_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def create_status_bar(self):
        """Tạo status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', side='bottom', padx=20, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Ready", 
                                      foreground=self.colors['success'])
        self.status_label.pack(side='left')
        
        self.time_label = ttk.Label(status_frame, text="", 
                                    foreground=self.colors['text_dim'])
        self.time_label.pack(side='right')
        
        self.update_time()
        
    def update_time(self):
        """Update current time"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    # Environment functions
    def install_dependencies(self):
        """Cài đặt thư viện phụ thuộc"""
        self.log_to_env("Installing dependencies from requirements.txt...\n", 'info')
        
        def install():
            try:
                process = subprocess.Popen(
                    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=os.path.dirname(os.path.abspath(__file__))
                )
                
                for line in process.stdout:
                    self.log_to_env(line, 'info')
                    
                process.wait()
                
                if process.returncode == 0:
                    self.log_to_env("\n✓ Dependencies installed successfully!\n", 'success')
                else:
                    self.log_to_env("\n✗ Installation failed!\n", 'error')
                    
            except Exception as e:
                self.log_to_env(f"\n✗ Error: {str(e)}\n", 'error')
        
        thread = threading.Thread(target=install, daemon=True)
        thread.start()
        
    def check_environment(self):
        """Kiểm tra môi trường"""
        self.env_status.delete(1.0, tk.END)
        self.log_to_env("Checking environment...\n\n", 'info')
        
        # Check Python
        self.log_to_env(f"✓ Python: {sys.version}\n", 'success')
        
        # Check key packages
        packages = ['ultralytics', 'torch', 'torchvision', 'opencv-python', 'numpy']
        
        for package in packages:
            try:
                __import__(package.replace('-', '_'))
                self.log_to_env(f"✓ {package}: Installed\n", 'success')
            except ImportError:
                self.log_to_env(f"✗ {package}: Not installed\n", 'error')
        
        # Check CUDA
        try:
            import torch
            if torch.cuda.is_available():
                self.log_to_env(f"\n✓ CUDA: Available (GPU: {torch.cuda.get_device_name(0)})\n", 'success')
            else:
                self.log_to_env("\n⚠ CUDA: Not available (will use CPU)\n", 'warning')
        except:
            self.log_to_env("\n⚠ Could not check CUDA\n", 'warning')
            
    def log_to_env(self, message, tag='info'):
        """Log to environment status"""
        self.env_status.insert(tk.END, message, tag)
        self.env_status.see(tk.END)
        self.env_status.update()
        
    # Model selection functions
    def browse_model(self):
        """Browse for custom model file"""
        filename = filedialog.askopenfilename(
            title="Select Model File",
            filetypes=[("PyTorch Model", "*.pt"), ("All Files", "*.*")]
        )
        if filename:
            self.custom_model_path.set(filename)
            
    def browse_dataset(self):
        """Browse for dataset YAML file"""
        filename = filedialog.askopenfilename(
            title="Select Dataset YAML",
            filetypes=[("YAML File", "*.yaml *.yml"), ("All Files", "*.*")]
        )
        if filename:
            self.dataset_path.set(filename)
            
    # Config functions
    def save_config(self):
        """Save current configuration"""
        config = {
            'model': self.model_var.get(),
            'custom_model': self.custom_model_path.get(),
            'dataset': self.dataset_path.get(),
            'params': {k: v.get() for k, v in self.params.items()},
            'bool_params': {
                'cos_lr': self.cos_lr_var.get(),
                'amp': self.amp_var.get(),
                'pretrained': self.pretrained_var.get(),
                'plots': self.plots_var.get()
            }
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON File", "*.json"), ("All Files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
    def load_config_file(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            title="Select Config File",
            filetypes=[("JSON File", "*.json"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                
                self.model_var.set(config.get('model', 'yolov8n.pt'))
                self.custom_model_path.set(config.get('custom_model', ''))
                self.dataset_path.set(config.get('dataset', ''))
                
                for k, v in config.get('params', {}).items():
                    if k in self.params:
                        self.params[k].set(v)
                
                bool_params = config.get('bool_params', {})
                self.cos_lr_var.set(bool_params.get('cos_lr', True))
                self.amp_var.set(bool_params.get('amp', True))
                self.pretrained_var.set(bool_params.get('pretrained', True))
                self.plots_var.set(bool_params.get('plots', True))
                
                messagebox.showinfo("Success", "Configuration loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {str(e)}")
                
    def load_config(self):
        """Load default config if exists"""
        config_file = "yolo_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                self.dataset_path.set(config.get('dataset', 'helmat.v1i.yolov11/data.yaml'))
            except:
                pass
                
    # Training functions
    def start_training(self):
        """Bắt đầu training"""
        if self.is_training:
            messagebox.showwarning("Warning", "Training is already in progress!")
            return
        
        # Validate inputs
        if not self.dataset_path.get():
            messagebox.showerror("Error", "Please select a dataset!")
            return
        
        # Get model path
        model_path = self.custom_model_path.get() if self.custom_model_path.get() else self.model_var.get()
        
        # Prepare training parameters
        try:
            epochs = int(self.params['epochs'].get())
            self.total_epochs = epochs
        except:
            messagebox.showerror("Error", "Invalid epochs value!")
            return
        
        # Update UI
        self.is_training = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="Training...", foreground=self.colors['warning'])
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        self.log_message("Starting YOLO training...\n", 'info')
        self.log_message(f"Model: {model_path}\n", 'info')
        self.log_message(f"Dataset: {self.dataset_path.get()}\n", 'info')
        self.log_message(f"Epochs: {epochs}\n\n", 'info')
        
        # Start training in separate thread
        self.training_thread = threading.Thread(target=self.run_training, 
                                               args=(model_path,), daemon=True)
        self.training_thread.start()
        
    def run_training(self, model_path):
        """Run training process"""
        try:
            # Build training script
            script_lines = [
                "from ultralytics import YOLO",
                "import sys",
                "",
                "def main():",
                f"    model = YOLO('{model_path}')",
                "    ",
                "    results = model.train(",
                f"        data='{self.dataset_path.get()}',",
            ]
            
            # Add parameters
            for key, var in self.params.items():
                value = var.get()
                if key in ['optimizer']:
                    script_lines.append(f"        {key}='{value}',")
                else:
                    script_lines.append(f"        {key}={value},")
            
            # Add boolean parameters
            script_lines.append(f"        cos_lr={self.cos_lr_var.get()},")
            script_lines.append(f"        amp={self.amp_var.get()},")
            script_lines.append(f"        pretrained={self.pretrained_var.get()},")
            script_lines.append(f"        plots={self.plots_var.get()},")
            script_lines.append("    )")
            script_lines.append("")
            script_lines.append("if __name__ == '__main__':")
            script_lines.append("    main()")
            
            script_content = "\n".join(script_lines)
            
            # Save training script
            script_path = "temp_train.py"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Run training
            self.training_process = subprocess.Popen(
                [sys.executable, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output
            for line in self.training_process.stdout:
                if not self.is_training:
                    break
                    
                self.log_message(line, 'info')
                self.parse_training_output(line)
            
            self.training_process.wait()
            
            # Training completed
            if self.is_training:
                self.log_message("\n✓ Training completed successfully!\n", 'success')
                self.status_label.config(text="Training completed", 
                                        foreground=self.colors['success'])
                self.progress_var.set(100)
                self.progress_text.config(text="Training completed!")
            else:
                self.log_message("\n⚠ Training stopped by user\n", 'warning')
                
        except Exception as e:
            self.log_message(f"\n✗ Error during training: {str(e)}\n", 'error')
            self.status_label.config(text="Training failed", foreground=self.colors['error'])
        finally:
            self.is_training = False
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            
            # Clean up
            if os.path.exists("temp_train.py"):
                try:
                    os.remove("temp_train.py")
                except:
                    pass
                    
    def stop_training(self):
        """Stop training process"""
        if self.training_process:
            self.is_training = False
            self.training_process.terminate()
            self.log_message("\nStopping training...\n", 'warning')
            
    def parse_training_output(self, line):
        """Parse training output to update metrics"""
        # Parse epoch
        epoch_match = re.search(r'Epoch\s+(\d+)/(\d+)', line)
        if epoch_match:
            current = int(epoch_match.group(1))
            total = int(epoch_match.group(2))
            self.current_epoch = current
            self.total_epochs = total
            
            progress = (current / total) * 100
            self.progress_var.set(progress)
            self.progress_text.config(text=f"Epoch {current}/{total} ({progress:.1f}%)")
            self.metric_labels['epoch'].config(text=f"{current}/{total}")
        
        # Parse metrics (simplified - actual parsing depends on ultralytics output format)
        # You may need to adjust these regex patterns based on actual output
        
        # Loss
        loss_match = re.search(r'loss:\s*([\d.]+)', line, re.IGNORECASE)
        if loss_match:
            self.metric_labels['loss'].config(text=f"{float(loss_match.group(1)):.4f}")
        
        # Precision
        precision_match = re.search(r'precision:\s*([\d.]+)', line, re.IGNORECASE)
        if precision_match:
            self.metric_labels['precision'].config(text=f"{float(precision_match.group(1)):.4f}")
        
        # Recall
        recall_match = re.search(r'recall:\s*([\d.]+)', line, re.IGNORECASE)
        if recall_match:
            self.metric_labels['recall'].config(text=f"{float(recall_match.group(1)):.4f}")
        
        # mAP50
        map50_match = re.search(r'mAP50:\s*([\d.]+)', line, re.IGNORECASE)
        if map50_match:
            self.metric_labels['mAP50'].config(text=f"{float(map50_match.group(1)):.4f}")
        
        # mAP50-95
        map5095_match = re.search(r'mAP50-95:\s*([\d.]+)', line, re.IGNORECASE)
        if map5095_match:
            self.metric_labels['mAP50-95'].config(text=f"{float(map5095_match.group(1)):.4f}")
            
    def log_message(self, message, tag='info'):
        """Log message to training log"""
        self.log_text.insert(tk.END, message, tag)
        self.log_text.see(tk.END)
        self.log_text.update()
        
    # Results functions
    def load_results(self):
        """Load training results"""
        results_dir = self.results_path.get()
        
        if not os.path.exists(results_dir):
            messagebox.showwarning("Warning", "Results directory not found!")
            return
        
        # Load summary
        self.summary_text.delete(1.0, tk.END)
        
        # Check for results.csv or results.txt
        results_file = os.path.join(results_dir, "results.csv")
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                self.summary_text.insert(tk.END, f.read())
        else:
            self.summary_text.insert(tk.END, "No results file found.\n")
            self.summary_text.insert(tk.END, f"Looking in: {results_dir}\n")
        
        # Load plots
        self.plots_list.delete(0, tk.END)
        
        plot_files = []
        if os.path.exists(results_dir):
            for file in os.listdir(results_dir):
                if file.endswith(('.png', '.jpg', '.jpeg')):
                    plot_files.append(os.path.join(results_dir, file))
                    self.plots_list.insert(tk.END, file)
        
        # Load weights info
        self.weights_text.delete(1.0, tk.END)
        weights_dir = os.path.join(results_dir, "weights")
        
        if os.path.exists(weights_dir):
            self.weights_text.insert(tk.END, f"Weights directory: {weights_dir}\n\n")
            for file in os.listdir(weights_dir):
                if file.endswith('.pt'):
                    file_path = os.path.join(weights_dir, file)
                    size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    self.weights_text.insert(tk.END, f"{file}: {size:.2f} MB\n")
        else:
            self.weights_text.insert(tk.END, "No weights found.\n")
            
    def browse_results_folder(self):
        """Browse for results folder"""
        folder = filedialog.askdirectory(
            title="Select Training Results Folder",
            initialdir=os.getcwd()
        )
        if folder:
            self.results_path.set(folder)
            # Automatically load results after selecting folder
            self.load_results()
            
    def open_results_folder(self):
        """Open results folder in file explorer"""
        results_dir = self.results_path.get()
        if os.path.exists(results_dir):
            os.startfile(results_dir)
        else:
            messagebox.showwarning("Warning", "Results directory not found!")
            
    def open_plot(self, event):
        """Open selected plot"""
        selection = self.plots_list.curselection()
        if selection:
            filename = self.plots_list.get(selection[0])
            file_path = os.path.join(self.results_path.get(), filename)
            if os.path.exists(file_path):
                os.startfile(file_path)


def main():
    root = tk.Tk()
    app = YOLOTrainerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

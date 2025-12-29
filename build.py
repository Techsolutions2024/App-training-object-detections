"""
Build Script for YOLO Training Studio
Đóng gói phần mềm thành file installer với PyInstaller và Inno Setup
Publisher: TxTech
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Configuration
APP_NAME = "YOLO Training Studio"
APP_VERSION = "1.0.0"
PUBLISHER = "TxTech"
MAIN_SCRIPT = "yolo_trainer_gui.py"
ICON_FILE = "app_icon.ico"  # Tạo icon nếu có
OUTPUT_DIR = "dist"
BUILD_DIR = "build"

class YOLOTrainerBuilder:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / OUTPUT_DIR
        self.build_dir = self.root_dir / BUILD_DIR
        
    def clean(self):
        """Xóa các thư mục build cũ"""
        print("🧹 Cleaning old build files...")
        
        dirs_to_clean = [self.dist_dir, self.build_dir, self.root_dir / "*.spec"]
        
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   ✓ Removed {dir_path}")
        
        # Remove spec files
        for spec_file in self.root_dir.glob("*.spec"):
            spec_file.unlink()
            print(f"   ✓ Removed {spec_file}")
            
        print("✓ Clean completed!\n")
        
    def check_dependencies(self):
        """Kiểm tra các dependencies cần thiết"""
        print("🔍 Checking dependencies...")
        
        try:
            import PyInstaller
            print(f"   ✓ PyInstaller: {PyInstaller.__version__}")
        except ImportError:
            print("   ✗ PyInstaller not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("   ✓ PyInstaller installed")
            
        print("✓ Dependencies check completed!\n")
        
    def create_icon(self):
        """Tạo icon cho ứng dụng (nếu chưa có)"""
        icon_path = self.root_dir / ICON_FILE
        
        if not icon_path.exists():
            print("⚠ Icon file not found. Creating default icon...")
            # Tạo icon đơn giản bằng PIL nếu có
            try:
                from PIL import Image, ImageDraw, ImageFont
                
                # Tạo icon 256x256
                size = 256
                img = Image.new('RGBA', (size, size), (30, 30, 46, 255))
                draw = ImageDraw.Draw(img)
                
                # Vẽ gradient background
                for i in range(size):
                    color = (0, int(212 * i / size), 255, 255)
                    draw.rectangle([(0, i), (size, i+1)], fill=color)
                
                # Vẽ text "YOLO"
                try:
                    font = ImageFont.truetype("arial.ttf", 80)
                except:
                    font = ImageFont.load_default()
                
                text = "YOLO"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                position = ((size - text_width) // 2, (size - text_height) // 2 - 20)
                
                # Shadow
                draw.text((position[0] + 3, position[1] + 3), text, 
                         fill=(0, 0, 0, 128), font=font)
                # Main text
                draw.text(position, text, fill=(255, 255, 255, 255), font=font)
                
                # Save as ICO
                img.save(str(icon_path), format='ICO', sizes=[(256, 256)])
                print(f"   ✓ Created icon: {icon_path}")
                
            except ImportError:
                print("   ⚠ PIL not available. Skipping icon creation.")
                print("   ℹ You can add a custom icon later as 'app_icon.ico'")
                return None
                
        return str(icon_path) if icon_path.exists() else None
        
    def build_exe(self):
        """Build executable với PyInstaller"""
        print("🔨 Building executable with PyInstaller...")
        
        icon_path = self.create_icon()
        
        # PyInstaller arguments
        args = [
            'pyinstaller',
            '--name=YOLOTrainingStudio',
            '--onefile',  # Single file
            '--windowed',  # No console window
            '--clean',
            f'--distpath={self.dist_dir}',
            f'--workpath={self.build_dir}',
        ]
        
        # Add icon if available
        if icon_path:
            args.append(f'--icon={icon_path}')
        
        # Add version info if available
        version_info_path = self.root_dir / 'version_info.txt'
        if version_info_path.exists():
            args.append(f'--version-file={version_info_path}')
        
        # Add metadata
        args.extend([
            f'--add-data=requirements.txt;.',  # Include requirements.txt
        ])
        
        # Hidden imports for common issues
        hidden_imports = [
            'tkinter',
            'tkinter.ttk',
            'tkinter.filedialog',
            'tkinter.messagebox',
            'tkinter.scrolledtext',
            'PIL',
            'PIL._tkinter_finder',
        ]
        
        for imp in hidden_imports:
            args.append(f'--hidden-import={imp}')
        
        # Main script
        args.append(MAIN_SCRIPT)
        
        print(f"   Running: {' '.join(args)}")
        
        try:
            subprocess.check_call(args, cwd=self.root_dir)
            print("✓ Executable built successfully!\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Build failed: {e}\n")
            return False
            
    def create_inno_setup_script(self):
        """Tạo Inno Setup script để build installer"""
        print("📝 Creating Inno Setup script...")
        
        exe_path = self.dist_dir / "YOLOTrainingStudio.exe"
        
        if not exe_path.exists():
            print("   ✗ Executable not found. Build exe first!")
            return None
            
        iss_content = f'''
; YOLO Training Studio Installer Script
; Generated by build.py
; Publisher: {PUBLISHER}

#define MyAppName "{APP_NAME}"
#define MyAppVersion "{APP_VERSION}"
#define MyAppPublisher "{PUBLISHER}"
#define MyAppURL "https://txtech.com"
#define MyAppExeName "YOLOTrainingStudio.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{{{B8F9E3D2-4A7C-4E9B-8F1D-2C5A6E8D9F3B}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile=
OutputDir={self.root_dir}\\installer
OutputBaseFilename=YOLOTrainingStudio_Setup_v{APP_VERSION}
SetupIconFile={self.root_dir / ICON_FILE if (self.root_dir / ICON_FILE).exists() else ""}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "{exe_path}"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{self.root_dir}\\requirements.txt"; DestDir: "{{app}}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{group}}\\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon
Name: "{{userappdata}}\\Microsoft\\Internet Explorer\\Quick Launch\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if Python is installed
  if not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore') then
  begin
    if MsgBox('Python is not detected on your system. YOLO Training Studio requires Python 3.8 or later.' + #13#10#13#10 + 
              'Would you like to continue anyway?', mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Optional: Run pip install requirements.txt
    if MsgBox('Would you like to install Python dependencies now?' + #13#10 + 
              '(This requires Python and pip to be installed)', mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec('cmd.exe', '/c pip install -r "' + ExpandConstant('{{app}}') + '\\requirements.txt"', 
           '', SW_SHOW, ewWaitUntilTerminated, ResultCode);
    end;
  end;
end;
'''
        
        iss_path = self.root_dir / "installer_script.iss"
        
        with open(iss_path, 'w', encoding='utf-8') as f:
            f.write(iss_content)
            
        print(f"   ✓ Created Inno Setup script: {iss_path}")
        return iss_path
        
    def build_installer(self):
        """Build installer với Inno Setup"""
        print("📦 Building installer with Inno Setup...")
        
        iss_path = self.create_inno_setup_script()
        
        if not iss_path:
            return False
            
        # Tìm Inno Setup compiler
        inno_paths = [
            r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
            r"C:\Program Files\Inno Setup 6\ISCC.exe",
            r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
            r"C:\Program Files\Inno Setup 5\ISCC.exe",
        ]
        
        iscc_path = None
        for path in inno_paths:
            if os.path.exists(path):
                iscc_path = path
                break
                
        if not iscc_path:
            print("   ⚠ Inno Setup not found!")
            print("   ℹ Please install Inno Setup from: https://jrsoftware.org/isdl.php")
            print(f"   ℹ Then run manually: ISCC.exe {iss_path}")
            return False
            
        try:
            subprocess.check_call([iscc_path, str(iss_path)])
            print("✓ Installer built successfully!")
            print(f"   📦 Installer location: {self.root_dir / 'installer'}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ✗ Installer build failed: {e}")
            return False
            
    def build_portable_zip(self):
        """Tạo phiên bản portable (ZIP)"""
        print("📦 Creating portable ZIP package...")
        
        exe_path = self.dist_dir / "YOLOTrainingStudio.exe"
        
        if not exe_path.exists():
            print("   ✗ Executable not found!")
            return False
            
        # Tạo thư mục portable
        portable_dir = self.root_dir / "portable" / "YOLOTrainingStudio"
        portable_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files
        shutil.copy2(exe_path, portable_dir / "YOLOTrainingStudio.exe")
        shutil.copy2(self.root_dir / "requirements.txt", portable_dir / "requirements.txt")
        
        # Create README
        readme_content = f"""
# {APP_NAME} v{APP_VERSION} - Portable Edition
Publisher: {PUBLISHER}

## Installation
1. Make sure Python 3.8+ is installed
2. Install dependencies: pip install -r requirements.txt
3. Run YOLOTrainingStudio.exe

## Features
- Environment setup and dependency installation
- Model selection (YOLOv8/v10/v11/v12)
- Training configuration
- Real-time training monitoring
- Results visualization

## Support
For support, please visit: https://txtech.com

© {PUBLISHER} - All rights reserved
"""
        
        with open(portable_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        # Create ZIP
        import zipfile
        
        zip_path = self.root_dir / f"YOLOTrainingStudio_v{APP_VERSION}_Portable.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in portable_dir.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(portable_dir.parent)
                    zipf.write(file, arcname)
                    
        print(f"   ✓ Created portable ZIP: {zip_path}")
        
        # Cleanup
        shutil.rmtree(self.root_dir / "portable")
        
        return True
        
    def build_all(self):
        """Build tất cả (exe + installer + portable)"""
        print("=" * 60)
        print(f"  {APP_NAME} v{APP_VERSION}")
        print(f"  Publisher: {PUBLISHER}")
        print("  Build Script")
        print("=" * 60)
        print()
        
        # Clean
        self.clean()
        
        # Check dependencies
        self.check_dependencies()
        
        # Build executable
        if not self.build_exe():
            print("\n❌ Build failed at executable stage!")
            return False
            
        # Build installer
        print()
        installer_success = self.build_installer()
        
        # Build portable
        print()
        portable_success = self.build_portable_zip()
        
        # Summary
        print("\n" + "=" * 60)
        print("  BUILD SUMMARY")
        print("=" * 60)
        print(f"✓ Executable: {self.dist_dir / 'YOLOTrainingStudio.exe'}")
        
        if installer_success:
            print(f"✓ Installer: {self.root_dir / 'installer' / f'YOLOTrainingStudio_Setup_v{APP_VERSION}.exe'}")
        else:
            print("⚠ Installer: Not created (Inno Setup required)")
            
        if portable_success:
            print(f"✓ Portable: {self.root_dir / f'YOLOTrainingStudio_v{APP_VERSION}_Portable.zip'}")
            
        print("\n🎉 Build completed successfully!")
        print(f"📦 Publisher: {PUBLISHER}")
        print("=" * 60)
        
        return True


def main():
    """Main build function"""
    builder = YOLOTrainerBuilder()
    
    # Parse arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'clean':
            builder.clean()
        elif command == 'exe':
            builder.check_dependencies()
            builder.build_exe()
        elif command == 'installer':
            builder.build_installer()
        elif command == 'portable':
            builder.build_portable_zip()
        elif command == 'all':
            builder.build_all()
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python build.py [command]")
            print("\nCommands:")
            print("  clean     - Clean build directories")
            print("  exe       - Build executable only")
            print("  installer - Build installer only")
            print("  portable  - Build portable ZIP only")
            print("  all       - Build everything (default)")
    else:
        # Default: build all
        builder.build_all()


if __name__ == "__main__":
    main()

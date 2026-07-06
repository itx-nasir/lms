; ─────────────────────────────────────────────────────────────────────────────
; Inno Setup script for Lab Management System
; Download Inno Setup free from: https://jrsoftware.org/isdl.php
; Compile this file with Inno Setup Compiler to produce LabManagementSetup.exe
; ─────────────────────────────────────────────────────────────────────────────

[Setup]
AppName=Lab Management System
AppVersion=1.0
AppPublisher=Your Lab Name
AppPublisherURL=
AppSupportURL=
AppCopyright=Your Lab Name

; Where the app is installed (e.g. C:\Program Files\LabManagementSystem)
DefaultDirName={autopf}\LabManagementSystem
DefaultGroupName=Lab Management System

; Output
OutputDir=installer_output
OutputBaseFilename=LabManagementSetup
SetupIconFile=icon.ico

; Compression
Compression=lzma2/ultra64
SolidCompression=yes

; Wizard appearance
WizardStyle=modern
WizardSmallImageFile=

; Minimum Windows version: Windows 7
MinVersion=6.1

; Does NOT require admin rights so it can install per-user if needed
; PrivilegesRequired=lowest   ← uncomment if you want per-user install

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";  Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: checkedonce
Name: "startupicon";  Description: "Start automatically when Windows starts"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; Copy entire PyInstaller output folder into the install directory
Source: "dist\LabManagement\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu
Name: "{group}\Lab Management System";         Filename: "{app}\LabManagement.exe"; WorkingDir: "{app}"
Name: "{group}\Uninstall Lab Management System"; Filename: "{uninstallexe}"

; Desktop shortcut (optional, shown only if task checked)
Name: "{commondesktop}\Lab Management System"; Filename: "{app}\LabManagement.exe"; WorkingDir: "{app}"; Tasks: desktopicon

; Startup folder (optional)
Name: "{userstartup}\Lab Management System";   Filename: "{app}\LabManagement.exe"; WorkingDir: "{app}"; Tasks: startupicon

[Run]
; After installation, offer to launch the app immediately
Filename: "{app}\LabManagement.exe"; Description: "Launch Lab Management System now"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any compiled Python cache left inside the install folder
Type: filesandordirs; Name: "{app}\__pycache__"

[Code]
{ Show a friendly page explaining login credentials }
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    MsgBox(
      'Installation complete!' + #13#10 + #13#10 +
      'To use the Lab Management System:' + #13#10 +
      '  1. Double-click the desktop shortcut (or Start Menu).' + #13#10 +
      '  2. A small control window will appear.' + #13#10 +
      '  3. Your browser will open automatically.' + #13#10 + #13#10 +
      'Default login credentials:' + #13#10 +
      '  Username : admin' + #13#10 +
      '  Password : admin123' + #13#10 + #13#10 +
      'Your data is stored in:' + #13#10 +
      '%APPDATA%\LabManagementSystem\lms.db' + #13#10 + #13#10 +
      'No internet connection is required.',
      mbInformation, MB_OK
    );
  end;
end;

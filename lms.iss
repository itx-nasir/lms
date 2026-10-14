[Setup]
AppName=Lab Management System
AppVersion=1.0
AppPublisher=Your Lab Name
DefaultDirName={autopf}\LabManagementSystem
DefaultGroupName=Lab Management System
OutputDir=installer_output
OutputBaseFilename=LabManagementSystem_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Files]
; Everything from PyInstaller output folder
Source: "dist\LabManagementSystem\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu
Name: "{group}\Lab Management System"; Filename: "{app}\LabManagementSystem.exe"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

; Desktop shortcut (only if user ticked)
Name: "{userdesktop}\Lab Management System"; Filename: "{app}\LabManagementSystem.exe"; Tasks: desktopicon

[Run]
; Launch app after install finishes
Filename: "{app}\LabManagementSystem.exe"; Description: "Launch Lab Management System"; Flags: nowait postinstall skipifsilent

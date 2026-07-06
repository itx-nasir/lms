[Setup]
AppName=Lab Management System
AppVersion=1.0
DefaultDirName={autopf}\LMS
DefaultGroupName=Lab Management System
OutputBaseFilename=LMS_Setup
OutputDir=installer_output
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\LMS\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Lab Management System"; Filename: "{app}\LMS.exe"
Name: "{commondesktop}\Lab Management System"; Filename: "{app}\LMS.exe"

[Run]
Filename: "{app}\LMS.exe"; Description: "Launch Lab Management System"; Flags: postinstall nowait skipifsilent
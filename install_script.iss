[Setup]
AppName=Password Manager
AppVersion=1.0
DefaultDirName={autopf}\Password Manager
DefaultGroupName=Password Manager
OutputDir=.
OutputBaseFilename=PasswordManagerInstaller
Compression=lzma
SolidCompression=yes

[Files]
; Učitaj novu verziju .exe fajla
Source: "PasswordManager.exe"; DestDir: "{app}"; Flags: ignoreversion
; Učitaj bazu podataka
Source: "password_manager.db"; DestDir: "{app}"; Flags: ignoreversion
; Ako želiš da imaš sliku, zadrži logo.png
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Password Manager"; Filename: "{app}\PasswordManager.exe"
Name: "{commondesktop}\Password Manager"; Filename: "{app}\PasswordManager.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: checkedonce

[Run]
Filename: "{app}\PasswordManager.exe"; Description: "Launch Password Manager"; Flags: nowait postinstall skipifsilent

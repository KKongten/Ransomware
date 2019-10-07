

reg add "hkcu\control panel\desktop" /v Wallpaper /t REG_SZ /d "C:\Users\user\Desktop\Ransomware\background.jpg" /f
reg add "hkcu\control panel\desktop" /v WallpaperStyle /t REG_SZ /d 10 /f
RUNDLL32.EXE user32.dll, UpdatePerUserSystemParameters ,1 ,True

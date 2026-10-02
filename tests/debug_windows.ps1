$ErrorActionPreference='SilentlyContinue'
$root = Split-Path -Parent $PSScriptRoot
Add-Type @"
using System; using System.Collections.Generic; using System.Runtime.InteropServices; using System.Text;
public class W2 {
  public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lParam);
  [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder sb, int max);
  public static List<string> All() {
    var res = new List<string>();
    EnumWindows((h, l) => {
      int p; GetWindowThreadProcessId(h, out p);
      var sb = new StringBuilder(512); GetWindowText(h, sb, 512);
      res.Add(p + "|" + h + "|vis=" + IsWindowVisible(h) + "|" + sb.ToString());
      return true;
    }, IntPtr.Zero);
    return res;
  }
}
"@
Remove-Item "$env:APPDATA\BabiProgrammeur\data.json" -Force
Remove-Item "$env:APPDATA\CodePulse\data.json" -Force
$p = Start-Process python -ArgumentList @('main.py','--demo') -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput "$env:TEMP\o.txt" -RedirectStandardError "$env:TEMP\e.txt" -PassThru
Start-Sleep -Seconds 9
$p.Refresh()
Write-Output ("exited=" + $p.HasExited + " pid=" + $p.Id)
Write-Output "--- fenetres du process ---"
[W2]::All() | Where-Object { $_ -like "$($p.Id)|*" } | ForEach-Object { Write-Output $_ }
Write-Output "--- titres BabiProgrammeur ---"
[W2]::All() | Where-Object { $_ -like "*BabiProgrammeur*" } | ForEach-Object { Write-Output $_ }
Stop-Process -Id $p.Id -Force

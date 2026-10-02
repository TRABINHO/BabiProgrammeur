# Capture la fenêtre de l'application BabiProgrammeur pendant qu'elle tourne.
#   powershell -ExecutionPolicy Bypass -File tests\screenshot.ps1 [-Name f.png] [-Demo]
param(
    [string]$Name = "cp_app.png",
    [string]$Tab = "",
    [switch]$Demo
)

$ErrorActionPreference = 'SilentlyContinue'
$root = Split-Path -Parent $PSScriptRoot

Add-Type @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public class Cap {
  public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lParam);
  [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder sb, int max);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int cmd);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  public struct RECT { public int Left, Top, Right, Bottom; }

  // Liste les fenêtres d'un processus : [visible, titre, handle]
  public static List<string> Windows(int pid) {
    var res = new List<string>();
    EnumWindows((h, l) => {
      int p; GetWindowThreadProcessId(h, out p);
      if (p != pid) return true;
      var sb = new StringBuilder(512);
      GetWindowText(h, sb, 512);
      res.Add(IsWindowVisible(h) + "|" + sb.ToString() + "|" + h.ToInt64());
      return true;
    }, IntPtr.Zero);
    return res;
  }
}
"@
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
# Sans cela Windows virtualise les coordonnées (écran 120 DPI) et la capture
# est décalée par rapport à la fenêtre réelle.
[Cap]::SetProcessDPIAware() | Out-Null

if ($Demo) { Remove-Item "$env:APPDATA\BabiProgrammeur\data.json" -Force; Remove-Item "$env:APPDATA\CodePulse\data.json" -Force }

$procArgs = @("main.py")
if ($Demo) { $procArgs += "--demo" }
if ($Tab) { $procArgs += @("--tab", $Tab) }
$logOut = Join-Path $env:TEMP "cp_app_stdout.txt"
$logErr = Join-Path $env:TEMP "cp_app_stderr.txt"
Remove-Item $logOut, $logErr -Force
$p = Start-Process -FilePath "python" -ArgumentList $procArgs -WorkingDirectory $root -PassThru `
    -RedirectStandardOutput $logOut -RedirectStandardError $logErr
Start-Sleep -Seconds 9
$p.Refresh()
if ($p.HasExited) {
    Write-Output "APPLICATION TERMINEE (code $($p.ExitCode))"
    Get-Content $logErr | Select-Object -Last 25
    exit 1
}

$app = [IntPtr]::Zero
foreach ($line in [Cap]::Windows($p.Id)) {
    $parts = $line.Split("|")
    $title = $parts[1]
    $handle = [IntPtr][long]$parts[2]
    if ($title -like "*BabiProgrammeur*") { $app = $handle }
    elseif ($title -like "*python*") { [Cap]::ShowWindow($handle, 6) | Out-Null }  # SW_MINIMIZE
}
Write-Output ("fenetre=0x{0:X}" -f $app)

[Cap]::SetWindowPos($app, [IntPtr]-1, 0, 0, 0, 0, 0x0013) | Out-Null
[Cap]::SetForegroundWindow($app) | Out-Null
Start-Sleep -Milliseconds 2000

$r = New-Object Cap+RECT
[Cap]::GetWindowRect($app, [ref]$r) | Out-Null
$w = $r.Right - $r.Left
$ht = $r.Bottom - $r.Top
Write-Output ("rect=" + $r.Left + "," + $r.Top + " " + $w + "x" + $ht)
$vs = [System.Windows.Forms.SystemInformation]::VirtualScreen
Write-Output ("virtual=" + $vs.X + "," + $vs.Y + " " + $vs.Width + "x" + $vs.Height)
if ($w -le 0 -or $ht -le 0) {
    Write-Output "fenetre introuvable ($w x $ht)"
    Stop-Process -Id $p.Id -Force
    exit 1
}
$bmp = New-Object System.Drawing.Bitmap $w, $ht
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size)
$out = Join-Path $env:TEMP $Name
$bmp.Save($out)
$g.Dispose(); $bmp.Dispose()
[Cap]::SetWindowPos($app, [IntPtr]-2, 0, 0, 0, 0, 0x0013) | Out-Null
Stop-Process -Id $p.Id -Force
Write-Output "$out ($w x $ht)"

$ErrorActionPreference='SilentlyContinue'
$root = Split-Path -Parent $PSScriptRoot
Add-Type @"
using System; using System.Collections.Generic; using System.Runtime.InteropServices; using System.Text;
public class D {
  public delegate bool EnumProc(IntPtr hWnd, IntPtr lParam);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr lParam);
  [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr hWnd, out int pid);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr hWnd, StringBuilder sb, int max);
  public struct RECT { public int Left, Top, Right, Bottom; }
  public static IntPtr Find(int pid, string must) {
    IntPtr f = IntPtr.Zero;
    EnumWindows((h, l) => {
      int p; GetWindowThreadProcessId(h, out p);
      if (p != pid) return true;
      var sb = new StringBuilder(512); GetWindowText(h, sb, 512);
      if (sb.ToString().IndexOf(must, StringComparison.OrdinalIgnoreCase) >= 0) { f = h; return false; }
      return true;
    }, IntPtr.Zero);
    return f;
  }
}
"@
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[D]::SetProcessDPIAware() | Out-Null

$p = Start-Process python -ArgumentList @('main.py','--demo') -WorkingDirectory $root -PassThru -RedirectStandardOutput "$env:TEMP\o.txt" -RedirectStandardError "$env:TEMP\e.txt"
Start-Sleep -Seconds 9
$h = [D]::Find($p.Id, "BabiProgrammeur")
$r = New-Object D+RECT
[D]::GetWindowRect($h, [ref]$r) | Out-Null
Write-Output ("rect=" + $r.Left + "," + $r.Top + " " + ($r.Right-$r.Left) + "x" + ($r.Bottom-$r.Top))
$vs = [System.Windows.Forms.SystemInformation]::VirtualScreen
Write-Output ("virtual=" + $vs.X + "," + $vs.Y + " " + $vs.Width + "x" + $vs.Height)
$bmp = New-Object System.Drawing.Bitmap $vs.Width, $vs.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($vs.X, $vs.Y, 0, 0, $bmp.Size)
$bmp.Save("$env:TEMP\cp_full.png")
$g.Dispose(); $bmp.Dispose()
Stop-Process -Id $p.Id -Force

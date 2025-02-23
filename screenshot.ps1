function Get-Screenshot {
  Add-Type -AssemblyName System.Windows.Forms
  Add-Type -AssemblyName System.Drawing

  $Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
  $Width  = $Screen.Width
  $Height = $Screen.Height
  $Left   = $Screen.Left
  $Top    = $Screen.Top

  $bitmap  = New-Object System.Drawing.Bitmap $Width, $Height
  $graphic = [System.Drawing.Graphics]::FromImage($bitmap)
  $graphic.CopyFromScreen($Left, $Top, 0, 0, $bitmap.Size)

  $bitmap.Save("C:\Users\ryans\OneDrive\Documents\aaSpring2025\openscad\screenshot.jpg")
  Write-Output "Screenshot saved to:"
  Write-Output C:\Users\ryans\OneDrive\Documents\aaSpring2025\openscad\screenshot.jpg
}


function Get-Window ($ProcessName) {
  Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Program {
  [DllImport("user32.dll")]
  [return: MarshalAs(UnmanagedType.Bool)]
  public static extern bool SetForegroundWindow(IntPtr hWnd);
}
"@



  $processes = Get-Process -Name "*${ProcessName}*"
  Write-Output $processes
  $process = $processes | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
  if ($process) {
      $hwnd = $process.MainWindowHandle
      [Program]::SetForegroundWindow($hwnd)
  } else {
      Write-Host "Program is not running or does not have a MainWindowHandle."
  }
}

Get-Window -ProcessName openscad
Start-Sleep -m 500
Get-Screenshot

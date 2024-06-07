Title: Using System XAML Islands in a MSIX-packaged .NET Framework app
Date: 2023-12-04 00:00  
Category: Cool Tricks  
Tags: xaml islands, wpf, uwp, C#, windows, windows 11, net framework, msix, very dangerous windows hack age 18 and up content
Slug: netfx-islands
Authors: Difegue  
HeroImage: images/wow.jpg  
Summary: MUX, WUX... more like FUX this shit eyy gotem

Here's a _"I want this to pop up in SEO results despite all the AI garbage flooding search results"_ article I wish I had on hand.  

[XAML Islands](https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/xaml-islands) is the catch-all term for the technologies that allow you to host WinRT/UWP user interface elements in apps built with other desktop frameworks, like WPF and al.  

Since nothing about modern Windows UI is simple, there are **two** versions of XAML Islands:  

  - one embedded into the OS/platform XAML ([`Windows.UI.Xaml.Hosting`](https://learn.microsoft.com/en-us/uwp/api/windows.ui.xaml.hosting?view=winrt-22621)),  
  - one included as part of the _Windows App SDK_. ([`Microsoft.UI.Xaml.Hosting`](https://learn.microsoft.com/en-us/windows/windows-app-sdk/api/winrt/microsoft.ui.xaml.hosting))  

This post will only talk about `Windows.UI.Xaml.Hosting`.  

The easiest way to use XAML Islands in a WPF (or Winforms) app remains the [Microsoft.Toolkit.Win32 package](https://github.com/CommunityToolkit/Microsoft.Toolkit.Win32) -- It's been archived as Microsoft wants you to use `Microsoft.UI.Xaml.Hosting`, but there's no convenient WPF integration for that just yet.  

Now, if like me you tend to read Microsoft documentation as gospel, you might think that this package won't work on [.NET Framework codebases](https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/xaml-islands#not-supported)...  
> XAML Islands are supported only in apps that target .NET Core 3.x  

But that's wrong! It is merely _unsupported_. The [package itself](https://www.nuget.org/packages/Microsoft.Toolkit.Wpf.UI.Controls) works perfectly fine on both `netcore3` and `netfx`<sup id="ref-1">[*](#note-1)</sup>.  
Well, not quite perfectly fine -- there are a number of pitfalls on .NET Framework I'll try to cover here.  

## Application Manifest 

The XAML islands toolchain in the Toolkit **needs** your app to have a [manifest](https://learn.microsoft.com/en-us/windows/win32/sbscs/application-manifests), as it will [inject](https://github.com/CommunityToolkit/Microsoft.Toolkit.Win32/issues/258#issuecomment-721421236) a `maxversiontested Id='10.0.18362.0'` attribute into it to ensure it works with XAML Islands<sup id="ref-2">[**](#note-2)</sup>.

You really don't need much in said manifest (and you can add the attribute yourself), here's a sample:  
```
<?xml version="1.0" encoding="utf-8"?>
<assembly manifestVersion="1.0" xmlns="urn:schemas-microsoft-com:asm.v1">
  <assemblyIdentity version="1.0.0.0" name="MyApplication.app"/>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <!-- UAC Manifest Options
             If you want to change the Windows User Account Control level replace the 
             requestedExecutionLevel node with one of the following.

        <requestedExecutionLevel  level="asInvoker" uiAccess="false" />
        <requestedExecutionLevel  level="requireAdministrator" uiAccess="false" />
        <requestedExecutionLevel  level="highestAvailable" uiAccess="false" />

            Specifying requestedExecutionLevel element will disable file and registry virtualization. 
            Remove this element if your application requires this virtualization for backwards
            compatibility.
        -->
        <requestedExecutionLevel level="asInvoker" uiAccess="false" />
      </requestedPrivileges>
    </security>
  </trustInfo>

  <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
    <application>
      <!-- A list of the Windows versions that this application has been tested on
           and is designed to work with. Uncomment the appropriate elements
           and Windows will automatically select the most compatible environment. -->

      <!-- Windows 10 -->
      <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}" />
	  <maxversiontested Id="10.0.18362" />

    </application>
  </compatibility>

  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <!-- Use PerMonitorV2, default to PerMonitor on systems where V2 isn't available. This order is required to use System XAML Islands correctly. -->
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2, PerMonitor</dpiAwareness>
    </windowsSettings>
  </application>

</assembly>
```

## MSIX Packaging  

If you're shipping your app in a MSIX/Appx package for Microsoft Store usage, you need to include the following files in your package:  

```
Microsoft.Toolkit.Wpf.UI.Controls.dll
Microsoft.Toolkit.Wpf.UI.XamlHost.dll
Microsoft.Toolkit.Win32.UI.XamlHost.dll
Microsoft.Toolkit.Win32.UI.XamlHost.winmd
Microsoft.Toolkit.Win32.UI.XamlHost.Managed.dll
```
Well, so far nothing out of the ordinary -- But the app might still **crash** once packaged, complaining about a Windows Runtime type missing. 
> Could not find Windows Runtime type Microsoft.Toolkit.Win32.UI.XamlHost.IXamlMetadataContainer  

Why would that be?  

There's an [obscure bug](https://github.com/dotnet/wpf/issues/1290#issuecomment-512944811) with MSIX packages where if you're including WinMDs (Windows Runtime metadata), they **must be at the root of the package**. Otherwise, they just.. won't be made available to your app.  
![wow](images/wow.jpg)  
I personally just use raw filemaps with `MakeAppx` instead of relying on Windows Application Packaging projects as it's frankly easier, but the github link above has csproj steps you can use:  

```
  <!-- Stomp the path to application executable.
    This task will copy the main exe to the appx root folder.
   -->
  <Target Name="_StompSourceProjectForWapProject" BeforeTargets="_ConvertItems">
    <ItemGroup>
      <!-- Stomp all "SourceProject" values for all incoming dependencies to flatten the package. -->
      <_TemporaryFilteredWapProjOutput Include="@(_FilteredNonWapProjProjectOutput)" />
      <_FilteredNonWapProjProjectOutput Remove="@(_TemporaryFilteredWapProjOutput)" />
      <_FilteredNonWapProjProjectOutput Include="@(_TemporaryFilteredWapProjOutput)">
      <!-- Blank the SourceProject here to vend all files into the root of the package. -->
      <SourceProject></SourceProject>
      </_FilteredNonWapProjProjectOutput>
    </ItemGroup>
  </Target>
```

And after all that mess... You should finally have your UWP controls!  

Was it worth it? Probably not, you can't even use Windows 11 styling/WinUI 2 unless you start dabbling in [Dynamic Dependencies.](https://learn.microsoft.com/en-us/windows/apps/desktop/modernize/framework-packages/use-the-dynamic-dependency-api)<sup id="ref-3">[***](#note-3)</sup>  

## Bonus round: MediaPlayerElement + AdaptiveMediaSource

This is a small extra thing that doesn't really warrant a separate post... One of the major reasons you'd want to use XAML Islands is for the UWP [MediaPlayerElement](https://learn.microsoft.com/en-us/uwp/api/windows.ui.xaml.controls.mediaplayerelement?view=winrt-22621) (the others being the Map or InkCanvas stuff).  

![MediaPlayerElement in its natural habitat](https://github.com/MicrosoftDocs/windows-dev-docs/raw/docs/hub/apps/design/controls/images/controls/mtc_double_video_inprod.png)  

The Toolkit package comes with a wrapper for MediaPlayerElement that allows you to simply set an URL as a `MediaSource`; But if you want to use an [AdaptiveMediaSource](https://learn.microsoft.com/en-us/samples/microsoft/windows-universal-samples/adaptivestreaming/) instead to customize bitrate selection or something else, it won't let you.  

In their infinite wisdom, the Toolkit devs thought they'd be helpful and add a [custom converter](https://github.com/CommunityToolkit/Microsoft.Toolkit.Win32/blob/9c1463e328a33168d0b0e7c7bea975838f35128f/Microsoft.Toolkit.Wpf.UI.Controls/MediaPlayerElement/MediaPlayerElement.cs#L61) to automatically map URLs to `MediaSource`s in XAML... Except that converter will [crash the app](https://github.com/CommunityToolkit/Microsoft.Toolkit.Win32/blob/9c1463e328a33168d0b0e7c7bea975838f35128f/Microsoft.Toolkit.Wpf.UI.Controls/MediaPlayerElement/MediaSourceConverter.cs#L25) if you use `AdaptiveMediaSource`, which doesn't have a `Uri` property.  

As it stands, the best solution I found is to duplicate the MediaPlayerElement control and just remove this binding at line 61. ¯\\\_(ツ)_/¯  

#  

<sup id="note-1">[\*](#ref-1) 
Aand it's broken in .NET 5 and above as those CLRs [don't support .winmds](https://github.com/dotnet/runtime/issues/35318) natively anymore... You can still hack it with cswinrt but it's probably not worth it tbh</sup>  
<sup id="note-2">[\*\*](#ref-2) which is frankly speaking a terrible idea?? why wouldn't you just document that developers need to add the attribute instead of bothering to do it yourself? Almost makes you think there's some conspiracy on the Microsoft side to document `app.manifest` files as little as humanly possible </sup>  
<sup id="note-3">[\*\*\*](#ref-3) which also has two different implementations i cant take this anymore </sup>  
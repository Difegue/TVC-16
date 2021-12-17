Title: Display a X509 Certificate with SFCertificatePanel on Xamarin.Mac
Date: 2021-12-17 00:00  
Category: Software  
Tags: macos, c#, xamarin, .net, certificate, sfcertificatepanel, x509certificate2ui
Slug: sfcertificate-mac-xamarin
Authors: Difegue  
HeroImage: images/certs/appkit-cert.png  
Summary: Nobody ever cares about Certificate UIs...but I do. (Or at least I had to)

Showing the details of a [X.509 certificate](https://en.wikipedia.org/wiki/X.509) on Windows is fairly simple through the [X509Certificate2UI](https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.x509certificates.x509certificate2ui?view=dotnet-plat-ext-6.0) class, which wraps the native Win32 certificate UI:  

![The Win32 certificate details window]({static}/images/certs/win32-cert.png)

Doing the same on macOS proves to be much less documented, but not that hard!  

# SFCertificatePanel

![A SFCertificatePanel.]({static}/images/certs/appkit-cert.png)

[SFCertificatePanel](https://developer.apple.com/documentation/securityinterface/sfcertificatepanel?language=objc) is the AppKit class that handles displaying Certificates and certificate chains.  

It's...not very well exposed but fairly easy to use:  

```
// Objective-C, show Modal
// trustCertificates is a NSArray of SecCertificate objects
[[SFCertificatePanel sharedCertificatePanel] runModalForCertificates:trustCertificates showGroup:YES];

// Swift, show Sheet in a parent window
DispatchQueue.main.async {
      let certData = //read certificate file
      let cert = SecCertificateCreateWithData(kCFAllocatorDefault, certData! as CFData)
      SFCertificatePanel.shared().beginSheet(for: self.view.window, modalDelegate: nil, didEnd: nil, contextInfo: nil, certificates: [cert!], showGroup: false)
    }
```

The Panel can show details for either a single [SecCertificate](https://developer.apple.com/documentation/security/seccertificateref?language=objc), an array of them symbolizing a Certificate chain, or a [SecTrust](https://developer.apple.com/documentation/security/sectrustref?language=objc) object.

# Usage from a Xamarin.Mac app

Sadly, Xamarin.Mac does not [wrap the SecurityInterface](https://github.com/xamarin/xamarin-macios/issues/4177) library that contains this class, so we have to dig a bit deeper to call on it.  

Using `objc_msgSend`, we can essentially [call Objective-C methods](http://jonathanpeppers.com/Blog/xamarin-ios-under-the-hood-calling-objective-c-from-csharp) on any class we want, including the unwrapped ones:  

```
:::csharp
public static class SecurityInterface
    {
        // https://developer.apple.com/documentation/securityinterface/sfcertificatepanel
        static Class _sfCertificatePanelClass = new Class("SFCertificatePanel");
        static Selector _sharedCertificatePanelSelector = new Selector("sharedCertificatePanel");
        static Selector _runModalForCertificatesSelector = new Selector("runModalForCertificates:showGroup:");
        static Selector _beginSheetForWindowSelector = new Selector("beginSheetForWindow:modalDelegate:didEndSelector:contextInfo:certificates:showGroup:");

        // Since we're not doing a full Xamarin binding project for SecurityInterface.framework,
        // We need to re-declare some of the ObjC messaging functions since they're normally hidden from us.
        // (http://jonathanpeppers.com/Blog/xamarin-ios-under-the-hood-calling-objective-c-from-csharp)
        [DllImport(Constants.ObjectiveCLibrary, EntryPoint = "objc_msgSend")]
        extern static IntPtr IntPtr_objc_msgSend(IntPtr receiver, IntPtr selector);
        [DllImport(Constants.ObjectiveCLibrary, EntryPoint = "objc_msgSend")]
        extern static global::System.nint nint_objc_msgSend_IntPtr_bool(IntPtr receiver, IntPtr selector, IntPtr arg1, bool arg2);
        [DllImport(Constants.ObjectiveCLibrary, EntryPoint = "objc_msgSend")]
        extern static void void_objc_msgSend_IntPtr_IntPtr_IntPtr_IntPtr_bool(IntPtr receiver, IntPtr selector, IntPtr arg1, IntPtr arg2, IntPtr arg3, IntPtr arg4, IntPtr arg5, bool arg6);


        // + (SFCertificatePanel *)sharedCertificatePanel;
        public static IntPtr GetSharedCertificatePanel() =>
            IntPtr_objc_msgSend(_sfCertificatePanelClass.Handle, _sharedCertificatePanelSelector.Handle);

        //- (NSInteger)runModalForCertificates:(NSArray *)certificates showGroup:(BOOL)showGroup;
        public static nint RunModalForCertificates(IntPtr certificatePanel, NSArray certificates, bool showGroup) =>
            nint_objc_msgSend_IntPtr_bool(certificatePanel, _runModalForCertificatesSelector.Handle, certificates.Handle, showGroup);

        // - (void)beginSheetForWindow:(NSWindow *)docWindow modalDelegate:(id)delegate didEndSelector:(SEL)didEndSelector contextInfo:(void *)contextInfo certificates:(NSArray *)certificates showGroup:(BOOL)showGroup;
        // delegate, didEndSelector and contextInfo are unmapped. (IntPtr.Zero)
        public static void BeginCertificateSheetForWindow(IntPtr certificatePanel, IntPtr windowHandle, NSArray certificates, bool showGroup) =>
            void_objc_msgSend_IntPtr_IntPtr_IntPtr_IntPtr_bool(certificatePanel, _beginSheetForWindowSelector.Handle, windowHandle,
                IntPtr.Zero, IntPtr.Zero, IntPtr.Zero, certificates.Handle, showGroup);
    }
```
(A full-on [Xamarin Binding Library](https://docs.microsoft.com/en-us/xamarin/cross-platform/macios/binding/?context=xamarin/mac) would obviously be cleaner than this, but it's not worth the effort considering we're not using all of SecurityInterface...)  

With those few methods on hand, we can easily invoke a SFCertificatePanel from .NET code:  

```
:::csharp
private void DisplayCertificate(X509Certificate2 certificate, IntPtr windowParent)
{
  using (var sc = new SecCertificate(certificate))
  {
      // Put the certificate in a NSArray for compliance with the API
      NSArray certificates = NSArray.FromNSObjects(sc);

      var certificatePanel = SecurityInterface.GetSharedCertificatePanel();

      if (windowParent == IntPtr.Zero)
          SecurityInterface.RunModalForCertificates(certificatePanel, certificates, true);
      else
      {
          SecurityInterface.BeginCertificateSheetForWindow(certificatePanel, windowParent, certificates, true);
      }
  }
}
```

And things just work! Although there are a few issues...  

## Mono and X509Certificate2 

Since we're still using a version of Xamarin that relies on [Mono]() instead of .NET 6, the X509Certificate2 class isn't fully implemented and won't show full certificate chains:  
![A lone, single certificate]({static}/images/certs/no-chain.png)  
This is troublesome if you want to show a certificate chain where some intermediates are not in the system keychain: it will show as untrusted...even though the full chain is valid!  

The easiest solution would be to move to .NET 6, but as that's not quite available yet, we have to bypass X509Certificate2 entirely and load the certificate using only macOS APIs:  

```
:::csharp
var pfx = [...] // class that contains both path to a .pfx certificate file and its password 
var options = new NSMutableDictionary
{
    [SecImportExport.Passphrase] = new NSString(pfx.Password),
    // ImportPkcs12 imports the given certificate to the Keychain by default.
    // Since we just want to check the certificate, we can avoid this behavior by setting ImportExportKeychain to nil.
    // (or an empty NSObject, since passing null isn't allowed here)
    [new NSString("kSecImportExportKeychain")] = new NSObject()
};

// Use SecImportExport to get SecCertificateRefs from the .pfx file
var status = SecImportExport.ImportPkcs12(NSData.FromFile(pfx.FilePath), options, out var outData);
if (status == SecStatusCode.Success)
{
    var certificateInfo = outData[0];

    // Get the chain as an array of SecCertificates
    var chain = certificateInfo["chain"] as NSArray;

    // Proceed as we did before
    var certificatePanel = SecurityInterface.GetSharedCertificatePanel();

    if (windowParent == IntPtr.Zero)
        SecurityInterface.RunModalForCertificates(certificatePanel, chain, true);
    else
    {
        SecurityInterface.BeginCertificateSheetForWindow(certificatePanel, windowParent, chain, true);
    }
}

```  

And then we get a full chain!  

![A certificate and his family 😊]({static}/images/certs/yes-chain.png)  

The first time, at least.

## Showing the panel multiple times

There seems to be a weird bug with the shared Certificate Panel on Big Sur where if you show it multiple times, the top part showing the certificate chain doesn't show anymore and stays blank. 😔   

To solve this, we have to **instantiate** the panel each time we want to show it.  
This requires a few more modifications to our static SecurityInterface class:  

```
:::csharp
/// <summary>
/// Instantiate a SFCertificatePanel object, wrapped in the Xamarin container.
/// We can't use sharedCertificatePanel: since it has display issues if we show a certificate chain multiple times.
/// 
/// From the Apple documentation (https://developer.apple.com/documentation/securityinterface/sfcertificatepanel/1543245-shared): 
/// If your application can display multiple certificate panels or sheets at once, you must allocate separate object instances
/// (using the alloc class method inherited from NSObject) and initialize them (using the init() instance method,
/// also inherited from NSObject) instead of using this class method.
/// </summary>
/// <returns></returns>
public static NSObject CreateCertificatePanel() => Runtime.GetNSObject(
    IntPtr_objc_msgSend(IntPtr_objc_msgSend(_sfCertificatePanelClass.Handle, Selector.GetHandle("alloc")), Selector.GetHandle("init")));

//- (NSInteger)runModalForCertificates:(NSArray *)certificates showGroup:(BOOL)showGroup;
public static nint RunModalForCertificates(NSObject certificatePanel, NSArray certificates, bool showGroup) =>
    nint_objc_msgSend_IntPtr_bool(certificatePanel.Handle, _runModalForCertificatesSelector.Handle, certificates.Handle, showGroup);

// - (void)beginSheetForWindow:(NSWindow *)docWindow modalDelegate:(id)delegate didEndSelector:(SEL)didEndSelector contextInfo:(void *)contextInfo certificates:(NSArray *)certificates showGroup:(BOOL)showGroup;
// delegate, didEndSelector and contextInfo are unmapped. (IntPtr.Zero)
public static void BeginCertificateSheetForWindow(NSObject certificatePanel, IntPtr windowHandle, NSArray certificates, bool showGroup) =>
    void_objc_msgSend_IntPtr_IntPtr_IntPtr_IntPtr_bool(certificatePanel.Handle, _beginSheetForWindowSelector.Handle, windowHandle,
        IntPtr.Zero, IntPtr.Zero, IntPtr.Zero, certificates.Handle, showGroup);
```
In this block of code, we now instantiate a SFCertificatePanel using the regular objc alloc/init selectors, and wrap it into a Xamarin NSObject to make the code _slightly_ clearer. (although it doesn't help that much...)  

Using the new methods, we can now show the certificate panel multiple times without any issues:  

```
:::csharp
// Make sure to deinitialize the created CertificatePanel.
// We use xamarin's built-in dispose for this, which calls the objc "release" selector on its own.
using (var certificatePanel = SecurityInterface.CreateCertificatePanel())
{
    if (hwndParent == IntPtr.Zero)
        SecurityInterface.RunModalForCertificates(certificatePanel, chain, true);
    else
        SecurityInterface.BeginCertificateSheetForWindow(certificatePanel, windowParent, chain, true);
        if (hwndParent == IntPtr.Zero)
            SecurityInterface.RunModalForCertificates(certificatePanel, chain, true);
        else
            SecurityInterface.BeginCertificateSheetForWindow(certificatePanel, windowParent, chain, true);
}
```

# Closing thoughts  

I added syntax highlighting to the blog after writing this article since all the giant blobs of `objc_msgSend` are already unreadable enough 😅  

It was simple enough:  
```
:::bash
pygmentize -S perldoc -f html -a .highlight > theme/static/css/pygment.css
```  

Followed by adding this new CSS into the headers of the template.  

Title: An approach to data binding with .NET in an iOS app
Date: 2024-03-31 00:00  
Category: Cool Tricks  
Tags: xamarin, dotnet, c#, macos, ios, mvvm, data binding, cocoa bindings, monkey trick, key-value coding
Slug: xamarin-binding
Authors: Difegue  
HeroImage: images/stylophone/v2-uikit2.jpg
Summary: Key-Value Observer on Timeless Temple

It's been a while since my last [Xamarinpost](/xamarin-resx.html), but since I just released a [Stylophone update](https://github.com/Difegue/Stylophone/releases/tag/2.6.2), I'm in the mood to wax .NET again!  

Stylophone, as a Windows-first app, was built upon the principle of [MVVM](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm), which as a quick refresher:  
- Isolates model and view code entirely  
- Uses "_ViewModel_" classes as glue between the two, exposing the model's data as properties the view picks up through **data binding**.  

One of the key advantages of this pattern is, as the MS documentation says:  
> The app UI can be redesigned without touching the view model and model code [...]. Therefore, a new version of the view should work with the existing view model.  

So if you can easily have multiple sets of UI with the same base... You should be able to have the same code for multiple platforms that run .NET, and only **remake the view** for each platform! That's what [Stylophone does](/stylophone-25).  

<img width="420" style="margin:0" src="{static}/images/stylophone/v25-ipad.jpg"/> <img width="420" style="margin:0" src="{static}/images/stylophone/v25-win.jpg"/>  

Data-binding comes for free on Windows thanks to XAML, but what about iOS?  
Can we bind our .NET code to native UIKit views so they just update automagically?  

As it turns out, yes! There **is** a native data-binding mechanism for Apple platforms!  
Well, kinda.  

### Cocoa Bindings  

[Cocoa Bindings](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CocoaBindings/Concepts/WhatAreBindings.html) is a piece of AppKit tech that allows you to do data-binding on Mac apps out of the box. It just works!™️  
![Cocoa Bindings](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CocoaBindings/art/sliderbindings_2x.png)  
Apple's flavor of data-binding relies on two elements:  

- *Key-Value Coding* (KVC), which gives access to an object’s property with a specified name (a **Keypath**)
- *Key-Value Observing* (KVO), which allows an object to receive notifications of changes to values in other objects  

For dotnetheads, this is basically _C# properties_ and `INotifyPropertyChanged`.  

That all sounds nice and easy to plug into..except Cocoa Bindings aren't available on UIKit/iOS.  
The components are, however! 

### Reimplementing Cocoa Bindings

Since UIKit still supports key-value coding, we can just create our own Bindings.  
Creating a .NET databinder for iOS basically means doing two things:  

- Keep track of `PropertyChanged` events on the C#/ViewModel side and update your views through **KVC**
- Keep track of view changes through **KVO** and update your properties on the ViewModel  

First, let's create our own `Binding` class that would act as universal glue code between C# and native objects.    
Xamarin's automatic type conversion is very useful here, so we don't need to write a lot of code at all:  

~~~csharp
    public class Binding
    {
        // Native UIKit object, and path to its KVC property
        public NSObject Object { get; set; }
        public NSString Keypath { get; set; }
        
        // C# property, this uses reflection
        public PropertyInfo Property { get; set; }

        /// Update our C# property with information from Key-Value Observing
        /// Since KVO cannot give you type information, you must provide the type yourself.
        public void UpdateProperty<T>(INotifyPropertyChanged targeTViewModel, NSObservedChange change)
        {
            var nativeValue = change.NewValue;

            object value = typeof(T) switch
            {
                // Cast to .NET types 
                Type t when t == typeof(int) => ((NSNumber)nativeValue).Int32Value,
                Type t when t == typeof(long) => ((NSNumber)nativeValue).Int64Value,
                Type t when t == typeof(double) => ((NSNumber)nativeValue).DoubleValue,
                Type t when t == typeof(bool) => ((NSNumber)nativeValue).BoolValue,
                Type t when t == typeof(string) => ((NSString)nativeValue).ToString(),
                _ => throw; // A wrapper class should be used in that case 
            };

            // Set the value on our viewmodel
            Property.SetValue(targeTViewModel, value);
        }

        /// Update the NSObject's value at the specified keypath with the property.
        public void UpdateNSObject(object value)
        {
            // Box the value into a native UIKit type
            // (If binding to more complex types than int/bool/strings, this will fail! A wrapper class should be used in that case)
            var nativeValue = NSObject.FromObject(value);

            // KVC operations need to run on the main thread
            UIApplication.SharedApplication.BeginInvokeOnMainThread(() =>
            {
                // https://developer.apple.com/documentation/objectivec/nsobject/1418139-setvalue?language=objc
                Object.SetValueForKeyPath(nativeValue, Keypath);
            });
        }

        
    };

~~~  

Then, our `PropertyBinder` can just create instances of this object for each property you want to bind, and listen to notifications from both sides:  

~~~csharp
    public class PropertyBinder<TViewModel>: IDisposable where TViewModel : INotifyPropertyChanged
    {
        // Per-property name bindings
        private readonly Dictionary<string, IList<Binding>> _bindings = new();
        // Per-property name 
        private readonly Dictionary<string, IDisposable> _observers = new();
        private TViewModel _observableObject;

        public PropertyBinder(TViewModel viewModel)
        {
            _observableObject = viewModel;
            // Listen to C# property changes
            _observableObject.PropertyChanged += OnObservablePropertyChanged;
        }
        
        public void Dispose()
        {
            if (_observableObject != null)
                _observableObject.PropertyChanged -= OnObservablePropertyChanged;

            // Dispose our observers
            foreach (IDisposable observer in _observers.Values)
                observer.Dispose();
        }

        // Bind a NSObject's keypath to a property of our observableObject
        public void Bind<T>(NSObject obj, string keypath, string property, bool isTwoWay = false)
            => Bind<T>(obj, new NSString(keypath), property, isTwoWay);

        private void OnObservablePropertyChanged(object sender, PropertyChangedEventArgs e)
        {
            var properties = new List<string>();

            // The PropertyChanged event can indicate all properties on the object have changed by using either null or String.Empty as
            // the property name in the PropertyChangedEventArgs.
            if (string.IsNullOrEmpty(e.PropertyName))
            {
                properties.AddRange(_bindings.Keys);
            }
            else if (_bindings.ContainsKey(e.PropertyName)) // Only one property has changed
            {
                properties.Add(e.PropertyName);
            }

            foreach (var property in properties)
            {
                var bindings = _bindings.GetValueOrDefault(property);
                foreach (var binding in bindings) // Update all bindings for this property
                    binding.UpdateNSObject(binding.Property.GetValue(_observableObject));
            }
        }

        private void Bind<T>(NSObject obj, NSString keypath, string property, bool isTwoWay = false)
        {
            var propertyInfo = GetProperty(property);
            var propertyValue = (T)propertyInfo.GetValue(_observableObject);

            // Create C#/UIKit binding and add it to the list to keep track of it
            var binding =
                new Binding { Object = obj, Keypath = keypath, Property = propertyInfo };

            if (_bindings.ContainsKey(property))
                _bindings.GetValueOrDefault(property).Add(binding);
            else
                _bindings.Add(property, new List<Binding>(new[] { binding }));

            // Set the initial value 
            binding.UpdateNSObject(propertyValue);

            if (isTwoWay)
            {
                // Create an Observer with KVO to keep track of UIKit-side changes
                // https://developer.apple.com/documentation/objectivec/nsobject/1412787-addobserver  
                var observer = obj.AddObserver(keypath, NSKeyValueObservingOptions.OldNew,
                    (c) => binding.UpdateProperty<T>(_observableObject, c));
                //      ^ Xamarin conveniently provides a version of this API call that  
                // takes a .NET event, so we can directly invoke our Binding object's Update.
                _observers.Add(obj.Handle.ToString() + "-" + keypath, observer);
            }
        }

        private PropertyInfo GetProperty(string propertyName)
        {
            // Small optimization to avoid calling reflection every time
            if (_bindings.ContainsKey(propertyName))
                return _bindings[propertyName].First().Property;

            var propertyInfo = typeof(TViewModel).GetProperty(propertyName);
            return propertyInfo ?? throw new ArgumentException($"Property {propertyName} not found on observable object {typeof(TViewModel).Name}");
        }

    }
~~~

And that's it!  
Usage is then as simple as creating a PropertyBinder from your view code:  

~~~csharp
public RandomViewModel ViewModel = new() {Name = ""}; 
public UILabel NameLabel = new();
public PropertyBinder<PlaylistViewModel> Binder => new(ViewModel);

public override void AwakeFromNib()
{
    base.AwakeFromNib();
    // Bind keypath "text" of UILabel to the Name property of our viewmodel
    Binder.Bind<string>(NameLabel, "text", nameof(ViewModel.Name));
}
~~~

### wait fuck this is iOS

One final gotcha is that for KVO to work, aka for [AddObserver](https://developer.apple.com/documentation/objectivec/nsobject/1412787-addobserver?language=objc) to correctly create Observers and send notifications, your native UI controls must be **KVO-compliant**.  

This is a funny Apple word to mean that the controls have to send notifications when their properties change - You can kind of think of it like DependencyProperties in XAML? It's a bit different though.  
According to [Apple documentation](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVOBasics.html):  
> Not all classes are KVO-compliant for all properties. [...] Typically properties in Apple-supplied frameworks are only KVO-compliant if they are documented as such.  

Basically, this means that since iOS didn't have Cocoa Bindings, they didn't give a single shit and most UIKit controls [will **not** work with KVO](https://stackoverflow.com/questions/6114261/how-reliable-is-kvo-with-uikit).  
So for Two-Way bindings, controls like `UISwitch` won't notify our `Binding` class when the user clicks on them! _Doushio?_  

Well, the easiest solution is basically to do Apple's job in their place, and subclass the UIKit controls you need to _make_ them comply.  
Which is [very easy](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/KeyValueObserving/Articles/KVOCompliance.html#//apple_ref/doc/uid/20002178-BAJEAIEE) as long as you only need a few properties:  
~~~csharp
[Register(nameof(KvoUISwitch))]
public class KvoUISwitch : UISwitch
{

    public KvoUISwitch(IntPtr handle) : base(handle)
    {
    }

    void ReleaseDesignerOutlets()
    {
    }

    public override void AwakeFromNib()
    {
        base.AwakeFromNib();

        // This will trigger when the switch value changes
        AddTarget(NotifyChange, UIControlEvent.ValueChanged);
    }

    private void NotifyChange(object sender, EventArgs e)
    {
        // low-budget kvo compliance
        WillChangeValue("on");
        DidChangeValue("on");
    }
}
~~~

There would be more complex things to add here (`ICommand` support, Managed object wrapping in bindings, Converters aka `NSValueTransformers` on the UIKit side), but I invite you to just peek at the [Stylophone source](https://github.com/Difegue/Stylophone/blob/dev/Sources/Stylophone.iOS/Helpers/PropertyBinder.cs) if you're interested.  
Have a nice day!  


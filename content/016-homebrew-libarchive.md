Title: Using macOS' bundled libarchive in a Homebrew formula
Date: 2020-05-25 00:00  
Category: Cool Tricks  
Tags: mac, macos, homebrew, libarchive, headers, apple
Slug: homebrew-libarchive
Authors: Difegue  
HeroImage: images/lrr-survey/survey2-image.jpg  
Summary: Apple has made me suffer plenty of times.

The LANraragi [Homebrew Port](https://formulae.brew.sh/formula/lanraragi) was recently merged into the core repository, making access to the world's only(_and therefore best_) Perl manga manager easy to all Macs.  

Getting the port to the acceptable level of standards for the core repository wasn't easy and needed one cool trick.  

# The libarchive conundrum  

LRR depends on the well-known [libarchive](https://www.libarchive.org/) project to handle archives.  
It's so well-known that Apple themselves use and bundle it in releases of macOS.  

Homebrew tries to be a good citizen by not installing dependencies which are already bundled by macOS if possible.  
This makes sense! No need having `libarchive` in triplicate if the system version does the job.  

Auditing the Homebrew formula henceforth gives you the following error:  
```bash
Dependency 'libarchive' is provided by macOS; please replace 'depends_on' with 'uses_from_macos'.
```  

So the Homebrew formula for LRR should `uses_from_macos "libarchive"`. Sounds easy! Except not.  

In their infinite wisdom, Apple made the decision that their libarchive should be [private API.](https://stackoverflow.com/a/3167763)  
As such, they only include a **compiled** version of libarchive, without the function headers.  

This would be fine if I was shipping precompiled executables that could call this compiled libarchive directly, but for better or worse, this is Perl! 🐫  

The way I use the lib is through a pair of [XS Modules](https://en.wikipedia.org/wiki/XS_%28Perl%29), which are basically C programs compiled on the user's machine when the module is installed.  
![wish I had an archive.h]({static}/images/libarchivexs.png)  
And so, we're hosed. Without the headers, the modules can't compile, making the Homebrew formula impossible to build on a stock Mac.  

This makes Homebrew's order a tall one:  
### "Use the bundled libarchive, except you can't compile anything that relies on it."  

# Sideloading headers  

The easiest solution here is providing the libarchive headers ourselves.  
Apple's version might be modified in some fashion from the original source code, so it's better to grab the headers directly [from them:](https://opensource.apple.com/source/libarchive/)  

```ruby
# libarchive headers from macOS 10.15 source
  resource "libarchive-headers-10.15" do
    url "https://opensource.apple.com/tarballs/libarchive/libarchive-72.11.2.tar.gz"
    sha256 "655b9270db794ba0b27052fd37b1750514b06769213656ab81e30727322e401f"
  end
```
(And you probably get nerd cred for jamming apple.com as a dependency in your formula. 😎)  

Homebrew decompresses resource tarballs on its own, so all we have to do to use the headers is move them in a custom `include` folder in our install:  

```ruby
  resource("libarchive-headers-10.15").stage do
    (libexec/"include").install "libarchive/libarchive/archive.h"
    (libexec/"include").install "libarchive/libarchive/archive_entry.h"
  end
```

And just add said folder using good ol' [CFLAGS](https://en.wikipedia.org/wiki/CFLAGS), so that the Perl Modules will automatically pick up the folder when compiling the XS scripts.  
```ruby
ENV["CFLAGS"] = "-I"+libexec/"include"
```  
`libexec` is automatically mapped by brew to a directory like `/usr/local/Cellar/foo/0.1/libexec`.  
And we're done!  

![oh no]({static}/images/brew-fail.png)  
![YOU GAIN CPAN]({static}/images/bullshit.jpg)

# Fixing the CPAN modules

Astute observers have probably noticed the error in the previous screenshot:  
The `cc` command called to compile the XS script does not include the `libexec` folder as an include. Why?  
Some background first.  

There exist a variety of ways to handle building/installing a CPAN module in Perl, and this article [wouldn't](https://metacpan.org/pod/Module::Install) be [enough](https://metacpan.org/pod/Module::Build) to [talk](https://metacpan.org/pod/Dist::Zilla) about [all of them](https://metacpan.org/pod/ExtUtils::MakeMaker).  

As said earlier, I use two XS Modules that both consume libarchive:  

* `Archive::Extract::Libarchive` (✅ builds fine with the new CFLAGS)
* `Archive::Peek::Libarchive` (❌ doesn't work yet)

You'd think that with such similar namespaces, both would use the same installer... Wrong! 😱  
Peek uses `ExtUtils::MakeMaker`, and Extract uses `Module::Build`.  

So let's focus on MakeMaker for a bit.  
You basically use it by writing a Perl-style Makefile, `Makefile.PL`, which when interpreted by Perl will spit out a regular Makefile to use with your regular make/make install combo.  

When building this Makefile, MakeMaker will **not** take into account your custom CFLAGS environment variable, instead opting to use the one that was used [when your version of Perl was built.](http://coding.derkeiler.com/Archive/Perl/comp.lang.perl.misc/2005-11/msg01613.html)  
In our case, the Perl we use comes from homebrew, and is built with esoteric include paths such as `/usr/local/Cellar/perl/5.30.2_1/lib/perl5/5.20.2/darwin-thread-multi-2level/CORE`. The horror.  

Now of course, Makefile.PL writers can add extra include paths, and our failing module certainly [does so](https://metacpan.org/source/REHSACK/Archive-Peek-Libarchive-0.38/Makefile.PL#L95), using another package called Config::AutoConf.  
Said module's documentation is a bit [empty](https://metacpan.org/pod/Config::AutoConf#_get_extra_compiler_flags) as to how it figures out the extra compiler flags, and this rabbit hole has gone on long enough, so let's just **patch the Makefile directly in Homebrew.**  

```ruby
resource("Archive::Peek::Libarchive").stage do
      inreplace "Makefile.PL" do |s|
        s.gsub! "$autoconf->_get_extra_compiler_flags", "$autoconf->_get_extra_compiler_flags .$ENV{CFLAGS}"
      end
      [...]
end
```

By adding the environment variable ourselves, the cumbersome module finally builds, and we're out of Perl module building hell.  

![took me three releases to get a working homebrew version]({static}/images/over.jpg)  

# Spare thoughts

I use the 10.15 headers from Apple, as they're the only ones that actually include all the functions used by LANraragi.  
This of course means that some functions are not available for both High Sierra and Mojave.  
Luckily all this stuff fails rather gracefully, with no stability issues.  

LRR is the [only formula](https://github.com/Homebrew/homebrew-core/search?q=uses_from_macos+%22libarchive%22&unscoped_q=uses_from_macos+%22libarchive%22) in homebrew/core using this trick with libarchive.  
The other are **weaksauce**, using a duplicate version instead. Plebeians!  

Jokes aside, it is a bit weird for the homebrew audit bot to consider libarchive to be bundled by the OS, where it is clearly unusable out of the box for something as simple as a `make` scenario. 😐  

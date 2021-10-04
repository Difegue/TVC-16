Title: Publishing MpcNET on NuGet.org (feat. Github Actions)
Date: 2021-10-04 00:00  
Category: Software  
Tags: mpd, c#, nuget, .net, music, stylophone, github actions
Slug: mpcnet-nuget
Authors: Difegue  
HeroImage: images/packages.png  
Summary: Timing both a visual refresh and a major refactoring in one? Don't mind if I do.  

While building [Stylophone](./stylophone.html), I based my initial work on the [LibMpc.net](https://github.com/glucaci/MpcNET) library, which I forked and improved with support for:  

* MPD Command Lists
* Binary Responses for `albumart` commands
* Various other commands that weren't implemented

This put it a bit above existing offerings (well except [libmpdclient](https://musicpd.org/libs/libmpdclient/) but that's not managed code), so I always wanted to release said fork as a standalone NuGet package.  
And well, [here we are!](https://www.nuget.org/packages/MpcNET/)  

This package auto-builds and auto-uploads through GitHub Actions, so hopefully I won't have to do too much maintenance. ✌️  

# GitHub Actions Workflow

Generating the NuGet package itself is pretty easy: Just build and `dotnet pack`!  
To automatically generate different version numbers for each commit, I've used the awesome [MinVer](https://github.com/adamralph/minver) NuGet package.  
While it requires you to work with Git tags, I already do that for my release workflow, so it's 🆒!  

NuGet automatically treats packages that have a prerelease string as [pre-versions](https://docs.microsoft.com/en-us/nuget/create-packages/prerelease-packages), but I didn't want to litter the NuGet repo with a package build for every commit...

So I'm going to litter* [GitHub Packages](https://github.com/Difegue/MpcNET/packages) instead!  

![hee ho here we go]({static}/images/packages.png)  

GH Packages pairs exceptionally well with Actions, since you can just use the provided `GITHUB_TOKEN` for everything:  
````yaml
name: Build and Test MpcNET

on:
  push:
    branches: [ dev ]

jobs:

  build:
    runs-on: windows-latest  

    env:
      Solution_Name: MpcNET    
      Configuration: Release     

    steps:
    - name: Checkout
      uses: actions/checkout@v2
      with:
        fetch-depth: 0

    # Add MSBuild to the PATH: https://github.com/microsoft/setup-msbuild
    - name: Setup MSBuild.exe
      uses: microsoft/setup-msbuild@v1.0.2

    # Build package and upload to github packages
    - name: Build package
      working-directory: ./Sources
      run: |
        dotnet nuget add source --username Difegue --password ${{ secrets.GITHUB_TOKEN }} --store-password-in-clear-text --name github "https://nuget.pkg.github.com/Difegue/index.json"
        dotnet build $env:Solution_Name --configuration $env:Configuration
        dotnet pack --configuration $env:Configuration -o ./ 
        dotnet nuget push *.nupkg  --api-key ${{ secrets.GITHUB_TOKEN }} --source "github" --skip-duplicate
````

For release packages, the recipe is essentially the same, except even simpler since we don't need to add GitHub as a source (We do need to add a nuget.org [API Key](https://www.nuget.org/account/apikeys) to our repo secrets however):  

````yaml
name: New Version Release

on: 
  release:
    types: [published]

jobs:

  build:
    runs-on: windows-latest  

    env:
      Solution_Name: MpcNET    
      Configuration: Release     

    steps:
    - name: Checkout
      uses: actions/checkout@v2
      with:
        fetch-depth: 0

    # Add MSBuild to the PATH: https://github.com/microsoft/setup-msbuild
    - name: Setup MSBuild.exe
      uses: microsoft/setup-msbuild@v1.0.2

    # Build package and upload to nuget.org
    - name: Build package
      working-directory: ./Sources
      run: |
        dotnet build $env:Solution_Name --configuration $env:Configuration
        dotnet pack --configuration $env:Configuration -o ./
        dotnet nuget push *.nupkg  --api-key ${{ secrets.NUGET_API }} --source "nuget.org"

````

\* I'm probably going to have to add the [Delete Package Versions](https://github.com/marketplace/actions/delete-package-versions) action to the mix at some point to avoid overloading GH's storage space. 😥 We'll see how popular the lib gets on its own. 😗  

# Extra Links

See here for a more detailed walkthrough of NuGet builds on Actions:  
[https://acraven.medium.com/a-nuget-package-workflow-using-github-actions-7da8c6557863](https://acraven.medium.com/a-nuget-package-workflow-using-github-actions-7da8c6557863)  

And here for explanations on MinVer: [https://rehansaeed.com/the-easiest-way-to-version-nuget-packages/](https://rehansaeed.com/the-easiest-way-to-version-nuget-packages/)  
workflow "Build TVC-16 to gh-pages branch" {
  on = "push"
  resolves = ["Push to gh-pages"]
}

action "Build TVC-16" {
  uses = "./.github/action-pelican"
}

action "Push to gh-pages" {
  uses = "JasonEtco/push-to-gh-pages@2259c84d9e1f489f4a416053ab69beae72b0492f"
  needs = ["Build TVC-16"]
  args = "output"
  secrets = ["GITHUB_TOKEN"]
}

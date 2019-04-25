FROM  vorakl/alpine-pelican:latest

LABEL "name"="tvc16-build"
LABEL "maintainer"="Difegue <sugoi@cock.li>"
LABEL "version"="0.0.1"

LABEL "com.github.actions.name"="Build TVC-16"
LABEL "com.github.actions.description"="Runs pelican to build master branch and force-pushes result to output branch"
LABEL "com.github.actions.icon"="eye"
LABEL "com.github.actions.color"="purple"

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
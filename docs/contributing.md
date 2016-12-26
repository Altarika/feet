# Contributing
Feet is open source. If you would like to contribute, you can do so in the following ways:

---

## Methodology

1. Add issues or bugs to the bug tracker: [https://github.com/altarika/feet/issues](https://github.com/altarika/feet/issues)
2. Work on a card on the dev board: [https://waffle.io/altarika/feet](https://waffle.io/altarika/feet)
3. Create a pull request in Github: [https://github.com/altarika/feet/pulls](https://github.com/altarika/feet/pulls)

The repository is set up in a typical production/release/development cycle as described in _[A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/)_. 

1. Select a card from the [dev board](https://waffle.io/altarika/feet) - preferably one that is "ready" then move it to "in-progress".

2. Create a branch off of develop called "feature-[feature name]", work and commit into that branch.

        $ git checkout -b feature-myfeature develop

3. Once you are done working (and everything is tested), push your branch and launch a Pull Request (PR). Make sure you have rebased your branch on the latest version of develop branch.


## Code quality

Use Flake8.

## Continuous Integration

TravisCI configuration.

## Maintainers

- Romary Dupuis: [@romaryd](https://github.com/romaryd/)

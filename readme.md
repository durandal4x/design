An [Obsidian](http://obsidian.md) vault we use to track meetings and design decisions for the project.

Design discussions and decisions should be performed using the [github project](https://github.com/orgs/durandal4x/projects/2), issue and Pull Request system.



# Design doc instructions

> [!feedback]
> These instructions were written by a programmer but are intended to be useful to non-programmers. Feedback and improvements to them are **very** welcome.

**0 - If this is your first time**
- [Install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 
- Create an account on [github](https://github.com)
- [Install the `gh` tool](https://github.com/cli/cli/blob/trunk/docs/install_linux.md) 
- `gh auth login` to authenticate
	- Optionally test the `gh` tool with `gh api /octocat`
- Fork the [Durandal4x design repo](https://github.com/durandal4x/design) to your github
- Clone your repo locally
	- Something like `git clone <your repo url>`
- Add the Durandal4x repo as a remote
	- `git remote add durandal git@github.com:durandal4x/design.git`

**1 - Create issue on Github**
- Create an issue in the [design repo](https://github.com/durandal4x/design/issues)
- Wait for the discussion to conclude

**2 - Update your local copy and create a branch**
```sh
git switch main
git pull durandal main
git switch -c {{branch name}}
```

**3 - Write your design doc**
- Create a new file in the `design docs` folder of this vault, ideally using the template (shortcut: Alt + N, select "design doc")
- Title the document accordingly
- Set the github issue number in the properties field based on the URL on github
- Write a first draft of the document

**4 - Create the comments file**
- Run the `scripts/get_comments.py` script with the issue number
	- e.g. `python3 scripts/get_comments.py 123`

**5 - Create the Pull request**
```sh
git add .
git commit -m "First draft of design doc"
git push origin {{branch name}}
```
- This will output something telling you how to create a new pull request, alternately you can go to the [github PR page](https://github.com/durandal4x/design/compare) and it will have an interface to do this.

**6 - PR cycle**
- Call for feedback on the PR (on the discord)
- Comments will be left
- Address the comments
- Repeat the first part of this stage

**7 - Merge**
- Once the doc is approved it will be merged
- Congratulations, you've officially contributed to Durandal4x!
